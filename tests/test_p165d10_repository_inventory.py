import tempfile,unittest
from pathlib import Path
from scripts.p165d10_repo_test_inventory import inventory,run
class InventoryTests(unittest.TestCase):
 def test_finds_known_historical_and_d10(self):
  r=inventory(".")
  for k in ("p161","p162","p163","p164","p165a","p165b","p165c","p165d"):
   self.assertGreater(r["legacy"][k]["declared_tests"],0,k)
  self.assertGreaterEqual(r["declared_tests"],120)
 def test_ast_does_not_execute_tests(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);(p/"tests").mkdir()
   marker=p/"EXECUTED"
   (p/"tests"/"test_side_effect.py").write_text(
    "from pathlib import Path\nPath(%r).write_text('oops')\ndef test_sample(): pass\n"%str(marker))
   report=inventory(p)
   self.assertEqual(report["declared_tests"],1)
   self.assertFalse(marker.exists())
 def test_output_preserved(self):
  with tempfile.TemporaryDirectory() as td:
   out=Path(td)/"report"
   result=run(".",out)
   self.assertGreater(result["test_files"],8)
   with self.assertRaises(ValueError):run(".",out)
if __name__=="__main__":unittest.main()
