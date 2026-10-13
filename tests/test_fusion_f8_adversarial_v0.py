"""Adversarial F8 checks: conflicting evidence, abstention, immutable historic skills."""
import tempfile,unittest,json
from pathlib import Path
from brody_world_physique.instrument_school_v2 import select_tool,TOOLS,UNFAMILIAR
from brody_world_physique.fusion_f5_multiskill_course_v0 import course,route
from brody_world_physique.fusion_f4_education_journal_v0 import verify_journal
from brody_world_physique.fusion_f3c_cumulative_skill_archive_v0 import load_registry
from brody_world_physique.fusion_f7_train_only_correction_v0 import run as correction

class AdversarialEducationTests(unittest.TestCase):
 def test_conflicting_training_overrides_preconception(self):
  examples=({"id":"first","goal":"LIGHT",
             "trial_losses":{"PENCIL":1.,"PEN":8.,"NIB":9.}},)
  self.assertEqual(select_tool(examples,"LIGHT")["chosen_tool"],"PENCIL")
  later=({"id":"second","goal":"LIGHT",
          "trial_losses":{"PENCIL":200.,"PEN":0.,"NIB":100.}},)
  self.assertEqual(select_tool(examples+later,"LIGHT")["chosen_tool"],"PEN")
  self.assertIsNone(select_tool(examples,UNFAMILIAR)["chosen_tool"])
 def test_malformed_training_fails_closed(self):
  with self.assertRaises(ValueError):
   select_tool(({"id":"bad","goal":"LIGHT","trial_losses":{"PENCIL":1}},),"LIGHT")
  with self.assertRaises(ValueError):
   select_tool(({"id":"bad","goal":"LIGHT","trial_losses":
                 {"PENCIL":-1,"PEN":2,"NIB":3}},),"LIGHT")
 def test_prior_snapshot_and_unknown_remain_held(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp)/"course";course(root)
   self.assertEqual(route(root,1,"triangle")["authority"],"HOLD")
   self.assertEqual(route(root,2,"ellipse")["authority"],"HOLD")
   self.assertEqual(route(root,3,"unknown")["authority"],"HOLD")
   self.assertEqual(len(load_registry(root,3)["skills"]),3)
   self.assertEqual(len(verify_journal(root)),6)
 def test_trained_correction_not_universal(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp)/"lesson";s=correction(root)
   self.assertTrue(s["better_on_this_test"])
   self.assertTrue(s["teacher_synthetic_shared_renderer"])
   self.assertTrue(s["not_generalization_proof"])
   self.assertEqual(s["correction_type"],"INSTRUMENT_ROUTING_NOT_GESTURE_REFINEMENT")
   self.assertTrue((root/"v001.json").exists())
   self.assertTrue((root/"v002.json").exists())
if __name__=="__main__":unittest.main()
