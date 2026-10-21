import unittest
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR / "scripts"))

from luna12_lageos2_relativity_engine import Luna12Lageos2RelativityEngine

class TestLuna12Lageos2LenseThirringDynamics(unittest.TestCase):
    def setUp(self):
        self.engine = Luna12Lageos2RelativityEngine()

    def test_luna12_mission_and_jubilee(self):
        luna = self.engine.compute_luna12_dynamics()
        self.assertEqual(luna["anniversary_years"], 60)
        self.assertIn("Diamond Jubilee", luna["jubilee_name"])
        self.assertEqual(luna["launcher"], "Molniya-M 8K78M")
        self.assertEqual(luna["launch_site"], "Baikonur 31/6")
        self.assertEqual(luna["launch_date_utc"], "1966-10-22 08:42:26")

    def test_luna12_initial_and_operational_orbits(self):
        luna = self.engine.compute_luna12_dynamics()
        init_orb = luna["initial_capture_orbit"]
        self.assertAlmostEqual(init_orb["perilune_alt_km"], 100.0, delta=1.0)
        self.assertAlmostEqual(init_orb["apolune_alt_km"], 1740.0, delta=1.0)
        self.assertAlmostEqual(init_orb["period_min"], 204.9, delta=1.0)

        op_orb = luna["operational_orbit"]
        self.assertAlmostEqual(op_orb["perilune_alt_km"], 133.0, delta=1.0)
        self.assertAlmostEqual(op_orb["apolune_alt_km"], 1200.0, delta=1.0)
        self.assertAlmostEqual(op_orb["semi_major_axis_km"], 2403.9, delta=2.0)
        self.assertAlmostEqual(op_orb["eccentricity"], 0.2219, delta=0.01)
        self.assertAlmostEqual(op_orb["period_min"], 176.3, delta=1.0)
        self.assertEqual(op_orb["inclination_deg"], 10.0)

    def test_luna12_velocities_and_imaging_payload(self):
        luna = self.engine.compute_luna12_dynamics()
        self.assertAlmostEqual(luna["perilune_velocity_km_s"], 1.790, delta=0.02)
        self.assertAlmostEqual(luna["apolune_velocity_km_s"], 1.140, delta=0.02)
        self.assertEqual(luna["scan_lines"], 1100)
        self.assertEqual(luna["ground_resolution_m"], (14.9, 19.8))
        self.assertIn("Mare Imbrium (Sea of Rains)", luna["primary_targets"])
        self.assertIn("Aristarchus Crater", luna["primary_targets"])

    def test_luna12_long_duration_orbits(self):
        luna = self.engine.compute_luna12_dynamics()
        self.assertEqual(luna["total_lunar_orbits"], 602)
        self.assertEqual(luna["radio_sessions"], 302)

    def test_lageos2_spacecraft_and_retroreflectors(self):
        lag = self.engine.compute_lageos2_relativity_dynamics()
        self.assertEqual(lag["anniversary_years"], 34)
        self.assertIn("STS-52", lag["launch_mission"])
        self.assertIn("Columbia", lag["launch_mission"])
        specs = lag["satellite_specs"]
        self.assertEqual(specs["mass_kg"], 405.4)
        self.assertEqual(specs["diameter_m"], 0.6)
        self.assertAlmostEqual(specs["cross_section_area_m2"], 0.2827, delta=0.001)
        self.assertAlmostEqual(specs["area_to_mass_ratio_m2_per_kg"], 0.000697, delta=0.00001)
        self.assertEqual(specs["retroreflectors_total"], 426)
        self.assertEqual(specs["fused_silica_prisms"], 422)
        self.assertEqual(specs["germanium_prisms"], 4)

    def test_lageos2_orbit_and_laser_ranging(self):
        lag = self.engine.compute_lageos2_relativity_dynamics()
        orb = lag["orbit"]
        self.assertAlmostEqual(orb["semi_major_axis_km"], 12210.0, delta=5.0)
        self.assertAlmostEqual(orb["inclination_deg"], 52.65, delta=0.05)
        self.assertAlmostEqual(orb["eccentricity"], 0.014, delta=0.001)
        rel = lag["relativity_physics"]
        self.assertEqual(rel["slr_ranging_precision_mm"], 2.0)
        self.assertAlmostEqual(rel["laser_roundtrip_time_ms"], 38.91, delta=1.0)

    def test_lageos2_general_relativity_lense_thirring(self):
        lag = self.engine.compute_lageos2_relativity_dynamics()
        rel = lag["relativity_physics"]
        self.assertAlmostEqual(rel["lense_thirring_precession_mas_per_yr"], 31.13, delta=0.2)
        self.assertAlmostEqual(rel["classic_j2_precession_deg_per_day"], -0.623, delta=0.01)
        self.assertTrue(rel["frame_dragging_verified"])
        self.assertIn("LAGEOS-1", lag["complementary_satellite"])

    def test_quadruple_deepspace_heritage(self):
        quad = self.engine.compute_quadruple_deepspace_heritage_2026()
        self.assertEqual(quad["epoch_date"], "2026-10-22")
        self.assertEqual(quad["total_heritage_count"], 4)
        names = [m["name"] for m in quad["milestones"]]
        self.assertIn("Luna 12", names)
        self.assertIn("Venera 9", names)
        self.assertIn("LAGEOS-2", names)
        self.assertIn("Chandrayaan-1", names)

if __name__ == "__main__":
    unittest.main()
