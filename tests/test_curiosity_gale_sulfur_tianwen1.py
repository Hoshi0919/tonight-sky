"""
Unit tests for Curiosity Gale Crater Sulfur & Tianwen-1 Mars Orbiter Dynamics Engine
and the 2026 Human Deep Space Grand Vigintet (Twenty-Fold Fleet) Matrix.
"""

import os
import sys
import math
from datetime import datetime, timezone
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))

from curiosity_gale_sulfur_tianwen1_engine import (
    compute_curiosity_gale_gediz_vallis_sulfur,
    compute_tianwen1_mars_orbiter_dynamics,
    compute_mars_exploration_trinity,
    compute_grand_vigintet_matrix_2026,
    R_MARS_KM,
    MU_MARS,
)


def test_curiosity_gale_mission_timeline():
    """Verify Curiosity mission timeline, Gale crater coordinates, and odometer."""
    t_utc = datetime(2026, 10, 16, 15, 0, 0, tzinfo=timezone.utc)
    res = compute_curiosity_gale_gediz_vallis_sulfur(t_utc)

    assert res["years_elapsed"] > 14.0
    assert res["sols_elapsed"] > 5000.0
    assert pytest.approx(res["coordinates"]["latitude_deg"], abs=0.1) == -4.58
    assert pytest.approx(res["coordinates"]["longitude_deg"], abs=0.1) == 137.44
    assert res["gale_crater"]["odometer_km"] >= 33.0
    assert res["gale_crater"]["elevation_gained_m"] >= 800.0


def test_curiosity_gediz_vallis_pure_sulfur():
    """Verify Curiosity's Sol 4189 Gediz Vallis pure sulfur discovery."""
    res = compute_curiosity_gale_gediz_vallis_sulfur()
    sulfur = res["gediz_vallis_sulfur"]

    assert sulfur["discovery_sol"] == 4189
    assert "S8" in sulfur["mineral_type"] or "Sulfur" in sulfur["mineral_type"]
    assert "APXS" in sulfur["confirmation_instruments"][0]
    assert "ChemCam" in sulfur["confirmation_instruments"][1]
    assert sulfur["days_since_discovery"] > 800.0  # More than 2 years since May 2024


def test_curiosity_mmrtg_power_decay():
    """Verify MMRTG Pu-238 decay model and thermocouple degradation."""
    res = compute_curiosity_gale_gediz_vallis_sulfur()
    mmrtg = res["mmrtg"]

    assert mmrtg["half_life_yr"] == 87.74
    assert 0.88 < mmrtg["thermal_decay_factor"] < 0.91
    assert 0.88 < mmrtg["thermocouple_health_factor"] < 0.91
    # Electrical power should be between 75 W and 95 W after 14.2 years
    assert 75.0 <= mmrtg["current_electric_w"] <= 95.0


def test_tianwen1_polar_orbit_geometry():
    """Verify Tianwen-1 Mars polar remote sensing orbit geometry."""
    res = compute_tianwen1_mars_orbiter_dynamics()
    orb = res["orbit"]

    assert orb["periapsis_altitude_km"] == 265.0
    assert orb["apoapsis_altitude_km"] == 10700.0
    assert pytest.approx(orb["semi_major_axis_km"], abs=1.0) == 8872.0
    assert pytest.approx(orb["eccentricity"], abs=0.01) == 0.5881
    assert pytest.approx(orb["inclination_deg"], abs=0.2) == 86.9


def test_tianwen1_vis_viva_orbital_speeds():
    """Verify Tianwen-1 vis-viva orbital speeds, period, and revolutions per sol."""
    res = compute_tianwen1_mars_orbiter_dynamics()
    orb = res["orbit"]

    # Periapsis speed ~ 4.31 km/s, apoapsis speed ~ 1.12 km/s
    assert pytest.approx(orb["periapsis_speed_km_s"], abs=0.05) == 4.314
    assert pytest.approx(orb["apoapsis_speed_km_s"], abs=0.05) == 1.119
    assert orb["speed_ratio"] > 3.8
    # Period around 7.05 hours -> ~3.5 revs/sol
    assert pytest.approx(orb["period_hours"], abs=0.1) == 7.05
    assert 3.4 <= orb["revolutions_per_sol"] <= 3.6


def test_tianwen1_payloads_and_interstellar_imaging():
    """Verify Tianwen-1 payload suite, 3I/ATLAS imaging, and 3.5 TB data release."""
    res = compute_tianwen1_mars_orbiter_dynamics()

    assert len(res["payloads"]) == 7
    payload_names = [p["name"] for p in res["payloads"]]
    for expected in ["MoRIC", "HiRIC", "MOSIR", "MMS", "MOMAG", "MINPA", "MEPA"]:
        assert expected in payload_names

    obs = res["interstellar_observation"]
    assert "3I/ATLAS" in obs["target"]
    assert obs["distance_au"] == 0.194
    assert res["science_data_released_tb"] >= 3.5


def test_mars_exploration_trinity_spatial_separation():
    """Verify spatial separation between Curiosity and Perseverance on Mars."""
    trinity = compute_mars_exploration_trinity()
    sep = trinity["rover_separation"]

    assert len(trinity["trinity_members"]) == 3
    # Angular separation should be ~63.3°
    assert pytest.approx(sep["angular_separation_deg"], abs=0.5) == 63.27
    # Surface distance should be ~3,743 km
    assert pytest.approx(sep["surface_distance_km"], abs=20.0) == 3742.9


def test_grand_vigintet_matrix_ordering_and_completeness():
    """Verify the 20-flagship fleet is strictly ordered by descending heliocentric distance."""
    vigintet = compute_grand_vigintet_matrix_2026()
    fleet = vigintet["fleet"]

    assert vigintet["total_flagships"] == 20
    assert len(fleet) == 20

    # Ensure strictly descending heliocentric distance (or equal for co-distance)
    for i in range(len(fleet) - 1):
        assert fleet[i]["heliocentric_distance_au"] >= fleet[i+1]["heliocentric_distance_au"]

    # First is Voyager 1, last is Parker Solar Probe
    assert fleet[0]["name"] == "Voyager 1"
    assert fleet[0]["heliocentric_distance_au"] > 170.0

    assert fleet[-1]["name"] == "Parker Solar Probe"
    assert fleet[-1]["heliocentric_distance_au"] < 0.05

    # Check key flagships present
    names = [f["name"] for f in fleet]
    for required in [
        "Voyager 1", "Voyager 2", "New Horizons", "Juno", "JUICE", "Europa Clipper",
        "Lucy", "Psyche", "Curiosity", "Perseverance", "Tianwen-1 Orbiter", "Hera",
        "Hayabusa2# (SHARP)", "OSIRIS-APEX", "JWST", "Tianwen-2", "Queqiao-2",
        "BepiColombo", "Solar Orbiter", "Parker Solar Probe"
    ]:
        assert required in names


def test_grand_vigintet_extreme_duality_ratios():
    """Verify extreme physical duality metrics across the 20 deep space flagships."""
    vigintet = compute_grand_vigintet_matrix_2026()
    extrema = vigintet["duality_extrema"]

    assert extrema["heliocentric_distance_span_ratio"] > 3700.0
    assert extrema["solar_radiation_flux_ratio"] > 1.4e7
    assert extrema["geocentric_distance_span_ratio"] > 67000.0
    assert extrema["one_way_light_time_ratio"] > 67000.0
    assert extrema["relative_speed_ratio"] > 2.5e7
    assert extrema["operating_thermal_span_k"] > 1670.0
