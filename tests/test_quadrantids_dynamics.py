"""
test_quadrantids_dynamics.py
============================
单元测试套件：2027 年象限仪座流星雨（Quadrantids 2027）天体动力学推演与西域晨光优势引擎
(Unit tests for 2027 Quadrantids Meteor Shower Dynamics Engine)
"""

import math
from datetime import datetime, timezone, timedelta
import pytest
import ephem

import sys
from pathlib import Path
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from quadrantids_dynamics_engine import (
    calculate_parent_body_mechanics,
    calculate_ablation_and_shock_physics,
    calculate_solar_longitude_and_peak,
    get_quadrantids_zhr_profile,
    calculate_radiant_and_moon_status,
    evaluate_western_china_advantage,
    generate_full_quadrantids_report,
    CIRCUMPOLAR_MIN_LAT,
    QUADRANTIDS_SOLAR_LON_PEAK,
    QUADRANTIDS_ENTRY_VELOCITY,
    CST_TZ
)


def test_parent_body_and_orbital_mechanics():
    """验证母体小行星 2003 EH1 及明代弘治彗星 C/1490 Y1 轨道参量与高倾角特征"""
    mech = calculate_parent_body_mechanics()
    
    assert "(196256) 2003 EH1" in mech["parent_body"]
    assert "C/1490 Y1" in mech["historical_comet"]
    assert "弘治" in mech["historical_comet"]
    
    # 轨道倾角高达 71.4° (典型穿透黄道面的高倾角动力学拓扑)
    assert 70.0 <= mech["inclination_deg"] <= 73.0
    
    # 半长轴与偏心率
    assert 3.0 <= mech["semi_major_axis_au"] <= 3.3
    assert 0.60 <= mech["eccentricity"] <= 0.65
    assert 5.0 <= mech["orbital_period_years"] <= 6.0
    
    # 碎屑流管束演化年龄（明孝宗弘治三年 1490 年至 2026/2027 年约 536 年）
    assert 500.0 <= mech["stream_dispersion_age_years"] <= 550.0


def test_ablation_and_energy_density():
    """验证 41.2 km/s 中高极速切入大气层时的气动激波与动能密度"""
    abl = calculate_ablation_and_shock_physics()
    
    # 大气层相对切入速度 41.2 km/s (时速约 14.8 万 km/h)
    assert 40.5 <= abl["entry_velocity_kms"] <= 42.0
    assert abl["entry_velocity_kmh"] > 140000.0
    
    # 单位质量动能释放 ~848.7 MJ/kg，相当于 > 200 倍 TNT 当量
    assert 840.0 <= abl["specific_kinetic_energy_mj_per_kg"] <= 860.0
    assert abl["tnt_equivalent_factor"] > 200.0
    
    # 1 毫克 (1e-6 kg) 颗粒动能约为 848.7 J
    assert 840.0 <= abl["kinetic_energy_1mg_joules"] <= 860.0
    
    # 激波停滞温度与消融层高度
    assert 6800.0 <= abl["shock_stagnation_temp_k"] <= 7600.0
    assert abl["ablation_altitude_range_km"] == [95.0, 105.0]
    
    # 包含中性钠、镁与铁原子光谱辐射
    emissions_str = "".join(abl["dominant_emission_lines"])
    assert "Na I" in emissions_str
    assert "Mg I" in emissions_str
    assert "Fe I" in emissions_str


def test_fwhm_narrow_peak_profile():
    """验证 4 小时超窄通量半高宽与尖峰通量几何"""
    # 峰值所在时刻 (2027-01-04 11:40 CST，太阳视黄经 283.16°)
    dt_peak = datetime(2027, 1, 4, 11, 40, tzinfo=CST_TZ)
    sol_lon = calculate_solar_longitude_and_peak(dt_peak.astimezone(timezone.utc))
    assert abs(sol_lon - QUADRANTIDS_SOLAR_LON_PEAK) < 0.01
    
    # 峰值 ZHR 达到 110
    peak_zhr = get_quadrantids_zhr_profile(QUADRANTIDS_SOLAR_LON_PEAK)
    assert peak_zhr >= 105.0
    
    # 离开峰值 4 小时（对应黄经差约 0.164°），ZHR 应衰减至半高（~55 左右）
    zhr_4h_off = get_quadrantids_zhr_profile(QUADRANTIDS_SOLAR_LON_PEAK + 0.164)
    assert zhr_4h_off <= 65.0
    
    # 离开峰值 10 小时，ZHR 应回落至背景平静期 (<= 15)
    zhr_10h_off = get_quadrantids_zhr_profile(QUADRANTIDS_SOLAR_LON_PEAK + 0.41)
    assert zhr_10h_off <= 15.0


def test_circumpolar_threshold_geometry():
    """验证华北/东北与西域恒显圈判定 (纬度 >= 40.5°N)"""
    assert CIRCUMPOLAR_MIN_LAT == 40.5
    
    # 漠河 (52.97°N) 与 乌鲁木齐 (43.83°N) 必须恒显 (终夜不落)
    report = generate_full_quadrantids_report()
    circumpolar = report["peak_geometry"]["circumpolar_cities_china"]
    dipping = report["peak_geometry"]["dipping_cities_china"]
    
    assert "漠河" in circumpolar
    assert "乌鲁木齐" in circumpolar
    assert "哈尔滨" in circumpolar
    
    # 上海 (31.23°N) 与 广州 (23.13°N) 必须下潜
    assert "上海" in dipping
    assert "广州" in dipping
    assert "成都" in dipping


def test_lunar_conditions_and_negligible_light_loss():
    """验证农历冬月廿六~廿七 13.5% 纤细残月带来的极佳暗空条件"""
    # 2027-01-04 03:00 CST 上海与北京天幕
    t_test = datetime(2027, 1, 4, 3, 0, tzinfo=CST_TZ)
    sh_stat = calculate_radiant_and_moon_status("Shanghai", t_test)
    
    # 月相约 13%~15%
    assert 12.0 <= sh_stat["moon_phase_percent"] <= 16.0
    # 03:00 CST 月球尚在地平线下，光害完全为零，极限星等维持 6.5 等
    assert sh_stat["moon_alt_deg"] < 0.0
    assert sh_stat["nelm"] >= 6.45
    assert sh_stat["twilight_status"] == "纯黑暗夜 (Pure Night)"


def test_western_china_advantage():
    """验证 2027 年 1 月 4 日早晨华夏西域（乌鲁木齐等）相比东部的关键观测优势"""
    adv = evaluate_western_china_advantage()
    comp = adv["comparison_analysis"]
    
    # 07:30 CST：东部京沪已日出或处于民用晨光（太阳高度角 >= -6°）
    sh_sun = comp["eastern_cities_status_0730"]["Shanghai"]["sun_alt"]
    bj_sun = comp["eastern_cities_status_0730"]["Beijing"]["sun_alt"]
    assert sh_sun >= -6.0 or comp["eastern_cities_status_0730"]["Shanghai"]["visible"] is False
    assert bj_sun >= -6.0 or comp["eastern_cities_status_0730"]["Beijing"]["visible"] is False
    
    # 07:30 CST：乌鲁木齐太阳高度仍低至 -23.3°（全黑夜空！），辐射点仰角达 58.3°
    um_0730 = comp["urumqi_status_0730"]
    assert um_0730["sun_alt"] <= -18.0
    assert um_0730["radiant_alt"] > 55.0
    assert um_0730["twilight_status"] == "纯黑暗夜 (Pure Night)"
    
    # 08:30 CST：乌鲁木齐太阳仍处于航海晨光 (-12.8°)，辐射点达 68.0°，距离 11:40 尖峰仅 3.1 小时
    um_0830 = comp["urumqi_status_0830"]
    assert um_0830["sun_alt"] <= -12.0
    assert um_0830["radiant_alt"] >= 65.0
    assert um_0830["hours_to_peak"] <= 3.5
    assert um_0830["hr_obs"] > 0.0


def test_reference_stars_geometry():
    """验证象限仪座古天区与北斗七星、大角星等周边亮星的几何标尺"""
    rad = ephem.FixedBody()
    rad._ra = ephem.hours("15:18:00")
    rad._dec = ephem.degrees("49:30:00")
    rad.compute()
    
    # 摇光 (Alkaid, 北斗七星斗柄之端)：角距约 14.7°
    alkaid = ephem.FixedBody()
    alkaid._ra = ephem.hours("13:47:32")
    alkaid._dec = ephem.degrees("49:18:48")
    alkaid.compute()
    sep_alkaid = float(ephem.separation(rad, alkaid)) * 180.0 / ephem.pi
    assert 14.0 <= sep_alkaid <= 15.5
    
    # 梗河一 (Beta Boo)：角距约 9.5°
    nekkar = ephem.FixedBody()
    nekkar._ra = ephem.hours("15:01:57")
    nekkar._dec = ephem.degrees("40:23:26")
    nekkar.compute()
    sep_nekkar = float(ephem.separation(rad, nekkar)) * 180.0 / ephem.pi
    assert 9.0 <= sep_nekkar <= 10.2
