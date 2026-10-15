import tempfile,unittest
from pathlib import Path
from brody_world_physique.u5b_u8_integrated_big_batch_v1 import run
class FullBigBatchTests(unittest.TestCase):
    def test_all_chapters_and_boundaries(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/"batch";r=run(root,seeds=1)
            self.assertEqual(r["U5B"]["status"],"HOLD_NO_INDEPENDENT_VIDEO")
            self.assertTrue(all(r["U6"]["local_contracts"].values()))
            self.assertFalse(r["U6"]["upstream_sens_verified"])
            self.assertEqual(r["U7B"]["camera_episodes"],6)
            self.assertEqual(r["U7B"]["heldout_views"],2)
            self.assertFalse(r["U7B"]["reverse_360_proven"])
            cases={x["case"]:x for x in r["U8"]["cases"]}
            self.assertEqual(cases["learned"]["visual_mae"],0.)
            self.assertEqual(cases["retained"]["visual_mae"],0.)
            self.assertIsNone(cases["unknown"]["visual_mae"])
            self.assertTrue(r["U8"]["single_candidate_state"])
            self.assertFalse(r["native_memory_write"])
            self.assertFalse(r["canonical_promotion"])
            self.assertTrue((root/"MASTER_REPORT.json").is_file())
    def test_video_file_metadata_not_misrepresented_as_video_exam(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"clip.mp4";p.write_bytes(b"fixture-bytes")
            r=run(Path(d)/"run",video=p,seeds=1)
            self.assertEqual(r["U5B"]["video_frames_examined"],0)
            self.assertFalse(r["U5B"]["actual_video_prediction_proven"])
    def test_preserve_old_reports(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"existing";p.mkdir()
            with self.assertRaisesRegex(ValueError,"PRESERVE_PRIOR_EVIDENCE"):run(p)
if __name__=="__main__":unittest.main()
