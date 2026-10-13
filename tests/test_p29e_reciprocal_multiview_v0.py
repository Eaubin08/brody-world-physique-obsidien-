import unittest
from brody_world_physique.p29e_reciprocal_multiview_v0 import analyze,reconnect_multiview

class P29EMultiview(unittest.TestCase):
    def test_reciprocal_candidate_not_proof(self):
        v=analyze({"apparent":8,"shifts":[4,4,4,4,4]},frame_ref="camera")
        self.assertEqual(v.object_relative_dx,4)
        self.assertEqual(v.reverse_relative_dx,-4)
        self.assertEqual(v.reciprocal_residual,0)
        self.assertEqual(v.status,"CANDIDATE_CORRELATED_CONSENSUS_ONLY")

    def test_correlated_majority_conflicts_with_historical_anchor(self):
        measurement={"apparent":8,"shifts":[4,26,26,26,26]}
        a=reconnect_multiview(pair_id="1",source_ref="source",measurement=measurement,
          observation_status="MEASURED_PIXELS",frame_ref="camera",goal="explore",
          anchor_id=0)
        self.assertEqual(a["historical_prediction"],4)
        self.assertIsNone(a["proposed_prediction"])
        self.assertIn("ANCHOR_VS_CORRELATED_CONSENSUS",a["contradictions"])
        self.assertFalse(a["majority_is_physical_truth"])

    def test_missing_detection_and_unsupported_anchor_hold(self):
        a=reconnect_multiview(pair_id="2",source_ref="source",measurement=None,
          observation_status="HOLD_OBJECT",frame_ref="camera",goal="generate",anchor_id=0)
        self.assertEqual(a["status"],"HOLD_CONFLICT_OR_MISSING_OBSERVATION")
        self.assertIsNone(a["proposed_prediction"])
        b=reconnect_multiview(pair_id="3",source_ref="source",
          measurement={"apparent":8,"shifts":[4,4,4,4,4]},
          observation_status="MEASURED_PIXELS",frame_ref="camera",goal="explain",anchor_id=None)
        self.assertEqual(b["status"],"HOLD_NO_HISTORICAL_ANCHOR")

    def test_goals_never_rewrite_motion(self):
        common=dict(pair_id="4",source_ref="source",measurement={"apparent":8,"shifts":[4]*5},
          observation_status="MEASURED_PIXELS",frame_ref="camera",anchor_id=0)
        x=reconnect_multiview(**common,goal="generate")
        y=reconnect_multiview(**common,goal="explain")
        self.assertEqual(x["view"],y["view"])
        self.assertEqual(x["proposed_prediction"],y["proposed_prediction"])
        self.assertNotEqual(x["goal"]["action_hint"],y["goal"]["action_hint"])

    def test_frame_is_required(self):
        with self.assertRaises(ValueError):
            analyze(None,frame_ref="")

if __name__=="__main__":
    unittest.main()
