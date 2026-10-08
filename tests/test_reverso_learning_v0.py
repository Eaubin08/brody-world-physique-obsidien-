"""Executable tests of the user's RECIPROQUE idea, with bounded technical claims."""
from dataclasses import FrozenInstanceError
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from PIL import Image

from brody_world_physique.reverso_learning_v0 import (
    LearningEpisodeSignalV0, WorldRelationCandidateV0,
    decompose_reverso, replay_reverso, triage_learning,
)


class ReversoPixelMethodTests(TestCase):
    def setUp(self):
        temp = TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.src = self.root / "input.png"
        im = Image.new("RGBA", (37, 39), (0, 0, 0, 0))
        for y in range(im.height):
            for x in range(im.width):
                im.putpixel((x, y), ((x * 5) % 256, (y * 7) % 256, (x + y) % 256, (x * 11 + y * 3) % 256))
        im.save(self.src, "PNG")

    def test_pixel_roundtrip_is_exact_even_across_tile_boundaries(self):
        result = decompose_reverso(
            self.src, self.root / "out", tile_size=16, intent="Preserve source completely"
        )
        self.assertEqual(result["pixel_equivalence"], "PASS_EXACT_DECODED_RGBA")
        self.assertEqual(result["layer_count"], 9)
        self.assertEqual(result["reference_rgba_pixel_digest"], result["reconstructed_rgba_pixel_digest"])
        with Image.open(self.src) as original, Image.open(result["reconstructed"]) as generated:
            self.assertEqual(original.mode, "RGBA")
            self.assertEqual(original.size, generated.size)
            self.assertEqual(original.tobytes(), generated.tobytes())
        data = json.loads(Path(result["manifest"]).read_text(encoding="utf-8"))
        self.assertEqual(data["intent"], "Preserve source completely")
        self.assertFalse(data["claims"]["world_physics_understood"])
        self.assertFalse(data["claims"]["semantic_decomposition"])
        self.assertFalse(data["memory_write_allowed"])

    def test_replay_works_from_files_after_original_is_deleted(self):
        result = decompose_reverso(self.src, self.root / "out", tile_size=16)
        self.src.unlink()
        replay = replay_reverso(result["manifest"], output=self.root / "replayed.png")
        self.assertEqual(replay["pixel_equivalence"], "PASS_EXACT_DECODED_RGBA")
        self.assertEqual(
            replay["reconstructed_rgba_pixel_digest"],
            result["reference_rgba_pixel_digest"],
        )

    def test_reject_tampered_layer(self):
        result = decompose_reverso(self.src, self.root / "out", tile_size=16)
        tile = self.root / "out" / "lossless_layers" / "tile-000-000.png"
        tile.write_bytes(tile.read_bytes() + b"extra")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            replay_reverso(result["manifest"])

    def test_reject_missing_or_overlapping_layers(self):
        result = decompose_reverso(self.src, self.root / "out", tile_size=16)
        manifest = Path(result["manifest"])
        original = json.loads(manifest.read_text())
        truncated = dict(original, layers=original["layers"][:-1])
        manifest.write_text(json.dumps(truncated))
        with self.assertRaisesRegex(ValueError, "missing source pixels"):
            replay_reverso(manifest)
        duplicated = dict(original, layers=original["layers"] + [original["layers"][0]])
        manifest.write_text(json.dumps(duplicated))
        with self.assertRaisesRegex(ValueError, "overlapping"):
            replay_reverso(manifest)

    def test_reject_layer_path_escape(self):
        result = decompose_reverso(self.src, self.root / "out", tile_size=16)
        manifest = Path(result["manifest"])
        raw = json.loads(manifest.read_text())
        raw["layers"][0]["asset"] = "../input.png"
        manifest.write_text(json.dumps(raw))
        with self.assertRaisesRegex(ValueError, "unsafe layer path"):
            replay_reverso(manifest)

    def test_refuse_overwrite_and_unsupported_tile(self):
        with self.assertRaisesRegex(ValueError, "tile_size"):
            decompose_reverso(self.src, self.root / "out", tile_size=1)
        with self.assertRaisesRegex(ValueError, "intent"):
            decompose_reverso(self.src, self.root / "out", intent=" ")
        with self.assertRaisesRegex(ValueError, "output directory"):
            decompose_reverso(self.src, self.root)
        decompose_reverso(self.src, self.root / "out", tile_size=16)
        with self.assertRaisesRegex(ValueError, "already contains"):
            decompose_reverso(self.src, self.root / "out", tile_size=16)

    def test_jpeg_reference_is_exact_decoded_rgba_not_file_bytes(self):
        jpeg = self.root / "photo.jpg"
        Image.new("RGB", (41, 37), (80, 70, 40)).save(jpeg, "JPEG")
        result = decompose_reverso(jpeg, self.root / "jpeg_out", tile_size=16)
        self.assertEqual(result["pixel_equivalence"], "PASS_EXACT_DECODED_RGBA")
        with Image.open(jpeg) as original, Image.open(result["reconstructed"]) as reconstructed:
            self.assertEqual(original.convert("RGBA").tobytes(), reconstructed.tobytes())


class LearningMemoryPolicyTests(TestCase):
    def make(self, kind, outcome="PASS", evidence=(), replay=False, relevant=True):
        return LearningEpisodeSignalV0(
            kind=kind, source_ref="sha256:abc",
            route_ref="reverso:tile-v0", outcome=outcome,
            independent_evidence_refs=evidence, replay_confirmed=replay,
            relevant_to_intent=relevant,
        )

    def test_source_anchor_kept_as_reference_not_dump(self):
        r = triage_learning(self.make("SOURCE_ANCHOR"))
        self.assertEqual(r["proposed_action"], "KEEP_SOURCE_REFERENCE")
        self.assertFalse(r["memory_write_allowed"])

    def test_unverified_qwen_output_is_not_retained_as_world_fact(self):
        for kind in ("MODEL_DESCRIPTION", "RAW_PIXEL_DUMP"):
            r = triage_learning(self.make(kind))
            self.assertEqual(r["proposed_action"], "REFERENCE_ONLY")
            self.assertFalse(r["world_fact_claim"])
            self.assertFalse(r["canonical_memory"])

    def test_relevant_validated_skill_or_invariant_is_review_candidate(self):
        for kind in ("INVARIANT", "SKILL", "FAILURE_PATTERN"):
            result = triage_learning(self.make(kind, evidence=("test:independent",), replay=True))
            self.assertEqual(result["proposed_action"], "REVIEW_VALIDATED_PATTERN")
            self.assertFalse(result["auto_promotion_allowed"])

    def test_failure_requires_evidence_and_replay_before_strong_retention(self):
        not_tested = triage_learning(self.make("FAILURE_PATTERN", outcome="FAIL"))
        self.assertEqual(not_tested["proposed_action"], "REVIEW_EXPERIENCE")
        tested = triage_learning(self.make("FAILURE_PATTERN", outcome="FAIL",
                                          evidence=("pixel-check:123",), replay=True),
                                 previous_failed_routes=("reverso:tile-v0",))
        self.assertTrue(tested["known_failed_route_repetition"])
        self.assertTrue(tested["should_propose_alternate_route"])
        self.assertFalse(tested["memory_write_allowed"])

    def test_irrelevant_and_unknown_not_promoted(self):
        irrelevant = triage_learning(self.make("SKILL", relevant=False))
        self.assertEqual(irrelevant["proposed_action"], "OMIT_FROM_LEARNING_CANDIDATE")
        unknown = triage_learning(self.make("INVARIANT", outcome="UNKNOWN"))
        self.assertEqual(unknown["proposed_action"], "REVIEW_HYPOTHESIS")

    def test_world_relation_is_only_candidate_even_if_reviewed(self):
        relation = WorldRelationCandidateV0(
            subject_ref="object:person-A", relation="left_of", object_ref="object:person-B",
            source_ref="sha256:image", evidence_status="REVIEWED",
        )
        self.assertFalse(relation.world_law_proven)
        self.assertEqual(relation.decision_authority, "KX108_ONLY")
        with self.assertRaises(FrozenInstanceError):
            relation.world_law_proven = True
        with self.assertRaisesRegex(ValueError, "cannot prove"):
            WorldRelationCandidateV0(
                subject_ref="object:A", relation="falls_to", object_ref="floor",
                source_ref="test", world_law_proven=True,
            )

    def test_bad_signal_rejected(self):
        with self.assertRaises(ValueError):
            self.make("UNKNOWN_KIND")
        with self.assertRaises(ValueError):
            self.make("SKILL", outcome="INVALID")
