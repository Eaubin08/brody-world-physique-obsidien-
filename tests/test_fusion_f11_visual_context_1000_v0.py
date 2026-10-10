import json,tempfile,unittest
from pathlib import Path
from brody_world_physique.fusion_f11_visual_context_1000_v0 import (
    scene,features,decide,run)
from brody_world_physique.fusion_f9_intensive_education_v0 import verify_chain

class VisualContextTests(unittest.TestCase):
 def test_actual_pixel_cues_and_ambiguous_abstention(self):
  for cue in ("LEFT","RIGHT","BOTH","NONE"):
   im,_=scene(cue,"angle",123)
   self.assertEqual(features(im),cue)
  memory={"LEFT":{"OLD":7,"NEW":0},"RIGHT":{"OLD":0,"NEW":7}}
  self.assertEqual(decide(memory,features(scene("LEFT","line",3)[0]))["regime"],"OLD")
  self.assertEqual(decide(memory,features(scene("RIGHT","line",3)[0]))["regime"],"NEW")
  self.assertIsNone(decide(memory,"BOTH")["regime"])
  self.assertIsNone(decide(memory,"NONE")["regime"])
 def test_heldout_snapshots_and_receipts(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp)/"course";r=run(root,episodes=120,checkpoint=30)
   self.assertEqual(r["episodes"],120)
   self.assertEqual(len(r["checkpoints"]),4)
   self.assertEqual(verify_chain(root/"receipts.jsonl")[0],120)
   self.assertTrue(r["inference_from_pixels"])
   self.assertFalse(r["native_memory_write"])
   first=r["checkpoints"][0]["scores"]
   self.assertEqual(first["evaluated"],80)
   self.assertGreater(first["holds_ambiguous"],0)
   with self.assertRaises(ValueError):run(root,episodes=120)
 def test_untrained_or_conflicting_evidence_causes_hold(self):
  self.assertIsNone(decide({},"LEFT")["regime"])
  self.assertIsNone(decide({"LEFT":{"OLD":5,"NEW":5}},"LEFT")["regime"])

if __name__=="__main__":unittest.main()
