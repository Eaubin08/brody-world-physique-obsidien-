import json,tempfile,unittest
from pathlib import Path
from brody_world_physique.consolidated_education_replay_v1 import run as train
from brody_world_physique.session_restart_replay_v1 import resume
class RestartReplayTests(unittest.TestCase):
    def test_restart_replay_with_disjoint_seeds(self):
        with tempfile.TemporaryDirectory() as d:
            a=Path(d)/"training";train(a)
            b=Path(d)/"restart";r=resume(a/"CANDIDATE_MEMORY.json",b)
            x={v["case"]:v for v in r["tests"]}
            self.assertEqual(x["restarted_clean"]["position_error"],0.)
            self.assertEqual(x["restarted_intervention"]["position_error"],0.)
            self.assertFalse(x["restarted_unknown"]["prediction_generated"])
            self.assertTrue(r["memory_bytes_unchanged"])
            self.assertFalse(r["multi_day_retention_proven"])
    def test_tamper_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            a=Path(d)/"training";train(a)
            path=a/"CANDIDATE_MEMORY.json"
            doc=json.loads(path.read_text(encoding="utf8"))
            doc["motion"]["clean"]=33
            path.write_text(json.dumps(doc),encoding="utf8")
            with self.assertRaisesRegex(ValueError,"MEMORY_TAMPER"):resume(path,Path(d)/"restart")
    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            a=Path(d)/"training";train(a)
            b=Path(d)/"existing";b.mkdir()
            with self.assertRaisesRegex(ValueError,"PRESERVE_PRIOR_EVIDENCE"):resume(a/"CANDIDATE_MEMORY.json",b)
if __name__=="__main__":unittest.main()
