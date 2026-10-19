"""
Unit tests for BepiColombo 8th Launch Anniversary & OSIRIS-REx Bennu TAG 6th Anniversary
Celestial Mechanics & 2026 Orionids 24-Hour Countdown Engine.
"""

import sys
import os
import unittest
import datetime

# Add scripts directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))

import bepicolombo_8th_anniversary_osiris_tag_engine as engine


class TestBepiColomboOsirisOrionidsEngine(unittest.TestCase):
    def setUp(self):
        self.ref_utc = datetime.datetime(2026, 10, 20, 3, 5, 0, tzinfo=datetime.timezone.utc)
        self.ref_cst = datetime.datetime(2026, 10, 20, 11, 5, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=8)))
        self.bepi_status = engine.get_bepicolombo_octennial_status(self.ref_utc)
        self.bepi_moi = engine.compute_bepicolombo_orbital_insertion_mechanics()
        self.osiris_status = engine.get_osiris_tag_sexennial_status(self.ref_utc)
        self.orionids_status = engine.get_orionids_2026_countdown_status(self.ref_cst)

    def test_bepicolombo_8th_anniversary_status(self):
        """Asserts BepiColombo 8.00 Julian years in space and mission countdowns."""
        self.assertTrue(self.bepi_status["is_8th_anniversary"])
        self.assertAlmostEqual(self.bepi_status["julian_years_since_launch"], 8.00, delta=0.01)
        self.assertGreater(self.bepi_status["days_since_launch"], 2921.0)
        self.assertLess(self.bepi_status["days_since_launch"], 2923.0)
        self.assertGreater(self.bepi_status["days_to_moi"], 31.0)
        self.assertLess(self.bepi_status["days_to_moi"], 33.0)
        self.assertGreater(self.bepi_status["days_since_mtm_sep"], 46.0)
        self.assertLess(self.bepi_status["days_since_mtm_sep"], 48.0)
        self.assertEqual(self.bepi_status["total_flybys"], 9)
        self.assertEqual(self.bepi_status["mercury_flybys"], 6)

    def test_bepicolombo_mass_amplification(self):
        """Asserts MTM separation mass reduction and thrust-to-mass acceleration multiplier."""
        self.assertEqual(self.bepi_status["launch_mass_kg"], 4121.0)
        self.assertEqual(self.bepi_status["jettisoned_mtm_mass_kg"], 1861.0)
        self.assertEqual(self.bepi_status["post_sep_stack_mass_kg"], 2260.0)
        self.assertGreater(self.bepi_status["thrust_to_mass_amplification"], 1.80)
        self.assertAlmostEqual(self.bepi_status["post_sep_tcm_dv_ms"], 11.4, delta=0.1)

    def test_bepicolombo_moi_kinematics(self):
        """Asserts capture velocities and orbital insertion parameters."""
        self.assertAlmostEqual(self.bepi_moi["periapsis_radius_km"], 2919.7, delta=0.2)
        self.assertAlmostEqual(self.bepi_moi["v_escape_periapsis_kms"], 3.885, delta=0.01)
        self.assertAlmostEqual(self.bepi_moi["v_hyperbolic_periapsis_kms"], 4.299, delta=0.01)
        self.assertAlmostEqual(self.bepi_moi["v_capture_periapsis_kms"], 3.853, delta=0.01)
        self.assertAlmostEqual(self.bepi_moi["delta_v_capture_ms"], 445.2, delta=2.0)

    def test_bepicolombo_gravity_assist_savings(self):
        """Asserts that 9 flybys saved >6000 m/s compared to direct transfer."""
        self.assertGreater(self.bepi_moi["delta_v_direct_hohmann_ms"], 6500.0)
        self.assertGreater(self.bepi_moi["delta_v_saved_ms"], 6000.0)
        self.assertGreater(self.bepi_moi["gravity_assist_savings_percent"], 93.0)

    def test_dual_orbiter_final_orbits(self):
        """Asserts ESA MPO and JAXA Mio target orbital periods."""
        self.assertAlmostEqual(self.bepi_moi["mpo_period_hours"], 2.32, delta=0.05)
        self.assertAlmostEqual(self.bepi_moi["mio_period_hours"], 9.32, delta=0.05)

    def test_osiris_tag_6th_anniversary(self):
        """Asserts OSIRIS-REx 6.00 Julian years since Bennu Nightingale TAG."""
        self.assertTrue(self.osiris_status["is_6th_anniversary"])
        self.assertAlmostEqual(self.osiris_status["julian_years_since_tag"], 6.00, delta=0.01)
        self.assertEqual(self.osiris_status["sample_mass_collected_grams"], 121.6)
        self.assertGreater(self.osiris_status["sample_mass_collected_grams"], self.osiris_status["sample_target_grams"])

    def test_osiris_apex_apophis_transition(self):
        """Asserts OSIRIS-APEX extended mission parameters and 0.50 AU thermal flux."""
        self.assertEqual(self.osiris_status["target_asteroid"], "(99942) Apophis")
        self.assertGreater(self.osiris_status["days_to_apophis_rendezvous"], 900.0)
        self.assertAlmostEqual(self.osiris_status["perihelion_solar_flux_wm2"], 5444.0, delta=10.0)
        self.assertEqual(self.osiris_status["flux_ratio_to_earth"], 4.0)

    def test_orionids_countdown_and_kinematics(self):
        """Asserts 2026 Orionids meteor shower countdown and velocities."""
        self.assertEqual(self.orionids_status["parent_comet"], "1P/Halley (哈雷彗星)")
        self.assertEqual(self.orionids_status["geocentric_velocity_kms"], 66.0)
        self.assertGreater(self.orionids_status["hours_to_peak_window"], 30.0)
        self.assertLess(self.orionids_status["hours_to_peak_window"], 40.0)
        self.assertAlmostEqual(self.orionids_status["oct20_moon_illum_percent"], 68.3, delta=0.5)


if __name__ == "__main__":
    unittest.main()
