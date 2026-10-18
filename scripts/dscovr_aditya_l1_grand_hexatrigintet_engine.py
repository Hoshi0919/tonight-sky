"""
DSCOVR, Aditya-L1 & The Grand Hexatrigintet Engine (2026-10-18)
==============================================================
Astrodynamics, payload physics, space weather early warning models,
and the comprehensive 36-probe deep-space armada (The Grand Hexatrigintet /
人类深空三十六极黄金舰队).

Sun-Earth L1 Lagrange Outposts:
  1. DSCOVR (NASA/NOAA/USAF, 2015): 1.5 million km L1 Lissajous orbit,
     EPIC full-disk Earth imager (10 spectral channels), PlasMag solar wind
     early warning (30-60 min geomagnetic storm lead time), NISTAR radiant budget.
  2. Aditya-L1 (ISRO, 2023/2024): 1.5 million km L1 Halo orbit (178d period),
     VELC visible emission line coronagraph (Fe XIV 530.3nm & Fe X 637.4nm, 1.05-3.0 Rsun),
     SUIT 200-400nm solar NUV disk imager, ASPEX & PAPA solar wind particle suites.

Thirty-Six Deep Space Probes (日心极距降序):
  Voyager 1, Voyager 2, New Horizons, Juno, JUICE, Europa Clipper, Lucy, Psyche,
  Mars Odyssey, Mars Express, ExoMars TGO, MAVEN, Hope, Curiosity, Perseverance,
  Tianwen-1 Orbiter, MRO, Hera, Hayabusa2#, OSIRIS-APEX, JWST, Euclid, Tianwen-2,
  LRO, Chandrayaan-2, Danuri, CAPSTONE, Queqiao-2, Chang'e-4/Yutu-2,
  SOHO, DSCOVR, Aditya-L1, STEREO-A, BepiColombo, Solar Orbiter, Parker Solar Probe.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
import math
from typing import Dict, List, Any

# Gravitational and physical constants
C_LIGHT = 299792458.0            # m/s
AU_KM = 149597870.7              # km
R_EARTH_KM = 6371.0              # Mean Earth radius in km
MAGNETOPAUSE_STANDOFF_KM = 64000.0 # ~10 Earth radii subsolar magnetopause standoff

# Epoch reference: 2026-10-18 21:30:00 CST (13:30:00 UTC)
EPOCH_2026_10_18 = datetime(2026, 10, 18, 13, 30, 0, tzinfo=timezone.utc)


@dataclass(frozen=True)
class L1ProbeState:
    name: str
    agency: str
    launch_date: str
    insertion_date: str
    orbit_type: str
    distance_from_earth_km: float
    heliocentric_distance_au: float
    cumulative_days_in_space: float
    cumulative_years_in_space: float
    cumulative_days_in_l1_orbit: float
    core_payloads: List[str]
    scientific_highlights: List[str]


def compute_dscovr_state(current_dt: datetime = EPOCH_2026_10_18) -> L1ProbeState:
    """计算 DSCOVR 深空气候观测台在轨状态与物理基准"""
    launch_dt = datetime(2015, 2, 11, 23, 3, 0, tzinfo=timezone.utc)
    arrival_dt = datetime(2015, 6, 8, 12, 0, 0, tzinfo=timezone.utc)
    
    total_days = (current_dt - launch_dt).total_seconds() / 86400.0
    orbit_days = (current_dt - arrival_dt).total_seconds() / 86400.0
    
    return L1ProbeState(
        name="DSCOVR (Deep Space Climate Observatory)",
        agency="NASA/NOAA/USAF",
        launch_date="2015-02-11",
        insertion_date="2015-06-08",
        orbit_type="Sun-Earth L1 Lissajous Orbit (1.5 million km sunward)",
        distance_from_earth_km=1500000.0,
        heliocentric_distance_au=0.990,
        cumulative_days_in_space=round(total_days, 1),
        cumulative_years_in_space=round(total_days / 365.25, 2),
        cumulative_days_in_l1_orbit=round(orbit_days, 1),
        core_payloads=[
            "EPIC (Earth Polychromatic Imaging Camera, 10 spectral channels 317-780nm)",
            "PlasMag Faraday Cup (Solar wind proton/alpha density, speed, temperature)",
            "PlasMag Fluxgate Magnetometer (High-rate 50Hz IMF Bx, By, Bz magnetic vector)",
            "NISTAR (National Institute of Standards and Technology Advanced Radiometer)",
            "PHA (Pulse Height Analyzer, microelectronic cosmic ray radiation)"
        ],
        scientific_highlights=[
            "First continuous deep-space vantage point imaging full sunlit Earth disk from 1.5M km",
            "Observed iconic Earth-Moon transits capturing the farside of the Moon crossing Earth",
            "Critical 30-60 min early warning of Earth-directed coronal mass ejections (CME) and solar storms",
            "NISTAR Earth energy imbalance (EEI) continuous radiometric monitoring"
        ]
    )


def compute_aditya_l1_state(current_dt: datetime = EPOCH_2026_10_18) -> L1ProbeState:
    """计算 Aditya-L1 太阳神空间天文台在轨状态与物理基准"""
    launch_dt = datetime(2023, 9, 2, 6, 20, 0, tzinfo=timezone.utc)
    arrival_dt = datetime(2024, 1, 6, 10, 30, 0, tzinfo=timezone.utc)
    
    total_days = (current_dt - launch_dt).total_seconds() / 86400.0
    orbit_days = (current_dt - arrival_dt).total_seconds() / 86400.0
    
    return L1ProbeState(
        name="Aditya-L1",
        agency="ISRO (Indian Space Research Organisation)",
        launch_date="2023-09-02",
        insertion_date="2024-01-06",
        orbit_type="Sun-Earth L1 Large Halo Orbit (Period ~178 days, zero occultation)",
        distance_from_earth_km=1500000.0,
        heliocentric_distance_au=0.990,
        cumulative_days_in_space=round(total_days, 1),
        cumulative_years_in_space=round(total_days / 365.25, 2),
        cumulative_days_in_l1_orbit=round(orbit_days, 1),
        core_payloads=[
            "VELC (Visible Emission Line Coronagraph, Fe XIV 530.3nm & Fe X 637.4nm, 1.05-3.0 Rsun)",
            "SUIT (Solar Ultraviolet Imaging Telescope, 11 filters 200-400nm full-disk)",
            "ASPEX (Aditya Solar wind Particle Experiment - SWIS & STEPS)",
            "PAPA (Plasma Analyser Package for Aditya)",
            "SoLEXS (Solar Low Energy X-ray Spectrometer)",
            "HEL1OS (High Energy L1 Orbiting X-ray Spectrometer)",
            "MAG (Digital Triaxial Fluxgate Magnetometers)"
        ],
        scientific_highlights=[
            "India's first dedicated space-based solar observatory positioned at L1 halo orbit",
            "VELC closes critical coronal imaging gap between chromospheric EUV and SOHO LASCO C2",
            "Fe XIV green line (2 MK) and Fe X red line (1 MK) diagnostics for coronal heating physics",
            "SUIT delivers unprecedented 200-400nm NUV full-disk solar photospheric-chromospheric dynamics"
        ]
    )


def compute_solar_wind_warning_lead_time(
    distance_l1_km: float = 1500000.0,
    magnetopause_km: float = MAGNETOPAUSE_STANDOFF_KM,
    solar_wind_speeds_kms: List[float] = None
) -> Dict[str, Any]:
    """
    计算日地 L1 哨位对地球磁层的太阳风暴/CME 提前预警时间窗口
    t_warning = (d_L1 - d_magnetopause) / v_sw
    """
    if solar_wind_speeds_kms is None:
        solar_wind_speeds_kms = [300.0, 400.0, 500.0, 600.0, 800.0, 1000.0, 1500.0, 2000.0]
    
    effective_dist_km = distance_l1_km - magnetopause_km
    
    speed_results = {}
    for v in solar_wind_speeds_kms:
        sec = effective_dist_km / v
        mins = sec / 60.0
        speed_results[f"{int(v)}_kms"] = {
            "speed_kms": v,
            "warning_seconds": round(sec, 1),
            "warning_minutes": round(mins, 2)
        }
    
    # Typical slow solar wind (400 km/s) and fast solar wind / moderate CME (800 km/s)
    slow_mins = speed_results["400_kms"]["warning_minutes"]
    fast_mins = speed_results["800_kms"]["warning_minutes"]
    extreme_cme_mins = speed_results["2000_kms"]["warning_minutes"]
    
    return {
        "l1_distance_km": distance_l1_km,
        "magnetopause_standoff_km": magnetopause_km,
        "effective_travel_distance_km": effective_dist_km,
        "typical_slow_wind_warning_mins": slow_mins,
        "typical_fast_wind_warning_mins": fast_mins,
        "extreme_cme_warning_mins": extreme_cme_mins,
        "speed_breakdown": speed_results
    }


def the_grand_hexatrigintet_fleet_census() -> Dict[str, Any]:
    """
    2026 人类深空三十六极黄金舰队 (The Grand Hexatrigintet) 全景普查矩阵
    严格按日心极距降序排列 (36 艘现役旗舰)
    """
    fleet = [
        {"rank": 1, "name": "Voyager 1", "agency": "NASA", "dist_au": 173.22, "arena": "Interstellar Frontier",
         "role": "Humanity's farthest emissary, 24.01 light-hours one-way, interstellar plasma wave detection"},
        {"rank": 2, "name": "Voyager 2", "agency": "NASA", "dist_au": 144.29, "arena": "Interstellar Frontier",
         "role": "20.00 light-hours crossed (2026-10-18), intact cosmic ray & magnetometer interstellar stream"},
        {"rank": 3, "name": "New Horizons", "agency": "NASA", "dist_au": 65.92, "arena": "Kuiper Belt & Beyond",
         "role": "Outer heliosphere COB dust, pickup ions (PUI), Kuiper Belt Object high-phase photometry"},
        {"rank": 4, "name": "Juno", "agency": "NASA", "dist_au": 5.20, "arena": "Jovian System",
         "role": "Titanium radiation vault, Io close flybys, polar magnetosphere & Jupiter gravity mapping"},
        {"rank": 5, "name": "JUICE", "agency": "ESA", "dist_au": 5.20, "arena": "Outer Solar System Cruise",
         "role": "En route to Jupiter/Ganymede, dual Earth-Moon gravity assist completed, 2031 arrival"},
        {"rank": 6, "name": "Europa Clipper", "agency": "NASA", "dist_au": 5.20, "arena": "Outer Solar System Cruise",
         "role": "En route to Europa habitability reconnaissance, REASON ice radar, 2030 arrival"},
        {"rank": 7, "name": "Lucy", "agency": "NASA", "dist_au": 5.04, "arena": "Jupiter Trojan Swarms",
         "role": "12-year odyssey to Jupiter L4/L5 Trojans, Dinkinesh & Donaldjohanson visited, UltraFlex solar"},
        {"rank": 8, "name": "Psyche", "agency": "NASA", "dist_au": 2.042, "arena": "Main Asteroid Belt Cruise",
         "role": "SPT-140 Hall-effect propulsion, DSOC deep-space optical comms, 16 Psyche metal core explorer"},
        {"rank": 9, "name": "2001 Mars Odyssey", "agency": "NASA", "dist_au": 1.579, "arena": "Martian Orbit",
         "role": "Quarter-century 25th orbit anniversary, GRS subsurface hydrogen ice, THEMIS IR thermal mapping"},
        {"rank": 10, "name": "Mars Express", "agency": "ESA", "dist_au": 1.579, "arena": "Martian Orbit",
         "role": "23 years active, MARSIS subsurface radar ice/brine sounding, Phobos grazing encounters"},
        {"rank": 11, "name": "ExoMars TGO", "agency": "ESA/Roscosmos", "dist_au": 1.579, "arena": "Martian Orbit",
         "role": "Decennial 10-year milestone, NOMAD/ACS trace gases, atmospheric HCl discovery, FREND 40% water oasis"},
        {"rank": 12, "name": "MAVEN", "agency": "NASA", "dist_au": 1.579, "arena": "Martian Upper Atmosphere",
         "role": "Upper atmosphere escape dynamics, solar wind stripping of CO2/H2O, periapsis dips to 125km"},
        {"rank": 13, "name": "Hope Probe (Al-Amal)", "agency": "UAESA", "dist_au": 1.579, "arena": "Martian High Orbit",
         "role": "55-hour high elliptical synoptic weather orbit, Deimos historic ultra-close 100km flybys"},
        {"rank": 14, "name": "Curiosity (MSL)", "agency": "NASA", "dist_au": 1.524, "arena": "Martian Surface",
         "role": "Gale crater, 14.2 years roving, Gediz Vallis pure elemental sulfur crystal breakthrough"},
        {"rank": 15, "name": "Perseverance", "agency": "NASA", "dist_au": 1.524, "arena": "Martian Surface",
         "role": "Jezero crater delta & crater rim climb, AutoNav visual odometry, sample return caching"},
        {"rank": 16, "name": "Tianwen-1 Orbiter", "agency": "CNSA", "dist_au": 1.524, "arena": "Martian Orbit",
         "role": "Comprehensive global high-res remote sensing, sub-surface radar polar cap layering"},
        {"rank": 17, "name": "MRO (Mars Reconnaissance Orbiter)", "agency": "NASA", "dist_au": 1.524, "arena": "Martian Orbit",
         "role": "0.3m HiRISE imaging, SHARAD sub-surface polar layering radar, primary relay backbone"},
        {"rank": 18, "name": "Hera", "agency": "ESA", "dist_au": 1.304, "arena": "Near-Earth Asteroid Cruise",
         "role": "Post-DART impact forensic probe to Didymos & Dimorphos, planetary defense verification"},
        {"rank": 19, "name": "Hayabusa2# (SHARP)", "agency": "JAXA", "dist_au": 1.120, "arena": "Extended Asteroid Cruise",
         "role": "Extended mission to fast-rotating micro-asteroid 1998 KY26, ion engine cruise"},
        {"rank": 20, "name": "OSIRIS-APEX", "agency": "NASA", "dist_au": 1.010, "arena": "Near-Earth Asteroid Cruise",
         "role": "En route to asteroid 99942 Apophis April 2029 Earth close encounter, thruster surface stirring"},
        {"rank": 21, "name": "JWST", "agency": "NASA/ESA/CSA", "dist_au": 1.010, "arena": "Sun-Earth L2 Halo Orbit",
         "role": "6.5m beryllium mirror, 6.7K cryogenic MIRI, early universe reionization & exoplanet transit"},
        {"rank": 22, "name": "Euclid", "agency": "ESA/NASA", "dist_au": 1.010, "arena": "Sun-Earth L2 Halo Orbit",
         "role": "Dark energy & dark matter mapper, 15,000 deg^2 weak gravitational lensing, VIS/NISP survey"},
        {"rank": 23, "name": "Tianwen-2", "agency": "CNSA", "dist_au": 1.001, "arena": "Near-Earth Asteroid / Comet Cruise",
         "role": "Targeting quasi-satellite 469219 Kamo`oalewa for sample return & main-belt comet 311P"},
        {"rank": 24, "name": "LRO (Lunar Reconnaissance Orbiter)", "agency": "NASA", "dist_au": 1.000, "arena": "Lunar Polar Orbit",
         "role": "17.3 years in quasi-frozen polar orbit, Diviner 26.0K Hermite crater solar system cold pole, LOLA 3D"},
        {"rank": 25, "name": "Chandrayaan-2 Orbiter", "agency": "ISRO", "dist_au": 1.000, "arena": "Lunar Polar Orbit",
         "role": "0.25m OHRC highest lunar optical resolution, DFSAR dual-frequency full-pol radar, CLASS Na map"},
        {"rank": 26, "name": "Danuri (KPLO)", "agency": "KARI/NASA", "dist_au": 1.000, "arena": "Lunar Polar Orbit",
         "role": "BLT low-energy transfer, ShadowCam 200x ultra-sensitive PSR imager, PolCam lunar polarimetry"},
        {"rank": 27, "name": "CAPSTONE", "agency": "NASA/Rocket Lab", "dist_au": 1.000, "arena": "Cislunar NRHO",
         "role": "12U CubeSat in 9:2 NRHO halo orbit, Gateway orbit pathfinder, 2.5 m/s/yr stationkeeping"},
        {"rank": 28, "name": "Queqiao-2", "agency": "CNSA", "dist_au": 1.000, "arena": "Cislunar Frozen Elliptical",
         "role": "4.2m umbrella mesh antenna, 54.8° critical frozen inclination, Chang'e-6/7/8 South Pole & farside relay"},
        {"rank": 29, "name": "Chang'e-4 / Yutu-2", "agency": "CNSA", "dist_au": 1.000, "arena": "Lunar Farside Surface",
         "role": "Farside Von Kármán crater, 7.8 years surviving 96+ lunar days, LPR sub-surface radar, 0.1-40MHz LFS"},
        {"rank": 30, "name": "SOHO", "agency": "ESA/NASA", "dist_au": 0.990, "arena": "Sun-Earth L1 Halo Orbit",
         "role": "31 years active, LASCO C2/C3 coronagraphs, 5,000+ sungrazing comets discovered, real-time CME tracker"},
        {"rank": 31, "name": "DSCOVR", "agency": "NASA/NOAA/USAF", "dist_au": 0.990, "arena": "Sun-Earth L1 Lissajous Orbit",
         "role": "EPIC continuous full sunlit Earth disk 10-channel imager, PlasMag 30-60 min geomagnetic storm early warning"},
        {"rank": 32, "name": "Aditya-L1", "agency": "ISRO", "dist_au": 0.990, "arena": "Sun-Earth L1 Halo Orbit",
         "role": "VELC low-coronal Fe XIV/X emission line coronagraph, SUIT 200-400nm full-disk solar NUV imager"},
        {"rank": 33, "name": "STEREO-A", "agency": "NASA", "dist_au": 0.962, "arena": "Heliocentric Orbit",
         "role": "20 years in orbit, 3D heliospheric stereoscopy, SECCHI imaging, ahead of Earth in heliocentric path"},
        {"rank": 34, "name": "BepiColombo", "agency": "ESA/JAXA", "dist_au": 0.387, "arena": "Inner Solar System Cruise",
         "role": "Mercury gravity well capture, -1405 MJ/kg MOI blind insertion approach countdown in 34 days"},
        {"rank": 35, "name": "Solar Orbiter", "agency": "ESA/NASA", "dist_au": 0.280, "arena": "High-Inclination Solar",
         "role": "Out-of-ecliptic polar imaging, 520°C bone-black heat shield, Christmas Eve VGA5 in 67 days"},
        {"rank": 36, "name": "Parker Solar Probe", "agency": "NASA", "dist_au": 0.046, "arena": "Solar Corona In-Situ",
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
        "fleet_name": "The Grand Hexatrigintet (人类深空三十六极黄金舰队)",
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


def sun_earth_l1_armada_summary() -> Dict[str, Any]:
    """生成日地 L1 三大深空前哨与空间天气预警网络综合分析"""
    dscovr = compute_dscovr_state()
    aditya = compute_aditya_l1_state()
    warning = compute_solar_wind_warning_lead_time()
    fleet = the_grand_hexatrigintet_fleet_census()
    
    return {
        "system_name": "Sun-Earth L1 Space Weather & Solar-Terrestrial Trio (日地L1空间天气与日地三杰)",
        "epoch": "2026-10-18 21:30 CST",
        "dscovr": {
            "name": dscovr.name,
            "agency": dscovr.agency,
            "cumulative_years": dscovr.cumulative_years_in_space,
            "cumulative_l1_days": dscovr.cumulative_days_in_l1_orbit,
            "orbit": dscovr.orbit_type,
            "payloads": dscovr.core_payloads,
            "highlights": dscovr.scientific_highlights
        },
        "aditya_l1": {
            "name": aditya.name,
            "agency": aditya.agency,
            "cumulative_years": aditya.cumulative_years_in_space,
            "cumulative_l1_days": aditya.cumulative_days_in_l1_orbit,
            "orbit": aditya.orbit_type,
            "payloads": aditya.core_payloads,
            "highlights": aditya.scientific_highlights
        },
        "space_weather_early_warning": {
            "lead_time_slow_solar_wind_mins": warning["typical_slow_wind_warning_mins"],
            "lead_time_fast_solar_wind_mins": warning["typical_fast_wind_warning_mins"],
            "lead_time_extreme_cme_mins": warning["extreme_cme_warning_mins"]
        },
        "fleet_status": {
            "name": fleet["fleet_name"],
            "probe_count": fleet["probe_count"],
            "extremes": fleet["extremes"]
        }
    }


if __name__ == "__main__":
    import json
    summary = sun_earth_l1_armada_summary()
    print("=== SUN-EARTH L1 ARMADA & THE GRAND HEXATRIGINTET ===")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
