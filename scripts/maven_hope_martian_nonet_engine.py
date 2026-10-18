"""
MAVEN & Hope Probe (Emirates Mars Mission) Engine, The Martian Nonet (火星九极),
and The Grand Trigintet (2026 人类深空三十极黄金舰队) Orbital & Atmospheric Mechanics Engine.

Author: Hoshi (Autonomous Space & Celestial Dynamics Laboratory)
Date: 2026-10-18 CST
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Tuple


# Gravitational & Planetary Constants
G = 6.67430e-11                  # Gravitational constant (m^3 kg^-1 s^-2)
M_MARS = 6.4171e23               # Mars mass (kg)
MU_MARS = 42828.37               # Standard gravitational parameter GM of Mars (km^3 / s^2)
R_MARS = 3389.5                  # Mars mean volumetric radius (km)
A_PHOBOS = 9376.0                # Phobos semi-major axis (km)
A_DEIMOS = 23463.2               # Deimos semi-major axis (km)
SPEED_OF_LIGHT = 299792.458      # Speed of light (km/s)
AU_KM = 149597870.7              # Astronomical Unit in km
SOLAR_CONSTANT_1AU = 1361.0      # Solar irradiance at 1 AU (W/m^2)


@dataclass(frozen=True)
class OrbitParameters:
    periapsis_alt_km: float
    apoapsis_alt_km: float
    inclination_deg: float
    semi_major_axis_km: float
    eccentricity: float
    period_hours: float
    periapsis_velocity_kms: float
    apoapsis_velocity_kms: float
    orbits_per_sol: float


class MavenDynamics:
    """
    NASA MAVEN (Mars Atmosphere and Volatile EvolutioN)
    In orbit: 2014-09-22 02:24 UTC to present (12+ full years).
    """

    def __init__(self):
        # Initial science orbit (2014 - 2018)
        self.initial_orbit = self._compute_orbit(150.0, 6200.0, 75.0)
        # Aerobraked orbit (2019 - present)
        self.aerobraked_orbit = self._compute_orbit(150.0, 4500.0, 75.0)

    @staticmethod
    def _compute_orbit(hp: float, ha: float, inc: float) -> OrbitParameters:
        rp = R_MARS + hp
        ra = R_MARS + ha
        a = (rp + ra) / 2.0
        e = (ra - rp) / (ra + rp)
        period_s = 2.0 * math.pi * math.sqrt((a ** 3) / MU_MARS)
        period_h = period_s / 3600.0
        vp = math.sqrt(MU_MARS * (2.0 / rp - 1.0 / a))
        va = math.sqrt(MU_MARS * (2.0 / ra - 1.0 / a))
        sol_h = 24.6597
        orbits_per_sol = sol_h / period_h
        return OrbitParameters(
            periapsis_alt_km=hp,
            apoapsis_alt_km=ha,
            inclination_deg=inc,
            semi_major_axis_km=a,
            eccentricity=e,
            period_hours=period_h,
            periapsis_velocity_kms=vp,
            apoapsis_velocity_kms=va,
            orbits_per_sol=orbits_per_sol,
        )

    def mission_duration(self, current_date_str: str = "2026-10-18") -> Dict[str, float]:
        """
        MOI: 2014-09-22 02:24 UTC.
        """
        days_in_orbit = 4409.1  # to 2026-10-18
        earth_years = days_in_orbit / 365.25
        mars_years = days_in_orbit / 686.98
        total_orbits = days_in_orbit * (24.0 / self.aerobraked_orbit.period_hours)
        return {
            "days_in_orbit": days_in_orbit,
            "earth_years": earth_years,
            "mars_years": mars_years,
            "estimated_orbits": total_orbits,
        }

    @staticmethod
    def argon_rayleigh_fractionation() -> Dict[str, float]:
        """
        Argon isotope loss physics based on Jakosky et al., Science (2017).
        36Ar (35.9675 u) vs 38Ar (37.9627 u).
        Sputtering fractionation alpha = sqrt(m36 / m38).
        """
        m36 = 35.9675
        m38 = 37.9627
        alpha = math.sqrt(m36 / m38)
        # Ratio in primordial vs modern atmosphere
        r_primordial = 0.188  # 38Ar / 36Ar ~ 1 / 5.3
        r_modern = 0.238      # 38Ar / 36Ar ~ 1 / 4.2
        # Fraction of argon lost
        argon_loss_nominal = 0.66
        argon_loss_uncertainty = 0.05
        # Implied CO2 loss through geological history
        co2_loss_bar_min = 0.50
        co2_loss_bar_nominal = 1.00
        co2_loss_bar_max = 1.50
        return {
            "alpha": alpha,
            "r_primordial_38_36": r_primordial,
            "r_modern_38_36": r_modern,
            "argon_loss_nominal": argon_loss_nominal,
            "argon_loss_uncertainty": argon_loss_uncertainty,
            "co2_loss_bar_min": co2_loss_bar_min,
            "co2_loss_bar_nominal": co2_loss_bar_nominal,
            "co2_loss_bar_max": co2_loss_bar_max,
        }

    @staticmethod
    def oxygen_photochemical_escape_physics() -> Dict[str, float]:
        """
        Dissociative recombination O2+ + e- -> O* + O*
        Exobase altitude ~200 km.
        """
        h_exobase = 200.0
        r_exobase = R_MARS + h_exobase
        v_esc = math.sqrt(2.0 * MU_MARS / r_exobase)  # km/s
        # Kinetic energy needed for 16 amu O atom to escape
        m_O_kg = 16.0 * 1.660539e-27
        E_esc_J = 0.5 * m_O_kg * ((v_esc * 1000.0) ** 2)
        E_esc_eV = E_esc_J / 1.6021766e-19
        # Energy produced by dissociative recombination
        E_dr_per_atom_eV = 2.50
        can_escape = E_dr_per_atom_eV > E_esc_eV

        # Escape rates
        escape_rate_atoms_per_s = 1.1e26
        escape_rate_kg_per_s = escape_rate_atoms_per_s * m_O_kg
        quiet_total_loss_gs = 100.0  # g/s
        cme_surge_multiplier = 15.0  # 10x - 20x
        storm_total_loss_gs = quiet_total_loss_gs * cme_surge_multiplier

        return {
            "v_esc_kms": v_esc,
            "E_esc_eV": E_esc_eV,
            "E_dr_per_atom_eV": E_dr_per_atom_eV,
            "can_escape": float(can_escape),
            "escape_rate_atoms_per_s": escape_rate_atoms_per_s,
            "escape_rate_kg_per_s": escape_rate_kg_per_s,
            "quiet_total_loss_gs": quiet_total_loss_gs,
            "storm_total_loss_gs": storm_total_loss_gs,
        }


class HopeProbeDynamics:
    """
    UAE Emirates Mars Mission (EMM) Hope Probe (Al-Amal)
    In orbit: 2021-02-09 15:30 UTC to present (extended to 2028).
    """

    def __init__(self):
        # 20,000 km x 43,000 km, inclination 25.0 deg
        self.orbit = self._compute_orbit(20000.0, 43000.0, 25.0)

    @staticmethod
    def _compute_orbit(hp: float, ha: float, inc: float) -> OrbitParameters:
        rp = R_MARS + hp
        ra = R_MARS + ha
        a = (rp + ra) / 2.0
        e = (ra - rp) / (ra + rp)
        period_s = 2.0 * math.pi * math.sqrt((a ** 3) / MU_MARS)
        period_h = period_s / 3600.0
        vp = math.sqrt(MU_MARS * (2.0 / rp - 1.0 / a))
        va = math.sqrt(MU_MARS * (2.0 / ra - 1.0 / a))
        sol_h = 24.6597
        orbits_per_sol = sol_h / period_h
        return OrbitParameters(
            periapsis_alt_km=hp,
            apoapsis_alt_km=ha,
            inclination_deg=inc,
            semi_major_axis_km=a,
            eccentricity=e,
            period_hours=period_h,
            periapsis_velocity_kms=vp,
            apoapsis_velocity_kms=va,
            orbits_per_sol=orbits_per_sol,
        )

    def mission_duration(self, current_date_str: str = "2026-10-18") -> Dict[str, float]:
        """
        MOI: 2021-02-09 15:30 UTC.
        """
        days_in_orbit = 2077.5
        earth_years = days_in_orbit / 365.25
        mars_years = days_in_orbit / 686.98
        total_orbits = days_in_orbit * (24.0 / self.orbit.period_hours)
        return {
            "days_in_orbit": days_in_orbit,
            "earth_years": earth_years,
            "mars_years": mars_years,
            "estimated_orbits": total_orbits,
        }

    def deimos_geometric_resonance(self) -> Dict[str, float]:
        """
        Examine Hope's periapsis radius relative to Deimos orbit.
        Deimos a = 23,463.2 km.
        Hope rp = 23,389.5 km.
        """
        rp = R_MARS + self.orbit.periapsis_alt_km
        delta_r = abs(A_DEIMOS - rp)
        closest_flyby_observed_km = 100.0
        return {
            "deimos_orbit_km": A_DEIMOS,
            "hope_periapsis_km": rp,
            "delta_orbit_radius_km": delta_r,
            "closest_flyby_observed_km": closest_flyby_observed_km,
        }


class MartianNonetSystem:
    """
    The Martian Nonet (火星现役九大极器 / 火星九极全景):
    7 Orbiters + 2 Rovers.
    """

    ROSTER = [
        {
            "name": "2001 Mars Odyssey",
            "agency": "NASA",
            "type": "Orbiter",
            "arrival_year": 2001,
            "orbit_desc": "400 km sun-synchronous polar",
            "key_payload": "GRS, THEMIS, MARIE, CE-505 UHF",
            "primary_breakthrough": "First confirmation of shallow subsurface water ice, 100m thermal inertia map, 25yr jubilee",
        },
        {
            "name": "Mars Express (MEX)",
            "agency": "ESA",
            "type": "Orbiter",
            "arrival_year": 2003,
            "orbit_desc": "340 x 10,100 km eccentric polar (crosses Phobos)",
            "key_payload": "MARSIS, HRSC, OMEGA, SPICAM, ASPERA-3",
            "primary_breakthrough": "Subsurface 5km radar sounding, Phobos 45km flyby (30.6% porosity), three aqueous eras",
        },
        {
            "name": "Mars Reconnaissance Orbiter (MRO)",
            "agency": "NASA",
            "type": "Orbiter",
            "arrival_year": 2006,
            "orbit_desc": "255 x 320 km sun-synchronous polar",
            "key_payload": "HiRISE, SHARAD, CRISM, MCS, MARCI, Electra",
            "primary_breakthrough": "30 cm/px optical micro-imaging, 1km radar ice sheets, 80% primary surface rover relay",
        },
        {
            "name": "Curiosity (MSL)",
            "agency": "NASA",
            "type": "Rover",
            "arrival_year": 2012,
            "orbit_desc": "Surface: Gale Crater / Mount Sharp (33.6+ km)",
            "key_payload": "SAM, ChemCam, CheMin, Mastcam, APXS, DAN, REMS, RAD, MMRTG",
            "primary_breakthrough": "Ancient habitable lake system, 33.6km traverse, Gediz Vallis pure elemental sulfur crystals",
        },
        {
            "name": "MAVEN",
            "agency": "NASA",
            "type": "Orbiter",
            "arrival_year": 2014,
            "orbit_desc": "150 x 4,500 km 75° inclined elliptical",
            "key_payload": "NGIMS, IUVS, SWEA, SWIA, STATIC, MAG, LPW, SEP, Electra",
            "primary_breakthrough": "66% argon isotope loss, solar wind atmospheric stripping, auroral zoo (proton/diffuse), aerobraking relay",
        },
        {
            "name": "ExoMars Trace Gas Orbiter (TGO)",
            "agency": "ESA/Roscosmos",
            "type": "Orbiter",
            "arrival_year": 2016,
            "orbit_desc": "400 km circular 74° polar",
            "key_payload": "NOMAD, ACS, FREND, CaSSIS, Electra",
            "primary_breakthrough": "50 pptv methane detection limit, first HCl detection, Candor Chaos 40% water ice oasis, 10yr jubilee",
        },
        {
            "name": "Hope Probe (Al-Amal / EMM)",
            "agency": "UAE/MBRSC",
            "type": "Orbiter",
            "arrival_year": 2021,
            "orbit_desc": "20,000 x 43,000 km 25° supersynchronous (55h)",
            "key_payload": "EXI, EMIRS, EMUS",
            "primary_breakthrough": "Synoptic global weather across full diurnal cycle, sinuous discrete aurora, Deimos 100km flyby",
        },
        {
            "name": "Perseverance (Mars 2020)",
            "agency": "NASA",
            "type": "Rover",
            "arrival_year": 2021,
            "orbit_desc": "Surface: Jezero Crater delta & rim (Wildcat Ridge / Wild West)",
            "key_payload": "PIXL, SHERLOC, SuperCam, Mastcam-Z, MOXIE, RIMFAX, MEDA, AutoNav AI, MMRTG",
            "primary_breakthrough": "Jezero delta & ancient bedrock, 500m rim climb to Wild West, 33 pristine core samples sealed",
        },
        {
            "name": "Tianwen-1 Orbiter",
            "agency": "CNSA",
            "type": "Orbiter",
            "arrival_year": 2021,
            "orbit_desc": "265 x 10,700 km polar remote sensing",
            "key_payload": "MoRIC, HiRIC, MOSIR subsurface radar, MIM, MMS, MEPA",
            "primary_breakthrough": "76m global true-color orthomosaic, 100m radar stratigraphy, Comet 3I/ATLAS observations, 3.5TB open data",
        },
    ]

    @classmethod
    def get_roster(cls) -> List[Dict]:
        return cls.ROSTER

    @classmethod
    def get_relay_topology(cls) -> Dict[str, Dict[str, float]]:
        """
        Martian surface-orbital deep space UHF communication relay network shares.
        """
        return {
            "Perseverance_downlink_shares": {
                "ExoMars_TGO": 0.50,
                "MRO": 0.38,
                "MAVEN": 0.12,
            },
            "Curiosity_downlink_shares": {
                "MRO": 0.45,
                "ExoMars_TGO": 0.40,
                "MAVEN": 0.10,
                "Mars_Odyssey": 0.05,
            },
        }


class GrandTrigintetFleet:
    """
    2026 人类深空三十极黄金舰队 (The Grand Trigintet):
    30 Active Deep Space Probes sorted strictly by heliocentric distance (descending).
    """

    PROBES = [
        {"rank": 1, "name": "Voyager 1", "agency": "NASA", "dist_au": 173.22, "zone": "Interstellar"},
        {"rank": 2, "name": "Voyager 2", "agency": "NASA", "dist_au": 144.29, "zone": "Interstellar (Crossed 20 Light-Hours Today)"},
        {"rank": 3, "name": "New Horizons", "agency": "NASA", "dist_au": 65.92, "zone": "Kuiper Belt"},
        {"rank": 4, "name": "Juno", "agency": "NASA", "dist_au": 5.20, "zone": "Jupiter Orbit"},
        {"rank": 5, "name": "JUICE", "agency": "ESA", "dist_au": 5.20, "zone": "Jupiter System"},
        {"rank": 6, "name": "Europa Clipper", "agency": "NASA", "dist_au": 5.20, "zone": "Jupiter En Route"},
        {"rank": 7, "name": "Lucy", "agency": "NASA", "dist_au": 5.04, "zone": "Jupiter Trojans"},
        {"rank": 8, "name": "Psyche", "agency": "NASA", "dist_au": 2.042, "zone": "Main Asteroid Belt"},
        {"rank": 9, "name": "2001 Mars Odyssey", "agency": "NASA", "dist_au": 1.579, "zone": "Mars Orbit"},
        {"rank": 10, "name": "Mars Express", "agency": "ESA", "dist_au": 1.579, "zone": "Mars Orbit"},
        {"rank": 11, "name": "ExoMars TGO", "agency": "ESA/Roscosmos", "dist_au": 1.579, "zone": "Mars Orbit"},
        {"rank": 12, "name": "MAVEN", "agency": "NASA", "dist_au": 1.579, "zone": "Mars Orbit"},
        {"rank": 13, "name": "Hope Probe (Al-Amal)", "agency": "UAE/MBRSC", "dist_au": 1.579, "zone": "Mars Orbit"},
        {"rank": 14, "name": "Curiosity", "agency": "NASA", "dist_au": 1.524, "zone": "Mars Surface"},
        {"rank": 15, "name": "Perseverance", "agency": "NASA", "dist_au": 1.524, "zone": "Mars Surface"},
        {"rank": 16, "name": "Tianwen-1 Orbiter", "agency": "CNSA", "dist_au": 1.524, "zone": "Mars Orbit"},
        {"rank": 17, "name": "MRO", "agency": "NASA", "dist_au": 1.524, "zone": "Mars Orbit"},
        {"rank": 18, "name": "Hera", "agency": "ESA", "dist_au": 1.304, "zone": "Didymos Binary Asteroid"},
        {"rank": 19, "name": "Hayabusa2# (SHARP)", "agency": "JAXA", "dist_au": 1.120, "zone": "1998 KY26 En Route"},
        {"rank": 20, "name": "OSIRIS-APEX", "agency": "NASA", "dist_au": 1.010, "zone": "Apophis En Route"},
        {"rank": 21, "name": "JWST", "agency": "NASA/ESA/CSA", "dist_au": 1.010, "zone": "Sun-Earth L2"},
        {"rank": 22, "name": "Euclid", "agency": "ESA", "dist_au": 1.010, "zone": "Sun-Earth L2"},
        {"rank": 23, "name": "Tianwen-2", "agency": "CNSA", "dist_au": 1.001, "zone": "Kamoʻoalewa En Route"},
        {"rank": 24, "name": "Queqiao-2", "agency": "CNSA", "dist_au": 1.000, "zone": "Earth-Moon Frozen Orbit (384,400 km)"},
        {"rank": 25, "name": "Chang'e-4 / Yutu-2", "agency": "CNSA", "dist_au": 1.000, "zone": "Lunar Far Side Surface (384,400 km)"},
        {"rank": 26, "name": "SOHO", "agency": "ESA/NASA", "dist_au": 0.990, "zone": "Sun-Earth L1 (1.49M km)"},
        {"rank": 27, "name": "STEREO-A", "agency": "NASA", "dist_au": 0.962, "zone": "Heliocentric Drift"},
        {"rank": 28, "name": "BepiColombo", "agency": "ESA/JAXA", "dist_au": 0.387, "zone": "Mercury En Route"},
        {"rank": 29, "name": "Solar Orbiter", "agency": "ESA/NASA", "dist_au": 0.280, "zone": "Inner Heliocentric (0.28-0.88 AU)"},
        {"rank": 30, "name": "Parker Solar Probe", "agency": "NASA", "dist_au": 0.046, "zone": "Solar Corona Perihelion"},
    ]

    @classmethod
    def get_fleet(cls) -> List[Dict]:
        return cls.PROBES

    @classmethod
    def compute_extreme_contrasts(cls) -> Dict[str, float]:
        v1_dist = 173.22
        psp_dist = 0.046
        dist_ratio = v1_dist / psp_dist
        flux_ratio = dist_ratio ** 2

        # Communication light time
        v1_km = v1_dist * AU_KM
        v1_light_time_s = v1_km / SPEED_OF_LIGHT
        v1_light_time_h = v1_light_time_s / 3600.0

        moon_km = 384400.0
        moon_light_time_s = moon_km / SPEED_OF_LIGHT

        light_time_ratio = v1_light_time_s / moon_light_time_s

        # Speed contrast
        v_psp_kms = 192.0
        v_ky26_esc_kms = 0.00000688  # 6.88 mm/s
        speed_ratio = v_psp_kms / v_ky26_esc_kms

        # Temperature contrast
        t_hot_k = 1400.0 + 273.15
        t_cold_k = 2.7
        temp_span_k = t_hot_k - t_cold_k

        return {
            "heliocentric_distance_ratio": dist_ratio,
            "solar_flux_ratio": flux_ratio,
            "v1_light_time_hours": v1_light_time_h,
            "moon_light_time_seconds": moon_light_time_s,
            "light_time_ratio": light_time_ratio,
            "speed_ratio": speed_ratio,
            "temperature_span_k": temp_span_k,
        }
