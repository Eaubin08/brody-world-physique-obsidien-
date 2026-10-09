"""P2.8 invariants: synthetic diagnostic only, never Native Memory or B8 authority."""
import tempfile
import unittest
from pathlib import Path

from brody_world_physique.p28_epistemic_reversal_v0 import (
    WorkingKnowledge, decide, execute, run, verify, episode,
)


class P28EpistemicReversalTests(unittest.TestCase):
    def test_duplicate_evidence_group_does_not_gain_votes(self):
        model = WorkingKnowledge()
        e = episode(2)
        self.assertTrue(model.apply_feedback(episode_id=2, group_id="same",
            observed_shifts=e["shifts"], verified_camera=e["camera"]))
        before = {k: tuple(v) for k, v in model.residuals.items()}
        self.assertFalse(model.apply_feedback(episode_id=2, group_id="same",
            observed_shifts=e["shifts"], verified_camera=e["camera"]))
        self.assertEqual(before, {k: tuple(v) for k, v in model.residuals.items()})

    def test_intent_cannot_change_prediction_or_truth(self):
        model = WorkingKnowledge()
        e = episode(0)
        model.apply_feedback(episode_id=0, group_id="p0",
            observed_shifts=e["shifts"], verified_camera=e["camera"])
        observed = {"shifts": e["shifts"], "apparent": e["apparent"]}
        outputs = [decide(observed, model, intent=g) for g in ("generate","explore","explain")]
        self.assertEqual(outputs[0]["predictions"], outputs[1]["predictions"])
        self.assertEqual(outputs[1]["predictions"], outputs[2]["predictions"])
        self.assertEqual(len({o["goal_route"] for o in outputs}), 3)
        self.assertTrue(all(o["memory_write"] is False for o in outputs))

    def test_pre_feedback_no_truth_fields(self):
        result = execute(70)
        for entry in result["precommit"]:
            self.assertNotIn("camera", entry["observed"])
            self.assertNotIn("world", entry["observed"])
            self.assertNotIn("truth", entry["observed"])
            self.assertFalse(entry["prediction"]["memory_write"])

    def test_reversal_does_not_remain_frozen(self):
        result = execute(70, 1)
        observed = [x["prediction"]["best_historical_id"] for x in result["precommit"]]
        self.assertEqual(observed[2], 4)
        self.assertEqual(observed[-1], 0)

    def test_hold_without_calibration(self):
        e = episode(0)
        decision = decide({"shifts": e["shifts"], "apparent": e["apparent"]}, WorkingKnowledge())
        self.assertIsNone(decision["predictions"]["scoped_revisable"])
        self.assertEqual(decision["reason"], "HOLD_UNCALIBRATED")

    def test_determinism_and_integrity(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "run"
            run(p, 70, 2)
            self.assertTrue(verify(p))
            with (p / "predictions_pre_feedback.json").open("ab") as f:
                f.write(b"altered")
            with self.assertRaises(ValueError):
                verify(p)


if __name__ == "__main__":
    unittest.main()
