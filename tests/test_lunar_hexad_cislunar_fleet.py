"""
Unit tests for Lunar Hexad & The Grand Quattuortrigintet Engine (2026-10-18)
==========================================================================
Verifies astrodynamics, payload physics, and fleet census for the six active
lunar exploration missions (The Lunar Hexad / 月球现役六大金刚) and the
comprehensive 34-probe deep-space armada (The Grand Quattuortrigintet /
人类深空三十四极黄金舰队).

Author: Hoshi (Autonomous Space & Celestial Dynamics Laboratory)
Date: 2026-10-18 CST
"""

import sys
from pathlib import Path
import pytest
import math
from datetime import datetime, timezone

DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR / "scripts"))

from lunar_hexad_cislunar_fleet_engine import (
    lro_orbital_and_thermal_dynamics,
    chandrayaan2_optical_sar_xray_dynamics,
    danuri_blt_shadowcam_polcam_dynamics,
    capstone_nrho_astrodynamics,
    queqiao2_frozen_relay_dynamics,
    change4_yutu2_farside_rhus_dynamics,
    lunar_hexad_system_summary,
    the_grand_quattuortrigintet_fleet_census
)


def test_lro_orbital_mechanics_and_cryogenics():
    """Verify LRO 17+ years quasi-frozen polar orbit and Diviner 26K record."""
    res = lro_orbital_and_thermal_dynamics()
    
    assert res["mission"] == "Lunar Reconnaissance Orbiter (LRO)"
    assert res["agency"] == "NASA"
    assert res["elapsed_years"] > 17.0
    assert res["hp_km"] == 30.0
    assert res["ha_km"] == 200.0
    assert 0.045 < res["eccentricity"] < 0.046
    assert 118.0 < res["period_minutes"] < 121.0
    assert res["perilune_velocity_kms"] > res["apolune_velocity_kms"]
    assert res["cumulative_orbits"] > 70000
    
    # Cryogenic thermal physics
    assert res["diviner_lowest_temp_k"] == 26.0
    assert res["diviner_lowest_temp_c"] < -247.0
    assert res["diviner_lowest_temp_k"] < res["temp_comparison_pluto_k"]
    assert res["lroc_nac_resolution_m"] == 0.50
    assert res["lola_laser_pulses_total"] > 4.0e9


def test_chandrayaan2_optical_sar_xray():
    """Verify Chandrayaan-2 100km polar orbit, 0.25m OHRC and DFSAR radar."""
    res = chandrayaan2_optical_sar_xray_dynamics()
    
    assert res["mission"] == "Chandrayaan-2 Orbiter"
    assert res["agency"] == "ISRO"
    assert res["elapsed_years"] > 7.0
    assert res["altitude_km"] == 100.0
    assert res["eccentricity"] == 0.0
    assert 117.0 < res["period_minutes"] < 119.0
    assert 1.62 < res["circular_velocity_kms"] < 1.65
    assert res["cumulative_orbits"] > 30000
    
    # Payload breakthroughs
    assert res["ohrc_resolution_m"] == 0.25
    assert res["ohrc_advantage_over_lroc_factor"] == 2.0
    assert res["dfsar_bands_ghz"]["L_band"] == 1.25
    assert res["dfsar_bands_ghz"]["S_band"] == 2.50
    assert res["dfsar_penetration_depth_m"] == 5.0
    assert "Na" in res["class_detected_elements"]


def test_danuri_blt_shadowcam_polcam():
    """Verify Danuri BLT trajectory savings, ShadowCam 200x sensitivity and PolCam."""
    res = danuri_blt_shadowcam_polcam_dynamics()
    
    assert res["mission"] == "Danuri (KPLO)"
    assert res["agency"] == "KARI / NASA"
    assert res["elapsed_years"] > 3.5
    assert res["altitude_km"] == 100.0
    assert res["cumulative_orbits"] > 16000
    
    # BLT trajectory
    assert res["blt_max_distance_km"] >= 1.5e6
    assert res["blt_loi_deltav_ms"] < 200.0
    assert res["blt_deltav_savings_pct"] > 70.0
    
    # ShadowCam and PolCam
    assert res["shadowcam_sensitivity_vs_lroc"] == 200.0
    assert res["polcam_wavelengths_nm"] == [320, 430, 750]


def test_capstone_nrho_gateway_pathfinder():
    """Verify CAPSTONE 12U CubeSat in 9:2 NRHO halo orbit and 2 m/s/yr stability."""
    res = capstone_nrho_astrodynamics()
    
    assert res["mission"] == "CAPSTONE"
    assert res["form_factor"] == "12U CubeSat"
    assert res["mass_kg"] == 25.0
    assert res["elapsed_years"] > 3.8
    assert "9:2 orbital resonance" in res["resonance_ratio"]
    assert res["perilune_alt_km"] == 1600.0
    assert res["apolune_alt_km"] == 70000.0
    assert 6.5 < res["period_days"] < 6.6
    assert res["annual_stationkeeping_deltav_ms"] <= 2.5
    assert res["cumulative_revolutions"] > 200


def test_queqiao2_frozen_relay_orbit():
    """Verify Queqiao-2 4.2m umbrella antenna and 54.8 deg frozen relay orbit."""
    res = queqiao2_frozen_relay_dynamics()
    
    assert res["mission"] == "Queqiao-2 (鹊桥二号)"
    assert res["agency"] == "CNSA"
    assert res["mass_kg"] == 1200.0
    assert res["antenna_diameter_m"] == 4.2
    assert res["elapsed_years"] > 2.5
    assert res["hp_km"] == 200.0
    assert res["ha_km"] == 16000.0
    assert 0.80 < res["eccentricity"] < 0.81
    assert 24.0 < res["period_hours"] < 24.5
    assert res["critical_inclination_deg"] == 54.8
    assert res["south_pole_duty_cycle_pct"] >= 75.0
    assert len(res["supported_missions"]) == 3


def test_change4_yutu2_farside_rhus():
    """Verify Chang'e-4 & Yutu-2 7.79 yrs farside survival, LPR radar, and RHU heating."""
    res = change4_yutu2_farside_rhus_dynamics()
    
    assert "Chang'e-4" in res["mission"]
    assert res["agency"] == "CNSA"
    assert "Von Kármán Crater" in res["landing_site"]
    assert res["elapsed_years"] > 7.7
    assert res["lunar_days_operational"] >= 96
    assert res["rover_traverse_distance_m"] > 1600.0
    assert res["rfi_shielding_diameter_km"] > 3400.0
    assert res["lfs_frequency_range_mhz"] == (0.1, 40.0)
    assert res["lpr_subsurface_depth_m"] == 40.0
    assert res["night_temperature_c"] == -180.0
    assert "Plutonium-238" in res["thermal_survival_mechanism"]


def test_lunar_hexad_synthesis():
    """Verify aggregation of all 6 active lunar missions in The Lunar Hexad."""
    res = lunar_hexad_system_summary()
    
    assert res["fleet_name"] == "The Lunar Explorer Hexad (月球现役六大金刚)"
    assert res["total_probes"] == 6
    assert res["combined_operational_years"] > 40.0
    
    names = [p["name"] for p in res["probes"]]
    assert any("LRO" in n for n in names)
    assert any("Chandrayaan-2" in n for n in names)
    assert any("Danuri" in n for n in names)
    assert any("CAPSTONE" in n for n in names)
    assert any("Queqiao-2" in n for n in names)
    assert any("Chang'e-4" in n for n in names)


def test_the_grand_quattuortrigintet_fleet_census():
    """Verify complete 34-probe deep space fleet census ordered by heliocentric distance."""
    res = the_grand_quattuortrigintet_fleet_census()
    
    assert res["fleet_name"] == "The Grand Quattuortrigintet (人类深空三十四极黄金舰队)"
    assert res["probe_count"] == 34
    
    fleet = res["fleet"]
    assert len(fleet) == 34
    
    # Verify strict descending order by heliocentric distance
    for i in range(len(fleet) - 1):
        assert fleet[i]["dist_au"] >= fleet[i+1]["dist_au"]
    
    # Boundary probes
    assert fleet[0]["name"] == "Voyager 1"
    assert fleet[0]["dist_au"] == 173.22
    assert fleet[-1]["name"] == "Parker Solar Probe"
    assert fleet[-1]["dist_au"] == 0.046
    
    # Verify Martian Nonet representation (9 probes)
    martian_probes = [p for p in fleet if "Mars" in p["arena"] or "Gale" in p["arena"] or "Jezero" in p["arena"]]
    assert len(martian_probes) == 9
    
    # Verify Lunar Hexad representation (6 probes)
    lunar_probes = [p for p in fleet if "Lunar" in p["arena"] or "Cislunar" in p["arena"]]
    assert len(lunar_probes) == 6


def test_extreme_physics_falloffs_34_probes():
    """Verify astronomical physical extremes across the 34-probe fleet."""
    res = the_grand_quattuortrigintet_fleet_census()
    ext = res["extremes"]
    
    assert ext["distance_span_ratio"] > 3700.0
    assert ext["solar_flux_drop_ratio"] > 1.4e7
    assert ext["temperature_span_k"] > 1600.0
    assert ext["communication_latency_ratio"] > 60000.0
    assert ext["velocity_ratio"] > 2.5e7
