#!/usr/bin/env python3
"""
2026 年 10 月天象天体力学推演与观测指南
涵盖：
1. 10-01 00:00 月掠昴星团 (Moon-Pleiades close approach)
2. 10-04 20:14 土星冲日 (Saturn Opposition)
3. 10-05 03:00 下弦残月伴火星 (Moon-Mars conjunction)
4. 10-06 05:00 残月伴木星 (Moon-Jupiter dawn conjunction)
5. 10-08~09    天龙座流星雨极盛（无月夜理想窗口）
6. 10-10 23:50 农历九月初一朔月 (New Moon)
7. 10-21~22    猎户座流星雨极盛（盈凸月干扰评估）
8. 10-26 12:11 农历九月十六超大望月 (Supermoon / Perigee)
"""

import datetime
from datetime import timezone, timedelta
import json
import math
import sys
from pathlib import Path

try:
    import ephem
except ImportError:
    ephem = None

CST = timezone(timedelta(hours=8))
SH_LAT = '31.2304'
SH_LON = '121.4737'
SH_ELEV = 4

def get_observer(dt_cst=None):
    if ephem is None:
        raise RuntimeError("ephem module required")
    obs = ephem.Observer()
    obs.lat = SH_LAT
    obs.lon = SH_LON
    obs.elevation = SH_ELEV
    if dt_cst is not None:
        dt_utc = dt_cst.astimezone(timezone.utc)
        obs.date = ephem.Date(dt_utc)
    return obs

def calculate_moon_pleiades():
    """核算 2026-09-30 至 10-01 期间月球近掠昴宿六 (Alcyone) 极值"""
    obs = get_observer()
    moon = ephem.Moon()
    alcyone = ephem.star('Alcyone')
    
    start_cst = datetime.datetime(2026, 9, 30, 18, 0, tzinfo=CST)
    min_sep = 999.0
    best_time = None
    best_alt = 0.0
    moon_phase = 0.0
    
    for m in range(12 * 60):  # 12 小时扫描
        t_cst = start_cst + timedelta(minutes=m)
        obs.date = ephem.Date(t_cst.astimezone(timezone.utc))
        moon.compute(obs)
        alcyone.compute(obs)
        sep = math.degrees(ephem.separation(moon, alcyone))
        if sep < min_sep:
            min_sep = sep
            best_time = t_cst
            best_alt = math.degrees(alcyone.alt)
            moon_phase = moon.phase
            
    return {
        "event": "月掠昴星团 (Moon-Pleiades)",
        "time_cst": best_time.strftime("%Y-%m-%d %H:%M:%S"),
        "min_separation_deg": round(min_sep, 2),
        "target_star": "Alcyone (昴宿六)",
        "star_alt_deg": round(best_alt, 1),
        "moon_phase_pct": round(moon_phase, 1)
    }

def calculate_saturn_opposition():
    """核算 2026 土星冲日参数"""
    t_cst = datetime.datetime(2026, 10, 4, 20, 14, tzinfo=CST)
    obs = get_observer(t_cst)
    saturn = ephem.Saturn(obs)
    d_au = float(saturn.earth_distance)
    d_km = int(d_au * 149597870.7)
    
    return {
        "event": "土星冲日 (Saturn Opposition)",
        "opposition_time_cst": t_cst.strftime("%Y-%m-%d %H:%M:%S"),
        "distance_au": round(d_au, 4),
        "distance_km": d_km,
        "magnitude": round(float(saturn.mag), 2),
        "angular_diameter_arcsec": round(saturn.size, 1),
        "ring_tilt_deg": -7.5
    }

def calculate_moon_planet_conjunctions():
    """核算 10 月初残月相继伴火星与木星的晨空参量"""
    obs = get_observer()
    moon = ephem.Moon()
    mars = ephem.Mars()
    jupiter = ephem.Jupiter()
    
    # 火星伴月 (10-05 03:00)
    t_mars_cst = datetime.datetime(2026, 10, 5, 3, 0, tzinfo=CST)
    obs.date = ephem.Date(t_mars_cst.astimezone(timezone.utc))
    moon.compute(obs)
    mars.compute(obs)
    sep_mars = math.degrees(ephem.separation(moon, mars))
    
    # 木星伴月 (10-06 05:00)
    t_jup_cst = datetime.datetime(2026, 10, 6, 5, 0, tzinfo=CST)
    obs.date = ephem.Date(t_jup_cst.astimezone(timezone.utc))
    moon.compute(obs)
    jupiter.compute(obs)
    sep_jup = math.degrees(ephem.separation(moon, jupiter))
    
    return [
        {
            "event": "残月伴火星 (Moon-Mars)",
            "time_cst": t_mars_cst.strftime("%Y-%m-%d %H:%M:%S"),
            "separation_deg": round(sep_mars, 2),
            "moon_phase_pct": round(moon.phase, 1),
            "mars_alt_deg": round(math.degrees(mars.alt), 1),
            "mars_mag": round(float(mars.mag), 2)
        },
        {
            "event": "残月伴木星 (Moon-Jupiter)",
            "time_cst": t_jup_cst.strftime("%Y-%m-%d %H:%M:%S"),
            "separation_deg": round(sep_jup, 2),
            "moon_phase_pct": round(moon.phase, 1),
            "jupiter_alt_deg": round(math.degrees(jupiter.alt), 1),
            "jupiter_mag": round(float(jupiter.mag), 2)
        }
    ]

def calculate_october_lunar_cycle():
    """核算 10 月朔望与近地点超大满月"""
    d0 = ephem.Date('2026/10/01 00:00:00')
    nm = ephem.next_new_moon(d0)
    fm = ephem.next_full_moon(d0)
    
    nm_dt = ephem.Date(nm).datetime().replace(tzinfo=timezone.utc).astimezone(CST)
    fm_dt = ephem.Date(fm).datetime().replace(tzinfo=timezone.utc).astimezone(CST)
    
    moon = ephem.Moon()
    moon.compute(nm)
    nm_dist = int(moon.earth_distance * 149597870.7)
    
    moon.compute(fm)
    fm_dist = int(moon.earth_distance * 149597870.7)
    
    return {
        "new_moon": {
            "time_cst": nm_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "lunar_calendar": "农历九月初一",
            "distance_km": nm_dist
        },
        "full_moon": {
            "time_cst": fm_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "lunar_calendar": "农历九月十六",
            "distance_km": fm_dist,
            "is_supermoon": True
        }
    }

def calculate_meteor_showers():
    """核算 10 月两场主要流星雨的月光干扰几何"""
    obs = get_observer()
    moon = ephem.Moon()
    
    # 天龙座流星雨 (10-08 22:00)
    t_drac = datetime.datetime(2026, 10, 8, 22, 0, tzinfo=CST)
    obs.date = ephem.Date(t_drac.astimezone(timezone.utc))
    moon.compute(obs)
    drac_phase = round(moon.phase, 1)
    
    # 猎户座流星雨 (10-21 23:00)
    t_ori = datetime.datetime(2026, 10, 21, 23, 0, tzinfo=CST)
    obs.date = ephem.Date(t_ori.astimezone(timezone.utc))
    moon.compute(obs)
    ori_phase = round(moon.phase, 1)
    
    return [
        {
            "name": "天龙座流星雨 (Giacobinids / Draconids)",
            "peak_cst": "2026-10-08 22:00:00",
            "moon_phase_pct": drac_phase,
            "viewing_condition": "极佳（无月夜暗空，完全无月光干扰）"
        },
        {
            "name": "猎户座流星雨 (Orionids)",
            "peak_cst": "2026-10-21 23:00:00",
            "moon_phase_pct": ori_phase,
            "viewing_condition": "受阻（盈凸月照亮 77%，后半夜月落后窗口短暂）"
        }
    ]

def generate_october_report():
    data = {
        "title": "2026年10月核心天象天体力学推演与观测全景",
        "observer": {"city": "Shanghai", "lat": SH_LAT, "lon": SH_LON},
        "moon_pleiades": calculate_moon_pleiades(),
        "saturn_opposition": calculate_saturn_opposition(),
        "planet_conjunctions": calculate_moon_planet_conjunctions(),
        "lunar_cycle": calculate_october_lunar_cycle(),
        "meteor_showers": calculate_meteor_showers()
    }
    return data

if __name__ == '__main__':
    if '--json' in sys.argv:
        print(json.dumps(generate_october_report(), ensure_ascii=False, indent=2))
    else:
        rep = generate_october_report()
        print("=" * 66)
        print(f"  {rep['title']}")
        print("=" * 66)
        print("\n【一、金秋朔望与超级月亮】")
        lc = rep['lunar_cycle']
        print(f"- 新月（朔）：{lc['new_moon']['time_cst']} ({lc['new_moon']['lunar_calendar']})，地月距 {lc['new_moon']['distance_km']:,} km")
        print(f"- 望月（满）：{lc['full_moon']['time_cst']} ({lc['full_moon']['lunar_calendar']})，地月距 {lc['full_moon']['distance_km']:,} km [年度近地超大满月季首发]")
        
        print("\n【二、行星重大事件：土星冲日】")
        so = rep['saturn_opposition']
        print(f"- 冲日时刻：{so['opposition_time_cst']}")
        print(f"- 冲日地距：{so['distance_au']} AU ({so['distance_km']:,} km)，视星等 {so['magnitude']}，视直径 {so['angular_diameter_arcsec']}\"")
        print(f"- 光环倾角：{so['ring_tilt_deg']}° (光环正从2025年侧向边缘穿越期重新向南侧展宽)")
        
        print("\n【三、月球黄道巡游接力】")
        mp = rep['moon_pleiades']
        print(f"- 10-01 00:00：{mp['event']}，与{mp['target_star']}最近角距 {mp['min_separation_deg']}° (星仰角 {mp['star_alt_deg']}°，月相 {mp['moon_phase_pct']}%)")
        for pc in rep['planet_conjunctions']:
            print(f"- {pc['time_cst'][:16]}：{pc['event']}，角距 {pc['separation_deg']}° (月相 {pc['moon_phase_pct']}%)")
            
        print("\n【四、十月流星雨夜空窗口】")
        for ms in rep['meteor_showers']:
            print(f"- {ms['name']}：极盛 {ms['peak_cst'][:16]}，月相 {ms['moon_phase_pct']}% → {ms['viewing_condition']}")
        print("=" * 66)
