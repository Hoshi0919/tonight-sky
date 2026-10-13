"""
测试帕克太阳探测器 (Parker Solar Probe) 极限近日点与日冕穿越天体力学推演引擎
"""

import sys
import math
from pathlib import Path
from datetime import date
import pytest

# 将 scripts 加入 Python 路径
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from parker_solar_probe_extreme_perihelion_engine import (
    SPEED_OF_LIGHT,
    AU_KM,
    SOLAR_RADIUS_KM,
    FINAL_ORBIT_PERIOD_DAYS,
    PERIHELION_RADIUS_KM,
    PERIHELION_RADIUS_AU,
    PERIHELION_SOLAR_RADII,
    PERIHELION_VELOCITY_KMS,
    APHELION_VELOCITY_KMS,
    PERIHELION_2026_EVENTS,
    get_orbital_metrics,
    compute_thermal_metrics,
    compute_relativistic_precession,
    compute_instantaneous_state,
    compare_with_voyager1,
    generate_full_psp_report
)


def test_orbital_mechanics_and_vis_viva():
    """验证开普勒终极轨道参数与活力公式速度"""
    orb = get_orbital_metrics()
    
    # 周期为 88 天
    assert math.isclose(orb.period_days, 88.0, abs_tol=1e-2)
    # 半长轴在 0.387 AU 附近
    assert 0.386 < orb.semi_major_axis_au < 0.388
    # 极端偏心率 ~0.8815
    assert 0.880 < orb.eccentricity < 0.883
    # 近日点在 9.85 R_sun，约 0.0459 AU
    assert 9.80 < orb.perihelion_rsun < 9.90
    assert 0.045 < orb.perihelion_au < 0.047
    # 距太阳光球表面约 616 万公里
    assert 6.15e6 < orb.perihelion_surface_alt_km < 6.20e6
    # 远日点在 0.728 AU (贴近金星轨道)
    assert 0.72 < orb.aphelion_au < 0.74
    # 近日点速度 190~192 km/s (人类极速)
    assert 190.0 < orb.perihelion_speed_kms < 192.5
    # 光速占比约 0.00064 c
    assert 0.00063 < orb.perihelion_speed_c_fraction < 0.00065
    # 远日点速度约 12 km/s
    assert 11.5 < orb.aphelion_speed_kms < 12.5
    # 极速比超过 15 倍
    assert orb.speed_ratio > 15.0


def test_extreme_thermal_and_heat_shield():
    """验证近日点极端热辐射通量与防热罩热工物理"""
    therm = compute_thermal_metrics()
    
    # 近日点辐射通量约 640~655 kW/m²
    assert 6.4e5 < therm.perihelion_flux_w_m2 < 6.6e5
    # 地球常数的 470~480 倍
    assert 470.0 < therm.flux_ratio_to_earth < 480.0
    # 防热罩迎日面温度约 1450~1500 K (~1170~1230 °C)
    assert 1400.0 < therm.equilibrium_temp_k < 1550.0
    assert 1150.0 < therm.equilibrium_temp_c < 1300.0
    # 仪器舱背阴面维持在 28 °C
    assert therm.bus_temp_c == 28.0
    # 绝热温降超过 1100 °C
    assert therm.temperature_drop_c > 1100.0
    # 径向温度梯度超万度/米
    assert therm.temperature_gradient_c_per_m > 10000.0
    # 传导热通量受限于低热导率碳泡沫 (< 800 W/m²)
    assert 500.0 < therm.conductive_heat_flux_w_m2 < 800.0


def test_general_relativistic_precession():
    """验证广义相对论引力场近日点进动效应"""
    rel = compute_relativistic_precession()
    
    # 单圈进动约 0.44~0.45 角秒
    assert 0.44 < rel.precession_arcsec_per_orbit < 0.45
    # 每年进动约 1.8~1.9 角秒
    assert 1.8 < rel.precession_arcsec_per_year < 1.9
    # 世纪进动率约 184~186 角秒/世纪
    assert 180.0 < rel.precession_arcsec_per_century < 190.0
    # 为水星进动 (42.98"/cy) 的 4.2~4.4 倍
    assert 4.2 < rel.ratio_to_mercury_precession < 4.4


def test_october_14_2026_current_state():
    """验证 2026-10-14 今日瞬时开普勒几何与状态"""
    today = date(2026, 10, 14)
    state = compute_instantaneous_state(today)
    
    # 距 P29 (09-05) 经过 39 天
    assert state.days_since_last_perihelion == 39.0
    # 距 10-19 远日点仅剩 5.0 天
    assert state.days_to_aphelion == 5.0
    # 距 P30 (12-02) 还有 49.0 天
    assert state.days_to_next_perihelion == 49.0
    # 真近点角已达 176°~178° (极度接近 180° 远日点)
    assert 175.0 < state.true_anomaly_deg < 179.0
    # 当前日心距离在 0.72 AU 附近 (154~156 R_sun)
    assert 0.71 < state.heliocentric_distance_au < 0.73
    assert 150.0 < state.heliocentric_distance_rsun < 160.0
    # 当前速度在 12.5~13.2 km/s 巡航低速
    assert 12.5 < state.heliocentric_velocity_kms < 13.2
    # 当前太阳光强仅约 1.8~2.0 倍地球
    assert 1.8 < state.flux_ratio_to_earth < 2.1
    # 防热罩当前表面温度低于 120 °C
    assert state.current_shield_temp_c < 120.0


def test_dual_extremes_comparison():
    """验证帕克 vs 旅行者1号深空极值对偶关系"""
    dual = compare_with_voyager1()
    
    # 空间距离比值约 3700~3800 倍
    assert 3700.0 < dual.distance_ratio < 3800.0
    # 辐射强度比值超 1400 万倍
    assert 1.4e7 < dual.solar_flux_ratio < 1.5e7
    # 速度比值超过 11 倍 (190.8 vs 16.9 km/s)
    assert 11.0 < dual.velocity_ratio < 11.5
    # 帕克近日点 0.0459 AU vs 旅行者一光日 173.14 AU
    assert math.isclose(dual.psp_perihelion_au, PERIHELION_RADIUS_AU, rel_tol=1e-3)
    assert math.isclose(dual.v1_milestone_au, 173.1446, rel_tol=1e-3)


def test_perihelion_2026_events_schedule():
    """验证 2026 年四次近日点交会历表合理性"""
    assert len(PERIHELION_2026_EVENTS) == 4
    
    # 编号为 27, 28, 29, 30
    nums = [e["num"] for e in PERIHELION_2026_EVENTS]
    assert nums == [27, 28, 29, 30]
    
    # 间隔应在 88~89 天之间 (开普勒周期)
    for i in range(len(PERIHELION_2026_EVENTS) - 1):
        dt = (PERIHELION_2026_EVENTS[i+1]["date_utc"] - PERIHELION_2026_EVENTS[i]["date_utc"]).days
        assert 88 <= dt <= 90


def test_full_report_generation():
    """验证学术报告文本生成与完整性"""
    report = generate_full_psp_report(date(2026, 10, 14))
    
    assert "帕克太阳探测器 (Parker Solar Probe)" in report
    assert "终极 88 天开普勒轨道" in report
    assert "极端热力学辐射与防热罩" in report
    assert "广义相对论近日点进动" in report
    assert "人类航天双极对偶" in report
    assert "190.77 km/s" in report
    assert "184.58 角秒 / 世纪" in report
