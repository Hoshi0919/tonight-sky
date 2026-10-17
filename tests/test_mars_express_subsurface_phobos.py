"""
单元测试集: 火星快车号 (Mars Express) 23 载在轨动力学、MARSIS 穿透雷达、
火卫一近距离飞掠测地学与 2026 人类深空二十六极黄金舰队 (The Grand Hexavigintet)
"""

import unittest
import math
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR / "scripts"))

from mars_express_subsurface_phobos_engine import (
    MarsExpressSubsurfacePhobosEngine,
    SPEED_OF_LIGHT,
    AU_KM,
    PHOBOS_SEMI_MAJOR_AXIS_KM,
    PHOBOS_MASS_KG,
    PHOBOS_VOLUME_KM3
)


class TestMarsExpressSubsurfacePhobos(unittest.TestCase):
    def setUp(self):
        self.engine = MarsExpressSubsurfacePhobosEngine()

    def test_mission_longevity(self):
        """测试 1: 验证在轨服役超 8,300 天 (超 22.8 年) 创欧洲深空纪录"""
        longevity = self.engine.compute_mission_longevity()
        self.assertGreater(longevity["flight_days"], 8500.0)
        self.assertGreater(longevity["orbit_days"], 8300.0)
        self.assertGreater(longevity["orbit_years"], 22.7)

    def test_orbital_dynamics(self):
        """测试 2: 验证高偏心椭圆极轨半长轴、偏心率与开普勒轨道周期"""
        orbit = self.engine.compute_orbit_state()
        self.assertAlmostEqual(orbit.semi_major_axis_km, 8609.5, delta=1.0)
        self.assertAlmostEqual(orbit.eccentricity, 0.5668, delta=0.001)
        self.assertAlmostEqual(orbit.orbital_period_hours, 6.735, delta=0.05)
        self.assertGreater(orbit.orbits_per_sol, 3.6)
        self.assertAlmostEqual(orbit.inclination_deg, 86.5, delta=0.5)

    def test_phobos_orbital_intersection(self):
        """测试 3: 验证近火点/远火点完全跨越火卫一轨道半径，确证轨道穿透唯一性"""
        orbit = self.engine.compute_orbit_state()
        self.assertLess(orbit.periapsis_radius_km, PHOBOS_SEMI_MAJOR_AXIS_KM)
        self.assertGreater(orbit.apoapsis_radius_km, PHOBOS_SEMI_MAJOR_AXIS_KM)
        self.assertTrue(orbit.intersects_phobos_orbit)

    def test_phobos_geodesy_and_porosity(self):
        """测试 4: 验证火卫一质量、体密度 (~1874 kg/m³) 与宏观孔隙度 (~30.6%) 碎石堆确证"""
        phobos = self.engine.compute_phobos_geodesy(closest_flyby_km=45.0)
        self.assertAlmostEqual(phobos.bulk_density_kgm3, 1873.6, delta=5.0)
        self.assertAlmostEqual(phobos.porosity_percentage, 30.6, delta=0.5)
        self.assertTrue(phobos.is_rubble_pile)
        self.assertEqual(phobos.closest_flyby_distance_km, 45.0)
        self.assertLess(phobos.escape_velocity_ms, 12.0)  # 逃逸速度极小 ~11 m/s

    def test_marsis_radar_physics(self):
        """测试 5: 验证 MARSIS 40m 天线、1.8~5.0 MHz 频段与纯冰介质雷达波速"""
        marsis = self.engine.compute_marsis_radar()
        self.assertEqual(marsis.antenna_length_m, 40.0)
        self.assertEqual(marsis.freq_min_mhz, 1.8)
        self.assertEqual(marsis.freq_max_mhz, 5.0)
        self.assertEqual(marsis.max_penetration_depth_km, 5.0)
        # 冰中波速 c / sqrt(3.15) ~ 168,913 km/s
        expected_v = SPEED_OF_LIGHT / math.sqrt(3.15)
        self.assertAlmostEqual(marsis.ice_radar_velocity_km_s, expected_v, delta=1.0)

    def test_subglacial_brine_reflectivity_anomaly(self):
        """测试 6: 验证冰-卤水界面菲涅尔反射率跃升与南极冰下湖强反射判定"""
        marsis = self.engine.compute_marsis_radar()
        # 冰-玄武岩反射率约 -14.1 dB
        self.assertAlmostEqual(marsis.ice_basalt_reflectivity_db, -14.1, delta=0.5)
        # 冰-卤水反射率约 -3.7 dB，反射率对比度显著跃升达 ~10.4 dB (> 9.5 dB)
        self.assertAlmostEqual(marsis.ice_brine_reflectivity_db, -3.7, delta=0.5)
        self.assertGreater(marsis.reflectivity_contrast_db, 9.5)
        self.assertTrue(marsis.is_liquid_lake_candidate)

    def test_mff_water_ice_reservoir(self):
        """测试 7: 验证美杜莎槽沟层 (MFF) 3.7 km 冰层体积与全球等效水层厚度"""
        mff = self.engine.compute_mff_water_reservoir()
        self.assertEqual(mff.max_thickness_km, 3.7)
        self.assertGreaterEqual(mff.water_equivalent_volume_km3, 1.5e6)
        # 等效淹没全火星水层厚度约 11.8 米
        self.assertAlmostEqual(mff.equivalent_global_water_layer_m, 11.8, delta=1.0)

    def test_grand_hexavigintet_fleet_completeness(self):
        """测试 8: 验证深空二十六极黄金舰队完整性 (26 艘)、日心极距降序单调性与火星快车归位"""
        fleet = self.engine.build_grand_hexavigintet_fleet()
        self.assertEqual(len(fleet), 26)
        # 验证单调降序
        dists = [p.heliocentric_au for p in fleet]
        self.assertTrue(all(x >= y for x, y in zip(dists, dists[1:])))
        # 验证边界: Voyager 1 居首，Parker Solar Probe 居尾
        self.assertIn("Voyager 1", fleet[0].name)
        self.assertIn("Parker Solar Probe", fleet[-1].name)
        # 验证 Mars Express 存在并处于火星编队
        mex_probe = [p for p in fleet if "Mars Express" in p.name]
        self.assertEqual(len(mex_probe), 1)
        self.assertEqual(mex_probe[0].agency, "ESA")
        self.assertAlmostEqual(mex_probe[0].heliocentric_au, 1.579, delta=0.01)

    def test_fleet_extreme_physical_ratios(self):
        """测试 9: 验证二十六极大舰队日心极距跨度超 3,700 倍、太阳能流落差超 1,400 万倍"""
        extremes = self.engine.compute_fleet_extremes()
        self.assertEqual(extremes["probe_count"], 26)
        self.assertGreater(extremes["heliocentric_distance_ratio"], 3700.0)
        self.assertGreater(extremes["solar_flux_ratio"], 1.4e7)
        self.assertGreater(extremes["one_way_light_time_ratio"], 3700.0)


if __name__ == "__main__":
    unittest.main()
