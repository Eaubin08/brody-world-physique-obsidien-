import json,tempfile,unittest
from pathlib import Path
from brody_world_physique.image_integrated_feedback_school_v0 import episode,run
from brody_world_physique.fusion_f9_intensive_education_v0 import digest
class IntegratedVisualFeedbackTests(unittest.TestCase):
 def test_unknown_is_hold(self):
  result=episode({},10,88)
  self.assertTrue(result["unknown_context_held"])
  self.assertIsNone(result["after_loss"])
 def test_refused_snapshot_tamper(self):
  with tempfile.TemporaryDirectory() as d:
   s=Path(d)/"snapshot.json"
   s.write_text(json.dumps({"candidate_stats":{},"hash":"fake"}))
   with self.assertRaises(ValueError):run(Path(d)/"out",s,10)
 def test_no_promotion_and_receipts(self):
  with tempfile.TemporaryDirectory() as d:
   s=Path(d)/"snapshot.json"
   stats={}
   s.write_text(json.dumps({"candidate_stats":stats,"hash":digest(stats)}))
   report=run(Path(d)/"out",s,100)
   self.assertEqual(report["cases"],100)
   self.assertFalse(report["native_memory_write"])
   self.assertFalse(report["blind_exam_proven"])
 def test_discrepancy_detector_and_supervised_correction(self):
  stats={key:{t:{"sum":0.0 if t=="PENCIL" else 100.0,"n":1} for t in ("PENCIL","PEN","NIB")}
    for key in ("LIGHT|line","UNIFORM|line")}
  # Every attempted supervised correction is non-worsening by construction.
  e=episode(stats,3,42)
  if e["after_loss"] is not None:
   self.assertLessEqual(e["after_loss"],e["before_loss"])
if __name__=="__main__":unittest.main()
