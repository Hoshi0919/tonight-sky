import sys
from pathlib import Path
import pytest

scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from sun_moon_coexistence import analyze_coexistence

def test_coexistence_2026_mid_autumn():
    data = analyze_coexistence("2026-09-25", "31.2304", "121.4737")
    assert data["date"] == "2026-09-25"
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
