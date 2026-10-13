import tempfile,unittest
from pathlib import Path
from brody_world_physique.image_forty_distinct_school_p136 import run,PROTOCOLS
class FortySchoolTests(unittest.TestCase):
 def test_protocols_are_unique_and_span_domains(self):
  self.assertEqual(len(PROTOCOLS),40)
  self.assertEqual(len({name for _,name in PROTOCOLS}),40)
  self.assertEqual(len({family for family,_ in PROTOCOLS}),8)
 def test_single_school_reports_all_competencies(self):
  with tempfile.TemporaryDirectory() as d:
   output=Path(d)/"school"
   result=run(output)
   self.assertEqual(result["total"],40)
   self.assertEqual(result["counts"]["TODO"],5)
   self.assertEqual(result["counts"]["FAIL"],0)
   self.assertEqual(result["counts"]["PASS"],35)
   self.assertTrue((output/"EVIDENCE.json").exists())
   self.assertFalse(result["real_world_generalization_proven"])
 def test_no_result_overwrite(self):
  with tempfile.TemporaryDirectory() as d:
   out=Path(d)/"result"
   run(out)
   with self.assertRaises(ValueError):run(out)
if __name__=="__main__":unittest.main()
