import unittest
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR / "scripts"))

from hunters_moon_shenzhou17_cassini_engine import (
    compute_hunters_moon_ephemeris,
    compute_shenzhou17_metrics,
    compute_cassini_titan_ta_metrics,
    synthesize_october26_celestial_overview
)

class TestHuntersMoonAndMilestones2026(unittest.TestCase):
    def test_hunters_moon_ephemeris(self):
        """Test the Hunter's moon distance, angular size and phase on 2026-10-26."""
        eph = compute_hunters_moon_ephemeris("2026/10/26 04:11:44")
        self.assertAlmostEqual(eph["distance_km"], 373104.4, delta=100.0)
        self.assertAlmostEqual(eph["angular_diameter_arcmin"], 32.06, delta=0.5)
        self.assertGreater(eph["phase_percent"], 99.5)
        self.assertGreater(eph["elongation_deg"], 175.0)

    def test_shenzhou17_metrics(self):
        """Test Shenzhou-17 triennial anniversary parameters."""
        sz = compute_shenzhou17_metrics("2026-10-26")
        self.assertEqual(sz["anniversary_order"], 3)
        self.assertEqual(sz["in_orbit_days"], 187)
        self.assertEqual(len(sz["crew"]), 3)
        self.assertIn("Tang Hongbo", sz["crew"])
        self.assertAlmostEqual(sz["elapsed_years"], 3.0, delta=0.05)
        self.assertIn("solar array repair", sz["key_feat"])

    def test_cassini_titan_ta_metrics(self):
        """Test Cassini Titan Ta flyby 22nd anniversary parameters."""
        cassini = compute_cassini_titan_ta_metrics("2026-10-26")
        self.assertEqual(cassini["anniversary_order"], 22)
        self.assertAlmostEqual(cassini["elapsed_years"], 22.0, delta=0.05)
        self.assertEqual(cassini["closest_approach_alt_km"], 1174.0)
        self.assertAlmostEqual(cassini["relative_speed_kms"], 6.06, delta=0.1)
        self.assertEqual(cassini["radar_frequency_ghz"], 13.78)

    def test_synthesized_overview(self):
        """Test overall synthesis dictionary structure."""
        synth = synthesize_october26_celestial_overview()
        self.assertEqual(synth["date"], "2026-10-26")
        self.assertEqual(synth["lunar_calendar"], "农历九月十七")
        self.assertIn("12:11:44 CST", synth["full_moon_cst"])
        self.assertEqual(synth["shenzhou17_anniversary"]["anniversary_order"], 3)
        self.assertEqual(synth["cassini_titan_anniversary"]["anniversary_order"], 22)

if __name__ == "__main__":
    unittest.main()
