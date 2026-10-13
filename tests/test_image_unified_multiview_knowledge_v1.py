import json,tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
from brody_world_physique.image_unified_multiview_knowledge_v1 import build
class UnifiedKnowledgeTests(unittest.TestCase):
 def test_one_identity_four_views_and_integrity(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d);src=r/"a.png"
   im=Image.new("L",(64,64),255);ImageDraw.Draw(im).rectangle((4,6,27,43),outline=0,width=2);im.save(src)
   m=r/"manifest.json";m.write_text(json.dumps({"identity":"A","examples":[str(src)]}))
   result=build(m,r/"out")
   self.assertEqual(result["identities"],1)
   self.assertEqual(result["observations"],4)
   self.assertEqual(result["relations"],4)
   graph=json.loads((r/"out"/"knowledge_graph_candidates.json").read_text())
   self.assertEqual(set(x["role"] for x in graph["observations"].values()),{"LESSON","EXAM"})
   self.assertFalse(graph["identities"]["A"]["semantic_identity_verified"])
   self.assertEqual(graph["identities"]["A"]["procedural_state"],"LEARNING")
   self.assertFalse(result["native_memory_write"])
 def test_duplicate_identity_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d);m=r/"m.json"
   m.write_text(json.dumps([{"identity":"A","examples":["missing"]},{"identity":"A","examples":["missing"]}]))
   with self.assertRaises(ValueError):build(m,r/"out")
   self.assertFalse((r/"out").exists())
if __name__=="__main__":unittest.main()
