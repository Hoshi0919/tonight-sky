import sys
from pathlib import Path
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import space_station_zenith_pass_2026_11_04_engine as sse


def test_iss_zenith_pass_parameters():
    res = sse.calculate_iss_pass_shanghai()
    assert res["target"] == "ISS (ZARYA)"
    assert res["date_local"] == "2026-11-04"
    assert res["city"] == "上海"
    
    tca = res["tca"]
    assert "05:04:50" in tca["time_cst"]
    assert 85.0 < tca["max_alt_deg"] < 86.0
    assert 420.0 < tca["range_km"] < 435.0
    assert 1.000 < tca["airmass"] < 1.010
    assert tca["sun_alt_deg"] < -14.0
    assert tca["estimated_magnitude"] < -3.0
    assert res["duration_seconds"] >= 300


def test_iss_celestial_trio_co_visibility():
    res = sse.calculate_iss_pass_shanghai()
    trio = res["co_visible_celestial_trio"]
    
    moon = trio["moon"]
    assert 27.0 < moon["phase_pct"] < 30.0
    assert moon["alt_deg"] > 45.0
    assert 110.0 < moon["az_deg"] < 120.0
    
    jup = trio["jupiter"]
    assert jup["alt_deg"] > 55.0
    assert jup["magnitude"] < -1.80
    assert 115.0 < jup["az_deg"] < 125.0
    
    mars = trio["mars"]
    assert mars["alt_deg"] > 60.0
    assert mars["magnitude"] < 1.00
    assert 115.0 < mars["az_deg"] < 125.0


def test_css_evening_pass():
    res = sse.calculate_css_evening_pass_shanghai()
    assert res["target"] == "CSS (TIANHE)"
    assert res["city"] == "上海"
    
    tca = res["tca"]
    assert "18:00" in tca["time_cst"]
    assert 34.0 < tca["max_alt_deg"] < 37.0
    assert 600.0 < tca["range_km"] < 700.0
    assert tca["sun_alt_deg"] < -6.0


def test_space_rendezvous_anniversaries():
    ann = sse.get_space_rendezvous_anniversaries()
    assert ann["2011-11-03"]["years_elapsed"] == 15
    assert "神舟八号" in ann["2011-11-03"]["event"]
    assert "天宫一号" in ann["2011-11-03"]["event"]
    
    assert ann["2016-11-03"]["years_elapsed"] == 10
    assert "长征五号" in ann["2016-11-03"]["event"]
    
    assert ann["2022-11-03"]["years_elapsed"] == 4
    assert "梦天实验舱" in ann["2022-11-03"]["event"]
    
    assert ann["2024-11-04"]["years_elapsed"] == 2
    assert "神舟十八号" in ann["2024-11-04"]["event"]
    
    assert ann["1973-11-03"]["years_elapsed"] == 53
    assert "水手10号" in ann["1973-11-03"]["event"]
