import json,tempfile,unittest
from pathlib import Path
from brody_world_physique.fusion_f7_train_only_correction_v0 import run
from brody_world_physique.fusion_f4_education_journal_v0 import verify_journal
class CorrectionTests(unittest.TestCase):
 def test_train_correction_changes_frozen_policy_on_unseen_geometry(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)/"lesson"
   result=run(root)
   self.assertEqual((result["old_tool"],result["new_tool"]),("PENCIL","PEN"))
   self.assertTrue(result["better_on_this_test"])
   self.assertGreater(result["old_test_loss"],result["new_test_loss"])
   self.assertEqual(result["new_test_loss"],0.0)
   self.assertEqual(result["journal_events"],3)
   self.assertEqual(len(verify_journal(root)),3)
   self.assertTrue((root/"v001.json").is_file())
   self.assertTrue((root/"v002.json").is_file())
   self.assertTrue((root/"sealed-before-test.json").is_file())
   self.assertFalse(result["native_memory_write"])
 def test_no_overwrite_and_history_tamper_detection(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)/"lesson";run(root)
   with self.assertRaises(ValueError):run(root)
   path=root/"education"/"event-0002.json"
   event=json.loads(path.read_text())
   event["payload"]["old_tool"]="PEN"
   path.write_text(json.dumps(event))
   with self.assertRaises(ValueError):verify_journal(root)
if __name__=="__main__":unittest.main()
