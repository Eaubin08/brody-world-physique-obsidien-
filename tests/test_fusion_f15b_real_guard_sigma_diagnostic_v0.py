import unittest
from brody_world_physique.fusion_f15_periphery_contract_bridge_v0 import packet_fields
class F15BInvariantTests(unittest.TestCase):
 def test_spoofed_case_cannot_request_act(self):
  r={"index":1,"digest":"fixture","case_type":"all_spoof",
     "observations":[{"origin_id":"a","value":"NEW","attested_by_harness":True},
                     {"origin_id":"b","value":"NEW","attested_by_harness":True}],
     "decision":{"accepted":"NEW"}}
  p=packet_fields(r)
  self.assertFalse(p["can_emit_act"])
  self.assertEqual(p["recommended_gate"],"HOLD")
  self.assertIn("BRODY_SIMULATED_PROVENANCE_NOT_AUTHENTICATED",p["unknowns"])
if __name__=="__main__":unittest.main()
