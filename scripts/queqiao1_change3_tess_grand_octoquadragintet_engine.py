"""
Queqiao-1 (Earth-Moon L2 Halo), Chang'e-3 Lander & LUT (Mare Imbrium),
TESS (P/2 Lunar-Resonant Orbit) & The Grand Octoquadragintet (48-Probe Fleet).

Accurately models:
1. Queqiao-1 (Magpie Bridge 1) relay satellite:
   - Launched: 2018-05-21, injected into Earth-Moon L2 Halo Orbit (2018-06-14).
   - Halo orbit geometry: Ay ~35,000 km, Az ~13,000 km, distance ~65,000 km from Moon, ~450,000 km from Earth.
   - Period ~14 days (half synodic month).
   - NCPE (Netherlands-China Low Frequency Explorer) 1-30 MHz radio astronomy in lunar radio-quiet zone.
   - Over 8.4 years (3,070+ days) continuous relay service for Chang'e-4 & Yutu-2.
2. Chang'e-3 Lander & Lunar-based Ultraviolet Telescope (LUT):
   - Landed: 2013-12-14 in Mare Imbrium (44.1214°N, 19.5116°W).
   - Active service: 12.85 years (4,692+ days / >158 lunar day-night cycles).
   - Longest-operating active robotic surface observatory on another celestial body.
   - 150 mm f/3.75 Ritchey-Chretien NUV (245-345 nm) telescope.
   - Strict observational upper limit on lunar exospheric water vapor (< 10^11 cm^-2 / < 10^4 molecules/cm^3).
   - Extreme thermal cycling (-180°C to +120°C) with Pu-238 RHU heating.
3. TESS (Transiting Exoplanet Survey Satellite):
   - Launched: 2018-04-18, Falcon 9.
   - P/2 Lunar-Resonant Orbit: 2:1 resonance with the Moon (period ~13.7 days).
   - Perigee ~108,000 km (17 R_E), Apogee ~375,000 km (59 R_E, near-lunar).
   - 90° out-of-phase with the Moon at apogee: zero station-keeping Delta-V, stable for decades.
   - 4 wide-field CCD cameras (24°x96° swath = 2,300 sq deg), >7,900 exoplanet candidates, >885 confirmed exoplanets.
4. The Grand Octoquadragintet (人类深空四十八极终极黄金舰队):
   - 48 active deep space & cislunar probes across the solar system (173.22 AU Voyager 1 to 0.046 AU Parker Solar Probe).
   - Cosmic synchronicity with Ptolemy's 48 Classical Constellations (托勒密四十八经典星座).
   - China CNSA 8-probe deep space matrix (Tianwen-1, Tianwen-2, Queqiao-1, Queqiao-2, Chang'e-4, Chang'e-3, Chang'e-5, Chang'e-6).
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
MOON_SYNODIC_PERIOD_DAYS = 29.530589

# Launch Dates
QUEQIAO1_LAUNCH_UTC = datetime.datetime(2018, 5, 20, 21, 28, 0, tzinfo=datetime.timezone.utc)
QUEQIAO1_HALO_INSERTION_UTC = datetime.datetime(2018, 6, 14, 3, 6, 0, tzinfo=datetime.timezone.utc)

CHANGE3_LAUNCH_UTC = datetime.datetime(2013, 12, 1, 17, 30, 0, tzinfo=datetime.timezone.utc)
CHANGE3_LANDING_UTC = datetime.datetime(2013, 12, 14, 13, 11, 18, tzinfo=datetime.timezone.utc)

TESS_LAUNCH_UTC = datetime.datetime(2018, 4, 18, 22, 51, 0, tzinfo=datetime.timezone.utc)
TESS_ORBIT_INSERTION_UTC = datetime.datetime(2018, 5, 30, 0, 0, 0, tzinfo=datetime.timezone.utc)


def get_queqiao1_status(target_utc=None):
    """
    Computes Queqiao-1 Earth-Moon L2 Halo orbit astrodynamics and status.
    """
    if target_utc is None:
        target_utc = datetime.datetime(2026, 10, 19, 12, 0, 0, tzinfo=datetime.timezone.utc)

    total_days = (target_utc - QUEQIAO1_LAUNCH_UTC).total_seconds() / 86400.0
    halo_days = (target_utc - QUEQIAO1_HALO_INSERTION_UTC).total_seconds() / 86400.0
    total_years = total_days / 365.25

    # Earth-Moon L2 distance from Moon center: r_L2 ~ D_EM * (mu_M / (3 * mu_E))^(1/3)
    em_l2_dist_km = MOON_SEMI_MAJOR_AXIS_KM * (MU_MOON / (3.0 * MU_EARTH)) ** (1.0 / 3.0) # ~64,500 km
    earth_distance_km = MOON_SEMI_MAJOR_AXIS_KM + em_l2_dist_km # ~448,900 km
    one_way_light_sec = earth_distance_km / C_LIGHT_KMS # ~1.50 sec

    # Halo orbit parameters
    ay_km = 35000.0 # horizontal amplitude
    az_km = 13000.0 # vertical amplitude
    orbital_period_days = 14.0 # ~ half synodic month

    # Line of sight check: minimum angle from Moon center as seen from Earth
    min_off_axis_angle_deg = math.degrees(math.atan(az_km / earth_distance_km)) # ~1.66 deg > Moon angular radius ~0.26 deg

    return {
        "name": "Queqiao-1 (鹊桥一号)",
        "launch_utc": QUEQIAO1_LAUNCH_UTC.isoformat(),
        "halo_insertion_utc": QUEQIAO1_HALO_INSERTION_UTC.isoformat(),
        "target_utc": target_utc.isoformat(),
        "total_days": round(total_days, 2),
        "total_years": round(total_years, 2),
        "halo_days": round(halo_days, 2),
        "earth_distance_km": round(earth_distance_km, 1),
        "moon_l2_dist_km": round(em_l2_dist_km, 1),
        "one_way_light_sec": round(one_way_light_sec, 3),
        "ay_amplitude_km": ay_km,
        "az_amplitude_km": az_km,
        "halo_period_days": orbital_period_days,
        "antenna_diameter_m": 4.2,
        "has_direct_earth_los": True,
        "has_direct_farside_los": True,
        "min_off_axis_angle_deg": round(min_off_axis_angle_deg, 3),
        "ncpe_payload": "Netherlands-China Low Frequency Explorer (1-30 MHz)",
        "design_life_years": 3.0,
        "life_extension_ratio": round(total_years / 3.0, 2)
    }


def get_change3_lut_status(target_utc=None):
    """
    Computes Chang'e-3 lander and Lunar-based Ultraviolet Telescope (LUT) status.
    """
    if target_utc is None:
        target_utc = datetime.datetime(2026, 10, 19, 12, 0, 0, tzinfo=datetime.timezone.utc)

    total_days = (target_utc - CHANGE3_LAUNCH_UTC).total_seconds() / 86400.0
    surface_days = (target_utc - CHANGE3_LANDING_UTC).total_seconds() / 86400.0
    total_years = surface_days / 365.25
    lunar_cycles = surface_days / MOON_SYNODIC_PERIOD_DAYS # ~158.8 cycles

    # LUT specifications
    aperture_mm = 150.0
    focal_length_mm = 562.5
    f_ratio = focal_length_mm / aperture_mm # 3.75
    bandpass_nm = (245.0, 345.0)
    fov_deg = 1.36
    limiting_mag = 13.5

    # Exospheric water limit discovered by LUT
    water_column_density_limit_cm2 = 1.0e11
    water_number_density_limit_cm3 = 1.0e4

    return {
        "name": "Chang'e-3 Lander & LUT (嫦娥三号)",
        "landing_utc": CHANGE3_LANDING_UTC.isoformat(),
        "target_utc": target_utc.isoformat(),
        "surface_days": round(surface_days, 2),
        "total_years": round(total_years, 2),
        "lunar_day_night_cycles": round(lunar_cycles, 1),
        "landing_site": "Mare Imbrium / Statio Guanghan (44.1214°N, 19.5116°W)",
        "aperture_mm": aperture_mm,
        "f_ratio": f_ratio,
        "bandpass_nm": bandpass_nm,
        "fov_deg": fov_deg,
        "limiting_mag": limiting_mag,
        "water_column_density_limit_cm2": water_column_density_limit_cm2,
        "water_number_density_limit_cm3": water_number_density_limit_cm3,
        "rhu_pu238": True,
        "longest_operating_surface_observatory": True
    }


def get_tess_status(target_utc=None):
    """
    Computes TESS P/2 Lunar-Resonant Orbit dynamics and status.
    """
    if target_utc is None:
        target_utc = datetime.datetime(2026, 10, 19, 12, 0, 0, tzinfo=datetime.timezone.utc)

    total_days = (target_utc - TESS_LAUNCH_UTC).total_seconds() / 86400.0
    total_years = total_days / 365.25

    # Orbit parameters
    perigee_km = 108000.0
    apogee_km = 375000.0
    semi_major_axis_km = (perigee_km + apogee_km) / 2.0 # 241,500 km
    eccentricity = (apogee_km - perigee_km) / (apogee_km + perigee_km) # ~0.5528
    orbital_period_days = 13.66 # exactly half Moon's sidereal period

    # Resonance ratio with the Moon
    resonance_ratio = MOON_SIDEREAL_PERIOD_DAYS / orbital_period_days # 2.000

    # Perigee in Earth radii
    perigee_re = perigee_km / R_EARTH_KM
    apogee_re = apogee_km / R_EARTH_KM

    # Total completed orbits
    completed_orbits = total_days / orbital_period_days

    return {
        "name": "TESS (Transiting Exoplanet Survey Satellite)",
        "launch_utc": TESS_LAUNCH_UTC.isoformat(),
        "target_utc": target_utc.isoformat(),
        "total_days": round(total_days, 2),
        "total_years": round(total_years, 2),
        "orbital_period_days": round(orbital_period_days, 2),
        "resonance_ratio": round(resonance_ratio, 2),
        "is_p_over_2_resonance": True,
        "perigee_km": perigee_km,
        "apogee_km": apogee_km,
        "semi_major_axis_km": semi_major_axis_km,
        "eccentricity": round(eccentricity, 4),
        "perigee_re": round(perigee_re, 1),
        "apogee_re": round(apogee_re, 1),
        "completed_orbits": round(completed_orbits, 1),
        "is_outside_van_allen_belts": perigee_re > 10.0,
        "cameras_count": 4,
        "total_fov_deg": "24° x 96° (2,300 sq deg)",
        "candidate_exoplanets": 7900,
        "confirmed_exoplanets": 885
    }


def get_grand_octoquadragintet_fleet():
    """
    Returns the complete 48-probe Grand Octoquadragintet fleet of humanity active in deep space and cislunar space as of 2026-10-19.
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
        {"name": "Queqiao-1", "heliocentric_au": 1.000, "regime": "Earth-Moon L2 Halo", "agency": "CNSA"},
        {"name": "LRO", "heliocentric_au": 1.000, "regime": "Lunar Orbit", "agency": "NASA"},
        {"name": "Chandrayaan-2", "heliocentric_au": 1.000, "regime": "Lunar Orbit", "agency": "ISRO"},
        {"name": "Danuri (KPLO)", "heliocentric_au": 1.000, "regime": "Lunar Orbit", "agency": "KARI"},
        {"name": "CAPSTONE", "heliocentric_au": 1.000, "regime": "Lunar NRHO", "agency": "NASA"},
        {"name": "Queqiao-2", "heliocentric_au": 1.000, "regime": "Lunar Frozen Orbit", "agency": "CNSA"},
        {"name": "Chang'e-4 / Yutu-2", "heliocentric_au": 1.000, "regime": "Lunar Far Side Surface", "agency": "CNSA"},
        {"name": "Chang'e-3 Lander & LUT", "heliocentric_au": 1.000, "regime": "Lunar Near Side Surface", "agency": "CNSA"},
        {"name": "ARTEMIS P1", "heliocentric_au": 1.000, "regime": "Lunar Retrograde Orbit", "agency": "NASA"},
        {"name": "ARTEMIS P2", "heliocentric_au": 1.000, "regime": "Lunar Prograde Orbit", "agency": "NASA"},
        {"name": "Chang'e-5 Orbiter", "heliocentric_au": 1.000, "regime": "Lunar DRO", "agency": "CNSA"},
        {"name": "Chandrayaan-3 PM", "heliocentric_au": 1.000, "regime": "Cislunar HEO", "agency": "ISRO"},
        {"name": "TESS", "heliocentric_au": 1.000, "regime": "P/2 Lunar-Resonant Orbit", "agency": "NASA"},
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
    fleet = get_grand_octoquadragintet_fleet()
    assert len(fleet) == 48, f"Expected 48 probes, got {len(fleet)}"
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
    fleet = get_grand_octoquadragintet_fleet()
    agencies = {}
    for p in fleet:
        ag = p["agency"]
        agencies[ag] = agencies.get(ag, 0) + 1
    return agencies


def get_cnsa_probes():
    fleet = get_grand_octoquadragintet_fleet()
    return [p for p in fleet if "CNSA" in p["agency"]]


if __name__ == "__main__":
    q1 = get_queqiao1_status()
    print("=== Queqiao-1 Status ===")
    for k, v in q1.items():
        print(f"  {k}: {v}")

    ce3 = get_change3_lut_status()
    print("\n=== Chang'e-3 LUT Status ===")
    for k, v in ce3.items():
        print(f"  {k}: {v}")

    tess = get_tess_status()
    print("\n=== TESS Status ===")
    for k, v in tess.items():
        print(f"  {k}: {v}")

    extremes = compute_fleet_extremes()
    print("\n=== Grand Octoquadragintet Extremes ===")
    for k, v in extremes.items():
        print(f"  {k}: {v}")

    agencies = get_agency_breakdown()
    print("\n=== Agency Breakdown ===")
    for k, v in sorted(agencies.items(), key=lambda x: x[1], reverse=True):
        print(f"  {k}: {v}")

    cnsa = get_cnsa_probes()
    print(f"\n=== CNSA Probes ({len(cnsa)}) ===")
    for p in cnsa:
        print(f"  {p['name']} ({p['regime']})")
