import tempfile,unittest
from pathlib import Path
from brody_world_physique.hard_scene_angles_p165d2 import draw
from brody_world_physique.image_persistent_tracks_p165d5 import associate,adjudicate,run
class P165D5Tests(unittest.TestCase):
 def test_image_only_path_candidates(self):
  s=dict(angle=0,motion="linear",occlusion="none",appearance="blue",background="plain")
  images,_=draw(s,52)
  try:
   d=associate(images)
   self.assertEqual(len(d["candidate_counts"]),7)
   self.assertFalse(d["uses_oracle"])
   self.assertTrue(d["tracks"])
  finally:
   for im in images:im.close()
 def test_multiple_objects_not_unique_identity(self):
  s=dict(angle=25,motion="jump",occlusion="full",appearance="red",background="parallax")
  images,_=draw(s,53)
  try:
   d=adjudicate(associate(images))
   self.assertFalse(d.get("unique_identity_proven",False))
   self.assertIn(d["status"],("MULTI","HOLD","CANDIDATE"))
  finally:
   for im in images:im.close()
 def test_preserved_evidence_and_bounded_beam(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/"exam"
   report=run(p,seeds=2,limit=6,beam=4)
   self.assertEqual(report["episodes"],12)
   self.assertFalse(report["inference_receives_truth"])
   self.assertTrue((p/"EXAMS.jsonl").is_file())
   with self.assertRaises(ValueError):run(p,seeds=2,limit=6,beam=4)
if __name__=="__main__":unittest.main()
