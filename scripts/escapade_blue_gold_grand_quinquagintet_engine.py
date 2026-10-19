"""
ESCAPADE Twin Probes (Blue & Gold), Loiter-Oberth Trajectory &
The Grand Quinquagintet (50-Probe Human Deep Space Fleet).

Accurately models:
1. ESCAPADE (Escape and Plasma Acceleration and Dynamics Explorers):
   - PI Institution: UC Berkeley Space Sciences Laboratory (SSL), PI: Robert Lillis.
   - Spacecraft Builder: Rocket Lab USA (custom Photon bus).
   - Launch Vehicle: Blue Origin New Glenn 2 (LC-36 Cape Canaveral).
   - Launch Date: 2025-11-13 20:55 UTC (3:55 PM EST).
   - Twin Probes: ESCAPADE A ("Blue") and ESCAPADE B ("Gold").
   - Dry Mass: 209 kg each, Wet Mass: 535 kg each (Total: 1,070 kg).
   - NASA SIMPLEx program (<$80 million total cost).
2. The "Loiter & Oberth" Trajectory Innovation:
   - 12-month kidney bean-shaped loiter orbit around Sun-Earth L2 (anti-sunward side up to 2.5 million km / ~390 R_E).
   - Distant Earth magnetotail crossings at ~320 R_E and ~80 R_E (March 2026).
   - Returning to Earth for a 500 km perigee flyby Oberth maneuver in November 2026.
   - Perigee Oberth impulsive Delta-V ~405 m/s yielding hyperbolic excess v_inf ~ 3.0 km/s (C3 ~ 9 km^2/s^2),
     achieving >7.3x velocity multiplication efficiency compared to deep-space burn.
   - Mars arrival: September 2027.
3. Science Payload & Mars Stereo Magnetosphere Physics:
   - EMM: Triaxial fluxgate magnetometers (NASA Goddard).
   - EMA: Suprathermal ion and electron electrostatic analyzers (UC Berkeley SSL).
   - ELP: Multi-needle Langmuir probe (Embry-Riddle Aeronautical Univ).
   - VIROS: Visible and infrared observation cameras (Northern Arizona Univ).
   - Mars hybrid magnetosphere & atmospheric sputtering/escape stereo resolution.
4. The Grand Quinquagintet (人类深空五十极半百黄金舰队):
   - Exactly 50 active deep space, lunar, and Lagrangian probes across the solar system.
   - Spanning from Voyager 1 at 173.22 AU to Parker Solar Probe at 0.046 AU.
   - Half-century (50 probes) milestone for human interplanetary civilization.
"""

import math
import datetime

# Physical and Astronomical Constants
AU_KM = 149597870.7
C_LIGHT_KMS = 299792.458
MU_EARTH = 398600.4418  # km^3 / s^2
MU_SUN = 1.32712440018e11 # km^3 / s^2
R_EARTH_KM = 6378.137
SOLAR_CONSTANT_1AU = 1361.0 # W / m^2

# Mission Dates
ESCAPADE_LAUNCH_UTC = datetime.datetime(2025, 11, 13, 20, 55, 0, tzinfo=datetime.timezone.utc)
ESCAPADE_OBERTH_PERIGEE_UTC = datetime.datetime(2026, 11, 15, 12, 0, 0, tzinfo=datetime.timezone.utc)
ESCAPADE_MARS_ARRIVAL_UTC = datetime.datetime(2027, 9, 15, 0, 0, 0, tzinfo=datetime.timezone.utc)

# Spacecraft Parameters
DRY_MASS_KG = 209.0
PROP_MASS_KG = 326.0
WET_MASS_KG = 535.0


def get_escapade_mission_status(target_utc=None):
    """
    Computes ESCAPADE mission timeline, current phase, and days in flight.
    """
    if target_utc is None:
        target_utc = datetime.datetime(2026, 10, 19, 12, 0, 0, tzinfo=datetime.timezone.utc)

    total_days = (target_utc - ESCAPADE_LAUNCH_UTC).total_seconds() / 86400.0
    days_to_perigee = (ESCAPADE_OBERTH_PERIGEE_UTC - target_utc).total_seconds() / 86400.0
    days_to_mars = (ESCAPADE_MARS_ARRIVAL_UTC - target_utc).total_seconds() / 86400.0

    # In October 2026, probes are in the returning segment of the Sun-Earth L2 loiter orbit
    phase = "Sun-Earth L2 Loiter Orbit (Returning to Earth for Oberth Flyby)"
    distance_earth_km = 1.48e6 # ~1.48 million km
    distance_earth_re = distance_earth_km / R_EARTH_KM # ~232 Earth radii
    heliocentric_au = 1.008 # Near Earth orbit

    return {
        "mission_name": "ESCAPADE (Escape and Plasma Acceleration and Dynamics Explorers)",
        "twin_spacecraft": ["ESCAPADE A (Blue)", "ESCAPADE B (Gold)"],
        "pi_institution": "UC Berkeley Space Sciences Laboratory (SSL)",
        "principal_investigator": "Robert Lillis",
        "spacecraft_bus": "Rocket Lab Photon",
        "launch_vehicle": "Blue Origin New Glenn 2",
        "launch_date_utc": ESCAPADE_LAUNCH_UTC.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "target_date_utc": target_utc.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "days_in_space": round(total_days, 2),
        "days_to_perigee_oberth": round(days_to_perigee, 1),
        "days_to_mars_arrival": round(days_to_mars, 1),
        "mission_phase": phase,
        "current_distance_earth_km": distance_earth_km,
        "current_distance_earth_re": round(distance_earth_re, 1),
        "heliocentric_au": heliocentric_au,
        "dry_mass_kg_each": DRY_MASS_KG,
        "wet_mass_kg_each": WET_MASS_KG,
        "total_launch_mass_kg": WET_MASS_KG * 2,
    }


def compute_oberth_maneuver(perigee_alt_km=500.0, v_inf_kms=3.0):
    """
    Computes kinematics and energy multiplication of the perigee Oberth maneuver.
    
    Parameters:
        perigee_alt_km: Altitude of perigee flyby above Earth surface (km)
        v_inf_kms: Required hyperbolic excess velocity for Mars transfer (km/s)
    """
    r_p = R_EARTH_KM + perigee_alt_km
    v_circ = math.sqrt(MU_EARTH / r_p)
    v_esc = math.sqrt(2.0 * MU_EARTH / r_p)
    
    # Target hyperbolic velocity at perigee
    # v_p^2 = v_esc^2 + v_inf^2
    v_p_hyperbola = math.sqrt(v_esc**2 + v_inf_kms**2)
    
    # Incoming parabolic approach velocity from deep loiter orbit
    v_in = v_esc
    
    # Required impulsive velocity boost at perigee
    delta_v_oberth = v_p_hyperbola - v_in
    
    # Required delta-v if performed in deep space (where v ~ 0)
    delta_v_deep_space = v_inf_kms
    
    # Oberth efficiency ratio
    oberth_amplification = delta_v_deep_space / delta_v_oberth
    
    # Specific mechanical energy gained per unit mass (MJ/kg)
    c3 = v_inf_kms ** 2 # km^2 / s^2
    specific_energy_gain_mj_kg = 0.5 * (v_p_hyperbola**2 - v_in**2) # km^2/s^2 = MJ/kg
    
    return {
        "perigee_alt_km": perigee_alt_km,
        "r_p_km": round(r_p, 3),
        "v_circular_kms": round(v_circ, 4),
        "v_escape_kms": round(v_esc, 4),
        "v_hyperbolic_perigee_kms": round(v_p_hyperbola, 4),
        "v_inf_kms": v_inf_kms,
        "c3_km2_s2": round(c3, 2),
        "delta_v_oberth_ms": round(delta_v_oberth * 1000.0, 1),
        "delta_v_deep_space_ms": round(delta_v_deep_space * 1000.0, 1),
        "oberth_amplification_factor": round(oberth_amplification, 2),
        "specific_energy_gain_mj_kg": round(specific_energy_gain_mj_kg, 2),
    }


def get_science_payload_specs():
    """
    Returns science payload suite for ESCAPADE twin probes.
    """
    return [
        {
            "name": "EMM (ESCAPADE Magnetometer)",
            "institution": "NASA Goddard Space Flight Center",
            "type": "Dual triaxial fluxgate magnetometers on 1.5 m boom",
            "science_goal": "Measure Martian crustal remnant fields, solar wind IMF draping, and magnetic reconnection."
        },
        {
            "name": "EMA (Electrostatic Analyzer)",
            "institution": "UC Berkeley Space Sciences Laboratory",
            "type": "Top-hat electrostatic analyzer for electrons (0.5 eV - 10 keV) and ions (10 eV - 20 keV)",
            "science_goal": "Determine 3D velocity distribution of escaping O+, O2+, and CO2+ ions and solar wind protons."
        },
        {
            "name": "ELP (m-NLP Langmuir Probe)",
            "institution": "Embry-Riddle Aeronautical University",
            "type": "Multi-needle Langmuir probe",
            "science_goal": "High-cadence thermal plasma density (10 - 10^6 cm^-3) and electron temperature measurements."
        },
        {
            "name": "VIROS (Visible and Infrared Observation System)",
            "institution": "Northern Arizona University",
            "type": "Visible and thermal infrared contextual camera system",
            "science_goal": "Optical navigation, surface monitoring, and nightside auroral emission imaging."
        }
    ]


def get_grand_quinquagintet_fleet():
    """
    Returns the complete 50-probe Grand Quinquagintet fleet of humanity active in deep space
    and cislunar space as of 2026-10-19.
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
        {"name": "ESCAPADE Blue", "heliocentric_au": 1.008, "regime": "Sun-Earth L2 Loiter (Mars Transfer)", "agency": "NASA"},
        {"name": "ESCAPADE Gold", "heliocentric_au": 1.008, "regime": "Sun-Earth L2 Loiter (Mars Transfer)", "agency": "NASA"},
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
    """
    Computes physical extrema across the 50-probe Grand Quinquagintet fleet.
    """
    fleet = get_grand_quinquagintet_fleet()
    assert len(fleet) == 50, f"Expected 50 probes, got {len(fleet)}"
    
    r_max = fleet[0]["heliocentric_au"]  # Voyager 1
    r_min = fleet[-1]["heliocentric_au"] # Parker Solar Probe
    distance_ratio = r_max / r_min
    solar_flux_ratio = distance_ratio ** 2

    # Communication Light Time
    light_time_max_sec = (r_max * AU_KM) / C_LIGHT_KMS # ~24.01 h
    light_time_min_sec = (384400.0) / C_LIGHT_KMS       # ~1.282 s (Earth-Moon)
    light_time_ratio = light_time_max_sec / light_time_min_sec

    # Speed Extremes
    v_max_kms = 192.0 # Parker Solar Probe perihelion speed
    v_min_kms = 0.00000688 # 1998 KY26 escape speed (6.88 mm/s)
    speed_ratio = v_max_kms / v_min_kms

    # Thermal Extremes
    t_max_k = 1673.15 # Parker Solar Probe heat shield (~1400°C)
    t_min_k = 6.70    # Deep Kuiper Belt cold trap (Voyager / New Horizons)
    delta_t_k = t_max_k - t_min_k

    # Agency Breakdown
    agencies = {}
    for p in fleet:
        ag = p["agency"]
        agencies[ag] = agencies.get(ag, 0) + 1

    return {
        "probe_count": len(fleet),
        "r_max_au": r_max,
        "r_min_au": r_min,
        "distance_ratio": round(distance_ratio, 2),
        "solar_flux_ratio": round(solar_flux_ratio, 2),
        "light_time_max_hours": round(light_time_max_sec / 3600.0, 2),
        "light_time_min_sec": round(light_time_min_sec, 3),
        "light_time_ratio": round(light_time_ratio, 1),
        "speed_ratio": round(speed_ratio, 1),
        "thermal_span_k": round(delta_t_k, 2),
        "agency_breakdown": agencies,
    }


if __name__ == "__main__":
    status = get_escapade_mission_status()
    oberth = compute_oberth_maneuver()
    extremes = compute_fleet_extremes()

    print("=" * 70)
    print("ESCAPADE Twin Probes (Blue & Gold) & The Grand Quinquagintet (50 Probes)")
    print("=" * 70)
    print(f"Mission: {status['mission_name']}")
    print(f"Twin Probes: {', '.join(status['twin_spacecraft'])}")
    print(f"PI: {status['principal_investigator']} ({status['pi_institution']})")
    print(f"Spacecraft Bus: {status['spacecraft_bus']} | Rocket: {status['launch_vehicle']}")
    print(f"Days in Space: {status['days_in_space']} days")
    print(f"Current Phase: {status['mission_phase']}")
    print(f"Days to Oberth Perigee Burn: {status['days_to_perigee_oberth']} days")
    print(f"Days to Mars Arrival: {status['days_to_mars_arrival']} days")
    print(f"Mass per probe: {status['dry_mass_kg_each']} kg dry / {status['wet_mass_kg_each']} kg wet")
    print("\n--- Oberth Flyby Maneuver Kinematics (Nov 2026) ---")
    print(f"Perigee Altitude: {oberth['perigee_alt_km']} km (r_p = {oberth['r_p_km']} km)")
    print(f"Escape Velocity at Perigee: {oberth['v_escape_kms']} km/s")
    print(f"Hyperbolic Velocity at Perigee: {oberth['v_hyperbolic_perigee_kms']} km/s")
    print(f"Impulsive Oberth Delta-V: {oberth['delta_v_oberth_ms']} m/s")
    print(f"Deep Space Delta-V equivalent: {oberth['delta_v_deep_space_ms']} m/s")
    print(f"Oberth Amplification Factor: {oberth['oberth_amplification_factor']}x")
    print(f"Specific Energy Gain: {oberth['specific_energy_gain_mj_kg']} MJ/kg")
    print("\n--- The Grand Quinquagintet (50-Probe Fleet) ---")
    print(f"Total Operational Probes: {extremes['probe_count']}")
    print(f"Heliocentric Span: {extremes['r_min_au']} AU -> {extremes['r_max_au']} AU (Ratio: {extremes['distance_ratio']}x)")
    print(f"Solar Flux Ratio: {extremes['solar_flux_ratio']}x")
    print(f"Light-Time Span: {extremes['light_time_min_sec']}s -> {extremes['light_time_max_hours']}h (Ratio: {extremes['light_time_ratio']}x)")
    print(f"Speed Span Ratio: {extremes['speed_ratio']}x")
    print(f"Thermal Span: {extremes['thermal_span_k']} K")
    print(f"Agencies: {extremes['agency_breakdown']}")
    print("=" * 70)
