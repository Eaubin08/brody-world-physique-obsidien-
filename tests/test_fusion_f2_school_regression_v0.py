import tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from brody_world_physique.fusion_f2_school_regression_v0 import run,SUITES

class RunnerTests(unittest.TestCase):
 def setup_repo(self,td):
    root=Path(td)/"repo";(root/"tests").mkdir(parents=True)
    for f in SUITES.values():(root/"tests"/f).write_text("from unittest import TestCase\nclass Test(TestCase):\n def test_ok(self): self.assertTrue(True)\n")
    return root
 def test_suite_logs_and_results(self):
    with tempfile.TemporaryDirectory() as td:
       root=self.setup_repo(td);out=Path(td)/"report"
       result=run(root,out)
       self.assertEqual(result["pass"],len(SUITES))
       self.assertEqual(result["fail"],0)
       self.assertEqual(len(list(out.glob("*.log"))),len(SUITES))
 def test_failure_not_hidden(self):
    with tempfile.TemporaryDirectory() as td:
       root=self.setup_repo(td)
       (root/"tests"/"test_drawing_school_v0.py").write_text("from unittest import TestCase\nclass Test(TestCase):\n def test_bad(self): self.fail('EXPECTED')\n")
       result=run(root,Path(td)/"report")
       self.assertEqual(result["fail"],1)
       self.assertEqual(result["pass"],len(SUITES)-1)
 def test_existing_output_rejected(self):
    with tempfile.TemporaryDirectory() as td:
       root=self.setup_repo(td);out=Path(td)/"report";out.mkdir()
       with self.assertRaises(ValueError):run(root,out)
if __name__=="__main__":unittest.main()
