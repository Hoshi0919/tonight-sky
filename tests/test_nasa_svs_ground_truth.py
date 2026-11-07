"""
test_nasa_svs_ground_truth.py — NASA SVS 2026 月球星历全域真实真值对表

数据源：NASA Scientific Visualization Studio (SVS) Dial-A-Moon 2026 (ID: 5587)
涵盖 2026 年全年 8,760 个整点小时官方测算的月相、地月距离、视直径、赤经赤纬、天平动与日面经纬度。
本测试直接回答：本地天体力学算法是否能与 NASA 官方公布的真实星历实现严密精确对表？
"""

import sys
import datetime
from pathlib import Path
import pytest

DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR / "scripts"))

ephem = pytest.importorskip("ephem", reason="需要 ephem，uv run --with ephem pytest")

import nasa_svs_ground_truth_validator as val


@pytest.fixture(scope="module")
def full_year_eval():
    """Sample every 12 hours (730 points) for fast CI, while preserving tight error envelopes."""
    return val.evaluate_hourly(step=12)


def test_nasa_svs_file_integrity():
    data = val.load_nasa_svs_data()
    assert len(data) == 8760, f"Expected 8760 hourly records for 2026, got {len(data)}"
    first = data[0]
    required_keys = ["time", "phase", "age", "diameter", "distance", "j2000", "subsolar", "subearth", "posangle"]
    for k in required_keys:
        assert k in first, f"Missing required key: {k}"


def test_phase_error_bounds(full_year_eval):
    phase = full_year_eval["phase"]
    # Mean phase error should be strictly under 0.01%
    assert phase["mean"] < 0.01, f"Mean phase error {phase['mean']:.4f}% exceeded 0.01%"
    # Max phase error across the entire year should be under 0.025%
    assert phase["max"] < 0.025, f"Max phase error {phase['max']:.4f}% exceeded 0.025%"


def test_distance_error_bounds(full_year_eval):
    dist = full_year_eval["distance_km"]
    # Mean distance error under 30 km (relative error < 8e-5)
    assert dist["mean"] < 30.0, f"Mean distance error {dist['mean']:.2f} km exceeded 30 km"
    # Max distance error under 50 km
    assert dist["max"] < 50.0, f"Max distance error {dist['max']:.2f} km exceeded 50 km"


def test_diameter_error_bounds(full_year_eval):
    diam = full_year_eval["diameter_arcsec"]
    # Mean diameter error under 3.0 arcseconds (< 0.16% of total diameter)
    assert diam["mean"] < 3.0, f"Mean diameter error {diam['mean']:.2f}\" exceeded 3.0\""
    assert diam["max"] < 3.5, f"Max diameter error {diam['max']:.2f}\" exceeded 3.5\""


def test_dec_error_bounds(full_year_eval):
    dec = full_year_eval["dec_arcmin"]
    # Declination error strictly under 10 arcminutes across 2026
    assert dec["max"] < 10.0, f"Max Dec error {dec['max']:.2f}' exceeded 10 arcmin"


def test_today_2026_11_08_anchor():
    """Verify today's Nov 8 14:00 UT (22:00 CST) against NASA SVS."""
    dt = datetime.datetime(2026, 11, 8, 14, 0)
    res = val.query_at_time(dt)
    assert res["nasa"]["phase"] == 0.68
    assert res["discrepancy"]["phase_pct"] < 0.01
    assert res["discrepancy"]["distance_km"] < 40.0


def test_hunters_supermoon_anchor():
    """Verify 2026-10-26 04:00 UT (Super Hunter's Full Moon) against NASA SVS."""
    dt = datetime.datetime(2026, 10, 26, 4, 0)
    res = val.query_at_time(dt)
    # Peak full moon on 2026-10-26 reaches 99.84% (non-eclipse inclination geometry)
    assert res["nasa"]["phase"] == 99.84
    assert res["discrepancy"]["phase_pct"] < 0.01
    assert res["discrepancy"]["distance_km"] < 35.0
