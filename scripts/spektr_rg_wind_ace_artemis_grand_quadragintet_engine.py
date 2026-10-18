"""
Spektr-RG, Wind, ACE, ARTEMIS P1/P2 & The Grand Unoctoquadragintet Engine (2026-10-19)
=====================================================================================
Astrodynamics, high-energy X-ray astrophysics, comprehensive solar wind kinetics,
lunar wake plasma dynamics, and the complete 41-probe deep-space armada
(The Grand Unoctoquadragintet / 人类深空四十一极黄金舰队).

Core Missions Highlighted:
  1. Spektr-RG (SRG, Roscosmos/IKI & DLR/MPE, 2019):
     Sun-Earth L2 Halo Orbit (1.5 million km anti-sunward, 1.010 AU).
     ART-XC 4-30 keV hard X-ray Wolter-I mirror concentrators + eROSITA 0.3-10 keV soft X-ray.
     >3 million X-ray sources, cosmic web large-scale structure & dark energy cosmology.
     Completes the Sun-Earth L2 Astronomy Trinity: JWST (IR) + Euclid (VIS/NIR) + Spektr-RG (X-ray).

  2. Wind Spacecraft (NASA, 1994):
     Sun-Earth L1 Halo Orbit (1.5 million km sunward, 0.990 AU).
     31.96 years continuous service (near 32-year milestone, launched 1994-11-01).
     WAVES radio/plasma waves (0.02 Hz - 14 MHz), Konus gamma-ray burst omnidirectional monitor
     (IPN triangulation backbone), SWE Faraday cups, EPACT energetic particles. 8000+ publications.

  3. ACE (Advanced Composition Explorer, NASA, 1997):
     Sun-Earth L1 Lissajous Orbit (0.990 AU).
     29.15 years continuous service (launched 1997-08-25, operable to ~2029).
     CRIS/SIS cosmic ray isotopic composition (Z=2-30, Ni-59 radioactive clock proves >10^5 yr delay),
     RTSW real-time space weather beacon to NOAA SWPC, SWEPAM/MAG solar wind & IMF Bz monitoring.
     With SOHO, DSCOVR, and Aditya-L1, forms the Sun-Earth L1 Heliospheric Pentad (日地 L1 五大先锋).

  4. ARTEMIS P1 & P2 (THEMIS-B & THEMIS-C, NASA, 2007/2011):
     Highly eccentric lunar orbits (hp ~ 100-200 km, ha ~ 18,000-19,000 km, T ~ 26-28 h).
     In lunar orbit for > 15.25 years (5,590+ days, LOI in June/July 2011).
     Dual-probe plasma physics constellation: nightside lunar wake ambipolar expansion,
     lunar crustal magnetic anomaly mini-magnetospheres, and terrestrial magnetotail reconnection.
     Expands the lunar fleet to The Lunar Octet (月球现役八大金刚).

Comprehensive Forty-One Deep Space Armada (日心极距降序):
  Voyager 1, Voyager 2, New Horizons, Juno, JUICE, Europa Clipper, Lucy, Psyche,
  Mars Odyssey, Mars Express, ExoMars TGO, MAVEN, Hope, Curiosity, Perseverance,
  Tianwen-1 Orbiter, MRO, Hera, Hayabusa2#, OSIRIS-APEX, JWST, Euclid, Spektr-RG,
  Tianwen-2, LRO, Chandrayaan-2, Danuri, CAPSTONE, Queqiao-2, Chang'e-4/Yutu-2,
  ARTEMIS P1, ARTEMIS P2, SOHO, Wind, ACE, DSCOVR, Aditya-L1,
  STEREO-A, BepiColombo, Solar Orbiter, Parker Solar Probe.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
import math
from typing import Dict, List, Any

# Fundamental physical constants
C_LIGHT = 299792458.0              # m/s
AU_KM = 149597870.7                # km
R_EARTH_KM = 6371.0                # Mean Earth radius in km
R_MOON_KM = 1737.4                 # Mean Lunar radius in km
MU_MOON = 4902.800066              # Lunar gravitational parameter G*M_moon in km^3/s^2

# Epoch reference: 2026-10-19 01:30:00 CST (2026-10-18 17:30:00 UTC)
EPOCH_2026_10_19 = datetime(2026, 10, 18, 17, 30, 0, tzinfo=timezone.utc)


@dataclass(frozen=True)
class DeepSpaceProbeState:
    name: str
    agency: str
    launch_date: str
    arrival_or_loi_date: str
    orbit_type: str
    distance_from_earth_km: float
    heliocentric_distance_au: float
    cumulative_days_in_space: float
    cumulative_years_in_space: float
    cumulative_days_in_target_orbit: float
    core_payloads: List[str]
    scientific_highlights: List[str]


def compute_spektr_rg_state(current_dt: datetime = EPOCH_2026_10_19) -> DeepSpaceProbeState:
    """计算 Spektr-RG 空间高能天文台在轨状态与物理基准"""
    launch_dt = datetime(2019, 7, 13, 12, 31, 0, tzinfo=timezone.utc)
    arrival_dt = datetime(2019, 10, 21, 15, 0, 0, tzinfo=timezone.utc)
    
    total_days = (current_dt - launch_dt).total_seconds() / 86400.0
    orbit_days = (current_dt - arrival_dt).total_seconds() / 86400.0
    
    return DeepSpaceProbeState(
        name="Spektr-RG (Spectrum-X-Gamma)",
        agency="Roscosmos/IKI & DLR/MPE",
        launch_date="2019-07-13",
        arrival_or_loi_date="2019-10-21",
        orbit_type="Sun-Earth L2 Halo Orbit (1.5 million km anti-sunward)",
        distance_from_earth_km=1500000.0,
        heliocentric_distance_au=1.010,
        cumulative_days_in_space=round(total_days, 1),
        cumulative_years_in_space=round(total_days / 365.25, 2),
        cumulative_days_in_target_orbit=round(orbit_days, 1),
        core_payloads=[
            "ART-XC (Astronomical Roentgen Telescope – X-ray Concentrator, 4-30 keV, 7 Wolter-I mirror arrays)",
            "eROSITA (extended Roentgen Survey with an Imaging Telescope Array, 0.3-10 keV, 7 Wolter-I mirror assemblies)"
        ],
        scientific_highlights=[
            "Completed 4+ full-sky all-sky surveys in soft and hard X-rays",
            "Cataloged > 3 million X-ray point sources (predominantly AGNs/supermassive black holes)",
            "Mapped large-scale cosmic web filaments and hundreds of thousands of galaxy clusters",
            "Completes the Sun-Earth L2 Astronomy Trinity: JWST (IR) + Euclid (VIS/NIR) + Spektr-RG (X-ray)"
        ]
    )


def compute_wind_state(current_dt: datetime = EPOCH_2026_10_19) -> DeepSpaceProbeState:
    """计算 Wind 风号航天器在轨状态与物理基准"""
    launch_dt = datetime(1994, 11, 1, 9, 31, 0, tzinfo=timezone.utc)
    l1_halo_dt = datetime(2020, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    
    total_days = (current_dt - launch_dt).total_seconds() / 86400.0
    orbit_days = (current_dt - l1_halo_dt).total_seconds() / 86400.0
    
    return DeepSpaceProbeState(
        name="Wind",
        agency="NASA",
        launch_date="1994-11-01",
        arrival_or_loi_date="1994-11-01",
        orbit_type="Sun-Earth L1 Halo Orbit (1.5 million km sunward)",
        distance_from_earth_km=1500000.0,
        heliocentric_distance_au=0.990,
        cumulative_days_in_space=round(total_days, 1),
        cumulative_years_in_space=round(total_days / 365.25, 2),
        cumulative_days_in_target_orbit=round(orbit_days, 1),
        core_payloads=[
            "WAVES (Radio and Plasma Wave Experiment: 0.02 Hz to 14 MHz dipole antennas)",
            "Konus (Omnidirectional hard X-ray / Gamma-Ray Burst Spectrometer 10 keV - 10 MeV)",
            "SWE (Solar Wind Experiment: Faraday cups, vector ion/electron spectrometers)",
            "EPACT (Energetic Particles: LEMT, STEP, IT, APE telescopes)"
        ],
        scientific_highlights=[
            "Nearly 32 years of continuous operational service in interplanetary space",
            "Over 8,000 refereed scientific publications powered by Wind data",
            "Foundational timing anchor for Interplanetary Network (IPN) triangulation of cosmic GRBs",
            "Pioneering collisionless shock physics, kinetic turbulence, and solar radio burst classification"
        ]
    )


def compute_ace_state(current_dt: datetime = EPOCH_2026_10_19) -> DeepSpaceProbeState:
    """计算 ACE 高级成分探测器在轨状态与物理基准"""
    launch_dt = datetime(1997, 8, 25, 14, 39, 0, tzinfo=timezone.utc)
    arrival_dt = datetime(1998, 1, 21, 12, 0, 0, tzinfo=timezone.utc)
    
    total_days = (current_dt - launch_dt).total_seconds() / 86400.0
    orbit_days = (current_dt - arrival_dt).total_seconds() / 86400.0
    
    return DeepSpaceProbeState(
        name="ACE (Advanced Composition Explorer)",
        agency="NASA",
        launch_date="1997-08-25",
        arrival_or_loi_date="1998-01-21",
        orbit_type="Sun-Earth L1 Lissajous Orbit (1.5 million km sunward)",
        distance_from_earth_km=1480000.0,
        heliocentric_distance_au=0.990,
        cumulative_days_in_space=round(total_days, 1),
        cumulative_years_in_space=round(total_days / 365.25, 2),
        cumulative_days_in_target_orbit=round(orbit_days, 1),
        core_payloads=[
            "CRIS (Cosmic Ray Isotope Spectrometer: Z=2 to 30 nuclei, 100-500 MeV/nucleon)",
            "SIS (Solar Isotope Spectrometer: Z=2 to 30, 10-100 MeV/nucleon)",
            "SWEPAM & MAG (Solar Wind Electron, Proton & Alpha Monitor, Fluxgate Magnetometer)",
            "RTSW (Real-Time Solar Wind continuous space weather beacon)",
            "ULEIS, SWICS, SWIMS, EPAM (Suprathermal & solar wind composition)"
        ],
        scientific_highlights=[
            "29.15 years of uninterrupted space weather watch and cosmic ray spectroscopy",
            "Used radioactive clock Ni-59 -> Co-59 (T_1/2 = 7.6*10^4 yr) to prove >10^5 yr delay before cosmic ray acceleration",
            "Continuous 24/7 RTSW solar wind and IMF Bz data stream to NOAA SWPC",
            "Adequate propellant reserves to sustain operations into 2029"
        ]
    )


def compute_artemis_pair_state(current_dt: datetime = EPOCH_2026_10_19) -> Dict[str, DeepSpaceProbeState]:
    """计算 ARTEMIS P1 与 P2 (THEMIS-B & C) 双星绕月轨道状态与物理基准"""
    launch_dt = datetime(2007, 2, 17, 23, 1, 0, tzinfo=timezone.utc)
    p1_loi = datetime(2011, 6, 27, 14, 0, 0, tzinfo=timezone.utc)
    p2_loi = datetime(2011, 7, 17, 20, 0, 0, tzinfo=timezone.utc)
    
    total_days = (current_dt - launch_dt).total_seconds() / 86400.0
    p1_orbit_days = (current_dt - p1_loi).total_seconds() / 86400.0
    p2_orbit_days = (current_dt - p2_loi).total_seconds() / 86400.0
    
    payloads = [
        "FGM (Fluxgate Magnetometer, 0.01 nT sensitivity, 128 vectors/s)",
        "ESA (Electrostatic Analyzer: electrons & ions from 3 eV to 30 keV)",
        "SST (Solid State Telescope: energetic ions & electrons 25 keV to 6 MeV)",
        "EFI (Electric Field Instrument: four 20m radial wire booms & 2 axial stanchions)",
        "SCM (Search Coil Magnetometer: AC magnetic fields up to 4 kHz)"
    ]
    
    highlights = [
        "Over 15.25 years of continuous multi-probe plasma observations in lunar orbit",
        "Discovered ambipolar electric field acceleration in the nightside lunar wake",
        "Quantified solar wind proton reflection (10-50%) at crustal magnetic anomalies (e.g., Reiner Gamma)",
        "Continuous 4-day monthly observation of terrestrial magnetotail reconnection at X_GSM ~ -60 Re"
    ]
    
    p1 = DeepSpaceProbeState(
        name="ARTEMIS P1 (THEMIS-B)",
        agency="NASA",
        launch_date="2007-02-17",
        arrival_or_loi_date="2011-06-27",
        orbit_type="Eccentric Lunar Retrograde Orbit (hp ~ 100 km, ha ~ 18,000 km, T ~ 26.5h)",
        distance_from_earth_km=384400.0,
        heliocentric_distance_au=1.000,
        cumulative_days_in_space=round(total_days, 1),
        cumulative_years_in_space=round(total_days / 365.25, 2),
        cumulative_days_in_target_orbit=round(p1_orbit_days, 1),
        core_payloads=payloads,
        scientific_highlights=highlights
    )
    
    p2 = DeepSpaceProbeState(
        name="ARTEMIS P2 (THEMIS-C)",
        agency="NASA",
        launch_date="2007-02-17",
        arrival_or_loi_date="2011-07-17",
        orbit_type="Eccentric Lunar Prograde Orbit (hp ~ 100 km, ha ~ 19,000 km, T ~ 27.5h)",
        distance_from_earth_km=384400.0,
        heliocentric_distance_au=1.000,
        cumulative_days_in_space=round(total_days, 1),
        cumulative_years_in_space=round(total_days / 365.25, 2),
        cumulative_days_in_target_orbit=round(p2_orbit_days, 1),
        core_payloads=payloads,
        scientific_highlights=highlights
    )
    
    return {"P1": p1, "P2": p2}


def compute_plasma_frequency_khz(electron_density_cm3: float) -> float:
    """
    计算太阳风等离子体特征频率 f_pe:
    f_pe = (1 / 2pi) * sqrt(n_e * e^2 / (epsilon_0 * m_e)) ~ 8.98 * sqrt(n_e [cm^-3]) kHz
    Wind WAVES 仪器以此共振截止峰直接反演太阳风瞬时电子密度。
    """
    return 8.98 * math.sqrt(electron_density_cm3)


def compute_lunar_wake_mach_number(v_sw_kms: float = 400.0, c_s_kms: float = 40.0) -> float:
    """计算太阳风流向月球的超声速马赫数 Ms = v_sw / c_s"""
    return v_sw_kms / c_s_kms


def the_sun_earth_l1_pentad() -> List[Dict[str, Any]]:
    """日地 L1 空间天气五大先锋旗舰 (The L1 Heliospheric Pentad)"""
    return [
        {"name": "SOHO", "agency": "ESA/NASA", "launch_year": 1995, "role": "Coronagraph CME monitoring & sungrazing comets"},
        {"name": "Wind", "agency": "NASA", "launch_year": 1994, "role": "WAVES radio/plasma laboratory & Konus IPN GRB timing"},
        {"name": "ACE", "agency": "NASA", "launch_year": 1997, "role": "CRIS/SIS cosmic ray isotopes & RTSW space weather alerts"},
        {"name": "DSCOVR", "agency": "NASA/NOAA/USAF", "launch_year": 2015, "role": "EPIC full-disk Earth imaging & PlasMag CME warning"},
        {"name": "Aditya-L1", "agency": "ISRO", "launch_year": 2023, "role": "VELC Fe emission line coronagraph & SUIT NUV imager"}
    ]


def the_sun_earth_l2_trinity() -> List[Dict[str, Any]]:
    """日地 L2 空间巡天三大天文台对偶矩阵 (The L2 Space Observatory Trinity)"""
    return [
        {"name": "JWST", "agency": "NASA/ESA/CSA", "wavelength": "Infrared (0.6 - 28 um)", "aperture_m": 6.5, "focus": "Cosmic dawn & exoplanet atmospheres"},
        {"name": "Euclid", "agency": "ESA/NASA", "wavelength": "Visible / NIR (0.55 - 2.0 um)", "aperture_m": 1.2, "focus": "Dark universe weak lensing & cosmic web"},
        {"name": "Spektr-RG", "agency": "Roscosmos/IKI & DLR", "wavelength": "X-ray (0.3 - 30 keV)", "aperture_m": "Wolter-I Grazing Incidence", "focus": "All-sky cluster growth, AGN & dark energy"}
    ]


def the_lunar_octet() -> List[Dict[str, Any]]:
    """月球现役八大金刚 (The Lunar Octet)"""
    return [
        {"name": "LRO", "agency": "NASA", "orbit": "Polar Orbit (50 km)", "role": "0.5m LROC imaging, LOLA altimetry, Diviner cold pole"},
        {"name": "Chandrayaan-2", "agency": "ISRO", "orbit": "Polar Orbit (100 km)", "role": "0.25m OHRC high-res optical, DFSAR SAR polar ice"},
        {"name": "Danuri (KPLO)", "agency": "KARI/NASA", "orbit": "Polar Orbit (100 km)", "role": "ShadowCam PSR imaging, PolCam lunar polarimetry"},
        {"name": "CAPSTONE", "agency": "NASA/Rocket Lab", "orbit": "Near-Rectilinear Halo Orbit (NRHO)", "role": "Gateway pathfinder, 9:2 resonance orbit maintenance"},
        {"name": "Queqiao-2", "agency": "CNSA", "orbit": "Frozen Elliptical Relay Orbit", "role": "4.2m umbrella antenna, Chang'e-6/7/8 farside & south pole relay"},
        {"name": "Chang'e-4 / Yutu-2", "agency": "CNSA", "orbit": "Farside Von Karman Surface", "role": "7.8 years surviving on farside, LPR radar, VLF radio"},
        {"name": "ARTEMIS P1", "agency": "NASA", "orbit": "Eccentric Retrograde Orbit", "role": "15+ years lunar wake plasma cavity & crustal magnetic shielding"},
        {"name": "ARTEMIS P2", "agency": "NASA", "orbit": "Eccentric Prograde Orbit", "role": "15+ years dual-point magnetotail reconnection & turbulence"}
    ]


def the_grand_unoctoquadragintet_fleet_census() -> Dict[str, Any]:
    """
    2026 人类深空四十一极黄金舰队 (The Grand Unoctoquadragintet) 全景普查
    严格按日心极距降序 (Heliocentric Distance Descending Order) 排列之 41 艘现役主力深空器。
    """
    fleet = [
        {"rank": 1, "name": "Voyager 1", "agency": "NASA", "dist_au": 173.22, "arena": "Interstellar Boundary",
         "role": "Farthest human artifact, 1 light-day milestone in 31 days, 2.7K interstellar plasma"},
        {"rank": 2, "name": "Voyager 2", "agency": "NASA", "dist_au": 144.29, "arena": "Interstellar Deep Space",
         "role": "Passed historic 20 light-hours milestone on 2026-10-18, heliopause magnetic bridge"},
        {"rank": 3, "name": "New Horizons", "agency": "NASA", "dist_au": 65.92, "arena": "Kuiper Belt / Interstellar Escape",
         "role": "Hyperbolic escape, cosmic optical background (COB), pickup ion deceleration"},
        {"rank": 4, "name": "Juno", "agency": "NASA", "dist_au": 5.20, "arena": "Jovian Polar Orbit",
         "role": "180kg titanium vault, 57.8 km/s perijove, Jovian deep interior dynamo"},
        {"rank": 5, "name": "JUICE", "agency": "ESA", "dist_au": 5.20, "arena": "Jovian System Cruise",
         "role": "Ganymede subsurface ocean explorer, 85m^2 solar arrays, 2.3-year resonance cruise"},
        {"rank": 6, "name": "Europa Clipper", "agency": "NASA", "dist_au": 5.20, "arena": "Jovian System Cruise",
         "role": "Europa habitability, MEGA trajectory, Earth flyby in 46 days"},
        {"rank": 7, "name": "Lucy", "agency": "NASA", "dist_au": 5.04, "arena": "Jupiter Trojans Cruise",
         "role": "7.3m UltraFlex solar wings, exploring primordial Trojan planetesimals"},
        {"rank": 8, "name": "Psyche", "agency": "NASA", "dist_au": 2.042, "arena": "Main-Belt Asteroid Cruise",
         "role": "Targeting 16 Psyche metal core, SPT-140 Hall-effect propulsion, DSOC optical link"},
        {"rank": 9, "name": "2001 Mars Odyssey", "agency": "NASA", "dist_au": 1.579, "arena": "Martian Orbit",
         "role": "25-year silver jubilee countdown in 5 days, GRS subsurface ice discoverer, THEMIS"},
        {"rank": 10, "name": "Mars Express", "agency": "ESA", "dist_au": 1.579, "arena": "Martian Polar Elliptical",
         "role": "23 years in orbit, MARSIS 5km radar, Phobos 45km flyby (30.6% rubble pile), OMEGA"},
        {"rank": 11, "name": "ExoMars TGO", "agency": "ESA/Roscosmos", "dist_au": 1.579, "arena": "Martian Orbit",
         "role": "10-year decennial anniversary TODAY (2026-10-19), 50 pptv methane limit, HCl discovery"},
        {"rank": 12, "name": "MAVEN", "agency": "NASA", "dist_au": 1.579, "arena": "Martian Elliptical Orbit",
         "role": "12 years measuring Mars atmospheric escape, D/H fractionation, coronal heating"},
        {"rank": 13, "name": "Hope Probe (Al-Amal)", "agency": "UAE Space Agency", "dist_au": 1.579, "arena": "Martian High Orbit",
         "role": "55h global diurnal weather cycle, EXI/EMUS/EMIRS synoptic imaging, Deimos 100km flyby"},
        {"rank": 14, "name": "Curiosity", "agency": "NASA", "dist_au": 1.524, "arena": "Martian Surface",
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
        {"rank": 23, "name": "Spektr-RG", "agency": "Roscosmos/IKI & DLR", "dist_au": 1.010, "arena": "Sun-Earth L2 Halo Orbit",
         "role": "7+ years all-sky hard/soft X-ray survey, ART-XC & eROSITA, cosmic web cluster growth"},
        {"rank": 24, "name": "Tianwen-2", "agency": "CNSA", "dist_au": 1.001, "arena": "Near-Earth Asteroid / Comet Cruise",
         "role": "Targeting quasi-satellite 469219 Kamo`oalewa for sample return & main-belt comet 311P"},
        {"rank": 25, "name": "LRO (Lunar Reconnaissance Orbiter)", "agency": "NASA", "dist_au": 1.000, "arena": "Lunar Polar Orbit",
         "role": "17.3 years in quasi-frozen polar orbit, Diviner 26.0K Hermite crater solar system cold pole, LOLA 3D"},
        {"rank": 26, "name": "Chandrayaan-2 Orbiter", "agency": "ISRO", "dist_au": 1.000, "arena": "Lunar Polar Orbit",
         "role": "0.25m OHRC highest lunar optical resolution, DFSAR dual-frequency full-pol radar, CLASS Na map"},
        {"rank": 27, "name": "Danuri (KPLO)", "agency": "KARI/NASA", "dist_au": 1.000, "arena": "Lunar Polar Orbit",
         "role": "BLT low-energy transfer, ShadowCam 200x ultra-sensitive PSR imager, PolCam lunar polarimetry"},
        {"rank": 28, "name": "CAPSTONE", "agency": "NASA/Rocket Lab", "dist_au": 1.000, "arena": "Cislunar NRHO",
         "role": "12U CubeSat in 9:2 NRHO halo orbit, Gateway orbit pathfinder, 2.5 m/s/yr stationkeeping"},
        {"rank": 29, "name": "Queqiao-2", "agency": "CNSA", "dist_au": 1.000, "arena": "Cislunar Frozen Elliptical",
         "role": "4.2m umbrella mesh antenna, 54.8° critical frozen inclination, Chang'e-6/7/8 South Pole & farside relay"},
        {"rank": 30, "name": "Chang'e-4 / Yutu-2", "agency": "CNSA", "dist_au": 1.000, "arena": "Lunar Farside Surface",
         "role": "Farside Von Kármán crater, 7.8 years surviving 96+ lunar days, LPR sub-surface radar, 0.1-40MHz LFS"},
        {"rank": 31, "name": "ARTEMIS P1", "agency": "NASA", "dist_au": 1.000, "arena": "Lunar Eccentric Retrograde",
         "role": "15+ years in lunar orbit, nightside lunar wake plasma void & ambipolar acceleration, FGM/EFI"},
        {"rank": 32, "name": "ARTEMIS P2", "agency": "NASA", "dist_au": 1.000, "arena": "Lunar Eccentric Prograde",
         "role": "15+ years in lunar orbit, dual-point magnetotail reconnection, crustal magnetic anomaly shielding"},
        {"rank": 33, "name": "SOHO", "agency": "ESA/NASA", "dist_au": 0.990, "arena": "Sun-Earth L1 Halo Orbit",
         "role": "31 years active, LASCO C2/C3 coronagraphs, 5,000+ sungrazing comets discovered, real-time CME tracker"},
        {"rank": 34, "name": "Wind", "agency": "NASA", "dist_au": 0.990, "arena": "Sun-Earth L1 Halo Orbit",
         "role": "32 years active, WAVES radio/plasma wave laboratory, Konus IPN gamma-ray burst triangulation"},
        {"rank": 35, "name": "ACE", "agency": "NASA", "dist_au": 0.990, "arena": "Sun-Earth L1 Lissajous Orbit",
         "role": "29 years active, CRIS/SIS cosmic ray isotopic clocks (Ni-59), RTSW 24/7 space weather broadcast"},
        {"rank": 36, "name": "DSCOVR", "agency": "NASA/NOAA/USAF", "dist_au": 0.990, "arena": "Sun-Earth L1 Lissajous Orbit",
         "role": "EPIC continuous full sunlit Earth disk 10-channel imager, PlasMag 30-60 min geomagnetic storm early warning"},
        {"rank": 37, "name": "Aditya-L1", "agency": "ISRO", "dist_au": 0.990, "arena": "Sun-Earth L1 Halo Orbit",
         "role": "VELC low-coronal Fe XIV/X emission line coronagraph, SUIT 200-400nm full-disk solar NUV imager"},
        {"rank": 38, "name": "STEREO-A", "agency": "NASA", "dist_au": 0.962, "arena": "Heliocentric Orbit",
         "role": "20 years in orbit, 3D heliospheric stereoscopy, SECCHI imaging, ahead of Earth in heliocentric path"},
        {"rank": 39, "name": "BepiColombo", "agency": "ESA/JAXA", "dist_au": 0.387, "arena": "Inner Solar System Cruise",
         "role": "Mercury gravity well capture, -1405 MJ/kg MOI blind insertion approach countdown in 34 days"},
        {"rank": 40, "name": "Solar Orbiter", "agency": "ESA/NASA", "dist_au": 0.280, "arena": "High-Inclination Solar",
         "role": "Out-of-ecliptic polar imaging, 520°C bone-black heat shield, Christmas Eve VGA5 in 66 days"},
        {"rank": 41, "name": "Parker Solar Probe", "agency": "NASA", "dist_au": 0.046, "arena": "Solar Corona In-Situ",
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
        "fleet_name": "The Grand Unoctoquadragintet (人类深空四十一极黄金舰队)",
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


def armada_41_comprehensive_summary() -> Dict[str, Any]:
    """生成 41 极深空黄金舰队与新晋 5 大旗舰综合分析"""
    spektr_rg = compute_spektr_rg_state()
    wind = compute_wind_state()
    ace = compute_ace_state()
    artemis = compute_artemis_pair_state()
    l1_pentad = the_sun_earth_l1_pentad()
    l2_trinity = the_sun_earth_l2_trinity()
    lunar_octet = the_lunar_octet()
    fleet = the_grand_unoctoquadragintet_fleet_census()
    
    return {
        "system_name": "The Grand Unoctoquadragintet & Deep Space Quintet Expansion",
        "epoch": "2026-10-19 01:30 CST",
        "spektr_rg": {
            "name": spektr_rg.name,
            "agency": spektr_rg.agency,
            "cumulative_years": spektr_rg.cumulative_years_in_space,
            "orbit": spektr_rg.orbit_type,
            "payloads": spektr_rg.core_payloads,
            "highlights": spektr_rg.scientific_highlights
        },
        "wind": {
            "name": wind.name,
            "agency": wind.agency,
            "cumulative_years": wind.cumulative_years_in_space,
            "orbit": wind.orbit_type,
            "payloads": wind.core_payloads,
            "highlights": wind.scientific_highlights
        },
        "ace": {
            "name": ace.name,
            "agency": ace.agency,
            "cumulative_years": ace.cumulative_years_in_space,
            "orbit": ace.orbit_type,
            "payloads": ace.core_payloads,
            "highlights": ace.scientific_highlights
        },
        "artemis_p1_p2": {
            "p1_name": artemis["P1"].name,
            "p2_name": artemis["P2"].name,
            "lunar_orbit_years": round(artemis["P1"].cumulative_days_in_target_orbit / 365.25, 2),
            "spacecraft_age_years": artemis["P1"].cumulative_years_in_space,
            "payloads": artemis["P1"].core_payloads,
            "highlights": artemis["P1"].scientific_highlights
        },
        "subsystems": {
            "l1_pentad": l1_pentad,
            "l2_trinity": l2_trinity,
            "lunar_octet": lunar_octet
        },
        "fleet_status": {
            "name": fleet["fleet_name"],
            "probe_count": fleet["probe_count"],
            "extremes": fleet["extremes"]
        }
    }


if __name__ == "__main__":
    import json
    summary = armada_41_comprehensive_summary()
    print("=== THE GRAND UNOCTOQUADRAGINTET & DEEP SPACE FLEET ===")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
