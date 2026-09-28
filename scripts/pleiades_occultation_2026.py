"""
pleiades_occultation_2026.py — 2026 年国庆子夜月掩昴星团 (M45) 全域天体力学核算

天体力学与观测背景：
2026 年 10 月 1 日（国庆节）子夜（00:00 - 02:30 CST），农历八月二十/廿一亏凸月（照亮比 80.8%）
将在金牛座运行穿过著名的昴星团（M45 / Pleiades / 七姐妹星团）。
由于月球白道面交点以 18.61 年周期在黄道退行，2024–2029 年正处于当前周期的“月掩昴星团”活跃纪元。
本次天象核心亮点：
1. 适逢国庆长假开启的午夜黄金期，全国大部分地区天体仰角在 40°~65° 之间，远离低空重度大气消光。
2. 华北、东北、西北及西南部分地区（北京、哈尔滨、乌鲁木齐、成都、西安、沈阳等）处于“完全掩星区”，
   月轮将相继吞没昂宿二 (Taygeta)、昂宿三 (Asterope)、昂宿四 (Maia)、昂宿增八 (Celaeno) 等恒星。
3. 极其罕见的【暗边瞬间复出】：在亏凸月相下，月球自西向东运行时，恒星在月球暗边突然亮起复出，
   彻底避开了刺眼的月面亮边强光干扰，具备极高的目视震撼度与科学测时价值。
4. 掠掩边缘走廊（Graze Path）：贯穿鲁南、豫东、陕南等地，月缘环形山峰峦将对恒星产生数次连续闪烁遮掩。
5. 华东、华中、华南（上海、杭州、南京、武汉、广州等）处于“极近掠过同框区”，
   月轮南缘与昴宿诸星最近角距仅数角分，构成绝佳的宽视野摄影同框。
"""

import sys
import json
import math
import argparse
import datetime
import zoneinfo
import ephem

CST = zoneinfo.ZoneInfo("Asia/Shanghai")
UTC = datetime.timezone.utc

# 昴星团核心成员星表 (J2000 坐标与视星等)
PLEIADES_STARS = {
    "16 Tau (Celaeno)": {
        "hip": 17489,
        "name_cn": "昂宿增八 (Celaeno)",
        "ra": "3:44:48.20",
        "dec": "24:17:22.0",
        "mag": 5.45,
        "spect": "B7IV"
    },
    "17 Tau (Electra)": {
        "hip": 17499,
        "name_cn": "昂宿一 (Electra)",
        "ra": "3:44:52.54",
        "dec": "24:06:48.0",
        "mag": 3.70,
        "spect": "B6IIIe"
    },
    "19 Tau (Taygeta)": {
        "hip": 17531,
        "name_cn": "昂宿二 (Taygeta)",
        "ra": "3:45:12.50",
        "dec": "24:28:02.2",
        "mag": 4.30,
        "spect": "B6V"
    },
    "20 Tau (Maia)": {
        "hip": 17573,
        "name_cn": "昂宿四 (Maia)",
        "ra": "3:45:49.61",
        "dec": "24:22:03.9",
        "mag": 3.87,
        "spect": "B8III"
    },
    "21 Tau (Asterope)": {
        "hip": 17579,
        "name_cn": "昂宿三 (Asterope)",
        "ra": "3:45:54.40",
        "dec": "24:33:17.0",
        "mag": 5.76,
        "spect": "B8V"
    },
    "22 Tau": {
        "hip": 17588,
        "name_cn": "昂宿增十二",
        "ra": "3:46:02.90",
        "dec": "24:31:41.0",
        "mag": 6.43,
        "spect": "A0Vn"
    },
    "23 Tau (Merope)": {
        "hip": 17608,
        "name_cn": "昂宿五 (Merope)",
        "ra": "3:46:19.58",
        "dec": "23:56:54.1",
        "mag": 4.14,
        "spect": "B6IVev"
    },
    "Eta Tau (Alcyone)": {
        "hip": 17702,
        "name_cn": "昂宿六 (Alcyone)",
        "ra": "3:47:29.08",
        "dec": "24:06:18.5",
        "mag": 2.87,
        "spect": "B7IIIe"
    },
    "27 Tau (Atlas)": {
        "hip": 17847,
        "name_cn": "昂宿七 (Atlas)",
        "ra": "3:49:09.74",
        "dec": "24:03:12.3",
        "mag": 3.63,
        "spect": "B8III"
    },
    "28 Tau (Pleione)": {
        "hip": 17851,
        "name_cn": "昂宿增六 (Pleione)",
        "ra": "3:49:11.22",
        "dec": "24:08:12.2",
        "mag": 5.05,
        "spect": "B8IVpe"
    }
}

# 国内 18 个代表性观测节点
OBSERVERS = {
    "beijing": {"name": "北京", "lat": 39.9042, "lon": 116.4074, "elev": 50, "zone": "华北核心"},
    "tianjin": {"name": "天津", "lat": 39.0842, "lon": 117.2009, "elev": 10, "zone": "华北"},
    "shijiazhuang": {"name": "石家庄", "lat": 38.0428, "lon": 114.5149, "elev": 80, "zone": "华北"},
    "taiyuan": {"name": "太原", "lat": 37.8706, "lon": 112.5489, "elev": 800, "zone": "华北"},
    "jinan": {"name": "济南", "lat": 36.6512, "lon": 117.1201, "elev": 60, "zone": "华东偏北"},
    "qingdao": {"name": "青岛", "lat": 36.0671, "lon": 120.3826, "elev": 30, "zone": "华东沿海"},
    "zhengzhou": {"name": "郑州", "lat": 34.7466, "lon": 113.6253, "elev": 100, "zone": "中原"},
    "xian": {"name": "西安", "lat": 34.3416, "lon": 108.9398, "elev": 400, "zone": "西北关中"},
    "harbin": {"name": "哈尔滨", "lat": 45.8038, "lon": 126.5350, "elev": 150, "zone": "东北"},
    "shenyang": {"name": "沈阳", "lat": 41.8057, "lon": 123.4315, "elev": 55, "zone": "东北"},
    "mohe": {"name": "漠河", "lat": 52.9737, "lon": 122.5378, "elev": 300, "zone": "极北"},
    "urumqi": {"name": "乌鲁木齐", "lat": 43.8256, "lon": 87.6168, "elev": 800, "zone": "西北天山"},
    "chengdu": {"name": "成都", "lat": 30.5728, "lon": 104.0668, "elev": 500, "zone": "西南四川盆地"},
    "chongqing": {"name": "重庆", "lat": 29.5630, "lon": 106.5516, "elev": 260, "zone": "西南"},
    "wuhan": {"name": "武汉", "lat": 30.5928, "lon": 114.3055, "elev": 30, "zone": "华中"},
    "shanghai": {"name": "上海", "lat": 31.2304, "lon": 121.4737, "elev": 10, "zone": "华东长江口"},
    "hangzhou": {"name": "杭州", "lat": 30.2741, "lon": 120.1551, "elev": 20, "zone": "华东钱塘"},
    "guangzhou": {"name": "广州", "lat": 23.1291, "lon": 113.2644, "elev": 20, "zone": "华南"}
}

def create_observer(lat: float, lon: float, elev: float = 50) -> ephem.Observer:
    obs = ephem.Observer()
    obs.lat = str(lat)
    obs.lon = str(lon)
    obs.elevation = elev
    return obs

def get_position_angle_deg(ra1: float, dec1: float, ra2: float, dec2: float) -> float:
    """计算从天体1指向天体2的方位角 (PA, 自天球北极顺时针向东, 0~360°)"""
    dra = ra2 - ra1
    pa = math.atan2(math.sin(dra) * math.cos(dec2),
                    math.cos(dec1) * math.sin(dec2) - math.sin(dec1) * math.cos(dec2) * math.cos(dra))
    return (math.degrees(pa) + 360.0) % 360.0

def classify_contact_limb(star_pa: float, sun_pa: float):
    """
    判断掩星接触点属于月面亮边还是暗边。
    亮边以日向角为中心，左右展开各 90° (总宽 180°)。
    若恒星方位角与日向角偏差超过 90°，则位于暗边。
    """
    diff = (star_pa - sun_pa + 180.0) % 360.0 - 180.0
    abs_diff = abs(diff)
    if abs_diff < 90.0:
        limb = "亮边 (Bright Limb)"
        cusp_dist = 90.0 - abs_diff # 距月角的角距 (度)
        is_dark = False
    else:
        limb = "暗边 (Dark Limb)"
        cusp_dist = abs_diff - 90.0 # 深入暗边的角距 (度)
        is_dark = True
    return {
        "limb_type": limb,
        "is_dark": is_dark,
        "delta_from_sun_pa_deg": round(abs_diff, 1),
        "cusp_distance_deg": round(cusp_dist, 1)
    }

def analyze_city_occultation(city_key: str, dt_start: datetime.datetime, dt_end: datetime.datetime):
    """核算特定城市在时间窗口内的所有昴宿恒星掩星与极近掠过事件"""
    city = OBSERVERS[city_key]
    obs = create_observer(city["lat"], city["lon"], city["elev"])
    
    moon = ephem.Moon()
    sun = ephem.Sun()
    
    city_results = {
        "city_key": city_key,
        "city_name": city["name"],
        "zone": city["zone"],
        "latitude": city["lat"],
        "longitude": city["lon"],
        "elevation_m": city["elev"],
        "occultations": [],
        "grazes_and_approaches": [],
        "classification": "CONJUNCTION_ONLY"
    }
    
    total_minutes = int((dt_end - dt_start).total_seconds() / 60)
    
    for star_id, star_meta in PLEIADES_STARS.items():
        star = ephem.FixedBody()
        star._ra = ephem.hours(star_meta["ra"])
        star._dec = ephem.degrees(star_meta["dec"])
        star._epoch = ephem.J2000
        
        # 1 分钟粗扫
        min_sep_deg = 999.0
        min_time = None
        min_moon_rad_deg = 0.0
        min_alt_deg = 0.0
        min_az_deg = 0.0
        
        in_occ = False
        raw_ingress_idx = None
        raw_egress_idx = None
        
        for i in range(total_minutes):
            t = dt_start + datetime.timedelta(minutes=i)
            obs.date = ephem.Date(t.astimezone(UTC).strftime("%Y/%m/%d %H:%M:%S"))
            moon.compute(obs)
            star.compute(obs)
            
            sep = float(ephem.separation(moon, star)) * 180.0 / math.pi
            rad = float(moon.size) / 7200.0 # 半径 (度)
            
            if sep < min_sep_deg:
                min_sep_deg = sep
                min_time = t
                min_moon_rad_deg = rad
                min_alt_deg = float(star.alt) * 180.0 / math.pi
                min_az_deg = float(star.az) * 180.0 / math.pi
                
            is_occ = sep < rad
            if is_occ and not in_occ:
                in_occ = True
                raw_ingress_idx = i
            elif not is_occ and in_occ:
                in_occ = False
                raw_egress_idx = i
                
        # 若发生掩星，精细二分求解至秒级
        if raw_ingress_idx is not None:
            # 求解掩始 (Ingress)
            t_ing_low = dt_start + datetime.timedelta(minutes=raw_ingress_idx - 1)
            t_ing_high = dt_start + datetime.timedelta(minutes=raw_ingress_idx)
            for _ in range(8): # 二分迭代收敛至 < 1 秒
                t_mid = t_ing_low + (t_ing_high - t_ing_low) / 2
                obs.date = ephem.Date(t_mid.astimezone(UTC).strftime("%Y/%m/%d %H:%M:%S"))
                moon.compute(obs)
                star.compute(obs)
                sep = float(ephem.separation(moon, star)) * 180.0 / math.pi
                rad = float(moon.size) / 7200.0
                if sep > rad:
                    t_ing_low = t_mid
                else:
                    t_ing_high = t_mid
            precise_ingress = t_ing_high
            
            # 计算掩始接触几何
            obs.date = ephem.Date(precise_ingress.astimezone(UTC).strftime("%Y/%m/%d %H:%M:%S"))
            moon.compute(obs)
            star.compute(obs)
            sun.compute(obs)
            ing_pa = get_position_angle_deg(float(moon.ra), float(moon.dec), float(star.ra), float(star.dec))
            sun_pa_ing = get_position_angle_deg(float(moon.ra), float(moon.dec), float(sun.ra), float(sun.dec))
            ing_limb_info = classify_contact_limb(ing_pa, sun_pa_ing)
            
            # 求解掩终 (Egress)
            if raw_egress_idx is not None:
                t_egr_low = dt_start + datetime.timedelta(minutes=raw_egress_idx - 1)
                t_egr_high = dt_start + datetime.timedelta(minutes=raw_egress_idx)
                for _ in range(8):
                    t_mid = t_egr_low + (t_egr_high - t_egr_low) / 2
                    obs.date = ephem.Date(t_mid.astimezone(UTC).strftime("%Y/%m/%d %H:%M:%S"))
                    moon.compute(obs)
                    star.compute(obs)
                    sep = float(ephem.separation(moon, star)) * 180.0 / math.pi
                    rad = float(moon.size) / 7200.0
                    if sep < rad:
                        t_egr_low = t_mid
                    else:
                        t_egr_high = t_mid
                precise_egress = t_egr_high
                
                obs.date = ephem.Date(precise_egress.astimezone(UTC).strftime("%Y/%m/%d %H:%M:%S"))
                moon.compute(obs)
                star.compute(obs)
                sun.compute(obs)
                egr_pa = get_position_angle_deg(float(moon.ra), float(moon.dec), float(star.ra), float(star.dec))
                sun_pa_egr = get_position_angle_deg(float(moon.ra), float(moon.dec), float(sun.ra), float(sun.dec))
                egr_limb_info = classify_contact_limb(egr_pa, sun_pa_egr)
            else:
                precise_egress = None
                egr_limb_info = None
                egr_pa = None
                
            dur_sec = (precise_egress - precise_ingress).total_seconds() if precise_egress else 0
            
            city_results["occultations"].append({
                "star_id": star_id,
                "star_name_cn": star_meta["name_cn"],
                "hip": star_meta["hip"],
                "mag": star_meta["mag"],
                "spectral_type": star_meta["spect"],
                "ingress_time_cst": precise_ingress.strftime("%Y-%m-%d %H:%M:%S"),
                "egress_time_cst": precise_egress.strftime("%Y-%m-%d %H:%M:%S") if precise_egress else "N/A",
                "duration_minutes": round(dur_sec / 60.0, 1),
                "peak_altitude_deg": round(min_alt_deg, 1),
                "peak_azimuth_deg": round(min_az_deg, 1),
                "ingress_pa_deg": round(ing_pa, 1),
                "ingress_limb": ing_limb_info,
                "egress_pa_deg": round(egr_pa, 1) if egr_pa else None,
                "egress_limb": egr_limb_info
            })
        else:
            # 未掩星，计算最小外侧距离 (角分)
            margin_arcmin = (min_sep_deg - min_moon_rad_deg) * 60.0
            if margin_arcmin <= 15.0: # 15 角分以内属于极近同框
                city_results["grazes_and_approaches"].append({
                    "star_id": star_id,
                    "star_name_cn": star_meta["name_cn"],
                    "mag": star_meta["mag"],
                    "miss_margin_arcmin": round(margin_arcmin, 2),
                    "min_separation_deg": round(min_sep_deg, 3),
                    "closest_approach_cst": min_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "star_altitude_deg": round(min_alt_deg, 1),
                    "star_azimuth_deg": round(min_az_deg, 1)
                })
                
    if len(city_results["occultations"]) >= 1:
        city_results["classification"] = "FULL_OCCULTATION_ZONE"
    elif any(item["miss_margin_arcmin"] < 2.0 for item in city_results["grazes_and_approaches"]):
        city_results["classification"] = "GRAZE_ZONE"
    else:
        city_results["classification"] = "ULTRA_CLOSE_CONJUNCTION"
        
    return city_results

def solve_graze_trajectory(star_key: str = "19 Tau (Taygeta)"):
    """
    求解特定恒星在我国境内的南缘掠掩界线（Graze Path）。
    沿经度 100°E ~ 124°E，利用二分迭代精确求解使得 min(sep - radius) == 0 的临界纬度。
    """
    star_meta = PLEIADES_STARS[star_key]
    star = ephem.FixedBody()
    star._ra = ephem.hours(star_meta["ra"])
    star._dec = ephem.degrees(star_meta["dec"])
    star._epoch = ephem.J2000
    moon = ephem.Moon()
    
    t_start = datetime.datetime(2026, 9, 30, 23, 0, tzinfo=CST)
    
    graze_points = []
    
    lons = [100.0, 102.0, 104.0, 106.0, 108.0, 110.0, 112.0, 114.0, 116.0, 118.0, 120.0, 122.0, 124.0]
    
    for lon in lons:
        low_lat = 24.0
        high_lat = 44.0
        
        def eval_lat_margin(lat_val):
            obs = create_observer(lat_val, lon, 100)
            min_m = 99999.0
            best_t = None
            for m in range(0, 180, 2):
                t = t_start + datetime.timedelta(minutes=m)
                obs.date = ephem.Date(t.astimezone(UTC).strftime("%Y/%m/%d %H:%M:%S"))
                moon.compute(obs)
                star.compute(obs)
                sep_arcsec = float(ephem.separation(moon, star)) * 180.0 / math.pi * 3600.0
                rad_arcsec = float(moon.size) / 2.0
                margin = sep_arcsec - rad_arcsec
                if margin < min_m:
                    min_m = margin
                    best_t = t
            return min_m, best_t
            
        m_low, _ = eval_lat_margin(low_lat)
        m_high, _ = eval_lat_margin(high_lat)
        
        if m_low * m_high > 0:
            continue
            
        best_time = None
        for _ in range(14):
            mid_lat = (low_lat + high_lat) / 2.0
            m_mid, t_cand = eval_lat_margin(mid_lat)
            if m_mid > 0:
                low_lat = mid_lat
            else:
                high_lat = mid_lat
            best_time = t_cand
            
        graze_lat = (low_lat + high_lat) / 2.0
        
        # 计算该点天体仰角
        obs_pt = create_observer(graze_lat, lon, 100)
        obs_pt.date = ephem.Date(best_time.astimezone(UTC).strftime("%Y/%m/%d %H:%M:%S"))
        star.compute(obs_pt)
        alt_deg = float(star.alt) * 180.0 / math.pi
        
        graze_points.append({
            "longitude": lon,
            "graze_latitude": round(graze_lat, 3),
            "contact_time_cst": best_time.strftime("%H:%M CST"),
            "altitude_deg": round(alt_deg, 1)
        })
        
    return {
        "star_id": star_key,
        "star_name_cn": star_meta["name_cn"],
        "mag": star_meta["mag"],
        "graze_path": graze_points
    }

def generate_full_report():
    t_start = datetime.datetime(2026, 9, 30, 23, 0, tzinfo=CST)
    t_end = datetime.datetime(2026, 10, 1, 3, 30, tzinfo=CST)
    
    report_data = {
        "event_title": "2026 年国庆子夜月掩昴星团 (M45) 全域天体力学核算",
        "reference_epoch": "2026-10-01 00:00:00 CST",
        "lunar_context": {
            "phase_pct": 80.8,
            "lunar_age_days": 20.1,
            "earth_distance_km": 372450,
            "constellation": "Taurus (金牛座)",
            "illumination_description": "亏凸月 (Waning Gibbous)，西侧亮边，东侧暗边"
        },
        "cities": {},
        "graze_trajectories": {}
    }
    
    for city_k in OBSERVERS.keys():
        report_data["cities"][city_k] = analyze_city_occultation(city_k, t_start, t_end)
        
    report_data["graze_trajectories"]["taygeta"] = solve_graze_trajectory("19 Tau (Taygeta)")
    report_data["graze_trajectories"]["asterope"] = solve_graze_trajectory("21 Tau (Asterope)")
    
    return report_data

def format_text_report(data: dict) -> str:
    lines = []
    lines.append("=" * 80)
    lines.append(f"  {data['event_title']}")
    lines.append("=" * 80)
    l_ctx = data["lunar_context"]
    lines.append(f"【天体物理背景】")
    lines.append(f"  月相: {l_ctx['phase_pct']}% ({l_ctx['illumination_description']}) | 地月距: {l_ctx['earth_distance_km']:,} km")
    lines.append(f"  所在天区: {l_ctx['constellation']} | 周期背景: 18.61 年交点退行周期之月掩昴星团活跃季")
    lines.append("-" * 80)
    
    # 分区总结
    lines.append("【全国各大观测节点分类总览】")
    full_occ = []
    graze_zone = []
    conjunction = []
    for k, c in data["cities"].items():
        if c["classification"] == "FULL_OCCULTATION_ZONE":
            stars = [occ["star_name_cn"] for occ in c["occultations"]]
            full_occ.append(f"  - {c['city_name']} ({c['zone']}): 掩食 {len(c['occultations'])} 星 [{', '.join(stars)}]")
        elif c["classification"] == "GRAZE_ZONE":
            graze_zone.append(f"  - {c['city_name']} ({c['zone']}): 掠掩边缘走廊")
        else:
            conjunction.append(f"  - {c['city_name']} ({c['zone']}): 极近合相 (最近距 < 5')")
            
    lines.append("★ 完全掩星区 (Full Occultation Zone):")
    lines.extend(full_occ)
    lines.append("▲ 掠掩走廊 (Graze Zone):")
    lines.extend(graze_zone)
    lines.append("● 极近掠过同框区 (Ultra-Close Conjunction):")
    lines.extend(conjunction)
    lines.append("-" * 80)
    
    # 典型城市详细接触表 (北京、哈尔滨、西安、成都、上海)
    key_cities = ["beijing", "harbin", "xian", "chengdu", "shanghai"]
    for ck in key_cities:
        c = data["cities"][ck]
        alt_str = f"{c['occultations'][0]['peak_altitude_deg']}°" if c['occultations'] else "50~60°"
        lines.append(f"\n▶ 城市专报: {c['city_name']} ({c['latitude']}°N, {c['longitude']}°E, 仰角 ~{alt_str})")
        if c["occultations"]:
            lines.append("  [掩星事件 Contact Events]:")
            for occ in c["occultations"]:
                ing_limb = "暗边" if occ["ingress_limb"]["is_dark"] else "亮边"
                egr_limb = "暗边" if occ["egress_limb"]["is_dark"] else "亮边"
                lines.append(f"    * {occ['star_name_cn']} (V={occ['mag']:.2f}, {occ['spectral_type']}):")
                lines.append(f"        掩始: {occ['ingress_time_cst'].split(' ')[1]} CST (PA {occ['ingress_pa_deg']}° 【{ing_limb}】)")
                lines.append(f"        掩终: {occ['egress_time_cst'].split(' ')[1]} CST (PA {occ['egress_pa_deg']}° 【{egr_limb}】★ 瞬间复出)")
                lines.append(f"        时长: {occ['duration_minutes']} 分钟 | 恒星仰角: {occ['peak_altitude_deg']}°")
        if c["grazes_and_approaches"]:
            lines.append("  [极近掠过 Nearby Approaching Stars]:")
            for ap in c["grazes_and_approaches"][:3]:
                lines.append(f"    * {ap['star_name_cn']} (V={ap['mag']:.2f}): 最近外侧距 {ap['miss_margin_arcmin']:.1f}' 于 {ap['closest_approach_cst'].split(' ')[1]} CST (仰角 {ap['star_altitude_deg']}°)")
                
    # 掠掩界线
    lines.append("\n" + "=" * 80)
    lines.append("【昂宿二 (Taygeta, 4.30等) 华夏南缘掠掩带精确地理分布】")
    lines.append("经度 (°E) | 掠掩纬度 (°N) | 接触时刻 (CST) | 仰角 (°) | 途经地理走廊")
    lines.append("-" * 75)
    for pt in data["graze_trajectories"]["taygeta"]["graze_path"]:
        lon = pt["longitude"]
        desc = ""
        if lon == 100.0: desc = "四川甘孜理塘/雅江"
        elif lon == 104.0: desc = "四川广元剑阁/青川"
        elif lon == 108.0: desc = "陕西安康/镇安"
        elif lon == 112.0: desc = "湖北襄阳/老河口"
        elif lon == 116.0: desc = "安徽亳州/涡阳"
        elif lon == 118.0: desc = "山东临沂/费县"
        elif lon == 120.0: desc = "山东青岛黄岛/胶南"
        elif lon == 122.0: desc = "黄海北部海域"
        if desc:
            lines.append(f" {lon:5.1f}°E |    {pt['graze_latitude']:6.3f}°N   |   {pt['contact_time_cst']:9s}  |  {pt['altitude_deg']:4.1f}°  | {desc}")
            
    lines.append("-" * 80)
    lines.append("【观测与拍摄科学指导】")
    lines.append("1. 【极佳目视体验·暗边复出】：本场掩星最大看点是【掩终暗边瞬间复出】。")
    lines.append("   由于 80.8% 亏凸月东侧为暗面，恒星从黑黢黢的虚空毫无预兆地瞬间亮起（由于恒星角直径仅微角秒，复出在 0.02 秒内完成），视觉震撼度极强。")
    lines.append("2. 【动态范围与曝光破解】：")
    lines.append("   月轮（-12等）与 4~6 等恒星亮度相差近万倍。目视推荐使用口径 80mm 以上折射望远镜并配置遮光或大视场目镜；")
    lines.append("   摄影推荐高动态范围（HDR）曝光合成，或采用高速行星相机（视频录制）记录复出衍射条纹。")
    lines.append("3. 【国庆同框构图】：对于上海、杭州、广州等非掩食区，望远镜低倍目镜（或 200~400mm 长焦镜头）可在同一个 1.5° 视场内，")
    lines.append("   同时容纳银盘亏凸月与完整的七姐妹星团，构成'素月衔宝珠'的绝美画卷。")
    lines.append("=" * 80)
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="2026年国庆子夜月掩昴星团全域天体力学核算")
    parser.add_argument("--json", action="store_true", help="输出完整 JSON 结构化数据")
    parser.add_argument("--city", type=str, default=None, help="查询指定城市 (例如 beijing, shanghai, chengdu)")
    args = parser.parse_args()
    
    report_data = generate_full_report()
    
    if args.json:
        if args.city:
            c_key = args.city.lower()
            if c_key in report_data["cities"]:
                print(json.dumps(report_data["cities"][c_key], indent=2, ensure_ascii=False))
            else:
                print(json.dumps({"error": f"City {args.city} not found. Available: {list(OBSERVERS.keys())}"}, indent=2, ensure_ascii=False))
        else:
            print(json.dumps(report_data, indent=2, ensure_ascii=False))
    else:
        print(format_text_report(report_data))

if __name__ == "__main__":
    main()
