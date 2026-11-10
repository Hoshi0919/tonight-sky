"""
水星凌日 (Mercury Transit) 7 周年交点共振与丢番图周期逼近自动化测试集
"""

import sys
from pathlib import Path
import pytest
from datetime import datetime, timezone

DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR / 'scripts'))

from mercury_transit_nodal_resonance_engine import MercuryTransitNodalResonanceEngine

@pytest.fixture
def engine():
    return MercuryTransitNodalResonanceEngine()

def test_orbital_resonance_diophantine(engine):
    data = engine.compute_orbital_resonance_diophantine()
    synodic = data["synodic_period_days"]
    ratio = data["period_ratio_PE_over_PM"]
    c7 = data["cycle_7yr"]
    c13 = data["cycle_13yr"]
    c46 = data["cycle_46yr"]

    # 验证水星会合周期 (~115.88天)
    assert 115.8 < synodic < 115.95
    # 验证地球年/水星年之比 (~4.1521)
    assert 4.150 < ratio < 4.155

    # 验证 7 年周期收敛
    assert c7["earth_years"] == 7
    assert c7["mercury_revolutions"] == 29
    assert c7["synodic_cycles"] == 22
    assert abs(c7["delta_days_vs_orbit"]) < 6.0
    assert c7["relative_error"] < 0.01 # < 1%

    # 验证 13 年周期收敛
    assert c13["earth_years"] == 13
    assert c13["mercury_revolutions"] == 54
    assert c13["synodic_cycles"] == 41
    assert abs(c13["delta_days_vs_orbit"]) < 2.5
    assert c13["relative_error"] < 0.002 # < 0.2%

    # 验证 46 年大周期高阶精确收敛
    assert c46["earth_years"] == 46
    assert c46["mercury_revolutions"] == 191
    assert c46["synodic_cycles"] == 145
    assert abs(c46["delta_days_vs_orbit"]) < 1.0
    assert c46["relative_error"] < 0.0001 # < 0.01%

def test_nodal_transit_geometry_and_asymmetry(engine):
    data = engine.compute_nodal_transit_geometry()
    nov = data["november_descending_node"]
    may = data["may_ascending_node"]
    freq_ratio = data["frequency_ratio_november_vs_may"]

    # 验证降交点 (11月) 靠近近日点，速度更快，视直径较小
    assert nov["mercury_sun_distance_au"] < 0.35
    assert nov["mercury_earth_distance_au"] > 0.65
    assert nov["orbital_speed_kms"] > 55.0 # ~56-59 km/s
    assert 9.0 < nov["mercury_apparent_diameter_arcsec"] < 11.0
    assert nov["typical_max_duration_hours"] <= 6.0

    # 验证升交点 (5月) 靠近远日点，速度更慢，视直径较大，历时更长
    assert may["mercury_sun_distance_au"] > 0.42
    assert may["mercury_earth_distance_au"] < 0.58
    assert may["orbital_speed_kms"] < 45.0 # ~40-42 km/s
    assert 11.5 < may["mercury_apparent_diameter_arcsec"] < 13.5
    assert may["typical_max_duration_hours"] >= 8.0

    # 验证 11 月与 5 月凌日频次比 ~2:1
    assert 1.9 < freq_ratio < 2.2

    # 验证微小遮光率 (十万分之二到三，~0.0025% - 0.0045%)
    assert 0.002 < nov["solar_flux_drop_percent"] < 0.005
    assert 0.003 < may["solar_flux_drop_percent"] < 0.006

def test_2019_transit_baseline_and_7yr_echo(engine):
    data = engine.compute_2019_transit_baseline_and_7yr_echo()
    base = data["transit_2019_11_11_observed"]
    anniv = data["seven_year_anniversary_2026"]

    # 验证 2019 实测历时 (~5.48 小时)
    assert 5.4 < base["duration_hours"] < 5.55
    assert abs(base["minimum_separation_arcsec"] - 75.9) < 0.5

    # 验证今日整 7 周年经历天数与水星公转圈数
    assert 2555.0 < anniv["exact_elapsed_days"] < 2558.0
    assert abs(anniv["exact_elapsed_earth_years"] - 7.0) < 0.02
    assert 29.0 < anniv["exact_mercury_orbits_completed"] < 29.2

    # 验证水星 2026-11-05 下合日后的晨曦展开
    assert anniv["days_since_inferior_conjunction"] == 6.0
    assert anniv["current_mercury_elongation_deg"] < -10.0
    assert anniv["upcoming_western_greatest_elongation"]["date"] == "2026-11-20"
    assert anniv["upcoming_western_greatest_elongation"]["elongation_deg"] == 19.5

def test_century_21_transits_catalog(engine):
    transits = engine.compute_century_21_transits_catalog()
    # 21 世纪共计 14 次水星凌日
    assert len(transits) == 14

    dates = [t["date"] for t in transits]
    assert "2003-05-07" in dates
    assert "2019-11-11" in dates
    assert "2032-11-13" in dates
    assert "2039-11-07" in dates
    assert "2049-05-07" in dates
    assert "2065-11-11" in dates
    assert "2098-11-10" in dates

    # 验证下一次水星凌日确为 2032-11-13 (距 2019 恰好 13 年)
    t_next = next(t for t in transits if t["date"] == "2032-11-13")
    assert "13 years" in t_next["interval_previous"]
    assert "Descending" in t_next["node"]
