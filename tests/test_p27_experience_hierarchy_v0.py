import tempfile
import unittest
from pathlib import Path
from brody_world_physique import p27_experience_hierarchy_v0 as p


class HierarchyExperienceTest(unittest.TestCase):
    def test_same_observation_different_order(self):
        measure={"apparent":10,"landmarks":[26,26,26,26,0]}
        reliabilities=[26,25,24,23,0]
        result=p.predict(measure,reliabilities)
        self.assertEqual(result["majority"],-16)
        self.assertEqual(result["hierarchy"],10)
        self.assertEqual(result["experience"],10)
        self.assertIsNone(result["hierarchy_experience"])

    def test_conflict_holds_majority_not_history(self):
        measure={"apparent":10,"landmarks":[26,0,26,0,0]}
        result=p.predict(measure,[26,26,26,0,0])
        self.assertIsNone(result["majority"])
        self.assertEqual(result["hierarchy_experience"],10)

    def test_replay_and_tampering(self):
        with tempfile.TemporaryDirectory() as root:
            out=Path(root)/"run"
            report=p.run(out,20,20)
            self.assertEqual(report["test_count"],20)
            self.assertTrue(p.verify(out)["verified"])
            with (out/"predictions_pre_scoring.jsonl").open("a") as stream:
                stream.write("tamper")
            with self.assertRaises(ValueError):
                p.verify(out)


if __name__=="__main__":
    unittest.main()
