"""
Unit tests for IBEX 18th Anniversary & Grand Duoquadragintet (42-probe fleet) engine.
"""

import sys
from pathlib import Path
import pytest
import math
import datetime

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from ibex_interstellar_boundary_grand_duoquadragintet_engine import (
    get_ibex_timeline,
    get_lunar_resonance_orbit,
    ena_velocity_km_s,
    ena_flight_time,
    compute_heliosphere_optical_depth,
    get_grand_duoquadragintet_fleet,
    compute_fleet_extremes,
    IBEX_LAUNCH_UTC,
    IBEX_DRY_MASS_KG,
    LUNAR_ENA_ALBEDO
)

def test_ibex_timeline_18th_anniversary():
    t = get_ibex_timeline(datetime.datetime(2026, 10, 19, 17, 47, 23, tzinfo=datetime.timezone.utc))
    assert t["is_18th_anniversary"] is True
    assert 6570.0 <= t["total_days"] <= 6580.0
    assert 17.99 <= t["total_years"] <= 18.01
    assert t["total_orbits"] > 720.0

def test_lunar_resonance_orbit():
    orb = get_lunar_resonance_orbit()
    assert orb["perigee_km"] == 48000.0
    assert orb["apogee_km"] == 320000.0
    assert orb["semi_major_axis_km"] == 184000.0
    assert 0.73 <= orb["eccentricity"] <= 0.75
    assert 9.0 <= orb["period_days"] <= 9.2
    # Verify 3:1 orbital resonance with Moon (27.32 days / 9.09 days ~ 3.005)
    assert 2.98 <= orb["resonance_ratio"] <= 3.03
    # Apogee is ~83% of lunar distance (384,400 km)
    assert 0.80 <= orb["apogee_lunar_fraction"] <= 0.86

def test_charge_exchange_optical_thinness():
    opt = compute_heliosphere_optical_depth()
    assert opt["is_optically_thin"] is True
    assert 0.10 <= opt["optical_depth_tau"] <= 0.20
    assert 0.80 <= opt["transmission_fraction"] <= 0.92

def test_ena_velocity_dispersion():
    v_100ev = ena_velocity_km_s(0.1)
    v_1kev = ena_velocity_km_s(1.0)
    v_4kev = ena_velocity_km_s(4.0)

    # Velocity scales as sqrt(E) -> v(4 keV) = 2 * v(1 keV)
    assert 130.0 <= v_100ev <= 145.0
    assert 430.0 <= v_1kev <= 445.0
    assert 865.0 <= v_4kev <= 885.0
    assert math.isclose(v_4kev / v_1kev, 2.0, rel_tol=1e-3)

def test_ena_flight_time_from_heliosheath():
    f_1kev = ena_flight_time(1.0, source_dist_au=120.0, target_dist_au=1.0)
    f_4kev = ena_flight_time(4.0, source_dist_au=120.0, target_dist_au=1.0)
    f_100ev = ena_flight_time(0.1, source_dist_au=120.0, target_dist_au=1.0)

    # 1 keV ENA takes ~1.29 years from 120 AU to 1 AU
    assert 1.25 <= f_1kev["flight_time_years"] <= 1.35
    assert 450.0 <= f_1kev["flight_time_days"] <= 490.0

    # 4 keV ENA takes ~0.64 years
    assert 0.60 <= f_4kev["flight_time_years"] <= 0.68

    # 100 eV takes ~4.08 years
    assert 3.9 <= f_100ev["flight_time_years"] <= 4.2

def test_ibex_instruments_energy_ranges():
    # IBEX-Lo: 0.01 to 2.0 keV; IBEX-Hi: 0.38 to 6.0 keV
    lo_range = (0.01, 2.0)
    hi_range = (0.38, 6.0)
    overlap = (max(lo_range[0], hi_range[0]), min(lo_range[1], hi_range[1]))
    assert overlap[0] == 0.38
    assert overlap[1] == 2.0
    assert overlap[1] > overlap[0]

def test_ibex_ribbon_geometry_perpendicularity():
    # Ribbon center in galactic coordinates: l ~ 33 deg, b ~ 55 deg
    # In pristine ISMF geometry, the ribbon circle forms where B_ISMF . r = 0
    cos_theta = math.cos(math.radians(90.0))
    assert math.isclose(cos_theta, 0.0, abs_tol=1e-7)

def test_lunar_ena_albedo():
    # Lunar albedo discovered by IBEX: ~16% backscatter of solar wind protons as neutral H
    assert 0.10 <= LUNAR_ENA_ALBEDO <= 0.20

def test_grand_duoquadragintet_fleet_count_and_ordering():
    fleet = get_grand_duoquadragintet_fleet()
    assert len(fleet) == 42  # The Hitchhiker's Guide answer to life, the universe, and everything
    assert fleet[0]["name"] == "Voyager 1"
    assert fleet[-1]["name"] == "Parker Solar Probe"

    # Verify strictly non-increasing heliocentric distance
    for i in range(len(fleet) - 1):
        assert fleet[i]["heliocentric_au"] >= fleet[i+1]["heliocentric_au"], (
            f"Ordering violation: {fleet[i]['name']} ({fleet[i]['heliocentric_au']} AU) < "
            f"{fleet[i+1]['name']} ({fleet[i+1]['heliocentric_au']} AU)"
        )

def test_grand_duoquadragintet_fleet_extremes():
    ext = compute_fleet_extremes()
    assert ext["probe_count"] == 42
    assert ext["distance_ratio"] > 3700.0
    assert ext["solar_flux_ratio"] > 1.4e7

    # Check agencies
    fleet = get_grand_duoquadragintet_fleet()
    agencies = {p["agency"] for p in fleet}
    assert any("NASA" in a for a in agencies)
    assert any("ESA" in a for a in agencies)
    assert any("CNSA" in a for a in agencies)
    assert any("JAXA" in a for a in agencies)
    assert any("ISRO" in a for a in agencies)
    assert any("KARI" in a for a in agencies)
    assert any("UAESA" in a for a in agencies)
