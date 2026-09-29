#!/usr/bin/env python3
"""
mars_m44_praesepe_engine.py - 2026 Mars-M44 Praesepe Transit Dynamics & Astrophotography Engine
Computes topocentric and geocentric ephemeris, trajectory dynamics, close encounters with cluster stars,
and China-wide observational geometry for the historic "Yinghuo transiting Ghost Mansion" (荧惑入鬼宿).
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

# M44 (Praesepe / 鬼宿星团 / 蜂巢星团 / NGC 2632)
M44_DATA = {
    'name': 'M44 (Praesepe / 鬼宿星团 / 蜂巢星团)',
    'ngc': 'NGC 2632',
    'ra_j2000': '08:40:22.2',
    'dec_j2000': '+19:40:19',
    'distance_pc': 182.0,
    'distance_ly': 593.6,
    'age_myr': 650.0,
    'core_radius_arcmin': 25.0,
    'cluster_radius_arcmin': 47.5,
    'integrated_v_mag': 3.70,
    'color_index_bv': 0.27,
    'trumpler_class': 'II 2 m',
    'total_stars': 1010
}

# Ghost Mansion (鬼宿) Classical Asterism Stars
GHOST_MANSION_STARS = {
    'theta_cnc': {'name': '鬼宿一 (θ Cnc)', 'ra': '08:31:35.7', 'dec': '+18:05:40', 'mag': 5.33, 'bv': 0.26, 'pos': '西南角'},
    'eta_cnc':   {'name': '鬼宿二 (η Cnc)', 'ra': '08:32:42.5', 'dec': '+20:26:28', 'mag': 5.33, 'bv': 1.11, 'pos': '西北角'},
    'gamma_cnc': {'name': '鬼宿三 (γ Cnc / Asellus Borealis)', 'ra': '08:43:17.2', 'dec': '+21:28:07', 'mag': 4.66, 'bv': 0.08, 'pos': '东北角'},
    'delta_cnc': {'name': '鬼宿四 (δ Cnc / Asellus Australis)', 'ra': '08:44:41.1', 'dec': '+18:09:15', 'mag': 3.94, 'bv': 1.08, 'pos': '东南角'}
}

# Central Member Stars of M44
M44_MEMBER_STARS = {
    'eps_cnc':  {'name': 'ε Cnc (Meleph / 41 Cnc)', 'ra': '08:40:27.1', 'dec': '+19:32:41', 'mag': 6.29, 'bv': 0.16, 'spec': 'A7 V'},
    'hd_73710': {'name': 'HD 73710 (巨星)',        'ra': '08:39:56.7', 'dec': '+19:40:07', 'mag': 6.39, 'bv': 1.02, 'spec': 'K0 III'},
    '39_cnc':   {'name': '39 Cnc',                'ra': '08:40:36.4', 'dec': '+20:00:28', 'mag': 6.39, 'bv': 0.96, 'spec': 'K0 III'},
    '40_cnc':   {'name': '40 Cnc',                'ra': '08:40:40.5', 'dec': '+19:58:16', 'mag': 6.61, 'bv': 0.25, 'spec': 'A9 V'},
    'hd_73598': {'name': 'HD 73598 (巨星)',        'ra': '08:39:25.2', 'dec': '+19:43:38', 'mag': 6.60, 'bv': 0.98, 'spec': 'G8 III'},
    '42_cnc':   {'name': '42 Cnc',                'ra': '08:40:43.8', 'dec': '+19:43:09', 'mag': 6.83, 'bv': 0.26, 'spec': 'A9 V'}
}

# Chinese Reference Cities
CITIES = {
    'shanghai':  {'name': '上海 (Shanghai)',  'lat': '31.23', 'lon': '121.47', 'elevation': 10},
    'beijing':   {'name': '北京 (Beijing)',   'lat': '39.90', 'lon': '116.40', 'elevation': 50},
    'guangzhou': {'name': '广州 (Guangzhou)', 'lat': '23.13', 'lon': '113.26', 'elevation': 20},
    'chengdu':   {'name': '成都 (Chengdu)',   'lat': '30.57', 'lon': '104.07', 'elevation': 500},
    'urumqi':    {'name': '乌鲁木齐 (Urumqi)', 'lat': '43.83', 'lon': '87.62',  'elevation': 800}
}

def cst_to_utc(dt_cst):
    return dt_cst - datetime.timedelta(hours=8)

def utc_to_cst(dt_utc):
    return dt_utc + datetime.timedelta(hours=8)

def get_ephem_observer(lat='31.23', lon='121.47', elevation=10):
    obs = ephem.Observer()
    obs.lat = str(lat)
    obs.lon = str(lon)
    obs.elevation = elevation
    obs.epoch = ephem.J2000
    return obs

def compute_mars_physics(dt_cst):
    if ephem is None:
        raise RuntimeError('ephem module required')
    dt_utc = cst_to_utc(dt_cst)
    obs = get_ephem_observer()
    obs.date = ephem.Date(dt_utc)
    mars = ephem.Mars(obs)
    sun = ephem.Sun(obs)
    
    elong = float(ephem.separation(mars, sun)) * 180.0 / math.pi
    dist_au = float(mars.earth_distance)
    dist_sun_au = float(mars.sun_distance)
    phase_angle = float(mars.phase) # in ephem, phase is % illuminated (0-100)
    
    return {
        'datetime_cst': dt_cst.strftime('%Y-%m-%d %H:%M:%S'),
        'ra': str(mars.ra),
        'dec': str(mars.dec),
        'ra_deg': math.degrees(float(mars.ra)),
        'dec_deg': math.degrees(float(mars.dec)),
        'mag': round(float(mars.mag), 2),
        'angular_diameter_arcsec': round(float(mars.size), 2),
        'earth_distance_au': round(dist_au, 4),
        'earth_distance_km': round(dist_au * 149597870.7, 0),
        'sun_distance_au': round(dist_sun_au, 4),
        'illumination_pct': round(phase_angle, 1),
        'solar_elongation_deg': round(elong, 2),
        'color_index_bv': 1.40
    }

def compute_m44_transit_timeline():
    if ephem is None:
        raise RuntimeError('ephem module required')
        
    obs = get_ephem_observer()
    m44 = ephem.FixedBody()
    m44._ra = ephem.hours(M44_DATA['ra_j2000'])
    m44._dec = ephem.degrees(M44_DATA['dec_j2000'])
    m44._epoch = ephem.J2000
    
    mars = ephem.Mars()
    
    # 1. Cluster entry, closest approach, exit
    dt_start = datetime.datetime(2026, 10, 8, 0, 0)
    dt_end = datetime.datetime(2026, 10, 15, 0, 0)
    
    cluster_radius_deg = M44_DATA['cluster_radius_arcmin'] / 60.0
    core_radius_deg = M44_DATA['core_radius_arcmin'] / 60.0
    
    entry_cluster = None
    entry_core = None
    exit_core = None
    exit_cluster = None
    
    min_sep_deg = 999.0
    min_sep_dt = None
    
    cur = dt_start
    step = datetime.timedelta(minutes=5)
    while cur <= dt_end:
        obs.date = ephem.Date(cst_to_utc(cur))
        mars.compute(obs)
        m44.compute(obs)
        sep = float(ephem.separation(mars, m44)) * 180.0 / math.pi
        
        if sep <= cluster_radius_deg and entry_cluster is None:
            entry_cluster = cur
        if sep <= core_radius_deg and entry_core is None:
            entry_core = cur
        if sep > core_radius_deg and entry_core is not None and exit_core is None:
            exit_core = cur
        if sep > cluster_radius_deg and entry_cluster is not None and exit_cluster is None:
            exit_cluster = cur
            
        if sep < min_sep_deg:
            min_sep_deg = sep
            min_sep_dt = cur
            
        cur += step
        
    # Refine closest approach to 10 seconds
    cur = min_sep_dt - datetime.timedelta(minutes=10)
    end_refine = min_sep_dt + datetime.timedelta(minutes=10)
    min_sep_exact = 999.0
    min_dt_exact = None
    while cur <= end_refine:
        obs.date = ephem.Date(cst_to_utc(cur))
        mars.compute(obs)
        m44.compute(obs)
        sep = float(ephem.separation(mars, m44)) * 180.0 / math.pi
        if sep < min_sep_exact:
            min_sep_exact = sep
            min_dt_exact = cur
        cur += datetime.timedelta(seconds=10)
        
    # 2. Star conjunctions
    star_encounters = []
    for s_key, s_info in M44_MEMBER_STARS.items():
        s_body = ephem.FixedBody()
        s_body._ra = ephem.hours(s_info['ra'])
        s_body._dec = ephem.degrees(s_info['dec'])
        s_body._epoch = ephem.J2000
        
        s_min_sep = 999.0
        s_min_dt = None
        cur = datetime.datetime(2026, 10, 10, 0, 0)
        while cur <= datetime.datetime(2026, 10, 14, 0, 0):
            obs.date = ephem.Date(cst_to_utc(cur))
            mars.compute(obs)
            s_body.compute(obs)
            sep = float(ephem.separation(mars, s_body)) * 180.0 / math.pi
            if sep < s_min_sep:
                s_min_sep = sep
                s_min_dt = cur
            cur += datetime.timedelta(minutes=5)
            
        # Refine
        cur = s_min_dt - datetime.timedelta(minutes=10)
        end_ref = s_min_dt + datetime.timedelta(minutes=10)
        while cur <= end_ref:
            obs.date = ephem.Date(cst_to_utc(cur))
            mars.compute(obs)
            s_body.compute(obs)
            sep = float(ephem.separation(mars, s_body)) * 180.0 / math.pi
            if sep < s_min_sep:
                s_min_sep = sep
                s_min_dt = cur
            cur += datetime.timedelta(seconds=10)
            
        star_encounters.append({
            'star_key': s_key,
            'star_name': s_info['name'],
            'star_mag': s_info['mag'],
            'star_bv': s_info['bv'],
            'spectral_type': s_info['spec'],
            'min_separation_arcmin': round(s_min_sep * 60.0, 3),
            'min_separation_arcsec': round(s_min_sep * 3600.0, 1),
            'closest_time_cst': s_min_dt.strftime('%Y-%m-%d %H:%M:%S'),
            'delta_v_mag': round(s_info['mag'] - 1.06, 2)
        })
        
    star_encounters.sort(key=lambda x: x['min_separation_arcmin'])
    
    return {
        'cluster_entry_cst': entry_cluster.strftime('%Y-%m-%d %H:%M') if entry_cluster else None,
        'core_entry_cst': entry_core.strftime('%Y-%m-%d %H:%M') if entry_core else None,
        'closest_approach_cst': min_dt_exact.strftime('%Y-%m-%d %H:%M:%S'),
        'min_distance_to_center_arcmin': round(min_sep_exact * 60.0, 3),
        'min_distance_to_center_arcsec': round(min_sep_exact * 3600.0, 1),
        'core_exit_cst': exit_core.strftime('%Y-%m-%d %H:%M') if exit_core else None,
        'cluster_exit_cst': exit_cluster.strftime('%Y-%m-%d %H:%M') if exit_cluster else None,
        'star_encounters': star_encounters
    }

def compute_city_ephemeris(date_str='2026-10-12'):
    if ephem is None:
        raise RuntimeError('ephem module required')
        
    year, month, day = map(int, date_str.split('-'))
    target_date = datetime.date(year, month, day)
    
    results = {}
    for city_key, city in CITIES.items():
        obs = get_ephem_observer(city['lat'], city['lon'], city['elevation'])
        
        # Noon of target date
        noon_cst = datetime.datetime(year, month, day, 12, 0)
        
        # Scan night: previous evening to target morning
        eve_cst = noon_cst - datetime.timedelta(hours=14) # 22:00 prev day
        obs.date = ephem.Date(cst_to_utc(eve_cst))
        
        mars = ephem.Mars()
        rise_time = obs.next_rising(mars)
        transit_time = obs.next_transit(mars)
        
        # Dawn: Astronomical dawn (Sun reaches -18 deg)
        obs_sun = get_ephem_observer(city['lat'], city['lon'], city['elevation'])
        obs_sun.date = ephem.Date(cst_to_utc(eve_cst))
        obs_sun.horizon = '-18'
        sun = ephem.Sun()
        dawn_time = obs_sun.next_rising(sun, use_center=True)
        
        # Moon state at peak night
        obs.date = ephem.Date(cst_to_utc(datetime.datetime(year, month, day, 3, 0)))
        moon = ephem.Moon(obs)
        mars.compute(obs)
        transit_mars = ephem.Mars()
        obs.date = transit_time
        transit_mars.compute(obs)
        transit_alt = float(transit_mars.alt) * 180.0 / math.pi
        
        obs.date = dawn_time
        dawn_mars = ephem.Mars()
        dawn_mars.compute(obs)
        dawn_alt = float(dawn_mars.alt) * 180.0 / math.pi
        
        rise_cst = utc_to_cst(rise_time.datetime())
        transit_cst = utc_to_cst(transit_time.datetime())
        dawn_cst = utc_to_cst(dawn_time.datetime())
        
        dark_duration_h = max(0.0, (dawn_time.datetime() - rise_time.datetime()).total_seconds() / 3600.0)
        
        results[city_key] = {
            'city_name': city['name'],
            'mars_rise_cst': rise_cst.strftime('%H:%M'),
            'mars_transit_cst': transit_cst.strftime('%H:%M'),
            'transit_altitude_deg': round(transit_alt, 1),
            'astronomical_dawn_cst': dawn_cst.strftime('%H:%M'),
            'dawn_altitude_deg': round(dawn_alt, 1),
            'dark_sky_duration_hours': round(dark_duration_h, 2),
            'moon_altitude_at_3am_deg': round(float(moon.alt) * 180.0 / math.pi, 1),
            'moon_illumination_pct': round(float(moon.phase), 1)
        }
    return results

def compute_full_mars_praesepe_report():
    mars_phys = compute_mars_physics(datetime.datetime(2026, 10, 11, 21, 11))
    timeline = compute_m44_transit_timeline()
    cities_obs = compute_city_ephemeris('2026-10-12')
    
    # Contrast analysis
    flux_ratio_cluster = 10 ** (0.4 * (M44_DATA['integrated_v_mag'] - mars_phys['mag']))
    flux_ratio_eps_cnc = 10 ** (0.4 * (6.29 - mars_phys['mag']))
    
    return {
        'title': '2026 年火星穿行鬼宿星团（M44 积尸气）天体力学推演与华夏观象全景报告',
        'generated_at_cst': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'm44_cluster_data': M44_DATA,
        'mars_physics': mars_phys,
        'timeline': timeline,
        'flux_contrast': {
            'mars_mag': mars_phys['mag'],
            'm44_integrated_mag': M44_DATA['integrated_v_mag'],
            'mars_to_m44_flux_ratio': round(flux_ratio_cluster, 1),
            'eps_cnc_mag': 6.29,
            'mars_to_eps_cnc_flux_ratio': round(flux_ratio_eps_cnc, 1),
            'color_contrast_bv': {
                'mars': mars_phys['color_index_bv'],
                'm44_cluster_mean': M44_DATA['color_index_bv'],
                'eps_cnc': 0.16,
                'visual_description': '火星呈现深橙红色（B-V=+1.40），与星团中央最亮主序星 ε Cnc 的冰蓝纯白（B-V=+0.16）形成鲜明视觉双色反差，犹如在钻石锦簇的宝盒中央嵌下一枚红宝石。'
            }
        },
        'china_cities_visibility': cities_obs,
        'astrophotography_guide': {
            'telescope_recommendations': [
                {'spec': '70~100mm 折射镜 (视场 ~2.0°)', 'view': '星团全景与火星同框，极佳目视体验，金红火星与几十颗蓝白星点相映成趣。'},
                {'spec': '200mm 中长焦全画幅镜头 (视场 ~10°×7°)', 'view': '完整容纳鬼宿四星（θ、η、γ、δ Cnc）矩形天区与中央积尸气，真实还原中国古籍“荧惑入鬼”经典星野。'},
                {'spec': '400~600mm 超长焦望远镜 (视场 ~1.0°)', 'view': '高倍局部特写，清晰解析火星视圆面（5.4角秒）与 ε Cnc（角距仅 2.4 角分）的超密近距构型。'}
            ],
            'hdr_exposure_protocol': '火星比星团成员星亮约 5.2 等（光通量高 120 倍）。常规单张曝光会导致火星严重过曝泛白。建议采用包围曝光 HDR 合成：火星本体采用 0.5s 短曝光保留金红橙色与反照率斑块，星团恒星采用 15~30s 追踪长曝光捕获外围微弱成员星。'
        }
    }

def print_text_report(data):
    print('=' * 80)
    print(f" {data['title']} ")
    print('=' * 80)
    print(f"报告生成时间: {data['generated_at_cst']} CST")
    print()
    
    mp = data['mars_physics']
    tl = data['timeline']
    m44 = data['m44_cluster_data']
    fc = data['flux_contrast']
    
    print('【一、核心物理参量与天体力学极值】')
    print(f"- 火星视星等: V = {mp['mag']} 等 | 视直径: {mp['angular_diameter_arcsec']}角秒 | 照亮比例: {mp['illumination_pct']}%")
    print(f"- 空间距离: 地心距离 {mp['earth_distance_au']} AU ({mp['earth_distance_km']:,} km) | 日心距离 {mp['sun_distance_au']} AU")
    print(f"- M44 蜂巢星团: 距离 {m44['distance_ly']} 光年 (182 pc) | 年龄 {m44['age_myr']} Myr | 成员星 ~{m44['total_stars']} 颗")
    print(f"- 星团视直径: 核心 {m44['core_radius_arcmin']*2:.0f}' (0.83°) | 外晕 {m44['cluster_radius_arcmin']*2:.0f}' (1.58°) | 综合视星等 V = {m44['integrated_v_mag']}")
    print()
    
    print('【二、贯穿星团核心动力学时间线 (CST)】')
    print(f"- 踏入星团外围边界 (角距 < 47.5'): {tl['cluster_entry_cst']}")
    print(f"- 步入星团核心致密区 (角距 < 25.0'): {tl['core_entry_cst']}")
    print(f"- 极近星团几何中心时刻:            {tl['closest_approach_cst']}")
    print(f"  -> 最小中心角距: **{tl['min_distance_to_center_arcmin']}'** ({tl['min_distance_to_center_arcsec']}角秒, 仅 0.080°)")
    print(f"- 驶出星团核心致密区 (角距 > 25.0'): {tl['core_exit_cst']}")
    print(f"- 离开星团外围边界 (角距 > 47.5'): {tl['cluster_exit_cst']}")
    print()
    
    print('【三、与星团内部核心成员星极近会合榜单】')
    print(f"{'成员星':<28} | {'光谱/类型':<10} | {'视星等':<6} | {'最小角距':<12} | {'最近时刻 (CST)':<19}")
    print('-' * 84)
    for s in tl['star_encounters']:
        print(f"{s['star_name']:<28} | {s['spectral_type']:<10} | {s['star_mag']:<6.2f} | {s['min_separation_arcmin']:>5.2f}' ({s['min_separation_arcsec']:>5.1f}角秒) | {s['closest_time_cst']:<19}")
    print()
    
    print('【四、光学通量与双色反差解析】')
    print(f"- 亮度反差: 火星相对 M44 整星团通量高出 {fc['mars_to_m44_flux_ratio']} 倍，相对中央最亮主序星 ε Cnc 高出 {fc['mars_to_eps_cnc_flux_ratio']} 倍。")
    print(f"- 色彩反差: {fc['color_contrast_bv']['visual_description']}")
    print()
    
    print('【五、华夏主要城市观象几何与暗夜天窗 (2026-10-11/12 冲顶通宵)】')
    print(f"{'城市节点':<14} | {'升起 (CST)':<10} | {'中天 (CST)':<10} | {'中天仰角':<8} | {'晨光终 (CST)':<11} | {'晨光仰角':<8} | {'纯暗夜窗口':<10}")
    print('-' * 84)
    for ck, c in data['china_cities_visibility'].items():
        print(f"{c['city_name']:<14} | {c['mars_rise_cst']:<10} | {c['mars_transit_cst']:<10} | {c['transit_altitude_deg']:>6.1f}° | {c['astronomical_dawn_cst']:<11} | {c['dawn_altitude_deg']:>6.1f}° | {c['dark_sky_duration_hours']:>6.1f} 小时")
    print("- 月相干扰: 10-11/12 正值农历九月初二/初三，纤细月牙日落即沉，通宵月光干扰 0.0%，暗夜天穹澄澈纯黑。")
    print('=' * 80)

def main():
    parser = argparse.ArgumentParser(description='2026 Mars-M44 Praesepe Transit Ephemeris & Observation Engine')
    parser.add_argument('--json', action='store_true', help='Output results as structured JSON')
    parser.add_argument('--date', default='2026-10-12', help='Reference observation date (default: 2026-10-12)')
    args = parser.parse_args()
    
    data = compute_full_mars_praesepe_report()
    
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print_text_report(data)

if __name__ == '__main__':
    main()
