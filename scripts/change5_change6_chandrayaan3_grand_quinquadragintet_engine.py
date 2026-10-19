"""
Chang'e-5 DRO, Chang'e-6 Sun-Earth L2, Chandrayaan-3 PM (SHAPE) & The Grand Quinquadragintet Fleet Engine.
Accurately models:
1. Chang'e-5 Orbiter extended mission timeline (launched 2020-11-23, sample return, Sun-Earth L1, Lunar DRO).
2. Lunar Distant Retrograde Orbit (DRO) astrodynamics:
   - CR3BP synodic frame stability (Lyapunov stable, zero station-keeping Delta-V < 2 m/s/yr)
   - Orbit size (radius 70,000 - 80,000 km > Moon Hill sphere 66,100 km)
   - Orbital period ~14 days (2:1 resonance with Moon's sidereal period 27.32d)
   - Spacecraft VLBI, navigation & lunar constellation anchor.
3. Chang'e-6 Orbiter extended mission timeline (launched 2024-05-03, far-side sample return, Sun-Earth L2 capture 2024-09-09).
4. Sun-Earth L2 Halo orbit dynamics:
   - Distance ~1.5 million km, heliocentric 1.010 AU
   - The SEL2 Quaternary Fleet: JWST, Euclid, Spektr-RG, Chang'e-6.
5. Chandrayaan-3 Propulsion Module (PM / SHAPE) timeline (launched 2023-07-14, lunar landing 2023-08-23, TEI 2023-10-13).
6. Double lunar gravity-assist flybys (Nov 2025: 3,740 km & 4,537 km) to 365,000 x 983,000 km cislunar HEO.
7. SHAPE (Spectro-polarimetry of Habitable Planet Earth) physics:
   - 0.3 - 1.0 um spectral band
   - Ocean glint Fresnel polarization at Brewster angle (53.1 deg, ~100% linear polarization)
   - Cloud rainbow scattering peak at 140 deg
   - Vegetation Red Edge (VRE) at 700 nm & Earth as an exoplanet analog.
8. The Grand Quinquadragintet: Complete 45-probe deep space fleet distribution across the solar system.
"""

import math
import datetime

# Physical and Astronomical Constants
AU_KM = 149597870.7
C_LIGHT_KMS = 299792.458
MU_EARTH = 398600.4418  # km^3 / s^2
MU_MOON = 4902.800066   # km^3 / s^2
R_EARTH_KM = 6378.137
R_MOON_KM = 1737.4
MOON_SEMI_MAJOR_AXIS_KM = 384400.0
MOON_SIDEREAL_PERIOD_DAYS = 27.321661

# Mission Launch Dates
CHANGE5_LAUNCH_UTC = datetime.datetime(2020, 11, 23, 20, 30, 12, tzinfo=datetime.timezone.utc)
CHANGE5_SAMPLE_RETURN_UTC = datetime.datetime(2020, 12, 16, 17, 59, 0, tzinfo=datetime.timezone.utc)
CHANGE5_L1_ARRIVAL_UTC = datetime.datetime(2021, 3, 15, 5, 39, 0, tzinfo=datetime.timezone.utc)
CHANGE5_DRO_ARRIVAL_UTC = datetime.datetime(2022, 2, 15, 0, 0, 0, tzinfo=datetime.timezone.utc)

CHANGE6_LAUNCH_UTC = datetime.datetime(2024, 5, 3, 9, 27, 29, tzinfo=datetime.timezone.utc)
CHANGE6_LANDING_UTC = datetime.datetime(2024, 6, 1, 22, 23, 16, tzinfo=datetime.timezone.utc)
CHANGE6_SAMPLE_RETURN_UTC = datetime.datetime(2024, 6, 25, 6, 7, 0, tzinfo=datetime.timezone.utc)
CHANGE6_L2_ARRIVAL_UTC = datetime.datetime(2024, 9, 9, 12, 0, 0, tzinfo=datetime.timezone.utc)

CHANDRAYAAN3_LAUNCH_UTC = datetime.datetime(2023, 7, 14, 9, 5, 17, tzinfo=datetime.timezone.utc)
CHANDRAYAAN3_LANDING_UTC = datetime.datetime(2023, 8, 23, 12, 34, 0, tzinfo=datetime.timezone.utc)
CHANDRAYAAN3_TEI_UTC = datetime.datetime(2023, 10, 13, 0, 0, 0, tzinfo=datetime.timezone.utc)
CHANDRAYAAN3_MOON_DEPARTURE_UTC = datetime.datetime(2023, 11, 10, 0, 0, 0, tzinfo=datetime.timezone.utc)

# Physical parameters of Lunar Distant Retrograde Orbit (DRO)
LUNAR_HILL_RADIUS_KM = MOON_SEMI_MAJOR_AXIS_KM * (MU_MOON / (3.0 * MU_EARTH)) ** (1.0 / 3.0) # ~66,100 km
DRO_AVERAGE_RADIUS_KM = 75000.0  # km from Moon center
DRO_ORBITAL_PERIOD_DAYS = 13.66  # ~ half sidereal month (2:1 resonance)
DRO_ANNUAL_STATION_KEEPING_DELTA_V = 1.5  # m/s / year (virtually zero)

# SHAPE parameters
REFRACTIVE_INDEX_WATER = 1.333
REFRACTIVE_INDEX_AIR = 1.000
BREWSTER_ANGLE_DEG = math.degrees(math.atan(REFRACTIVE_INDEX_WATER / REFRACTIVE_INDEX_AIR)) # ~53.12 deg
RAINBOW_SCATTERING_ANGLE_DEG = 140.0
VEGETATION_RED_EDGE_WAVELENGTH_NM = 700.0


def get_change5_timeline(target_utc=None):
    if target_utc is None:
        target_utc = datetime.datetime(2026, 10, 19, 12, 0, 0, tzinfo=datetime.timezone.utc)
    delta = target_utc - CHANGE5_LAUNCH_UTC
    total_days = delta.total_seconds() / 86400.0
    total_years = total_days / 365.25
    dro_days = (target_utc - CHANGE5_DRO_ARRIVAL_UTC).total_seconds() / 86400.0
    return {
        "launch_utc": CHANGE5_LAUNCH_UTC.isoformat(),
        "target_utc": target_utc.isoformat(),
        "total_days": round(total_days, 2),
        "total_years": round(total_years, 2),
        "dro_days": round(dro_days, 2),
        "sample_returned_grams": 1731.0,
        "sample_site": "Mons Rümker / Statio Tianchuan (43.0576°N, 51.9161°W)",
        "current_regime": "Lunar Distant Retrograde Orbit (DRO)"
    }


def compute_lunar_dro_dynamics():
    """
    Computes Distant Retrograde Orbit astrodynamic characteristics.
    """
    hill_radius = LUNAR_HILL_RADIUS_KM
    dro_radius = DRO_AVERAGE_RADIUS_KM
    ratio_to_hill = dro_radius / hill_radius
    resonance_ratio = MOON_SIDEREAL_PERIOD_DAYS / DRO_ORBITAL_PERIOD_DAYS
    return {
        "lunar_hill_radius_km": round(hill_radius, 1),
        "dro_average_radius_km": dro_radius,
        "ratio_to_hill_sphere": round(ratio_to_hill, 3),
        "is_outside_hill_sphere": dro_radius > hill_radius,
        "orbital_period_days": DRO_ORBITAL_PERIOD_DAYS,
        "resonance_with_moon": round(resonance_ratio, 2),
        "station_keeping_delta_v_ms_yr": DRO_ANNUAL_STATION_KEEPING_DELTA_V,
        "stability_type": "Lyapunov linearly stable in CR3BP synodic frame"
    }


def get_change6_timeline(target_utc=None):
    if target_utc is None:
        target_utc = datetime.datetime(2026, 10, 19, 12, 0, 0, tzinfo=datetime.timezone.utc)
    delta = target_utc - CHANGE6_LAUNCH_UTC
    total_days = delta.total_seconds() / 86400.0
    total_years = total_days / 365.25
    l2_days = (target_utc - CHANGE6_L2_ARRIVAL_UTC).total_seconds() / 86400.0
    return {
        "launch_utc": CHANGE6_LAUNCH_UTC.isoformat(),
        "target_utc": target_utc.isoformat(),
        "total_days": round(total_days, 2),
        "total_years": round(total_years, 2),
        "l2_days": round(l2_days, 2),
        "sample_returned_grams": 1935.3,
        "sample_site": "Lunar Far Side / South Pole-Aitken Apollo Basin (41.625°S, 153.985°W)",
        "current_regime": "Sun-Earth L2 Halo Orbit"
    }


def compute_change6_l2_halo_orbit():
    """
    Computes Sun-Earth L2 Halo orbit characteristics for Chang'e-6.
    """
    l2_distance_km = 1500000.0
    light_time_s = l2_distance_km / C_LIGHT_KMS
    heliocentric_au = 1.010
    halo_period_days = 180.0
    return {
        "l2_distance_km": l2_distance_km,
        "light_time_one_way_s": round(light_time_s, 2),
        "light_time_round_trip_s": round(2 * light_time_s, 2),
        "heliocentric_au": heliocentric_au,
        "halo_period_days": halo_period_days,
        "sel2_quaternary_fleet": ["JWST", "Euclid", "Spektr-RG", "Chang'e-6 Orbiter"]
    }


def get_chandrayaan3_pm_timeline(target_utc=None):
    if target_utc is None:
        target_utc = datetime.datetime(2026, 10, 19, 12, 0, 0, tzinfo=datetime.timezone.utc)
    delta = target_utc - CHANDRAYAAN3_LAUNCH_UTC
    total_days = delta.total_seconds() / 86400.0
    total_years = total_days / 365.25
    return {
        "launch_utc": CHANDRAYAAN3_LAUNCH_UTC.isoformat(),
        "target_utc": target_utc.isoformat(),
        "total_days": round(total_days, 2),
        "total_years": round(total_years, 2),
        "tei_date": CHANDRAYAAN3_TEI_UTC.isoformat(),
        "current_orbit": "365,000 x 983,000 km Cislunar HEO (inc 22°)",
        "current_regime": "Cislunar High Earth Orbit (Earth as Exoplanet Analog)",
        "primary_instrument": "SHAPE (Spectro-polarimetry of Habitable Planet Earth)"
    }


def compute_shape_earth_polarimetry():
    """
    Computes physical optical polarization parameters of Earth as observed by SHAPE.
    """
    theta_b = BREWSTER_ANGLE_DEG
    water_pol_max = 1.00  # 100% linear polarization at Brewster angle for Fresnel reflection
    rainbow_angle = RAINBOW_SCATTERING_ANGLE_DEG
    vre_nm = VEGETATION_RED_EDGE_WAVELENGTH_NM
    return {
        "spectral_range_um": [0.3, 1.0],
        "ocean_glint_brewster_angle_deg": round(theta_b, 2),
        "ocean_glint_max_polarization": water_pol_max,
        "cloud_rainbow_scattering_angle_deg": rainbow_angle,
        "vegetation_red_edge_nm": vre_nm,
        "scientific_role": "Earth as benchmark for biosignatures & oceans in habitable exoplanets"
    }


def get_grand_quinquadragintet_fleet():
    """
    Returns the complete 45-probe Grand Quinquadragintet fleet of humanity active in deep space and cislunar space as of 2026-10-19.
    Ordered by descending heliocentric distance (AU).
    """
    fleet = [
        {"name": "Voyager 1", "heliocentric_au": 173.22, "regime": "Interstellar Medium", "agency": "NASA"},
        {"name": "Voyager 2", "heliocentric_au": 144.29, "regime": "Interstellar Medium", "agency": "NASA"},
        {"name": "New Horizons", "heliocentric_au": 65.92, "regime": "Kuiper Belt", "agency": "NASA"},
        {"name": "Juno", "heliocentric_au": 5.20, "regime": "Jupiter System", "agency": "NASA"},
        {"name": "JUICE", "heliocentric_au": 5.20, "regime": "Jupiter Cruise", "agency": "ESA"},
        {"name": "Europa Clipper", "heliocentric_au": 5.20, "regime": "Jupiter Cruise", "agency": "NASA"},
        {"name": "Lucy", "heliocentric_au": 5.04, "regime": "Trojan Asteroid Cruise", "agency": "NASA"},
        {"name": "Psyche", "heliocentric_au": 2.042, "regime": "Main Asteroid Belt", "agency": "NASA"},
        {"name": "2001 Mars Odyssey", "heliocentric_au": 1.579, "regime": "Mars Orbit", "agency": "NASA"},
        {"name": "Mars Express", "heliocentric_au": 1.579, "regime": "Mars Orbit", "agency": "ESA"},
        {"name": "ExoMars TGO", "heliocentric_au": 1.579, "regime": "Mars Orbit", "agency": "ESA/Roscosmos"},
        {"name": "MAVEN", "heliocentric_au": 1.579, "regime": "Mars Orbit", "agency": "NASA"},
        {"name": "Hope Probe", "heliocentric_au": 1.579, "regime": "Mars Orbit", "agency": "UAESA"},
        {"name": "Curiosity", "heliocentric_au": 1.524, "regime": "Mars Surface (Gale)", "agency": "NASA"},
        {"name": "Perseverance", "heliocentric_au": 1.524, "regime": "Mars Surface (Jezero)", "agency": "NASA"},
        {"name": "Tianwen-1 Orbiter", "heliocentric_au": 1.524, "regime": "Mars Orbit", "agency": "CNSA"},
        {"name": "MRO", "heliocentric_au": 1.524, "regime": "Mars Orbit", "agency": "NASA"},
        {"name": "Hera", "heliocentric_au": 1.304, "regime": "Didymos Cruise", "agency": "ESA"},
        {"name": "Hayabusa2#", "heliocentric_au": 1.120, "regime": "1998 KY26 Cruise", "agency": "JAXA"},
        {"name": "OSIRIS-APEX", "heliocentric_au": 1.010, "regime": "Apophis Cruise", "agency": "NASA"},
        {"name": "JWST", "heliocentric_au": 1.010, "regime": "Sun-Earth L2", "agency": "NASA/ESA/CSA"},
        {"name": "Euclid", "heliocentric_au": 1.010, "regime": "Sun-Earth L2", "agency": "ESA"},
        {"name": "Spektr-RG", "heliocentric_au": 1.010, "regime": "Sun-Earth L2", "agency": "Roscosmos/DLR"},
        {"name": "Chang'e-6 Orbiter", "heliocentric_au": 1.010, "regime": "Sun-Earth L2", "agency": "CNSA"},
        {"name": "Tianwen-2", "heliocentric_au": 1.001, "regime": "Kamo'oalewa Cruise", "agency": "CNSA"},
        {"name": "LRO", "heliocentric_au": 1.000, "regime": "Lunar Orbit", "agency": "NASA"},
        {"name": "Chandrayaan-2", "heliocentric_au": 1.000, "regime": "Lunar Orbit", "agency": "ISRO"},
        {"name": "Danuri (KPLO)", "heliocentric_au": 1.000, "regime": "Lunar Orbit", "agency": "KARI"},
        {"name": "CAPSTONE", "heliocentric_au": 1.000, "regime": "Lunar NRHO", "agency": "NASA"},
        {"name": "Queqiao-2", "heliocentric_au": 1.000, "regime": "Lunar Frozen Orbit", "agency": "CNSA"},
        {"name": "Chang'e-4 / Yutu-2", "heliocentric_au": 1.000, "regime": "Lunar Far Side Surface", "agency": "CNSA"},
        {"name": "ARTEMIS P1", "heliocentric_au": 1.000, "regime": "Lunar Retrograde Orbit", "agency": "NASA"},
        {"name": "ARTEMIS P2", "heliocentric_au": 1.000, "regime": "Lunar Prograde Orbit", "agency": "NASA"},
        {"name": "Chang'e-5 Orbiter", "heliocentric_au": 1.000, "regime": "Lunar DRO", "agency": "CNSA"},
        {"name": "Chandrayaan-3 PM", "heliocentric_au": 1.000, "regime": "Cislunar HEO", "agency": "ISRO"},
        {"name": "IBEX", "heliocentric_au": 1.000, "regime": "3:1 Lunar-Resonant Orbit", "agency": "NASA"},
        {"name": "SOHO", "heliocentric_au": 0.990, "regime": "Sun-Earth L1", "agency": "ESA/NASA"},
        {"name": "Wind", "heliocentric_au": 0.990, "regime": "Sun-Earth L1", "agency": "NASA"},
        {"name": "ACE", "heliocentric_au": 0.990, "regime": "Sun-Earth L1", "agency": "NASA"},
        {"name": "DSCOVR", "heliocentric_au": 0.990, "regime": "Sun-Earth L1", "agency": "NOAA/NASA"},
        {"name": "Aditya-L1", "heliocentric_au": 0.990, "regime": "Sun-Earth L1", "agency": "ISRO"},
        {"name": "STEREO-A", "heliocentric_au": 0.962, "regime": "Heliocentric Orbit", "agency": "NASA"},
        {"name": "BepiColombo", "heliocentric_au": 0.387, "regime": "Mercury Approach", "agency": "ESA/JAXA"},
        {"name": "Solar Orbiter", "heliocentric_au": 0.280, "regime": "Inner Heliocentric Orbit", "agency": "ESA/NASA"},
        {"name": "Parker Solar Probe", "heliocentric_au": 0.046, "regime": "Extreme Solar Corona", "agency": "NASA"}
    ]
    return fleet


def compute_fleet_extremes():
    fleet = get_grand_quinquadragintet_fleet()
    assert len(fleet) == 45, f"Expected 45 probes, got {len(fleet)}"
    r_max = fleet[0]["heliocentric_au"]  # Voyager 1
    r_min = fleet[-1]["heliocentric_au"] # Parker Solar Probe
    distance_ratio = r_max / r_min
    solar_flux_ratio = distance_ratio ** 2
    return {
        "probe_count": len(fleet),
        "r_max_au": r_max,
        "r_min_au": r_min,
        "distance_ratio": round(distance_ratio, 2),
        "solar_flux_ratio": round(solar_flux_ratio, 2)
    }


def get_agency_breakdown():
    fleet = get_grand_quinquadragintet_fleet()
    agencies = {}
    for p in fleet:
        ag = p["agency"]
        agencies[ag] = agencies.get(ag, 0) + 1
    return agencies


if __name__ == "__main__":
    t5 = get_change5_timeline()
    t6 = get_change6_timeline()
    tch3 = get_chandrayaan3_pm_timeline()
    dro = compute_lunar_dro_dynamics()
    shape = compute_shape_earth_polarimetry()
    extremes = compute_fleet_extremes()
    print("CE-5 Timeline:", t5)
    print("CE-6 Timeline:", t6)
    print("CH-3 PM Timeline:", tch3)
    print("DRO Dynamics:", dro)
    print("SHAPE Polarimetry:", shape)
    print("Fleet Extremes (45 probes):", extremes)
