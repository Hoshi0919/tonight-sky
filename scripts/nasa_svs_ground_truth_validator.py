"""
nasa_svs_ground_truth_validator.py

Validates local astronomical calculations against official NASA Scientific
Visualization Studio (SVS) Dial-A-Moon 2026 ephemeris (ID: 5587).
8,760 hourly ground-truth data points covering Phase, Distance, Diameter,
Age, RA, Dec, Sub-solar coordinates, and Sub-earth libration.
"""

import json
import math
import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import ephem

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "nasa_svs_mooninfo_2026.json"
KM_PER_AU = 149597870.7
EARTH_RADIUS_M = 6378137.0


def load_nasa_svs_data() -> List[Dict[str, Any]]:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"NASA SVS data file not found: {DATA_PATH}")
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def create_geocentric_observer() -> ephem.Observer:
    obs = ephem.Observer()
    obs.lat = "0"
    obs.lon = "0"
    obs.elevation = -EARTH_RADIUS_M  # Earth center for geocentric comparison
    return obs


def evaluate_hourly(step: int = 1) -> Dict[str, Any]:
    """
    Evaluates PyEphem's geocentric Moon parameters against NASA SVS data.
    step: step size in hours (e.g. 1 for all 8760 hours, 24 for daily).
    """
    data = load_nasa_svs_data()
    sampled = data[::step]
    
    obs = create_geocentric_observer()
    moon = ephem.Moon()
    
    phase_diffs = []
    dist_diffs = []
    diam_diffs = []
    ra_diffs_arcmin = []
    dec_diffs_arcmin = []
    
    for entry in sampled:
        dt = datetime.datetime.strptime(entry["time"], "%d %b %Y %H:%M UT")
        obs.date = ephem.Date(dt)
        moon.compute(obs)
        
        # Phase (% illumination)
        p_err = abs(entry["phase"] - moon.phase)
        phase_diffs.append(p_err)
        
        # Distance (km)
        d_km = moon.earth_distance * KM_PER_AU
        d_err = abs(entry["distance"] - d_km)
        dist_diffs.append(d_err)
        
        # Diameter (arcsec)
        diam_err = abs(entry["diameter"] - moon.size)
        diam_diffs.append(diam_err)
        
        # Coordinates (RA in hours -> deg, Dec in deg)
        ephem_ra_deg = float(moon.g_ra) * 180.0 / math.pi
        nasa_ra_deg = entry["j2000"]["ra"] * 15.0
        ra_diff_deg = abs(ephem_ra_deg - nasa_ra_deg)
        if ra_diff_deg > 180.0:
            ra_diff_deg = 360.0 - ra_diff_deg
        ra_diffs_arcmin.append(ra_diff_deg * 60.0)
        
        ephem_dec_deg = float(moon.g_dec) * 180.0 / math.pi
        nasa_dec_deg = entry["j2000"]["dec"]
        dec_diffs_arcmin.append(abs(ephem_dec_deg - nasa_dec_deg) * 60.0)
        
    n = len(sampled)
    return {
        "n_samples": n,
        "step_hours": step,
        "phase": {
            "mean": sum(phase_diffs) / n,
            "max": max(phase_diffs),
            "median": sorted(phase_diffs)[n // 2],
        },
        "distance_km": {
            "mean": sum(dist_diffs) / n,
            "max": max(dist_diffs),
            "median": sorted(dist_diffs)[n // 2],
        },
        "diameter_arcsec": {
            "mean": sum(diam_diffs) / n,
            "max": max(diam_diffs),
            "median": sorted(diam_diffs)[n // 2],
        },
        "ra_arcmin": {
            "mean": sum(ra_diffs_arcmin) / n,
            "max": max(ra_diffs_arcmin),
            "median": sorted(ra_diffs_arcmin)[n // 2],
        },
        "dec_arcmin": {
            "mean": sum(dec_diffs_arcmin) / n,
            "max": max(dec_diffs_arcmin),
            "median": sorted(dec_diffs_arcmin)[n // 2],
        },
    }


def query_at_time(dt_utc: datetime.datetime) -> Dict[str, Any]:
    """Finds nearest NASA SVS hourly record and computes ephem values."""
    data = load_nasa_svs_data()
    # Format: '08 Nov 2026 14:00 UT'
    time_str = dt_utc.strftime("%d %b %Y %H:00 UT")
    match = next((x for x in data if x["time"] == time_str), None)
    if not match:
        raise ValueError(f"No NASA SVS record matching time: {time_str}")
        
    obs = create_geocentric_observer()
    obs.date = ephem.Date(dt_utc)
    moon = ephem.Moon(obs)
    
    return {
        "time_utc": dt_utc.isoformat(),
        "nasa": match,
        "ephem": {
            "phase": float(moon.phase),
            "distance_km": float(moon.earth_distance * KM_PER_AU),
            "diameter_arcsec": float(moon.size),
            "ra_hours": float(moon.g_ra) * 12.0 / math.pi,
            "dec_deg": float(moon.g_dec) * 180.0 / math.pi,
        },
        "discrepancy": {
            "phase_pct": abs(match["phase"] - moon.phase),
            "distance_km": abs(match["distance"] - moon.earth_distance * KM_PER_AU),
            "diameter_arcsec": abs(match["diameter"] - moon.size),
        }
    }


if __name__ == "__main__":
    import pprint
    print("Evaluating all 8,760 hours of 2026 against NASA SVS Ground Truth...")
    summary = evaluate_hourly(step=1)
    pprint.pprint(summary)
