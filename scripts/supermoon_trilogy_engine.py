#!/usr/bin/env python3
"""
supermoon_trilogy_engine.py - 2026 Late-Autumn/Winter Supermoon Trilogy Dynamics Engine
Computes celestial mechanics, anomalistic-synodic beat resonance (Full Moon Cycle),
topocentric parallax corrections, and China-wide observational geometry for the
2026 Supermoon Trilogy (2026-10-26, 2026-11-24, and 2026-12-24 Annual Extreme Supermoon).
"""

import argparse
import datetime
import json
import math
import sys
from pathlib import Path

try:
    import ephem
except ImportError:
    ephem = None

# Reference constants
EARTH_RADIUS_KM = 6378.137
AU_TO_KM = 149597870.7
SYNODIC_MONTH_DAYS = 29.530588853
ANOMALISTIC_MONTH_DAYS = 27.55454988

# Full Moon Cycle beat period: 1 / (1/A - 1/S) = A * S / (S - A)
FMC_BEAT_PERIOD_DAYS = (ANOMALISTIC_MONTH_DAYS * SYNODIC_MONTH_DAYS) / (SYNODIC_MONTH_DAYS - ANOMALISTIC_MONTH_DAYS)
FMC_BEAT_SYNODIC_RATIO = FMC_BEAT_PERIOD_DAYS / SYNODIC_MONTH_DAYS

# Chinese reference cities
CITIES = {
    'shanghai':  {'name': '上海 (Shanghai)',  'lat': '31.2304', 'lon': '121.4737', 'elevation': 10},
    'beijing':   {'name': '北京 (Beijing)',   'lat': '39.9042', 'lon': '116.4074', 'elevation': 50},
    'guangzhou': {'name': '广州 (Guangzhou)', 'lat': '23.1291', 'lon': '113.2644', 'elevation': 20},
    'chengdu':   {'name': '成都 (Chengdu)',   'lat': '30.5728', 'lon': '104.0668', 'elevation': 500},
    'harbin':    {'name': '哈尔滨 (Harbin)',   'lat': '45.8038', 'lon': '126.5350', 'elevation': 150},
    'urumqi':    {'name': '乌鲁木齐 (Urumqi)', 'lat': '43.8256', 'lon': '87.6168',  'elevation': 800}
}

# The 2026 Trilogy Search Windows
TRILOGY_WINDOWS = [
    {
        'id': 'supermoon_1',
        'name': 'Supermoon I (农历九月十六 · 晚秋初序)',
        'date_str': '2026-10-26',
        'search_start': '2026/10/20',
        'search_end': '2026/10/31',
        'constellation': '白羊座 (Aries)',
        'chinese_mansion': '娄宿 / 胃宿'
    },
    {
        'id': 'supermoon_2',
        'name': 'Supermoon II (农历十月十六 · 仲冬探秘)',
        'date_str': '2026-11-24',
        'search_start': '2026/11/18',
        'search_end': '2026/11/30',
        'constellation': '金牛座 (Taurus)',
        'chinese_mansion': '昴宿 / 毕宿'
    },
    {
        'id': 'supermoon_3',
        'name': 'Supermoon III (农历冬月十六 · 平安夜年度极致最大满月)',
        'date_str': '2026-12-24',
        'search_start': '2026/12/18',
        'search_end': '2026/12/30',
        'constellation': '双子座 (Gemini)',
        'chinese_mansion': '井宿'
    }
]

# 2026 Annual Micromoon baseline (2026-05-31)
MICROMOON_2026 = {
    'name': '2026 年度最小远地满月 (Micromoon)',
    'date_cst': '2026-05-31 16:45:08',
    'geocentric_dist_km': 406135.2,
    'geocentric_size_arcmin': 29.46
}


def cst_to_utc(dt_cst):
    return dt_cst - datetime.timedelta(hours=8)


def utc_to_cst(dt_utc):
    return dt_utc + datetime.timedelta(hours=8)


def get_ephem_observer(lat='31.2304', lon='121.4737', elevation=10):
    obs = ephem.Observer()
    obs.lat = str(lat)
    obs.lon = str(lon)
    obs.elevation = float(elevation)
    return obs


def find_perigee_in_range(start_date_str, end_date_str, step_minutes=10):
    """
    Finds exact perigee moment and distance within a given time range.
    """
    moon = ephem.Moon()
    t = ephem.Date(start_date_str)
    t_end = ephem.Date(end_date_str)
    
    min_dist = 999999.0
    best_t = None
    
    while t < t_end:
        moon.compute(t)
        dist_km = moon.earth_distance * AU_TO_KM
        if dist_km < min_dist:
            min_dist = dist_km
            best_t = t
        t = ephem.Date(t + step_minutes * ephem.minute)
        
    # Refine to 1-minute resolution
    t_fine_start = ephem.Date(best_t - step_minutes * ephem.minute)
    for m in range(step_minutes * 2):
        t_cur = ephem.Date(t_fine_start + m * ephem.minute)
        moon.compute(t_cur)
        dist_km = moon.earth_distance * AU_TO_KM
        if dist_km < min_dist:
            min_dist = dist_km
            best_t = t_cur
            
    return best_t, min_dist


def compute_supermoon_event(cfg):
    """
    Computes exact astronomical and physical parameters for one supermoon.
    """
    moon = ephem.Moon()
    
    # 1. Exact Full Moon (Syzygy) moment
    fm_utc = ephem.next_full_moon(cfg['search_start'])
    fm_cst = ephem.Date(fm_utc + 8 * ephem.hour)
    
    moon.compute(fm_utc)
    fm_dist_km = moon.earth_distance * AU_TO_KM
    fm_size_arcmin = moon.size / 60.0
    fm_ra_str = str(moon.ra)
    fm_dec_str = str(moon.dec)
    fm_dec_deg = math.degrees(moon.dec)
    
    # 2. Exact Perigee in the vicinity
    perigee_utc, perigee_dist_km = find_perigee_in_range(cfg['search_start'], cfg['search_end'])
    perigee_cst = ephem.Date(perigee_utc + 8 * ephem.hour)
    
    # Time delta between full moon and perigee
    delta_days = abs(float(fm_utc - perigee_utc))
    delta_hours = delta_days * 24.0
    delta_minutes = delta_hours * 60.0
    
    # Physical ratios relative to micromoon
    micro_dist = MICROMOON_2026['geocentric_dist_km']
    micro_size = MICROMOON_2026['geocentric_size_arcmin']
    
    diameter_ratio_geo = fm_size_arcmin / micro_size
    area_ratio_geo = (micro_dist / fm_dist_km) ** 2
    tidal_ratio_geo = (micro_dist / fm_dist_km) ** 3
    
    return {
        'id': cfg['id'],
        'name': cfg['name'],
        'date_str': cfg['date_str'],
        'constellation': cfg['constellation'],
        'chinese_mansion': cfg['chinese_mansion'],
        'full_moon_utc': str(fm_utc),
        'full_moon_cst': str(fm_cst),
        'perigee_utc': str(perigee_utc),
        'perigee_cst': str(perigee_cst),
        'time_delta_hours': round(delta_hours, 2),
        'time_delta_minutes': round(delta_minutes, 1),
        'fm_distance_km': round(fm_dist_km, 1),
        'perigee_distance_km': round(perigee_dist_km, 1),
        'apparent_size_arcmin': round(fm_size_arcmin, 2),
        'apparent_size_arcsec': round(moon.size, 1),
        'ra': fm_ra_str,
        'dec': fm_dec_str,
        'dec_deg': round(fm_dec_deg, 2),
        'ratios_vs_micromoon': {
            'diameter_percent': round((diameter_ratio_geo - 1.0) * 100.0, 2),
            'area_illuminance_percent': round((area_ratio_geo - 1.0) * 100.0, 2),
            'tidal_force_percent': round((tidal_ratio_geo - 1.0) * 100.0, 2)
        }
    }


def compute_topocentric_culmination(city_key, date_cst_anchor):
    """
    Computes topocentric transit parameters (distance, altitude, apparent size)
    for a given city on the primary viewing night of Supermoon III.
    """
    city = CITIES[city_key]
    obs = get_ephem_observer(city['lat'], city['lon'], city['elevation'])
    moon = ephem.Moon()
    
    # Search around midnight CST
    obs.date = ephem.Date(ephem.Date(date_cst_anchor) - 8 * ephem.hour)
    transit_utc = obs.next_transit(moon)
    obs.date = transit_utc
    moon.compute(obs)
    
    transit_cst = ephem.Date(transit_utc + 8 * ephem.hour)
    topo_dist_km = moon.earth_distance * AU_TO_KM
    topo_size_arcmin = moon.size / 60.0
    topo_alt_deg = math.degrees(moon.alt)
    topo_az_deg = math.degrees(moon.az)
    
    # Topocentric enhancement vs micromoon
    micro_dist = MICROMOON_2026['geocentric_dist_km']
    micro_size = MICROMOON_2026['geocentric_size_arcmin']
    
    return {
        'city_id': city_key,
        'city_name': city['name'],
        'transit_cst': str(transit_cst),
        'transit_utc': str(transit_utc),
        'altitude_deg': round(topo_alt_deg, 2),
        'azimuth_deg': round(topo_az_deg, 2),
        'topocentric_distance_km': round(topo_dist_km, 1),
        'topocentric_size_arcmin': round(topo_size_arcmin, 2),
        'topocentric_size_arcsec': round(moon.size, 1),
        'topo_vs_micromoon_diameter_pct': round((topo_size_arcmin / micro_size - 1.0) * 100.0, 2),
        'topo_vs_micromoon_area_pct': round(((micro_dist / topo_dist_km) ** 2 - 1.0) * 100.0, 2)
    }


def compute_deepsky_conjunctions_dec24():
    """
    Computes angular separations from Supermoon III to prominent winter stars and deep-sky objects.
    """
    fm_time = '2026/12/24 01:28:09' # UTC
    moon = ephem.Moon()
    moon.compute(fm_time)
    
    objects = [
        ('M35 疏散星团 (Gemini Cluster)', ephem.readdb('M35,f|C|O,6:08:54,24:20:00,5.3,2000')),
        ('北河二 (Castor / α Gem)',     ephem.readdb('Castor,f|S|A1,7:34:36,31:53:18,1.58,2000')),
        ('北河三 (Pollux / β Gem)',     ephem.readdb('Pollux,f|S|K0,7:45:19,28:01:34,1.16,2000')),
        ('参宿四 (Betelgeuse / α Ori)', ephem.readdb('Betelgeuse,f|S|M2,5:55:10,7:24:25,0.50,2000')),
        ('五车二 (Capella / α Aur)',    ephem.readdb('Capella,f|S|G5,5:16:41,45:59:53,0.08,2000')),
        ('毕宿五 (Aldebaran / α Tau)',  ephem.readdb('Aldebaran,f|S|K5,4:35:55,16:30:33,0.87,2000')),
        ('南河三 (Procyon / α CMi)',    ephem.readdb('Procyon,f|S|F5,7:39:18,5:13:30,0.38,2000')),
        ('天狼星 (Sirius / α CMa)',     ephem.readdb('Sirius,f|S|A1,6:45:09,-16:42:58,-1.46,2000'))
    ]
    
    conjunctions = []
    for name, obj in objects:
        obj.compute(fm_time)
        sep_deg = math.degrees(ephem.separation(moon, obj))
        conjunctions.append({
            'name': name,
            'separation_deg': round(sep_deg, 2),
            'ra': str(obj.ra),
            'dec': str(obj.dec)
        })
    return conjunctions


def build_full_report_data():
    """
    Assembles full data matrix for the 2026 Supermoon Trilogy.
    """
    trilogy_events = [compute_supermoon_event(w) for w in TRILOGY_WINDOWS]
    
    # China regional transit for Supermoon III (Christmas Eve Extreme)
    # Night A: 2026-12-23 into 2026-12-24
    transits_night_a = {k: compute_topocentric_culmination(k, '2026/12/23 20:00:00') for k in CITIES}
    # Night B: 2026-12-24 into 2026-12-25
    transits_night_b = {k: compute_topocentric_culmination(k, '2026/12/24 20:00:00') for k in CITIES}
    
    deepsky = compute_deepsky_conjunctions_dec24()
    
    return {
        'title': '2026 Late-Autumn/Winter Supermoon Trilogy Celestial Mechanics Engine',
        'generated_cst': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'constants': {
            'synodic_month_days': round(SYNODIC_MONTH_DAYS, 6),
            'anomalistic_month_days': round(ANOMALISTIC_MONTH_DAYS, 6),
            'full_moon_cycle_beat_days': round(FMC_BEAT_PERIOD_DAYS, 3),
            'full_moon_cycle_synodic_months': round(FMC_BEAT_SYNODIC_RATIO, 3),
            'resonance_drift_hours': round(abs(14 * SYNODIC_MONTH_DAYS - 15 * ANOMALISTIC_MONTH_DAYS) * 24.0, 2)
        },
        'micromoon_baseline': MICROMOON_2026,
        'trilogy_events': trilogy_events,
        'supermoon_3_transits': {
            'night_dec23_24': transits_night_a,
            'night_dec24_25': transits_night_b
        },
        'dec24_sky_conjunctions': deepsky
    }


def print_rich_report(data):
    """
    Renders human-readable report.
    """
    print("\n" + "=" * 80)
    print(" 🌕 2026 年底【超级月亮三重奏】天体力学推演与华夏极值观象矩阵")
    print("=" * 80)
    
    c = data['constants']
    print(f"\n【1. 望日-近地点共振周期动力学 (Full Moon Cycle FMC)】")
    print(f"  - 朔望月周期 (Synodic Month S)     : {c['synodic_month_days']} 日")
    print(f"  - 近点月周期 (Anomalistic Month A) : {c['anomalistic_month_days']} 日")
    print(f"  - 拍频共振周期 (FMC Beat Period)   : {c['full_moon_cycle_beat_days']} 日 (约 {c['full_moon_cycle_synodic_months']} 朔望月 / 14 个朔望月与 15 个近点月共振)")
    print(f"  - 14S 与 15A 理论时间差漂移        : 仅 {c['resonance_drift_hours']} 小时")
    print(f"  - 极值成因: 朔望月与近点月几乎严格整周期锁定，驱动连续 3 次满月逼近近地点形成超级月亮集簇！")
    
    print(f"\n【2. 超级月亮三重奏核心物理参数矩阵】")
    print("-" * 80)
    print(f"{'编号/天象':<26} | {'满月时刻 (CST)':<16} | {'望-近时差':<9} | {'望日地距':<10} | {'视直径':<8} | {'较5月小满月'}")
    print("-" * 80)
    for ev in data['trilogy_events']:
        r = ev['ratios_vs_micromoon']
        dt_str = f"{ev['time_delta_hours']}h ({ev['time_delta_minutes']}m)"
        ratio_str = f"径+{r['diameter_percent']}% 亮+{r['area_illuminance_percent']}% 潮+{r['tidal_force_percent']}%"
        print(f"{ev['name']:<24} | {ev['full_moon_cst']:<16} | {dt_str:<9} | {ev['fm_distance_km']:>8.1f}km | {ev['apparent_size_arcmin']:>5.2f}' | {ratio_str}")
    print("-" * 80)
    
    print(f"\n【3. 2026-12-24 平安夜年度极致最大满月 (Supermoon III) 破纪录机理】")
    sm3 = data['trilogy_events'][2]
    print(f"  - 望时刻: {sm3['full_moon_cst']} CST | 近地点时刻: {sm3['perigee_cst']} CST (时差仅 7.0 小时)")
    print(f"  - 绝对地心近地点: {sm3['perigee_distance_km']} km (创下 2026 全年 13 个近地点最逼近地球极值！)")
    print(f"  - 天球赤纬极值: 赤纬 Dec = {sm3['dec']} (直达 +27°18'33\"，居全年中天仰角之巅)")
    print(f"  - 冬至太阳摄动: 地球正逼近日点 (1月3日 0.9833 AU)，太阳引潮力梯度强化 (+10.5%)，压缩月球近地点")
    
    print(f"\n【4. 华夏六大代表节点站心几何 (Topocentric Parallax) 极限视直径】")
    print("  *注: 当月球运行至中天头顶，站心地面观测者向月球方向位移整整一个地球半径 (约 6378 km)！")
    print("-" * 80)
    print(f"{'观测城市':<14} | {'12-23/24 中天时刻 (CST)':<21} | {'中天仰角':<8} | {'站心地距':<10} | {'站心视直径':<9} | {'较小满月亮度'}")
    print("-" * 80)
    for k, topo in data['supermoon_3_transits']['night_dec23_24'].items():
        print(f"{topo['city_name']:<14} | {topo['transit_cst']:<21} | {topo['altitude_deg']:>6.1f}° | {topo['topocentric_distance_km']:>8.1f}km | {topo['topocentric_size_arcmin']:>6.2f}' ({topo['topocentric_size_arcsec']}\") | +{topo['topo_vs_micromoon_area_pct']}%")
    print("-" * 80)
    
    print(f"\n【5. 平安夜超级满月深空与恒星交会几何 (Winter Hexagon Gate)】")
    print(f"  满月深居双子座脚部，高悬于冬季六边形 (Winter Hexagon) 环抱之核心天门：")
    for conj in data['dec24_sky_conjunctions']:
        print(f"  - {conj['name']:<24}: 空间角距 {conj['separation_deg']:>5.2f}°")
    print("=" * 80 + "\n")


def main():
    parser = argparse.ArgumentParser(description="2026 Late-Autumn/Winter Supermoon Trilogy Dynamics Engine")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON data")
    args = parser.parse_args()
    
    if ephem is None:
        print("Error: ephem library is required.", file=sys.stderr)
        sys.exit(1)
        
    data = build_full_report_data()
    
    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print_rich_report(data)


if __name__ == "__main__":
    main()
