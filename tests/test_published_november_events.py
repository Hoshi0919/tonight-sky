"""test_published_november_events.py — 外部公开天文年历 (Sea and Sky) 锚点回归

与常规推演断言不同：本测试的期望值来自外部第三方天文年历公开数据
(Sea and Sky Astronomy Calendar 2026)。
用于严格验证 tonight-sky 算出的 11 月核心天象与国际天文界公开发布的数据一致。
"""

import sys
from pathlib import Path
import pytest

DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR / "scripts"))

ephem = pytest.importorskip("ephem", reason="需要 ephem，uv run --with ephem pytest")

import verify_seasky_november as vsn


@pytest.fixture(scope="module")
def november_audit():
    return vsn.check_november_events()


def test_new_moon_matches_seasky(november_audit):
    """朔月时刻与年历相差不到 1 分钟"""
    nm = november_audit["new_moon"]
    assert nm["pass"] is True
    assert nm["error_s"] < 60.0


def test_full_moon_supermoon_matches_seasky(november_audit):
    """望月与年历相差在舍入容差内，且确认为年度近地点超级大满月"""
    fm = november_audit["full_moon_supermoon"]
    assert fm["pass"] is True
    assert fm["error_s"] < 120.0
    assert fm["is_supermoon_confirmed"] is True
    assert fm["perigee_distance_km"] < 360000


def test_mercury_elongation_matches_seasky(november_audit):
    """水星西大距日距角与年历 19.6° 误差 < 0.05°，UTC 发生日期严格对齐 11-20"""
    me = november_audit["mercury_elongation"]
    assert me["pass"] is True
    assert me["elongation_diff_deg"] < 0.05
    assert me["peak_date_utc"] == "2026-11-20"


def test_uranus_opposition_matches_seasky(november_audit):
    """天王星冲日 UTC 发生日期严格对齐 11-25"""
    uo = november_audit["uranus_opposition"]
    assert uo["pass"] is True
    assert uo["opposition_date_utc"] == "2026-11-25"


def test_all_november_events_pass(november_audit):
    """全项外部对照综合断言"""
    for event_name, res in november_audit.items():
        assert res["pass"] is True, f"Event {event_name} failed external anchor verification"
