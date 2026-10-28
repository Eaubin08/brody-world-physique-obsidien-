import tempfile,unittest
from pathlib import Path
from brody_world_physique.u5_u7_video_multiview_evidence_v1 import run
class VideoMultiviewEvidenceTests(unittest.TestCase):
    def test_bounded_multiview_and_no_external_video(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/"run";r=run(root,seeds=1)
            self.assertEqual(r["U5"]["status"],"HOLD_NO_INDEPENDENT_VIDEO")
            self.assertEqual(r["U7"]["episodes"],6)
            self.assertEqual(len(r["U7"]["case_results"]),6)
            self.assertFalse(r["U7"]["camera_parameters_provided_to_tracker"])
            self.assertFalse(r["U7"]["identity_labels_provided_to_tracker"])
            self.assertFalse(r["U7"]["full_reverse_360_proven"])
            self.assertFalse(r["native_memory_write"])
    def test_video_is_hashed_not_claimed_as_exam(self):
        with tempfile.TemporaryDirectory() as d:
            src=Path(d)/"sample.mp4";src.write_bytes(b"not authenticated video bytes")
            r=run(Path(d)/"run",video=src,seeds=1)
            self.assertEqual(r["U5"]["status"],"FILE_HASHED_NOT_VISUALLY_EXAMINED")
            self.assertEqual(r["U5"]["video_frames_examined"],0)
    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/"run";root.mkdir()
            with self.assertRaisesRegex(ValueError,"PRESERVE_PRIOR_EVIDENCE"):run(root)
if __name__=="__main__":unittest.main()
