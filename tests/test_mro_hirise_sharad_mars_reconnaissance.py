"""
Unit tests for MRO Mars Reconnaissance Orbiter Engine and Grand Trevigintet 23-Pillar Fleet.
Author: Hoshi
Date: 2026-10-17
"""

import sys
from pathlib import Path
import pytest
import math

scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from mro_hirise_sharad_mars_reconnaissance_engine import (
    MROMarsReconnaissanceEngine,
    PSO_PERIAPSIS_ALT_KM,
    PSO_APOAPSIS_ALT_KM,
    PSO_INCLINATION_DEG,
    HIRISE_APERTURE_M,
    HIRISE_FOCAL_LENGTH_M,
    SHARAD_CENTER_FREQ_MHZ,
    WATER_ICE_RELATIVE_PERMITTIVITY,
    ELECTRA_MAX_DATA_RATE_KBPS
)


@pytest.fixture
def engine():
    return MROMarsReconnaissanceEngine()


def test_mission_duration_twenty_year_milestone(engine):
    """Verify MRO exceeds 20 years, 7,500 days in orbit, and 95,000 revolutions."""
    metrics = engine.calculate_mission_duration_metrics()
    assert metrics["days_in_mars_orbit"] > 7500.0
    assert metrics["earth_years_in_orbit"] >= 20.6
    assert metrics["mars_years_in_orbit"] > 10.9
    assert metrics["total_orbits_completed"] > 95000
    assert metrics["extended_mission_factor"] >= 10.0
    assert "20th Anniversary" in metrics["anniversary_milestone"]


def test_orbital_mechanics_frozen_sun_synchronous(engine):
    """Verify orbital parameters, period, and orbital speeds in Mars frame."""
    orbit = engine.compute_orbital_mechanics()
    assert orbit["periapsis_radius_km"] == pytest.approx(3644.5, abs=0.1)
    assert orbit["apoapsis_radius_km"] == pytest.approx(3709.5, abs=0.1)
    assert orbit["semi_major_axis_km"] == pytest.approx(3677.0, abs=0.1)
    assert 0.008 < orbit["eccentricity"] < 0.010

    # Period around 112.8 minutes
    assert 112.0 < orbit["orbital_period_minutes"] < 113.5
    # Orbits per day
    assert 12.5 < orbit["orbits_per_earth_day"] < 13.0
    assert 13.0 < orbit["orbits_per_mars_sol"] < 13.2

    # Speeds between 3.36 and 3.43 km/s
    assert 3.42 < orbit["periapsis_velocity_km_s"] < 3.46
    assert 3.36 < orbit["apoapsis_velocity_km_s"] < 3.40
    assert 3.40 < orbit["mean_orbital_velocity_km_s"] < 3.42


def test_nodal_precession_j2_synchrony(engine):
    """Verify first-order J2 nodal precession matches Mars solar year to ~0.2 degrees."""
    orbit = engine.compute_orbital_mechanics()
    assert orbit["sun_sync_precession_deg_per_day"] == pytest.approx(0.52403, abs=0.001)
    assert abs(orbit["inclination_analytical_deg"] - orbit["inclination_actual_deg"]) < 0.35
    assert "15:00 LMST" in orbit["local_solar_time_ascending_node"]


def test_hirise_optical_resolutions_and_gsd(engine):
    """Verify HiRISE 1.0 microradian IFOV and 30 cm/pixel ground sampling distance."""
    hirise = engine.compute_hirise_optics_physics()
    assert hirise["ifov_microradians"] == pytest.approx(1.00, abs=0.01)
    assert hirise["ifov_arcseconds"] == pytest.approx(0.2063, abs=0.005)

    # GSD ranges from 25.5 cm at periapsis to 32.0 cm at apoapsis
    assert hirise["gsd_periapsis_cm"] == pytest.approx(25.5, abs=0.5)
    assert hirise["gsd_mean_cm"] == pytest.approx(28.75, abs=0.5)
    assert hirise["gsd_apoapsis_cm"] == pytest.approx(32.0, abs=0.5)


def test_hirise_diffraction_and_swath(engine):
    """Verify optical diffraction, swath width ~5.89 km, and TDI line scan rate."""
    hirise = engine.compute_hirise_optics_physics()
    assert 0.34 < hirise["airy_radius_arcsec"] < 0.36
    assert 40.0 < hirise["airy_disk_diameter_focal_plane_um"] < 42.0
    assert 5.5 < hirise["swath_width_mean_km"] < 6.2
    assert 10000.0 < hirise["line_rate_hz"] < 12000.0
    assert 80.0 < hirise["line_integration_time_us"] < 100.0


def test_sharad_radar_dielectric_penetration(engine):
    """Verify SHARAD free space and subsurface radar resolution in ice and regolith."""
    sharad = engine.compute_sharad_subsurface_radar()
    assert sharad["free_space_wavelength_m"] == pytest.approx(14.99, abs=0.05)
    assert sharad["free_space_resolution_m"] == pytest.approx(14.99, abs=0.05)
    assert sharad["ice_refractive_index"] == pytest.approx(1.7748, abs=0.005)
    assert sharad["vertical_resolution_in_ice_m"] == pytest.approx(8.45, abs=0.1)
    assert sharad["vertical_resolution_in_regolith_m"] == pytest.approx(6.39, abs=0.4)
    assert 5.8 < sharad["twtt_500m_ice_microseconds"] < 6.0
    assert sharad["max_penetration_ice_m"] >= 1000.0


def test_sharad_utopia_planitia_water_ice_volume(engine):
    """Verify Utopia Planitia ice volume exceeds Lake Superior."""
    sharad = engine.compute_sharad_subsurface_radar()
    assert sharad["utopia_planitia_ice_volume_km3"] == 14300.0
    assert sharad["ratio_to_lake_superior"] > 1.15


def test_telecom_xband_gain_and_electra_throughput(engine):
    """Verify X-band 3m HGA gain >46 dBi, Electra throughput, and 450+ Tbit volume."""
    telecom = engine.compute_telecommunications_architecture()
    assert 46.0 < telecom["x_band_gain_dbi"] < 46.5
    assert 66.0 < telecom["eirp_dbw"] < 66.5
    assert telecom["electra_max_rate_kbps"] == 2048.0
    assert telecom["electra_single_pass_capacity_mb"] > 150.0  # >150 MB per 10-min pass
    assert telecom["cumulative_data_returned_tbits"] >= 450.0
    assert telecom["cumulative_data_returned_terabytes"] > 56.0


def test_grand_trevigintet_twenty_three_pillars(engine):
    """Verify the 23-pillar fleet structure, Mars Quaternity count, and extreme physical span."""
    fleet = engine.evaluate_grand_trevigintet_fleet()
    assert fleet["fleet_size"] == 23
    assert "Trevigintet" in fleet["designation"]
    assert "二十三极" in fleet["designation"]
    assert fleet["mars_quaternity_count"] == 4
    assert fleet["heliocentric_distance_ratio"] > 3700.0
    assert fleet["solar_radiation_flux_ratio_millions"] > 14.0
    assert fleet["voyager2_countdown_hours"] <= 13.0
