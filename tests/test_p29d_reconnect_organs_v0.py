import unittest
from brody_world_physique.p29d_reconnect_organs_v0 import reconnect


class ReconnectedOrgansTests(unittest.TestCase):
    def test_actual_existing_world_and_triage_objects(self):
        x=reconnect(pair_id="p1",source_ref="sha256:source",
                    measurement={"apparent":8.0,"shifts":[4.,28.,28.,28.,28.]},
                    observation_status="MEASURED_PIXELS",frame_ref="camera:1",
                    anchor_id=0,goal="explore",prior_prediction=-20)
        self.assertEqual(x["belief"]["inferred_world_dx"],4.)
        self.assertIn("PRIOR_VS_CURRENT_PREDICTION",x["delta"]["contradictions"])
        self.assertEqual(x["learning_triage"]["proposed_action"],"REVIEW_HYPOTHESIS")
        self.assertFalse(x["experience"]["canonical_memory"])
        self.assertFalse(x["experience"]["memory_write_allowed"])
        self.assertFalse(x["memory_write"])
        self.assertFalse(x["b8_promotion"])
        self.assertEqual(x["decision_authority"],"KX108_ONLY")

    def test_hold_propagates_across_every_layer(self):
        x=reconnect(pair_id="p2",source_ref="sha256:source",
                    measurement=None,observation_status="HOLD_OBJECT",
                    frame_ref="camera:1",anchor_id=0,goal="generate")
        self.assertEqual(x["spatial"]["status"],"HOLD_PERCEPTION")
        self.assertEqual(x["belief"]["epistemic_status"],"HOLD")
        self.assertEqual(x["experience"]["outcome"],"HOLD")
        self.assertEqual(x["goal"]["action_hint"],"REQUEST_MISSING_EVIDENCE")

    def test_intent_does_not_alter_predictions_or_evidence(self):
        args=dict(pair_id="p3",source_ref="sha256:other",
                  measurement={"apparent":8.,"shifts":[4.,28.,28.,28.,28.]},
                  observation_status="MEASURED_PIXELS",
                  frame_ref="camera:1",anchor_id=0)
        a=reconnect(**args,goal="generate")
        b=reconnect(**args,goal="explain")
        self.assertEqual(a["belief"],b["belief"])
        self.assertEqual(a["delta"],b["delta"])
        self.assertNotEqual(a["goal"]["action_hint"],b["goal"]["action_hint"])

    def test_fail_closed_unknown_frame_and_anchor(self):
        args=dict(pair_id="p4",source_ref="sha256:x",
                  measurement={"apparent":8.,"shifts":[4.,28.,28.,28.,28.]},
                  observation_status="MEASURED_PIXELS",goal="explain")
        with self.assertRaises(ValueError):
            reconnect(**args,frame_ref="",anchor_id=0)
        with self.assertRaises(ValueError):
            reconnect(**args,frame_ref="camera:1",anchor_id=5)

    def test_repeatability_and_source_provenance(self):
        args=dict(pair_id="p5",source_ref="sha256:s",measurement=None,
                  observation_status="HOLD_OBJECT",frame_ref="camera:1",
                  anchor_id=None,goal="explore")
        x=reconnect(**args)
        self.assertEqual(x,reconnect(**args))
        self.assertIn("sha256:s",x["belief"]["evidence_refs"])
        self.assertFalse(x["delta"]["causal_proof"])


if __name__=="__main__":
    unittest.main()
