import sys
from pathlib import Path
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import dawn_trio_gathering_engine as dtge


def test_calculate_gathering_ephemeris_shanghai():
    res = dtge.calculate_gathering_ephemeris(city_key="Shanghai")
    assert res["city"] == "上海"
    assert "2026-11-03 05:59" in res["conjunction_time_cst"]
    assert 0.68 < res["min_separation_moon_jupiter_deg"] < 0.71
    assert 40.5 < res["min_separation_moon_jupiter_arcmin"] < 42.5
    assert 4.9 < res["separation_moon_mars_deg"] < 5.2
    assert 4.9 < res["separation_jupiter_mars_deg"] < 5.2
    assert res["trio_maximum_span_deg"] < 5.2
    assert res["binocular_fov_fit"] is True
    assert 37.0 < res["moon_phase_pct"] < 40.0
    assert res["moon_altitude_deg"] > 65.0
    assert res["jupiter_altitude_deg"] > 65.0
    assert res["jupiter_magnitude"] < -1.80
    assert res["mars_altitude_deg"] > 70.0
    assert res["mars_magnitude"] < 1.00
    assert "05:45" in res["twilight_schedule_cst"]["civil_dawn"]
    assert "06:10" in res["twilight_schedule_cst"]["sunrise"]


def test_topocentric_parallax_gradient():
    summary = dtge.calculate_all_cities_summary()
    cities = summary["cities"]

    gz_sep = cities["Guangzhou"]["min_separation_moon_jupiter_deg"]
    sh_sep = cities["Shanghai"]["min_separation_moon_jupiter_deg"]
    bj_sep = cities["Beijing"]["min_separation_moon_jupiter_deg"]
    hrb_sep = cities["Harbin"]["min_separation_moon_jupiter_deg"]

    # 视差单调性：纬度越高，月球视差向下位移越大，导致北向观测者与木星角距变大
    assert gz_sep < sh_sep < bj_sep < hrb_sep
    assert 0.49 < gz_sep < 0.53   # 广州近乎擦边掠掩 (~30.6')
    assert 0.90 < hrb_sep < 0.95  # 哈尔滨角距近 1 度 (~55.8')


def test_binocular_envelope_all_cities():
    summary = dtge.calculate_all_cities_summary()
    for name, c in summary["cities"].items():
        assert c["binocular_fov_fit"] is True
        assert c["trio_maximum_span_deg"] <= 5.5
        assert c["jupiter_magnitude"] < -1.8
        assert c["mars_magnitude"] < 1.0


def test_high_altitude_and_airmass():
    sh = dtge.calculate_gathering_ephemeris(city_key="Shanghai")
    alt = sh["moon_altitude_deg"]
    am = dtge.airmass(alt)
    # 高仰角 (>65°) 对应气团数极低 (< 1.15)
    assert alt > 65.0
    assert 1.0 < am < 1.15
