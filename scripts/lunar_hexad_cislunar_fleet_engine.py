"""
Lunar Hexad & The Grand Quattuortrigintet Engine (2026-10-18)
============================================================
Astrodynamics, payload physics, and fleet census for the six active
lunar exploration missions (The Lunar Hexad / 月球现役六大金刚) and the
comprehensive 34-probe deep-space armada (The Grand Quattuortrigintet /
人类深空三十四极黄金舰队).

Six Lunar Flagships:
  1. LRO (NASA, 2009): 17.3 yrs quasi-frozen orbit, 0.5m LROC, Diviner 26K PSR cold pole, LOLA 3D
  2. Chandrayaan-2 Orbiter (ISRO, 2019): 100km polar, 0.25m OHRC highest optical resolution, DFSAR, CLASS Na
  3. Danuri / KPLO (KARI/NASA, 2022): 100km polar, BLT trajectory, ShadowCam 200x PSR, PolCam DoLP, DTN
  4. CAPSTONE (NASA/Rocket Lab, 2022): 12U CubeSat, 9:2 NRHO halo orbit, 1.5 m/s/yr stationkeeping, Gateway pathfinder
  5. Queqiao-2 (CNSA, 2024): Frozen elliptical relay orbit (200x16000km, 24h), 4.2m umbrella antenna, CE-6/7/8
  6. Chang'e-4 / Yutu-2 (CNSA, 2019): Farside Von Kármán crater, 7.8 yrs, 96+ lunar days, LPR radar, Pu-238 RHU

Thirty-Four Deep Space Probes (日心极距降序):
  Voyager 1, Voyager 2, New Horizons, Juno, JUICE, Europa Clipper, Lucy, Psyche,
  Mars Odyssey, Mars Express, ExoMars TGO, MAVEN, Hope, Curiosity, Perseverance,
  Tianwen-1 Orbiter, MRO, Hera, Hayabusa2#, OSIRIS-APEX, JWST, Euclid, Tianwen-2,
  LRO, Chandrayaan-2, Danuri, CAPSTONE, Queqiao-2, Chang'e-4/Yutu-2, SOHO, STEREO-A,
  BepiColombo, Solar Orbiter, Parker Solar Probe.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
import math
from typing import Dict, List, Any

# Gravitational and physical constants
G = 6.67430e-11                  # m^3 / (kg * s^2)
C_LIGHT = 299792458.0            # m/s
AU_KM = 149597870.7              # km

# Moon physical parameters
MU_MOON = 4902.800066            # km^3 / s^2 (Moon gravitational parameter GM)
R_MOON_KM = 1737.4               # Mean lunar radius in km
MASS_MOON_KG = 7.342e22          # Moon mass in kg

# Reference epoch: 2026-10-18 17:00:00 CST (09:00:00 UTC)
EPOCH_2026_10_18 = datetime(2026, 10, 18, 9, 0, 0, tzinfo=timezone.utc)


@dataclass(frozen=True)
class LunarOrbitalState:
    name: str
    agency: str
    launch_date: str
    arrival_date: str
    orbit_type: str
    semi_major_axis_km: float
    eccentricity: float
    perilune_alt_km: float
    apolune_alt_km: float
    period_minutes: float
    orbital_velocity_mean_kms: float
    cumulative_days: float
    cumulative_years: float
    cumulative_orbits: int
    core_payloads: List[str]
    scientific_highlights: List[str]


def lro_orbital_and_thermal_dynamics(ref_dt: datetime = EPOCH_2026_10_18) -> Dict[str, Any]:
    """
    Computes orbital and cryogenic thermal dynamics for NASA's Lunar Reconnaissance Orbiter (LRO).
    LRO launched 2009-06-18, MOI 2009-06-23.
    Operates in a quasi-frozen elliptical polar orbit (30 km x 200 km) with perilune at South Pole.
    """
    launch_dt = datetime(2009, 6, 18, 21, 32, 0, tzinfo=timezone.utc)
    arrival_dt = datetime(2009, 6, 23, 10, 27, 0, tzinfo=timezone.utc)
    
    elapsed_days = (ref_dt - arrival_dt).total_seconds() / 86400.0
    elapsed_years = elapsed_days / 365.25
    
    hp = 30.0    # Perilune altitude over South Pole in km
    ha = 200.0   # Apolune altitude over North Pole in km
    rp = R_MOON_KM + hp
    ra = R_MOON_KM + ha
    
    a = (rp + ra) / 2.0
    e = (ra - rp) / (2.0 * a)
    
    period_sec = 2.0 * math.pi * math.sqrt((a ** 3) / MU_MOON)
    period_min = period_sec / 60.0
    
    vp = math.sqrt(MU_MOON * (2.0 / rp - 1.0 / a))
    va = math.sqrt(MU_MOON * (2.0 / ra - 1.0 / a))
    v_mean = math.sqrt(MU_MOON / a)
    
    daily_orbits = 86400.0 / period_sec
    est_cumulative_orbits = int(elapsed_days * daily_orbits)
    
    # Cryogenic thermal physics (Diviner)
    diviner_lowest_temp_k = 26.0  # Measured in Hermite Crater floor PSR
    diviner_lowest_temp_c = diviner_lowest_temp_k - 273.15
    pluto_surface_temp_k = 40.0
    
    # LROC optical resolution & LOLA measurements
    lroc_res_m = 0.50
    lola_points_count = 4.5e9
    
    return {
        "mission": "Lunar Reconnaissance Orbiter (LRO)",
        "agency": "NASA",
        "elapsed_days": round(elapsed_days, 2),
        "elapsed_years": round(elapsed_years, 3),
        "hp_km": hp,
        "ha_km": ha,
        "semi_major_axis_km": round(a, 2),
        "eccentricity": round(e, 5),
        "period_minutes": round(period_min, 2),
        "perilune_velocity_kms": round(vp, 4),
        "apolune_velocity_kms": round(va, 4),
        "mean_velocity_kms": round(v_mean, 4),
        "cumulative_orbits": est_cumulative_orbits,
        "diviner_lowest_temp_k": diviner_lowest_temp_k,
        "diviner_lowest_temp_c": round(diviner_lowest_temp_c, 2),
        "temp_comparison_pluto_k": pluto_surface_temp_k,
        "lroc_nac_resolution_m": lroc_res_m,
        "lola_laser_pulses_total": lola_points_count,
        "quasifrozen_stability_note": "Perilune locked over south pole to preserve fuel and enable zero-deltaV stability"
    }


def chandrayaan2_optical_sar_xray_dynamics(ref_dt: datetime = EPOCH_2026_10_18) -> Dict[str, Any]:
    """
    Computes dynamics and payload physics for ISRO's Chandrayaan-2 Orbiter.
    Launched 2019-07-22, MOI 2019-08-20.
    100 km circular polar orbit, carrying OHRC (0.25m/px), DFSAR, and CLASS.
    """
    launch_dt = datetime(2019, 7, 22, 9, 13, 0, tzinfo=timezone.utc)
    arrival_dt = datetime(2019, 8, 20, 3, 32, 0, tzinfo=timezone.utc)
    
    elapsed_days = (ref_dt - arrival_dt).total_seconds() / 86400.0
    elapsed_years = elapsed_days / 365.25
    
    h = 100.0
    r = R_MOON_KM + h
    a = r
    e = 0.0
    
    period_sec = 2.0 * math.pi * math.sqrt((a ** 3) / MU_MOON)
    period_min = period_sec / 60.0
    v_circ = math.sqrt(MU_MOON / r)
    
    daily_orbits = 86400.0 / period_sec
    est_cumulative_orbits = int(elapsed_days * daily_orbits)
    
    # OHRC optical resolution
    ohrc_res_m = 0.25  # 25 cm/pixel from 100 km orbit
    res_advantage_vs_lroc = 0.50 / ohrc_res_m  # 2.0x higher spatial resolution
    
    # DFSAR Dual-Frequency SAR physics
    l_band_freq_ghz = 1.25
    s_band_freq_ghz = 2.50
    radar_depth_m = 5.0
    
    # CLASS X-ray fluorescence
    detected_species = ["Na", "Mg", "Al", "Si", "Ca", "Fe"]
    
    return {
        "mission": "Chandrayaan-2 Orbiter",
        "agency": "ISRO",
        "elapsed_days": round(elapsed_days, 2),
        "elapsed_years": round(elapsed_years, 3),
        "altitude_km": h,
        "semi_major_axis_km": round(a, 2),
        "eccentricity": e,
        "period_minutes": round(period_min, 2),
        "circular_velocity_kms": round(v_circ, 4),
        "cumulative_orbits": est_cumulative_orbits,
        "ohrc_resolution_m": ohrc_res_m,
        "ohrc_advantage_over_lroc_factor": round(res_advantage_vs_lroc, 2),
        "dfsar_bands_ghz": {"L_band": l_band_freq_ghz, "S_band": s_band_freq_ghz},
        "dfsar_penetration_depth_m": radar_depth_m,
        "class_detected_elements": detected_species,
        "fuel_margin_years": "Extended life 7 to 10 years thanks to GSLV Mk III precise injection"
    }


def danuri_blt_shadowcam_polcam_dynamics(ref_dt: datetime = EPOCH_2026_10_18) -> Dict[str, Any]:
    """
    Computes dynamics and payload physics for Danuri (Korea Pathfinder Lunar Orbiter, KPLO).
    Launched 2022-08-04, LOI 2022-12-16, circular 100km polar orbit.
    Pioneered Ballistic Lunar Transfer (BLT), ShadowCam, PolCam, and DTN.
    """
    arrival_dt = datetime(2022, 12, 16, 17, 0, 0, tzinfo=timezone.utc)
    elapsed_days = (ref_dt - arrival_dt).total_seconds() / 86400.0
    elapsed_years = elapsed_days / 365.25
    
    h = 100.0
    r = R_MOON_KM + h
    a = r
    e = 0.0
    
    period_sec = 2.0 * math.pi * math.sqrt((a ** 3) / MU_MOON)
    period_min = period_sec / 60.0
    v_circ = math.sqrt(MU_MOON / r)
    
    daily_orbits = 86400.0 / period_sec
    est_cumulative_orbits = int(elapsed_days * daily_orbits)
    
    # Ballistic Lunar Transfer (BLT) mechanics
    blt_apogee_dist_km = 1.56e6  # Traveled 1.56 million km to Sun-Earth L1 region
    loi_deltav_blt_ms = 174.0
    loi_deltav_direct_ms = 750.0
    deltav_saving_pct = ((loi_deltav_direct_ms - loi_deltav_blt_ms) / loi_deltav_direct_ms) * 100.0
    
    # ShadowCam sensitivity
    shadowcam_sensitivity_multiplier = 200.0  # 200x more sensitive than LROC NAC
    
    # PolCam polarimetry
    polcam_bands_nm = [320, 430, 750]
    
    return {
        "mission": "Danuri (KPLO)",
        "agency": "KARI / NASA",
        "elapsed_days": round(elapsed_days, 2),
        "elapsed_years": round(elapsed_years, 3),
        "altitude_km": h,
        "semi_major_axis_km": round(a, 2),
        "period_minutes": round(period_min, 2),
        "circular_velocity_kms": round(v_circ, 4),
        "cumulative_orbits": est_cumulative_orbits,
        "blt_max_distance_km": blt_apogee_dist_km,
        "blt_loi_deltav_ms": loi_deltav_blt_ms,
        "blt_deltav_savings_pct": round(deltav_saving_pct, 1),
        "shadowcam_sensitivity_vs_lroc": shadowcam_sensitivity_multiplier,
        "polcam_wavelengths_nm": polcam_bands_nm,
        "dtn_protocol": "Delay-Tolerant Networking (RFC 5050/9171) space Internet demonstrated"
    }


def capstone_nrho_astrodynamics(ref_dt: datetime = EPOCH_2026_10_18) -> Dict[str, Any]:
    """
    Computes dynamics for NASA / Advanced Space CAPSTONE in Near-Rectilinear Halo Orbit (NRHO).
    Launched 2022-06-28, NRHO insertion 2022-11-13.
    12U CubeSat (25 kg) testing Artemis Gateway's baseline orbit.
    """
    arrival_dt = datetime(2022, 11, 13, 23, 0, 0, tzinfo=timezone.utc)
    elapsed_days = (ref_dt - arrival_dt).total_seconds() / 86400.0
    elapsed_years = elapsed_days / 365.25
    
    mass_kg = 25.0
    form_factor = "12U CubeSat"
    
    # NRHO orbital elements (L2 Southern Halo in 9:2 synodic resonance)
    hp = 1600.0     # Perilune over lunar North Pole in km
    ha = 70000.0    # Apolune over lunar South Pole in km
    rp = R_MOON_KM + hp
    ra = R_MOON_KM + ha
    
    period_days = 6.55  # ~6.55 days (approx 157.2 hours)
    period_hours = period_days * 24.0
    
    # Stationkeeping requirement in NRHO
    annual_stationkeeping_deltav_ms = 2.0  # ~1.5 - 2.5 m/s per year
    
    cumulative_revolutions = int(elapsed_days / period_days)
    
    return {
        "mission": "CAPSTONE",
        "agency": "NASA / Advanced Space / Rocket Lab",
        "mass_kg": mass_kg,
        "form_factor": form_factor,
        "elapsed_days": round(elapsed_days, 2),
        "elapsed_years": round(elapsed_years, 3),
        "orbit_family": "Earth-Moon L2 Southern Near-Rectilinear Halo Orbit (NRHO)",
        "resonance_ratio": "9:2 orbital resonance with lunar synodic month",
        "perilune_alt_km": hp,
        "apolune_alt_km": ha,
        "period_days": period_days,
        "period_hours": period_hours,
        "cumulative_revolutions": cumulative_revolutions,
        "annual_stationkeeping_deltav_ms": annual_stationkeeping_deltav_ms,
        "caps_autonomous_navigation": "Peer-to-peer cross-link ranging with LRO without Earth DSN dependency",
        "gateway_significance": "Pathfinder and risk-reduction flight for Artemis Gateway space station"
    }


def queqiao2_frozen_relay_dynamics(ref_dt: datetime = EPOCH_2026_10_18) -> Dict[str, Any]:
    """
    Computes dynamics for CNSA's Queqiao-2 (鹊桥二号) lunar relay satellite.
    Launched 2024-03-20, entered lunar relay orbit 2024-03-25.
    High-inclination frozen elliptical orbit (200 km x 16,000 km, ~24h period).
    Carries 4.2m umbrella mesh parabolic antenna.
    """
    arrival_dt = datetime(2024, 3, 25, 16, 0, 0, tzinfo=timezone.utc)
    elapsed_days = (ref_dt - arrival_dt).total_seconds() / 86400.0
    elapsed_years = elapsed_days / 365.25
    
    mass_kg = 1200.0
    antenna_diam_m = 4.2
    
    hp = 200.0
    ha = 16000.0
    rp = R_MOON_KM + hp
    ra = R_MOON_KM + ha
    
    a = (rp + ra) / 2.0
    e = (ra - rp) / (2.0 * a)
    
    period_sec = 2.0 * math.pi * math.sqrt((a ** 3) / MU_MOON)
    period_hours = period_sec / 3600.0
    
    # Critical inclination for frozen lunar orbit
    critical_inclination_deg = 54.8  # Eliminates secular drift of argument of periapsis under Earth 3-body + mascon
    
    # Southern visibility fraction
    south_pole_viewing_duty_cycle_pct = 75.0  # Over 16-18 hours of continuous view per orbit
    
    cumulative_orbits = int((elapsed_days * 24.0) / period_hours)
    
    return {
        "mission": "Queqiao-2 (鹊桥二号)",
        "agency": "CNSA",
        "mass_kg": mass_kg,
        "antenna_diameter_m": antenna_diam_m,
        "elapsed_days": round(elapsed_days, 2),
        "elapsed_years": round(elapsed_years, 3),
        "orbit_type": "Lunar Frozen Elliptical Relay Orbit (冻结大椭圆中继轨道)",
        "hp_km": hp,
        "ha_km": ha,
        "semi_major_axis_km": round(a, 2),
        "eccentricity": round(e, 5),
        "period_hours": round(period_hours, 2),
        "critical_inclination_deg": critical_inclination_deg,
        "south_pole_duty_cycle_pct": south_pole_viewing_duty_cycle_pct,
        "cumulative_orbits": cumulative_orbits,
        "supported_missions": ["Chang'e-6 (Farside Sample Return)", "Chang'e-7 (South Pole Water Ice)", "Chang'e-8 (ISRU & Station)"]
    }


def change4_yutu2_farside_rhus_dynamics(ref_dt: datetime = EPOCH_2026_10_18) -> Dict[str, Any]:
    """
    Computes operational and physical state of CNSA's Chang'e-4 Lander & Yutu-2 Rover.
    Launched 2018-12-08, landed 2019-01-03 in Von Kármán crater, South Pole-Aitken Basin.
    Active for over 7.79 years and 96+ lunar days.
    """
    landing_dt = datetime(2019, 1, 3, 2, 26, 0, tzinfo=timezone.utc)
    elapsed_days = (ref_dt - landing_dt).total_seconds() / 86400.0
    elapsed_years = elapsed_days / 365.25
    
    lunar_synodic_days = 29.530588
    lunar_days_passed = int(elapsed_days / lunar_synodic_days)
    
    traverse_distance_m = 1613.0
    
    # Low frequency radio astronomy (LFS)
    rfi_shielding_km = 3474.8  # Moon diameter blocks Earth anthropogenic radio noise
    freq_range_mhz = (0.1, 40.0)
    
    # Subsurface radar (LPR)
    radar_depth_m = 40.0  # Finsen ejecta layer
    
    # Thermal survival
    night_temp_c = -180.0
    night_temp_k = night_temp_c + 273.15
    heat_source = "Plutonium-238 Radioisotope Heater Units (RHU)"
    
    return {
        "mission": "Chang'e-4 & Yutu-2 (嫦娥四号与玉兔二号)",
        "agency": "CNSA",
        "landing_site": "Von Kármán Crater, South Pole-Aitken Basin (45.45°S, 177.6°E)",
        "elapsed_days": round(elapsed_days, 2),
        "elapsed_years": round(elapsed_years, 3),
        "lunar_days_operational": lunar_days_passed,
        "rover_traverse_distance_m": traverse_distance_m,
        "rfi_shielding_diameter_km": rfi_shielding_km,
        "lfs_frequency_range_mhz": freq_range_mhz,
        "lpr_subsurface_depth_m": radar_depth_m,
        "night_temperature_k": round(night_temp_k, 2),
        "night_temperature_c": night_temp_c,
        "thermal_survival_mechanism": heat_source
    }


def lunar_hexad_system_summary(ref_dt: datetime = EPOCH_2026_10_18) -> Dict[str, Any]:
    """
    Synthesizes the complete six-probe Lunar Exploration Armada (The Lunar Hexad / 月球现役六大金刚).
    """
    lro = lro_orbital_and_thermal_dynamics(ref_dt)
    ch2 = chandrayaan2_optical_sar_xray_dynamics(ref_dt)
    danuri = danuri_blt_shadowcam_polcam_dynamics(ref_dt)
    capstone = capstone_nrho_astrodynamics(ref_dt)
    queqiao2 = queqiao2_frozen_relay_dynamics(ref_dt)
    change4 = change4_yutu2_farside_rhus_dynamics(ref_dt)
    
    probes = [
        {
            "id": 1,
            "name": "LRO (Lunar Reconnaissance Orbiter)",
            "agency": "NASA",
            "launch_year": 2009,
            "years_active": lro["elapsed_years"],
            "orbit_regime": "Quasi-frozen polar (30 x 200 km)",
            "signature_capability": "0.5m LROC imaging, Diviner 26K PSR cold pole, LOLA 4.5B-point 3D DEM"
        },
        {
            "id": 2,
            "name": "Chandrayaan-2 Orbiter",
            "agency": "ISRO",
            "launch_year": 2019,
            "years_active": ch2["elapsed_years"],
            "orbit_regime": "100 km circular polar",
            "signature_capability": "0.25m OHRC highest lunar optical resolution, DFSAR dual polarimetry, CLASS Na XRF"
        },
        {
            "id": 3,
            "name": "Danuri (KPLO)",
            "agency": "KARI / NASA",
            "launch_year": 2022,
            "years_active": danuri["elapsed_years"],
            "orbit_regime": "100 km circular polar (via BLT)",
            "signature_capability": "ShadowCam 200x optical sensitivity in PSRs, PolCam DoLP titanium mapping, DTN"
        },
        {
            "id": 4,
            "name": "CAPSTONE",
            "agency": "NASA / Advanced Space",
            "launch_year": 2022,
            "years_active": capstone["elapsed_years"],
            "orbit_regime": "9:2 NRHO Halo Orbit (1,600 x 70,000 km)",
            "signature_capability": "12U CubeSat Artemis Gateway orbit validation, 2 m/s/yr stationkeeping, CAPS cross-link"
        },
        {
            "id": 5,
            "name": "Queqiao-2 (鹊桥二号)",
            "agency": "CNSA",
            "launch_year": 2024,
            "years_active": queqiao2["elapsed_years"],
            "orbit_regime": "Frozen elliptical 24h relay (200 x 16,000 km, 54.8°)",
            "signature_capability": "4.2m umbrella parabolic gold antenna, Chang'e-6 farside relay, Chang'e-7/8 backbone"
        },
        {
            "id": 6,
            "name": "Chang'e-4 & Yutu-2 (嫦娥四号与玉兔二号)",
            "agency": "CNSA",
            "launch_year": 2018,
            "years_active": change4["elapsed_years"],
            "orbit_regime": "Lunar Farside Surface (Von Kármán Crater)",
            "signature_capability": "Humankind's only farside landing, 96+ lunar days, 1613m traverse, LPR radar, Pu-238 RHU"
        }
    ]
    
    total_lunar_probes = len(probes)
    total_operational_years = sum(p["years_active"] for p in probes)
    
    return {
        "fleet_name": "The Lunar Explorer Hexad (月球现役六大金刚)",
        "total_probes": total_lunar_probes,
        "combined_operational_years": round(total_operational_years, 2),
        "probes": probes
    }


def the_grand_quattuortrigintet_fleet_census(ref_dt: datetime = EPOCH_2026_10_18) -> Dict[str, Any]:
    """
    Authoritative, comprehensive census of all 34 active deep-space probes
    operating outside low-Earth orbit as of October 2026.
    Strictly ordered by descending heliocentric distance (日心极距降序).
    """
    fleet = [
        # 1. Interstellar Space
        {"rank": 1, "name": "Voyager 1", "agency": "NASA", "dist_au": 173.22, "arena": "Interstellar Boundary",
         "role": "Deepest human reach, 24.01h one-way light time, 1 light-day countdown"},
        {"rank": 2, "name": "Voyager 2", "agency": "NASA", "dist_au": 144.29, "arena": "Interstellar Southern Sky",
         "role": "Southern interstellar trajectory, crossed 20.00h light-time mark today"},
        {"rank": 3, "name": "New Horizons", "agency": "NASA", "dist_au": 65.92, "arena": "Kuiper Belt Escape",
         "role": "Hyperbolic escape, Cosmic Optical Background, PUI solar wind deceleration"},
        # 2. Outer Planets & Jupiter
        {"rank": 4, "name": "Juno", "agency": "NASA", "dist_au": 5.20, "arena": "Jupiter Polar Orbit",
         "role": "Radiation vault, 57.8 km/s perijove, PJ89 countdown in 26 days"},
        {"rank": 5, "name": "JUICE", "agency": "ESA", "dist_au": 5.20, "arena": "Jupiter Icy Moons Cruise",
         "role": "Ganymede/Callisto/Europa deep oceans, 85m² solar arrays"},
        {"rank": 6, "name": "Europa Clipper", "agency": "NASA", "dist_au": 5.20, "arena": "Europa Habitability Cruise",
         "role": "Europa habitability, MEGA Earth flyby countdown in 46 days"},
        {"rank": 7, "name": "Lucy", "agency": "NASA", "dist_au": 5.04, "arena": "Trojan Asteroids Cruise",
         "role": "Jupiter Trojan swarms, 7.3m UltraFlex solar arrays, 5th launch anniversary"},
        # 3. Asteroid Belt
        {"rank": 8, "name": "Psyche", "agency": "NASA", "dist_au": 2.042, "arena": "Metal Core Asteroid Cruise",
         "role": "SPT-140 Hall electric thrusters, DSOC optical communications"},
        # 4. Martian Nonet (火星现役九大极器)
        {"rank": 9, "name": "2001 Mars Odyssey", "agency": "NASA", "dist_au": 1.579, "arena": "Mars Orbit",
         "role": "25-year silver jubilee countdown in 6 days, 111,300+ orbits, GRS shallow water ice"},
        {"rank": 10, "name": "Mars Express", "agency": "ESA", "dist_au": 1.579, "arena": "Mars Orbit",
         "role": "23 years in orbit, MARSIS 5km radar, Phobos 45km rubble-pile flyby"},
        {"rank": 11, "name": "ExoMars TGO", "agency": "ESA/Roscosmos", "dist_au": 1.579, "arena": "Mars Orbit",
         "role": "10-year decennial countdown in 30 hours, NOMAD 50pptv methane, HCl discovery, Candor Chaos 40% ice"},
        {"rank": 12, "name": "MAVEN", "agency": "NASA", "dist_au": 1.579, "arena": "Mars Orbit",
         "role": "12 years in orbit, 66% Ar isotope atmospheric escape, oxygen photochemical loss"},
        {"rank": 13, "name": "Hope Probe (Al-Amal)", "agency": "UAE/MBRSC", "dist_au": 1.579, "arena": "Mars 55h Orbit",
         "role": "Extended to 2028, full-disc 55h weather dynamics, sinuous aurora, Deimos 100km flyby"},
        {"rank": 14, "name": "Curiosity Rover", "agency": "NASA", "dist_au": 1.524, "arena": "Mars Surface (Gale)",
         "role": "14 years traversing 33.6km, Gediz Vallis pure sulfur crystal breakthrough, MMRTG"},
        {"rank": 15, "name": "Perseverance Rover", "agency": "NASA", "dist_au": 1.524, "arena": "Mars Surface (Jezero)",
         "role": "Scaled 500m crater rim to Wild West, generative AI navigation, 33 sealed rock cores"},
        {"rank": 16, "name": "Tianwen-1 Orbiter", "agency": "CNSA", "dist_au": 1.524, "arena": "Mars Orbit",
         "role": "Global polar remote sensing, 76m orthorectified color map, MOSIR sub-surface radar"},
        {"rank": 17, "name": "Mars Reconnaissance Orbiter (MRO)", "agency": "NASA", "dist_au": 1.524, "arena": "Mars Orbit",
         "role": "20.6 years in orbit, HiRISE 30cm micro-vision, SHARAD 1km ice, 80% surface relay backbone"},
        # 5. Inner Asteroids & Planetary Defense
        {"rank": 18, "name": "Hera", "agency": "ESA", "dist_au": 1.304, "arena": "Didymos Binary Cruise",
         "role": "Planetary defense, post-DART crater characterization, BRM-1 burn complete"},
        {"rank": 19, "name": "Hayabusa2# (SHARP)", "agency": "JAXA", "dist_au": 1.120, "arena": "Micro-Asteroid Cruise",
         "role": "1998 KY26 fast rotator rendezvous, Torifune flyby, 490x centrifugal landing challenge"},
        {"rank": 20, "name": "OSIRIS-APEX", "agency": "NASA", "dist_au": 1.010, "arena": "Apophis Cruise",
         "role": "Apophis 2029 rendezvous, 4x solar flux perihelion thermal shielding, STIR thruster plumes"},
        # 6. Sun-Earth L2 Space Observatories
        {"rank": 21, "name": "JWST", "agency": "NASA/ESA/CSA", "dist_au": 1.010, "arena": "Sun-Earth L2 Halo",
         "role": "6.5m beryllium-gold mirror, 6.7 K cryocooler, z>14 cosmic dawn galaxies"},
        {"rank": 22, "name": "Euclid", "agency": "ESA", "dist_au": 1.010, "arena": "Sun-Earth L2 Halo",
         "role": "1.2m SiC TMA telescope, 0.53 deg² field, 3D cosmic web dark matter / dark energy mapping"},
        # 7. Earth Quasi-Satellites
        {"rank": 23, "name": "Tianwen-2", "agency": "CNSA", "dist_au": 1.001, "arena": "Quasi-Satellite Cruise",
         "role": "Kamoʻoalewa quasi-satellite touch-and-go sampling & 311P active asteroid dual mission"},
        # 8. Earth-Moon Cislunar System / Lunar Hexad (月球现役六大金刚)
        {"rank": 24, "name": "LRO (Lunar Reconnaissance Orbiter)", "agency": "NASA", "dist_au": 1.000, "arena": "Lunar Quasi-Frozen Polar",
         "role": "17.3 yrs in orbit, 0.5m LROC imaging, Diviner 26K PSR cold pole, LOLA 3D topography"},
        {"rank": 25, "name": "Chandrayaan-2 Orbiter", "agency": "ISRO", "dist_au": 1.000, "arena": "Lunar 100km Polar",
         "role": "7.2 yrs in orbit, 0.25m OHRC highest optical resolution, DFSAR dual polarimetry, CLASS Na XRF"},
        {"rank": 26, "name": "Danuri (KPLO)", "agency": "KARI/NASA", "dist_au": 1.000, "arena": "Lunar 100km Polar",
         "role": "3.8 yrs in orbit, BLT trajectory, ShadowCam 200x PSR imaging, PolCam DoLP titanium, DTN"},
        {"rank": 27, "name": "CAPSTONE", "agency": "NASA/Advanced Space", "dist_au": 1.000, "arena": "Cislunar 9:2 NRHO Halo",
         "role": "12U CubeSat, 3.9 yrs in 9:2 NRHO, 2 m/s/yr stationkeeping, Artemis Gateway pathfinder"},
        {"rank": 28, "name": "Queqiao-2 (鹊桥二号)", "agency": "CNSA", "dist_au": 1.000, "arena": "Lunar Frozen Relay Orbit",
         "role": "4.2m umbrella parabolic gold antenna, Chang'e-6 farside relay, Chang'e-7/8 backbone"},
        {"rank": 29, "name": "Chang'e-4 & Yutu-2 (嫦娥四号与玉兔二号)", "agency": "CNSA", "dist_au": 1.000, "arena": "Lunar Farside Surface",
         "role": "Humankind's only farside landing, 96+ lunar days, 1613m traverse, LPR radar, Pu-238 RHU"},
        # 9. Sun-Earth L1 & Heliospheric / Sun Grazers
        {"rank": 30, "name": "SOHO", "agency": "ESA/NASA", "dist_au": 0.990, "arena": "Sun-Earth L1 Halo",
         "role": "30.8 yrs in orbit, 1.49M km, LASCO CME early warning, 5,200+ sungrazing comets"},
        {"rank": 31, "name": "STEREO-A", "agency": "NASA", "dist_au": 0.962, "arena": "Heliocentric Drift",
         "role": "20th anniversary, 3D heliospheric stereoscopy, far-side CME 5-day early warning"},
        {"rank": 32, "name": "BepiColombo", "agency": "ESA/JAXA", "dist_au": 0.387, "arena": "Mercury Orbit Transfer",
         "role": "Mercury gravity well capture, -1405 MJ/kg MOI blind insertion approach countdown"},
        {"rank": 33, "name": "Solar Orbiter", "agency": "ESA/NASA", "dist_au": 0.280, "arena": "High-Inclination Solar",
         "role": "Out-of-ecliptic polar imaging, 520°C bone-black heat shield, Christmas Eve VGA5 in 67 days"},
        {"rank": 34, "name": "Parker Solar Probe", "agency": "NASA", "dist_au": 0.046, "arena": "Solar Corona In-Situ",
         "role": "192 km/s record speed, 1400°C carbon shield, P30 perihelion in 45 days"}
    ]
    
    # Compute physical extremes
    max_dist_au = fleet[0]["dist_au"]
    min_dist_au = fleet[-1]["dist_au"]
    dist_span_ratio = max_dist_au / min_dist_au
    solar_flux_drop_ratio = (max_dist_au / min_dist_au) ** 2
    
    # Temperature extreme
    t_max_k = 1400.0 + 273.15  # Parker Solar Probe front shield
    t_min_k = 6.7              # JWST MIRI detector stage
    delta_t_k = t_max_k - t_min_k
    
    # Light-time extreme
    v1_light_sec = (max_dist_au * AU_KM * 1000.0) / C_LIGHT
    lunar_dist_km = 384400.0
    moon_light_sec = (lunar_dist_km * 1000.0) / C_LIGHT
    latency_ratio = v1_light_sec / moon_light_sec
    
    # Velocity extreme
    parker_v_ms = 192000.0
    ky26_v_ms = 0.00688
    velocity_ratio = parker_v_ms / ky26_v_ms
    
    return {
        "fleet_name": "The Grand Quattuortrigintet (人类深空三十四极黄金舰队)",
        "probe_count": len(fleet),
        "fleet": fleet,
        "extremes": {
            "max_heliocentric_dist_au": max_dist_au,
            "min_heliocentric_dist_au": min_dist_au,
            "distance_span_ratio": round(dist_span_ratio, 2),
            "solar_flux_drop_ratio": round(solar_flux_drop_ratio, 1),
            "max_temperature_k": round(t_max_k, 2),
            "min_temperature_k": t_min_k,
            "temperature_span_k": round(delta_t_k, 2),
            "voyager1_one_way_light_hours": round(v1_light_sec / 3600.0, 2),
            "lunar_one_way_light_seconds": round(moon_light_sec, 3),
            "communication_latency_ratio": round(latency_ratio, 1),
            "velocity_ratio": round(velocity_ratio, 1)
        }
    }


if __name__ == "__main__":
    import json
    hexad = lunar_hexad_system_summary()
    fleet = the_grand_quattuortrigintet_fleet_census()
    print("=== THE LUNAR HEXAD ===")
    print(json.dumps(hexad, indent=2, ensure_ascii=False))
    print("\n=== THE GRAND QUATTUORTRIGINTET (34 PROBES) ===")
    print(f"Total active deep space probes: {fleet['probe_count']}")
    print(f"Distance ratio: {fleet['extremes']['distance_span_ratio']}x")
    print(f"Solar flux drop: {fleet['extremes']['solar_flux_drop_ratio']}x")
    print(f"Latency ratio: {fleet['extremes']['communication_latency_ratio']}x")
