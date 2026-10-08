"""Mocked provider-contract tests; NO local model, network or PC hardware needed."""
from dataclasses import asdict, FrozenInstanceError
from io import BytesIO
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch
from urllib.error import URLError

from PIL import Image

from brody_world_physique.jarvis_vision_v0 import (
    DEFAULT_ENDPOINT,
    VisionDescriptionCandidateV0,
    _local_endpoint,
    describe_image,
    main,
)


class LocalVisionAdapterTests(TestCase):
    def setUp(self):
        work = TemporaryDirectory()
        self.addCleanup(work.cleanup)
        self.root = Path(work.name)
        self.image = self.root / "reference.png"
        Image.new("RGBA", (180, 70), (120, 80, 40, 200)).save(self.image)
        self.calls = []

    def _mock_provider(self, answer="Objet visible, couleur brune. Contexte inconnu."):
        outer = self

        class FakeOpener:
            def open(self, request, timeout):
                outer.calls.append((request, timeout))
                return BytesIO(json.dumps({"choices": [{"message": {"content": answer}}]}).encode())

        return patch(
            "brody_world_physique.jarvis_vision_v0.build_opener",
            return_value=FakeOpener(),
        )

    def test_actual_image_bytes_sent_in_jarvis_compatible_payload(self):
        with self._mock_provider():
            receipt = describe_image(self.image, prompt="Quels objets vois-tu ?")
        self.assertIsInstance(receipt, VisionDescriptionCandidateV0)
        request, timeout = self.calls[0]
        self.assertEqual(timeout, 120)
        self.assertEqual(request.full_url, DEFAULT_ENDPOINT)
        packet = json.loads(request.data.decode("utf-8"))
        self.assertEqual(packet["model"], "Qwen2.5-VL-3B-Instruct")
        self.assertEqual(packet["stream"], False)
        self.assertEqual(packet["messages"][1]["content"][0]["text"], "Quels objets vois-tu ?")
        data_url = packet["messages"][1]["content"][1]["image_url"]["url"]
        self.assertTrue(data_url.startswith("data:image/jpeg;base64,"))
        import base64
        with Image.open(BytesIO(base64.b64decode(data_url.split(",", 1)[1]))) as sent:
            self.assertEqual(sent.size, (180, 70))
            self.assertEqual(sent.format, "JPEG")
        self.assertEqual(receipt.provider, "JARVIS_LOCAL_QWEN_VL")
        self.assertEqual(receipt.observation_status, "MODEL_DESCRIPTION_UNVERIFIED")
        self.assertFalse(receipt.semantics_verified)
        self.assertFalse(receipt.real_image_observation)
        self.assertFalse(receipt.memory_write_allowed)
        self.assertFalse(receipt.auto_promotion_allowed)
        self.assertFalse(receipt.allowed_to_act)
        self.assertFalse(receipt.kernel_mutation)
        self.assertEqual(receipt.decision_authority, "KX108_ONLY")
        self.assertEqual(receipt.source_kind, "USER_IMAGE_FILE")
        self.assertEqual(len(receipt.source_sha256), 64)
        self.assertEqual(len(receipt.model_input_sha256), 64)
        self.assertNotEqual(receipt.source_sha256, receipt.model_input_sha256)

    def test_generated_file_cannot_be_labeled_real_observation(self):
        with self._mock_provider("Un objet dessiné."):
            receipt = describe_image(self.image, source_kind="GENERATED_ARTIFACT")
        self.assertEqual(receipt.source_kind, "GENERATED_ARTIFACT")
        self.assertFalse(receipt.real_image_observation)
        self.assertEqual(receipt.observation_status, "MODEL_DESCRIPTION_UNVERIFIED")

    def test_resize_and_source_hash_are_distinct(self):
        with self._mock_provider():
            a = describe_image(self.image, max_dimension=64)
        self.assertEqual(max(a.model_input_size), 64)
        self.assertEqual(a.source_sha256, __import__("hashlib").sha256(self.image.read_bytes()).hexdigest())

    def test_no_execution_fields_can_be_mutated(self):
        with self._mock_provider():
            receipt = describe_image(self.image)
        with self.assertRaises(FrozenInstanceError):
            receipt.allowed_to_act = True

    def test_reject_non_loopback_or_redirect_risk(self):
        for endpoint in (
            "https://api.example.com/v1/chat/completions",
            "http://192.168.1.23:8081/v1/chat/completions",
            "http://example.com:8081/v1/chat/completions",
            "http://127.0.0.1:8081/insecure",
            "http://user:pass@127.0.0.1:8081/v1/chat/completions",
            "http://127.0.0.1:8081/v1/chat/completions?x=1",
        ):
            with self.subTest(endpoint=endpoint):
                with self.assertRaises(ValueError):
                    _local_endpoint(endpoint)
        self.assertEqual(_local_endpoint(DEFAULT_ENDPOINT), DEFAULT_ENDPOINT)
        self.assertEqual(_local_endpoint("http://localhost:8081/v1/chat/completions"),
                         "http://localhost:8081/v1/chat/completions")

    def test_reject_missing_or_ambiguous_metadata(self):
        with self.assertRaisesRegex(ValueError, "source_kind"):
            describe_image(self.image, source_kind="REAL_IMAGE_VERIFIED")
        with self.assertRaisesRegex(ValueError, "max_dimension"):
            describe_image(self.image, max_dimension=1)
        with self.assertRaisesRegex(ValueError, "max_tokens"):
            describe_image(self.image, max_tokens=2048)
        with self.assertRaises(ValueError):
            describe_image(self.image, prompt=" ")
        self.assertEqual(self.calls, [])

    def test_response_malformed_fails_closed(self):
        class InvalidOpener:
            def open(self, request, timeout):
                return BytesIO(b'{"choices":[]}')
        with patch("brody_world_physique.jarvis_vision_v0.build_opener", return_value=InvalidOpener()):
            with self.assertRaisesRegex(RuntimeError, "invalid local vision response"):
                describe_image(self.image)

    def test_response_non_text_fails_closed(self):
        with self._mock_provider(answer=[{"type": "text", "text": "oops"}]):
            with self.assertRaisesRegex(RuntimeError, "empty or non-textual"):
                describe_image(self.image)

    def test_unavailable_provider_does_not_fake_reply(self):
        class Offline:
            def open(self, request, timeout):
                raise URLError("offline")
        with patch("brody_world_physique.jarvis_vision_v0.build_opener", return_value=Offline()):
            with self.assertRaisesRegex(RuntimeError, "unavailable"):
                describe_image(self.image)

    def test_disallow_non_images_and_missing_image(self):
        not_image = self.root / "not_image.txt"
        not_image.write_text("fake")
        with self.assertRaises(Exception):
            describe_image(not_image)
        with self.assertRaises(FileNotFoundError):
            describe_image(self.root / "missing.png")

    def test_cli_writes_only_candidate_json(self):
        out = self.root / "candidate.json"
        with self._mock_provider("Je vois un objet."), patch(
            "sys.stdout", new_callable=__import__("io").StringIO
        ):
            status = main(["--image", str(self.image), "--out", str(out)])
        self.assertEqual(status, 0)
        packet = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(packet["candidate_text"], "Je vois un objet.")
        self.assertFalse(packet["memory_write_allowed"])
        self.assertEqual(packet["source_kind"], "USER_IMAGE_FILE")
        self.assertEqual(len(self.calls), 1)

    def test_cli_disallows_overwriting_source(self):
        with patch("sys.stderr", new_callable=__import__("io").StringIO):
            with self.assertRaises(SystemExit):
                main(["--image", str(self.image), "--out", str(self.image)])
        self.assertEqual(self.calls, [])
