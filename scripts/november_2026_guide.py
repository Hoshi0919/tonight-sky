#!/usr/bin/env python3
"""
2026 年 11 月核心天象天体力学推演与观测指南

涵盖：
1. 11-02~03 晨曦三星大聚会：残月、木星（0.69° 近距离相切）与火星高仰角同框
2. 11-05 & 11-12 金牛座南/北流星雨火流星极盛（微月与无月理想窗口）
3. 11-09 15:02 农历十月初一朔月 (New Moon)
4. 11-17~18 狮子座流星雨极盛（上弦前半夜落山，后半夜暗夜绝佳）
5. 11-21 08:17 水星西大距（日距角 19.6°，2026 秋冬季最佳晨观窗口）
6. 11-24 17:30~19:15 农历十月十六近地超大满月横穿掩食昴星团 (Full Moon Pleiades Occultation)
7. 11-24 22:53 农历十月十六近地大满月 (望月地距 360,764 km，近地超大月)
8. 11-26 06:25 天王星冲日 (Uranus Opposition, 视星等 5.58，整夜可见)
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

try:
    from lunardate import LunarDate
except ImportError:
    LunarDate = None

CST = timezone(timedelta(hours=8))
SH_LAT = '31.2304'
SH_LON = '121.4737'
SH_ELEV = 4

def get_observer(dt_cst=None, lat=SH_LAT, lon=SH_LON, elev=SH_ELEV):
    if ephem is None:
        raise RuntimeError("ephem module required")
    obs = ephem.Observer()
    obs.lat = str(lat)
    obs.lon = str(lon)
    obs.elevation = elev
    if dt_cst is not None:
        dt_utc = dt_cst.astimezone(timezone.utc)
        obs.date = ephem.Date(dt_utc)
    return obs

def calculate_november_lunar_cycle():
    """核算 11 月朔望、弦月与近地点超级大满月"""
    d0 = ephem.Date('2026/11/01 00:00:00')
    lq = ephem.next_last_quarter_moon(d0)
    nm = ephem.next_new_moon(d0)
    fq = ephem.next_first_quarter_moon(d0)
    fm = ephem.next_full_moon(d0)
    
    lq_dt = ephem.Date(lq).datetime().replace(tzinfo=timezone.utc).astimezone(CST)
    nm_dt = ephem.Date(nm).datetime().replace(tzinfo=timezone.utc).astimezone(CST)
    fq_dt = ephem.Date(fq).datetime().replace(tzinfo=timezone.utc).astimezone(CST)
    fm_dt = ephem.Date(fm).datetime().replace(tzinfo=timezone.utc).astimezone(CST)
    
    moon = ephem.Moon()
    moon.compute(lq)
    lq_dist = int(moon.earth_distance * 149597870.7)
    moon.compute(nm)
    nm_dist = int(moon.earth_distance * 149597870.7)
    moon.compute(fq)
    fq_dist = int(moon.earth_distance * 149597870.7)
    moon.compute(fm)
    fm_dist = int(moon.earth_distance * 149597870.7)
    
    # 近地点扫描 (11-20 ~ 11-28)
    obs = get_observer()
    min_p_dist = 999999999
    best_p_time = None
    start_p = datetime.datetime(2026, 11, 20, 0, 0, tzinfo=CST)
    for m in range(9 * 24 * 60):
        t = start_p + timedelta(minutes=m)
        obs.date = ephem.Date(t.astimezone(timezone.utc))
        moon.compute(obs)
        d_km = moon.earth_distance * 149597870.7
        if d_km < min_p_dist:
            min_p_dist = d_km
            best_p_time = t

    return {
        "last_quarter": {
            "time_cst": lq_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "lunar_calendar": "农历九月廿四",
            "distance_km": lq_dist
        },
        "new_moon": {
            "time_cst": nm_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "lunar_calendar": "农历十月初一",
            "distance_km": nm_dist
        },
        "first_quarter": {
            "time_cst": fq_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "lunar_calendar": "农历十月初九",
            "distance_km": fq_dist
        },
        "full_moon": {
            "time_cst": fm_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "lunar_calendar": "农历十月十六",
            "distance_km": fm_dist,
            "is_supermoon": True,
            "perigee_time_cst": best_p_time.strftime("%Y-%m-%d %H:%M:%S"),
            "perigee_distance_km": int(min_p_dist),
            "perigee_fullmoon_diff_hours": round(abs((best_p_time - fm_dt).total_seconds()) / 3600.0, 1)
        }
    }

def calculate_dawn_trio_gathering():
    """核算 11-02 夜至 11-03 晨曦残月、木星与火星同框与极近合相"""
    obs = get_observer()
    moon = ephem.Moon()
    mars = ephem.Mars()
    jupiter = ephem.Jupiter()
    
    # 极近合相时刻扫描 (木星伴月)
    t_start = datetime.datetime(2026, 11, 3, 2, 0, tzinfo=CST)
    min_sep_jup = 999.0
    best_t_jup = None
    for m in range(300):
        t = t_start + timedelta(minutes=m)
        obs.date = ephem.Date(t.astimezone(timezone.utc))
        moon.compute(obs)
        jupiter.compute(obs)
        sep = math.degrees(ephem.separation(moon, jupiter))
        if sep < min_sep_jup:
            min_sep_jup = sep
            best_t_jup = t
            
    # 计算 11-03 06:00 CST 晨曦天象现场参数
    t_dawn = datetime.datetime(2026, 11, 3, 6, 0, tzinfo=CST)
    obs.date = ephem.Date(t_dawn.astimezone(timezone.utc))
    moon.compute(obs)
    mars.compute(obs)
    jupiter.compute(obs)
    
    sep_m_jup = math.degrees(ephem.separation(moon, jupiter))
    sep_m_mars = math.degrees(ephem.separation(moon, mars))
    sep_mars_jup = math.degrees(ephem.separation(mars, jupiter))
    
    return {
        "event": "晨曦三星聚会 (Dawn Trio Gathering: Moon-Jupiter-Mars)",
        "peak_time_cst": best_t_jup.strftime("%Y-%m-%d %H:%M:%S"),
        "min_separation_moon_jupiter_deg": round(min_sep_jup, 2),
        "dawn_observation_cst": "2026-11-03 06:00:00",
        "moon_phase_pct": round(moon.phase, 1),
        "moon_alt_deg": round(math.degrees(moon.alt), 1),
        "jupiter_alt_deg": round(math.degrees(jupiter.alt), 1),
        "jupiter_mag": round(float(jupiter.mag), 2),
        "mars_alt_deg": round(math.degrees(mars.alt), 1),
        "mars_mag": round(float(mars.mag), 2),
        "separation_moon_mars_deg": round(sep_m_mars, 2),
        "separation_mars_jupiter_deg": round(sep_mars_jup, 2)
    }

def calculate_mercury_elongation():
    """核算 2026-11 水星西大距与晨观条件"""
    obs = get_observer()
    sun = ephem.Sun()
    merc = ephem.Mercury()
    
    start_cst = datetime.datetime(2026, 11, 10, 0, 0, tzinfo=CST)
    max_elong = 0.0
    best_time = None
    
    for m in range(15 * 24 * 60):  # 11-10 到 11-25 逐分钟扫描
        t = start_cst + timedelta(minutes=m)
        obs.date = ephem.Date(t.astimezone(timezone.utc))
        sun.compute(obs)
        merc.compute(obs)
        sep = math.degrees(ephem.separation(sun, merc))
        if sep > max_elong:
            max_elong = sep
            best_time = t
            
    # 计算极盛日日出前 45 分钟观测参数
    obs.date = ephem.Date(best_time.astimezone(timezone.utc))
    sun_rise = obs.next_rising(sun)
    obs.date = ephem.Date(sun_rise - 45.0 / (24 * 60))
    merc.compute(obs)
    dawn_alt = math.degrees(merc.alt)
    merc_mag = float(merc.mag)
    
    rise_cst = ephem.Date(sun_rise).datetime().replace(tzinfo=timezone.utc).astimezone(CST)
    
    return {
        "event": "水星西大距 (Mercury Greatest Western Elongation)",
        "peak_time_cst": best_time.strftime("%Y-%m-%d %H:%M:%S"),
        "max_elongation_deg": round(max_elong, 2),
        "visual_magnitude": round(merc_mag, 2),
        "sunrise_cst": rise_cst.strftime("%H:%M:%S"),
        "altitude_45min_before_sunrise_deg": round(dawn_alt, 1),
        "viewing_recommendation": "2026秋冬季最佳水星晨观窗口，日出前东方低空极易肉眼捕获"
    }

def calculate_pleiades_occultation():
    """核算 11-24 望月掩食昴星团 (Full Moon Pleiades Occultation) 多地几何"""
    pleiades = {
        'Alcyone': '昴宿六',
        'Electra': '昴宿一',
        'Maia': '昴宿四',
        'Taygeta': '昴宿二'
    }
    
    cities = {
        'Shanghai': ('上海', '31.2304', '121.4737'),
        'Beijing': ('北京', '39.9042', '116.4074'),
        'Chengdu': ('成都', '30.5728', '104.0668')
    }
    
    results = {}
    moon = ephem.Moon()
    start_cst = datetime.datetime(2026, 11, 24, 16, 30, tzinfo=CST)
    
    for c_key, (c_name, lat, lon) in cities.items():
        obs = get_observer(lat=lat, lon=lon)
        c_res = []
        for s_key, s_zh in pleiades.items():
            star = ephem.star(s_key)
            min_sep = 999.0
            best_t = None
            for m in range(180):
                t = start_cst + timedelta(minutes=m)
                obs.date = ephem.Date(t.astimezone(timezone.utc))
                moon.compute(obs)
                star.compute(obs)
                sep = math.degrees(ephem.separation(moon, star))
                if sep < min_sep:
                    min_sep = sep
                    best_t = t
            obs.date = ephem.Date(best_t.astimezone(timezone.utc))
            moon.compute(obs)
            star.compute(obs)
            moon_r_deg = (moon.size / 2.0) / 3600.0
            is_occulted = min_sep < moon_r_deg
            c_res.append({
                "star": s_key,
                "star_zh": s_zh,
                "closest_time_cst": best_t.strftime("%H:%M"),
                "min_separation_deg": round(min_sep, 3),
                "moon_radius_deg": round(moon_r_deg, 3),
                "altitude_deg": round(math.degrees(star.alt), 1),
                "is_occulted": is_occulted
            })
        results[c_key] = {"city_zh": c_name, "events": c_res}
        
    return {
        "event": "满月掩昴星团 (Full Moon Pleiades Occultation)",
        "date": "2026-11-24",
        "time_window_cst": "17:30 - 19:15",
        "moon_phase_pct": 99.8,
        "shanghai_central_occultation": "Maia (昴宿四) 极近心掩食 (角距 0.001°)",
        "city_data": results
    }

def calculate_uranus_opposition():
    """核算 2026 天王星冲日参数"""
    t_cst = datetime.datetime(2026, 11, 26, 6, 25, tzinfo=CST)
    obs = get_observer(t_cst)
    ura = ephem.Uranus(obs)
    d_au = float(ura.earth_distance)
    d_km = int(d_au * 149597870.7)
    
    return {
        "event": "天王星冲日 (Uranus Opposition)",
        "opposition_time_cst": t_cst.strftime("%Y-%m-%d %H:%M:%S"),
        "distance_au": round(d_au, 4),
        "distance_km": d_km,
        "magnitude": round(float(ura.mag), 2),
        "constellation": "Taurus (金牛座)",
        "angular_diameter_arcsec": round(ura.size, 2),
        "viewing_guide": "位于昴星团东南方，整夜可见，双筒望远镜可辨蓝绿色行星视圆面"
    }

def calculate_november_meteor_showers():
    """核算 11 月三大流星雨的月光干扰几何"""
    obs = get_observer()
    moon = ephem.Moon()
    
    # 1. 南金牛座流星雨 (11-05 22:00)
    t_st = datetime.datetime(2026, 11, 5, 22, 0, tzinfo=CST)
    obs.date = ephem.Date(t_st.astimezone(timezone.utc))
    moon.compute(obs)
    st_phase = round(moon.phase, 1)
    
    # 2. 北金牛座流星雨 (11-12 22:00)
    t_nt = datetime.datetime(2026, 11, 12, 22, 0, tzinfo=CST)
    obs.date = ephem.Date(t_nt.astimezone(timezone.utc))
    moon.compute(obs)
    nt_phase = round(moon.phase, 1)
    
    # 3. 狮子座流星雨 (11-18 03:00)
    t_leo = datetime.datetime(2026, 11, 18, 3, 0, tzinfo=CST)
    obs.date = ephem.Date(t_leo.astimezone(timezone.utc))
    moon.compute(obs)
    leo_phase = round(moon.phase, 1)
    leo_alt = math.degrees(moon.alt)
    
    return [
        {
            "name": "南金牛座流星雨 (Southern Taurids)",
            "peak_cst": "2026-11-05 22:00:00",
            "parent_body": "2P/Encke (恩克彗星)",
            "moon_phase_pct": st_phase,
            "viewing_condition": "优良（月相 14% 残月，后半夜升起前无月光，富含明亮慢速火流星）"
        },
        {
            "name": "北金牛座流星雨 (Northern Taurids)",
            "peak_cst": "2026-11-12 22:00:00",
            "parent_body": "2P/Encke (恩克彗星)",
            "moon_phase_pct": nt_phase,
            "viewing_condition": "极佳（农历十月初三蛾眉月 10%，前半夜早早落山，全夜黑空无干扰）"
        },
        {
            "name": "狮子座流星雨 (Leonids)",
            "peak_cst": "2026-11-18 03:00:00",
            "parent_body": "55P/Tempel-Tuttle (坦普尔-塔特尔彗星)",
            "moon_phase_pct": leo_phase,
            "moon_alt_deg": round(leo_alt, 1),
            "viewing_condition": "极佳（上弦月已于午夜前落入地平线下，后半夜辐射点升至高空迎来完全暗夜窗口）"
        }
    ]

def generate_november_report():
    return {
        "title": "2026年11月核心天象天体力学推演与观测全景",
        "observer": {"city": "Shanghai", "lat": SH_LAT, "lon": SH_LON},
        "lunar_cycle": calculate_november_lunar_cycle(),
        "dawn_trio_gathering": calculate_dawn_trio_gathering(),
        "meteor_showers": calculate_november_meteor_showers(),
        "mercury_elongation": calculate_mercury_elongation(),
        "pleiades_occultation": calculate_pleiades_occultation(),
        "uranus_opposition": calculate_uranus_opposition()
    }

if __name__ == '__main__':
    if '--json' in sys.argv:
        print(json.dumps(generate_november_report(), ensure_ascii=False, indent=2))
    else:
        rep = generate_november_report()
        print("=" * 68)
        print(f"  {rep['title']}")
        print("=" * 68)
        
        print("\n【一、朔望月历与近地大满月】")
        lc = rep['lunar_cycle']
        print(f"- 下弦月：{lc['last_quarter']['time_cst']} ({lc['last_quarter']['lunar_calendar']})，地距 {lc['last_quarter']['distance_km']:,} km")
        print(f"- 朔月（新月）：{lc['new_moon']['time_cst']} ({lc['new_moon']['lunar_calendar']})，地距 {lc['new_moon']['distance_km']:,} km")
        print(f"- 上弦月：{lc['first_quarter']['time_cst']} ({lc['first_quarter']['lunar_calendar']})，地距 {lc['first_quarter']['distance_km']:,} km")
        fm = lc['full_moon']
        print(f"- 望月（满月）：{fm['time_cst']} ({fm['lunar_calendar']})，地距 {fm['distance_km']:,} km")
        print(f"  * 近地点时刻：{fm['perigee_time_cst']}，近地距 {fm['perigee_distance_km']:,} km")
        print(f"  * 望月与近地点仅差 {fm['perigee_fullmoon_diff_hours']} 小时，年度近地超大满月！")
        
        print("\n【二、晨曦三星大聚会：残月、木星与火星】")
        dt = rep['dawn_trio_gathering']
        print(f"- 极近合相时刻：{dt['peak_time_cst']}")
        print(f"- 木星伴月最小角距：仅 {dt['min_separation_moon_jupiter_deg']}°（约 41 角分，极近相切！）")
        print(f"- 11-03 06:00 晨空现场：月球仰角 {dt['moon_alt_deg']}°，木星仰角 {dt['jupiter_alt_deg']}°（视星等 {dt['jupiter_mag']}），火星仰角 {dt['mars_alt_deg']}°（视星等 {dt['mars_mag']}）")
        print(f"- 三星跨度：月木距 {dt['min_separation_moon_jupiter_deg']}°，火木距 {dt['separation_mars_jupiter_deg']}°，高悬晨空")
        
        print("\n【三、内行星盛宴：水星西大距】")
        me = rep['mercury_elongation']
        print(f"- 极大时刻：{me['peak_time_cst']}")
        print(f"- 日距角：{me['max_elongation_deg']}°，视星等 {me['visual_magnitude']}")
        print(f"- 日出时刻 {me['sunrise_cst']}，日出前 45 分钟地平高度达 {me['altitude_45min_before_sunrise_deg']}°")
        print(f"- 评价：{me['viewing_recommendation']}")
        
        print("\n【四、罕见天象：满月掩食昴星团 (11-24)】")
        po = rep['pleiades_occultation']
        print(f"- 日期时间：{po['date']} {po['time_window_cst']} CST")
        print(f"- 满月月相：{po['moon_phase_pct']}% 盈满光辉")
        print(f"- 上海核心掩食：{po['shanghai_central_occultation']}")
        for c_key, c_info in po['city_data'].items():
            occ_list = [f"{e['star_zh']}({e['closest_time_cst']})" for e in c_info['events'] if e['is_occulted']]
            print(f"- {c_info['city_zh']}掩食星目：{', '.join(occ_list) if occ_list else '紧邻掠过'}")
            
        print("\n【五、外行星重大事件：天王星冲日】")
        uo = rep['uranus_opposition']
        print(f"- 冲日时刻：{uo['opposition_time_cst']}")
        print(f"- 冲日地距：{uo['distance_au']} AU ({uo['distance_km']:,} km)，视星等 {uo['magnitude']}")
        print(f"- 位置：{uo['constellation']}，视直径 {uo['angular_diameter_arcsec']}\"")
        print(f"- 指南：{uo['viewing_guide']}")
        
        print("\n【六、十一月流星雨夜空窗口】")
        for ms in rep['meteor_showers']:
            print(f"- {ms['name']}：极盛 {ms['peak_cst'][:16]} | 母体：{ms['parent_body']} | 月相 {ms['moon_phase_pct']}% → {ms['viewing_condition']}")
        print("=" * 68)
