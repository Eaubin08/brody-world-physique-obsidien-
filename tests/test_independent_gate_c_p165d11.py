import tempfile,unittest
from pathlib import Path
from brody_world_physique.independent_gate_c_p165d11 import KINDS,render,run
from brody_world_physique.reappearance_gate_p165d6 import infer,evaluate_tracks
class GateCTests(unittest.TestCase):
 def test_unique_families(self):
  self.assertEqual(len(KINDS),10);self.assertEqual(len(KINDS),len(set(KINDS)))
 def test_renderer_finite_and_seven_frames(self):
  for kind in KINDS:
   frames,truth=render(kind,71)
   try:
    self.assertEqual(len(frames),7);self.assertEqual(len(truth),7)
    self.assertTrue(all(0<=x<168 for x in truth))
   finally:
    for im in frames:im.close()
 def test_replay_identical_seed(self):
  a,at=render("abrupt_jump",99);b,bt=render("abrupt_jump",99)
  try:
   self.assertEqual(at,bt)
   self.assertEqual([im.tobytes() for im in a],[im.tobytes() for im in b])
  finally:
   for im in a+b:im.close()
 def test_change_in_law_is_not_merely_metadata(self):
  a,at=render("abrupt_jump",99);b,bt=render("abrupt_brake",99)
  try:self.assertNotEqual(at,bt)
  finally:
   for im in a+b:im.close()
 def test_synthetic_counterfactual_keeps_uncertainty(self):
  frames,truth=render("indistinguishable_crossing",42)
  try:
   result=infer(frames,beam=8)
   self.assertFalse(result["unique_identity_proven"])
   self.assertFalse(result["fixture_label_used"])
  finally:
   for im in frames:im.close()
 def test_raster_visibility_not_truth_inference(self):
  frames,truth=render("long_occlusion",48)
  try:
   result=infer(frames,beam=8)
   self.assertTrue(result["raw"]["tracks"])
   scored=evaluate_tracks(result["raw"]["tracks"],truth)
   self.assertTrue(scored["oracle_for_scoring_only"])
  finally:
   for im in frames:im.close()
 def test_report_no_overwrite(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/"gate"
   report=run(p,seeds=2,beam=4)
   self.assertEqual(report["episodes"],20)
   self.assertEqual(len(report["families"]),10)
   self.assertTrue((p/"EXAMS.jsonl").exists())
   with self.assertRaises(ValueError):run(p,seeds=2,beam=4)
if __name__=="__main__":unittest.main()
