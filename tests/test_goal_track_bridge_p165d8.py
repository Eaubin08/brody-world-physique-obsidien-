import tempfile,unittest
from pathlib import Path
from brody_world_physique.hard_scene_angles_p165d2 import draw
from brody_world_physique.goal_track_bridge_p165d8 import views_from_frames,run,GOALS
class D8Tests(unittest.TestCase):
 def test_different_goals_do_not_mutate_evidence(self):
  s=dict(angle=0,motion="linear",occlusion="none",appearance="red",background="plain")
  ims,_=draw(s,42)
  try:
   r=views_from_frames(ims)
   self.assertTrue(r["unchanged_under_goals"])
   self.assertNotEqual(r["views"]["LOCATE"]["focused"],r["views"]["REIDENTIFY"]["focused"])
   self.assertEqual(len(r["views"]),len(GOALS))
  finally:
   for im in ims:im.close()
 def test_symbol_without_user_interpretation_holds(self):
  s=dict(angle=0,motion="still",occlusion="full",appearance="blue",background="plain")
  ims,_=draw(s,43)
  try:self.assertEqual(views_from_frames(ims)["views"]["INTERPRET_SYMBOL"]["status"],"HOLD")
  finally:
   for im in ims:im.close()
 def test_repeatability(self):
  s=dict(angle=25,motion="jump",occlusion="partial",appearance="change",background="parallax")
  ims,_=draw(s,77)
  try:
   a=views_from_frames(ims);b=views_from_frames(ims)
   self.assertEqual(a["digest"],b["digest"])
   self.assertEqual(a["views"]["EXPLORE"] if "EXPLORE" in a["views"] else a["views"]["LOCATE"],
                    b["views"]["EXPLORE"] if "EXPLORE" in b["views"] else b["views"]["LOCATE"])
  finally:
   for im in ims:im.close()
 def test_evidence_no_overwrite(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/"run"
   r=run(p,seeds=1,limit=3,beam=4)
   self.assertEqual(r["episodes"],3)
   self.assertTrue((p/"EXAMS.jsonl").exists())
   with self.assertRaises(ValueError):run(p,seeds=1,limit=3,beam=4)
if __name__=="__main__":unittest.main()
