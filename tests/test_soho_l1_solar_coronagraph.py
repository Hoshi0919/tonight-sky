"""
SOHO 日地 L1 晕轨道动力学、LASCO 日冕仪、CME 空间天气预警、
克鲁兹彗星猎手与深空二十四极黄金舰队单元测试集
"""

import sys
from pathlib import Path
import pytest
from datetime import datetime, timezone

scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from soho_l1_solar_coronagraph_engine import (
    SOHOL1SolarCoronagraphEngine,
    SOHOEpochs,
    SPEED_OF_LIGHT,
    AU_KM,
    SOLAR_RADIUS_KM,
)


@pytest.fixture
def engine():
    return SOHOL1SolarCoronagraphEngine()


def test_crtbp_l1_solution(engine):
    """测试圆型限制性三体问题日地 L1 点数值解与光时延迟"""
    crtbp = engine.solve_crtbp_l1()
    # 距地距离在 149 万公里左右
    assert 1490000.0 < crtbp.distance_to_earth_km < 1495000.0
    # 归一化距离在 0.0099~0.0100 AU
    assert 0.00995 < crtbp.gamma_1_normalized < 0.01000
    # 日心极距在 0.9900 AU
    assert 0.9899 < crtbp.distance_to_sun_au < 0.9901
    # 单向光时在 4.97~4.98 秒之间
    assert 4.96 < crtbp.one_way_light_time_sec < 4.99
    # 往返光时约 9.95 秒
    assert 9.93 < crtbp.round_trip_light_time_sec < 9.98
    # SOHO 轨道处太阳能流微弱增高 (1380~1395 W/m^2)
    assert 1380.0 < crtbp.solar_flux_at_soho_wm2 < 1395.0


def test_halo_orbit_rf_exclusion(engine):
    """测试晕轨道大振幅几何与 3.5° 太阳射电回避死区判定"""
    halo = engine.compute_halo_orbit_metrics()
    assert halo.orbit_period_days == pytest.approx(177.8, rel=1e-2)
    assert halo.amplitude_y_km == 650000.0
    assert halo.amplitude_z_km == 200000.0
    # 回避角必须大于 3.5 度以避开强微波噪声
    assert halo.min_separation_deg >= 3.5
    assert halo.min_projected_offset_km > 90000.0
    assert halo.avoids_solar_radio_exclusion is True
    # 年维持速度增量很小 (< 5 m/s)
    assert 1.0 < halo.annual_station_keeping_dv_ms < 5.0


def test_mission_longevity(engine):
    """测试 SOHO 超 30 年在轨服役长寿统计"""
    ref_dt = datetime(2026, 10, 17, 7, 47, 0, tzinfo=timezone.utc)
    longevity = engine.compute_mission_longevity(ref_dt)
    assert longevity["total_days_in_space"] > 11200.0
    assert longevity["total_years_in_space"] >= 30.8
    assert longevity["halo_orbits_completed"] > 60.0
    assert longevity["solar_cycles_covered"] == 3
    assert longevity["longevity_multiplication_factor"] > 15.0


def test_lasco_coronagraph_optics(engine):
    """测试 LASCO C2 与 C3 日冕仪视场与行星际物理覆盖尺寸"""
    optics = engine.compute_lasco_optics()
    assert "C2" in optics and "C3" in optics

    c2 = optics["C2"]
    assert c2.fov_inner_rsun == 2.0
    assert c2.fov_outer_rsun == 6.0
    assert c2.total_diameter_km == pytest.approx(12.0 * SOLAR_RADIUS_KM, rel=1e-4)
    assert 3.0 < c2.angular_fov_deg < 3.5

    c3 = optics["C3"]
    assert c3.fov_inner_rsun == 3.7
    assert c3.fov_outer_rsun == 32.0
    # C3 总跨度超过 4400 万公里 (近 0.3 AU)
    assert c3.total_diameter_km > 44000000.0
    assert c3.total_diameter_au > 0.29
    assert 16.5 < c3.angular_fov_deg < 17.5
    # C2 分辨率优于 C3
    assert c2.spatial_resolution_arcsec < c3.spatial_resolution_arcsec


def test_cme_early_warning_dynamics(engine):
    """测试日冕物质抛射 (CME) 空间天气预警传播速度与预警时间裕量"""
    scenarios = engine.simulate_cme_early_warning()
    assert len(scenarios) == 4

    # 极端超级太阳风暴 (2500 km/s)
    super_storm = scenarios[0]
    assert super_storm.speed_kms == 2500.0
    assert 16.0 < super_storm.transit_time_to_earth_hours < 17.0
    assert 15.5 < super_storm.warning_lead_time_hours < 16.5

    # 高速 CME (1500 km/s)
    fast_storm = scenarios[1]
    assert fast_storm.speed_kms == 1500.0
    assert 27.0 < fast_storm.transit_time_to_earth_hours < 28.5
    assert fast_storm.warning_lead_time_hours > 26.5

    # 慢速 CME (500 km/s)
    slow_storm = scenarios[3]
    assert slow_storm.speed_kms == 500.0
    assert 80.0 < slow_storm.transit_time_to_earth_hours < 85.0
    assert 3.3 < slow_storm.transit_time_to_earth_days < 3.6


def test_comet_discoveries(engine):
    """测试 SOHO 发现 5,200+ 颗彗星与克鲁兹族掠日动力学"""
    comets = engine.get_comet_discovery_metrics()
    assert comets.total_comets_discovered >= 5200
    assert comets.kreutz_sungrazers_count > 4400
    assert comets.kreutz_percentage > 80.0
    # 近日点在 0.01 AU 以内
    assert comets.perihelion_distance_au < 0.01
    assert comets.amateur_discoverer_ratio > 90.0


def test_helioseismology_tachocline(engine):
    """测试日震学差旋层与太阳发电机动力学"""
    tacho = engine.get_helioseismology_tachocline()
    assert tacho.tachocline_radius_rsun == pytest.approx(0.713, abs=0.005)
    # 距日表深度在 19.5~20.5 万公里
    assert 195000.0 < tacho.tachocline_depth_km < 205000.0
    # 核心声速高达 500 km/s，表面仅约 7 km/s
    assert tacho.sound_speed_core_kms > 480.0
    assert tacho.sound_speed_surface_kms < 10.0
    # 声波 5 分钟 (3.3 mHz) 主振荡
    assert 4.8 < tacho.dominant_oscillation_period_min < 5.3
    assert 3.1 < tacho.dominant_frequency_mhertz < 3.5
    # 辐射区刚体自转周期约 26.6 天
    assert 26.0 < tacho.radiative_zone_rotation_days < 27.5


def test_1998_great_recovery(engine):
    """测试 1998 年绝境盲操复活历史数据"""
    rec = engine.get_recovery_story()
    # 失控持续超过 120 天
    assert rec.blackout_duration_days > 120.0
    assert rec.minimum_temperature_celsius <= -100.0
    assert rec.recovered_payload_count == 12
    assert rec.extended_mission_years > 27.0


def test_grand_quattuorvigintet_fleet_matrix(engine):
    """测试 2026 人类深空二十四极黄金舰队 (The Grand Quattuorvigintet) 矩阵与极端物理对偶"""
    fleet = engine.generate_grand_quattuorvigintet_fleet()
    assert len(fleet) == 24

    # 检验严格降序排列
    for i in range(len(fleet) - 1):
        assert (
            fleet[i].heliocentric_distance_au >= fleet[i + 1].heliocentric_distance_au
        ), f"Fleet order error at index {i}: {fleet[i].name} vs {fleet[i+1].name}"

    # 检验首尾与关键探测器
    assert "旅行者 1 号" in fleet[0].name
    assert fleet[0].heliocentric_distance_au == 173.22

    assert "旅行者 2 号" in fleet[1].name
    assert fleet[1].heliocentric_distance_au == 144.26

    # 检验 SOHO 处于第 20 位 (0.990 AU)
    assert "SOHO" in fleet[20].name
    assert fleet[20].heliocentric_distance_au == 0.990

    # 检验末尾帕克太阳探测器
    assert "帕克太阳探测器" in fleet[-1].name
    assert fleet[-1].heliocentric_distance_au == 0.046

    # 检验对偶极值比率
    metrics = engine.compute_fleet_dual_metrics()
    assert metrics["total_fleet_probe_count"] == 24
    # 日心极距跨度 > 3700 倍
    assert metrics["heliocentric_distance_span_ratio"] > 3700.0
    # 辐射能流落差 > 1400 万倍
    assert metrics["solar_flux_drop_ratio"] > 14000000.0
    # 极端速度跨度 > 2500 万倍
    assert metrics["extreme_velocity_span_ratio"] > 25000000.0
