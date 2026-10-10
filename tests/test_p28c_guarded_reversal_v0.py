import tempfile
import unittest
from pathlib import Path
from brody_world_physique import p28c_guarded_reversal_v0 as p


class GuardedTests(unittest.TestCase):
    def test_no_feedback_holds(self):
        self.assertEqual(p.GuardedBelief().predict({"apparent":1,"shifts":[1]*5})[1],
                         "HOLD_NO_VERIFIED_FEEDBACK")

    def test_deduplication(self):
        model=p.GuardedBelief()
        self.assertTrue(model.feedback("a",[1,2,3,4,5],1))
        self.assertFalse(model.feedback("a",[1,2,3,4,5],1))
        self.assertEqual(len(model.samples),1)

    def test_rank_can_change_after_reversal(self):
        model=p.GuardedBelief(window=4)
        for k in range(4):
            model.feedback("a"+str(k),[20,20,20,20,0],0)
        self.assertEqual(model.ranking()[0][1],4)
        for k in range(4):
            model.feedback("b"+str(k),[0,20,20,20,20],0)
        self.assertEqual(model.ranking()[0][1],0)

    def test_boundary_and_identical_baselines(self):
        r=p.execute(100,2,8)
        self.assertFalse(r["native_memory_write"])
        self.assertFalse(r["b8_promotion"])
        self.assertTrue(all(not x["memory_write"] for x in r["predictions_pre_feedback"]))
        self.assertEqual(len(r["rows"]),100)

    def test_replay_integrity(self):
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/"run"
            p.run(out,100,2,8)
            self.assertTrue(p.verify(out))
            with (out/"predictions_pre_feedback.json").open("ab") as f:
                f.write(b"tamper")
            with self.assertRaises(ValueError):
                p.verify(out)


if __name__=="__main__":
    unittest.main()
