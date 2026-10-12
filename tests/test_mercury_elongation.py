"""
test_mercury_elongation.py — 2026 年水星东大距、开普勒轨道动力学与暮光三曜连珠单元测试集
"""

import sys
import os
import pytest

# 添加 scripts 目录至模块搜索路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from mercury_greatest_elongation_engine import (
    airmass,
    extinct_mag,
    calculate_keplerian_elongation_extremes,
    calculate_mercury_greatest_elongation,
    calculate_trio_alignment,
    calculate_geographic_visibility,
    calculate_day_night_relay,
)


def test_keplerian_elongation_extremes():
    """验证水星开普勒高偏心率轨道理论大距极值"""
    ext = calculate_keplerian_elongation_extremes()
    assert ext["semi_major_axis_au"] == pytest.approx(0.387098, abs=1e-4)
    assert ext["eccentricity"] == pytest.approx(0.20563, abs=1e-4)
    assert 17.8 <= ext["theoretical_min_elongation_deg"] <= 18.1
    assert 27.7 <= ext["theoretical_max_elongation_deg"] <= 28.0
    assert 9.7 <= ext["elongation_amplitude_deg"] <= 10.1


def test_mercury_greatest_elongation_timing():
    """验证 2026-10-12 水星东大距时刻与轨道几何参数"""
    opp = calculate_mercury_greatest_elongation()
    assert "2026-10-12 18:0" in opp["moment_cst"]
    assert 25.1 <= opp["max_elongation_deg"] <= 25.2
    assert opp["elongation_direction"] == "East (Evening)"
    # 日心距处于远日点附近（>80%）
    assert opp["aphelion_proximity_ratio"] > 0.78
    assert 0.43 <= opp["mercury_sun_distance_au"] <= 0.44
    assert 0.0 <= opp["apparent_magnitude"] <= 0.15
    assert 60.0 <= opp["phase_percent"] <= 63.0


def test_trio_alignment_collinearity():
    """验证黄昏西南天‘金星-初三蛾眉月-水星’三曜近乎严格共线连珠"""
    trio = calculate_trio_alignment()
    seps = trio["separations"]

    # 金星与月球、月球与水星间距
    assert 3.8 <= seps["venus_to_moon_deg"] <= 4.3
    assert 4.4 <= seps["moon_to_mercury_deg"] <= 4.9
    assert 8.4 <= seps["venus_to_mercury_total_deg"] <= 8.8

    # 直线度偏差残差极其微小（< 10 角分 / 0.16°）
    assert seps["collinearity_residual_arcmin"] < 10.0
    assert seps["is_quasi_linear"] is True

    # 视圆面与相位断言
    assert trio["venus"]["phase_percent"] < 7.0  # 极细金钩
    assert trio["venus"]["size_arcsec"] > 55.0  # 近下合大视圆面
    assert trio["moon"]["phase_percent"] < 5.0   # 农历初三纤细月牙
    assert trio["mercury"]["phase_percent"] > 55.0  # 水星处于凸相


def test_geographic_latitude_monotonicity():
    """验证秋季傍晚黄道交角带来的南北纬度仰角单调性"""
    cities = calculate_geographic_visibility()
    city_map = {c["city_en"]: c for c in cities}

    # 低纬度城市日落仰角显著高于高纬度城市
    alt_sanya = city_map["Sanya"]["sunset_state"]["mercury_alt_deg"]
    alt_gz = city_map["Guangzhou"]["sunset_state"]["mercury_alt_deg"]
    alt_sh = city_map["Shanghai"]["sunset_state"]["mercury_alt_deg"]
    alt_bj = city_map["Beijing"]["sunset_state"]["mercury_alt_deg"]
    alt_ur = city_map["Urumqi"]["sunset_state"]["mercury_alt_deg"]

    assert alt_sanya > alt_gz > alt_sh > alt_bj > alt_ur

    # 日落后 30 分钟仰角与消光梯次
    alt_30m_sanya = city_map["Sanya"]["twilight_30m_state"]["mercury_alt_deg"]
    alt_30m_gz = city_map["Guangzhou"]["twilight_30m_state"]["mercury_alt_deg"]
    alt_30m_bj = city_map["Beijing"]["twilight_30m_state"]["mercury_alt_deg"]

    assert alt_30m_sanya > 9.0
    assert alt_30m_gz > 7.5
    assert alt_30m_bj < 4.0


def test_airmass_extinction_physics():
    """验证气团数与消光模型物理自洽性"""
    assert airmass(90.0) == pytest.approx(1.0, abs=0.01)
    assert airmass(30.0) == pytest.approx(2.0, abs=0.05)
    assert airmass(10.0) == pytest.approx(5.59, abs=0.1)
    assert airmass(0.0) == 40.0

    # 消光后星等必然变暗（增大）
    m_raw = 0.07
    m_ext_10 = extinct_mag(m_raw, 10.0)
    m_ext_5 = extinct_mag(m_raw, 5.0)
    assert m_ext_5 > m_ext_10 > m_raw


def test_day_night_relay_structure():
    """验证昼夜天象接力链结构完整性"""
    relay = calculate_day_night_relay()
    assert "stage_1_dusk" in relay
    assert "stage_2_descent" in relay
    assert "stage_3_midnight_vesta" in relay
    assert "stage_4_dawn_mars_m44" in relay
