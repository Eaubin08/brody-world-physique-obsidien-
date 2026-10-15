import tempfile,unittest,json
from pathlib import Path
from scripts.p165d10_global_regression_runner import run
from scripts.p165d10_repo_test_inventory import inventory
class GlobalRegressionRunnerTests(unittest.TestCase):
 def test_minimal_green_capture(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp)/"repo";(root/"tests").mkdir(parents=True)
   (root/"tests"/"test_ok.py").write_text(
    "import unittest\nclass TestOK(unittest.TestCase):\n def test_ok(self): self.assertTrue(True)\n")
   out=Path(tmp)/"proof"
   result=run(out,root=root,timeout=30)
   self.assertEqual(result["verdict"],"GREEN")
   self.assertTrue((out/"STDERR.txt").is_file())
 def test_red_is_not_green(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp)/"repo";(root/"tests").mkdir(parents=True)
   (root/"tests"/"test_fail.py").write_text(
    "import unittest\nclass TestFail(unittest.TestCase):\n def test_fail(self): self.assertEqual(1,2)\n")
   result=run(Path(tmp)/"proof",root=root,timeout=30)
   self.assertEqual(result["verdict"],"RED_OR_INCOMPLETE")
   self.assertNotEqual(result["exit_code"],0)
 def test_report_immutable(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp)/"repo";(root/"tests").mkdir(parents=True)
   out=Path(tmp)/"proof";run(out,root=root,timeout=30)
   with self.assertRaises(ValueError):run(out,root=root,timeout=30)
 def test_exact_p165d_inventory(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);(root/"tests").mkdir()
   (root/"tests"/"test_scene_event_epistemic_p165d.py").write_text("def test_one(): pass\n")
   (root/"tests"/"test_persistent_world_state_p165d4.py").write_text("def test_other(): pass\n")
   report=inventory(root)
   self.assertEqual(report["legacy"]["p165d"]["declared_tests"],1)
   self.assertEqual(report["legacy"]["p165d"]["files"],["tests/test_scene_event_epistemic_p165d.py"])
if __name__=="__main__":unittest.main()
