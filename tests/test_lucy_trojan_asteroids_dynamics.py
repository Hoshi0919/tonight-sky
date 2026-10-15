"""
Unit tests for NASA Lucy Jupiter Trojan Asteroids Tour, UltraFlex Solar Array LILT Dynamics,
Nice Model Primordial Fossil Taxonomy & 2026 Grand Duodecet (人类深空十二极黄金舰队) Physics Engine.
"""

import pytest
import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))

from lucy_trojan_asteroids_dynamics_engine import (
    calculate_lucy_heliocentric_cruise_and_pretzal_resonance,
    calculate_ultraflex_solar_array_power_and_tension_dynamics,
    calculate_nice_model_trojan_taxonomy_and_spectral_diversity,
    calculate_autonomous_tracking_terminal_optics,
    calculate_grand_duodecet_matrix_2026,
    ULTRAFLEX_DIAMETER_M,
    CRUISE_POWER_BASELINE_W,
)


def test_heliocentric_cruise_and_orbit_parameters():
    """Verify Keplerian orbit elements after EGA-2 and 2026-10-15 state."""
    res = calculate_lucy_heliocentric_cruise_and_pretzal_resonance()

    assert res["perihelion_au"] == pytest.approx(0.985, abs=0.01)
    assert res["aphelion_au"] == pytest.approx(5.680, abs=0.01)
    assert res["semimajor_axis_au"] == pytest.approx(3.3325, abs=0.01)
    assert res["eccentricity"] == pytest.approx(0.7044, abs=0.01)
    assert res["orbital_period_years"] == pytest.approx(6.084, abs=0.05)

    # Heliocentric distance on 2026-10-15 should cross the 5 AU milestone
    assert 5.00 <= res["heliocentric_distance_au"] <= 5.10
    assert 9.0 <= res["orbital_speed_km_s"] <= 10.0
    assert res["days_since_launch"] == 1825.0  # Tomorrow is exactly 5 years!


def test_light_travel_time_and_delay():
    """Verify deep space radio delay at ~5.08 AU geocentric distance."""
    res = calculate_lucy_heliocentric_cruise_and_pretzal_resonance()

    assert 40.0 <= res["one_way_light_time_min"] <= 45.0
    assert 80.0 <= res["rtlt_light_time_min"] <= 90.0


def test_ultraflex_solar_array_geometry_and_lilt_power():
    """Verify 7.3m UltraFlex array geometry and LILT power output at >5 AU."""
    res = calculate_ultraflex_solar_array_power_and_tension_dynamics()

    assert res["array_diameter_m"] == 7.30
    assert res["single_array_area_m2"] == pytest.approx(41.85, abs=0.1)
    assert res["total_array_area_m2"] == pytest.approx(83.71, abs=0.1)

    # Solar flux drops below 4% of Earth's value
    assert res["flux_ratio_current_pct"] < 4.0
    assert res["flux_ratio_aphelion_pct"] < 3.5

    # Power output exceeds baseline cruise needs with healthy margin
    assert res["power_output_current_w"] > 1200.0
    assert res["power_output_aphelion_w"] > 950.0
    assert res["power_margin_aphelion_w"] > 500.0
    assert res["power_margin_aphelion_pct"] > 100.0


def test_ultraflex_tension_recovery_dynamics():
    """Verify recovery from array deployment anomaly and modal stiffening."""
    res = calculate_ultraflex_solar_array_power_and_tension_dynamics()

    assert res["initial_deployment_angle_deg"] == 345.0
    assert res["recovered_deployment_angle_deg"] >= 355.0
    assert res["recovered_tension_pct"] >= 98.0
    assert res["structural_frequency_recovered_hz"] > 0.25
    assert res["structural_frequency_recovered_hz"] > 2.5 * res["structural_frequency_unlatched_hz"]


def test_nice_model_target_diversity_and_spectral_taxonomy():
    """Verify the 11 mission targets and primordial solar system taxonomy."""
    res = calculate_nice_model_trojan_taxonomy_and_spectral_diversity()

    assert res["target_count"] == 11
    assert res["s_type_count"] >= 2  # Dinkinesh & Selam
    assert res["c_type_count"] >= 2  # Donaldjohanson, Eurybates, Queta
    assert res["p_type_count"] >= 3  # Polymele, Shaun, Patroclus/Menoetius
    assert res["d_type_count"] >= 3  # Leucus, Orus, Patroclus/Menoetius

    # Extremely dark primitive asteroids (albedo ~0.04 to 0.05) vs S-type (0.27)
    assert res["min_albedo"] <= 0.045
    assert res["max_albedo"] >= 0.25

    # Patroclus-Menoetius binary density indicative of porous ice-rock (Kuiper belt origin)
    assert res["patroclus_density_g_cm3"] < 1.0


def test_terminal_tracking_system_and_ipp_slew_capability():
    """Verify autonomous terminal optical tracking and IPP platform margins."""
    res = calculate_autonomous_tracking_terminal_optics()

    assert res["flyby_velocity_km_s"] == 5.78
    assert res["closest_approach_km"] == 1000.0
    assert 0.30 <= res["max_angular_slew_rate_deg_s"] <= 0.36
    assert res["ipp_max_slew_rate_deg_s"] == 1.50
    assert res["slew_rate_margin_pct"] > 300.0
    assert res["closed_loop_update_rate_hz"] == 10.0


def test_grand_duodecet_fleet_composition_and_extrema():
    """Verify the 12 flagship missions of the 2026 Grand Duodecet."""
    res = calculate_grand_duodecet_matrix_2026()

    assert res["fleet_count"] == 12
    fleet_names = [f["name"] for f in res["fleet"]]

    # Check key flagships
    assert any("旅行者 1 号" in n for n in fleet_names)
    assert any("新视野号" in n for n in fleet_names)
    assert any("木星冰月探测器" in n for n in fleet_names)
    assert any("欧罗巴快船" in n for n in fleet_names)
    assert any("露西号" in n for n in fleet_names)
    assert any("灵神星探测器" in n for n in fleet_names)
    assert any("赫拉号" in n for n in fleet_names)
    assert any("天问二号" in n for n in fleet_names)
    assert any("OSIRIS-APEX" in n for n in fleet_names)
    assert any("詹姆斯·韦伯" in n for n in fleet_names)
    assert any("贝皮可伦坡" in n for n in fleet_names)
    assert any("帕克太阳探测器" in n for n in fleet_names)

    # Extremes
    assert res["heliocentric_min_au"] == 0.046
    assert res["heliocentric_max_au"] == 173.22
    assert res["heliocentric_span_ratio"] > 3700.0
    assert res["flux_span_ratio"] > 1.4e7


def test_mission_milestones_and_countdown():
    """Verify countdowns to key Lucy maneuvers and encounters."""
    res = calculate_lucy_heliocentric_cruise_and_pretzal_resonance()

    assert 160.0 <= res["days_to_dsm3"] <= 180.0
    assert 290.0 <= res["days_to_eurybates"] <= 315.0
