import sys
from pathlib import Path
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import october_2026_guide as og

def test_moon_pleiades_approach():
    data = og.calculate_moon_pleiades()
    assert "Alcyone" in data["target_star"]
    assert 0.5 < data["min_separation_deg"] < 1.5
    assert "2026-10-01" in data["time_cst"] or "2026-09-30" in data["time_cst"]
    assert data["star_alt_deg"] > 30.0

def test_saturn_opposition():
    data = og.calculate_saturn_opposition()
    assert "2026-10-04" in data["opposition_time_cst"]
    assert 8.4 < data["distance_au"] < 8.5
    assert 0.2 < data["magnitude"] < 0.4
    assert data["ring_tilt_deg"] == -7.5

def test_planet_conjunctions():
    conjs = og.calculate_moon_planet_conjunctions()
    assert len(conjs) == 2
    mars_c = conjs[0]
    jup_c = conjs[1]
    
    assert "火星" in mars_c["event"]
    assert mars_c["separation_deg"] < 6.0
    assert "2026-10-05" in mars_c["time_cst"]
    
    assert "木星" in jup_c["event"]
    assert jup_c["separation_deg"] < 8.0
    assert "2026-10-06" in jup_c["time_cst"]

def test_lunar_cycle_october():
    lc = og.calculate_october_lunar_cycle()
    nm = lc["new_moon"]
    fm = lc["full_moon"]
    
    assert "2026-10-10" in nm["time_cst"]
    assert "2026-10-26" in fm["time_cst"]
    assert fm["distance_km"] < 370000  # 近地满月
    assert fm["is_supermoon"] is True

def test_meteor_showers():
    ms = og.calculate_meteor_showers()
    assert len(ms) == 2
    drac = ms[0]
    ori = ms[1]
    
    assert drac["moon_phase_pct"] < 10.0  # 理想暗夜
    assert ori["moon_phase_pct"] > 70.0   # 月光干扰
