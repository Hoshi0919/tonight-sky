"""
单元测试集：詹姆斯·韦伯空间望远镜 (JWST) 日地 L2 晕轨道天体力学、极寒热力学隔热与红外物理推演
Unit tests for James Webb Space Telescope (JWST) Sun-Earth L2 Halo Orbit, Cryogenic Thermodynamics & Deep Infrared Physics
"""

import sys
import math
from pathlib import Path
import pytest

scripts_dir = Path(__file__).parent.parent / "scripts"
repo_dir = Path(__file__).parent.parent
sys.path.insert(0, str(scripts_dir))
sys.path.insert(0, str(repo_dir))

from jwst_l2_halo_orbit_cryogenic_engine import (
    calculate_crtbp_l2,
    calculate_halo_orbit_geometry,
    calculate_sunshield_thermal,
    calculate_stationkeeping_and_propulsion,
    calculate_optical_capabilities,
    calculate_grand_septet_summary
)


def test_crtbp_l2_position_and_light_time():
    """断言 1: 日地 L2 空间距离与单向光行时精准解算"""
    crtbp = calculate_crtbp_l2()
    # L2 距地球中心在 148 万 ~ 152 万公里之间 (约 0.010 AU)
    assert 1480000.0 <= crtbp.l2_distance_km <= 1520000.0
    assert 0.0098 <= crtbp.l2_distance_au <= 0.0103
    # 单向光行时在 4.9 ~ 5.2 秒之间 (往返 10 秒)
    assert 4.9 <= crtbp.light_travel_time_sec <= 5.2
    # 李雅普诺夫鞍点发散时间尺度在 20 ~ 26 天
    assert 20.0 <= crtbp.instability_tau_days <= 26.0


def test_halo_orbit_dimensions_and_period():
    """断言 2: 晕轨道三维振幅、周期与尺度"""
    halo = calculate_halo_orbit_geometry()
    # 周期约 180 天 (6 个月)
    assert 170.0 <= halo.period_days <= 190.0
    # 面内振幅 Ay 约 80 万公里, 垂直振幅 Az 约 45 万公里
    assert 700000.0 <= halo.amplitude_y_km <= 900000.0
    assert 400000.0 <= halo.amplitude_z_km <= 500000.0
    assert 200000.0 <= halo.amplitude_x_km <= 300000.0


def test_eclipse_free_geometry_constraint():
    """断言 3: 无食约束物理验证 (365 天无阴影)"""
    halo = calculate_halo_orbit_geometry()
    # 地球半影在 1.5M km 处截面半径远小于 30,000 km
    assert halo.earth_umbra_radius_km < 30000.0
    # 最小离轴投影距离 450,000 km 必须比地影大 10 倍以上
    assert halo.min_off_axis_dist_km > halo.earth_umbra_radius_km * 10.0
    assert halo.is_eclipse_free is True


def test_stationkeeping_and_propulsion_lifetime():
    """断言 4: 轨道维持微推力动力学与 20 年超长寿命"""
    prop = calculate_stationkeeping_and_propulsion()
    # 每年轨道维持 Delta-V 预算低于 5.0 m/s/年
    assert prop["total_annual_dv_mps"] < 5.0
    assert prop["annual_skm_dv_mps"] < 3.0
    # 维持周期约为 21 天一次
    assert prop["stationkeeping_cadence_days"] == 21.0
    # 剩余 Delta-V 预算充足，预期寿命大于 20 年
    assert prop["remaining_total_dv_mps"] >= 300.0
    assert prop["projected_life_years"] >= 20.0


def test_sunshield_thermal_attenuation_and_gradient():
    """断言 5: 五层遮阳罩 300 K 巨大温差与千万倍热衰减"""
    thermal = calculate_sunshield_thermal()
    # 日侧温度高于 +50°C
    assert thermal.hot_side_temp_c >= 50.0
    # 背阴面被动辐射制冷温度低于 45 K (-228°C)
    assert thermal.cold_side_temp_k <= 45.0
    # 5 层温度严格单调递减
    for i in range(len(thermal.layer_temps_c) - 1):
        assert thermal.layer_temps_c[i] > thermal.layer_temps_c[i + 1]
    # 热衰减比例超过 1000 万倍
    assert thermal.attenuation_ratio > 1.0e7
    assert thermal.cold_leakage_mw < 100.0  # 背侧漏热极微弱 (毫瓦级)


def test_miri_active_cryocooler_physics():
    """断言 6: MIRI 闭式循环氦制冷机 6.7 K 工作基准"""
    thermal = calculate_sunshield_thermal()
    # MIRI 工作在 6.7 K (距离绝对零度仅 6.7 度)
    assert 6.0 <= thermal.miri_temp_k <= 7.0
    assert thermal.miri_temp_k < thermal.cold_side_temp_k


def test_optics_diffraction_limit_and_sensitivity():
    """断言 7: 6.5 米口径衍射极限、角分辨率与极端红移"""
    optics = calculate_optical_capabilities()
    assert optics.aperture_m == 6.5
    assert optics.collecting_area_m2 >= 25.0
    # 2 微米近红外衍射极限在 70 ~ 85 毫角秒之间
    assert 70.0 <= optics.diffraction_limit_2um_mas <= 85.0
    # 10 微米中红外衍射极限在 350 ~ 420 毫角秒之间
    assert 350.0 <= optics.diffraction_limit_10um_mas <= 420.0
    # 灵敏度达 10 nJy
    assert optics.limiting_sensitivity_njy <= 10.0
    # 可探测红移 z >= 14
    assert optics.max_redshift_z >= 14.0


def test_grand_septet_completeness():
    """断言 8: 2026 深空七极黄金舰队对偶矩阵完备性"""
    fleet = calculate_grand_septet_summary()
    assert len(fleet) == 7
    names = [p["name"] for p in fleet]
    assert any("旅行者 1 号" in n for n in names)
    assert any("帕克" in n for n in names)
    assert any("贝皮可伦坡" in n for n in names)
    assert any("赫拉号" in n for n in names)
    assert any("欧罗巴快船" in n for n in names)
    assert any("JUICE" in n for n in names)
    assert any("韦伯" in n or "JWST" in n for n in names)
    
    # 验证极距跨度: 帕克 0.045 AU 至 旅行者 173 AU，跨度超 3700 倍
    min_dist = min(p["distance_au"] for p in fleet)
    max_dist = max(p["distance_au"] for p in fleet)
    assert min_dist < 0.05
    assert max_dist > 170.0
    assert (max_dist / min_dist) > 3700.0
    
    # 验证极端温度跨度: 旅行者 2.7 K 至 帕克 1673 K
    temps = [p["temp_k"] for p in fleet]
    assert min(temps) <= 2.7
    assert max(temps) >= 1600.0
