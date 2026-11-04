import sys
from pathlib import Path
import pytest

DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR / "scripts"))

from lunar_orbiter2_diamond_jubilee_engine import LunarOrbiter2DiamondJubileeEngine

@pytest.fixture
def lo2_engine():
    return LunarOrbiter2DiamondJubileeEngine()

def test_orbital_dynamics_initial_and_photo(lo2_engine):
    res = lo2_engine.compute_orbital_dynamics()
    assert res["anniversary_years"] == 60
    assert "Diamond Jubilee" in res["jubilee_name"]
    assert res["dry_mass_kg"] == 385.6
    
    # Initial orbit
    init = res["initial_capture_orbit"]
    assert init["perilune_alt_km"] == 196.3
    assert init["apolune_alt_km"] == 1850.0
    assert 2750.0 < init["semi_major_axis_km"] < 2770.0
    assert 0.29 < init["eccentricity"] < 0.31
    assert 210.0 < init["period_min"] < 220.0
    assert 1800.0 < init["perilune_velocity_m_s"] < 1830.0

    # Photo reconnaissance orbit
    photo = res["photo_orbit"]
    assert photo["perilune_alt_km"] == 45.1
    assert photo["apolune_alt_km"] == 1843.0
    assert 2670.0 < photo["semi_major_axis_km"] < 2690.0
    assert 0.33 < photo["eccentricity"] < 0.34
    assert 205.0 < photo["period_min"] < 210.0
    assert photo["perilune_velocity_m_s"] > 1900.0
    assert photo["apolune_velocity_m_s"] < 960.0

    # LOI burn
    loi = res["loi_maneuver"]
    assert loi["actual_marquardt_delta_v_m_s"] == 829.7
    assert loi["actual_marquardt_burn_duration_s"] == 611.6
    assert loi["engine_thrust_n"] == 445.0

def test_photographic_and_imc_physics(lo2_engine):
    res = lo2_engine.compute_photographic_and_imc_physics()
    
    # Paxar High Resolution Lens
    paxar = res["high_resolution_paxar"]
    assert paxar["focal_length_mm"] == 610.0
    assert 108.0 < paxar["clear_aperture_mm"] < 110.0
    assert 1.2 < paxar["diffraction_limit_arcsec"] < 1.35
    assert paxar["diffraction_ground_resolution_m"] < 0.30
    assert paxar["film_emulsion_ground_resolution_m"] < 0.35
    assert paxar["practical_readout_resolution_m"] == 1.0
    assert 5.0 < paxar["field_of_view_deg"] < 5.3

    # Xenotar Medium Resolution Lens
    xenotar = res["medium_resolution_xenotar"]
    assert xenotar["focal_length_mm"] == 80.0
    assert 28.0 < xenotar["clear_aperture_mm"] < 29.0
    assert 36.0 < xenotar["field_of_view_deg"] < 40.0
    assert 8.0 < xenotar["ground_resolution_m"] < 9.0

    # Image Motion Compensation (IMC)
    imc = res["image_motion_compensation_imc"]
    assert 2.3 < imc["ground_angular_rate_deg_s"] < 2.6
    assert 25.0 < imc["platen_speed_hr_mm_s"] < 27.0
    assert imc["uncompensated_ground_smear_m"] > 70.0
    assert imc["uncompensated_film_smear_mm"] > 1.0
    assert imc["smear_to_grain_blur_factor"] > 250.0
    assert imc["residual_film_smear_microns"] <= 3.0
    assert imc["residual_ground_smear_m"] < 0.25

def test_copernicus_picture_of_century_geometry(lo2_engine):
    res = lo2_engine.compute_copernicus_picture_of_century_geometry()
    assert "Picture of the Century" in res["photo_title"]
    assert res["orbit_number"] == 52
    assert res["capture_utc"] == "1966-11-23 00:05:42"
    
    cop = res["copernicus_crater"]
    assert cop["diameter_km"] == 93.0
    assert cop["rim_wall_depth_km"] == 3.8
    assert cop["central_peaks_height_km"] == 1.2
    
    geom = res["viewing_geometry"]
    assert geom["spacecraft_roll_angle_deg"] == 17.0
    assert 370.0 < geom["slant_range_to_rim_km"] < 400.0
    assert 6.0 < geom["grazing_perspective_angle_deg"] < 8.0
    assert 10.0 < geom["central_peak_angular_height_arcmin"] < 12.0

def test_bimat_and_telemetry(lo2_engine):
    res = lo2_engine.compute_bimat_and_telemetry()
    
    chem = res["chemical_processing"]
    assert chem["film_stock"].startswith("Kodak SO-243")
    assert chem["film_capacity_meters"] == 80.0
    assert chem["bimat_reagent_web_meters"] == 79.0
    assert 29.0 <= chem["process_temperature_c"] <= 30.0
    
    fss = res["flying_spot_scanner"]
    assert fss["electron_beam_diameter_microns"] == 5.0
    assert fss["framelet_width_mm"] == 2.68
    assert fss["effective_scan_density_lines_per_mm"] == 287.0
    assert fss["framelets_per_telephoto_frame"] == 117
    
    s_band = res["s_band_downlink"]
    assert s_band["carrier_frequency_ghz"] == 2.295
    assert s_band["twta_rf_power_watts"] == 10.0
    assert s_band["readout_time_per_framelet_s"] == 42.0
    
    out = res["reconnaissance_output"]
    assert out["dual_frame_exposures"] == 211
    assert out["total_individual_images"] == 422
    assert out["primary_apollo_sites_covered"] == 13
    assert "Mare Tranquillitatis" in out["apollo_11_site_verified"]

def test_mascon_gravitational_perturbation(lo2_engine):
    res = lo2_engine.compute_mascon_gravitational_perturbation()
    dop = res["doppler_tracking_perturbation"]
    assert dop["doppler_residual_peak_mm_s"] == 12.0
    assert dop["gravity_anomaly_mgal"] == 125.0
    assert 5e16 < dop["estimated_excess_mass_kg"] < 5e17
    assert "Muller & Sjogren" in dop["discovery_by"]
    assert "Mare Imbrium" in dop["target_basin"]

def test_exploration_continuum(lo2_engine):
    res = lo2_engine.compute_exploration_continuum()
    assert "mariner_3_1964" in res
    assert "luna_12_1966" in res
    assert "lunar_orbiter_2_1966" in res
    assert "change_1_2007" in res
    assert "mangalyaan_2013" in res
    assert "voyager_2_2018" in res
    
    # Assert specific historical milestones
    assert res["luna_12_1966"]["diamond_jubilee"] == 60
    assert res["lunar_orbiter_2_1966"]["diamond_jubilee"] == 60
    assert res["change_1_2007"]["anniversary_years"] == 19
    assert res["mangalyaan_2013"]["anniversary_years"] == 13
    assert res["voyager_2_2018"]["anniversary_years"] == 8
    assert res["voyager_2_2018"]["crossing_distance_au"] == 119.7
    assert res["voyager_2_2018"]["one_way_light_time_hours"] > 20.0
