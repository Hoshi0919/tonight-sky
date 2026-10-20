import unittest
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR / "scripts"))

from chandrayaan1_venera9_orionids_peak_engine import Chandrayaan1Venera9OrionidsPeakEngine

class TestChandrayaan1Venera9OrionidsPeak(unittest.TestCase):
    def setUp(self):
        self.engine = Chandrayaan1Venera9OrionidsPeakEngine()

    def test_chandrayaan1_orbit_and_maneuver(self):
        ch1 = self.engine.compute_chandrayaan1_dynamics()
        self.assertEqual(ch1["anniversary_years"], 18)
        self.assertEqual(ch1["launcher"], "PSLV-XL (C11)")
        self.assertAlmostEqual(ch1["v_perigee_tli_km_s"], 10.87, delta=0.1)
        self.assertAlmostEqual(ch1["loi_braking_dv_mps"], 370.2, delta=10.0)
        self.assertAlmostEqual(ch1["orbit_100km_v_circ_km_s"], 1.634, delta=0.01)
        self.assertAlmostEqual(ch1["orbit_100km_period_min"], 117.8, delta=0.5)
        self.assertAlmostEqual(ch1["orbit_200km_period_min"], 127.5, delta=0.5)

    def test_chandrayaan1_m3_and_mip_payloads(self):
        ch1 = self.engine.compute_chandrayaan1_dynamics()
        self.assertEqual(ch1["m3_spectral_range_um"], (0.43, 3.0))
        self.assertEqual(ch1["m3_water_hydroxyl_band_um"], (2.8, 3.0))
        self.assertAlmostEqual(ch1["mip_impact_speed_km_s"], 1.69, delta=0.05)
        self.assertIn("Shackleton Crater", ch1["mip_impact_target"])

    def test_chandrayaan1_radar_rediscovery(self):
        ch1 = self.engine.compute_chandrayaan1_dynamics()
        self.assertEqual(ch1["jpl_radar_rediscovery_year"], 2017)
        self.assertAlmostEqual(ch1["radar_roundtrip_delay_s"], 2.564, delta=0.05)

    def test_venera9_hyperbolic_entry_and_aerodynamics(self):
        v9 = self.engine.compute_venera9_landing_dynamics()
        self.assertEqual(v9["anniversary_years"], 51)
        self.assertAlmostEqual(v9["v_entry_km_s"], 10.7, delta=0.2)
        self.assertAlmostEqual(v9["peak_deceleration_g"], 168.0, delta=15.0)
        self.assertEqual(v9["chute_cut_altitude_km"], 50.0)
        self.assertEqual(v9["aero_disk_diameter_m"], 2.1)

    def test_venera9_terminal_impact_and_shock_absorption(self):
        v9 = self.engine.compute_venera9_landing_dynamics()
        self.assertAlmostEqual(v9["venus_surface_density_kg_m3"], 65.0, delta=1.0)
        self.assertGreater(v9["terminal_impact_velocity_m_s"], 5.0)
        self.assertLess(v9["terminal_impact_velocity_m_s"], 9.0)
        self.assertAlmostEqual(v9["impact_kinetic_energy_kj"], 14.3, delta=3.0)

    def test_venera9_extreme_environment_and_pcm_thermal(self):
        v9 = self.engine.compute_venera9_landing_dynamics()
        self.assertEqual(v9["surface_pressure_mpa"], 9.0)
        self.assertEqual(v9["surface_pressure_bar"], 90.0)
        self.assertEqual(v9["equivalent_ocean_depth_m"], 900.0)
        self.assertEqual(v9["surface_temp_c"], 485.0)
        self.assertAlmostEqual(v9["surface_temp_k"], 758.15, delta=0.1)
        self.assertIn("LiNO3", v9["pcm_material"])
        self.assertAlmostEqual(v9["heat_absorption_capacity_mj"], 9.8, delta=0.5)
        self.assertEqual(v9["operational_duration_min"], 53.0)
        self.assertTrue(v9["first_extraterrestrial_surface_photo"])
        self.assertEqual(v9["panorama_field_of_view_deg"], 180.0)

    def test_orionids_peak_collision_and_energy(self):
        ori = self.engine.compute_orionids_peak_night_dynamics()
        self.assertEqual(ori["parent_comet"], "1P/Halley")
        self.assertAlmostEqual(ori["comet_orbital_period_years"], 76.0, delta=1.0)
        self.assertEqual(ori["entry_velocity_km_s"], 66.0)
        self.assertAlmostEqual(ori["kinetic_energy_density_gj_per_kg"], 2.18, delta=0.05)
        self.assertAlmostEqual(ori["tnt_equivalent_kg_per_kg"], 520.6, delta=10.0)
        self.assertEqual(ori["persistent_train_fraction"], 0.48)
        self.assertEqual(ori["zhr_peak"], 23)
        self.assertIn("06h 20m", ori["radiant_ra"])
        self.assertIn("+16.0°", ori["radiant_dec"])

    def test_orionids_china_peak_dark_windows_and_efficiency(self):
        ori = self.engine.compute_orionids_peak_night_dynamics()
        windows = ori["city_dark_windows"]
        self.assertEqual(len(windows), 6)
        for w in windows:
            self.assertGreaterEqual(w["window_hr"], 2.5)
            self.assertGreaterEqual(w["culm_alt"], 65.0)
            self.assertGreaterEqual(w["elevation_efficiency_factor"], 0.88)
            self.assertLessEqual(w["elevation_efficiency_factor"], 1.0)

if __name__ == "__main__":
    unittest.main()
