"""
欧罗巴快船 (Europa Clipper) MEGA 引力助推天体力学推演引擎单元测试
"""

import sys
import math
from pathlib import Path
from datetime import datetime, timezone
import pytest

# 将 scripts 加入 Python 路径
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from europa_clipper_mega_trajectory_engine import (
    get_full_europa_clipper_analysis,
    compute_hyperbolic_flyby,
    compute_heliocentric_orbit,
    compute_instantaneous_state,
    LAUNCH_UTC,
    MARS_FLYBY_UTC,
    EARTH_FLYBY_UTC,
    JUPITER_ARRIVAL_UTC,
    LAUNCH_MASS_KG,
    DRY_MASS_KG,
    PROPELLANT_MASS_KG,
    LAUNCH_C3_KM2_S2,
    LAUNCH_V_INF_KMS,
    MU_EARTH,
    MU_MARS,
    EARTH_RADIUS_KM,
    MARS_RADIUS_KM,
    SOLAR_ARRAY_SPAN_M,
    SOLAR_ARRAY_AREA_M2,
    EUROPA_RADIUS_KM,
    EUROPA_OCEAN_VOLUME_M3
)


def test_launch_energetics():
    """验证发射能量与运载基准参量"""
    assert LAUNCH_UTC.year == 2024
    assert LAUNCH_UTC.month == 10
    assert LAUNCH_UTC.day == 14
    
    assert LAUNCH_MASS_KG == 6065.0
    assert DRY_MASS_KG == 3315.0
    assert PROPELLANT_MASS_KG == 2750.0
    assert LAUNCH_MASS_KG == pytest.approx(DRY_MASS_KG + PROPELLANT_MASS_KG, abs=1.0)
    
    # 特征能量 C3 与无穷远速度 v_inf
    assert LAUNCH_C3_KM2_S2 == 41.69
    assert LAUNCH_V_INF_KMS == pytest.approx(math.sqrt(41.69), abs=1e-4)
    assert 6.45 < LAUNCH_V_INF_KMS < 6.46


def test_mars_gravity_assist_mechanics():
    """验证火星引力助推力学"""
    res = compute_hyperbolic_flyby(
        body_name="Mars",
        mu_body=MU_MARS,
        body_radius_km=MARS_RADIUS_KM,
        altitude_km=884.0,
        v_inf_kms=4.12,
        heliocentric_delta_v_boost_kms=1.80
    )
    assert res.periapsis_radius_km == pytest.approx(4273.5, abs=0.1)
    assert res.eccentricity == pytest.approx(2.694, abs=0.01)
    assert res.turn_angle_deg == pytest.approx(43.58, abs=0.1)
    assert res.heliocentric_delta_v_kms == 1.80
    assert res.periapsis_speed_kms > res.v_infinity_kms


def test_earth_gravity_assist_mechanics():
    """验证地球引力助推 (EGA) 核心天体力学"""
    res = compute_hyperbolic_flyby(
        body_name="Earth",
        mu_body=MU_EARTH,
        body_radius_km=EARTH_RADIUS_KM,
        altitude_km=3200.0,
        v_inf_kms=6.15,
        heliocentric_delta_v_boost_kms=3.90
    )
    # 近掠半径与地球半径比值 ~1.50 R_earth
    assert res.periapsis_radius_km == pytest.approx(9578.14, abs=0.1)
    assert res.periapsis_radius_km / EARTH_RADIUS_KM == pytest.approx(1.5017, abs=0.01)
    
    # 双曲线偏心率与渐近线偏折角
    assert res.eccentricity == pytest.approx(1.9089, abs=0.01)
    assert res.turn_angle_deg == pytest.approx(63.19, abs=0.1)
    
    # 近地点极速超过 11 km/s (近 4 万公里/小时)
    assert res.periapsis_speed_kms == pytest.approx(11.002, abs=0.01)
    assert res.periapsis_speed_kms * 3600.0 > 39600.0
    
    # 地心矢量偏转量与日心增量
    assert res.deflection_delta_v_kms == pytest.approx(6.444, abs=0.01)
    assert res.heliocentric_delta_v_kms == 3.90


def test_heliocentric_transfer_orbits():
    """验证日心转移轨道几何演化"""
    # 地火段
    leg1 = compute_heliocentric_orbit(1.00, 1.524)
    assert leg1.semi_major_axis_au == pytest.approx(1.262, abs=0.01)
    assert leg1.eccentricity == pytest.approx(0.2076, abs=0.01)
    
    # EGA 助推后直奔木星终极转移轨道
    post_ega = compute_heliocentric_orbit(1.00, 5.30)
    assert post_ega.semi_major_axis_au == pytest.approx(3.15, abs=0.01)
    assert post_ega.eccentricity == pytest.approx(0.6825, abs=0.01)
    assert post_ega.period_years == pytest.approx(5.59, abs=0.05)
    
    # 远日点速度显著低于近日点速度 (开普勒活力公式守恒)
    assert post_ega.perihelion_speed_kms > 37.0
    assert post_ega.aphelion_speed_kms < 7.5
    assert post_ega.perihelion_speed_kms / post_ega.aphelion_speed_kms == pytest.approx(5.3, abs=0.2)


def test_instantaneous_state_2026_10_14():
    """验证 2026-10-14 发射两周年整即时状态"""
    ref_dt = datetime(2026, 10, 14, 16, 6, 0, tzinfo=timezone.utc) # 严格发射两周年整
    status = compute_instantaneous_state(ref_dt)
    
    # 整整运行 730 天 (2.00 年)
    assert status.days_since_launch == pytest.approx(730.0, abs=0.01)
    assert status.years_since_launch == pytest.approx(2.00, abs=0.01)
    
    # 距 2026-12-03 21:15 UTC 地球引力助推仅 50.2 天
    assert status.days_until_earth_flyby == pytest.approx(50.21, abs=0.1)
    
    # 距地几何距离约 0.468 AU，光行时 3 分 53 秒
    assert status.geocentric_distance_au == pytest.approx(0.4679, abs=0.001)
    assert 230.0 < status.light_travel_time_seconds < 235.0
    assert "3分" in status.light_travel_time_str
    assert "天蝎座" in status.target_constellation


def test_solar_array_physics_at_jupiter():
    """验证 5.2 AU 太阳能逆平方反比衰减与超大阵列能效"""
    full_data = get_full_europa_clipper_analysis()
    solar = full_data["solar_power_physics"]
    
    assert solar["array_span_m"] == 30.5
    assert solar["array_area_m2"] == 102.0
    assert solar["solar_flux_5_2au_w_m2"] == pytest.approx(50.33, abs=0.1)
    assert solar["solar_flux_ratio_percent"] == pytest.approx(3.70, abs=0.05)
    
    # 木星处实际发电能力充裕超越 700 W 基准线
    assert solar["power_output_at_jupiter_w"] > 700.0
    assert solar["power_output_at_jupiter_w"] == pytest.approx(708.5, abs=5.0)


def test_europa_ocean_and_laplace_resonance():
    """验证木卫二海洋学物理与拉普拉斯潮汐共振"""
    full_data = get_full_europa_clipper_analysis()
    ocean = full_data["europa_ocean_physics"]
    
    assert ocean["radius_km"] == 1560.8
    assert ocean["ice_shell_thickness_km"] == 20.0
    assert ocean["ocean_depth_km"] == 100.0
    assert ocean["ocean_volume_m3"] == 3.0e18
    
    # 水体总量达到地球全部海洋总和的 2.25 倍
    assert ocean["water_volume_multiple_of_earth"] == pytest.approx(2.25, abs=0.05)
    assert ocean["forced_eccentricity"] == 0.009
    assert ocean["tidal_heating_power_w"] == 1.0e12
    assert "1 : 木卫二(Europa) 2" in ocean["laplace_resonance_ratio"]


def test_full_analysis_consistency():
    """验证整体分析包数据完整性与键值覆盖"""
    full_data = get_full_europa_clipper_analysis()
    expected_sections = [
        "launch",
        "mars_gravity_assist",
        "earth_gravity_assist",
        "transfer_orbits",
        "jupiter_capture",
        "solar_power_physics",
        "europa_ocean_physics",
        "instantaneous_today"
    ]
    for sec in expected_sections:
        assert sec in full_data, f"缺失分析模块: {sec}"
    
    assert full_data["jupiter_capture"]["planned_europa_flybys"] == 49
    assert full_data["jupiter_capture"]["min_europa_flyby_altitude_km"] == 25.0
