"""
Unit tests for STEREO-A heliospheric stereoscopy engine and The Grand Quinvigintet fleet.
"""

import math
import pytest
from datetime import datetime, timezone

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from stereo_a_heliospheric_stereoscopy_engine import (
    StereoAHeliosphericStereoscopyEngine,
    StereoAOrbitMetrics,
    FarSideEarlyWarningMetrics,
    StereoscopicTriangulation3DMetrics,
    SECCHIInstrumentSuite,
    InSituAndRadioSuite,
    GrandQuinvigintetMatrix,
    AU_KM,
    SPEED_OF_LIGHT,
    SOLAR_IRRADIANCE_1AU,
)


@pytest.fixture
def engine():
    return StereoAHeliosphericStereoscopyEngine()


def test_stereo_a_orbit_and_keplerian_dynamics(engine):
    orbit = engine.compute_orbit_and_drift_dynamics()
    assert isinstance(orbit, StereoAOrbitMetrics)
    assert orbit.semi_major_axis_au == pytest.approx(0.9624, abs=1e-4)
    assert orbit.eccentricity == pytest.approx(0.0563, abs=1e-4)
    assert orbit.inclination_deg == pytest.approx(0.12, abs=0.01)

    # 近日点与远日点
    assert orbit.perihelion_au == pytest.approx(0.9624 * (1.0 - 0.0563), abs=1e-3)
    assert orbit.aphelion_au == pytest.approx(0.9624 * (1.0 + 0.0563), abs=1e-3)

    # 公转周期开普勒第三定律
    assert 344.0 < orbit.orbital_period_days < 346.0
    assert 0.94 < orbit.orbital_period_years < 0.95

    # 差速超前漂移率
    assert 21.0 < orbit.drift_rate_deg_per_year < 21.6
    assert 0.057 < orbit.drift_rate_deg_per_day < 0.060

    # 会合大周期 ~16.9 年
    assert 16.5 < orbit.synodic_revolution_years < 17.2


def test_service_milestones_and_20th_anniversary(engine):
    orbit = engine.compute_orbit_and_drift_dynamics()
    # 2026-10-17 距 2006-10-25 发射已近 20 年
    assert orbit.days_since_launch > 7290.0
    assert orbit.years_since_launch == pytest.approx(19.98, abs=0.05)
    assert orbit.heliocentric_orbits_completed > 21.0

    # 超前地球的角度 (2023-08 掠地后累积)
    assert 65.0 < orbit.separation_angle_ahead_deg < 72.0

    # 距地球距离与光时延迟
    assert 1.05 < orbit.distance_to_earth_au < 1.15
    assert 1.55e8 < orbit.distance_to_earth_km < 1.70e8
    assert 520.0 < orbit.one_way_light_time_seconds < 570.0
    assert 8.5 < orbit.one_way_light_time_minutes < 9.5


def test_solar_flux_and_thermal_environment(engine):
    orbit = engine.compute_orbit_and_drift_dynamics()
    # 0.9624 AU 处太阳辐射能流增强 ~8%
    assert 1450.0 < orbit.solar_flux_at_stereo_w_m2 < 1485.0
    assert 1.07 < orbit.solar_flux_ratio_to_1au < 1.09


def test_far_side_early_warning_dynamics(engine):
    warning = engine.compute_far_side_early_warning()
    assert isinstance(warning, FarSideEarlyWarningMetrics)
    assert warning.solar_synodic_rotation_period_days == pytest.approx(27.275, abs=0.01)
    assert warning.solar_rotation_rate_deg_per_day == pytest.approx(13.199, abs=0.01)

    # 超前预警时间 ~5.1 天 (120+ 小时)
    assert 4.8 < warning.advance_lead_time_days < 5.5
    assert 115.0 < warning.advance_lead_time_hours < 132.0

    # 地球+STEREO-A 联合可视日面经度范围
    assert 240.0 < warning.combined_visible_longitude_span_deg < 255.0
    assert 66.0 < warning.visible_surface_fraction_percent < 71.0
    assert "提前" in warning.active_region_early_detection_capability


def test_cme_stereoscopic_triangulation_and_deprojection(engine):
    cme = engine.compute_cme_stereoscopic_triangulation(
        cme_radial_velocity_kms=1200.0,
        cme_half_angle_deg=30.0
    )
    assert isinstance(cme, StereoscopicTriangulation3DMetrics)
    assert cme.triangulation_baseline_au > 1.05
    assert cme.triangulation_baseline_km > 1.55e8

    # SOHO 单视角投影严重低估径向速度
    assert cme.soho_plane_of_sky_projected_speed_kms == pytest.approx(1200.0 * math.tan(math.radians(30.0)), abs=5.0)
    assert 40.0 < cme.soho_projection_underestimation_percent < 45.0

    # STEREO-A 侧面大张角观测到显著横向速度
    assert cme.stereo_plane_of_sky_transverse_speed_kms > 1050.0

    # 误差收敛
    assert cme.triangulation_speed_reconstruction_accuracy_percent > 95.0
    assert cme.time_of_arrival_error_reduction_hours == (12.0, 2.8)


def test_secchi_instrument_suite(engine):
    secchi = engine.get_secchi_instrument_suite()
    assert isinstance(secchi, SECCHIInstrumentSuite)
    assert len(secchi.euvi_channels) == 4
    for key in ["304A", "171A", "195A", "284A"]:
        assert key in secchi.euvi_channels
        assert "ion" in secchi.euvi_channels[key]
        assert "temp_k" in secchi.euvi_channels[key]

    assert secchi.cor1_inner_coronagraph_fov_rsun == (1.4, 4.0)
    assert secchi.cor2_outer_coronagraph_fov_rsun == (2.5, 15.0)
    assert secchi.hi1_heliospheric_imager_elongation_deg == (4.0, 24.0)
    assert secchi.hi2_heliospheric_imager_elongation_deg == (18.7, 88.7)
    assert secchi.hi2_max_heliocentric_reach_au == pytest.approx(1.0, abs=0.1)
    assert secchi.thomson_scattering_cross_section_m2 == pytest.approx(6.652e-29, rel=1e-3)


def test_insitu_and_swaves_radio_diagnostics(engine):
    insitu = engine.get_insitu_suite()
    assert isinstance(insitu, InSituAndRadioSuite)
    assert insitu.impact_magnetometer_sample_rate_hz == pytest.approx(8.0, abs=0.1)
    assert insitu.plastic_ion_energy_range_kev_e == (0.3, 80.0)
    assert insitu.swaves_radio_freq_range_mhz == (0.0025, 16.025)
    assert "Type II" in insitu.type_ii_radio_burst_diagnostic or "激波" in insitu.type_ii_radio_burst_diagnostic
    assert "Type III" in insitu.type_iii_radio_burst_diagnostic or "电子束" in insitu.type_iii_radio_burst_diagnostic


def test_grand_quinvigintet_matrix_ordering_and_completeness(engine):
    matrix = engine.build_grand_quinvigintet_matrix()
    assert isinstance(matrix, GrandQuinvigintetMatrix)
    assert matrix.total_fleet_count == 25
    assert len(matrix.vessels) == 25

    # 严格降序排列验证
    for i in range(len(matrix.vessels) - 1):
        assert matrix.vessels[i].heliocentric_distance_au >= matrix.vessels[i + 1].heliocentric_distance_au

    # 极值旗舰核实
    assert matrix.vessels[0].rank == 1
    assert matrix.vessels[0].name == "Voyager 1"
    assert matrix.vessels[0].heliocentric_distance_au == pytest.approx(173.22, abs=0.1)

    assert matrix.vessels[-1].rank == 25
    assert matrix.vessels[-1].name == "Parker Solar Probe"
    assert matrix.vessels[-1].heliocentric_distance_au == pytest.approx(0.046, abs=0.005)

    # STEREO-A 位于第 22 位 (0.9624 AU)
    assert matrix.vessels[21].name == "STEREO-A"
    assert matrix.vessels[21].rank == 22
    assert matrix.vessels[21].heliocentric_distance_au == pytest.approx(0.9624, abs=0.01)

    # 内日球层立体网监测探测器数量
    assert matrix.inner_solar_observing_fleet_count == 5


def test_grand_quinvigintet_physical_extremes(engine):
    matrix = engine.build_grand_quinvigintet_matrix()
    assert matrix.heliocentric_span_ratio > 3700.0
    assert matrix.solar_flux_span_ratio > 1.4e7
    assert matrix.geocentric_distance_span_ratio > 67000.0
    assert matrix.light_time_span_ratio > 67000.0
    assert matrix.speed_span_ratio > 2.5e7


def test_exact_twentieth_anniversary_epoch():
    from datetime import datetime, timezone
    from stereo_a_heliospheric_stereoscopy_engine import StereoAHeliosphericStereoscopyEngine
    engine_20 = StereoAHeliosphericStereoscopyEngine(
        observation_time=datetime(2026, 10, 25, 0, 52, 0, tzinfo=timezone.utc)
    )
    orbit = engine_20.compute_orbit_and_drift_dynamics()
    assert orbit.years_since_launch == pytest.approx(20.00, abs=1e-3)
    assert orbit.days_since_launch == pytest.approx(7305.00, abs=1e-2)
    assert 21.15 < orbit.heliocentric_orbits_completed < 21.20
    assert 68.10 < orbit.separation_angle_ahead_deg < 68.30
    assert 1.09 < orbit.distance_to_earth_au < 1.11
    assert 9.0 < orbit.one_way_light_time_minutes < 9.3

    warning = engine_20.compute_far_side_early_warning()
    assert 5.10 < warning.advance_lead_time_days < 5.25
    assert 68.5 < warning.visible_surface_fraction_percent < 69.5
