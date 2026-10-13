import tempfile
import unittest
from pathlib import Path
from brody_world_physique.p29b_layer_wiring_v0 import (
    layered_prediction, execute, run, verify, GOALS,
)
from brody_world_physique.p28c_guarded_reversal_v0 import GuardedBelief


class LayerWiringTests(unittest.TestCase):
    def test_observation_hold_propagates_without_inventing_truth(self):
        x = layered_prediction("a", None, "HOLD_OBJECT", GuardedBelief(), "generate")
        self.assertEqual(x["spatial"]["status"], "HOLD_PERCEPTION")
        self.assertEqual(x["belief"]["epistemic_status"], "HOLD")
        self.assertIsNone(x["prediction"])
        self.assertEqual(x["goal_route"]["action_hint"], "REQUEST_MISSING_EVIDENCE")

    def test_goal_changes_routing_only(self):
        g = GuardedBelief(window=4)
        for i in range(4):
            g.feedback("g"+str(i), [0,24,24,24,24], 0)
        observed = {"apparent": 8, "shifts": [0,24,24,24,24]}
        results = [layered_prediction("a", observed, "MEASURED_PIXELS", g, goal)
                   for goal in GOALS]
        self.assertEqual(len({x["prediction"] for x in results}), 1)
        self.assertEqual(len({x["goal_route"]["action_hint"] for x in results}), 3)
        self.assertTrue(all(x["belief"]["epistemic_status"] == "WORKING_UNVERIFIED"
                            for x in results))

    def test_same_pixels_same_pred_as_p28c(self):
        r = execute(100, 2, 8)
        self.assertTrue(r["identical_to_p28c_reference"])
        self.assertTrue(all(x["p29b_prediction"] == x["p28c_reference"]
                            for x in r["receipts"]))
        self.assertTrue(all(not x["memory_write"] for x in r["receipts"]))
        self.assertFalse(r["native_memory_write"])
        self.assertFalse(r["b8_promotion"])

    def test_replay_tamper(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "run"
            run(out, 100, 2, 8)
            self.assertTrue(verify(out)["verified"])
            with (out/"predictions_pre_feedback.json").open("ab") as f:
                f.write(b"tamper")
            with self.assertRaises(ValueError):
                verify(out)


if __name__ == "__main__":
    unittest.main()
