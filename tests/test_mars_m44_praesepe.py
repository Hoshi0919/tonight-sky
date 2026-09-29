"""
test_mars_m44_praesepe.py - Unit test suite for 2026 Mars-M44 Praesepe Transit Engine
"""

import datetime
import json
import subprocess
import sys
import unittest
from pathlib import Path

# Add project root and scripts dir to path
DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = DIR / 'scripts'
sys.path.insert(0, str(SCRIPTS_DIR))

import mars_m44_praesepe_engine as engine

class TestMarsM44Praesepe(unittest.TestCase):

    def test_m44_data_constants(self):
        m44 = engine.M44_DATA
        self.assertEqual(m44['ngc'], 'NGC 2632')
        self.assertAlmostEqual(m44['distance_pc'], 182.0, delta=5.0)
        self.assertAlmostEqual(m44['integrated_v_mag'], 3.70, delta=0.1)
        self.assertEqual(m44['core_radius_arcmin'], 25.0)
        self.assertEqual(m44['cluster_radius_arcmin'], 47.5)

    def test_mars_physics_at_closest_approach(self):
        dt = datetime.datetime(2026, 10, 11, 21, 11)
        phys = engine.compute_mars_physics(dt)
        self.assertAlmostEqual(phys['mag'], 1.06, delta=0.05)
        self.assertGreater(phys['angular_diameter_arcsec'], 5.0)
        self.assertLess(phys['angular_diameter_arcsec'], 7.0)
        self.assertGreater(phys['earth_distance_au'], 1.5)
        self.assertLess(phys['earth_distance_au'], 1.8)
        self.assertAlmostEqual(phys['illumination_pct'], 90.0, delta=1.0)
        self.assertEqual(phys['color_index_bv'], 1.40)

    def test_m44_transit_timeline(self):
        timeline = engine.compute_m44_transit_timeline()
        self.assertIsNotNone(timeline['cluster_entry_cst'])
        self.assertIsNotNone(timeline['core_entry_cst'])
        self.assertIsNotNone(timeline['core_exit_cst'])
        self.assertIsNotNone(timeline['cluster_exit_cst'])
        
        # Closest approach should be on 2026-10-11 evening
        self.assertIn('2026-10-11', timeline['closest_approach_cst'])
        # Distance to center < 5.0 arcmin
        self.assertLess(timeline['min_distance_to_center_arcmin'], 5.0)
        self.assertGreater(timeline['min_distance_to_center_arcmin'], 4.5)

    def test_member_star_encounters(self):
        timeline = engine.compute_m44_transit_timeline()
        encounters = {e['star_key']: e for e in timeline['star_encounters']}
        
        # Check ε Cnc (Meleph)
        self.assertIn('eps_cnc', encounters)
        eps = encounters['eps_cnc']
        self.assertAlmostEqual(eps['min_separation_arcmin'], 2.38, delta=0.1)
        self.assertIn('2026-10-11 23:', eps['closest_time_cst'])
        self.assertAlmostEqual(eps['delta_v_mag'], 5.23, delta=0.1)
        
        # Check HD 73710
        self.assertIn('hd_73710', encounters)
        hd = encounters['hd_73710']
        self.assertAlmostEqual(hd['min_separation_arcmin'], 3.29, delta=0.1)
        
        # Check 42 Cnc
        self.assertIn('42_cnc', encounters)
        c42 = encounters['42_cnc']
        self.assertAlmostEqual(c42['min_separation_arcmin'], 8.70, delta=0.1)

    def test_china_cities_visibility(self):
        cities_obs = engine.compute_city_ephemeris('2026-10-12')
        self.assertEqual(len(cities_obs), 5)
        for city_key, obs in cities_obs.items():
            # Mars transit altitude should be very high (> 60 deg)
            self.assertGreater(obs['transit_altitude_deg'], 60.0)
            # Dawn altitude > 45 deg
            self.assertGreater(obs['dawn_altitude_deg'], 45.0)
            # Dark sky duration at least 3.8 hours
            self.assertGreaterEqual(obs['dark_sky_duration_hours'], 3.8)
            # Moon illumination minimal (crescent, < 5%)
            self.assertLess(obs['moon_illumination_pct'], 5.0)

    def test_full_report_structure_and_json(self):
        report = engine.compute_full_mars_praesepe_report()
        self.assertIn('title', report)
        self.assertIn('mars_physics', report)
        self.assertIn('timeline', report)
        self.assertIn('flux_contrast', report)
        self.assertIn('china_cities_visibility', report)
        self.assertIn('astrophotography_guide', report)
        
        # Test JSON serialization
        json_str = json.dumps(report, ensure_ascii=False)
        self.assertGreater(len(json_str), 1000)
        reloaded = json.loads(json_str)
        self.assertEqual(reloaded['title'], report['title'])

    def test_cli_execution_json(self):
        cmd = [sys.executable, str(SCRIPTS_DIR / 'mars_m44_praesepe_engine.py'), '--json']
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(res.stdout)
        self.assertIn('timeline', data)
        self.assertLess(data['timeline']['min_distance_to_center_arcmin'], 5.0)

if __name__ == '__main__':
    unittest.main()
