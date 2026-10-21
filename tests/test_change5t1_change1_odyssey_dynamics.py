import unittest
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR / "scripts"))

from change5t1_change1_odyssey_dynamics_engine import Change5T1Change1OdysseyDynamicsEngine

class TestChange5T1Change1OdysseyDynamics(unittest.TestCase):
    def setUp(self):
        self.engine = Change5T1Change1OdysseyDynamicsEngine()

    def test_change5t1_free_return_trajectory(self):
        ch5 = self.engine.compute_change5t1_dynamics()
        self.assertEqual(ch5["anniversary_years"], 12)
        self.assertEqual(ch5["launcher"], "Long March 3C/G2 (长征三号丙改二型)")
        self.assertAlmostEqual(ch5["v_tli_km_s"], 10.92, delta=0.05)
        self.assertEqual(ch5["periselenium_altitude_km"], 11300.0)
        self.assertEqual(ch5["mission_duration_hours"], 196.0)

    def test_change5t1_skip_reentry_aerodynamics_and_heat(self):
        ch5 = self.engine.compute_change5t1_dynamics()
        self.assertAlmostEqual(ch5["v_entry_km_s"], 10.87, delta=0.05)
        self.assertEqual(ch5["entry_flight_path_angle_deg"], -5.8)
        self.assertEqual(ch5["first_dip_min_alt_km"], 60.0)
        self.assertEqual(ch5["skip_apogee_alt_km"], 140.0)
        self.assertAlmostEqual(ch5["v_skip_exit_km_s"], 7.60, delta=0.05)
        self.assertAlmostEqual(ch5["energy_dissipated_first_skip_mj_kg"], 30.2, delta=0.5)
        self.assertGreater(ch5["energy_dissipated_pct"], 50.0)

    def test_change5t1_g_load_suppression_and_service_module(self):
        ch5 = self.engine.compute_change5t1_dynamics()
        self.assertEqual(ch5["lift_to_drag_ratio"], 0.32)
        self.assertLess(ch5["peak_g_load_skip"], 5.0)
        self.assertGreater(ch5["peak_g_load_ballistic"], 15.0)
        self.assertGreater(ch5["g_load_reduction_pct"], 70.0)
        self.assertIn("四子王旗", ch5["touchdown_site"])
        self.assertIn("l2_halo", ch5["service_module_extensions"])
        self.assertIn("dro", ch5["service_module_extensions"])

    def test_change1_orbital_phasing_and_capture(self):
        ch1 = self.engine.compute_change1_dynamics()
        self.assertEqual(ch1["anniversary_years"], 19)
        self.assertEqual(ch1["launcher"], "Long March 3A (长征三号甲)")
        self.assertEqual(len(ch1["phasing_orbits"]), 3)
        self.assertAlmostEqual(ch1["polar_orbit_v_circ_km_s"], 1.591, delta=0.01)
        self.assertAlmostEqual(ch1["polar_orbit_period_min"], 127.54, delta=0.5)

    def test_change1_scientific_payload_and_impact(self):
        ch1 = self.engine.compute_change1_dynamics()
        self.assertEqual(ch1["dem_resolution_m"], 120.0)
        self.assertGreater(ch1["laser_altimeter_points"], 3000000)
        self.assertEqual(len(ch1["celms_frequencies_ghz"]), 4)
        self.assertGreater(ch1["estimated_he3_reserve_tons"], 1000000.0)
        self.assertIn("丰富海", ch1["controlled_impact_site"])
        self.assertEqual(ch1["controlled_impact_utc"], "2009-03-01 08:13:10 UTC")

    def test_mars_odyssey_moi_and_aerobraking(self):
        ody = self.engine.compute_mars_odyssey_dynamics()
        self.assertEqual(ody["anniversary_years"], 25)
        self.assertAlmostEqual(ody["initial_orbit"]["period_hours"], 18.6, delta=0.5)
        self.assertEqual(ody["aerobraking"]["atmospheric_passes"], 335)
        self.assertEqual(ody["aerobraking"]["duration_days"], 76)
        self.assertGreaterEqual(ody["aerobraking"]["propellant_saved_kg"], 200.0)
        self.assertAlmostEqual(ody["science_orbit"]["v_circ_km_s"], 3.359, delta=0.01)
        self.assertAlmostEqual(ody["science_orbit"]["period_min"], 118.35, delta=0.5)

    def test_mars_odyssey_subterranean_water_ice(self):
        ody = self.engine.compute_mars_odyssey_dynamics()
        min_ice, max_ice = ody["water_ice_discovery"]["ice_mass_fraction_pct"]
        self.assertEqual(min_ice, 20.0)
        self.assertEqual(max_ice, 50.0)
        self.assertEqual(ody["continuous_operating_years"], 25)

    def test_sky_mechanics_and_supermoon_metrics(self):
        sky = self.engine.compute_sky_mechanics_2026_10_23_24()
        d23 = sky["2026-10-23"]
        d24 = sky["2026-10-24"]
        self.assertEqual(d23["lunar_calendar"], "农历九月十四")
        self.assertAlmostEqual(d23["illumination_pct"], 91.8, delta=0.5)
        self.assertEqual(d23["days_to_supermoon"], 3)
        self.assertAlmostEqual(d23["darksky_window_min"], 56.0, delta=2.0)
        self.assertEqual(d24["lunar_calendar"], "农历九月十五")
        self.assertAlmostEqual(d24["illumination_pct"], 97.2, delta=0.5)
        self.assertEqual(d24["days_to_supermoon"], 2)

if __name__ == "__main__":
    unittest.main()
