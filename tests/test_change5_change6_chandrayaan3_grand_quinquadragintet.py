"""
Unit tests for Chang'e-5 DRO, Chang'e-6 Sun-Earth L2, Chandrayaan-3 PM (SHAPE)
and The Grand Quinquadragintet (45-probe fleet) engine.
"""

import sys
from pathlib import Path
import pytest
import math
import datetime

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from change5_change6_chandrayaan3_grand_quinquadragintet_engine import (
    get_change5_timeline,
    compute_lunar_dro_dynamics,
    get_change6_timeline,
    compute_change6_l2_halo_orbit,
    get_chandrayaan3_pm_timeline,
    compute_shape_earth_polarimetry,
    get_grand_quinquadragintet_fleet,
    compute_fleet_extremes,
    get_agency_breakdown,
    CHANGE5_LAUNCH_UTC,
    CHANGE6_LAUNCH_UTC,
    CHANDRAYAAN3_LAUNCH_UTC
)


def test_change5_timeline():
    t = get_change5_timeline(datetime.datetime(2026, 10, 19, 12, 0, 0, tzinfo=datetime.timezone.utc))
    assert 2150.0 <= t["total_days"] <= 2160.0
    assert 5.85 <= t["total_years"] <= 5.95
    assert t["dro_days"] > 1700.0
    assert t["sample_returned_grams"] == 1731.0
    assert "Mons Rümker" in t["sample_site"]
    assert "DRO" in t["current_regime"]


def test_lunar_dro_dynamics():
    dro = compute_lunar_dro_dynamics()
    assert 60000.0 <= dro["lunar_hill_radius_km"] <= 63000.0
    assert dro["dro_average_radius_km"] == 75000.0
    assert dro["is_outside_hill_sphere"] is True
    assert 13.0 <= dro["orbital_period_days"] <= 14.5
    assert 1.9 <= dro["resonance_with_moon"] <= 2.1
    assert dro["station_keeping_delta_v_ms_yr"] <= 2.0
    assert "CR3BP" in dro["stability_type"]


def test_change6_timeline():
    t = get_change6_timeline(datetime.datetime(2026, 10, 19, 12, 0, 0, tzinfo=datetime.timezone.utc))
    assert 895.0 <= t["total_days"] <= 905.0
    assert 2.40 <= t["total_years"] <= 2.50
    assert t["l2_days"] > 765.0
    assert t["sample_returned_grams"] == 1935.3
    assert "Far Side" in t["sample_site"]
    assert "L2" in t["current_regime"]


def test_change6_l2_halo_orbit():
    halo = compute_change6_l2_halo_orbit()
    assert halo["l2_distance_km"] == 1500000.0
    assert 4.9 <= halo["light_time_one_way_s"] <= 5.1
    assert halo["heliocentric_au"] == 1.010
    assert len(halo["sel2_quaternary_fleet"]) == 4
    assert "JWST" in halo["sel2_quaternary_fleet"]
    assert "Euclid" in halo["sel2_quaternary_fleet"]
    assert "Spektr-RG" in halo["sel2_quaternary_fleet"]
    assert "Chang'e-6 Orbiter" in halo["sel2_quaternary_fleet"]


def test_chandrayaan3_pm_timeline():
    t = get_chandrayaan3_pm_timeline(datetime.datetime(2026, 10, 19, 12, 0, 0, tzinfo=datetime.timezone.utc))
    assert 1190.0 <= t["total_days"] <= 1200.0
    assert 3.20 <= t["total_years"] <= 3.35
    assert "SHAPE" in t["primary_instrument"]
    assert "Exoplanet Analog" in t["current_regime"]


def test_shape_earth_polarimetry():
    shape = compute_shape_earth_polarimetry()
    assert shape["spectral_range_um"] == [0.3, 1.0]
    assert 53.0 <= shape["ocean_glint_brewster_angle_deg"] <= 53.3
    assert shape["ocean_glint_max_polarization"] == 1.0
    assert shape["cloud_rainbow_scattering_angle_deg"] == 140.0
    assert shape["vegetation_red_edge_nm"] == 700.0


def test_grand_quinquadragintet_fleet_count_and_ordering():
    fleet = get_grand_quinquadragintet_fleet()
    assert len(fleet) == 45, f"Expected 45 probes, got {len(fleet)}"
    
    # Assert non-increasing heliocentric AU
    distances = [p["heliocentric_au"] for p in fleet]
    for i in range(len(distances) - 1):
        assert distances[i] >= distances[i + 1], f"Fleet not sorted at index {i}: {fleet[i]} vs {fleet[i+1]}"
    
    # Assert extreme endpoints
    assert fleet[0]["name"] == "Voyager 1"
    assert fleet[0]["heliocentric_au"] == 173.22
    assert fleet[-1]["name"] == "Parker Solar Probe"
    assert fleet[-1]["heliocentric_au"] == 0.046


def test_fleet_extremes():
    ext = compute_fleet_extremes()
    assert ext["probe_count"] == 45
    assert ext["r_max_au"] == 173.22
    assert ext["r_min_au"] == 0.046
    assert 3760.0 <= ext["distance_ratio"] <= 3770.0
    assert ext["solar_flux_ratio"] > 14000000.0


def test_chinese_deep_space_fleet():
    fleet = get_grand_quinquadragintet_fleet()
    cnsa_probes = [p["name"] for p in fleet if p["agency"] == "CNSA"]
    assert len(cnsa_probes) == 6
    expected = [
        "Tianwen-1 Orbiter",
        "Chang'e-6 Orbiter",
        "Tianwen-2",
        "Queqiao-2",
        "Chang'e-4 / Yutu-2",
        "Chang'e-5 Orbiter"
    ]
    for exp in expected:
        assert exp in cnsa_probes, f"Missing expected CNSA probe: {exp}"


def test_indian_deep_space_fleet():
    fleet = get_grand_quinquadragintet_fleet()
    isro_probes = [p["name"] for p in fleet if p["agency"] == "ISRO"]
    assert len(isro_probes) == 3
    expected = [
        "Chandrayaan-2",
        "Chandrayaan-3 PM",
        "Aditya-L1"
    ]
    for exp in expected:
        assert exp in isro_probes, f"Missing expected ISRO probe: {exp}"
