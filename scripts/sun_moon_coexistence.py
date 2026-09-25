#!/usr/bin/env python3
"""
Calculate the exact astronomical geometry and celestial conditions
during the "日月同辉" (Sun and Moon simultaneously in the sky) on 2026 Mid-Autumn Festival.
"""

import ephem
import math
from datetime import datetime, timezone, timedelta

def analyze_coexistence(date_str="2026-09-25", lat="31.2304", lon="121.4737"):
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
    obs.horizon = '0' # reset
    
    # Duration of coexistence in minutes
    coexistence_duration_min = (ss_dt - mr_dt).total_seconds() / 60.0
    
    timeline = []
    # From 10 min before moonrise to 30 min after sunset
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
        "location": {"lat": lat, "lon": lon},
        "moonrise_cst": mr_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "sunset_cst": ss_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "civil_twilight_end_cst": tw_civil_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "coexistence_duration_minutes": round(coexistence_duration_min, 1),
        "timeline": timeline
    }

if __name__ == "__main__":
    data = analyze_coexistence()
    print(f"=== 2026 中秋日月同辉天象核算 ===")
    print(f"日期: {data['date']}")
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
