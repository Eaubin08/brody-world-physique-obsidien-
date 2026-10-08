"""No-camera/no-video/OpenCV-independent checks of the real-video intake."""
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import patch

from brody_world_physique.video_observation_v0 import (
    choose_frame_indices, make_measurements, annotate_video, video_sha256,
)
from brody_world_physique.preverbal_prediction_v0 import evaluate_four_measurements


class VideoObservationTests(TestCase):
    def setUp(self):
        temp=TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root=Path(temp.name)
        self.video=self.root/"toy.mp4"
        self.video.write_bytes(b"FAKE_VIDEO_FILE_ONLY_FOR_MOCK_TESTS")
        self.digest=video_sha256(self.video)

    def test_video_hash_and_sampling(self):
        self.assertEqual(len(self.digest), 64)
        self.assertEqual(
            choose_frame_indices(fps=30.0, frame_count=400,
                                 start_seconds=2.0, interval_seconds=0.2),
            (60,66,72,78)
        )

    def test_reject_bad_time_and_missing_video_frames(self):
        failures=[
            dict(fps=0,frame_count=100,start_seconds=0,interval_seconds=.2),
            dict(fps=float("nan"),frame_count=100,start_seconds=0,interval_seconds=.2),
            dict(fps=30,frame_count=4,start_seconds=0,interval_seconds=.2),
            dict(fps=30,frame_count=100,start_seconds=-1,interval_seconds=.2),
            dict(fps=30,frame_count=100,start_seconds=0,interval_seconds=0.001),
        ]
        for opts in failures:
            with self.subTest(opts=opts), self.assertRaises(ValueError):
                choose_frame_indices(**opts)

    def test_manual_points_are_provenance_candidate_not_physical_truth(self):
        sample=make_measurements(
            (0,6,12,18), ((10,10),(16,11),(22,14),(28,19)),
            fps=30,video_hash=self.digest,entity_ref="object:ball",source_kind="SIMULATED",
        )
        self.assertEqual(sample[0].source_kind,"SIMULATED")
        self.assertEqual(sample[0].frame_ref,"camera-image-plane:sha256:"+self.digest)
        self.assertIn("CAMERA_MOTION_UNVERIFIED",sample[0].uncertainty_refs)
        self.assertEqual(sample[3].time_s,0.6)
        self.assertEqual(sample[3].unit,"px")
        result=evaluate_four_measurements(sample)
        self.assertFalse(result["real_world_proven"])
        self.assertFalse(result["world_knowledge_validated"])
        self.assertEqual(result["physics_causality"],"UNKNOWN")

    def test_reject_malformed_object_metadata_or_clicks(self):
        with self.assertRaisesRegex(ValueError,"one point"):
            make_measurements((0,6,12,18),((1,2),)*3,fps=30,
                              video_hash=self.digest,entity_ref="ball",source_kind="SIMULATED")
        with self.assertRaisesRegex(ValueError,"coordinates"):
            make_measurements((0,6,12),((0,0),(float("nan"),1),(2,4)),
                              fps=30,video_hash=self.digest,entity_ref="ball",source_kind="SIMULATED")
        with self.assertRaisesRegex(ValueError,"indices"):
            make_measurements((0,6,6),((0,0),(1,1),(2,2)),
                              fps=30,video_hash=self.digest,entity_ref="ball",source_kind="SIMULATED")
        with self.assertRaisesRegex(ValueError,"SHA256"):
            make_measurements((0,6,12),((0,0),(1,1),(2,2)),
                              fps=30,video_hash="not-hash",entity_ref="ball",source_kind="SIMULATED")

    def test_heldout_is_not_even_annotated_until_forecast_receipt_written(self):
        class Capture:
            def __init__(self):self.released=False
            def isOpened(self):return True
            def get(self,key):return 30.0 if key==2 else 80.0
            def release(self):self.released=True
        cap=Capture()
        fake_cv2=SimpleNamespace(
            VideoCapture=lambda p:cap, CAP_PROP_FPS=2, CAP_PROP_FRAME_COUNT=3,
            destroyAllWindows=lambda:None,
        )
        dest=self.root/"run"
        observed=[]
        def fake_annotator(cv2,capture,idx,name,prompt):
            observed.append(idx)
            if len(observed)==4:
                receipt=dest/"prediction_before_frame_4.json"
                self.assertTrue(receipt.is_file())
                forecast=json.loads(receipt.read_text())
                self.assertEqual(len(forecast["history_source_refs"]),3)
                self.assertEqual(forecast["future_time_s"],18/30)
                self.assertFalse(forecast["physical_law_proven"])
            return (10.0 + idx, 4.0 + (idx/6)**2)
        with patch.dict(sys.modules,{"cv2":fake_cv2}), patch(
            "brody_world_physique.video_observation_v0._annotate_frame",
            side_effect=fake_annotator
        ):
            result=annotate_video(self.video,dest,interval_seconds=0.2,source_kind="SIMULATED")
        self.assertEqual(observed,[0,6,12,18])
        self.assertTrue(cap.released)
        self.assertEqual(result["comparison"],"BETTER_THAN_LINEAR_BASELINE")
        self.assertFalse(result["world_knowledge_validated"])
        payload=json.loads((dest/"source_measurements.json").read_text())
        self.assertEqual(payload["metadata"]["observation_method"],
                         "FOUR_MANUAL_IMAGE_PLANE_CLICKS")
        self.assertTrue(payload["metadata"]["prediction_precommitted_before_fourth_annotation"])
        self.assertFalse(payload["metadata"]["real_world_proven"])
        self.assertEqual(payload["metadata"]["source_kind_declared_by_user"],"SIMULATED")
        self.assertFalse(payload["metadata"]["source_kind_independently_verified"])

    def test_explicit_provenance_required_and_reject_forged_real_claim(self):
        with self.assertRaisesRegex(ValueError,"source_kind"):
            make_measurements(
                (0,3,6), ((1,1),(2,2),(3,3)), fps=30,
                video_hash=self.digest, entity_ref="ball", source_kind="VERIFIED_REAL",
            )
        samples = make_measurements(
            (0,3,6), ((1,1),(2,2),(3,3)), fps=30,
            video_hash=self.digest, entity_ref="ball", source_kind="GENERATED",
        )
        self.assertTrue(all(x.source_kind == "GENERATED" for x in samples))

    def test_early_escape_does_not_forge_prediction_or_experience(self):
        class Capture:
            def isOpened(self):return True
            def get(self,key):return 30.0 if key==2 else 80.0
            def release(self):pass
        fake_cv2=SimpleNamespace(VideoCapture=lambda path:Capture(), CAP_PROP_FPS=2,
                                 CAP_PROP_FRAME_COUNT=3,destroyAllWindows=lambda:None)
        dest=self.root/"abort"
        with patch.dict(sys.modules,{"cv2":fake_cv2}), patch(
            "brody_world_physique.video_observation_v0._annotate_frame",
            side_effect=RuntimeError("user cancelled")
        ):
            with self.assertRaisesRegex(RuntimeError,"cancelled"):
                annotate_video(self.video,dest,interval_seconds=.2,source_kind="SIMULATED")
        self.assertFalse((dest/"heldout_evaluation.json").exists())
