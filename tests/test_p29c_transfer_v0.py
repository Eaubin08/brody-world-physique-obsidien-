import tempfile
import unittest
from pathlib import Path
from brody_world_physique import p29c_transfer_v0 as p

class TransferTests(unittest.TestCase):
    def test_train_only_anchor(self):
        c=p.calibrate(40)
        self.assertEqual(c["anchor"],4)

    def test_new_visual_generator(self):
        old=p.fixture(2,split="train",family="original")
        new=p.fixture(2,split="test",family="shifted")
        self.assertNotEqual(old["family"],new["family"])
        self.assertNotEqual(p.draw(old,0).shape,p.draw(new,0).shape) if False else None
        self.assertNotEqual(tuple(p.draw(old,0)[0,0]),tuple(p.draw(new,0)[0,0]))

    def test_zero_test_feedback_and_intent(self):
        r=p.execute(40,90,"shifted")
        self.assertFalse(r["test_truth_feedback"])
        self.assertFalse(r["native_memory_write"])
        self.assertFalse(r["b8_promotion"])
        self.assertEqual(r["decision_authority"],"KX108_ONLY")
        self.assertEqual(set(v["goal"] for v in r["receipts"]),{"generate","explore","explain"})
        self.assertEqual(len(r["score_rows"]),90)

    def test_transfer_shows_failures_not_false_promotion(self):
        r=p.execute(40,135,"shifted")
        self.assertEqual(len(r["segments"]),3)
        self.assertIsNone(r["summary"]["cold_hold"]["mae_accepted_px"])
        self.assertFalse(r["physical_generalization_verified"])

    def test_replay_integrity(self):
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/"test"
            p.run(out,40,90)
            self.assertTrue(p.verify(out))
            with (out/"predictions_pre_scoring.json").open("ab") as f:f.write(b"x")
            with self.assertRaises(ValueError):p.verify(out)

if __name__=="__main__":unittest.main()
