import unittest
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR / "scripts"))

from capstone_nrho_cislunar_soyuz_guiana_engine import CapstoneNRHOSoyuzGuianaEngine

class TestCapstoneNRHOSoyuzGuiana(unittest.TestCase):
    def setUp(self):
        self.engine = CapstoneNRHOSoyuzGuianaEngine()

    def test_capstone_resonance_period(self):
        res = self.engine.compute_capstone_nrho_parameters()
        self.assertAlmostEqual(res["period_days"], 6.562, delta=0.01)
        self.assertAlmostEqual(res["period_hours"], 157.5, delta=0.5)
        self.assertEqual(res["resonance"], "9:2 synodic resonance")

    def test_capstone_nrho_geometry(self):
        res = self.engine.compute_capstone_nrho_parameters()
        self.assertAlmostEqual(res["hp_km"], 1602.6, delta=2.0)
        self.assertAlmostEqual(res["ha_km"], 69662.6, delta=2.0)
        self.assertAlmostEqual(res["eccentricity"], 0.9106, delta=0.005)
        self.assertAlmostEqual(res["vp_cr3bp_km_s"], 2.40, delta=0.1)
        self.assertAlmostEqual(res["va_cr3bp_m_s"], 110.0, delta=10.0)

    def test_capstone_stability_stationkeeping(self):
        res = self.engine.compute_capstone_nrho_parameters()
        self.assertAlmostEqual(res["floquet_multiplier"], 1.30, delta=0.05)
        self.assertAlmostEqual(res["instability_time_days"], 25.0, delta=2.0)
        self.assertLessEqual(res["annual_stationkeeping_dv_mps"], 5.0)
        self.assertGreaterEqual(res["annual_stationkeeping_dv_mps"], 2.0)

    def test_capstone_caps_delay_and_specs(self):
        res = self.engine.compute_capstone_nrho_parameters()
        self.assertEqual(res["probe_mass_kg"], 25.0)
        self.assertEqual(res["probe_form_factor"], "12U CubeSat")
        self.assertAlmostEqual(res["caps_twoway_delay_ms"], 333.56, delta=1.0)

    def test_soyuz_guiana_tangential_boost(self):
        boost = self.engine.compute_soyuz_guiana_boost()
        self.assertAlmostEqual(boost["v_tang_baikonur_mps"], 323.55, delta=0.5)
        self.assertAlmostEqual(boost["v_tang_csg_mps"], 463.16, delta=0.5)
        self.assertAlmostEqual(boost["v_boost_mps"], 139.60, delta=0.5)

    def test_soyuz_guiana_gto_plane_savings_and_payload(self):
        boost = self.engine.compute_soyuz_guiana_boost()
        self.assertGreater(boost["dv_plane_saved_mps"], 1200.0)
        self.assertAlmostEqual(boost["payload_gto_baikonur_kg"], 1700.0)
        self.assertAlmostEqual(boost["payload_gto_csg_kg"], 3200.0)
        self.assertAlmostEqual(boost["payload_increase_pct"], 88.2, delta=0.5)

    def test_galileo_iov_meo_orbit(self):
        boost = self.engine.compute_soyuz_guiana_boost()
        self.assertEqual(boost["galileo_semimajor_axis_km"], 29600.0)
        self.assertAlmostEqual(boost["galileo_v_circ_km_s"], 3.670, delta=0.01)
        self.assertAlmostEqual(boost["galileo_period_hours"], 14.08, delta=0.1)

    def test_orionids_china_dark_windows_and_tm33(self):
        # Orionids dark window checks
        windows = self.engine.compute_orionids_china_dark_windows()
        self.assertEqual(len(windows), 6)
        for w in windows:
            self.assertGreaterEqual(w["pure_dark_window_hours"], 2.5)
            self.assertGreaterEqual(w["radiant_culmination_alt_deg"], 60.0)
            self.assertEqual(w["moon_illum_pct"], 77.2)

        # Soyuz TM-33 checks
        tm33 = self.engine.get_soyuz_tm33_milestones()
        self.assertEqual(tm33["mission_name"], "Andromède")
        self.assertTrue(tm33["first_european_woman_on_iss"])
        self.assertEqual(len(tm33["crew"]), 3)
        self.assertAlmostEqual(tm33["duration_days"], 9.83, delta=0.1)

if __name__ == "__main__":
    unittest.main()
