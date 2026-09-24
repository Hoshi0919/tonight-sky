import sys
from pathlib import Path
import pytest

# 将 scripts 目录加入 sys.path
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from mid_autumn_moon_mechanics import (
    get_mid_autumn_full_moon,
    analyze_century_distribution,
    format_report_2026,
)


def test_2026_mid_autumn_mechanics():
    info = get_mid_autumn_full_moon(2026)
    assert info["year"] == 2026
    assert info["mid_autumn_solar"] == "2026-09-25"
    assert info["lunar_day"] == 17
    assert info["lunar_desc"] == "八月17"
    assert "2026-09-27 00:48" in info["full_moon_cst"]
    assert 15.5 < info["duration_days"] < 15.6
    assert info["duration_hours"] > 370.0
    # 远地点距离应该大于 40 万公里
    assert info["apogee_near"]["distance_km"] > 405000.0


def test_2023_mid_autumn_mechanics():
    # 2023 年中秋是 2023-09-29，当年满月在 09-29（八月十五）
    info = get_mid_autumn_full_moon(2023)
    assert info["year"] == 2023
    assert info["mid_autumn_solar"] == "2023-09-29"
    assert info["lunar_day"] == 15
    assert info["lunar_desc"] == "八月15"


def test_century_distribution():
    # 抽取 2000-2030 (31年) 验证分布和无异常
    res = analyze_century_distribution(2000, 2030)
    assert res["total_years"] == 31
    assert "八月15" in res["counts"]
    assert "八月16" in res["counts"]
    assert "八月17" in res["counts"]
    # 不应该存在八月十四
    assert "八月14" not in res["counts"]
    # 持续时间应该在合理的天文学物理边界内
    assert res["min_duration"]["days"] > 13.5
    assert res["max_duration"]["days"] < 16.0


def test_format_report_2026():
    report = format_report_2026()
    assert "2026 年中秋月相天体力学" in report
    assert "十五的月亮十七圆" in report
    assert "开普勒第二定律" in report
