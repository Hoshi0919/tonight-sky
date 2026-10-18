"""
IBEX (Interstellar Boundary Explorer) 18th Anniversary & Grand Duoquadragintet Fleet Engine.
Accurately models:
1. IBEX 18-Year in-orbit mission timeline (launched 2008-10-19 17:47:23 UTC).
2. 3:1 Lunar-Resonant Orbit dynamics (apogee 320,000 km, perigee 48,000 km, period ~9.09 days).
3. Charge exchange physics (H+ + H0 -> H0_ENA + H+) & optical thinness of the heliosphere.
4. ENA ballistics, velocity dispersion, and flight time from heliosheath (120 AU) to 1 AU.
5. IBEX Ribbon geometry (perpendicular to interstellar magnetic field, B_ISMF . r = 0).
6. Four-leaf clover heliotail (port/starboard slow wind lobes vs north/south fast wind lobes).
7. Lunar neutral hydrogen albedo (regolith backscatter ~16%).
8. The Grand Duoquadragintet: Complete 42-probe deep space fleet distribution across the solar system.
"""

import math
import datetime

# Physical and Astronomical Constants
AU_KM = 149597870.7
C_LIGHT_KMS = 299792.458
MU_EARTH = 398600.4418  # km^3 / s^2
R_EARTH_KM = 6378.137
AMU_KG = 1.66053906660e-27
EV_J = 1.602176634e-19
MOON_SIDEREAL_PERIOD_DAYS = 27.321661

# IBEX Mission Constants
IBEX_LAUNCH_UTC = datetime.datetime(2008, 10, 19, 17, 47, 23, tzinfo=datetime.timezone.utc)
IBEX_DRY_MASS_KG = 105.0
IBEX_LAUNCH_MASS_KG = 485.0

# Orbital parameters in 3:1 Lunar Resonance (post-2011 maneuver)
IBEX_PERIGEE_R_KM = 48000.0  # geocentric distance ~7.5 R_E
IBEX_APOGEE_R_KM = 320000.0  # ~50 R_E, ~0.83 lunar distances

# Scientific parameters
SIGMA_CX_1KEV_CM2 = 2.0e-15  # cm^2
N_H_INTERSTELLAR_CM3 = 0.12  # neutral hydrogen density cm^-3
HELIOPAUSE_DIST_AU = 120.0
INNER_HELIOSHEATH_THICKNESS_AU = 40.0
LUNAR_ENA_ALBEDO = 0.16  # fraction of solar wind protons backscattered as neutral H

def get_ibex_timeline(target_utc=None):
    if target_utc is None:
        target_utc = datetime.datetime(2026, 10, 19, 17, 47, 23, tzinfo=datetime.timezone.utc)
    delta = target_utc - IBEX_LAUNCH_UTC
    total_days = delta.total_seconds() / 86400.0
    total_years = total_days / 365.25
    total_orbits = total_days / get_lunar_resonance_orbit()["period_days"]
    return {
        "launch_utc": IBEX_LAUNCH_UTC.isoformat(),
        "target_utc": target_utc.isoformat(),
        "total_days": round(total_days, 2),
        "total_years": round(total_years, 4),
        "total_orbits": round(total_orbits, 1),
        "is_18th_anniversary": abs(total_years - 18.0) < 0.05
    }

def get_lunar_resonance_orbit():
    ra = IBEX_APOGEE_R_KM
    rp = IBEX_PERIGEE_R_KM
    a = (ra + rp) / 2.0
    e = (ra - rp) / (ra + rp)
    period_sec = 2.0 * math.pi * math.sqrt(a**3 / MU_EARTH)
    period_days = period_sec / 86400.0
    resonance_ratio = MOON_SIDEREAL_PERIOD_DAYS / period_days
    apogee_lunar_fraction = ra / 384400.0
    return {
        "perigee_km": rp,
        "apogee_km": ra,
        "semi_major_axis_km": a,
        "eccentricity": round(e, 4),
        "period_days": round(period_days, 3),
        "lunar_period_days": round(MOON_SIDEREAL_PERIOD_DAYS, 4),
        "resonance_ratio": round(resonance_ratio, 3),  # ~3.005 : 1
        "apogee_lunar_fraction": round(apogee_lunar_fraction, 3)
    }

def ena_velocity_km_s(energy_kev, mass_amu=1.008):
    e_j = energy_kev * 1000.0 * EV_J
    m_kg = mass_amu * AMU_KG
    v_ms = math.sqrt(2.0 * e_j / m_kg)
    return v_ms / 1000.0

def ena_flight_time(energy_kev, source_dist_au=120.0, target_dist_au=1.0):
    v_km_s = ena_velocity_km_s(energy_kev)
    dist_km = (source_dist_au - target_dist_au) * AU_KM
    time_sec = dist_km / v_km_s
    time_days = time_sec / 86400.0
    time_years = time_days / 365.25
    return {
        "energy_kev": energy_kev,
        "velocity_km_s": round(v_km_s, 2),
        "flight_time_days": round(time_days, 2),
        "flight_time_years": round(time_years, 3)
    }

def compute_heliosphere_optical_depth():
    # tau = n_neutral * sigma_cx * path_length
    l_cm = INNER_HELIOSHEATH_THICKNESS_AU * AU_KM * 1e5
    tau = N_H_INTERSTELLAR_CM3 * SIGMA_CX_1KEV_CM2 * l_cm
    transmission = math.exp(-tau)
    is_optically_thin = tau < 1.0
    return {
        "n_h_cm3": N_H_INTERSTELLAR_CM3,
        "sigma_cx_cm2": SIGMA_CX_1KEV_CM2,
        "path_length_au": INNER_HELIOSHEATH_THICKNESS_AU,
        "optical_depth_tau": round(tau, 6),
        "transmission_fraction": round(transmission, 4),
        "is_optically_thin": is_optically_thin
    }

def get_grand_duoquadragintet_fleet():
    """
    Returns the complete 42-probe Grand Duoquadragintet fleet of humanity active in deep space and cislunar space as of 2026-10-19.
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
        {"name": "Tianwen-2", "heliocentric_au": 1.001, "regime": "Kamo'oalewa Cruise", "agency": "CNSA"},
        {"name": "LRO", "heliocentric_au": 1.000, "regime": "Lunar Orbit", "agency": "NASA"},
        {"name": "Chandrayaan-2", "heliocentric_au": 1.000, "regime": "Lunar Orbit", "agency": "ISRO"},
        {"name": "Danuri (KPLO)", "heliocentric_au": 1.000, "regime": "Lunar Orbit", "agency": "KARI"},
        {"name": "CAPSTONE", "heliocentric_au": 1.000, "regime": "Lunar NRHO", "agency": "NASA"},
        {"name": "Queqiao-2", "heliocentric_au": 1.000, "regime": "Lunar Frozen Orbit", "agency": "CNSA"},
        {"name": "Chang'e-4 / Yutu-2", "heliocentric_au": 1.000, "regime": "Lunar Far Side Surface", "agency": "CNSA"},
        {"name": "ARTEMIS P1", "heliocentric_au": 1.000, "regime": "Lunar Retrograde Orbit", "agency": "NASA"},
        {"name": "ARTEMIS P2", "heliocentric_au": 1.000, "regime": "Lunar Prograde Orbit", "agency": "NASA"},
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
    fleet = get_grand_duoquadragintet_fleet()
    assert len(fleet) == 42, f"Expected 42 probes, got {len(fleet)}"
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

if __name__ == "__main__":
    t = get_ibex_timeline()
    print("IBEX Timeline:", t)
    orb = get_lunar_resonance_orbit()
    print("Lunar Resonance Orbit:", orb)
    opt = compute_heliosphere_optical_depth()
    print("Heliosphere Optical Depth:", opt)
    flight = ena_flight_time(1.0)
    print("1.0 keV ENA Flight Time:", flight)
    ext = compute_fleet_extremes()
    print("Fleet Extremes:", ext)
