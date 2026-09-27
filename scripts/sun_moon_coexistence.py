#!/usr/bin/env python3
"""
Calculate the exact astronomical geometry and celestial conditions
during "日月同辉" (Sun and Moon simultaneously in the sky).

Supports both:
1. Evening coexistence (傍晚日月同辉: moonrise before sunset, e.g. Mid-Autumn 2026-09-25)
2. Morning coexistence (清晨日月同辉: sunrise before moonset, e.g. Post-Full Moon 2026-09-28)
"""

import ephem
import math
import sys
import json
import argparse
from datetime import datetime, timezone, timedelta

def analyze_evening_coexistence(date_str="2026-09-25", lat="31.2304", lon="121.4737"):
    cst = timezone(timedelta(hours=8))
    obs = ephem.Observer()
    obs.lat, obs.lon, obs.elevation = str(lat), str(lon), 5
    
    # Observer date at noon CST
    noon_cst = datetime.strptime(f"{date_str} 12:00:00", "%Y-%m-%d %H:%M:%S").replace(tzinfo=cst)
    obs.date = ephem.Date(noon_cst.astimezone(timezone.utc).strftime("%Y/%m/%d %H:%M:%S"))
    
    sun = ephem.Sun()
    moon = ephem.Moon()
    venus = ephem.Venus()
    saturn = ephem.Saturn()
    
    # Moonrise
    mr_ephem = obs.next_rising(moon)
    mr_dt = ephem.Date(mr_ephem).datetime().replace(tzinfo=timezone.utc).astimezone(cst)
    
    # Sunset
    ss_ephem = obs.next_setting(sun)
    ss_dt = ephem.Date(ss_ephem).datetime().replace(tzinfo=timezone.utc).astimezone(cst)
    
    # Civil twilight end (Sun alt = -6 deg)
    obs.horizon = '-6'
    tw_civil_end = obs.next_setting(sun, use_center=True)
    tw_civil_dt = ephem.Date(tw_civil_end).datetime().replace(tzinfo=timezone.utc).astimezone(cst)
    obs.horizon = '0'
    
    coexistence_duration_min = (ss_dt - mr_dt).total_seconds() / 60.0
    
    timeline = []
    start_t = mr_dt - timedelta(minutes=10)
    end_t = ss_dt + timedelta(minutes=30)
    
    curr = start_t
    while curr <= end_t:
        obs.date = ephem.Date(curr.astimezone(timezone.utc).strftime("%Y/%m/%d %H:%M:%S"))
        sun.compute(obs)
        moon.compute(obs)
        venus.compute(obs)
        saturn.compute(obs)
        
        sep_deg = math.degrees(ephem.separation(sun, moon))
        s_alt = math.degrees(sun.alt)
        s_az = math.degrees(sun.az)
        m_alt = math.degrees(moon.alt)
        m_az = math.degrees(moon.az)
        v_alt = math.degrees(venus.alt)
        v_az = math.degrees(venus.az)
        
        is_coexisting = (s_alt >= -0.26 and m_alt >= -0.26)
        
        timeline.append({
            "time_cst": curr.strftime("%H:%M:%S"),
            "sun_alt": round(s_alt, 2),
            "sun_az": round(s_az, 2),
            "moon_alt": round(m_alt, 2),
            "moon_az": round(m_az, 2),
            "moon_phase_pct": round(moon.moon_phase * 100, 2),
            "angular_separation_deg": round(sep_deg, 2),
            "venus_alt": round(v_alt, 2),
            "venus_az": round(v_az, 2),
            "saturn_alt": round(math.degrees(saturn.alt), 2),
            "is_coexisting": is_coexisting
        })
        curr += timedelta(minutes=5)
        
    return {
        "date": date_str,
        "mode": "evening",
        "location": {"lat": lat, "lon": lon},
        "moonrise_cst": mr_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "sunset_cst": ss_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "civil_twilight_end_cst": tw_civil_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "coexistence_duration_minutes": round(coexistence_duration_min, 1),
        "timeline": timeline
    }

def analyze_morning_coexistence(date_str="2026-09-28", lat="31.2304", lon="121.4737"):
    cst = timezone(timedelta(hours=8))
    obs = ephem.Observer()
    obs.lat, obs.lon, obs.elevation = str(lat), str(lon), 5
    
    # Morning base at 04:00 CST
    dt_base = datetime.strptime(f"{date_str} 04:00:00", "%Y-%m-%d %H:%M:%S").replace(tzinfo=cst)
    obs.date = ephem.Date(dt_base.astimezone(timezone.utc).strftime("%Y/%m/%d %H:%M:%S"))
    
    sun = ephem.Sun()
    moon = ephem.Moon()
    jupiter = ephem.Jupiter()
    saturn = ephem.Saturn()
    mars = ephem.Mars()
    
    # Sunrise
    sr_ephem = obs.next_rising(sun)
    sr_dt = ephem.Date(sr_ephem).datetime().replace(tzinfo=timezone.utc).astimezone(cst)
    
    # Moonset
    ms_ephem = obs.next_setting(moon)
    ms_dt = ephem.Date(ms_ephem).datetime().replace(tzinfo=timezone.utc).astimezone(cst)
    
    # Saturn set
    ss_ephem = obs.next_setting(saturn)
    ss_dt = ephem.Date(ss_ephem).datetime().replace(tzinfo=timezone.utc).astimezone(cst)
    
    # Civil dawn (Sun alt = -6 deg)
    obs.horizon = '-6'
    tw_dawn = obs.next_rising(sun, use_center=True)
    tw_dawn_dt = ephem.Date(tw_dawn).datetime().replace(tzinfo=timezone.utc).astimezone(cst)
    obs.horizon = '0'
    
    duration_min = (ms_dt - sr_dt).total_seconds() / 60.0
    
    # Find equilibrium point
    t = sr_dt
    step = timedelta(seconds=10)
    best_t = None
    min_diff = 999.0
    while t <= ms_dt:
        obs.date = ephem.Date(t.astimezone(timezone.utc).strftime("%Y/%m/%d %H:%M:%S"))
        sun.compute(obs)
        moon.compute(obs)
        diff = abs(sun.alt - moon.alt)
        if diff < min_diff:
            min_diff = diff
            best_t = t
        t += step
        
    obs.date = ephem.Date(best_t.astimezone(timezone.utc).strftime("%Y/%m/%d %H:%M:%S"))
    sun.compute(obs)
    moon.compute(obs)
    saturn.compute(obs)
    jupiter.compute(obs)
    mars.compute(obs)
    
    eq_info = {
        "time_cst": best_t.strftime("%H:%M:%S"),
        "sun_alt": round(math.degrees(sun.alt), 2),
        "sun_az": round(math.degrees(sun.az), 2),
        "moon_alt": round(math.degrees(moon.alt), 2),
        "moon_az": round(math.degrees(moon.az), 2),
        "moon_phase_pct": round(moon.moon_phase * 100, 2),
        "angular_separation_deg": round(math.degrees(ephem.separation(sun, moon)), 2),
        "saturn_alt": round(math.degrees(saturn.alt), 2),
        "jupiter_alt": round(math.degrees(jupiter.alt), 2),
        "mars_alt": round(math.degrees(mars.alt), 2),
    }
    
    # Timeline
    timeline = []
    start_t = sr_dt - timedelta(minutes=30)
    end_t = ms_dt + timedelta(minutes=10)
    curr = start_t
    while curr <= end_t:
        obs.date = ephem.Date(curr.astimezone(timezone.utc).strftime("%Y/%m/%d %H:%M:%S"))
        sun.compute(obs)
        moon.compute(obs)
        saturn.compute(obs)
        jupiter.compute(obs)
        mars.compute(obs)
        
        s_alt = math.degrees(sun.alt)
        m_alt = math.degrees(moon.alt)
        sat_alt = math.degrees(saturn.alt)
        jup_alt = math.degrees(jupiter.alt)
        m_phase = moon.moon_phase * 100
        sep = math.degrees(ephem.separation(sun, moon))
        is_co = (s_alt >= -0.26 and m_alt >= -0.26)
        
        timeline.append({
            "time_cst": curr.strftime("%H:%M:%S"),
            "sun_alt": round(s_alt, 2),
            "sun_az": round(math.degrees(sun.az), 2),
            "moon_alt": round(m_alt, 2),
            "moon_az": round(math.degrees(moon.az), 2),
            "moon_phase_pct": round(m_phase, 2),
            "angular_separation_deg": round(sep, 2),
            "saturn_alt": round(sat_alt, 2),
            "jupiter_alt": round(jup_alt, 2),
            "mars_alt": round(math.degrees(mars.alt), 2),
            "is_coexisting": is_co,
            "is_triple_coexisting": (is_co and sat_alt >= -0.26)
        })
        curr += timedelta(minutes=5)
        
    return {
        "date": date_str,
        "mode": "morning",
        "location": {"lat": lat, "lon": lon},
        "civil_dawn_cst": tw_dawn_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "sunrise_cst": sr_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "saturn_set_cst": ss_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "moonset_cst": ms_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "coexistence_duration_minutes": round(duration_min, 1),
        "equilibrium_point": eq_info,
        "timeline": timeline
    }

def analyze_coexistence(date_str="2026-09-25", lat="31.2304", lon="121.4737", mode="auto"):
    if mode == "evening":
        return analyze_evening_coexistence(date_str, lat, lon)
    elif mode == "morning":
        return analyze_morning_coexistence(date_str, lat, lon)
    elif mode == "auto":
        if date_str == "2026-09-25":
            return analyze_evening_coexistence(date_str, lat, lon)
        elif date_str == "2026-09-28":
            return analyze_morning_coexistence(date_str, lat, lon)
        else:
            eve = analyze_evening_coexistence(date_str, lat, lon)
            mor = analyze_morning_coexistence(date_str, lat, lon)
            if mor["coexistence_duration_minutes"] > eve["coexistence_duration_minutes"]:
                return mor
            return eve
    return analyze_evening_coexistence(date_str, lat, lon)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="日月同辉天象天体力学核算")
    parser.add_argument("--date", default="2026-09-28", help="核算日期 (YYYY-MM-DD)")
    parser.add_argument("--mode", choices=["auto", "evening", "morning"], default="auto", help="同辉模式")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出")
    args = parser.parse_args()
    
    data = analyze_coexistence(args.date, mode=args.mode)
    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
        sys.exit(0)
        
    mode_name = "清晨" if data.get("mode") == "morning" else "傍晚"
    print(f"=== {data['date']} {mode_name}日月同辉天象核算 ===")
    print(f"日期: {data['date']} ({mode_name})")
    if data.get("mode") == "morning":
        print(f"民用晨光始 (CST): {data['civil_dawn_cst']}")
        print(f"日出时刻 (CST): {data['sunrise_cst']}")
        print(f"土星西沉 (CST): {data['saturn_set_cst']}")
        print(f"月落时刻 (CST): {data['moonset_cst']}")
        print(f"日月同辉持续时间: {data['coexistence_duration_minutes']} 分钟")
        eq = data['equilibrium_point']
        print(f"地平天平平衡点 (CST): {eq['time_cst']} (日高 {eq['sun_alt']}°, 月高 {eq['moon_alt']}°, 角距 {eq['angular_separation_deg']}°)")
        print()
        print("时间 (CST) | 太阳高度/方位 | 月亮高度/方位 (照亮比) | 日月角距 | 土星高度 | 木星高度 | 同辉状态")
        print("-" * 92)
        for p in data["timeline"]:
            if p.get("is_triple_coexisting"):
                flag = "★ 日月土同辉"
            elif p.get("is_coexisting"):
                flag = "★ 日月同辉"
            else:
                flag = "  ——"
            print(f"{p['time_cst']}  | {p['sun_alt']:5.1f}°/{p['sun_az']:5.1f}° | {p['moon_alt']:5.1f}°/{p['moon_az']:5.1f}° ({p['moon_phase_pct']:4.1f}%) | {p['angular_separation_deg']:6.2f}° | {p['saturn_alt']:5.1f}° | {p['jupiter_alt']:5.1f}° | {flag}")
    else:
        print(f"月出时刻 (CST): {data['moonrise_cst']}")
        print(f"日落时刻 (CST): {data['sunset_cst']}")
        print(f"日月同辉持续时间: {data['coexistence_duration_minutes']} 分钟")
        print(f"民用昏影终时刻 (CST): {data['civil_twilight_end_cst']}")
        print()
        print("时间 (CST) | 太阳高度/方位 | 月亮高度/方位 (照亮比) | 日月角距 | 金星高度/方位 | 同辉状态")
        print("-" * 88)
        for p in data["timeline"]:
            flag = "★ 日月同辉" if p["is_coexisting"] else "  ——"
            print(f"{p['time_cst']}  | {p['sun_alt']:5.1f}°/{p['sun_az']:5.1f}° | {p['moon_alt']:5.1f}°/{p['moon_az']:5.1f}° ({p['moon_phase_pct']:4.1f}%) | {p['angular_separation_deg']:6.2f}° | {p['venus_alt']:5.1f}°/{p['venus_az']:5.1f}° | {flag}")
