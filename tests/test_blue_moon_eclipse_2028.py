"""
test_blue_moon_eclipse_2028.py
==============================
单元测试集：2028-12-31 跨年夜蓝月全食天体力学推演、
沙罗 134 序列、华夏全境天顶仰角与冬季大六角星空穹顶突变。
"""

import sys
import os
from pathlib import Path
import pytest

# 将 scripts 加入 Python 路径
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from blue_moon_eclipse_2028_engine import (
    compute_blue_moon_metrics,
    compute_eclipse_contacts,
    compute_china_observability,
    compute_deep_sky_contrast,
    compute_danjon_and_atmospheric_scattering,
    build_full_report,
    format_markdown_summary,
    SAROS_134_CATALOG,
)


def test_blue_moon_metrics():
    """验证 2028 年 12 月双满月历法参量与蓝月判定。"""
    metrics = compute_blue_moon_metrics()

    assert metrics["is_calendar_blue_moon"] is True
    assert "2028-12-02" in metrics["first_full_moon_cst"]
    assert "2029-01-01" in metrics["second_full_moon_cst"]
    # 实际朔望月因地球近日点开普勒第二定律在 29.27 ~ 29.83 天之间变动
    assert 29.50 <= metrics["synodic_span_days"] <= 29.70
    assert metrics["calendar_month"] == "2028-12"
    assert "2018-01-31" in metrics["last_blue_moon_total_eclipse"]


def test_eclipse_contacts_and_midnight():
    """验证月食关键接触点时刻、跨年夜倒计时本影咬蚀度与持续时间。"""
    res = compute_eclipse_contacts()
    contacts = res["contacts"]
    dur = res["durations"]
    mid_obs = res["midnight_obscuration"]

    # 接触时刻断言 (CST)
    assert "2028-12-31 22:02:00" in contacts["P1_penumbral_ingress"]
    assert "2028-12-31 23:07:00" in contacts["U1_umbral_ingress"]
    assert "2029-01-01 00:16:00" in contacts["U2_totality_begins"]
    assert "2029-01-01 00:53:00" in contacts["Greatest_Eclipse_mid"]
    assert "2029-01-01 01:29:00" in contacts["U3_totality_ends"]
    assert "2029-01-01 02:37:00" in contacts["U4_umbral_egress"]
    assert "2029-01-01 03:42:00" in contacts["P4_penumbral_egress"]

    # 跨年零点本影遮挡率在 78% ~ 80% 之间
    assert 78.0 <= mid_obs["lunar_diameter_obscured_percent"] <= 80.0

    # 全食时长 73 分钟，偏食总时长 210 分钟
    assert dur["totality_duration_minutes"] == 73.0
    assert dur["umbral_duration_minutes"] == 210.0
    assert dur["penumbral_duration_minutes"] == 340.0


def test_magnitudes_and_separation():
    """验证本影与半影食分及最小角距。"""
    res = compute_eclipse_contacts()
    mags = res["magnitudes"]

    # 本影食分 > 1.250，属于较深的全食
    assert 1.250 <= mags["umbral_magnitude"] <= 1.260
    # 半影食分 > 2.25
    assert 2.25 <= mags["penumbral_magnitude"] <= 2.35
    # 最小角偏距约 19 角分
    assert 18.5 <= mags["minimum_separation_arcmin"] <= 19.5


def test_china_observability_zenith_altitudes():
    """验证食甚时华夏各大城市高仰角（全境 > 62°，广州与三亚几近天顶 > 84°）。"""
    cities = compute_china_observability()

    for city_key, data in cities.items():
        assert data["altitude_deg"] > 62.0
        assert data["airmass"] <= 1.15

    # 低纬度近天顶断言
    assert cities["Guangzhou"]["altitude_deg"] >= 84.5
    assert cities["Sanya"]["altitude_deg"] >= 84.5
    assert cities["Chengdu"]["altitude_deg"] >= 81.5
    assert cities["Shanghai"]["altitude_deg"] >= 75.0
    assert cities["Beijing"]["altitude_deg"] >= 71.0


def test_deep_sky_contrast_and_flux_attenuation():
    """验证月球赤纬极值、与 M35 等天体角距及光通量骤降。"""
    deep_sky = compute_deep_sky_contrast()

    # 月球赤纬高挂 +23°
    assert deep_sky["moon_equatorial"]["dec_degrees"] > 23.0
    assert deep_sky["moon_equatorial"]["constellation"] == "Gemini (双子座)"

    # 与双子座 M35 疏散星团角距 < 9°
    assert deep_sky["surrounding_targets"]["M35"]["angular_distance_deg"] < 9.0
    assert deep_sky["surrounding_targets"]["Castor"]["angular_distance_deg"] < 15.0
    assert deep_sky["surrounding_targets"]["Pollux"]["angular_distance_deg"] < 15.0

    # 光通量衰减比 > 500,000 倍
    assert deep_sky["photometric_collapse"]["flux_attenuation_ratio"] > 500000


def test_saros_catalog_and_report_generation():
    """验证沙罗 134 历史名录与完整报告生成。"""
    report = build_full_report()
    summary = format_markdown_summary(report)

    assert "Lunar Saros 134" in report["saros_series"]
    assert len(report["saros_catalog"]) == 5
    assert any("2010-12-21" in item["date"] for item in report["saros_catalog"])

    # Markdown 摘要包含核心关键词
    assert "跨年夜超级蓝月全食" in summary
    assert "00:00 CST (01-01)" in summary
    assert "广州" in summary
    assert "M35" in summary
