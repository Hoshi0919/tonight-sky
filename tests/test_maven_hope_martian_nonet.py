"""
Unit tests for MAVEN, Hope Probe (EMM), The Martian Nonet (火星九极),
and The Grand Trigintet (2026 人类深空三十极黄金舰队).

Author: Hoshi (Autonomous Space & Celestial Dynamics Laboratory)
Date: 2026-10-18 CST
"""

import math
import sys
from pathlib import Path
import pytest

DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR / "scripts"))

from maven_hope_martian_nonet_engine import (
    MavenDynamics,
    HopeProbeDynamics,
    MartianNonetSystem,
    GrandTrigintetFleet,
)


def test_maven_orbital_mechanics_aerobraking():
    maven = MavenDynamics()
    init = maven.initial_orbit
    aero = maven.aerobraked_orbit

    # Initial orbit (150 x 6200 km)
    assert init.periapsis_alt_km == 150.0
    assert init.apoapsis_alt_km == 6200.0
    assert pytest.approx(init.semi_major_axis_km, rel=1e-3) == 6564.5
    assert pytest.approx(init.eccentricity, rel=1e-3) == 0.4608
    assert pytest.approx(init.period_hours, rel=1e-2) == 4.473

    # Aerobraked orbit (150 x 4500 km)
    assert aero.periapsis_alt_km == 150.0
    assert aero.apoapsis_alt_km == 4500.0
    assert pytest.approx(aero.semi_major_axis_km, rel=1e-3) == 5714.5
    assert pytest.approx(aero.eccentricity, rel=1e-3) == 0.3806
    assert pytest.approx(aero.period_hours, rel=1e-2) == 3.615
    assert pytest.approx(aero.periapsis_velocity_kms, rel=1e-2) == 4.088
    assert pytest.approx(aero.apoapsis_velocity_kms, rel=1e-2) == 1.834
    assert pytest.approx(aero.orbits_per_sol, rel=1e-2) == 6.82


def test_maven_mission_duration():
    maven = MavenDynamics()
    duration = maven.mission_duration("2026-10-18")
    assert duration["days_in_orbit"] > 4400.0
    assert duration["earth_years"] > 12.0
    assert duration["mars_years"] > 6.4
    assert duration["estimated_orbits"] > 25000.0


def test_maven_argon_rayleigh_fractionation():
    maven = MavenDynamics()
    ar = maven.argon_rayleigh_fractionation()
    assert pytest.approx(ar["alpha"], rel=1e-3) == 0.9734
    assert ar["argon_loss_nominal"] == 0.66
    assert ar["argon_loss_uncertainty"] == 0.05
    assert ar["co2_loss_bar_min"] >= 0.50
    assert ar["co2_loss_bar_nominal"] == 1.00


def test_maven_oxygen_photochemical_escape_physics():
    maven = MavenDynamics()
    escape = maven.oxygen_photochemical_escape_physics()
    assert pytest.approx(escape["v_esc_kms"], rel=1e-2) == 4.886
    assert pytest.approx(escape["E_esc_eV"], rel=1e-2) == 1.98
    assert escape["E_dr_per_atom_eV"] > escape["E_esc_eV"]
    assert escape["can_escape"] == 1.0
    assert pytest.approx(escape["escape_rate_atoms_per_s"], rel=1e-2) == 1.1e26
    assert pytest.approx(escape["escape_rate_kg_per_s"], rel=1e-2) == 2.92
    assert escape["storm_total_loss_gs"] >= 10.0 * escape["quiet_total_loss_gs"]


def test_hope_probe_orbital_mechanics():
    hope = HopeProbeDynamics()
    orb = hope.orbit

    assert orb.periapsis_alt_km == 20000.0
    assert orb.apoapsis_alt_km == 43000.0
    assert orb.inclination_deg == 25.0
    assert pytest.approx(orb.semi_major_axis_km, rel=1e-3) == 34889.5
    assert pytest.approx(orb.eccentricity, rel=1e-3) == 0.3296
    assert pytest.approx(orb.period_hours, rel=1e-2) == 54.96
    assert pytest.approx(orb.periapsis_velocity_kms, rel=1e-2) == 1.564
    assert pytest.approx(orb.apoapsis_velocity_kms, rel=1e-2) == 0.789
    assert pytest.approx(orb.orbits_per_sol, rel=1e-2) == 0.449


def test_hope_deimos_orbital_resonance():
    hope = HopeProbeDynamics()
    res = hope.deimos_geometric_resonance()
    assert pytest.approx(res["deimos_orbit_km"], rel=1e-3) == 23463.2
    assert pytest.approx(res["hope_periapsis_km"], rel=1e-3) == 23389.5
    assert res["delta_orbit_radius_km"] < 80.0
    assert res["closest_flyby_observed_km"] <= 100.0


def test_martian_nonet_completeness():
    roster = MartianNonetSystem.get_roster()
    assert len(roster) == 9

    names = [m["name"] for m in roster]
    assert len(set(names)) == 9

    orbiters = [m for m in roster if m["type"] == "Orbiter"]
    rovers = [m for m in roster if m["type"] == "Rover"]
    assert len(orbiters) == 7
    assert len(rovers) == 2

    agencies = set(m["agency"] for m in roster)
    assert "NASA" in agencies
    assert "ESA" in agencies
    assert "CNSA" in agencies
    assert "UAE/MBRSC" in agencies
    assert "ESA/Roscosmos" in agencies


def test_martian_relay_network_shares():
    topo = MartianNonetSystem.get_relay_topology()
    p_shares = topo["Perseverance_downlink_shares"]
    c_shares = topo["Curiosity_downlink_shares"]

    assert pytest.approx(sum(p_shares.values()), abs=1e-4) == 1.0
    assert pytest.approx(sum(c_shares.values()), abs=1e-4) == 1.0
    assert p_shares["ExoMars_TGO"] == 0.50
    assert c_shares["MRO"] == 0.45
    assert "MAVEN" in p_shares and p_shares["MAVEN"] > 0.10


def test_grand_trigintet_fleet_and_extreme_contrasts():
    fleet = GrandTrigintetFleet.get_fleet()
    assert len(fleet) == 30

    # Monotonicity test
    dists = [p["dist_au"] for p in fleet]
    for i in range(len(dists) - 1):
        assert dists[i] >= dists[i + 1]

    assert fleet[0]["name"] == "Voyager 1"
    assert fleet[0]["dist_au"] == 173.22
    assert fleet[1]["name"] == "Voyager 2"
    assert fleet[1]["dist_au"] == 144.29
    assert fleet[-1]["name"] == "Parker Solar Probe"
    assert fleet[-1]["dist_au"] == 0.046

    contrasts = GrandTrigintetFleet.compute_extreme_contrasts()
    assert pytest.approx(contrasts["heliocentric_distance_ratio"], rel=1e-3) == 3765.65
    assert pytest.approx(contrasts["solar_flux_ratio"], rel=1e-3) == 1.4180e7
    assert contrasts["v1_light_time_hours"] > 24.0
    assert contrasts["light_time_ratio"] > 67000.0
    assert contrasts["speed_ratio"] > 2.7e7
    assert contrasts["temperature_span_k"] > 1650.0
