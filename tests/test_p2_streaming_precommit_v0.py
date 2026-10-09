"""P2.3 tests for precommit arm inputs and conservative HOLD."""
import unittest
from brody_world_physique.p2_streaming_precommit_v0 import _predictions, ARMS


class P2StreamingTest(unittest.TestCase):
    def test_past_only_inputs_and_fusion(self):
        pts=[[0.0,10.0],[6.0,10.0],[12.0,10.0]]
        result=_predictions(pts,pts,(0,6,12))
        self.assertEqual(set(result),set(ARMS))
        self.assertEqual(result["A1_linear_kinematics"],[18.0,10.0])
        self.assertEqual(result["A3_raster_only"],[18.0,10.0])
        self.assertEqual(result["A6_raster_spatial_fixed_fusion"],[18.0,10.0])

    def test_fusion_holds_when_raster_disagrees(self):
        s=[[0.0,10.0],[6.0,10.0],[12.0,10.0]]
        r=[[0.0,10.0],[6.0,10.0],[100.0,10.0]]
        result=_predictions(s,r,(0,6,12))
        self.assertIsNone(result["A6_raster_spatial_fixed_fusion"])
        self.assertIsNotNone(result["A1_linear_kinematics"])

    def test_invalid_or_unknown_input(self):
        self.assertTrue(all(x is None for x in _predictions([None,[1,1],[2,2]],
                            [[0,0],[1,1],[2,2]],(0,6,12)).values()))
        with self.assertRaises(ValueError):
            _predictions([[0,0],[1,1]],[[0,0],[1,1]],(0,6))


if __name__=="__main__":
    unittest.main()
