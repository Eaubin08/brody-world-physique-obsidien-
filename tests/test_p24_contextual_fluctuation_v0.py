"""P2.4: keep contextual fluctuations and refuse invalid cross-frame fusion."""
import tempfile
import unittest
from pathlib import Path
from brody_world_physique import p24_contextual_fluctuation_v0 as p


class ContextualFluctuationTest(unittest.TestCase):
    def test_all_seven_adversarial_fixtures(self):
        report=p.evaluate()
        self.assertEqual(report["total"],7)
        self.assertTrue(report["all_pass"])
        self.assertFalse(report["raw_pixels_tested"])

    def test_same_pixels_opposite_interpretations(self):
        cases={key:data for key,data,_ in p.fixtures()}
        moving=p.interpret(cases["moving_object_fixed_camera"])
        static=p.interpret(cases["fixed_object_moving_camera"])
        self.assertEqual(moving["apparent_displacement"],
                         static["apparent_displacement"])
        self.assertEqual(moving["world_displacement"],10)
        self.assertEqual(static["world_displacement"],0)

    def test_conflict_is_not_averaged(self):
        cases={key:data for key,data,_ in p.fixtures()}
        self.assertEqual(p.interpret(cases["ambiguous_conflict"])["status"],
                         "HOLD_CONFLICTING_CONTEXT")
        self.assertIsNone(p.interpret(cases["missing_context"])["world_displacement"])

    def test_provenance_and_replay(self):
        cases={key:data for key,data,_ in p.fixtures()}
        with self.assertRaises(ValueError):
            p.interpret({**cases["moving_object_fixed_camera"],"view_frame":"WORLD_X"})
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/"evaluation.json"
            self.assertEqual(p.main(["--out",str(out)]),0)
            self.assertEqual(p.main(["--out",str(out),"--verify"]),0)
            out.write_text("tampered",encoding="utf-8")
            with self.assertRaises(ValueError):
                p.main(["--out",str(out),"--verify"])


if __name__=="__main__":
    unittest.main()
