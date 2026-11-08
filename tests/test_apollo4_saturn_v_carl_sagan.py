"""
Unit tests for Apollo 4 59th anniversary & Carl Sagan 92nd birth anniversary engine.
"""

import math
import datetime
import sys
from pathlib import Path
import pytest

DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR / "scripts"))

from apollo4_saturn_v_carl_sagan_engine import (
    Apollo4CarlSaganEngine,
    SPEED_OF_LIGHT,
    AU_METERS,
    SOLAR_CONSTANT_1AU,
    R_EARTH_METERS,
    STEFAN_BOLTZMANN
)


def test_apollo4_launch_timeline_and_propulsion():
    engine = Apollo4CarlSaganEngine()
    ap4 = engine.compute_apollo4_launch_and_reentry()

    # 59 周年整 (1967-11-09 至 2026-11-09)
    assert abs(ap4["elapsed_years"] - 59.0) < 0.1
    assert ap4["elapsed_days"] > 21500.0

    # 土星 5 号 S-IC 一级海平面推力超过 33 MN (约 750 万磅推力)
    assert 33.0 < ap4["liftoff_thrust_mn"] < 35.0
    assert 7.4e6 < ap4["liftoff_thrust_pounds"] < 7.8e6

    # 起飞推重比大于 1.15
    assert 1.15 < ap4["liftoff_twr"] < 1.30


def test_apollo4_s4b_restart_and_elliptical_orbit():
    engine = Apollo4CarlSaganEngine()
    ap4 = engine.compute_apollo4_launch_and_reentry()

    # 验证 S-IVB 二次点火送入的 185 x 18079 km 高椭圆轨道
    assert ap4["perigee_km"] == 185.0
    assert ap4["apogee_km"] == 18079.0
    assert 0.55 < ap4["orbit_eccentricity"] < 0.60

    # 轨道周期在 5.0 ~ 5.6 小时之间
    assert 5.0 < ap4["orbit_period_hours"] < 5.6

    # 活力公式验证：近地点速度大于远地点速度
    assert ap4["v_perigee_kms"] > ap4["v_apogee_kms"]
    assert 9.5 < ap4["v_perigee_kms"] < 11.0
    assert 2.5 < ap4["v_apogee_kms"] < 3.5


def test_apollo4_reentry_energy_and_heat_shield():
    engine = Apollo4CarlSaganEngine()
    ap4 = engine.compute_apollo4_launch_and_reentry()

    # 第二宇宙速度再入 (约 11.14 km/s / 40,000+ km/h)
    assert 11.0 < ap4["reentry_speed_kms"] < 11.3
    assert ap4["reentry_speed_kmh"] > 40000.0

    # 5.4 吨指令舱携带的再入动能达 300+ GJ
    assert 320.0 < ap4["reentry_kinetic_energy_gj"] < 350.0

    # Avcoat 防热盾承受极温高于 2500 °C
    assert ap4["heat_shield_temp_celsius"] >= 2700.0


def test_carl_sagan_92nd_anniversary():
    engine = Apollo4CarlSaganEngine()
    cs = engine.compute_carl_sagan_pale_blue_dot_and_greenhouse()

    # 92 周年诞辰 (1934-11-09 至 2026-11-09)
    assert abs(cs["sagan_birth_anniversary_years"] - 92.0) < 0.1


def test_pale_blue_dot_geometry():
    engine = Apollo4CarlSaganEngine()
    cs = engine.compute_carl_sagan_pale_blue_dot_and_greenhouse()

    # 距离约 60 亿公里 (40.11 AU)，光行时 5.5 小时以上
    assert 5.8 < cs["pbd_distance_billion_km"] < 6.2
    assert 5.4 < cs["pbd_light_hours"] < 5.7

    # 地球在 40 AU 处的视张角小于 0.5 角秒
    assert 0.40 < cs["pbd_earth_angular_diam_arcsec"] < 0.48

    # 旅行者 1 号窄角相机单像素为 2.096 角秒，地球仅占约 0.2 像素
    assert 2.0 < cs["pbd_pixel_scale_arcsec"] < 2.2
    assert 0.15 < cs["pbd_earth_pixel_fraction"] < 0.25

    # 视星等在 +11.5 到 +12.5 等之间
    assert 11.5 < cs["pbd_apparent_magnitude"] < 12.5


def test_venus_greenhouse_radiation_physics():
    engine = Apollo4CarlSaganEngine()
    cs = engine.compute_carl_sagan_pale_blue_dot_and_greenhouse()

    # 金星日面辐射通量约 2600 W/m2 (约为地球的 1.91 倍)
    assert 2550.0 < cs["venus_solar_flux_w_m2"] < 2650.0

    # 若无温室效应，裸星平衡温度极低 (约 -46 °C / 226 K)
    assert 220.0 < cs["venus_equilibrium_temp_k"] < 235.0
    assert -55.0 < cs["venus_equilibrium_temp_celsius"] < -40.0

    # 真实地表温度达 737 K (463+ °C)，温室抬升 500 °C 以上
    assert cs["venus_actual_surface_temp_k"] == 737.0
    assert cs["venus_greenhouse_temp_boost_c"] > 500.0

    # 灰体辐射传输要求红外光学厚度 tau 超过 140
    assert 140.0 < cs["venus_required_optical_depth_tau"] < 160.0


def test_night_darksky_status():
    engine = Apollo4CarlSaganEngine()
    sky = engine.compute_night_darksky_status()

    # 朔日新月亮面低于 0.5%
    assert sky["lunar_phase_percent"] < 0.5
    # 月龄小于 1 天
    assert sky["moon_age_days"] < 1.0
    # 距精确朔月时刻在 6 ~ 9 小时之间
    assert 6.0 < sky["hours_since_exact_new_moon"] < 9.0
    # 100% 纯黑夜空
    assert sky["darksky_window_percent"] == 100.0
