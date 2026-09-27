import sys
from pathlib import Path
import pytest

scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from sun_moon_coexistence import analyze_coexistence, analyze_evening_coexistence, analyze_morning_coexistence

def test_coexistence_2026_mid_autumn():
    data = analyze_coexistence("2026-09-25", "31.2304", "121.4737")
    assert data["date"] == "2026-09-25"
    assert data["mode"] == "evening"
    assert "16:53" in data["moonrise_cst"]
    assert "17:47" in data["sunset_cst"]
    assert 53.0 <= data["coexistence_duration_minutes"] <= 55.0
    
    # Check timeline properties
    coexisting_points = [p for p in data["timeline"] if p["is_coexisting"]]
    assert len(coexisting_points) >= 10
    
    # Check angular separation ~164 degrees
    for p in coexisting_points:
        assert 160.0 <= p["angular_separation_deg"] <= 170.0
        assert p["moon_phase_pct"] > 97.0

def test_coexistence_midpoint_balance():
    data = analyze_coexistence("2026-09-25", "31.2304", "121.4737")
    # Around 17:23, both Sun and Moon should be between 3 and 7 degrees altitude
    mid_points = [p for p in data["timeline"] if "17:20" <= p["time_cst"] <= "17:25"]
    assert len(mid_points) > 0
    p = mid_points[0]
    assert 3.0 <= p["sun_alt"] <= 6.0
    assert 4.0 <= p["moon_alt"] <= 7.0

def test_morning_coexistence_2026_09_28():
    data = analyze_morning_coexistence("2026-09-28", "31.2304", "121.4737")
    assert data["date"] == "2026-09-28"
    assert data["mode"] == "morning"
    assert "05:45" in data["sunrise_cst"]
    assert "07:07" in data["moonset_cst"]
    assert "06:22" in data["saturn_set_cst"]
    assert 80.0 <= data["coexistence_duration_minutes"] <= 83.0
    
    eq = data["equilibrium_point"]
    assert "06:25" in eq["time_cst"]
    assert 7.0 <= eq["sun_alt"] <= 8.5
    assert 7.0 <= eq["moon_alt"] <= 8.5
    assert 163.0 <= eq["angular_separation_deg"] <= 166.0
    assert eq["moon_phase_pct"] >= 97.5
    
    # Check triple coexistence (Sun, Moon, Saturn)
    triple_points = [p for p in data["timeline"] if p.get("is_triple_coexisting")]
    assert len(triple_points) >= 5
    
    # Check timeline duration
    coexisting = [p for p in data["timeline"] if p["is_coexisting"]]
    assert len(coexisting) >= 15

def test_coexistence_mode_dispatch():
    eve = analyze_coexistence("2026-09-25", mode="auto")
    assert eve["mode"] == "evening"
    
    mor = analyze_coexistence("2026-09-28", mode="auto")
    assert mor["mode"] == "morning"
