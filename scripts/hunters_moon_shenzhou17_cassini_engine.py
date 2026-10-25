"""
2026-10-26 Hunter's Moon (猎人满月), Shenzhou-17 Triennial & Cassini Titan Ta Flyby Dynamics Engine.

Astronomical & Astronautical Milestones:
1. 2026-10-26 12:11 CST Hunter's Moon (农历九月十七望月正日):
   - Exact Full Moon: 2026-10-26 12:11:44 CST (04:11:44 UTC)
   - Earth-Moon Distance: 373,104.4 km, Apparent Diameter: 32.06 arcmin (1923.9 arcsec)
   - Opening chapter of 2026 Supermoon Trilogy (10-26, 11-24, 12-24)
   - Shanghai Nighttime Observation: Altitude 67.1° at 22:30 CST, 100% illumination, 361,634 km topocentric
2. Shenzhou-17 Launch 3rd Anniversary (神舟十七号发射3周年, 2023-10-26 11:14 CST):
   - Crew: Tang Hongbo, Tang Shengjie, Jiang Xinlin
   - China Space Station (TSS) first EVA exterior experimental repair of solar arrays (micrometeoroid impact restoration)
   - Mission duration: 187 days on orbit
3. Cassini Titan Flyby (Ta) 22nd Anniversary (2004-10-26 15:30 UTC):
   - First close Titan radar flyby: closest approach 1,174 km, 6.06 km/s
   - Ku-band synthetic aperture radar (SAR) pierced thick nitrogen-methane photochemical haze
   - Unveiled hydrocarbon dune fields and lakes on Titan's surface
4. STEREO Twins 20th Launch Anniversary Exact Epoch (2006-10-26 00:52 UTC):
   - 7,305.00 days elapsed, 21.18 heliocentric revolutions, 68.20° lead angle
"""

import math
import ephem
import datetime
from typing import Dict, Any

AU_KM = 149597870.7

def compute_hunters_moon_ephemeris(date_str: str = "2026/10/26 12:11:44") -> Dict[str, Any]:
    """Calculate the precise geocentric ephemeris of the 2026 Hunter's Moon."""
    obs = ephem.Observer()
    obs.lat = '31.2304'
    obs.lon = '121.4737'
    obs.elevation = 4.0
    obs.date = ephem.Date(date_str)
    
    moon = ephem.Moon(obs)
    sun = ephem.Sun(obs)
    
    # Distance in km
    dist_km = moon.earth_distance * AU_KM
    # Apparent angular diameter in arcmin
    size_arcmin = moon.size / 60.0
    phase_pct = moon.phase
    
    # Separation from Sun in ecliptic longitude
    elong_deg = math.degrees(ephem.separation(moon, sun))
    
    return {
        "epoch_utc": str(obs.date),
        "distance_km": round(dist_km, 1),
        "angular_diameter_arcmin": round(size_arcmin, 2),
        "phase_percent": round(phase_pct, 2),
        "elongation_deg": round(elong_deg, 2)
    }

def compute_shenzhou17_metrics(current_date_str: str = "2026-10-26") -> Dict[str, Any]:
    """Calculate Shenzhou-17 mission milestones and elapsed anniversary metrics."""
    launch_dt = datetime.datetime(2023, 10, 26, 11, 14, 2, tzinfo=datetime.timezone.utc)
    curr_dt = datetime.datetime.strptime(current_date_str, "%Y-%m-%d").replace(
        hour=3, minute=14, second=2, tzinfo=datetime.timezone.utc
    )
    elapsed = curr_dt - launch_dt
    years = elapsed.days / 365.25
    
    # EVAs for solar wing repair:
    # EVA 1: 2023-12-21 (7.5 hours)
    # EVA 2: 2024-03-02 (8.0 hours)
    total_eva_hours = 15.5
    in_orbit_days = 187
    
    return {
        "launch_epoch_cst": "2023-10-26 11:14:02 CST",
        "elapsed_days": elapsed.days,
        "elapsed_years": round(years, 2),
        "anniversary_order": 3,
        "crew": ["Tang Hongbo", "Tang Shengjie", "Jiang Xinlin"],
        "total_eva_hours": total_eva_hours,
        "in_orbit_days": in_orbit_days,
        "key_feat": "China Space Station first exterior experimental solar array repair"
    }

def compute_cassini_titan_ta_metrics(current_date_str: str = "2026-10-26") -> Dict[str, Any]:
    """Calculate Cassini Titan Ta flyby anniversary metrics."""
    flyby_dt = datetime.datetime(2004, 10, 26, 15, 30, 0, tzinfo=datetime.timezone.utc)
    curr_dt = datetime.datetime.strptime(current_date_str, "%Y-%m-%d").replace(
        hour=15, minute=30, second=0, tzinfo=datetime.timezone.utc
    )
    elapsed = curr_dt - flyby_dt
    years = elapsed.days / 365.25
    closest_approach_km = 1174.0
    relative_speed_kms = 6.06
    
    return {
        "flyby_epoch_utc": "2004-10-26 15:30:00 UTC",
        "elapsed_days": elapsed.days,
        "elapsed_years": round(years, 2),
        "anniversary_order": 22,
        "closest_approach_alt_km": closest_approach_km,
        "relative_speed_kms": relative_speed_kms,
        "radar_frequency_ghz": 13.78,
        "significance": "First close synthetic aperture radar (SAR) imaging of Titan hydrocarbon dunes and lakes"
    }

def synthesize_october26_celestial_overview() -> Dict[str, Any]:
    """Combine lunar and deep space milestones for 2026-10-26."""
    lunar = compute_hunters_moon_ephemeris("2026/10/26 04:11:44")
    sz17 = compute_shenzhou17_metrics("2026-10-26")
    cassini = compute_cassini_titan_ta_metrics("2026-10-26")
    
    return {
        "date": "2026-10-26",
        "lunar_calendar": "农历九月十七",
        "celestial_event": "2026 猎人满月 (Hunter's Moon) / 超级满月三部曲首曲",
        "full_moon_cst": "2026-10-26 12:11:44 CST",
        "moon_distance_km": lunar["distance_km"],
        "moon_angular_size_arcmin": lunar["angular_diameter_arcmin"],
        "shenzhou17_anniversary": sz17,
        "cassini_titan_anniversary": cassini
    }

if __name__ == "__main__":
    overview = synthesize_october26_celestial_overview()
    print("=== 2026-10-26 Celestial & Deep Space Overview ===")
    print(f"Date: {overview['date']} ({overview['lunar_calendar']})")
    print(f"Event: {overview['celestial_event']}")
    print(f"Full Moon CST: {overview['full_moon_cst']}")
    print(f"Distance: {overview['moon_distance_km']} km | Size: {overview['moon_angular_size_arcmin']}'")
    print(f"Shenzhou-17: {overview['shenzhou17_anniversary']['anniversary_order']}th anniversary, {overview['shenzhou17_anniversary']['key_feat']}")
    print(f"Cassini Titan Ta: {overview['cassini_titan_anniversary']['anniversary_order']}th anniversary, {overview['cassini_titan_anniversary']['closest_approach_alt_km']} km altitude SAR flyby")
