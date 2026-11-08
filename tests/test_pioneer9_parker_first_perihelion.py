"""
Unit tests for Pioneer 9 58th anniversary & Parker Solar Probe 1st perihelion dynamics engine.
"""

import math
import datetime
import sys
from pathlib import Path
import pytest

DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR / "scripts"))

from pioneer9_parker_first_perihelion_engine import (
    Pioneer9ParkerPerihelionEngine,
    SOLAR_CONSTANT_1AU,
    AU_METERS,
    R_SUN_METERS
)


def test_pioneer9_timeline_and_lifetime():
    engine = Pioneer9ParkerPerihelionEngine()
    timeline = engine.compute_pioneer9_timeline_and_orbit()

    # 58 周年验证 (1968-11-08 至 2026-11-08)
    assert timeline["total_elapsed_years"] >= 57.99
    # 实测服役超过 5000 天 (14+ 年)
    assert timeline["active_service_days"] > 5200.0
    assert timeline["active_service_years"] > 14.0
    # 超出设计寿命 (180 天) 25 倍以上
    assert timeline["lifetime_margin_factor"] > 25.0


def test_pioneer9_keplerian_orbit():
    engine = Pioneer9ParkerPerihelionEngine()
    orbit = engine.compute_pioneer9_timeline_and_orbit()

    # 轨道半长轴在 0.85 ~ 0.90 AU 区间
    assert 0.85 < orbit["semi_major_axis_au"] < 0.90
    # 偏心率约 0.135
    assert 0.10 < orbit["eccentricity"] < 0.18
    # 公转周期 290 ~ 305 天
    assert 290.0 < orbit["period_days"] < 305.0
    # 58 年公转圈数超过 70 圈
    assert orbit["orbital_revolutions_completed"] > 70.0
    # 活力公式：近日点速度大于远日点速度
    assert orbit["v_perihelion_kms"] > orbit["v_aphelion_kms"]
    assert 34.0 < orbit["v_perihelion_kms"] < 40.0
    assert 25.0 < orbit["v_aphelion_kms"] < 30.0


def test_parker_first_perihelion_8th_anniversary():
    engine = Pioneer9ParkerPerihelionEngine()
    psp = engine.compute_parker_first_perihelion_physics()

    # 8 周年整 (2018-11-08 至 2026-11-08)
    assert abs(psp["first_perihelion_elapsed_years"] - 8.0) < 0.1
    # 首次近日点距日心 0.166 AU，约 35 太阳半径
    assert psp["p1_distance_au"] == 0.166
    assert 30.0 < psp["p1_distance_solar_radii"] < 40.0
    # 速度约 95 km/s
    assert psp["p1_speed_kms"] == 95.3


def test_parker_solar_flux_and_thermal_escalation():
    engine = Pioneer9ParkerPerihelionEngine()
    psp = engine.compute_parker_first_perihelion_physics()

    # 平方反比律：S_p1 = S0 / (0.166)^2 ≈ 36.3 倍地球通量
    expected_flux_p1 = SOLAR_CONSTANT_1AU / (0.166 ** 2)
    assert abs(psp["p1_solar_flux_w_m2"] - expected_flux_p1) < 1.0
    assert 35.0 < psp["p1_flux_earth_ratio"] < 38.0

    # 极限近日点 0.046 AU 较第 1 次近日点能流增大约 13 倍
    assert 12.5 < psp["flux_escalation_ratio"] < 13.5
    assert psp["p24_flux_earth_ratio"] > 450.0

    # 极限近日点热盾表面温度超过 1400 °C，远高于第 1 次近日点
    assert psp["p24_tps_equilibrium_celsius"] > psp["p1_tps_equilibrium_celsius"]
    assert psp["p24_tps_equilibrium_celsius"] > 1400.0


def test_night_darksky_status():
    engine = Pioneer9ParkerPerihelionEngine()
    sky = engine.compute_night_darksky_status()

    # 残月亮面小于 1%
    assert sky["lunar_phase_percent"] < 1.0
    # 月龄接近 29 天
    assert 28.0 < sky["moon_age_days"] < 29.5
    # 距精确新月朔日约 16.5 小时 (明日 15:02 CST)
    assert 15.0 < sky["hours_to_exact_new_moon"] < 18.0
    # 100% 纯黑夜空
    assert sky["darksky_window_percent"] == 100.0
