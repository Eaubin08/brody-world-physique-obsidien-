import tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
from brody_world_physique.image_visual_reflex_teacher_loop_v1 import run
class VisualReflexLoopTests(unittest.TestCase):
 def test_pause_resume_and_stabilization(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);sources=root/"sources";sources.mkdir()
   for i in range(4):
    im=Image.new("L",(64,64),255)
    ImageDraw.Draw(im).line((8,i+10,53,i+40),fill=0,width=3)
    im.save(sources/(f"example{i}.png"))
   first=run(sources,root/"training",interrupt_after=2)
   self.assertEqual(first["status"],"PAUSED_CHECKPOINTED")
   final=run(sources,root/"training")
   self.assertEqual(final["lessons"],4)
   self.assertTrue((root/"training"/"knowledge_candidates_snapshot.json").exists())
   self.assertFalse(final["native_memory_write"])
   again=run(sources,root/"training")
   self.assertEqual(again["receipt_tip"],final["receipt_tip"])
 def test_duplicate_images_not_recounted_as_lessons(self):
  with tempfile.TemporaryDirectory() as d:
   import json
   r=Path(d);p=r/"source";p.mkdir()
   im=Image.new("L",(64,64),255)
   ImageDraw.Draw(im).line((8,8,52,47),fill=0,width=3)
   for i in range(5):im.save(p/(f"repeat{i}.png"))
   result=run(p,r/"out")
   self.assertEqual(result["lessons"],5)
   state=json.loads((r/"out"/"knowledge_candidates_snapshot.json").read_text())["state"]
   self.assertEqual(sum(len(x["lessons"]) for x in state["concepts"].values()),1)
   self.assertEqual(result["stable"],0)
   rows=[json.loads(line) for line in (r/"out"/"receipts.jsonl").read_text().splitlines()]
   self.assertEqual(sum(x["duplicate_evidence_skipped"] for x in rows),4)
 def test_corrupted_checkpoint_fails_closed(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);p=root/"source";p.mkdir()
   Image.new("L",(64,64),255).save(p/"one.png")
   run(p,root/"out",interrupt_after=1)
   checkpoint=root/"out"/"checkpoint.json"
   checkpoint.write_text(checkpoint.read_text().replace('"completed": 1','"completed": 3'))
   with self.assertRaises(ValueError):run(p,root/"out")
if __name__=="__main__":unittest.main()
