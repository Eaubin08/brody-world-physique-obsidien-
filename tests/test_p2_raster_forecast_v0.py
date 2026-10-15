"""Unit tests for past-only raster candidate and agreement gate."""
import unittest
from brody_world_physique.p2_raster_forecast_v0 import (
    raster_linear_forecast, raster_spatial_agreement,
)


class P2RasterTest(unittest.TestCase):
    def test_linear_future_from_past(self):
        past=[(0,1),(5,2),(10,3)]
        self.assertEqual(raster_linear_forecast(past,(0,6,12),18),[15,4])

    def test_hold_missing_raster(self):
        self.assertIsNone(raster_linear_forecast(None,(0,6,12),18))
        self.assertFalse(raster_spatial_agreement(None,[2,3]))

    def test_agreement_is_conservative(self):
        self.assertTrue(raster_spatial_agreement([3,4],[4,5]))
        self.assertFalse(raster_spatial_agreement([3,4],[30,50]))
        self.assertFalse(raster_spatial_agreement(None,[3,4]))

    def test_reject_future_or_mismatched_frames(self):
        with self.assertRaises(ValueError):
            raster_linear_forecast([(0,0),(1,1),(2,2)],(0,6,12),12)
        with self.assertRaises(ValueError):
            raster_linear_forecast([(0,0),(1,1),(2,2)],(0,6),18)


if __name__=="__main__":
    unittest.main()
