"""
test_overnight_celestial_relay.py — 2026-10-12 至 10-13 通宵八重天象大接力推演自动化单元测试集
"""

import sys
import os
import pytest

# 引入被测试脚本
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))
from overnight_celestial_relay_engine import (
    calculate_mercury_twilight_alignment,
    calculate_overnight_darkness,
    calculate_deepsky_planets_midnight,
    calculate_mars_praesepe_postmidnight,
    generate_full_relay_report,
)


def test_stage1_twilight_alignment_collinear_residual():
    """断言 1：黄昏三曜连珠共线残差极小 (<10')，水星离日角 >25°，金星呈极细金钩 (<10%)"""
    data = calculate_mercury_twilight_alignment()
    align = data["alignment"]
    merc = data["mercury"]
    venus = data["venus"]
    moon = data["moon"]

    # 水星处于东大距极大离日点 (>25°)
    assert merc["elongation_deg"] >= 25.0
    assert merc["mag"] <= 0.2

    # 金星与月球均呈现极细新月形
    assert venus["phase_percent"] < 10.0
    assert moon["phase_percent"] < 6.0

    # 三曜准共线残差小于 10 角分（仅 6.7 角分）
    assert align["collinear_residual_arcmin"] < 10.0
    # 总天球跨度约为 8.6°
    assert 8.0 <= align["total_span_deg"] <= 9.2


def test_stage2_darkness_window_and_zero_lunar_interference():
    """断言 2：华夏主要城市全夜独享近 10 小时纯暗夜，月光干扰严格为 0.0%"""
    for city_key in ["Beijing", "Shanghai", "Guangzhou", "Chengdu", "Sanya"]:
        dark_info = calculate_overnight_darkness(city_key)
        assert dark_info["dark_duration_hours"] >= 9.5
        assert dark_info["lunar_interference"] == 0.0


def test_stage3_m31_zenith_transit():
    """断言 3：M31 仙女座大星系在北京中天仰角突破 88°（直插天顶），上海突破 79°"""
    data = calculate_deepsky_planets_midnight()
    transits = data["cities_transit"]

    assert transits["Beijing"]["M31_alt"] >= 88.0
    assert transits["Shanghai"]["M31_alt"] >= 79.0
    assert transits["Guangzhou"]["M31_alt"] >= 71.0


def test_stage4_vesta_opposition_coordinates_and_magnitude():
    """断言 4：4 号灶神星视星等达到 6.39 等峰值，中天仰角在华夏全境均适宜双筒观测"""
    data = calculate_deepsky_planets_midnight()
    targets = data["targets"]
    vesta = targets["Vesta"]

    # 冲日前夕达到 6.39 等峰值
    assert 6.35 <= vesta["mag"] <= 6.45
    # 华夏主要城市中天仰角均在 45° 以上
    transits = data["cities_transit"]
    assert transits["Beijing"]["Vesta_alt"] >= 45.0
    assert transits["Shanghai"]["Vesta_alt"] >= 54.0
    assert transits["Guangzhou"]["Vesta_alt"] >= 62.0


def test_stage5_mars_praesepe_proximity():
    """断言 5：火星在巨蟹座贴近 M44 积尸气星团（角距 < 50 角分），双筒可轻松同框"""
    data = calculate_mars_praesepe_postmidnight()
    sep = data["separation"]

    assert sep["arcmin"] < 50.0
    assert sep["deg"] < 0.85
    # 木星在凌晨 03:00 仰角已升起 (>15°)
    assert data["city_altitudes_0300"]["Beijing"]["Jupiter_alt"] > 15.0


def test_full_relay_report_structure():
    """断言 6：全套通宵接力综合报告字段完整无缺失"""
    report = generate_full_relay_report()
    assert "stage1_twilight_trio_mercury" in report
    assert "overnight_darkness_window" in report
    assert "midnight_deepsky_and_vesta" in report
    assert "postmidnight_mars_m44_and_jupiter" in report
    assert report["vesta_opposition_exact_cst"] == "2026-10-13 06:40:00 CST"
