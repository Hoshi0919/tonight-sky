import unittest
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR / "scripts"))

from venera10_beta_regio_lava_plain_engine import Venera10BetaRegioLavaPlainEngine


class TestVenera10BetaRegioLavaPlain(unittest.TestCase):
    def setUp(self):
        self.engine = Venera10BetaRegioLavaPlainEngine()

    def test_orbiter_keplerian_and_relay(self):
        orb = self.engine.compute_orbiter_dynamics()
        self.assertEqual(orb["mission"], "Venera 10 Orbiter")
        self.assertAlmostEqual(orb["semi_major_axis_km"], 63826.8, delta=10.0)
        self.assertAlmostEqual(orb["eccentricity"], 0.8798, delta=0.005)
        self.assertEqual(orb["inclination_deg"], 29.5)
        self.assertAlmostEqual(orb["orbital_period_hours"], 49.38, delta=0.5)
        self.assertAlmostEqual(orb["v_periapsis_km_s"], 8.91, delta=0.1)
        self.assertAlmostEqual(orb["v_apoapsis_km_s"], 0.57, delta=0.1)
        self.assertEqual(orb["relay_window_minutes"], 72.0)

    def test_lander_hyperbolic_entry_and_aero(self):
        lander = self.engine.compute_lander_entry_and_descent()
        self.assertEqual(lander["v_entry_km_s"], 10.7)
        self.assertEqual(lander["peak_deceleration_g"], 168.0)
        self.assertEqual(lander["chute_jettison_altitude_km"], 50.0)
        self.assertEqual(lander["aero_disk_diameter_m"], 2.1)
        self.assertAlmostEqual(lander["aero_disk_area_m2"], 3.4636, delta=0.01)

    def test_terminal_descent_and_impact_energy(self):
        lander = self.engine.compute_lander_entry_and_descent()
        self.assertEqual(lander["impact_mass_kg"], 660.0)
        self.assertEqual(lander["surface_density_kg_m3"], 65.0)
        # 终端沉降速度 6.0 ~ 7.5 m/s
        self.assertGreater(lander["terminal_velocity_m_s"], 6.0)
        self.assertLess(lander["terminal_velocity_m_s"], 7.5)
        self.assertAlmostEqual(lander["terminal_velocity_km_h"], lander["terminal_velocity_m_s"] * 3.6, delta=0.1)
        # 撞击动能 12 ~ 18 kJ
        self.assertGreater(lander["impact_kinetic_energy_kj"], 12.0)
        self.assertLess(lander["impact_kinetic_energy_kj"], 18.0)
        self.assertEqual(lander["crush_distance_cm"], 18.0)
        self.assertGreater(lander["crush_deceleration_g"], 5.0)

    def test_extreme_surface_pressure_temperature(self):
        env = self.engine.compute_extreme_surface_environment()
        self.assertEqual(env["surface_pressure_mpa"], 9.0)
        self.assertEqual(env["surface_pressure_bar"], 90.0)
        self.assertEqual(env["surface_pressure_atm"], 92.0)
        self.assertEqual(env["equivalent_ocean_depth_m"], 900.0)
        self.assertEqual(env["surface_temp_c"], 465.0)
        self.assertAlmostEqual(env["surface_temp_k"], 738.15, delta=0.1)

    def test_pcm_thermal_storage_system(self):
        env = self.engine.compute_extreme_surface_environment()
        self.assertIn("LiNO3", env["pcm_material"])
        self.assertEqual(env["pcm_mass_kg"], 35.0)
        self.assertAlmostEqual(env["pcm_total_storage_mj"], 9.8, delta=0.1)
        self.assertEqual(env["initial_internal_temp_c"], -10.0)
        self.assertEqual(env["operational_duration_min"], 65.0)
        self.assertEqual(env["designed_duration_min"], 30.0)
        self.assertAlmostEqual(env["lifetime_extension_percent"], 116.7, delta=0.5)

    def test_surface_wind_dynamics_and_dynamic_pressure(self):
        env = self.engine.compute_extreme_surface_environment()
        w_min, w_max = env["wind_speed_range_m_s"]
        self.assertEqual(w_min, 0.8)
        self.assertEqual(w_max, 1.3)
        q_min, q_max = env["dynamic_pressure_range_pa"]
        self.assertAlmostEqual(q_min, 20.8, delta=0.5)
        self.assertAlmostEqual(q_max, 54.9, delta=0.5)

    def test_geological_formation_and_rock_density(self):
        geo = self.engine.compute_surface_science_and_geology()
        self.assertEqual(geo["anniversary_years"], 51)
        self.assertEqual(geo["landing_site"], "Beta Regio, Venus")
        self.assertEqual(geo["latitude_deg"], 15.42)
        self.assertEqual(geo["longitude_deg"], 291.51)
        self.assertEqual(geo["telephotometer_fov_deg"], 180.0)
        self.assertAlmostEqual(geo["rock_density_g_cm3"], 2.8, delta=0.01)
        self.assertEqual(geo["rock_density_error_g_cm3"], 0.1)
        self.assertTrue(geo["second_extraterrestrial_surface_photo"])
        self.assertIn("Basaltic", geo["geological_formation"])
        self.assertIn("Young tectonics", geo["venera9_geology_contrast"])
        self.assertIn("Older weathered plain", geo["venera10_geology_contrast"])

    def test_distance_to_venera9(self):
        geo = self.engine.compute_surface_science_and_geology()
        self.assertAlmostEqual(geo["distance_to_venera9_km"], 1975.0, delta=10.0)

    def test_daily_synthesis_stereo_vicennial(self):
        synth = self.engine.compute_daily_synthesis()
        self.assertEqual(synth["date"], "2026-10-25")
        self.assertEqual(synth["lunar_calendar"], "农历九月十六")
        self.assertAlmostEqual(synth["moon_phase_percent"], 98.14, delta=0.5)
        self.assertIn("2026-10-26 12:11", synth["next_full_moon_cst"])
        # STEREO 双星双十华诞
        stereo = synth["stereo_vicennial_jubilee"]
        self.assertEqual(stereo["years"], 20.0)
        self.assertEqual(stereo["days"], 7305.0)
        self.assertAlmostEqual(stereo["ahead_angle_deg"], 68.20, delta=0.1)
        self.assertAlmostEqual(stereo["warning_lead_days"], 5.17, delta=0.05)
        self.assertAlmostEqual(stereo["surface_coverage_percent"], 68.9, delta=0.2)


if __name__ == "__main__":
    unittest.main()
