import json,tempfile,unittest
from pathlib import Path
from brody_world_physique.p29i_paired_audit_v0 import analyze,run,verify

def fixture():
    arms=["A1_SPATIAL_DELTA","A4_FROZEN_MEMORY"]
    proposals=[
      {"clip":"a","future_frame":18,"predictions":dict.fromkeys(arms)},
      {"clip":"a","future_frame":24,"predictions":dict.fromkeys(arms)},
      {"clip":"b","future_frame":18,"predictions":dict.fromkeys(arms)}]
    scores=[]
    for clip,frame,s,m in [("a",3,4.,2.),("a",4,15.,None),("b",3,None,None)]:
        for arm,err in zip(arms,[s,m]):
            scores.append({"clip":clip,"frame":frame,"arm":arm,"error_px":err})
    return {"schema":"BRODY_P29H_PRECOMMITTED_POSITION_ABLATION_V0",
            "test_feedback_used_for_learning":False,"native_memory_write":False,
            "decision_authority":"KX108_ONLY","shared_test_cases":3,
            "precommit":proposals,"scores":scores,"arms":{a:{} for a in arms}}

class PairedAudit(unittest.TestCase):
    def test_paired_groups(self):
        r=analyze(fixture())
        self.assertEqual(r["paired_episodes"],1)
        self.assertEqual(r["mean_paired_memory_minus_spatial_px"],-2.)
        self.assertEqual(r["spatial_on_memory_hold_cases"]["mae_px"],15.)
        self.assertEqual(r["groups"]["both_hold"],1)
    def test_replay_and_tamper(self):
        with tempfile.TemporaryDirectory() as td:
            source=Path(td)/"source.json";out=Path(td)/"paired.json"
            source.write_text(json.dumps(fixture()),encoding="utf-8")
            run(source,out)
            self.assertTrue(verify(source,out)["verified"])
            report=json.loads(out.read_text());report["paired_episodes"]=100
            out.write_text(json.dumps(report))
            with self.assertRaises(ValueError):verify(source,out)
    def test_incomplete_case_fails(self):
        d=fixture();d["scores"].pop()
        with self.assertRaises(ValueError):analyze(d)
    def test_illegal_test_training_flag_fails(self):
        d=fixture();d["test_feedback_used_for_learning"]=True
        with self.assertRaises(ValueError):analyze(d)

if __name__=="__main__":unittest.main()
