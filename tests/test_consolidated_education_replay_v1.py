import tempfile,unittest
from pathlib import Path
from brody_world_physique.consolidated_education_replay_v1 import run
class ConsolidatedReplayTests(unittest.TestCase):
    def test_old_new_unknown_and_retention(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/"session";r=run(root)
            by={a["case"]:a for a in r["replays"]}
            self.assertEqual(r["retention_gate_global_update"],"BLOCKED")
            self.assertEqual(by["old_clean_replay"]["position_error"],0)
            self.assertEqual(by["old_clean_replay"]["image_mae"],0)
            self.assertEqual(by["new_slope_transfer"]["position_error"],0)
            self.assertEqual(by["new_slope_transfer"]["image_mae"],0)
            self.assertFalse(by["unknown_novel"]["prediction_generated"])
            self.assertTrue((root/"CANDIDATE_MEMORY.json").is_file())
            self.assertEqual(len(list(root.glob("*_PRECOMMIT.json"))),3)
            self.assertFalse(r["native_memory_write"])
            self.assertFalse(r["long_term_memory_retention_proven"])
    def test_refuse_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/"existing";root.mkdir()
            with self.assertRaisesRegex(ValueError,"PRESERVE_PRIOR_EVIDENCE"):run(root)
if __name__=="__main__":unittest.main()
