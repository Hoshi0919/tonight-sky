import sys
from pathlib import Path
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import november_2026_guide as ng

def test_lunar_cycle_november():
    lc = ng.calculate_november_lunar_cycle()
    lq = lc["last_quarter"]
    nm = lc["new_moon"]
    fq = lc["first_quarter"]
    fm = lc["full_moon"]
    
    assert "2026-11-02" in lq["time_cst"]
    assert "2026-11-09" in nm["time_cst"]
    assert "2026-11-17" in fq["time_cst"]
    assert "2026-11-24" in fm["time_cst"]
    
    # 望月距地与近地点
    assert 355000 < fm["distance_km"] < 365000
    assert fm["is_supermoon"] is True
    assert "2026-11-26" in fm["perigee_time_cst"]
    assert fm["perigee_distance_km"] < 355000
    assert fm["perigee_fullmoon_diff_hours"] < 30.0

def test_dawn_trio_gathering():
    dt = ng.calculate_dawn_trio_gathering()
    assert "2026-11-03" in dt["peak_time_cst"]
    assert dt["min_separation_moon_jupiter_deg"] < 0.8  # 极近合相 (<48角分)
    assert dt["moon_alt_deg"] > 60.0                   # 晨空高仰角
    assert dt["jupiter_alt_deg"] > 60.0
    assert dt["mars_alt_deg"] > 65.0
    assert dt["jupiter_mag"] < -1.8                    # 木星璀璨
    assert dt["separation_mars_jupiter_deg"] < 6.0     # 火星与木星同框

def test_mercury_elongation():
    me = ng.calculate_mercury_elongation()
    assert "2026-11-21" in me["peak_time_cst"]
    assert 19.0 < me["max_elongation_deg"] < 20.5
    assert me["visual_magnitude"] < 0.0                # 亮于 0 等
    assert me["altitude_45min_before_sunrise_deg"] > 8.0

def test_pleiades_occultation():
    po = ng.calculate_pleiades_occultation()
    assert po["date"] == "2026-11-24"
    assert po["moon_phase_pct"] > 99.0
    
    # 上海数据验证
    sh_events = po["city_data"]["Shanghai"]["events"]
    star_map = {e["star"]: e for e in sh_events}
    assert star_map["Electra"]["is_occulted"] is True
    assert star_map["Maia"]["is_occulted"] is True
    assert star_map["Taygeta"]["is_occulted"] is True
    assert star_map["Maia"]["min_separation_deg"] < 0.01  # 中心掩食

    # 北京数据验证：包含 Alcyone (昴宿六) 掠掩
    bj_events = po["city_data"]["Beijing"]["events"]
    bj_map = {e["star"]: e for e in bj_events}
    assert bj_map["Alcyone"]["is_occulted"] is True

def test_uranus_opposition():
    uo = ng.calculate_uranus_opposition()
    assert "2026-11-26" in uo["opposition_time_cst"]
    assert 18.0 < uo["distance_au"] < 19.0
    assert 5.4 < uo["magnitude"] < 5.8
    assert "Taurus" in uo["constellation"]

def test_november_meteor_showers():
    ms = ng.calculate_november_meteor_showers()
    assert len(ms) == 3
    st, nt, leo = ms[0], ms[1], ms[2]
    
    assert "南金牛" in st["name"]
    assert "北金牛" in nt["name"]
    assert "狮子" in leo["name"]
    
    assert st["moon_phase_pct"] < 20.0
    assert nt["moon_phase_pct"] < 15.0
    assert leo["moon_alt_deg"] < 0.0  # 极盛后半夜月已落
