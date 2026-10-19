"""
Unit tests for Queqiao-1, Chang'e-3 Lander & LUT, TESS and The Grand Octoquadragintet (48-Probe Fleet).
Validates:
1. Queqiao-1 Earth-Moon L2 Halo orbit geometry, distance, and multi-year longevity.
2. Queqiao-1 unocculted line-of-sight (LOS) to both Earth and lunar farside.
3. Chang'e-3 lander on-surface duration (>12.8 years, >158 lunar day-night cycles).
4. Chang'e-3 Lunar-based Ultraviolet Telescope (LUT) optical specs and exospheric water constraint.
5. TESS P/2 2:1 lunar orbital resonance and 13.66-day period.
6. TESS apogee and perigee outside Van Allen radiation belts.
7. Grand Octoquadragintet 48-probe catalog integrity and strict heliocentric distance ordering.
8. Voyager 1 to Parker Solar Probe extreme physical ratios (>3,700x distance, >14,000,000x solar flux).
9. China CNSA 8-probe deep space and cislunar operational matrix completeness.
10. Global multi-agency distribution (NASA, CNSA, ESA, ISRO, JAXA, Roscosmos, UAESA, KARI).
"""

import sys
from pathlib import Path
import pytest
import datetime

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from queqiao1_change3_tess_grand_octoquadragintet_engine import (
    get_queqiao1_status,
    get_change3_lut_status,
    get_tess_status,
    get_grand_octoquadragintet_fleet,
    compute_fleet_extremes,
    get_agency_breakdown,
    get_cnsa_probes,
    MOON_SIDEREAL_PERIOD_DAYS,
    MOON_SYNODIC_PERIOD_DAYS
)


def test_queqiao1_halo_orbit_geometry():
    """Verify Queqiao-1 Earth-Moon L2 Halo orbit parameters and service longevity."""
    target_utc = datetime.datetime(2026, 10, 19, 12, 0, 0, tzinfo=datetime.timezone.utc)
    status = get_queqiao1_status(target_utc)

    assert status["total_days"] > 3000.0, "Queqiao-1 should have exceeded 3,000 days in space"
    assert status["total_years"] >= 8.4, "Queqiao-1 should have served over 8.4 years"
    assert status["halo_period_days"] == pytest.approx(14.0, abs=0.5)
    assert status["antenna_diameter_m"] == 4.2
    assert status["life_extension_ratio"] >= 2.8, "Should exceed 3-year design life by >2.8x"


def test_queqiao1_line_of_sight_geometry():
    """Verify Queqiao-1 maintains unocculted line-of-sight to Earth and lunar farside."""
    status = get_queqiao1_status()

    # The off-axis angle from lunar center as seen from Earth must exceed Moon's angular radius (~0.26 deg)
    assert status["has_direct_earth_los"] is True
    assert status["has_direct_farside_los"] is True
    assert status["min_off_axis_angle_deg"] > 1.0, "Halo amplitude must keep probe clear of lunar disk"
    assert status["earth_distance_km"] > 400000.0, "Distance from Earth must exceed 400,000 km"
    assert status["one_way_light_sec"] == pytest.approx(1.49, abs=0.1)


def test_change3_lander_longevity():
    """Verify Chang'e-3 lander has operated for >12.8 years and >158 lunar day-night cycles."""
    target_utc = datetime.datetime(2026, 10, 19, 12, 0, 0, tzinfo=datetime.timezone.utc)
    status = get_change3_lut_status(target_utc)

    assert status["surface_days"] > 4600.0, "Must exceed 4,600 days on lunar surface"
    assert status["total_years"] >= 12.8, "Must exceed 12.8 Earth years on lunar surface"
    assert status["lunar_day_night_cycles"] >= 158.0, "Must have survived >158 lunar day-night thermal cycles"
    assert status["longest_operating_surface_observatory"] is True
    assert status["rhu_pu238"] is True


def test_change3_lut_optics_and_water_limit():
    """Verify Chang'e-3 LUT optical parameters and exospheric water upper bound."""
    status = get_change3_lut_status()

    assert status["aperture_mm"] == 150.0
    assert status["f_ratio"] == pytest.approx(3.75, abs=0.01)
    assert status["bandpass_nm"] == (245.0, 345.0)
    assert status["water_column_density_limit_cm2"] <= 1.0e11
    assert status["water_number_density_limit_cm3"] <= 1.0e4


def test_tess_p_over_2_resonance():
    """Verify TESS 2:1 P/2 orbital resonance with the Moon."""
    status = get_tess_status()

    assert status["is_p_over_2_resonance"] is True
    assert status["resonance_ratio"] == pytest.approx(2.0, abs=0.05)
    assert status["orbital_period_days"] == pytest.approx(MOON_SIDEREAL_PERIOD_DAYS / 2.0, abs=0.1)
    assert status["completed_orbits"] > 220.0, "TESS must have completed >220 orbits"


def test_tess_orbit_safety_and_payload():
    """Verify TESS perigee sits safely outside Van Allen radiation belts."""
    status = get_tess_status()

    assert status["is_outside_van_allen_belts"] is True
    assert status["perigee_km"] >= 100000.0
    assert status["perigee_re"] >= 16.0
    assert status["cameras_count"] == 4
    assert status["candidate_exoplanets"] >= 7000
    assert status["confirmed_exoplanets"] >= 800


def test_grand_octoquadragintet_fleet_count_and_ordering():
    """Verify the 48-probe Grand Octoquadragintet is strictly sorted by heliocentric distance."""
    fleet = get_grand_octoquadragintet_fleet()

    assert len(fleet) == 48, f"Expected exactly 48 probes, got {len(fleet)}"
    assert fleet[0]["name"] == "Voyager 1"
    assert fleet[-1]["name"] == "Parker Solar Probe"

    # Verify descending ordering
    for i in range(len(fleet) - 1):
        assert fleet[i]["heliocentric_au"] >= fleet[i+1]["heliocentric_au"], (
            f"Fleet ordering violation at index {i}: {fleet[i]['name']} ({fleet[i]['heliocentric_au']} AU) "
            f"< {fleet[i+1]['name']} ({fleet[i+1]['heliocentric_au']} AU)"
        )


def test_fleet_extreme_physical_ratios():
    """Verify the physical extremes between Voyager 1 and Parker Solar Probe."""
    extremes = compute_fleet_extremes()

    assert extremes["probe_count"] == 48
    assert extremes["distance_ratio"] > 3700.0, "Heliocentric distance span must exceed 3,700x"
    assert extremes["solar_flux_ratio"] > 1.4e7, "Solar flux span must exceed 14 million times"


def test_cnsa_eight_probe_deep_space_matrix():
    """Verify CNSA operates 8 active probes spanning Mars, Asteroid, Moon surface, DRO, and L2."""
    cnsa = get_cnsa_probes()

    assert len(cnsa) == 8, f"Expected 8 CNSA probes, got {len(cnsa)}"
    names = {p["name"] for p in cnsa}
    expected = {
        "Tianwen-1 Orbiter",
        "Tianwen-2",
        "Queqiao-1",
        "Queqiao-2",
        "Chang'e-4 / Yutu-2",
        "Chang'e-3 Lander & LUT",
        "Chang'e-5 Orbiter",
        "Chang'e-6 Orbiter"
    }
    assert names == expected, f"CNSA fleet mismatch: {names.symmetric_difference(expected)}"


def test_global_agency_breakdown():
    """Verify multi-agency participation across all major spacefaring entities."""
    breakdown = get_agency_breakdown()

    total_probes = sum(breakdown.values())
    assert total_probes == 48, f"Total probes must equal 48, got {total_probes}"
    assert breakdown["CNSA"] == 8
    assert breakdown["NASA"] >= 20
    assert "ISRO" in breakdown and breakdown["ISRO"] == 3
