"""
test_queqiao2_lunar_frozen_orbit.py
===================================
中国探月四期 鹊桥二号中继卫星 (Queqiao-2 Relay Satellite)
环月大椭圆冻结轨道天体力学、月瘤引力摄动抑制、
4.2米伞状展开式天线微波链路与 2026 人类深空十八极黄金舰队 (The Grand Octodecet) 测试集。
"""

import sys
import os
import math
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))

from queqiao2_lunar_frozen_orbit_engine import (
    Queqiao2LunarFrozenOrbitEngine,
    MOON_RADIUS_KM,
    MOON_GM_KM3_S2,
    EARTH_MOON_MEAN_DISTANCE_KM,
    ANTENNA_DIAMETER_M,
    ANTENNA_MESH_MASS_KG,
    QUEQIAO2_WET_MASS_KG,
    DESIGN_LIFETIME_YEARS
)


@pytest.fixture
def engine():
    return Queqiao2LunarFrozenOrbitEngine()


def test_measured_orbit_keplerian_dynamics(engine):
    """测试 1: 验证鹊桥二号实测 26.2 小时环月大椭圆轨道开普勒动力学与活力公式速度"""
    orbit = engine.compute_measured_mission_orbit()
    assert 250.0 <= orbit.periapsis_altitude_km <= 260.0
    assert 16900.0 <= orbit.apoapsis_altitude_km <= 17000.0
    assert abs(orbit.semi_major_axis_km - 10335.1) < 1.0
    assert 0.805 <= orbit.eccentricity <= 0.810
    assert abs(orbit.inclination_deg - 119.25) < 0.1

    # 周期验证：约 26.19 小时 (94,282 秒)
    assert 26.0 <= orbit.orbital_period_hours <= 26.5
    assert 94000.0 <= orbit.orbital_period_seconds <= 95000.0

    # 活力公式验证速度与速度比
    assert 2.09 <= orbit.periapsis_velocity_km_s <= 2.13  # 约 2.11 km/s
    assert 0.22 <= orbit.apoapsis_velocity_km_s <= 0.23  # 约 0.225 km/s
    assert orbit.velocity_ratio > 9.0  # 近心点速度是远心点的 9.38 倍


def test_nominal_design_orbit_and_future_12h_orbit(engine):
    """测试 2: 验证工程标称 24.0 小时轨道与后续嫦娥七号 12.0 小时南极使命轨道"""
    nom = engine.compute_nominal_24h_orbit()
    assert nom.periapsis_altitude_km == 200.0
    assert nom.apoapsis_altitude_km == 16000.0
    assert 23.5 <= nom.orbital_period_hours <= 24.5
    assert 0.79 <= nom.eccentricity <= 0.81

    fut = engine.compute_future_12h_south_pole_orbit()
    assert fut.periapsis_altitude_km == 300.0
    assert fut.apoapsis_altitude_km == 8600.0
    assert 11.5 <= fut.orbital_period_hours <= 12.5
    assert 0.65 <= fut.eccentricity <= 0.75


def test_dwell_time_fraction_apoapsis_half(engine):
    """测试 3: 验证开普勒方程解析解算远月点半球 (覆盖南极与月背) 滞留时间占比 > 94%"""
    meas = engine.compute_measured_mission_orbit()
    dwell = engine.compute_dwell_time_metrics(meas)

    # 远心点半球 (theta in [90°, 270°]) 滞留时间比例应超过 94%
    assert dwell.apoapsis_dwell_fraction > 0.94
    assert 0.94 <= dwell.apoapsis_dwell_fraction <= 0.96  # 实测 95.07%
    assert dwell.apoapsis_dwell_hours > 24.0  # 26.19h 轨道中连续覆盖 24.9 小时
    assert dwell.periapsis_transit_hours < 1.5  # 近月点快速掠过仅 1.29 小时

    # 远近滞留比例超过 19:1
    assert dwell.south_pole_view_efficiency_ratio > 18.0
    assert abs((dwell.apoapsis_dwell_fraction + dwell.periapsis_transit_fraction) - 1.0) < 1e-6


def test_frozen_orbit_stability_and_mascon_cancellation(engine):
    """测试 4: 验证近月点幅角锁定 ω=90° 自主抑制月瘤与 J3 奇次摄动，保障 8 年寿命"""
    stability = engine.compute_frozen_orbit_stability()
    assert stability.argument_of_periapsis_deg == 90.0
    assert stability.eccentricity_secular_drift_rate == 0.0
    assert stability.periapsis_secular_drift_rate == 0.0
    assert stability.is_frozen is True
    assert stability.design_lifetime_years >= DESIGN_LIFETIME_YEARS
    assert "omega=90" in stability.perturbation_cancellation_mechanism


def test_antenna_rf_link_aperture_gain_and_beamwidth(engine):
    """测试 5: 验证 4.2 米展开天线口径面积、X/Ka 频段高增益与波束覆盖特性"""
    x_band = engine.compute_antenna_link_metrics(frequency_ghz=8.4, efficiency=0.55)
    ka_band = engine.compute_antenna_link_metrics(frequency_ghz=32.0, efficiency=0.55)

    # 4.2米口径物理面积
    expected_area = math.pi * (ANTENNA_DIAMETER_M / 2.0) ** 2
    assert abs(x_band.aperture_area_m2 - expected_area) < 1e-3

    # X 频段 (8.4 GHz) 增益与波束角
    assert 48.0 <= x_band.gain_dbi <= 49.5  # 约 48.76 dBi
    assert 0.55 <= x_band.half_power_beamwidth_deg <= 0.65  # 约 0.595°
    assert 34.0 <= x_band.half_power_beamwidth_arcmin <= 37.0  # 约 35.7' 恰好整包月面 (31~34')

    # Ka 频段 (32.0 GHz) 增益与波束角
    assert 59.5 <= ka_band.gain_dbi <= 61.0  # 约 60.38 dBi
    assert 0.14 <= ka_band.half_power_beamwidth_deg <= 0.18  # 约 0.156°
    assert 8.5 <= ka_band.half_power_beamwidth_arcmin <= 10.5  # 约 9.4' 窄波束对地高速数传


def test_earth_moon_light_time_and_delay(engine):
    """测试 6: 验证地月 38.44 万公里单向/往返通信光时与秒级响应基准"""
    metrics = engine.compute_antenna_link_metrics(frequency_ghz=32.0)
    assert abs(metrics.earth_moon_distance_km - EARTH_MOON_MEAN_DISTANCE_KM) < 1.0
    assert 1.25 <= metrics.one_way_light_time_seconds <= 1.30  # 约 1.282 秒
    assert 2.50 <= metrics.round_trip_light_time_seconds <= 2.60  # 约 2.564 秒
    assert metrics.free_space_path_loss_db > 210.0  # Ka 频段空间损耗超 214 dB


def test_grand_octodecet_fleet_cardinality_and_ordering(engine):
    """测试 7: 验证十八极深空黄金舰队成员数严格为 18 且日心距离严格单调递减"""
    fleet = engine.get_grand_octodecet_fleet()
    assert len(fleet) == 18

    distances = [c.distance_au for c in fleet]
    for i in range(len(distances) - 1):
        assert distances[i] >= distances[i + 1], f"舰队未按日心距离降序排列: {fleet[i].name} < {fleet[i+1].name}"

    names = [c.name for c in fleet]
    assert "Queqiao-2" in names
    assert "Perseverance" in names
    assert "Voyager 1" in names
    assert "Parker Solar Probe" in names
    assert "Hayabusa2# (SHARP)" in names
    assert "Tianwen-2" in names
    assert "BepiColombo" in names


def test_grand_octodecet_fleet_extremes_ratios(engine):
    """测试 8: 验证十八极黄金舰队日心、地心与光时极端物理解算跨度"""
    extremes = engine.compute_fleet_extremes()
    assert extremes["fleet_size"] == 18
    assert extremes["max_distance_au"] == 173.22  # Voyager 1
    assert extremes["min_distance_au"] == 0.046   # Parker Solar Probe
    assert extremes["heliocentric_distance_ratio"] > 3700.0
    assert extremes["solar_radiation_flux_ratio"] > 1.4e7  # 太阳辐射落差超 1400 万倍
    assert extremes["geocentric_distance_span_ratio"] > 65000.0  # V1 vs Q2 地心跨度超 6.7 万倍
    assert extremes["communication_owlt_span_ratio"] > 65000.0  # 光时跨度超 6.7 万倍
    assert extremes["temperature_span_k"] > 1650.0  # 1400°C 对偶 2.7K


def test_cislunar_relay_antenna_structure_and_spacecraft_mass(engine):
    """测试 9: 验证鹊桥二号 1.2 吨湿重、20 公斤超轻镀金钼丝经编反射面网与 18 微米线径"""
    metrics = engine.compute_antenna_link_metrics(8.4)
    assert abs(QUEQIAO2_WET_MASS_KG - 1200.0) < 1.0
    assert abs(ANTENNA_MESH_MASS_KG - 20.0) < 1.0
    assert metrics.mesh_wire_diameter_microns == 18.0
    assert "molybdenum" in metrics.mesh_material_description.lower()
