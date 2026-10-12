import pytest
import math
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from saros136_century_eclipse_2027 import (
    compute_saros_harmonics,
    compute_luxor_greatest_eclipse,
    compute_international_stations,
    compute_china_western_stations,
    SAROS_136_CATALOG,
)


def test_saros_harmonics():
    hm = compute_saros_harmonics()
    # 223 synodic months ~ 6585.32 days
    assert 6585.0 < hm["synodic_period_days"] < 6586.0
    # Difference to 242 draconic months < 2 hours
    assert abs(hm["draconic_diff_hours"]) < 2.0
    # Difference to 239 anomalistic months < 8 hours
    assert abs(hm["anomalistic_diff_hours"]) < 8.0
    # Fractional day extra hours ~ 7.7 hours
    assert 7.0 < hm["saros_extra_hours"] < 8.5
    # Westward longitude shift ~ 115° to 120°
    assert 110.0 < hm["longitude_shift_west_deg"] < 125.0
    # Exeligmos period ~ 54.1 years
    assert 53.5 < hm["exeligmos_years"] < 54.5


def test_luxor_greatest_eclipse_contacts():
    ge = compute_luxor_greatest_eclipse()
    
    # Check contact chronology
    contacts = ge["contacts"]
    assert "08:" in contacts["C1_first_contact"]["utc"]
    assert "10:01" in contacts["C2_totality_begins"]["utc"] or "10:02" in contacts["C2_totality_begins"]["utc"]
    assert "10:08" in contacts["C3_totality_ends"]["utc"] or "10:09" in contacts["C3_totality_ends"]["utc"]
    assert "11:" in contacts["C4_fourth_contact"]["utc"]
    
    # Check totality duration > 6 minutes (360 seconds) and <= 7 minutes
    dur = ge["totality_duration_seconds"]
    assert 360.0 <= dur <= 420.0
    
    # Check altitude near zenith (> 80.0°)
    assert ge["sun_altitude_deg"] > 80.0
    
    # Check airmass is nearly 1.0 (negligible extinction)
    assert 1.00 <= ge["airmass"] <= 1.03
    
    # Check magnitude (Moon diameter / Sun diameter) > 1.07
    assert 1.065 < ge["eclipse_magnitude"] < 1.095
    assert ge["moon_topocentric_diameter_arcsec"] > ge["sun_diameter_arcsec"]


def test_international_totality_corridor():
    stations = compute_international_stations()
    assert len(stations) >= 8
    
    station_map = {s["key"]: s for s in stations}
    
    # Verify key stations have totality
    for key in ["Tarifa", "Tangier", "Oran", "Sfax", "Benghazi", "Luxor", "Jeddah", "Bossaso"]:
        assert station_map[key]["is_total"] is True
        assert station_map[key]["totality_duration_seconds"] >= 180  # At least 3 minutes
        
    # Luxor should have the longest duration in the corridor
    assert station_map["Luxor"]["totality_duration_seconds"] >= station_map["Tarifa"]["totality_duration_seconds"]
    assert station_map["Luxor"]["totality_duration_seconds"] >= station_map["Tangier"]["totality_duration_seconds"]
    
    # Altitude peak near Luxor
    assert station_map["Luxor"]["sun_altitude_deg"] > 80.0
    assert station_map["Tarifa"]["sun_altitude_deg"] < 45.0


def test_china_western_border_partial_eclipse():
    china = compute_china_western_stations()
    china_map = {s["key"]: s for s in china}
    
    # Taxkorgan (Xinjiang) and Ali (Tibet) must have visible sunset partial eclipse
    assert china_map["Taxkorgan"]["visible"] is True
    assert china_map["Ali"]["visible"] is True
    
    # Check magnitudes
    assert 0.03 <= china_map["Taxkorgan"]["max_magnitude"] <= 0.06
    assert 0.04 <= china_map["Ali"]["max_magnitude"] <= 0.08
    
    # Check solar altitude during eclipse is comfortably above horizon (> 25°)
    assert china_map["Taxkorgan"]["sun_altitude_at_max_deg"] > 30.0
    assert china_map["Ali"]["sun_altitude_at_max_deg"] > 25.0
    
    # Eclipse timing in evening CST (18:00 - 19:30 CST)
    assert "18:" in china_map["Ali"]["start_time_cst"]
    assert "18:" in china_map["Taxkorgan"]["start_time_cst"]


def test_saros_136_historical_catalog():
    assert len(SAROS_136_CATALOG) >= 8
    nums = [e["saros_num"] for e in SAROS_136_CATALOG]
    assert 32 in nums  # 1919 Eddington
    assert 35 in nums  # 1973 Concorde
    assert 37 in nums  # 2009 Yangtze River
    assert 38 in nums  # 2027 Luxor
    assert 39 in nums  # 2045 USA
    
    # Find 2027 entry
    e2027 = next(e for e in SAROS_136_CATALOG if e["saros_num"] == 38)
    assert e2027["date"] == "2027-08-02"
    assert "埃及" in e2027["location"] or "卢克索" in e2027["location"]
