"""
BepiColombo 8th Launch Anniversary (八周年整) & OSIRIS-REx Bennu TAG 6th Anniversary (六周年整)
Celestial Mechanics & 2026 Orionids 24-Hour Countdown Engine.
========================================================================================

Covers:
1. BepiColombo: 8.00 Julian years in space (2018-10-20 to 2026-10-20), 9.9 billion km journey,
   9 planetary flybys (1 Earth, 2 Venus, 6 Mercury), MTM jettison efficiency gain,
   and Mercury Orbit Insertion (MOI) countdown (32 days to 2026-11-21).
2. Gravity assist delta-V dissipation: v_inf reduced from 9.61 km/s to 1.84 km/s,
   saving >6,000 m/s in capture propellant.
3. Dual-orbiter post-capture decoupling: ESA MPO (480x1500 km) & JAXA Mio (590x11640 km).
4. OSIRIS-REx Bennu TAG 6th Anniversary: 2020-10-20 22:12 UTC contact dynamics,
   121.6g sample collection, and OSIRIS-APEX 0.50 AU fig-leaf thermal defense en route to Apophis 2029.
5. Orionids 2026 24-hour countdown: peak window 2026-10-21 23:00 - 10-22 02:00 CST,
   66 km/s Halley dust stream, and moonset dark-sky window mechanics.
"""

import math
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List

# ---------------------------------------------------------
# Astrodynamical & Physical Constants (IAU / CODATA 2018)
# ---------------------------------------------------------
SPEED_OF_LIGHT = 299792.458               # km/s
AU_KM = 149597870.7                       # 1 AU in km
MU_SUN = 1.32712440018e11                 # Sun GM, km^3/s^2
MU_EARTH = 3.986004418e5                  # Earth GM, km^3/s^2
MU_MERCURY = 22032.09                     # Mercury GM, km^3/s^2
MERCURY_RADIUS_KM = 2439.7                # Mercury equatorial radius, km
SOLAR_CONSTANT_1AU = 1361.0               # W/m^2

# ---------------------------------------------------------
# Key Mission Epochs
# ---------------------------------------------------------
BEPI_LAUNCH_UTC = datetime(2018, 10, 20, 1, 45, 28, tzinfo=timezone.utc)
BEPI_MTM_SEP_UTC = datetime(2026, 9, 3, 14, 0, 0, tzinfo=timezone.utc)
BEPI_MPO_TCM_UTC = datetime(2026, 9, 24, 8, 42, 0, tzinfo=timezone.utc)
BEPI_MOI_UTC = datetime(2026, 11, 21, 0, 0, 0, tzinfo=timezone.utc)
BEPI_MIO_SEP_UTC = datetime(2026, 12, 10, 0, 0, 0, tzinfo=timezone.utc)
BEPI_SCIENCE_START_UTC = datetime(2027, 4, 1, 0, 0, 0, tzinfo=timezone.utc)

OSIRIS_TAG_UTC = datetime(2020, 10, 20, 22, 12, 0, tzinfo=timezone.utc)
OSIRIS_SRC_LAND_UTC = datetime(2023, 9, 24, 14, 52, 0, tzinfo=timezone.utc)
APOPHIS_RENDEZVOUS_UTC = datetime(2029, 4, 23, 0, 0, 0, tzinfo=timezone.utc)

ORIONIDS_PEAK_START_CST = datetime(2026, 10, 21, 23, 0, 0, tzinfo=timezone(timedelta(hours=8)))
ORIONIDS_PEAK_END_CST = datetime(2026, 10, 22, 2, 0, 0, tzinfo=timezone(timedelta(hours=8)))


def get_bepicolombo_octennial_status(ref_utc: datetime = None) -> Dict[str, Any]:
    """
    Computes precise timeline and status for BepiColombo on its 8th launch anniversary.
    """
    if ref_utc is None:
        ref_utc = datetime(2026, 10, 20, 3, 5, 0, tzinfo=timezone.utc)

    elapsed_since_launch = (ref_utc - BEPI_LAUNCH_UTC).total_seconds() / 86400.0
    julian_years = elapsed_since_launch / 365.25
    elapsed_since_mtm_sep = (ref_utc - BEPI_MTM_SEP_UTC).total_seconds() / 86400.0
    days_to_moi = (BEPI_MOI_UTC - ref_utc).total_seconds() / 86400.0
    days_to_mio_sep = (BEPI_MIO_SEP_UTC - ref_utc).total_seconds() / 86400.0

    # Stack masses
    mass_launch = 4121.0        # kg
    mass_mtm = 1861.0           # kg
    mass_post_sep = 2260.0      # kg (MPO 1760kg + Mio 285kg + MOSIF 215kg)
    thrust_weight_mult = mass_launch / mass_post_sep

    return {
        "mission_name": "BepiColombo (ESA / JAXA)",
        "launch_utc": BEPI_LAUNCH_UTC.isoformat(),
        "ref_utc": ref_utc.isoformat(),
        "days_since_launch": round(elapsed_since_launch, 2),
        "julian_years_since_launch": round(julian_years, 3),
        "is_8th_anniversary": abs(julian_years - 8.00) < 0.01,
        "days_since_mtm_sep": round(elapsed_since_mtm_sep, 2),
        "days_to_moi": round(days_to_moi, 2),
        "days_to_mio_sep": round(days_to_mio_sep, 2),
        "total_flybys": 9,
        "earth_flybys": 1,
        "venus_flybys": 2,
        "mercury_flybys": 6,
        "launch_mass_kg": mass_launch,
        "jettisoned_mtm_mass_kg": mass_mtm,
        "post_sep_stack_mass_kg": mass_post_sep,
        "thrust_to_mass_amplification": round(thrust_weight_mult, 3),
        "post_sep_tcm_dv_ms": 11.4,
        "post_sep_tcm_duration_s": 522.0,  # 8m42s
    }


def compute_bepicolombo_orbital_insertion_mechanics(
    v_inf_kms: float = 1.84,
    periapsis_alt_km: float = 480.0,
    initial_apoapsis_km: float = 178000.0,
    direct_hohmann_v_inf_kms: float = 9.61
) -> Dict[str, Any]:
    """
    Computes ballistic capture kinematics and delta-V savings from gravity assist dissipation.
    """
    r_p = MERCURY_RADIUS_KM + periapsis_alt_km
    v_esc_p = math.sqrt(2.0 * MU_MERCURY / r_p)
    v_hyp_p = math.sqrt(v_inf_kms ** 2 + v_esc_p ** 2)

    # Initial capture orbit (apocentre near sphere of influence boundary)
    a_cap = (r_p + initial_apoapsis_km) / 2.0
    v_cap_p = math.sqrt(MU_MERCURY * (2.0 / r_p - 1.0 / a_cap))
    delta_v_cap = v_hyp_p - v_cap_p

    # Theoretical direct transfer without gravity assists
    v_hyp_direct = math.sqrt(direct_hohmann_v_inf_kms ** 2 + v_esc_p ** 2)
    delta_v_direct = v_hyp_direct - v_cap_p
    delta_v_saved = delta_v_direct - delta_v_cap

    # Final orbit parameters
    # ESA MPO: 480 x 1500 km, period = 2.32 hours
    r_p_mpo = MERCURY_RADIUS_KM + 480.0
    r_a_mpo = MERCURY_RADIUS_KM + 1500.0
    a_mpo = (r_p_mpo + r_a_mpo) / 2.0
    period_mpo_s = 2.0 * math.pi * math.sqrt(a_mpo ** 3 / MU_MERCURY)

    # JAXA Mio: 590 x 11640 km, period = 9.32 hours
    r_p_mio = MERCURY_RADIUS_KM + 590.0
    r_a_mio = MERCURY_RADIUS_KM + 11640.0
    a_mio = (r_p_mio + r_a_mio) / 2.0
    period_mio_s = 2.0 * math.pi * math.sqrt(a_mio ** 3 / MU_MERCURY)

    return {
        "periapsis_radius_km": round(r_p, 1),
        "v_escape_periapsis_kms": round(v_esc_p, 3),
        "v_hyperbolic_periapsis_kms": round(v_hyp_p, 3),
        "v_capture_periapsis_kms": round(v_cap_p, 3),
        "delta_v_capture_ms": round(delta_v_cap * 1000.0, 1),
        "delta_v_direct_hohmann_ms": round(delta_v_direct * 1000.0, 1),
        "delta_v_saved_ms": round(delta_v_saved * 1000.0, 1),
        "gravity_assist_savings_percent": round(delta_v_saved / delta_v_direct * 100.0, 1),
        "mpo_period_hours": round(period_mpo_s / 3600.0, 2),
        "mio_period_hours": round(period_mio_s / 3600.0, 2),
    }


def get_osiris_tag_sexennial_status(ref_utc: datetime = None) -> Dict[str, Any]:
    """
    Computes status and parameters for OSIRIS-REx on the 6th anniversary of Bennu TAG.
    """
    if ref_utc is None:
        ref_utc = datetime(2026, 10, 20, 3, 5, 0, tzinfo=timezone.utc)

    elapsed_since_tag = (ref_utc - OSIRIS_TAG_UTC).total_seconds() / 86400.0
    julian_years = elapsed_since_tag / 365.25
    days_to_apophis = (APOPHIS_RENDEZVOUS_UTC - ref_utc).total_seconds() / 86400.0

    # Solar flux at 0.50 AU perihelion during APEX cruise
    perihelion_au = 0.500
    solar_flux_peri = SOLAR_CONSTANT_1AU / (perihelion_au ** 2)

    return {
        "event_name": "OSIRIS-REx Touch-And-Go (TAG) at Asteroid Bennu",
        "tag_utc": OSIRIS_TAG_UTC.isoformat(),
        "days_since_tag": round(elapsed_since_tag, 2),
        "julian_years_since_tag": round(julian_years, 3),
        "is_6th_anniversary": abs(julian_years - 6.00) < 0.01,
        "sample_mass_collected_grams": 121.6,
        "sample_target_grams": 60.0,
        "sample_return_earth_utc": OSIRIS_SRC_LAND_UTC.isoformat(),
        "extended_mission_name": "OSIRIS-APEX (Apophis Explorer)",
        "target_asteroid": "(99942) Apophis",
        "days_to_apophis_rendezvous": round(days_to_apophis, 1),
        "perihelion_solar_flux_wm2": round(solar_flux_peri, 1),
        "flux_ratio_to_earth": round(1.0 / (perihelion_au ** 2), 1),
        "thermal_defense_attitude": "Lockheed Martin 'fig-leaf' solar panel sunshade",
    }


def get_orionids_2026_countdown_status(ref_cst: datetime = None) -> Dict[str, Any]:
    """
    Computes countdown and celestial viewing window for 2026 Orionids meteor shower.
    """
    if ref_cst is None:
        ref_cst = datetime(2026, 10, 20, 3, 5, 0, tzinfo=timezone(timedelta(hours=8)))

    hours_to_peak_start = (ORIONIDS_PEAK_START_CST - ref_cst).total_seconds() / 3600.0

    return {
        "shower_name": "2026 Orionids (猎户座流星雨)",
        "parent_comet": "1P/Halley (哈雷彗星)",
        "geocentric_velocity_kms": 66.0,
        "hours_to_peak_window": round(hours_to_peak_start, 1),
        "days_to_peak": round(hours_to_peak_start / 24.0, 2),
        "peak_window_cst": "2026-10-21 23:00 至 10-22 02:00 CST",
        "dark_sky_window_hours": 2.9,
        "oct20_moon_illum_percent": 68.3,
        "oct20_moonset_cst": "2026-10-21 00:48 CST",
        "oct21_moon_illum_percent": 77.0,
        "oct21_moonset_cst": "2026-10-22 01:46 CST",
    }
