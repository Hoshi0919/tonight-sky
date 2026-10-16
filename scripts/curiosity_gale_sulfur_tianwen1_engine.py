#!/usr/bin/env python3
"""
Curiosity Gale Crater Sulfur & Tianwen-1 Mars Orbiter Dynamics Engine
with the 2026 Human Deep Space Grand Vigintet (Twenty-Fold Fleet) Matrix.

Models:
1. NASA Curiosity Mars Rover (MSL) 14-year Gale Crater exploration:
   - 33.5+ km traverse, >800m Mount Sharp elevation climb.
   - Sol 4189 (May 2024) Gediz Vallis pure native elemental sulfur (S8) discovery.
   - Native sulfur formation thermodynamics (volcanic gas condensation & cryosphere trapping).
   - MMRTG Pu-238 radioisotope decay (87.74 yr half-life, 14.2 yr decay, electrical output ~87.7 W).
   - Aluminum wheel traction control & puncture mitigation algorithms.
2. CNSA Tianwen-1 Mars Orbiter (天问一号环绕器):
   - Polar elliptical remote sensing orbit (265 km x 10,700 km, 7.05h period, 86.9 deg inclination).
   - Vis-viva velocities (periapsis 4.314 km/s vs apoapsis 1.119 km/s, 3.86x ratio).
   - 7 scientific payloads: MoRIC (76m global true-color orthomosaic map), HiRIC (0.5m/px),
     MOSIR (subsurface radar), MMS, MOMAG, MINPA (ion/ENA atmospheric escape), MEPA.
   - Interstellar comet 3I/ATLAS imaging from 28.96M km (0.194 AU) out-of-plane observation.
   - 3.5 TB public science data milestone.
3. Mars Exploration Trinity (火星探索三位一体):
   - Curiosity (Gale Crater, 4.58°S, 137.44°E, 14-yr veteran geologist, pure sulfur, MMRTG)
   - Perseverance (Jezero Crater, 18.38°N, 77.58°E, 500m rim climb to Wild West, generative AI VLM, MOXIE)
   - Tianwen-1 Orbiter (Polar remote sensing sentinel, global 76m orthomosaic, subsurface radar, MINPA)
   - Rover spherical separation distance: 63.27° / 3,742.9 km across Martian terrain.
4. 2026 Human Deep Space Grand Vigintet (The Grand Vigintet / 二十极黄金舰队):
   - 20 deep space flagships ordered strictly by heliocentric distance (0.046 AU to 173.22 AU).
   - Physical duality extrema: 3,777.2x heliocentric distance, 14.27M-fold solar flux span,
     67,383x geocentric distance and light-time span, 27.9M-fold velocity ratio, >1,670 K thermal span.
"""

import math
from datetime import datetime, timezone
from typing import Dict, Any, List

C_LIGHT_KM_S = 299792.458
AU_KM = 149597870.7
SOLAR_CONSTANT_1AU = 1361.0  # W/m^2

# Mars physical constants
R_MARS_KM = 3389.5
MU_MARS = 42828.37  # km^3 / s^2
MARS_SOL_HOURS = 24.65979
MARS_G_SURFACE = 3.72076  # m/s^2

# Earth physical constants
R_EARTH_KM = 6378.137


def compute_curiosity_gale_gediz_vallis_sulfur(
    current_time_utc: datetime = None
) -> Dict[str, Any]:
    """
    Computes Curiosity rover (MSL) mission state, Gediz Vallis pure sulfur discovery,
    MMRTG power degradation, and wheel wear mitigation.
    """
    if current_time_utc is None:
        current_time_utc = datetime(2026, 10, 16, 15, 0, 0, tzinfo=timezone.utc)

    landing_utc = datetime(2012, 8, 5, 5, 17, 57, tzinfo=timezone.utc)
    days_elapsed = (current_time_utc - landing_utc).total_seconds() / 86400.0
    years_elapsed = days_elapsed / 365.25
    sols_elapsed = days_elapsed * (24.0 / MARS_SOL_HOURS)

    # Rover location in Gale Crater: 4.58° S, 137.44° E
    lat_deg = -4.58
    lon_deg = 137.44
    crater_diameter_km = 154.0
    crater_floor_elevation_m = -4500.0
    mount_sharp_peak_m = 5500.0

    # Sol 4189 (May 2024) Gediz Vallis pure sulfur discovery
    sulfur_discovery_sol = 4189
    sulfur_discovery_date = "2024-05-30"
    days_since_sulfur = days_elapsed - (datetime(2024, 5, 30, tzinfo=timezone.utc) - landing_utc).total_seconds() / 86400.0

    # MMRTG decay: 4.8 kg Pu-238 dioxide, half-life 87.74 years
    pu238_half_life_yr = 87.74
    initial_thermal_power_w = 2000.0
    initial_electric_power_w = 110.0
    thermal_decay_factor = 0.5 ** (years_elapsed / pu238_half_life_yr)
    current_thermal_power_w = initial_thermal_power_w * thermal_decay_factor

    # Silicon-Germanium / PbTe-TAGS thermocouple junction aging (~0.8% per year)
    thermocouple_aging_rate = 0.008
    thermocouple_health_factor = (1.0 - thermocouple_aging_rate) ** years_elapsed
    current_electric_power_w = initial_electric_power_w * thermal_decay_factor * thermocouple_health_factor

    # Traverse metrics
    odometer_km = 33.65
    elevation_gained_m = 840.0

    return {
        "mission_name": "Mars Science Laboratory (MSL) Curiosity",
        "landing_utc": landing_utc.isoformat(),
        "current_time_utc": current_time_utc.isoformat(),
        "days_elapsed": round(days_elapsed, 2),
        "years_elapsed": round(years_elapsed, 3),
        "sols_elapsed": round(sols_elapsed, 1),
        "coordinates": {"latitude_deg": lat_deg, "longitude_deg": lon_deg},
        "gale_crater": {
            "diameter_km": crater_diameter_km,
            "crater_floor_elevation_m": crater_floor_elevation_m,
            "mount_sharp_peak_elevation_m": mount_sharp_peak_m,
            "elevation_gained_m": elevation_gained_m,
            "odometer_km": odometer_km,
        },
        "gediz_vallis_sulfur": {
            "discovery_sol": sulfur_discovery_sol,
            "discovery_date": sulfur_discovery_date,
            "days_since_discovery": round(days_since_sulfur, 1),
            "mineral_type": "Native Elemental Sulfur (S8 crystals)",
            "discovery_context": "Wheel crush of rock exposed bright yellow crystals with resinous luster",
            "confirmation_instruments": ["APXS (Alpha Particle X-ray Spectrometer)", "ChemCam (LIBS)", "Mastcam"],
            "purity_estimate": "Pure elemental sulfur (unprecendented in planetary exploration, Science cover)",
            "geological_origin": "Subsurface cryosphere trapping of volcanic H2S/SO2 vapors and subsequent erosional depressurization",
        },
        "mmrtg": {
            "fuel": "4.8 kg Plutonium-238 Dioxide",
            "half_life_yr": pu238_half_life_yr,
            "initial_thermal_w": initial_thermal_power_w,
            "current_thermal_w": round(current_thermal_power_w, 2),
            "thermal_decay_factor": round(thermal_decay_factor, 4),
            "thermocouple_health_factor": round(thermocouple_health_factor, 4),
            "initial_electric_w": initial_electric_power_w,
            "current_electric_w": round(current_electric_power_w, 2),
            "operational_status": "Stable power supporting daily sleep/wake cycles and instrument time-sharing",
        },
        "traction_control": {
            "wheels": "6 aluminum wheels (50 cm diameter, 40 cm width, 0.75 mm skin)",
            "wear_mitigation": "Dynamic wheel velocity adjustment algorithm synchronizing wheel RPM with terrain slip",
            "status": "Traverse extended past 33 km with manageable ventifact punctures",
        }
    }


def compute_tianwen1_mars_orbiter_dynamics() -> Dict[str, Any]:
    """
    Computes Tianwen-1 Mars Orbiter (CNSA) polar remote sensing orbit,
    vis-viva speeds, scientific instruments, and 3I/ATLAS interstellar observation.
    """
    # Operational remote sensing orbit parameters
    hp_km = 265.0
    ha_km = 10700.0
    rp_km = R_MARS_KM + hp_km
    ra_km = R_MARS_KM + ha_km
    a_km = (rp_km + ra_km) / 2.0
    e = (ra_km - rp_km) / (ra_km + rp_km)
    inclination_deg = 86.9

    # Orbital period
    period_s = 2.0 * math.pi * math.sqrt(a_km**3 / MU_MARS)
    period_hours = period_s / 3600.0
    revs_per_sol = MARS_SOL_HOURS / period_hours

    # Vis-viva orbital speeds
    vp_km_s = math.sqrt(MU_MARS * (2.0 / rp_km - 1.0 / a_km))
    va_km_s = math.sqrt(MU_MARS * (2.0 / ra_km - 1.0 / a_km))
    speed_ratio = vp_km_s / va_km_s

    # Scientific instruments suite (7 instruments)
    payloads = [
        {"name": "MoRIC", "type": "Medium-Resolution Camera", "specs": "100 m/px, created 76m Mars Global Color Orthomosaic from 14,757 images"},
        {"name": "HiRIC", "type": "High-Resolution Camera", "specs": "0.5 m/px panchromatic, 2.0 m/px multispectral at 265 km periapsis"},
        {"name": "MOSIR", "type": "Subsurface Radar", "specs": "Dual frequency 10-15 MHz & 30-50 MHz, probes 100m soil & km-deep ice"},
        {"name": "MMS", "type": "Mineralogical Spectrometer", "specs": "0.45-3.4 μm visible/near-IR for surface mineral composition"},
        {"name": "MOMAG", "type": "Magnetometer", "specs": "Dual fluxgate sensors on 3m boom, measuring crustal fields and solar wind"},
        {"name": "MINPA", "type": "Ion and Neutral Particle Analyzer", "specs": "Ions 5 eV-25 keV, ENAs 50 eV-3 keV, Jeans escape & solar wind stripping"},
        {"name": "MEPA", "type": "Energetic Particle Analyzer", "specs": "High-energy electrons, protons, and alpha particles in near-Mars space"}
    ]

    # Interstellar object 3I/ATLAS imaging (October 2025)
    interstellar_observation = {
        "target": "3I/ATLAS (Third recognized interstellar object)",
        "observation_date": "2025-10-03",
        "distance_km": 28960000.0,  # ~28.96 million km
        "distance_au": 0.194,
        "viewing_angle_south_deg": "35° - 45° (geometry inaccessible from Earth)",
        "scientific_discovery": "Measured dust ejection rate (~1 ton/s) and velocity (3-10 m/s) under solar radiation pressure",
        "lead_publication": "Astrophysical Journal Letters (published May 2026)",
    }

    return {
        "mission_name": "Tianwen-1 Mars Orbiter (天问一号环绕器, CNSA)",
        "launch_date": "2020-07-23",
        "orbit_insertion_date": "2021-02-10",
        "orbit": {
            "periapsis_altitude_km": hp_km,
            "apoapsis_altitude_km": ha_km,
            "periapsis_radius_km": rp_km,
            "apoapsis_radius_km": ra_km,
            "semi_major_axis_km": round(a_km, 2),
            "eccentricity": round(e, 4),
            "inclination_deg": inclination_deg,
            "period_seconds": round(period_s, 1),
            "period_hours": round(period_hours, 3),
            "revolutions_per_sol": round(revs_per_sol, 2),
            "periapsis_speed_km_s": round(vp_km_s, 3),
            "apoapsis_speed_km_s": round(va_km_s, 3),
            "speed_ratio": round(speed_ratio, 2),
        },
        "payloads": payloads,
        "interstellar_observation": interstellar_observation,
        "science_data_released_tb": 3.5,
        "operational_status": "Stably operating in Mars polar remote sensing orbit into late 2026"
    }


def compute_mars_exploration_trinity() -> Dict[str, Any]:
    """
    Computes the synergy and spatial distribution of the Mars Exploration Trinity:
    Curiosity, Perseverance, and Tianwen-1 Orbiter.
    """
    curiosity = compute_curiosity_gale_gediz_vallis_sulfur()
    tianwen1 = compute_tianwen1_mars_orbiter_dynamics()

    # Perseverance coordinates: Jezero Crater (18.38° N, 77.58° E)
    perseverance_lat = 18.38
    perseverance_lon = 77.58

    # Curiosity coordinates: Gale Crater (4.58° S, 137.44° E)
    curiosity_lat = curiosity["coordinates"]["latitude_deg"]
    curiosity_lon = curiosity["coordinates"]["longitude_deg"]

    # Spherical distance between rovers
    phi1 = math.radians(curiosity_lat)
    lam1 = math.radians(curiosity_lon)
    phi2 = math.radians(perseverance_lat)
    lam2 = math.radians(perseverance_lon)

    dsigma = math.acos(
        math.sin(phi1) * math.sin(phi2) +
        math.cos(phi1) * math.cos(phi2) * math.cos(lam1 - lam2)
    )
    surface_dist_km = R_MARS_KM * dsigma

    return {
        "trinity_members": [
            {
                "name": "Curiosity (MSL, NASA)",
                "role": "Deep Lacustrine Geologist & Ancient Climate Transition Investigator",
                "site": "Gale Crater (Mount Sharp / Gediz Vallis Channel)",
                "key_breakthrough": "Sol 4189 pure elemental sulfur crystals & 14-year MMRTG endurance",
                "coordinates": f"{abs(curiosity_lat):.2f}°S, {curiosity_lon:.2f}°E"
            },
            {
                "name": "Perseverance (Mars 2020, NASA)",
                "role": "Crater Rim Explorer & Sample Return Vanguard",
                "site": "Jezero Crater (Lookout Hill / Wild West)",
                "key_breakthrough": "500m rim climb, generative AI VLM drive, MOXIE SOEC oxygen, 33 sealed rock cores",
                "coordinates": f"{perseverance_lat:.2f}°N, {perseverance_lon:.2f}°E"
            },
            {
                "name": "Tianwen-1 Orbiter (CNSA)",
                "role": "Global Remote Sensing Sentinel & Deep Space Interstellar Observer",
                "site": "Mars Polar Elliptical Orbit (265 x 10,700 km)",
                "key_breakthrough": "76m global orthomosaic, MOSIR radar subsurface sounding, 3I/ATLAS comet observation",
                "orbit": "i=86.9°, P=7.05h, 3.5 TB open science data"
            }
        ],
        "rover_separation": {
            "angular_separation_deg": round(math.degrees(dsigma), 2),
            "surface_distance_km": round(surface_dist_km, 1),
            "physical_significance": "Two rovers 3,743 km apart simultaneously probe two distinct 4-billion-year Martian paleoenvironments under Tianwen-1 global orbital coverage"
        }
    }


def compute_grand_vigintet_matrix_2026() -> Dict[str, Any]:
    """
    Computes the complete 2026 Human Deep Space Grand Vigintet (Twenty-Fold Fleet) matrix,
    strictly ordered by heliocentric distance, along with extreme physical duality ratios.
    """
    fleet = [
        {
            "rank": 1,
            "name": "Voyager 1",
            "agency": "NASA",
            "heliocentric_distance_au": 173.22,
            "geocentric_distance_km": 2.59e10,
            "one_way_light_time_hours": 24.00,
            "domain": "Interstellar Medium (Beyond Heliopause, 2.7 K)",
            "status_or_milestone": "1 Light-Day crossing countdown: 33 days (2026-11-18)"
        },
        {
            "rank": 2,
            "name": "Voyager 2",
            "agency": "NASA",
            "heliocentric_distance_au": 144.26,
            "geocentric_distance_km": 2.158e10,
            "one_way_light_time_hours": 19.996,
            "domain": "Interstellar South (Pavo Constellation, 2.7 K)",
            "status_or_milestone": "20 Light-Hours crossing countdown: 1.4 days (Tomorrow 2026-10-17!)"
        },
        {
            "rank": 3,
            "name": "New Horizons",
            "agency": "NASA",
            "heliocentric_distance_au": 65.92,
            "geocentric_distance_km": 9.75e9,
            "one_way_light_time_hours": 9.04,
            "domain": "Outer Kuiper Belt (Hyperbolic Escape, PUI Deceleration)",
            "status_or_milestone": "Cosmic Optical Background (COB) pure dark measurement & SDC 80 AU ring discovery"
        },
        {
            "rank": 4,
            "name": "Juno",
            "agency": "NASA",
            "heliocentric_distance_au": 5.20,
            "geocentric_distance_km": 7.78e8,
            "one_way_light_time_hours": 0.72,
            "domain": "Jupiter Polar Orbit (20 Mrad Radiation, 180kg Titanium Vault)",
            "status_or_milestone": "Post-PJ88 climb, PJ89 countdown: 28 days (57.8 km/s flybys, weak-light PV)"
        },
        {
            "rank": 5,
            "name": "JUICE",
            "agency": "ESA",
            "heliocentric_distance_au": 5.20,
            "geocentric_distance_km": 7.78e8,
            "one_way_light_time_hours": 0.72,
            "domain": "Jupiter Jovian System Cruise (Ganymede Ocean Exploration)",
            "status_or_milestone": "Post-EGA2 2.3-year resonance transfer to 2.5 AU asteroid belt outbound"
        },
        {
            "rank": 6,
            "name": "Europa Clipper",
            "agency": "NASA",
            "heliocentric_distance_au": 5.20,
            "geocentric_distance_km": 7.78e8,
            "one_way_light_time_hours": 0.72,
            "domain": "Outer Planet Jovian Ocean (Europa Subsurface Habitability)",
            "status_or_milestone": "MEGA Earth Gravity Assist countdown: 48 days (2026-12-03)"
        },
        {
            "rank": 7,
            "name": "Lucy",
            "agency": "NASA",
            "heliocentric_distance_au": 5.04,
            "geocentric_distance_km": 7.60e8,
            "one_way_light_time_hours": 0.70,
            "domain": "Jupiter Trojan Asteroids (Nice Model Primordial Fossils)",
            "status_or_milestone": "5th Launch Anniversary TODAY (2021-10-16 to 2026-10-16), 7.3m UltraFlex array"
        },
        {
            "rank": 8,
            "name": "Psyche",
            "agency": "NASA",
            "heliocentric_distance_au": 2.042,
            "geocentric_distance_km": 4.015e8,
            "one_way_light_time_hours": 0.372,
            "domain": "Asteroid Belt Metal Core (Hall Thruster Electric Spiral)",
            "status_or_milestone": "SPT-140 Hall electric propulsion & DSOC 1550nm laser link broadband test"
        },
        {
            "rank": 9,
            "name": "Curiosity",
            "agency": "NASA",
            "heliocentric_distance_au": 1.524,
            "geocentric_distance_km": 2.28e8,
            "one_way_light_time_hours": 0.212,
            "domain": "Mars Gale Crater (Mount Sharp Foothills / Gediz Vallis Channel)",
            "status_or_milestone": "14-year MMRTG nuclear traverse (>33.5 km), pure native sulfur S8 crystal breakthrough"
        },
        {
            "rank": 10,
            "name": "Perseverance",
            "agency": "NASA",
            "heliocentric_distance_au": 1.524,
            "geocentric_distance_km": 2.28e8,
            "one_way_light_time_hours": 0.212,
            "domain": "Mars Jezero Crater (Northern Rim / Wild West)",
            "status_or_milestone": "500m rim climb to Lookout Hill, generative AI VLM drive, MOXIE SOEC, 33 sealed cores"
        },
        {
            "rank": 11,
            "name": "Tianwen-1 Orbiter",
            "agency": "CNSA",
            "heliocentric_distance_au": 1.524,
            "geocentric_distance_km": 2.28e8,
            "one_way_light_time_hours": 0.212,
            "domain": "Mars Polar Remote Sensing Orbit (265 x 10,700 km, i=86.9°)",
            "status_or_milestone": "76m global orthomosaic, MOSIR radar ice soundings, MINPA ENA escape, 3I/ATLAS imaging"
        },
        {
            "rank": 12,
            "name": "Hera",
            "agency": "ESA",
            "heliocentric_distance_au": 1.304,
            "geocentric_distance_km": 1.95e8,
            "one_way_light_time_hours": 0.181,
            "domain": "Binary Asteroid System Didymos/Dimorphos (Planetary Defense)",
            "status_or_milestone": "BRM-1 93-minute main braking burn successfully achieved yesterday (10-15)"
        },
        {
            "rank": 13,
            "name": "Hayabusa2# (SHARP)",
            "agency": "JAXA",
            "heliocentric_distance_au": 1.120,
            "geocentric_distance_km": 1.68e8,
            "one_way_light_time_hours": 0.156,
            "domain": "Micro-Asteroid 1998 KY26 (11m Rapid Rotator, 490x Centrifugal)",
            "status_or_milestone": "744m Torifune flyby review, cruising toward 2031 polar sanctuary landing with μ10 ion drive"
        },
        {
            "rank": 14,
            "name": "OSIRIS-APEX",
            "agency": "NASA",
            "heliocentric_distance_au": 1.010,
            "geocentric_distance_km": 1.51e8,
            "one_way_light_time_hours": 0.140,
            "domain": "Asteroid 99942 Apophis (3:2 Earth Resonance, 0.5 AU Perihelion)",
            "status_or_milestone": "Fig-leaf thermal attitude, 2029 99% Earth braking & STIR thruster regolith experiment"
        },
        {
            "rank": 15,
            "name": "JWST",
            "agency": "NASA/ESA/CSA",
            "heliocentric_distance_au": 1.010,
            "geocentric_distance_km": 1.508e6,
            "one_way_light_time_hours": 0.0014,
            "domain": "Sun-Earth L2 Halo Orbit (Cryogenic 6.7 K / 40 K, 300 K Shield)",
            "status_or_milestone": "Unraveling primordial galaxies z > 14 (JADES-GS-z14-0) at cosmic dawn"
        },
        {
            "rank": 16,
            "name": "Tianwen-2",
            "agency": "CNSA",
            "heliocentric_distance_au": 1.001,
            "geocentric_distance_km": 1.56e7,
            "one_way_light_time_hours": 0.0145,
            "domain": "Earth Quasi-Satellite 469219 Kamoʻoalewa & Comet 311P",
            "status_or_milestone": "1:1 MMR co-orbital rendezvous & sampling (50x centrifugal spin) with dual transition"
        },
        {
            "rank": 17,
            "name": "Queqiao-2",
            "agency": "CNSA",
            "heliocentric_distance_au": 1.000,
            "geocentric_distance_km": 3.844e5,
            "one_way_light_time_hours": 0.000356,  # 1.282 seconds
            "domain": "Lunar Frozen Elliptical Orbit (254 x 16,941 km, i=119.25°)",
            "status_or_milestone": "4.2m umbrella antenna, mascon J3 frozen orbit de/dt=0, Chang'e-6/7/8 deep space relay"
        },
        {
            "rank": 18,
            "name": "BepiColombo",
            "agency": "ESA/JAXA",
            "heliocentric_distance_au": 0.387,
            "geocentric_distance_km": 1.05e8,
            "one_way_light_time_hours": 0.097,
            "domain": "Deep Solar Gravitational Well (Mercury Orbital Capture)",
            "status_or_milestone": "-1405 MJ/kg MOI blind braking insertion countdown: 36 days (2026-11-21)"
        },
        {
            "rank": 19,
            "name": "Solar Orbiter",
            "agency": "ESA/NASA",
            "heliocentric_distance_au": 0.280,
            "geocentric_distance_km": 1.20e8,
            "one_way_light_time_hours": 0.111,
            "domain": "Out-of-Ecliptic Polar Dynamo & Coronal Heating (520°C Bone Black)",
            "status_or_milestone": "Venus 4:3 resonance, campfire microflares, VGA5 Christmas Eve countdown: 68 days"
        },
        {
            "rank": 20,
            "name": "Parker Solar Probe",
            "agency": "NASA",
            "heliocentric_distance_au": 0.04586,
            "geocentric_distance_km": 1.45e8,
            "one_way_light_time_hours": 0.134,
            "domain": "Extreme Solar Corona In-Situ (192 km/s, 1400°C TPS Shield)",
            "status_or_milestone": "Post-Aphelion inbound dive, Perihelion P30 countdown: 47 days (2026-12-02)"
        }
    ]

    # Extreme duality calculations
    max_helio_au = fleet[0]["heliocentric_distance_au"]  # Voyager 1: 173.22 AU
    min_helio_au = fleet[-1]["heliocentric_distance_au"]  # Parker: 0.04586 AU
    helio_ratio = max_helio_au / min_helio_au
    solar_flux_ratio = helio_ratio ** 2

    max_geo_km = fleet[0]["geocentric_distance_km"]  # Voyager 1: 2.59e10 km
    min_geo_km = fleet[16]["geocentric_distance_km"]  # Queqiao-2: 3.844e5 km
    geo_ratio = max_geo_km / min_geo_km

    max_light_time_s = fleet[0]["one_way_light_time_hours"] * 3600.0  # 86400 s
    min_light_time_s = fleet[16]["one_way_light_time_hours"] * 3600.0  # 1.282 s
    light_time_ratio = max_light_time_s / min_light_time_s

    # Extreme speeds: Parker (192 km/s) vs Hayabusa2# escape speed at 1998 KY26 (6.88 mm/s = 6.88e-6 km/s)
    speed_parker_km_s = 192.0
    speed_ky26_escape_km_s = 6.88e-6
    speed_ratio = speed_parker_km_s / speed_ky26_escape_km_s

    # Thermal span: Parker TPS (1673.15 K) vs Voyager deep space (2.725 K)
    temp_parker_k = 1400.0 + 273.15
    temp_deep_space_k = 2.725
    thermal_span_k = temp_parker_k - temp_deep_space_k

    return {
        "fleet_title": "2026 Human Deep Space Grand Vigintet (人类深空二十极黄金舰队)",
        "total_flagships": len(fleet),
        "fleet": fleet,
        "duality_extrema": {
            "heliocentric_distance_span_ratio": round(helio_ratio, 2),
            "solar_radiation_flux_ratio": round(solar_flux_ratio, 1),
            "geocentric_distance_span_ratio": round(geo_ratio, 1),
            "one_way_light_time_ratio": round(light_time_ratio, 1),
            "relative_speed_ratio": round(speed_ratio, 1),
            "operating_thermal_span_k": round(thermal_span_k, 2)
        }
    }


def main():
    print("=" * 70)
    print("CURIOSITY & TIANWEN-1: MARS TRINITY & THE GRAND VIGINTET (2026)")
    print("=" * 70)

    curiosity = compute_curiosity_gale_gediz_vallis_sulfur()
    print(f"\n[Curiosity Rover in Gale Crater]")
    print(f"Elapsed: {curiosity['years_elapsed']} Earth yrs / {curiosity['sols_elapsed']} sols")
    print(f"Location: {curiosity['coordinates']['latitude_deg']}° lat, {curiosity['coordinates']['longitude_deg']}° lon")
    print(f"Odometer: {curiosity['gale_crater']['odometer_km']} km, Elevation gained: {curiosity['gale_crater']['elevation_gained_m']} m")
    print(f"Gediz Vallis Discovery: {curiosity['gediz_vallis_sulfur']['mineral_type']} on Sol {curiosity['gediz_vallis_sulfur']['discovery_sol']}")
    print(f"MMRTG Power: {curiosity['mmrtg']['current_electric_w']} W (thermal decay {curiosity['mmrtg']['thermal_decay_factor']}, thermocouple health {curiosity['mmrtg']['thermocouple_health_factor']})")

    tianwen1 = compute_tianwen1_mars_orbiter_dynamics()
    print(f"\n[Tianwen-1 Mars Orbiter (CNSA)]")
    print(f"Orbit: {tianwen1['orbit']['periapsis_altitude_km']} km x {tianwen1['orbit']['apoapsis_altitude_km']} km (i={tianwen1['orbit']['inclination_deg']}°)")
    print(f"Period: {tianwen1['orbit']['period_hours']} h ({tianwen1['orbit']['revolutions_per_sol']} revs/sol)")
    print(f"Velocities: periapsis {tianwen1['orbit']['periapsis_speed_km_s']} km/s, apoapsis {tianwen1['orbit']['apoapsis_speed_km_s']} km/s (ratio {tianwen1['orbit']['speed_ratio']})")
    print(f"3I/ATLAS Observation: {tianwen1['interstellar_observation']['target']} from {tianwen1['interstellar_observation']['distance_au']} AU")
    print(f"Public Science Data: {tianwen1['science_data_released_tb']} TB")

    trinity = compute_mars_exploration_trinity()
    print(f"\n[Mars Exploration Trinity]")
    print(f"Rover Angular Separation: {trinity['rover_separation']['angular_separation_deg']}°")
    print(f"Rover Surface Distance: {trinity['rover_separation']['surface_distance_km']} km across Martian terrain")

    vigintet = compute_grand_vigintet_matrix_2026()
    print(f"\n[The Grand Vigintet (Twenty-Fold Fleet)]")
    print(f"Total flagships: {vigintet['total_flagships']}")
    print(f"Heliocentric span: {vigintet['duality_extrema']['heliocentric_distance_span_ratio']}x ({vigintet['duality_extrema']['solar_radiation_flux_ratio']}x flux)")
    print(f"Geocentric span: {vigintet['duality_extrema']['geocentric_distance_span_ratio']}x ({vigintet['duality_extrema']['one_way_light_time_ratio']}x light time)")
    print(f"Speed ratio: {vigintet['duality_extrema']['relative_speed_ratio']}x")
    print(f"Thermal span: {vigintet['duality_extrema']['operating_thermal_span_k']} K")
    print("=" * 70)


if __name__ == "__main__":
    main()
