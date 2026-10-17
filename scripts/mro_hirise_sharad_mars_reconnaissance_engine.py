#!/usr/bin/env python3
"""
Mars Reconnaissance Orbiter (MRO) Orbital Mechanics, HiRISE Ultra-High-Resolution Optics,
SHARAD Subsurface Ice Radar Sounding, Electra UHF Rover Relay, and
2026 Human Deep Space 23rd Pillar (The Grand Trevigintet) Astrophysics Engine.

Author: Hoshi
Date: 2026-10-17
"""

import math
from datetime import datetime, timezone
from typing import Dict, Any, Tuple

# Physical & Astrodynamical Constants (CODATA / IAU / JPL NAIF)
SPEED_OF_LIGHT = 299792458.0  # m/s
AU_KM = 149597870.700  # km per AU

# Mars Planetary Constants
MARS_GM = 42828.37  # km^3/s^2 (G * M_mars)
MARS_EQUATORIAL_RADIUS_KM = 3396.2  # km
MARS_MEAN_RADIUS_KM = 3389.5  # km
MARS_POLAR_RADIUS_KM = 3376.2  # km
MARS_J2 = 1.96045e-3  # Second gravitational zonal harmonic
MARS_SOL_SECONDS = 88775.244  # seconds (24h 39m 35.244s)
MARS_SIDEREAL_YEAR_DAYS = 686.980  # Earth days

# MRO Mission Milestones
MRO_LAUNCH_UTC = datetime(2005, 8, 12, 11, 43, 0, tzinfo=timezone.utc)
MRO_MOI_UTC = datetime(2006, 3, 10, 21, 24, 0, tzinfo=timezone.utc)
MRO_PRIMARY_SCIENCE_UTC = datetime(2006, 11, 6, 0, 0, 0, tzinfo=timezone.utc)
CURRENT_EPOCH_UTC = datetime(2026, 10, 17, 12, 0, 0, tzinfo=timezone.utc)

# MRO Primary Science Orbit (PSO) - Frozen Sun-Synchronous Polar Orbit
PSO_PERIAPSIS_ALT_KM = 255.0  # km (over South Pole region ~270° argument of periapsis)
PSO_APOAPSIS_ALT_KM = 320.0  # km (over North Pole region)
PSO_INCLINATION_DEG = 92.8  # degrees (retrograde polar orbit)
PSO_LOCAL_SOLAR_TIME_HOURS = 15.0  # 3:00 PM LMST ascending node crossing

# HiRISE Camera Specifications
HIRISE_APERTURE_M = 0.50  # 50 cm primary mirror diameter
HIRISE_FOCAL_LENGTH_M = 12.0  # 12.0 m effective focal length
HIRISE_FOCAL_RATIO = 24.0  # f/24
HIRISE_PIXEL_PITCH_UM = 12.0  # 12.0 micrometers
HIRISE_RED_SWATH_PIXELS = 20480  # 10 CCDs stitched x 2048 pixels
HIRISE_RED_CENTER_WAVELENGTH_NM = 700.0  # nm (Red band: 570 - 830 nm)

# SHARAD Subsurface Radar Specifications (ASI/NASA)
SHARAD_CENTER_FREQ_MHZ = 20.0  # MHz
SHARAD_BANDWIDTH_MHZ = 10.0  # MHz (chirp 15 - 25 MHz)
WATER_ICE_RELATIVE_PERMITTIVITY = 3.15  # dielectric constant epsilon_r of pure cold ice
BASALTIC_REGOLITH_PERMITTIVITY = 5.5  # dielectric constant of dry basalt regolith

# Electra UHF & Deep Space Telecom
ELECTRA_MAX_DATA_RATE_KBPS = 2048.0  # kbps (2.048 Mbps proximity-1 UHF link)
X_BAND_HGA_DIAMETER_M = 3.0  # 3.0 m high gain Cassegrain dish
X_BAND_FREQ_GHZ = 8.439  # GHz
X_BAND_TWTA_POWER_W = 100.0  # 100 Watts (+50 dBm)
X_BAND_EFFICIENCY = 0.60  # 60% aperture efficiency
TOTAL_DATA_RETURNED_TBITS = 455.0  # >450 Terabits (>56 Terabytes) returned over 20 years


class MROMarsReconnaissanceEngine:
    """Astrodynamics, HiRISE Optics, SHARAD Radar, and Telecom Engine for MRO."""

    def __init__(self, target_time: datetime = CURRENT_EPOCH_UTC):
        self.target_time = target_time

    def calculate_mission_duration_metrics(self) -> Dict[str, Any]:
        """Compute operational duration, total orbits, and longevity multiplication factor."""
        delta_since_moi = self.target_time - MRO_MOI_UTC
        days_in_orbit = delta_since_moi.total_seconds() / 86400.0
        earth_years = days_in_orbit / 365.25
        mars_years = days_in_orbit / MARS_SIDEREAL_YEAR_DAYS

        # Original primary mission was 2 Earth years (Nov 2006 to Nov 2008)
        nominal_primary_mission_years = 2.0
        extended_factor = earth_years / nominal_primary_mission_years

        # Nominal orbital period ~112.98 min (1.883 hours)
        orbital_period_hours = 6778.6 / 3600.0
        total_orbits = (days_in_orbit * 24.0) / orbital_period_hours

        return {
            "days_in_mars_orbit": round(days_in_orbit, 2),
            "earth_years_in_orbit": round(earth_years, 3),
            "mars_years_in_orbit": round(mars_years, 3),
            "total_orbits_completed": int(round(total_orbits)),
            "extended_mission_factor": round(extended_factor, 2),
            "anniversary_milestone": "20th Anniversary in Mars Orbit (2006 - 2026)"
        }

    def compute_orbital_mechanics(self) -> Dict[str, Any]:
        """
        Compute frozen sun-synchronous orbital parameters, velocities, period,
        and J2 nodal precession balance.
        """
        r_p = MARS_MEAN_RADIUS_KM + PSO_PERIAPSIS_ALT_KM
        r_a = MARS_MEAN_RADIUS_KM + PSO_APOAPSIS_ALT_KM
        a = (r_p + r_a) / 2.0
        e = (r_a - r_p) / (r_a + r_p)
        p = a * (1.0 - e**2)

        # Orbital period (Kepler's Third Law in two-body Mars frame)
        period_seconds = 2.0 * math.pi * math.sqrt((a * 1e3)**3 / (MARS_GM * 1e9))
        period_minutes = period_seconds / 60.0
        period_hours = period_seconds / 3600.0

        # Orbits per Earth day and per Mars sol
        orbits_per_earth_day = 86400.0 / period_seconds
        orbits_per_mars_sol = MARS_SOL_SECONDS / period_seconds

        # Orbital velocities at periapsis, apoapsis, and mean circular velocity
        v_p = math.sqrt(MARS_GM * (2.0 / r_p - 1.0 / a))  # km/s
        v_a = math.sqrt(MARS_GM * (2.0 / r_a - 1.0 / a))  # km/s
        v_mean = math.sqrt(MARS_GM / a)  # km/s

        # Ground speed at equator (accounting for planet rotation)
        # v_ground = v_orbit * (R_mars / r)
        v_ground_suborbital = v_mean * (MARS_MEAN_RADIUS_KM / a) * 1e3  # m/s

        # Sun-synchronous nodal precession verification:
        # Mars orbital motion around Sun: 360 deg / 686.980 days = 0.52403 deg/day
        target_precession_deg_per_day = 360.0 / MARS_SIDEREAL_YEAR_DAYS
        target_precession_rad_s = math.radians(target_precession_deg_per_day) / 86400.0

        # First-order J2 nodal precession:
        # dOmega/dt = -1.5 * J2 * (R_eq / p)^2 * n * cos(i)
        n_mean_motion = 2.0 * math.pi / period_seconds  # rad/s
        req_over_p_sq = (MARS_EQUATORIAL_RADIUS_KM / p)**2
        j2_precession_factor = -1.5 * MARS_J2 * req_over_p_sq * n_mean_motion

        # Calculate exact inclination required for sun-synchronous balance:
        cos_i_req = target_precession_rad_s / j2_precession_factor
        i_req_deg = math.degrees(math.acos(cos_i_req))

        return {
            "periapsis_radius_km": round(r_p, 2),
            "apoapsis_radius_km": round(r_a, 2),
            "semi_major_axis_km": round(a, 2),
            "eccentricity": round(e, 6),
            "orbital_period_seconds": round(period_seconds, 2),
            "orbital_period_minutes": round(period_minutes, 3),
            "orbits_per_earth_day": round(orbits_per_earth_day, 3),
            "orbits_per_mars_sol": round(orbits_per_mars_sol, 3),
            "periapsis_velocity_km_s": round(v_p, 4),
            "apoapsis_velocity_km_s": round(v_a, 4),
            "mean_orbital_velocity_km_s": round(v_mean, 4),
            "ground_suborbital_speed_m_s": round(v_ground_suborbital, 2),
            "sun_sync_precession_deg_per_day": round(target_precession_deg_per_day, 5),
            "inclination_actual_deg": PSO_INCLINATION_DEG,
            "inclination_analytical_deg": round(i_req_deg, 2),
            "local_solar_time_ascending_node": f"{int(PSO_LOCAL_SOLAR_TIME_HOURS):02d}:00 LMST (3:00 PM)"
        }

    def compute_hirise_optics_physics(self) -> Dict[str, Any]:
        """
        Compute optical diffraction, Instantaneous Field of View (IFOV),
        Ground Sampling Distance (GSD), swath width, and TDI line integration rate.
        """
        # Instantaneous Field of View (IFOV) per pixel:
        # theta_pix = pixel_pitch / focal_length
        ifov_rad = (HIRISE_PIXEL_PITCH_UM * 1e-6) / HIRISE_FOCAL_LENGTH_M
        ifov_urad = ifov_rad * 1e6
        ifov_arcsec = math.degrees(ifov_rad) * 3600.0

        # Ground Sampling Distance (GSD) at periapsis (255 km), mean (287.5 km), and apoapsis (320 km)
        gsd_periapsis_m = (PSO_PERIAPSIS_ALT_KM * 1e3) * ifov_rad
        gsd_mean_m = (((PSO_PERIAPSIS_ALT_KM + PSO_APOAPSIS_ALT_KM) / 2.0) * 1e3) * ifov_rad
        gsd_apoapsis_m = (PSO_APOAPSIS_ALT_KM * 1e3) * ifov_rad

        # Swath width on Martian ground (Red band: 20,480 stitched pixels)
        swath_width_periapsis_km = (HIRISE_RED_SWATH_PIXELS * gsd_periapsis_m) / 1e3
        swath_width_mean_km = (HIRISE_RED_SWATH_PIXELS * gsd_mean_m) / 1e3
        swath_width_apoapsis_km = (HIRISE_RED_SWATH_PIXELS * gsd_apoapsis_m) / 1e3

        # Optical diffraction limit (Airy disk radius) at center wavelength (700 nm)
        wavelength_m = HIRISE_RED_CENTER_WAVELENGTH_NM * 1e-9
        airy_radius_rad = 1.22 * (wavelength_m / HIRISE_APERTURE_M)
        airy_radius_arcsec = math.degrees(airy_radius_rad) * 3600.0
        airy_disk_diameter_focal_plane_um = (2.44 * wavelength_m * HIRISE_FOCAL_RATIO) * 1e6

        # Line scan rate and TDI integration time
        # v_ground ~ 3146 m/s
        v_ground_nominal = 3146.0  # m/s
        line_rate_hz = v_ground_nominal / gsd_mean_m
        line_time_us = (1.0 / line_rate_hz) * 1e6

        return {
            "aperture_diameter_m": HIRISE_APERTURE_M,
            "focal_length_m": HIRISE_FOCAL_LENGTH_M,
            "focal_ratio": f"f/{HIRISE_FOCAL_RATIO:.1f}",
            "pixel_pitch_um": HIRISE_PIXEL_PITCH_UM,
            "ifov_microradians": round(ifov_urad, 2),
            "ifov_arcseconds": round(ifov_arcsec, 4),
            "gsd_periapsis_cm": round(gsd_periapsis_m * 100.0, 2),
            "gsd_mean_cm": round(gsd_mean_m * 100.0, 2),
            "gsd_apoapsis_cm": round(gsd_apoapsis_m * 100.0, 2),
            "swath_width_mean_km": round(swath_width_mean_km, 2),
            "airy_radius_arcsec": round(airy_radius_arcsec, 4),
            "airy_disk_diameter_focal_plane_um": round(airy_disk_diameter_focal_plane_um, 2),
            "line_rate_hz": round(line_rate_hz, 1),
            "line_integration_time_us": round(line_time_us, 2),
            "resolution_benchmark": "30 cm/pixel (resolves Curiosity/Perseverance rover tracks and boulders)"
        }

    def compute_sharad_subsurface_radar(self) -> Dict[str, Any]:
        """
        Compute radar chirped pulse parameters, vertical range resolution in free space,
        ice sheet penetration, dielectric properties, and two-way travel time.
        """
        # Free-space wavelength and vertical range resolution
        f_c_hz = SHARAD_CENTER_FREQ_MHZ * 1e6
        bandwidth_hz = SHARAD_BANDWIDTH_MHZ * 1e6
        lambda_0_m = SPEED_OF_LIGHT / f_c_hz

        # Free space range resolution: delta_r_0 = c / (2 * B)
        delta_r_free_space_m = SPEED_OF_LIGHT / (2.0 * bandwidth_hz)

        # In cold water ice (epsilon_r ~ 3.15, refractive index n = sqrt(epsilon_r))
        n_ice = math.sqrt(WATER_ICE_RELATIVE_PERMITTIVITY)
        v_ice_m_s = SPEED_OF_LIGHT / n_ice
        delta_r_ice_m = delta_r_free_space_m / n_ice

        # In dry basaltic regolith (epsilon_r ~ 5.5)
        n_regolith = math.sqrt(BASALTIC_REGOLITH_PERMITTIVITY)
        v_regolith_m_s = SPEED_OF_LIGHT / n_regolith
        delta_r_regolith_m = delta_r_free_space_m / n_regolith

        # Two-way travel time (TWTT) for typical 500 m thick ice sheet
        depth_nominal_ice_m = 500.0
        twtt_500m_ice_us = (2.0 * depth_nominal_ice_m / v_ice_m_s) * 1e6

        # Maximum penetration depth in clean water ice (~1000 m / 1 km)
        max_penetration_m = 1000.0

        # Utopia Planitia subsurface ice sheet volume discovery estimate (~14,300 km^3)
        utopia_ice_volume_km3 = 14300.0
        lake_superior_volume_km3 = 12100.0
        lake_superior_ratio = utopia_ice_volume_km3 / lake_superior_volume_km3

        return {
            "center_frequency_mhz": SHARAD_CENTER_FREQ_MHZ,
            "bandwidth_mhz": SHARAD_BANDWIDTH_MHZ,
            "free_space_wavelength_m": round(lambda_0_m, 2),
            "free_space_resolution_m": round(delta_r_free_space_m, 2),
            "ice_refractive_index": round(n_ice, 4),
            "propagation_speed_in_ice_km_s": round(v_ice_m_s / 1e3, 1),
            "vertical_resolution_in_ice_m": round(delta_r_ice_m, 2),
            "vertical_resolution_in_regolith_m": round(delta_r_regolith_m, 2),
            "twtt_500m_ice_microseconds": round(twtt_500m_ice_us, 3),
            "max_penetration_ice_m": max_penetration_m,
            "utopia_planitia_ice_volume_km3": utopia_ice_volume_km3,
            "ratio_to_lake_superior": round(lake_superior_ratio, 2),
            "geophysical_impact": "Direct detection of massive subsurface water ice deposits on Mars"
        }

    def compute_telecommunications_architecture(self) -> Dict[str, Any]:
        """
        Compute high-gain X-band dish gain, EIRP, Electra UHF rover relay throughput,
        and cumulative 20-year data legacy.
        """
        # X-band High Gain Antenna (HGA) gain:
        # G = eta * (pi * D / lambda)^2
        lambda_x_m = SPEED_OF_LIGHT / (X_BAND_FREQ_GHZ * 1e9)
        gain_linear = X_BAND_EFFICIENCY * ((math.pi * X_BAND_HGA_DIAMETER_M) / lambda_x_m)**2
        gain_dbi = 10.0 * math.log10(gain_linear)

        # Transmitter Power and EIRP:
        p_tx_dbw = 10.0 * math.log10(X_BAND_TWTA_POWER_W)  # 20.0 dBW
        eirp_dbw = p_tx_dbw + gain_dbi  # Equivalent Isotropically Radiated Power

        # Mars to Earth distance on 2026-10-17:
        # Mean distance ~1.95 AU (~291.7 million km)
        dist_earth_mars_au = 1.950
        dist_earth_mars_km = dist_earth_mars_au * AU_KM
        owlt_seconds = (dist_earth_mars_km * 1e3) / SPEED_OF_LIGHT
        owlt_minutes = owlt_seconds / 60.0

        # Electra UHF relay pass capacity:
        # 10 minute pass at 2048 kbps
        pass_duration_s = 600.0  # 10 minutes
        pass_volume_mbits = (ELECTRA_MAX_DATA_RATE_KBPS * pass_duration_s) / 1e3  # Mbits
        pass_volume_mbytes = pass_volume_mbits / 8.0

        # Cumulative data returned in Terabytes (455 Tbits)
        total_tbytes = TOTAL_DATA_RETURNED_TBITS / 8.0

        return {
            "x_band_hga_diameter_m": X_BAND_HGA_DIAMETER_M,
            "x_band_frequency_ghz": X_BAND_FREQ_GHZ,
            "x_band_gain_dbi": round(gain_dbi, 2),
            "transmitter_power_w": X_BAND_TWTA_POWER_W,
            "eirp_dbw": round(eirp_dbw, 2),
            "earth_mars_distance_au": dist_earth_mars_au,
            "earth_mars_distance_km": round(dist_earth_mars_km, 1),
            "owlt_minutes": round(owlt_minutes, 2),
            "rtlt_minutes": round(owlt_minutes * 2.0, 2),
            "electra_max_rate_kbps": ELECTRA_MAX_DATA_RATE_KBPS,
            "electra_single_pass_capacity_mb": round(pass_volume_mbytes, 2),
            "rover_data_relay_percentage": "> 80% of all Mars surface science relayed via MRO",
            "cumulative_data_returned_tbits": TOTAL_DATA_RETURNED_TBITS,
            "cumulative_data_returned_terabytes": round(total_tbytes, 2)
        }

    def evaluate_grand_trevigintet_fleet(self) -> Dict[str, Any]:
        """
        Evaluate the 23-pillar Grand Trevigintet deep space fleet matrix,
        anchored by MRO as the high-resolution orbital reconnaissance & telecom pillar.
        """
        pillars = [
            {"rank": 1, "name": "Voyager 1", "dist_au": 173.22, "type": "Interstellar Boundary", "agency": "NASA"},
            {"rank": 2, "name": "Voyager 2", "dist_au": 144.26, "type": "Interstellar Celestial South (20 LH Crossing Today)", "agency": "NASA"},
            {"rank": 3, "name": "New Horizons", "dist_au": 65.92, "type": "Kuiper Belt Hyperbolic", "agency": "NASA"},
            {"rank": 4, "name": "Juno", "dist_au": 5.20, "type": "Jupiter Polar Radiation Vault", "agency": "NASA"},
            {"rank": 5, "name": "JUICE", "dist_au": 5.20, "type": "Jupiter Icy Moons Ganymede", "agency": "ESA"},
            {"rank": 6, "name": "Europa Clipper", "dist_au": 5.20, "type": "Outer Solar Habitability", "agency": "NASA"},
            {"rank": 7, "name": "Lucy", "dist_au": 5.04, "type": "Jupiter Trojan Micro-planets", "agency": "NASA"},
            {"rank": 8, "name": "Psyche", "dist_au": 2.042, "type": "Metal World Core Hall Propulsion", "agency": "NASA"},
            {"rank": 9, "name": "Curiosity", "dist_au": 1.524, "type": "Mars Gale Crater Floor Rover", "agency": "NASA"},
            {"rank": 10, "name": "Perseverance", "dist_au": 1.524, "type": "Mars Jezero Crater Rim Rover", "agency": "NASA"},
            {"rank": 11, "name": "Tianwen-1", "dist_au": 1.524, "type": "Mars Global Polar Remote Sensing", "agency": "CNSA"},
            {"rank": 12, "name": "Mars Reconnaissance Orbiter (MRO)", "dist_au": 1.524, "type": "Mars 20-Year High-Res Reconnaissance & Telecom Backbone", "agency": "NASA"},
            {"rank": 13, "name": "Hera", "dist_au": 1.304, "type": "Binary Asteroid Planetary Defense", "agency": "ESA"},
            {"rank": 14, "name": "Hayabusa2#", "dist_au": 1.120, "type": "Fast-Spin Micro-Asteroid 1998 KY26", "agency": "JAXA"},
            {"rank": 15, "name": "OSIRIS-APEX", "dist_au": "1.010/0.500", "type": "Apophis Encounter Fig Leaf Thermal", "agency": "NASA"},
            {"rank": 16, "name": "JWST", "dist_au": 1.010, "type": "SEL2 Deep Space Cryogenic Infrared", "agency": "NASA/ESA/CSA"},
            {"rank": 17, "name": "Euclid", "dist_au": 1.010, "type": "SEL2 Dark Universe Cosmic Shear & BAO", "agency": "ESA"},
            {"rank": 18, "name": "Tianwen-2", "dist_au": 1.001, "type": "Quasi-Satellite Fast Anchor Sampling", "agency": "CNSA"},
            {"rank": 19, "name": "Queqiao-2", "dist_au": 1.000, "type": "Earth-Moon L2 Frozen Relay", "agency": "CNSA"},
            {"rank": 20, "name": "Chang'e-4 / Yutu-2", "dist_au": 1.000, "type": "Lunar Far Side SPA Exploration", "agency": "CNSA"},
            {"rank": 21, "name": "BepiColombo", "dist_au": 0.387, "type": "Mercury Gravitational Trap MOI", "agency": "ESA/JAXA"},
            {"rank": 22, "name": "Solar Orbiter", "dist_au": "0.280-0.880", "type": "High-Inclination Solar Dynamo", "agency": "ESA/NASA"},
            {"rank": 23, "name": "Parker Solar Probe", "dist_au": 0.046, "type": "Extreme Perihelion Stellar Corona", "agency": "NASA"}
        ]

        # Mars fleet Quaternity at 1.524 AU
        mars_fleet = [p for p in pillars if p["dist_au"] == 1.524]

        # Physical span extremes:
        max_dist_au = 173.22  # Voyager 1
        min_dist_au = 0.046  # Parker Solar Probe
        heliocentric_ratio = max_dist_au / min_dist_au
        solar_flux_drop = (max_dist_au / min_dist_au)**2

        return {
            "fleet_size": len(pillars),
            "designation": "The Grand Trevigintet (二十三极黄金舰队)",
            "mars_quaternity_count": len(mars_fleet),
            "heliocentric_distance_ratio": round(heliocentric_ratio, 2),
            "solar_radiation_flux_ratio_millions": round(solar_flux_drop / 1e6, 2),
            "mro_role": "20-Year Orbital High-Res Imaging & Telecommunications Backbone",
            "voyager2_countdown_hours": 12.5  # crossing 20 LH today
        }


def main():
    engine = MROMarsReconnaissanceEngine()
    print("=== MRO Mars Reconnaissance Engine (2006-2026) ===")
    mission = engine.calculate_mission_duration_metrics()
    print(f"Days in Orbit: {mission['days_in_mars_orbit']} days ({mission['earth_years_in_orbit']} years, {mission['total_orbits_completed']} orbits)")
    
    orbit = engine.compute_orbital_mechanics()
    print(f"Orbit: {orbit['periapsis_radius_km']} x {orbit['apoapsis_radius_km']} km (Period: {orbit['orbital_period_minutes']} min)")
    print(f"Sun-sync Inc: actual={orbit['inclination_actual_deg']}°, analytical={orbit['inclination_analytical_deg']}°")
    
    hirise = engine.compute_hirise_optics_physics()
    print(f"HiRISE: IFOV={hirise['ifov_microradians']} µrad, GSD={hirise['gsd_mean_cm']} cm/pix, Swath={hirise['swath_width_mean_km']} km")
    
    sharad = engine.compute_sharad_subsurface_radar()
    print(f"SHARAD: Res in ice={sharad['vertical_resolution_in_ice_m']} m, Utopia Ice Vol={sharad['utopia_planitia_ice_volume_km3']} km^3")
    
    telecom = engine.compute_telecommunications_architecture()
    print(f"Telecom: HGA Gain={telecom['x_band_gain_dbi']} dBi, Cumulative Data={telecom['cumulative_data_returned_tbits']} Tbits")
    
    fleet = engine.evaluate_grand_trevigintet_fleet()
    print(f"Fleet: {fleet['fleet_size']} Pillars ({fleet['designation']}), Mars Quaternity={fleet['mars_quaternity_count']}")


if __name__ == "__main__":
    main()
