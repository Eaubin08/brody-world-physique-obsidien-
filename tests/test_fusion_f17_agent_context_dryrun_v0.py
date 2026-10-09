import tempfile,unittest,json
from pathlib import Path
from brody_world_physique.fusion_f17_agent_context_dryrun_v0 import run
class F17Tests(unittest.TestCase):
 def test_missing_input_fails_closed(self):
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaises(ValueError):run(Path(d)/"none",d,Path(d)/"out")
 def test_no_fake_runtime_contract(self):
  with tempfile.TemporaryDirectory() as d:
   base=Path(d);source=base/"packets.jsonl"
   source.write_text(json.dumps({"domain":"brody_image","recommended_gate":"HOLD","can_emit_act":False})+"\n")
   with self.assertRaises(RuntimeError):run(source,d,base/"out")
if __name__=="__main__":unittest.main()
