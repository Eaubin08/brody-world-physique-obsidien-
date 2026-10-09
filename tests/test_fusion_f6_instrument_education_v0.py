import tempfile,unittest,json
from pathlib import Path
from brody_world_physique.fusion_f6_instrument_education_v0 import run
from brody_world_physique.fusion_f4_education_journal_v0 import verify_journal
class InstrumentIntegrationTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.temp=tempfile.TemporaryDirectory()
  cls.root=Path(cls.temp.name)/"course"
  cls.report=run(cls.root)
 @classmethod
 def tearDownClass(cls):
  cls.temp.cleanup()
 def test_three_instruments_and_heldout_hold(self):
  rows=self.report["rows"]
  self.assertEqual([r["instrument"] for r in rows],["PENCIL","PEN","NIB",None])
  self.assertEqual(self.report["known_proposals"],3)
  self.assertEqual(self.report["holds"],1)
  self.assertTrue(all(not r["target_used_for_selection"] for r in rows))
  self.assertFalse(self.report["semantic_tool_understanding_proven"])
 def test_sealed_candidate_and_persistent_visual_memory(self):
  for i,shape in enumerate(("rectangle","triangle","ellipse"),1):
   folder=self.root/("exam-%02d-%s"%(i,shape))
   self.assertTrue((folder/"candidate.png").is_file())
   self.assertTrue((folder/"comparison.png").is_file())
   receipt=json.loads((folder/"sealed_choice.json").read_text())
   self.assertTrue(receipt["target_read_before_seal"] is False)
  self.assertEqual(len(verify_journal(self.root/"visual")),10)
 def test_unchanged_output_refusal(self):
  with self.assertRaises(ValueError):run(self.root)
if __name__=="__main__":unittest.main()
