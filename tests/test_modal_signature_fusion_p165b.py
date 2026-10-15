import tempfile,unittest
from pathlib import Path
from brody_world_physique.modal_signature_fusion_p165b import obs,compare,identity,scene,run,CASES,MODES
class P165BTests(unittest.TestCase):
 def test_changed_color_does_not_erase_other_signatures(self):
  a,b=scene("color_changed");v=identity(a,b)
  self.assertEqual(v["status"],"MULTI")
  self.assertIn("RGB",v["conflicts"])
  self.assertIn("THERMAL",v["votes"])
  self.assertFalse(v["identity_proven"])
 def test_conflicting_sensor_is_not_silently_ignored(self):
  v=identity(*scene("thermal_contradiction"))
  self.assertEqual(v["status"],"MULTI")
  self.assertIn("THERMAL",v["conflicts"])
 def test_generated_evidence_cannot_validate_itself(self):
  v=identity(*scene("generated_forgery"))
  self.assertEqual(v["status"],"HOLD")
  self.assertFalse(v["votes"])
 def test_time_and_frame_mismatch_hold(self):
  for case in ("time_mismatch","camera_frame_mismatch"):
   self.assertEqual(identity(*scene(case))["status"],"HOLD")
 def test_same_signature_is_not_unique_id_proof(self):
  v=identity(*scene("same_signature_distinct_entities"))
  self.assertEqual(v["status"],"SUPPORTED_CANDIDATE")
  self.assertFalse(v["identity_proven"])
 def test_absence_sensor_is_hold(self):
  self.assertEqual(identity(*scene("no_sensor_available"))["status"],"HOLD")
 def test_no_overwrite_and_matrix(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/"proof";report=run(p)
   self.assertEqual(report["cases_completed"],len(CASES))
   self.assertFalse(report["real_sensor_connected"])
   self.assertEqual(report["false_identity_proofs"],0)
   with self.assertRaises(ValueError):run(p)
if __name__=="__main__":unittest.main()
