#!/usr/bin/env python3
"""verify_seasky_november.py — 对照 Sea and Sky 2026 年 11 月公开天文年历

数据来源：tests/data/astronomy_calendar_2026_seasky.json
外部锚点：
- 2026-11-09 07:03 UTC 朔月
- 2026-11-24 14:55 UTC 望月（超级月亮，年度近地点大满月）
- 2026-11-20 UTC 水星西大距 19.6°
- 2026-11-25 UTC 天王星冲日
"""

import json
import math
from datetime import datetime, timezone, timedelta
from pathlib import Path

try:
    import ephem
except ImportError:
    ephem = None

DATA_PATH = Path(__file__).resolve().parent.parent / "tests" / "data" / "astronomy_calendar_2026_seasky.json"


def check_november_events():
    if ephem is None:
        raise RuntimeError("ephem required")

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    events = data["events"]
    results = {}

    # 1. 朔月 (New Moon)
    d0 = ephem.Date("2026/11/01 00:00:00")
    nm = ephem.next_new_moon(d0)
    nm_utc = ephem.Date(nm).datetime().replace(tzinfo=timezone.utc)
    target_nm = datetime(2026, 11, 9, 7, 3, 0, tzinfo=timezone.utc)
    nm_diff_s = abs((nm_utc - target_nm).total_seconds())

    results["new_moon"] = {
        "ephem_utc": nm_utc.strftime("%Y-%m-%d %H:%M:%S"),
        "seasky_utc": "2026-11-09 07:03:00",
        "error_s": round(nm_diff_s, 1),
        "pass": nm_diff_s < 60.0
    }

    # 2. 望月与超级月亮 (Full Moon & Supermoon)
    fm = ephem.next_full_moon(d0)
    fm_utc = ephem.Date(fm).datetime().replace(tzinfo=timezone.utc)
    target_fm = datetime(2026, 11, 24, 14, 55, 0, tzinfo=timezone.utc)
    fm_diff_s = abs((fm_utc - target_fm).total_seconds())

    # 校验近地点距离与时间差
    obs = ephem.Observer()
    obs.lat, obs.lon = '0', '0'
    moon = ephem.Moon()
    start_p = datetime(2026, 11, 20, 0, 0, tzinfo=timezone.utc)
    min_dist_km = 9999999
    best_p_time = None
    for m in range(9 * 24 * 60):
        t = start_p + timedelta(minutes=m)
        obs.date = ephem.Date(t)
        moon.compute(obs)
        d_km = moon.earth_distance * 149597870.7
        if d_km < min_dist_km:
            min_dist_km = d_km
            best_p_time = t

    diff_hours = abs((best_p_time - fm_utc).total_seconds()) / 3600.0
    is_supermoon = (min_dist_km < 362000.0) and (diff_hours < 36.0)

    results["full_moon_supermoon"] = {
        "ephem_utc": fm_utc.strftime("%Y-%m-%d %H:%M:%S"),
        "seasky_utc": "2026-11-24 14:55:00",
        "error_s": round(fm_diff_s, 1),
        "perigee_distance_km": int(min_dist_km),
        "perigee_utc": best_p_time.strftime("%Y-%m-%d %H:%M:%S"),
        "perigee_fullmoon_diff_hours": round(diff_hours, 1),
        "is_supermoon_confirmed": is_supermoon,
        "pass": (fm_diff_s < 120.0) and is_supermoon
    }

    # 3. 水星西大距 (Mercury Greatest Western Elongation)
    sun = ephem.Sun()
    merc = ephem.Mercury()
    start_m = datetime(2026, 11, 15, 0, 0, tzinfo=timezone.utc)
    max_elong = 0.0
    best_m_time = None
    for m in range(10 * 24 * 60):
        t = start_m + timedelta(minutes=m)
        obs.date = ephem.Date(t)
        sun.compute(obs)
        merc.compute(obs)
        sep = math.degrees(ephem.separation(sun, merc))
        if sep > max_elong:
            max_elong = sep
            best_m_time = t

    elong_diff = abs(max_elong - events["mercury_greatest_western_elongation"]["elongation_deg"])
    results["mercury_elongation"] = {
        "ephem_max_elongation_deg": round(max_elong, 2),
        "seasky_elongation_deg": events["mercury_greatest_western_elongation"]["elongation_deg"],
        "elongation_diff_deg": round(elong_diff, 2),
        "peak_utc": best_m_time.strftime("%Y-%m-%d %H:%M:%S"),
        "peak_date_utc": best_m_time.strftime("%Y-%m-%d"),
        "seasky_date_utc": events["mercury_greatest_western_elongation"]["date_utc"],
        "pass": (elong_diff < 0.1) and (best_m_time.strftime("%Y-%m-%d") == "2026-11-20")
    }

    # 4. 天王星冲日 (Uranus Opposition)
    ura = ephem.Uranus()
    start_u = datetime(2026, 11, 24, 0, 0, tzinfo=timezone.utc)
    min_ura_diff = 999.0
    best_u_time = None
    for m in range(3 * 24 * 60):
        t = start_u + timedelta(minutes=m)
        obs.date = ephem.Date(t)
        sun.compute(obs)
        ura.compute(obs)
        sep = math.degrees(ephem.separation(sun, ura))
        d_180 = abs(180.0 - sep)
        if d_180 < min_ura_diff:
            min_ura_diff = d_180
            best_u_time = t

    results["uranus_opposition"] = {
        "opposition_peak_utc": best_u_time.strftime("%Y-%m-%d %H:%M:%S"),
        "opposition_date_utc": best_u_time.strftime("%Y-%m-%d"),
        "seasky_date_utc": events["uranus_opposition"]["date_utc"],
        "pass": best_u_time.strftime("%Y-%m-%d") == events["uranus_opposition"]["date_utc"]
    }

    return results


if __name__ == "__main__":
    r = check_november_events()
    print(json.dumps(r, indent=2, ensure_ascii=False))
