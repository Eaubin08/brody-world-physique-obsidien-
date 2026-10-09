import unittest,json,tempfile
from pathlib import Path
from brody_world_physique.p29j_frozen_hybrid_audit_v0 import audit,produce

def example():
    arms=["A4_FROZEN_MEMORY","A1_SPATIAL_DELTA"]
    pts=[("x",18,[1.,1.],[5.,5.],2.,4.),("x",24,None,[6.,6.],None,8.),("x",30,None,None,None,None)]
    pre=[];scores=[]
    for clip,frame,mem,sp,me,se in pts:
        pre.append({"clip":clip,"future_frame":frame,
                    "predictions":dict(zip(arms,(mem,sp)))})
        for arm,err in zip(arms,(me,se)):
            scores.append({"clip":clip,"frame":frame//6,"arm":arm,"error_px":err})
    return {"schema":"BRODY_P29H_PRECOMMITTED_POSITION_ABLATION_V0",
        "test_feedback_used_for_learning":False,"native_memory_write":False,
        "decision_authority":"KX108_ONLY","precommit":pre,"scores":scores,
        "shared_test_cases":3}

class HybridTests(unittest.TestCase):
    def test_frozen_choice_is_memory_else_spatial_else_hold(self):
        r=audit(example())
        self.assertEqual(r["choices"],{"A4_FROZEN_MEMORY":1,"A1_SPATIAL_DELTA":1,"HOLD":1})
        self.assertEqual(r["accepted"],2)
        self.assertEqual(r["mean_error_px"],5.)
        self.assertFalse(r["test_errors_used_to_choose"])
        self.assertFalse(r["independent_data_validation"])
    def test_precommitted_prediction_with_missing_future_is_unscorable(self):
        x=example()
        # The sealed spatial proposal exists, but its future observation is missing.
        for row in x["scores"]:
            if row["frame"]==4:
                row["error_px"]=None
        result=audit(x)
        self.assertEqual(result["issued_predictions"],2)
        self.assertEqual(result["unscorable_predictions"],1)
        self.assertEqual(result["future_observed_cases"],1)
        self.assertEqual(result["accepted"],1)
        self.assertEqual(result["mean_error_px"],2.)
        self.assertEqual(result["choices"]["A1_SPATIAL_DELTA"],1)

    def test_observed_future_with_missing_selected_score_rejected(self):
        x=example()
        for row in x["scores"]:
            if row["frame"]==3 and row["arm"]=="A4_FROZEN_MEMORY":
                row["error_px"]=None
        with self.assertRaises(ValueError):
            audit(x)

    def test_replay_and_mutation(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"source.json";out=Path(td)/"out.json"
            p.write_text(json.dumps(example()))
            produce(p,out)
            self.assertTrue(produce(p,out,True)["verified"])
            x=json.loads(out.read_text());x["coverage"]=0.12345
            out.write_text(json.dumps(x))
            with self.assertRaises(ValueError):produce(p,out,True)
    def test_fail_closed_missing_proof(self):
        x=example();x["precommit"][0]["predictions"].pop("A4_FROZEN_MEMORY")
        with self.assertRaises(ValueError):audit(x)
    def test_test_feedback_never_accepted(self):
        x=example();x["test_feedback_used_for_learning"]=True
        with self.assertRaises(ValueError):audit(x)
if __name__=="__main__":unittest.main()
