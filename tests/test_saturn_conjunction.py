import sys
from pathlib import Path
import pytest

scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from saturn_opposition_conjunction import compute_tonight_conjunction, compute_saturn_opposition


def test_saturn_conjunction_timing():
    data = compute_tonight_conjunction("2026-09-27")
    timing = data["timing"]
    
    # Moon and Saturn rise within 20 minutes of each other
    assert "17:52" in timing["moon_rise"]
    assert "18:09" in timing["saturn_rise"]
    
    # Transit within 10 minutes near midnight
    assert "00:16" in timing["saturn_transit"]
    assert "00:25" in timing["moon_transit"]
    
    # Both set at dawn
    assert "06:22" in timing["saturn_set"]
    assert "07:07" in timing["moon_set"]


def test_saturn_conjunction_separation():
    data = compute_tonight_conjunction("2026-09-27")
    min_sep = data["min_separation"]
    
    # Shanghai topocentric closest approach occurs in afternoon (below horizon) around 5.45 deg
    assert 5.4 <= min_sep["topocentric_deg"] <= 5.5
    assert "14:5" in min_sep["topocentric_time"]
    
    # Geocentric minimum separation ~6.19 deg
    assert 6.1 <= min_geo <= 6.3 if (min_geo := min_sep["geocentric_deg"]) else False
    
    # Track check: separation expands from ~5.9 deg to ~10.0 deg across the night
    track = data["hourly_track"]
    assert len(track) == 13
    assert track[0]["hour"] == "18:00"
    assert 5.8 <= track[0]["separation_deg"] <= 6.0
    assert track[-1]["hour"] == "06:00"
    assert 9.9 <= track[-1]["separation_deg"] <= 10.2


def test_saturn_opposition_2026():
    opp = compute_saturn_opposition(2026)
    
    # Opposition date in CST: 2026-10-04 around 20:14
    assert "2026-10-04" in opp["opposition_time_cst"]
    assert "20:14" in opp["opposition_time_cst"]
    
    # Perigee date within hours of opposition
    assert "2026-10-04" in opp["perigee_time_cst"]
    assert 8.43 <= opp["min_distance_au"] <= 8.44
    assert 1260000000 <= opp["min_distance_km"] <= 1265000000
    
    # Magnitude ~0.3, angular size ~19.6 arcsec
    assert 0.25 <= opp["magnitude_at_opposition"] <= 0.40
    assert 19.0 <= opp["angular_size_arcsec"] <= 20.5
