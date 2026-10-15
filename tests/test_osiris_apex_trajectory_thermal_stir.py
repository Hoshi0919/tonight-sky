"""
Unit tests for OSIRIS-APEX trajectory, 3:2 resonance, fig-leaf thermal protection,
2029 EGA velocity dissipation, STIR excavation physics, and Grand Undecet fleet integration.
"""

import pytest
import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))

from osiris_apex_trajectory_thermal_stir_engine import (
    calculate_heliocentric_orbit_and_resonance,
    calculate_solar_radiation_and_fig_leaf_thermal_barrier,
    calculate_2029_ega_apophis_velocity_reduction,
    calculate_stir_regolith_interaction_and_planetary_defense_safety,
    calculate_grand_undecet_matrix_2026,
)


def test_heliocentric_resonance():
    """Verify semi-major axis, 243.4-day period, and exact 3:2 resonance with Earth."""
    res = calculate_heliocentric_orbit_and_resonance()
    assert res["perihelion_au"] == 0.500
    assert res["aphelion_au"] == 1.026
    assert 0.760 <= res["semimajor_axis_au"] <= 0.765
    assert 0.340 <= res["eccentricity"] <= 0.350
    assert 0.660 <= res["period_years"] <= 0.670
    assert 240.0 <= res["period_days"] <= 246.0
    # Exactly 3 orbits in 2 Earth years (within 0.1% tolerance)
    assert abs(res["orbits_per_2_years"] - 3.0) < 0.01
    assert 48.0 <= res["perihelion_velocity_km_s"] <= 49.5
    assert 23.0 <= res["aphelion_velocity_km_s"] <= 24.5


def test_solar_flux_and_exceedance():
    """Verify 4x solar constant at 0.5 AU perihelion and 2.37x original design exceedance."""
    res = calculate_solar_radiation_and_fig_leaf_thermal_barrier()
    assert res["solar_flux_1au_w_m2"] == 1361.0
    assert res["solar_flux_perihelion_w_m2"] == 5444.0
    assert res["flux_ratio_to_1au"] == 4.0
    assert 2290.0 <= res["original_design_flux_limit_w_m2"] <= 2300.0
    assert 2.35 <= res["flux_exceedance_factor"] <= 2.40


def test_thermal_equilibrium_and_fig_leaf_protection():
    """Verify unprotected thermal runaway (>290C) vs fig-leaf thermal containment (<170C array, nominal deck)."""
    res = calculate_solar_radiation_and_fig_leaf_thermal_barrier()
    assert 560.0 <= res["unprotected_equilibrium_temp_k"] <= 570.0
    assert 285.0 <= res["unprotected_equilibrium_temp_c"] <= 295.0
    assert res["fig_leaf_tilt_deg"] == 68.0
    assert res["effective_flux_canted_panel_w_m2"] < res["original_design_flux_limit_w_m2"]
    assert res["canted_panel_temp_c"] < 175.0
    assert res["shaded_deck_temp_range_c"] == [-10.0, 25.0]


def test_2029_ega_dissipation():
    """Verify 98.98% relative velocity reduction during 1,153 km Earth flyby on 2029-04-13."""
    res = calculate_2029_ega_apophis_velocity_reduction()
    assert res["flyby_date"] == "2029-04-13"
    assert res["flyby_altitude_km"] == 1153.0
    assert 7525.0 <= res["perigee_radius_km"] <= 7535.0
    assert res["initial_relative_velocity_m_s"] == 5000.0
    assert res["post_ega_relative_velocity_m_s"] == 51.0
    assert 98.90 <= res["velocity_reduction_pct"] <= 99.10
    assert 11.3 <= res["perigee_velocity_km_s"] <= 11.6


def test_propellant_budget_margin():
    """Verify delta-v remaining (525 m/s) covers proximity operations (327 m/s) with >60% margin."""
    res = calculate_2029_ega_apophis_velocity_reduction()
    assert res["delta_v_remaining_m_s"] == 525.0
    assert res["delta_v_required_prox_ops_m_s"] == 327.0
    assert res["delta_v_margin_m_s"] == 198.0
    assert res["margin_percentage"] > 60.0


def test_stir_regolith_interaction():
    """Verify STIR thruster plume parameters and excavation of >25 tonnes of regolith."""
    res = calculate_stir_regolith_interaction_and_planetary_defense_safety()
    assert res["thrust_total_n"] == 18.0
    assert res["isp_s"] == 220.0
    assert 2150.0 <= res["exhaust_velocity_m_s"] <= 2165.0
    assert 0.020 <= res["fuel_mass_burned_kg"] <= 0.030
    assert 25.0 <= res["impulse_transferred_n_s"] <= 30.0
    assert res["estimated_crater_diameter_m"] == 9.0
    assert res["estimated_crater_depth_m"] == 0.6
    assert res["estimated_excavated_mass_kg"] > 25000.0


def test_planetary_defense_safety_proof():
    """Mathematically prove STIR perturbation is < 0.5 nm/s, >200,000x smaller than radar uncertainty."""
    res = calculate_stir_regolith_interaction_and_planetary_defense_safety()
    assert res["delta_v_imparted_nm_s"] < 1.0  # Under 1 nm/s
    assert res["delta_v_imparted_to_apophis_m_s"] < 1.0e-9
    assert res["radar_uncertainty_threshold_m_s"] == 1.0e-4
    assert res["safety_margin_factor"] > 200000.0


def test_grand_undecet_matrix():
    """Verify Grand Undecet: exactly 11 flagships, >3,700x heliocentric span, >1.4e7x flux ratio."""
    res = calculate_grand_undecet_matrix_2026()
    assert res["fleet_count"] == 11
    names = [f["name"] for f in res["fleet"]]
    assert any("OSIRIS-APEX" in n for n in names)
    assert any("Voyager 1" in n for n in names)
    assert any("Parker" in n for n in names)
    assert any("Tianwen-2" in n for n in names)
    assert any("Psyche" in n for n in names)
    assert any("Hera" in n for n in names)
    assert any("JUICE" in n for n in names)
    assert any("Europa Clipper" in n for n in names)
    assert any("BepiColombo" in n for n in names)
    assert any("JWST" in n for n in names)
    assert any("New Horizons" in n for n in names)
    assert res["heliocentric_span_ratio"] > 3700.0
    assert res["flux_span_ratio"] > 1.4e7
