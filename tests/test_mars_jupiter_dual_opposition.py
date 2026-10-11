"""
test_mars_jupiter_dual_opposition.py
====================================
单元测试集：2027 年火星与木星双冲日、双星同向逆行、
荧惑三犯轩辕十四与元宵双星捧月天体力学推演引擎。
"""

import pytest
import os
import sys

# 将 scripts 加入 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))

from mars_jupiter_dual_opposition_2027 import (
    calculate_oppositions,
    calculate_retrograde_loops,
    calculate_mars_regulus_triple_pass,
    calculate_lantern_festival_quadrangle,
    calculate_china_observability,
    build_full_report,
    format_markdown_summary,
)


def test_oppositions_calculation():
    """验证 2027 年木星与火星冲日时空参量与时间差。"""
    opp = calculate_oppositions()
    
    # 木星冲日断言
    jup = opp["jupiter_opposition"]
    assert "2027-02-11" in jup["ecliptic_time_cst"]
    assert jup["apparent_magnitude"] <= -2.35
    assert jup["angular_diameter_arcsec"] >= 44.5
    assert 4.30 <= jup["earth_distance_au"] <= 4.45
    assert 35.0 <= jup["light_time_minutes"] <= 38.0

    # 火星冲日断言
    mars = opp["mars_opposition"]
    assert "2027-02-19" in mars["ecliptic_time_cst"] or "2027-02-20" in mars["ecliptic_time_cst"]
    assert mars["apparent_magnitude"] <= -1.05
    assert mars["angular_diameter_arcsec"] >= 13.5
    assert 0.65 <= mars["earth_distance_au"] <= 0.70
    assert 5.0 <= mars["light_time_minutes"] <= 6.0

    # 火星近地点断言
    perigee = opp["mars_closest_approach"]
    assert "2027-02-20" in perigee["time_cst"]
    assert perigee["min_distance_au"] <= mars["earth_distance_au"]

    # 双冲日极窄时间间隔断言（必须在 10 天以内）
    gap = opp["cluster_interval"]
    assert gap["ecliptic_gap_days"] < 10.0
    assert gap["is_tight_cluster"] is True


def test_retrograde_loops_and_overlap():
    """验证双星逆行留点、持续天数与同步重叠窗口。"""
    ret = calculate_retrograde_loops()
    
    # 木星逆行
    jup_ret = ret["jupiter_retrograde"]
    assert "2026-12-13" in jup_ret["first_stationary_point"]["time_cst"]
    assert "2027-04-13" in jup_ret["second_stationary_point"]["time_cst"]
    assert 118.0 <= jup_ret["retrograde_duration_days"] <= 123.0

    # 火星逆行
    mars_ret = ret["mars_retrograde"]
    assert "2027-01-12" in mars_ret["first_stationary_point"]["time_cst"]
    assert "2027-04-03" in mars_ret["second_stationary_point"]["time_cst"]
    assert 78.0 <= mars_ret["retrograde_duration_days"] <= 83.0

    # 同步逆行重叠期
    overlap = ret["synchronous_overlap"]
    assert "2027-01-12" in overlap["start_cst"]
    assert "2027-04-03" in overlap["end_cst"]
    assert 78.0 <= overlap["duration_days"] <= 83.0


def test_mars_regulus_triple_pass():
    """验证荧惑三犯轩辕十四的三幕交会角距与时序。"""
    passes = calculate_mars_regulus_triple_pass()
    assert len(passes) == 3

    # 初犯：2026 年底顺行东进
    p1 = passes[0]
    assert "2026-11-26" in p1["time_cst"]
    assert p1["min_separation_deg"] < 2.0
    assert p1["min_separation_arcmin"] < 120.0

    # 二犯：2027 年 2 月逆行西退（正值火星冲日时分）
    p2 = passes[1]
    assert "2027-02-21" in p2["time_cst"]
    assert p2["min_separation_deg"] < 4.5
    assert p2["mars_magnitude"] <= -1.0

    # 三犯：2027 年 5 月恢复顺行再追越
    p3 = passes[2]
    assert "2027-05-15" in p3["time_cst"]
    assert p3["min_separation_deg"] < 1.5


def test_lantern_festival_quadrangle():
    """验证 2027 元宵节（丁未年正月十五）满月与四曜汇聚几何。"""
    lan = calculate_lantern_festival_quadrangle()
    
    assert lan["date_info"]["gregorian_date"] == "2027-02-20"
    assert "正月十五" in lan["date_info"]["lunar_date"]
    assert lan["date_info"]["moon_phase_pct"] >= 99.0

    seps = lan["celestial_separations"]
    assert seps["moon_to_jupiter_evening_deg"] < 10.0
    assert seps["moon_to_mars_evening_deg"] < 10.0
    assert 8.0 <= seps["mars_to_jupiter_deg"] <= 12.0

    # 上海站子夜中天时序：木星 -> 满月 -> 火星，在 60 分钟内完成
    seq = lan["shanghai_midnight_transit_sequence"]
    assert seq["total_span_minutes"] < 60.0
    assert seq["jupiter_altitude_deg"] > 70.0
    assert seq["moon_altitude_deg"] > 65.0
    assert seq["mars_altitude_deg"] > 70.0


def test_china_observability():
    """验证华夏主要城市通宵地平几何与高天顶仰角。"""
    c_obs = calculate_china_observability()
    assert len(c_obs) == 5

    for city in ["Beijing", "Shanghai", "Guangzhou", "Chengdu", "Urumqi"]:
        assert city in c_obs
        info = c_obs[city]
        assert info["jupiter"]["transit_alt_deg"] >= 60.0
        assert info["mars"]["transit_alt_deg"] >= 60.0

    # 广州作为南方枢纽，仰角直插天顶
    assert c_obs["Guangzhou"]["mars"]["transit_alt_deg"] >= 82.0
    assert c_obs["Guangzhou"]["mars"]["zenith_airmass"] < 1.02


def test_full_report_and_summary():
    """验证全量报告生成与 Markdown 格式化输出。"""
    report = build_full_report()
    assert "oppositions" in report
    assert "retrograde_loops" in report
    assert "mars_regulus_triple_pass" in report
    assert "lantern_festival_quadrangle" in report
    assert "china_observability" in report

    summary = format_markdown_summary(report)
    assert "# 2027 年火木双冲日与元宵双星捧月天体力学推演报告" in summary
    assert "8.64 天" in summary
    assert "荧惑三犯轩辕十四" in summary
    assert "丁未年元宵夜“双星捧月”" in summary
