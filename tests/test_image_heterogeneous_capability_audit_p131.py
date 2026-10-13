import json,tempfile,unittest
from pathlib import Path
from brody_world_physique.image_heterogeneous_capability_audit_p131 import run
class P131HeterogeneousTests(unittest.TestCase):
 def test_multidomain_probe_reports_real_limits(self):
  with tempfile.TemporaryDirectory() as d:
   report=run(Path(d)/"probe")
   self.assertGreaterEqual(report["domains"],7)
   self.assertEqual(report["distinct_probes"],16)
   self.assertEqual(report["counts"]["TODO"],8)
   self.assertFalse(report["real_world_transfer_proven"])
   self.assertEqual(report["counts"]["FAIL"],0)
   self.assertEqual(report["counts"]["PASS"],8)
 def test_preserve_evidence(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"probe";run(p)
   with self.assertRaises(ValueError):run(p)
if __name__=="__main__":unittest.main()
