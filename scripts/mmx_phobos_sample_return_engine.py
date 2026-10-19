"""
MMX (Martian Moons eXploration) Mars Moon Phobos Sample-Return Astrodynamics Engine.
===================================================================================

Covers:
1. MMX Historic Launch on 2026-10-20 04:41:03 JST (03:41:03 CST / 19:41:03 UTC Oct 19)
   from Tanegashima LA-Y2 on H3-24L (F10) with 4,480 kg wet launch mass.
2. Spacecraft separation & Trans-Mars Injection (TMI) at 05:53 JST (04:53 CST).
3. Mars Transfer & Orbital Mechanics: 10-month cruise, Mars Orbit Insertion (MOI) in Aug 2027.
4. Quasi-Satellite Orbit (QSO) around Phobos: Hill-Clohessy-Wiltshire (HCW) 2:1 ellipse,
   Hill sphere boundary constraint (r_Hill ~ 16.6 km vs R_phobos ~ 11.1 km),
   three-tiered QSO altitude strategy (QSO-H 100km, QSO-M 50km, QSO-L 20km).
5. IDEFIX 25 kg microgravity rover dynamics: Phobos surface gravity ~0.0057 m/s^2 (1/1720 g),
   surface weight ~0.1425 N, cm/s creeping velocity to prevent ballistic bouncing.
6. Dual sampling mechanism (Pneumatic gas-lift + Corer) targeting >= 10 grams of regolith.
7. Ancient Martian impact ejecta accumulation model (~0.5% mass fraction, ~50 mg Mars material).
8. Earth Re-entry Capsule (ERC) hyperbolic atmospheric return at Woomera, Australia in 2031.
"""

import math
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List

# ---------------------------------------------------------
# Astrodynamical & Planetary Constants (IAU / NASA PDS)
# ---------------------------------------------------------
SPEED_OF_LIGHT = 299792.458               # km/s
AU_KM = 149597870.7                       # 1 AU in km
G_CONST = 6.67430e-11                     # m^3 / (kg * s^2)

# Mars System Constants
MU_MARS = 42828.375                       # Mars GM, km^3 / s^2
MARS_RADIUS_EQUAT_KM = 3396.2             # km
MARS_RADIUS_MEAN_KM = 3389.5              # km
MARS_MASS_KG = 6.4171e23                  # kg
MARS_SURFACE_G = 3.72076                  # m / s^2
MARS_ESCAPE_VEL_KMS = 5.027               # km / s

# Phobos Constants
PHOBOS_A_KM = 13.4                        # Triaxial semi-axis a, km
PHOBOS_B_KM = 11.2                        # Triaxial semi-axis b, km
PHOBOS_C_KM = 9.2                         # Triaxial semi-axis c, km
PHOBOS_MEAN_RADIUS_KM = 11.1              # Mean volumetric radius, km
PHOBOS_MASS_KG = 1.0659e16                # kg
MU_PHOBOS = 7.112e-4                      # Phobos GM, km^3 / s^2 (711,200 m^3/s^2)
PHOBOS_ORBIT_A_KM = 9376.0                # Semi-major axis around Mars, km
PHOBOS_ORBIT_ECC = 0.0151                 # Orbital eccentricity
PHOBOS_ORBIT_INC_DEG = 1.075              # Orbital inclination to Mars equator, deg
PHOBOS_PERIOD_HOURS = 7.6538              # Orbital period (7h 39m 14s)
PHOBOS_SURFACE_G_MS2 = 0.0057             # Mean surface gravity, m / s^2 (approx 1/1720 of Earth)
PHOBOS_ESCAPE_VEL_MS = 11.39              # Surface escape velocity, m / s

# Earth Constants
MU_EARTH = 3.986004418e5                  # Earth GM, km^3 / s^2
EARTH_SURFACE_G = 9.80665                 # m / s^2

# ---------------------------------------------------------
# MMX Mission Milestone Epochs
# ---------------------------------------------------------
# Launch: 2026-10-20 04:41:03 JST = 2026-10-20 03:41:03 CST = 2026-10-19 19:41:03 UTC
MMX_LAUNCH_UTC = datetime(2026, 10, 19, 19, 41, 3, tzinfo=timezone.utc)
# Spacecraft separation: 2026-10-20 05:53:00 JST = 2026-10-20 04:53:00 CST = 2026-10-19 20:53:00 UTC
MMX_SEP_UTC = datetime(2026, 10, 19, 20, 53, 0, tzinfo=timezone.utc)

# Expected Target Milestones
MMX_MARS_ARRIVAL_UTC = datetime(2027, 8, 15, 12, 0, 0, tzinfo=timezone.utc)
MMX_QSO_ENTRY_UTC = datetime(2027, 9, 20, 0, 0, 0, tzinfo=timezone.utc)
MMX_IDEFIX_DEPLOY_UTC = datetime(2029, 1, 15, 0, 0, 0, tzinfo=timezone.utc)
MMX_SAMPLING_PRIMARY_UTC = datetime(2030, 2, 10, 0, 0, 0, tzinfo=timezone.utc)
MMX_MARS_DEPARTURE_UTC = datetime(2030, 8, 25, 0, 0, 0, tzinfo=timezone.utc)
MMX_EARTH_RETURN_UTC = datetime(2031, 7, 20, 0, 0, 0, tzinfo=timezone.utc)


def get_mmx_mission_status(ref_utc: datetime = None) -> Dict[str, Any]:
    """
    Returns real-time operational flight status of MMX following launch.
    """
    if ref_utc is None:
        ref_utc = datetime(2026, 10, 19, 23, 20, 0, tzinfo=timezone.utc)

    elapsed_launch_s = (ref_utc - MMX_LAUNCH_UTC).total_seconds()
    is_launched = elapsed_launch_s >= 0
    is_separated = (ref_utc - MMX_SEP_UTC).total_seconds() >= 0

    days_to_mars = (MMX_MARS_ARRIVAL_UTC - ref_utc).total_seconds() / 86400.0
    days_to_qso = (MMX_QSO_ENTRY_UTC - ref_utc).total_seconds() / 86400.0
    days_to_earth_return = (MMX_EARTH_RETURN_UTC - ref_utc).total_seconds() / 86400.0

    # Stack mass properties
    wet_launch_mass_kg = 4480.0
    propellant_mass_kg = 2100.0
    dry_mass_kg = wet_launch_mass_kg - propellant_mass_kg
    idefix_rover_mass_kg = 25.0
    sample_target_min_grams = 10.0

    return {
        "mission_name": "MMX (Martian Moons eXploration - JAXA / NASA / CNES / DLR / ESA)",
        "launch_vehicle": "H3-24L (Flight No. 10)",
        "launch_site": "Tanegashima Space Center, Yoshinobu Complex LA-Y2",
        "launch_utc": MMX_LAUNCH_UTC.isoformat(),
        "separation_utc": MMX_SEP_UTC.isoformat(),
        "ref_utc": ref_utc.isoformat(),
        "is_launched": is_launched,
        "is_separated": is_separated,
        "hours_since_launch": round(elapsed_launch_s / 3600.0, 3) if is_launched else 0.0,
        "hours_since_separation": round((ref_utc - MMX_SEP_UTC).total_seconds() / 3600.0, 3) if is_separated else 0.0,
        "current_flight_phase": "Trans-Mars Injection (TMI) & Earth Escape Coast" if is_separated else "Ascent / Upper Stage Coast",
        "days_to_mars_arrival": round(days_to_mars, 1),
        "days_to_qso_entry": round(days_to_qso, 1),
        "days_to_earth_return": round(days_to_earth_return, 1),
        "wet_launch_mass_kg": wet_launch_mass_kg,
        "propellant_mass_kg": propellant_mass_kg,
        "dry_mass_kg": dry_mass_kg,
        "idefix_rover_mass_kg": idefix_rover_mass_kg,
        "sample_target_min_grams": sample_target_min_grams,
        "target_celestial_body": "Phobos (Mars I)",
        "secondary_target": "Deimos (Mars II)",
    }


def compute_phobos_hill_sphere_and_qso_mechanics(
    r_orbit_km: float = PHOBOS_ORBIT_A_KM,
    m_phobos: float = PHOBOS_MASS_KG,
    m_mars: float = MARS_MASS_KG
) -> Dict[str, Any]:
    """
    Computes Phobos' Hill sphere radius, Roche limit, and Quasi-Satellite Orbit (QSO) parameters.
    Demonstrates why traditional Keplerian circular orbits around Phobos are impossible
    and why QSO (2:1 relative epicycle) is required.
    """
    # 1. Hill sphere radius: r_H = a * (m_phobos / (3 * m_mars))^(1/3)
    mass_ratio = m_phobos / (3.0 * m_mars)
    r_hill_km = r_orbit_km * (mass_ratio ** (1.0 / 3.0))

    # Margin between Hill sphere and physical surface
    clearance_mean_km = r_hill_km - PHOBOS_MEAN_RADIUS_KM
    clearance_long_axis_km = r_hill_km - PHOBOS_A_KM

    # 2. Mars Roche Limit for Phobos (fluid vs rigid)
    # Rigid Roche limit: d = R_mars * (2 * rho_mars / rho_phobos)^(1/3)
    # Phobos mean density: ~1876 kg/m^3, Mars mean density: ~3933 kg/m^3
    rho_mars = m_mars / (4.0 / 3.0 * math.pi * ((MARS_RADIUS_MEAN_KM * 1000.0) ** 3))
    rho_phobos = m_phobos / (4.0 / 3.0 * math.pi * ((PHOBOS_MEAN_RADIUS_KM * 1000.0) ** 3))
    density_ratio = rho_mars / rho_phobos
    roche_rigid_km = MARS_RADIUS_MEAN_KM * ((2.0 * density_ratio) ** (1.0 / 3.0))
    roche_fluid_km = 2.44 * MARS_RADIUS_MEAN_KM * (density_ratio ** (1.0 / 3.0))

    # Orbital decay: Phobos orbits Mars inside synchronous orbit radius
    # Mars sidereal day = 24.6229 hours
    mars_sync_radius_km = ((MU_MARS * ((24.6229 * 3600.0) / (2.0 * math.pi)) ** 2) ** (1.0 / 3.0))
    is_inside_sync = r_orbit_km < mars_sync_radius_km

    # 3. QSO Tiers & Epicycle Geometry
    # In Hill-Clohessy-Wiltshire (HCW) relative frame, QSO motion satisfies:
    # x(t) = A * cos(n * t + phi) (Radial: Mars-Phobos axis)
    # y(t) = -2 * A * sin(n * t + phi) (Along-track: Phobos velocity direction)
    # z(t) = B * cos(n * t + psi) (Cross-track: Out-of-plane)
    # Thus the trajectory forms a 2:1 retrograde ellipse relative to Phobos.
    qso_tiers = {
        "QSO-H": {"radial_amplitude_km": 50.0, "along_track_amplitude_km": 100.0, "objective": "Global mapping & gravity estimation"},
        "QSO-M": {"radial_amplitude_km": 25.0, "along_track_amplitude_km": 50.0, "objective": "Landing site reconnaissance & spectroscopy"},
        "QSO-L": {"radial_amplitude_km": 10.0, "along_track_amplitude_km": 20.0, "objective": "Descent initiation & IDEFIX deployment"},
    }

    # Orbital frequency n in rad/s
    orbital_freq_rad_s = math.sqrt(MU_MARS / (r_orbit_km ** 3))
    period_s = 2.0 * math.pi / orbital_freq_rad_s

    return {
        "phobos_semi_major_axis_km": r_orbit_km,
        "phobos_hill_sphere_radius_km": round(r_hill_km, 3),
        "phobos_mean_radius_km": PHOBOS_MEAN_RADIUS_KM,
        "phobos_max_semi_axis_km": PHOBOS_A_KM,
        "hill_clearance_mean_km": round(clearance_mean_km, 3),
        "hill_clearance_long_axis_km": round(clearance_long_axis_km, 3),
        "mars_roche_limit_rigid_km": round(roche_rigid_km, 1),
        "mars_roche_limit_fluid_km": round(roche_fluid_km, 1),
        "mars_synchronous_orbit_radius_km": round(mars_sync_radius_km, 1),
        "is_inside_synchronous_orbit": is_inside_sync,
        "secular_spiral_inward": True,  # Tidal lag accelerates inward spiral (~1.8 m/century)
        "phobos_orbital_period_hours": round(period_s / 3600.0, 4),
        "qso_aspect_ratio_along_to_radial": 2.0,  # 2:1 HCW ellipse
        "qso_tiers": qso_tiers,
        "keplerian_circular_stable": False,  # Hill radius too small relative to Phobos body
    }


def compute_idefix_microgravity_mobility(
    rover_mass_kg: float = 25.0,
    phobos_surface_g: float = PHOBOS_SURFACE_G_MS2
) -> Dict[str, Any]:
    """
    Computes IDEFIX rover mobility kinematics under Phobos' extreme microgravity.
    Shows surface weight, critical liftoff velocity, and traction mechanics.
    """
    weight_n = rover_mass_kg * phobos_surface_g
    earth_equiv_weight_kg = weight_n / EARTH_SURFACE_G

    # Critical vertical bouncing threshold:
    # If a wheel hits an obstacle of height h at speed v, vertical impulse can exceed escape velocity
    # Escape velocity is ~11.39 m/s, but even 0.1 m/s launch can cause long-duration flight (minutes)
    # Flight duration for vertical hop v_0: t_flight = 2 * v_0 / g
    v_hop_test_ms = 0.05  # 5 cm/s vertical bounce
    t_flight_s = 2.0 * v_hop_test_ms / phobos_surface_g
    h_max_m = (v_hop_test_ms ** 2) / (2.0 * phobos_surface_g)

    # Safe driving speed range: 1 to 2 cm/s
    v_drive_nominal_cms = 1.5

    return {
        "rover_name": "IDEFIX (CNES / DLR)",
        "rover_mass_kg": rover_mass_kg,
        "phobos_surface_g_ms2": phobos_surface_g,
        "surface_weight_newtons": round(weight_n, 4),
        "earth_equivalent_mass_grams": round(earth_equiv_weight_kg * 1000.0, 2),
        "gravity_reduction_ratio": round(EARTH_SURFACE_G / phobos_surface_g, 1),
        "nominal_drive_speed_cms": v_drive_nominal_cms,
        "sample_hop_speed_cms": v_hop_test_ms * 100.0,
        "hop_flight_duration_seconds": round(t_flight_s, 1),
        "hop_flight_max_height_meters": round(h_max_m, 3),
        "autonomous_uprighting_mechanism": True,  # 4-wheel flipping arms
    }


def compute_phobos_martian_ejecta_fraction(
    collected_mass_grams: float = 10.0,
    ejecta_fraction_min: float = 0.001,   # 0.1%
    ejecta_fraction_nominal: float = 0.005,# 0.5%
    ejecta_fraction_max: float = 0.010    # 1.0%
) -> Dict[str, Any]:
    """
    Computes expected yield of ancient Martian crustal ejecta within the returned Phobos sample.
    Over 4 billion years of Martian meteorite impacts, high-velocity ejecta (>5.03 km/s)
    has been swept up by Phobos orbiting deep within Mars' gravity well.
    """
    mars_ejecta_min_mg = collected_mass_grams * ejecta_fraction_min * 1000.0
    mars_ejecta_nom_mg = collected_mass_grams * ejecta_fraction_nominal * 1000.0
    mars_ejecta_max_mg = collected_mass_grams * ejecta_fraction_max * 1000.0

    # Number of 10-micron silicate/carbonate grains in 50 mg (assuming density 2.8 g/cm^3)
    grain_radius_um = 10.0
    grain_vol_cm3 = (4.0 / 3.0) * math.pi * ((grain_radius_um * 1e-4) ** 3)
    grain_mass_g = grain_vol_cm3 * 2.8
    num_grains_nominal = (mars_ejecta_nom_mg * 1e-3) / grain_mass_g

    return {
        "collected_sample_mass_grams": collected_mass_grams,
        "martian_ejecta_fraction_nominal_percent": ejecta_fraction_nominal * 100.0,
        "martian_ejecta_min_mg": round(mars_ejecta_min_mg, 1),
        "martian_ejecta_nominal_mg": round(mars_ejecta_nom_mg, 1),
        "martian_ejecta_max_mg": round(mars_ejecta_max_mg, 1),
        "estimated_10um_martian_grain_count": int(num_grains_nominal),
        "scientific_value": "Allows laboratory analysis of ancient Mars crust without high-risk Mars surface ascent",
        "primary_sample_system": "Pneumatic gas-lift + Corer drill (>= 10g target)",
        "return_location": "Woomera Desert, South Australia (2031)",
    }
