"""
Unit tests for ESCAPADE Twin Probes (Blue & Gold), Loiter-Oberth Trajectory &
The Grand Quinquagintet (50-Probe Fleet).
"""

import sys
import os
import unittest
import datetime

# Add scripts directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))

import escapade_blue_gold_grand_quinquagintet_engine as engine


class TestEscapadeGrandQuinquagintet(unittest.TestCase):
    def setUp(self):
        self.ref_utc = datetime.datetime(2026, 10, 19, 12, 0, 0, tzinfo=datetime.timezone.utc)
        self.status = engine.get_escapade_mission_status(self.ref_utc)
        self.oberth = engine.compute_oberth_maneuver(perigee_alt_km=500.0, v_inf_kms=3.0)
        self.fleet = engine.get_grand_quinquagintet_fleet()
        self.extremes = engine.compute_fleet_extremes()

    def test_escapade_mission_timeline(self):
        """Asserts launch date, elapsed days in space, and future milestones."""
        self.assertEqual(self.status["launch_date_utc"], "2025-11-13 20:55:00 UTC")
        self.assertGreater(self.status["days_in_space"], 338.0)
        self.assertLess(self.status["days_in_space"], 342.0)
        self.assertGreater(self.status["days_to_perigee_oberth"], 20.0)
        self.assertLess(self.status["days_to_perigee_oberth"], 35.0)
        self.assertGreater(self.status["days_to_mars_arrival"], 320.0)
        self.assertLess(self.status["days_to_mars_arrival"], 340.0)

    def test_escapade_spacecraft_specs(self):
        """Asserts twin probe naming, mass specs, builder, and PI institution."""
        self.assertEqual(len(self.status["twin_spacecraft"]), 2)
        self.assertIn("ESCAPADE A (Blue)", self.status["twin_spacecraft"])
        self.assertIn("ESCAPADE B (Gold)", self.status["twin_spacecraft"])
        self.assertEqual(self.status["spacecraft_bus"], "Rocket Lab Photon")
        self.assertEqual(self.status["pi_institution"], "UC Berkeley Space Sciences Laboratory (SSL)")
        self.assertEqual(self.status["principal_investigator"], "Robert Lillis")
        self.assertEqual(self.status["dry_mass_kg_each"], 209.0)
        self.assertEqual(self.status["wet_mass_kg_each"], 535.0)
        self.assertEqual(self.status["total_launch_mass_kg"], 1070.0)

    def test_loiter_orbit_geometry(self):
        """Asserts Sun-Earth L2 loiter orbit characteristics and distance."""
        self.assertIn("Sun-Earth L2", self.status["mission_phase"])
        self.assertAlmostEqual(self.status["heliocentric_au"], 1.008, delta=0.01)
        self.assertGreater(self.status["current_distance_earth_km"], 1.0e6)
        self.assertGreater(self.status["current_distance_earth_re"], 200.0)

    def test_oberth_maneuver_kinematics(self):
        """Asserts orbital velocities and impulsive delta-V at 500 km perigee."""
        self.assertAlmostEqual(self.oberth["r_p_km"], 6878.137, delta=0.01)
        self.assertAlmostEqual(self.oberth["v_circular_kms"], 7.6125, delta=0.01)
        self.assertAlmostEqual(self.oberth["v_escape_kms"], 10.7659, delta=0.01)
        self.assertAlmostEqual(self.oberth["v_hyperbolic_perigee_kms"], 11.176, delta=0.02)
        self.assertAlmostEqual(self.oberth["delta_v_oberth_ms"], 410.2, delta=2.0)
        self.assertAlmostEqual(self.oberth["c3_km2_s2"], 9.0, delta=0.1)

    def test_oberth_amplification_efficiency(self):
        """Asserts Oberth delta-V amplification factor and energy gain."""
        self.assertGreater(self.oberth["oberth_amplification_factor"], 7.0)
        self.assertLess(self.oberth["oberth_amplification_factor"], 7.6)
        self.assertAlmostEqual(self.oberth["specific_energy_gain_mj_kg"], 4.5, delta=0.1)

    def test_science_payload_suite(self):
        """Asserts 4 science payloads and their respective developer institutions."""
        payloads = engine.get_science_payload_specs()
        self.assertEqual(len(payloads), 4)
        names = [p["name"] for p in payloads]
        self.assertTrue(any("EMM" in n for n in names))
        self.assertTrue(any("EMA" in n for n in names))
        self.assertTrue(any("ELP" in n for n in names))
        self.assertTrue(any("VIROS" in n for n in names))
        institutions = [p["institution"] for p in payloads]
        self.assertTrue(any("Goddard" in inst for inst in institutions))
        self.assertTrue(any("Berkeley" in inst for inst in institutions))
        self.assertTrue(any("Embry-Riddle" in inst for inst in institutions))
        self.assertTrue(any("Northern Arizona" in inst for inst in institutions))

    def test_grand_quinquagintet_fleet_completeness(self):
        """Asserts exactly 50 probes in the Grand Quinquagintet, uniquely named and ordered."""
        self.assertEqual(len(self.fleet), 50)
        names = [p["name"] for p in self.fleet]
        self.assertEqual(len(names), len(set(names)), "Probe names must be unique")
        # Assert strict descending order of heliocentric distance
        for i in range(len(self.fleet) - 1):
            self.assertGreaterEqual(self.fleet[i]["heliocentric_au"], self.fleet[i+1]["heliocentric_au"])
        # Check first and last probes
        self.assertEqual(self.fleet[0]["name"], "Voyager 1")
        self.assertEqual(self.fleet[-1]["name"], "Parker Solar Probe")
        # Check ESCAPADE twins
        self.assertTrue(any("ESCAPADE Blue" in n for n in names))
        self.assertTrue(any("ESCAPADE Gold" in n for n in names))

    def test_agency_distribution(self):
        """Asserts agency breakdown across the 50 probes."""
        breakdown = self.extremes["agency_breakdown"]
        self.assertEqual(breakdown["NASA"], 25)
        self.assertEqual(breakdown["CNSA"], 8)
        self.assertEqual(breakdown["ESA"], 4)
        self.assertEqual(breakdown["ISRO"], 3)
        self.assertIn("JAXA", breakdown)
        self.assertIn("UAESA", breakdown)
        self.assertIn("KARI", breakdown)
        total_accounted = sum(breakdown.values())
        self.assertEqual(total_accounted, 50)

    def test_fleet_physical_extremes(self):
        """Asserts extreme physical ratio boundaries across all 50 probes."""
        self.assertEqual(self.extremes["probe_count"], 50)
        self.assertAlmostEqual(self.extremes["distance_ratio"], 3765.65, delta=1.0)
        self.assertGreater(self.extremes["solar_flux_ratio"], 1.41e7)
        self.assertAlmostEqual(self.extremes["light_time_max_hours"], 24.01, delta=0.1)
        self.assertAlmostEqual(self.extremes["light_time_min_sec"], 1.282, delta=0.01)
        self.assertGreater(self.extremes["light_time_ratio"], 6.7e4)
        self.assertGreater(self.extremes["speed_ratio"], 2.7e7)
        self.assertAlmostEqual(self.extremes["thermal_span_k"], 1666.45, delta=1.0)

    def test_mars_stereo_magnetosphere_resolution(self):
        """Asserts that twin probes resolve spatiotemporal ambiguity at Mars."""
        status = self.status
        self.assertEqual(len(status["twin_spacecraft"]), 2)
        # Verify that both probes carry identical magnetometer and electrostatic analyzer
        payloads = engine.get_science_payload_specs()
        combined_text = " ".join([p["name"] + " " + p["type"] + " " + p["science_goal"] for p in payloads])
        self.assertIn("reconnection", combined_text)
        self.assertIn("escaping", combined_text)
        self.assertIn("Langmuir probe", combined_text)
        self.assertIn("plasma density", combined_text)


if __name__ == "__main__":
    unittest.main()
