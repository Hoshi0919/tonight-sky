import pytest
import math
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from vesta_opposition_engine import (
    calculate_vesta_opposition,
    calculate_ground_visibility,
    simulate_rotational_lightcurve,
    bowell_magnitude,
    VESTA_PHYSICAL,
)


def test_opposition_timing_and_geometry():
    opp = calculate_vesta_opposition()
    assert "2026-10-12" in opp["opposition_time_utc"] or "2026-10-13" in opp["opposition_time_utc"]
    assert "2026-10-13" in opp["opposition_time_cst"]
    
    # Check ecliptic longitude opposition condition: Delta lambda = 180°
    lon_diff = abs(opp["vesta_ecliptic_lon_deg"] - opp["sun_ecliptic_lon_deg"])
    assert abs(lon_diff - 180.0) < 0.1
    
    # Check position in Cetus
    assert "Cetus" in opp["constellation"]
    assert "1:30" in opp["ra_j2000"]
    assert "-3:20" in opp["dec_j2000"] or "-3:21" in opp["dec_j2000"] or "-3:22" in opp["dec_j2000"]


def test_distance_and_light_travel():
    opp = calculate_vesta_opposition()
    assert 2.40 < opp["sun_distance_au"] < 2.55
    assert 1.40 < opp["earth_distance_au"] < 1.55
    assert 2.1e8 < opp["earth_distance_km"] < 2.3e8
    assert 11.5 < opp["light_travel_time_min"] < 13.0


def test_bowell_magnitude_and_phase():
    opp = calculate_vesta_opposition()
    assert opp["phase_angle_deg"] < 5.5
    assert 6.30 <= opp["visual_magnitude"] <= 6.50
    
    # Test bowell_magnitude function consistency
    # At alpha = 0, V = H + 5*log10(r*Delta)
    h, g = 3.25, 0.32
    r, delta = 2.46, 1.48
    v_zero = bowell_magnitude(h, g, r, delta, 0.0)
    expected_v_zero = h + 5.0 * math.log10(r * delta)
    assert abs(v_zero - expected_v_zero) < 1e-4


def test_apparent_motion_dynamics():
    opp = calculate_vesta_opposition()
    # Retrograde motion in RA should be negative
    assert opp["motion_dra_arcsec_h"] < 0
    # Total motion between 30 and 45 arcsec/h
    assert 30.0 < opp["total_motion_arcsec_h"] < 45.0
    # Daily motion between 12 and 18 arcmin/day
    assert 12.0 < opp["daily_motion_arcmin_d"] < 18.0


def test_reference_star_hop():
    opp = calculate_vesta_opposition()
    ref = opp["reference_star"]
    assert ref["name"] == "Theta Ceti (天仓三)"
    # Angular separation < 5.0 deg (fits into 7x50 binocular FOV)
    assert ref["separation_deg"] < 5.0
    # Position angle should be NNE (10° to 30°)
    assert 10.0 <= ref["position_angle_deg"] <= 30.0


def test_ground_visibility_across_china():
    cities_vis = calculate_ground_visibility()
    assert len(cities_vis) == 5
    
    city_map = {c["city_key"]: c for c in cities_vis}
    
    # All cities must have > 9.0 hours of pure moonless dark sky
    for c in cities_vis:
        assert c["pure_dark_duration_hours"] >= 9.0
        assert c["moon_phase_pct"] < 12.0  # Waxing crescent
        assert c["vesta_culmination_alt_deg"] > 40.0
        
    # Latitudinal culmination hierarchy: Guangzhou (lowest lat) > Shanghai > Beijing > Urumqi
    assert city_map["Guangzhou"]["vesta_culmination_alt_deg"] > city_map["Shanghai"]["vesta_culmination_alt_deg"]
    assert city_map["Shanghai"]["vesta_culmination_alt_deg"] > city_map["Beijing"]["vesta_culmination_alt_deg"]
    assert city_map["Beijing"]["vesta_culmination_alt_deg"] > city_map["Urumqi"]["vesta_culmination_alt_deg"]


def test_rotational_lightcurve_simulation():
    curve = simulate_rotational_lightcurve(hours=6.0, step_minutes=15)
    assert len(curve) == int(6.0 * 60 / 15) + 1
    
    # Check rotation cycle completes within 6 hours (period is 5.34 h)
    phases = [pt["rotational_phase"] for pt in curve]
    assert max(phases) > 0.95
    
    # Light curve magnitude variation is bounded around 6.39 +/- 0.10
    v_mags = [pt["predicted_v_mag"] for pt in curve]
    assert min(v_mags) >= 6.30
    assert max(v_mags) <= 6.50


def test_protoplanet_physical_parameters():
    assert VESTA_PHYSICAL["mean_diameter_km"] > 500.0
    assert VESTA_PHYSICAL["bulk_density_g_cm3"] > 3.0
    assert VESTA_PHYSICAL["rheasilvia_crater_diameter_km"] > 500.0
    assert VESTA_PHYSICAL["rheasilvia_central_peak_km"] > 20.0
    assert "HED" in VESTA_PHYSICAL["meteorite_family"]
