import unittest
from brody_world_physique.fusion_f15_periphery_contract_bridge_v0 import packet_fields
class F15ContractTests(unittest.TestCase):
 def test_spoof_never_emits_action(self):
  r={"index":1,"digest":"abc","case_type":"all_spoof",
     "observations":[{"origin_id":"a","value":"NEW","attested_by_harness":True},
                     {"origin_id":"b","value":"NEW","attested_by_harness":True}],
     "decision":{"accepted":"NEW"}}
  p=packet_fields(r)
  self.assertFalse(p["can_emit_act"])
  self.assertEqual(p["recommended_gate"],"HOLD")
  self.assertIn("BRODY_SIMULATED_PROVENANCE_NOT_AUTHENTICATED",p["unknowns"])
  self.assertIn("BRODY_COORDINATED_SPOOFING_TEST_CASE",p["risk_flags"])
 def test_missing_independence_is_explicit(self):
  r={"index":2,"digest":"def","case_type":"shared_origin",
     "observations":[{"origin_id":"same","value":"OLD","attested_by_harness":True},
                     {"origin_id":"same","value":"OLD","attested_by_harness":True}],
     "decision":{"accepted":None}}
  self.assertIn("BRODY_INDEPENDENCE_NOT_ESTABLISHED",packet_fields(r)["unknowns"])
 def test_contradiction_is_transferred(self):
  r={"index":3,"digest":"ghi","case_type":"conflict",
     "observations":[{"origin_id":"a","value":"OLD","attested_by_harness":True},
                     {"origin_id":"b","value":"NEW","attested_by_harness":True}],
     "decision":{"accepted":None}}
  self.assertIn("BRODY_OBSERVATION_CONTRADICTION",packet_fields(r)["contradictions"])
if __name__=="__main__":unittest.main()
