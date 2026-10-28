import json,tempfile,unittest
from pathlib import Path
from PIL import Image
from brody_world_physique.p210a_visual_loop_contract_v0 import evaluate,verify

class VisualLoopContractTests(unittest.TestCase):
    def make(self,root,errors):
        paths=[]
        for i,n in enumerate(errors):
            p=Path(root)/f"frame_{i}.png"
            im=Image.new("RGB",(8,8),"white")
            for k in range(n):im.putpixel((k%8,k//8),(0,0,0))
            im.save(p)
            paths.append(p)
        return paths

    def test_correction_accepted_and_replayed(self):
        with tempfile.TemporaryDirectory() as td:
            src,old,new=self.make(td,(0,10,2))
            out=Path(td)/"report.json"
            r=evaluate(src,old,new,out)
            self.assertEqual(r["verdict"],"ACCEPTED")
            self.assertEqual(r["initial_pixel_error"],10)
            self.assertEqual(r["candidate_pixel_error"],2)
            self.assertTrue(verify(out)["verified"])

    def test_regression_rolls_back_but_preserves_attempt(self):
        with tempfile.TemporaryDirectory() as td:
            src,old,new=self.make(td,(0,2,10))
            out=Path(td)/"report.json"
            r=evaluate(src,old,new,out)
            self.assertEqual(r["verdict"],"ROLLED_BACK")
            self.assertEqual(r["best"]["sha256"],r["initial"]["sha256"])
            self.assertEqual(len(r["attempts"]),1)
            self.assertTrue(r["attempts"][0]["preserved_even_if_rejected"])
            self.assertTrue(verify(out)["verified"])

    def test_equal_hold_and_no_rewrite(self):
        with tempfile.TemporaryDirectory() as td:
            src,old,new=self.make(td,(0,2,2))
            out=Path(td)/"report.json"
            self.assertEqual(evaluate(src,old,new,out)["verdict"],"HOLD_EQUAL")
            with self.assertRaises(ValueError):evaluate(src,old,new,out)

    def test_tampered_candidate_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            src,old,new=self.make(td,(0,5,1))
            out=Path(td)/"report.json"
            evaluate(src,old,new,out)
            Image.new("RGB",(8,8),"black").save(new)
            with self.assertRaises(ValueError):verify(out)

    def test_invalid_size_and_attempt_budget(self):
        with tempfile.TemporaryDirectory() as td:
            src,old,new=self.make(td,(0,5,1))
            out=Path(td)/"report.json"
            with self.assertRaises(ValueError):evaluate(src,old,new,out,max_attempts=0)
            Image.new("RGB",(9,8)).save(new)
            with self.assertRaises(ValueError):evaluate(src,old,new,out)

if __name__=="__main__":unittest.main()
