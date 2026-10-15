import unittest
from dataclasses import fields
from brody_world_physique.p29_layer_contracts_v0 import (
    PixelObservation, represent, infer, route, BOUNDARY,
)


class P29Boundaries(unittest.TestCase):
    def test_observation_cannot_contain_truth_or_goal(self):
        keys = {x.name for x in fields(PixelObservation)}
        self.assertFalse(keys.intersection({
            "camera", "world", "truth", "anchor", "goal", "promotion", "authority"}))

    def test_perception_hold_cannot_be_inferred(self):
        obs = PixelObservation("pair-1", "rendered-frame-1", None, (), "HOLD_OBJECT")
        relations = represent(obs, coordinate_frame="camera-relative")
        self.assertEqual(relations.status, "HOLD_PERCEPTION")
        belief = infer(relations, historical_anchor_id=4)
        self.assertIsNone(belief.inferred_world_dx)
        self.assertEqual(belief.epistemic_status, "HOLD")

    def test_goal_does_not_rewrite_belief(self):
        obs = PixelObservation("pair-2", "image-pair-hash", 12.0,
                               (4.0, 28.0, 28.0, 28.0, 28.0), "MEASURED_PIXELS")
        rel = represent(obs, coordinate_frame="camera-relative")
        b = infer(rel, historical_anchor_id=0)
        plans = [route(intent, b) for intent in ("generate", "explore", "explain")]
        self.assertEqual(b.inferred_world_dx, 8.0)
        self.assertTrue(all(p.belief is b for p in plans))
        self.assertEqual(len({p.action_hint for p in plans}), 3)
        self.assertEqual(b.epistemic_status, "WORKING_UNVERIFIED")

    def test_explicit_frame_and_invalid_ids(self):
        obs = PixelObservation("a", "source", 1.0, (0,0,0,0,0), "MEASURED_PIXELS")
        with self.assertRaises(ValueError):
            represent(obs, coordinate_frame="")
        with self.assertRaises(ValueError):
            infer(represent(obs, coordinate_frame="frame-a"), historical_anchor_id=5)

    def test_nonsovereignty(self):
        self.assertIs(BOUNDARY["memory_write"], False)
        self.assertIs(BOUNDARY["b8_promotion"], False)
        self.assertIs(BOUNDARY["emits_act"], False)
        self.assertEqual(BOUNDARY["decision_authority"], "KX108_ONLY")


if __name__ == "__main__":
    unittest.main()
