"""
Unit tests for MMX (Martian Moons eXploration) Mars Moon Phobos Sample-Return Astrodynamics Engine.
===================================================================================================
"""

import sys
import os
import math
from datetime import datetime, timezone, timedelta
import unittest

# Add scripts directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))

import mmx_phobos_sample_return_engine as engine
import bepicolombo_8th_anniversary_osiris_tag_engine as bepi_engine


class TestMMXPhobosSampleReturn(unittest.TestCase):
    def setUp(self):
        self.ref_now_utc = datetime(2026, 10, 19, 23, 20, 0, tzinfo=timezone.utc)
        self.ref_now_cst = datetime(2026, 10, 20, 7, 20, 0, tzinfo=timezone(timedelta(hours=8)))

    def test_mmx_launch_and_separation_timeline(self):
        """Verify launch epoch, separation milestone, and mission phase transition."""
        status_at_launch = engine.get_mmx_mission_status(engine.MMX_LAUNCH_UTC)
        self.assertTrue(status_at_launch["is_launched"])
        self.assertFalse(status_at_launch["is_separated"])
        self.assertEqual(status_at_launch["hours_since_launch"], 0.0)

        status_now = engine.get_mmx_mission_status(self.ref_now_utc)
        self.assertTrue(status_now["is_launched"])
        self.assertTrue(status_now["is_separated"])
        self.assertGreater(status_now["hours_since_launch"], 3.0)
        self.assertGreater(status_now["hours_since_separation"], 2.0)
        self.assertIn("Trans-Mars Injection", status_now["current_flight_phase"])

        # Countdowns
        self.assertGreater(status_now["days_to_mars_arrival"], 290.0)
        self.assertGreater(status_now["days_to_qso_entry"], 330.0)
        self.assertGreater(status_now["days_to_earth_return"], 1700.0)

    def test_mmx_mission_mass_properties(self):
        """Verify wet mass, propellant, dry mass, rover mass and sample targets."""
        status = engine.get_mmx_mission_status()
        self.assertEqual(status["wet_launch_mass_kg"], 4480.0)
        self.assertEqual(status["propellant_mass_kg"], 2100.0)
        self.assertEqual(status["dry_mass_kg"], 2380.0)
        self.assertEqual(status["idefix_rover_mass_kg"], 25.0)
        self.assertEqual(status["sample_target_min_grams"], 10.0)

    def test_phobos_hill_sphere_and_clearance(self):
        """
        Verify Phobos' Hill sphere radius (~16.6 km) and the razor-thin clearance
        above the physical surface, proving classical circular Keplerian orbits are impossible.
        """
        res = engine.compute_phobos_hill_sphere_and_qso_mechanics()
        self.assertGreater(res["phobos_hill_sphere_radius_km"], 16.0)
        self.assertLess(res["phobos_hill_sphere_radius_km"], 17.0)
        # Mean clearance is only ~5.5 km
        self.assertGreater(res["hill_clearance_mean_km"], 5.0)
        self.assertLess(res["hill_clearance_mean_km"], 6.0)
        # Long axis semi-major (13.4 km) leaves only ~3.2 km clearance
        self.assertGreater(res["hill_clearance_long_axis_km"], 2.5)
        self.assertLess(res["hill_clearance_long_axis_km"], 4.0)
        self.assertFalse(res["keplerian_circular_stable"])

    def test_mars_synchronous_and_decay_mechanics(self):
        """
        Verify Phobos orbits well inside Mars synchronous orbit radius (~20,400 km),
        causing tidal deceleration and secular inward spiraling.
        """
        res = engine.compute_phobos_hill_sphere_and_qso_mechanics()
        self.assertTrue(res["is_inside_synchronous_orbit"])
        self.assertTrue(res["secular_spiral_inward"])
        self.assertGreater(res["mars_synchronous_orbit_radius_km"], 20000.0)
        self.assertLess(res["phobos_orbital_period_hours"], 8.0)

    def test_qso_2_to_1_epicycle_geometry(self):
        """
        Verify Quasi-Satellite Orbit (QSO) 2:1 along-track to radial amplitude ratio
        derived from Hill-Clohessy-Wiltshire relative orbital dynamics.
        """
        res = engine.compute_phobos_hill_sphere_and_qso_mechanics()
        self.assertEqual(res["qso_aspect_ratio_along_to_radial"], 2.0)
        tiers = res["qso_tiers"]
        self.assertIn("QSO-H", tiers)
        self.assertEqual(tiers["QSO-H"]["along_track_amplitude_km"], 100.0)
        self.assertIn("QSO-M", tiers)
        self.assertEqual(tiers["QSO-M"]["along_track_amplitude_km"], 50.0)
        self.assertIn("QSO-L", tiers)
        self.assertEqual(tiers["QSO-L"]["along_track_amplitude_km"], 20.0)

    def test_idefix_microgravity_weight_and_kinematics(self):
        """
        Verify IDEFIX 25 kg rover surface weight on Phobos (~0.14 N) and ballistic hop dynamics.
        """
        mob = engine.compute_idefix_microgravity_mobility(rover_mass_kg=25.0)
        self.assertGreater(mob["surface_weight_newtons"], 0.13)
        self.assertLess(mob["surface_weight_newtons"], 0.16)
        # Equivalent to ~14.5 grams on Earth
        self.assertGreater(mob["earth_equivalent_mass_grams"], 13.0)
        self.assertLess(mob["earth_equivalent_mass_grams"], 16.0)
        self.assertGreater(mob["gravity_reduction_ratio"], 1700.0)
        self.assertGreater(mob["hop_flight_duration_seconds"], 15.0)
        self.assertGreater(mob["hop_flight_max_height_meters"], 0.20)
        self.assertTrue(mob["autonomous_uprighting_mechanism"])

    def test_phobos_martian_ejecta_fraction_yield(self):
        """
        Verify expected yield of ancient Martian crustal material within 10g Phobos sample.
        """
        ejecta = engine.compute_phobos_martian_ejecta_fraction(collected_mass_grams=10.0)
        self.assertEqual(ejecta["collected_sample_mass_grams"], 10.0)
        self.assertEqual(ejecta["martian_ejecta_nominal_mg"], 50.0)
        self.assertEqual(ejecta["martian_ejecta_min_mg"], 10.0)
        self.assertEqual(ejecta["martian_ejecta_max_mg"], 100.0)
        self.assertGreater(ejecta["estimated_10um_martian_grain_count"], 1000000)
        self.assertIn("Woomera", ejecta["return_location"])

    def test_solar_system_grand_octennial_confluence(self):
        """
        Verify confluence on 2026-10-20:
        MMX launch + BepiColombo 8th launch anniversary + OSIRIS-REx 6th TAG anniversary + Orionids countdown.
        """
        bepi = bepi_engine.get_bepicolombo_octennial_status(self.ref_now_utc)
        osiris = bepi_engine.get_osiris_tag_sexennial_status(self.ref_now_utc)
        orionids = bepi_engine.get_orionids_2026_countdown_status(self.ref_now_cst)
        mmx = engine.get_mmx_mission_status(self.ref_now_utc)

        self.assertTrue(bepi["is_8th_anniversary"])
        self.assertTrue(osiris["is_6th_anniversary"])
        self.assertLess(orionids["hours_to_peak_window"], 45.0)
        self.assertTrue(mmx["is_launched"])
        self.assertTrue(mmx["is_separated"])


if __name__ == "__main__":
    unittest.main()
