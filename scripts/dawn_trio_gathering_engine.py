"""
dawn_trio_gathering_engine.py — 2026-11-03 晨曦三星聚会天体力学推演引擎

天体物理与动力学背景：
1. 晨曦三星聚会（Dawn Trio Gathering: Moon-Jupiter-Mars）：
   - 2026年11月03日清晨（农历九月廿五），东方破晓前的晨曦夜空中，下弦后的弯弯残月（38.4% 照亮）
     与太阳系两颗明亮行星——木星（Jupiter, -1.88 等）与火星（Mars, +0.86 等）在双子座足部天区
     上演极其罕见的紧密同框与极近合相。
2. 站心视差（Topocentric Parallax）与月木相切几何：
   - 地月距离约为 368,000 km，月球赤道地平视差高达 ~59'；
   - 木星距离地球约 4.3 AU，火星距离地球约 1.5 AU，二者站心视差 < 2"，可视为恒星背景基准；
   - 观测者地理纬度的差异对月球站心视位置产生显著位移：
     * 华南低纬区（广州 23°N）：月球与木星站心角距在 05:54 CST 达到极小值 0.510° (30.6')，
       近乎与月轮亮缘无缝贴合掠过（月球视半径约 15.6'）；
     * 华东沿海（上海 31°N）：相切时刻在 06:00 CST，最小角距 0.693° (41.6')，正值民用晨光蓝调时刻；
     * 华北地区（北京 40°N）：相切时刻在 05:48 CST，最小角距 0.785° (47.1')；
     * 东北地区（哈尔滨 46°N）：最小角距 0.929° (55.8')。
3. 双筒望远镜（Binocular Field of View）完整同框包络：
   - 火星与木星角距稳定在 5.06°；
   - 残月与火星角距稳定在 5.04°；
   - 残月、木星与火星三者构成的锐角三角形最大外接跨度仅 5.06°，可被标准 7×50 或 10×50 双筒望远镜
     （典型视场 FOV 6.5°~7.2°）完整收纳于同一视野之内。
4. 晨曦光照阶段与肉眼反差（Twilight Visibility & Earthshine）：
   - 木星（-1.88 等）表面亮度极高，在民用晨光（太阳高度 -6° 至 0°）期间依然肉眼清晰可见；
   - 残月暗面由地球反照光照亮，呈现微弱而优雅的达·芬奇辉光（Earthshine / 地照）；
   - 高仰角优势：相切时刻在东部沿海仰角高达 68.6°，几乎直指天顶，完全避开低空大气湍流与雾霾消光。
"""

import sys
import json
import math
import datetime
import zoneinfo
from typing import Dict, Any, List

import ephem

CST = zoneinfo.ZoneInfo("Asia/Shanghai")
UTC = datetime.timezone.utc

# 国内典型代表城市坐标
CITIES = [
    {"name": "Shanghai", "chinese": "上海", "lat": 31.2304, "lon": 121.4737, "elevation": 10},
    {"name": "Beijing", "chinese": "北京", "lat": 39.9042, "lon": 116.4074, "elevation": 50},
    {"name": "Guangzhou", "chinese": "广州", "lat": 23.1291, "lon": 113.2644, "elevation": 20},
    {"name": "Chengdu", "chinese": "成都", "lat": 30.5728, "lon": 104.0668, "elevation": 500},
    {"name": "Harbin", "chinese": "哈尔滨", "lat": 45.7569, "lon": 126.6366, "elevation": 150},
    {"name": "Urumqi", "chinese": "乌鲁木齐", "lat": 43.8256, "lon": 87.6168, "elevation": 800},
    {"name": "Lhasa", "chinese": "拉萨", "lat": 29.6500, "lon": 91.1000, "elevation": 3650},
]


def airmass(alt_deg: float) -> float:
    """计算高度角 alt_deg 对应的大气气团数 (Airmass)。"""
    if alt_deg <= 0.1:
        return 40.0
    z_deg = max(0.0, min(89.9, 90.0 - alt_deg))
    z_rad = math.radians(z_deg)
    cos_z = math.cos(z_rad)
    sec_z_eff = 1.0 / (cos_z + 0.50572 * max(0.1, 96.07995 - z_deg) ** (-1.6364))
    return min(40.0, float(sec_z_eff))


def calculate_gathering_ephemeris(date_str: str = "2026-11-03", city_key: str = "Shanghai") -> Dict[str, Any]:
    """计算指定城市在 2026-11-03 晨曦三星聚会全流程天象参数。"""
    city_info = next((c for c in CITIES if c["name"].lower() == city_key.lower()), CITIES[0])

    obs = ephem.Observer()
    obs.lat = str(city_info["lat"])
    obs.lon = str(city_info["lon"])
    obs.elevation = city_info["elevation"]

    moon = ephem.Moon()
    jup = ephem.Jupiter()
    mars = ephem.Mars()
    sun = ephem.Sun()

    # 1. 扫描 11-03 01:00 ~ 08:00 CST 间的月木站心角距极小值
    t_base_utc = datetime.datetime(2026, 11, 2, 17, 0, tzinfo=UTC) # 01:00 CST
    min_sep_mj = 999.0
    best_t_utc = None

    for m in range(0, 421):
        cur_t_utc = t_base_utc + datetime.timedelta(minutes=m)
        obs.date = ephem.Date(cur_t_utc)
        moon.compute(obs)
        jup.compute(obs)
        sep = math.degrees(ephem.separation(moon, jup))
        if sep < min_sep_mj:
            min_sep_mj = sep
            best_t_utc = cur_t_utc

    best_t_cst = best_t_utc.astimezone(CST)

    # 2. 计算极值时刻的三曜参数
    obs.date = ephem.Date(best_t_utc)
    moon.compute(obs)
    jup.compute(obs)
    mars.compute(obs)
    sun.compute(obs)

    sep_moon_mars = math.degrees(ephem.separation(moon, mars))
    sep_jup_mars = math.degrees(ephem.separation(jup, mars))

    # 3. 计算日出与晨光分期
    obs.date = ephem.Date(datetime.datetime(2026, 11, 2, 20, 0, tzinfo=UTC)) # 04:00 CST
    sunrise_utc = obs.next_rising(sun)
    sunrise_cst = ephem.localtime(sunrise_utc)

    obs.horizon = "-6"
    civ_twilight_utc = obs.next_rising(sun, use_center=True)
    civ_twilight_cst = ephem.localtime(civ_twilight_utc)

    obs.horizon = "-12"
    naut_twilight_utc = obs.next_rising(sun, use_center=True)
    naut_twilight_cst = ephem.localtime(naut_twilight_utc)

    obs.horizon = "-18"
    astro_twilight_utc = obs.next_rising(sun, use_center=True)
    astro_twilight_cst = ephem.localtime(astro_twilight_utc)

    # 4. 双筒望远镜包络跨度 (三曜最大角距)
    max_span = max(min_sep_mj, sep_moon_mars, sep_jup_mars)
    binocular_fit_7deg = max_span <= 7.0

    return {
        "city": city_info["chinese"],
        "city_en": city_info["name"],
        "latitude": city_info["lat"],
        "longitude": city_info["lon"],
        "conjunction_time_cst": best_t_cst.strftime("%Y-%m-%d %H:%M:%S"),
        "min_separation_moon_jupiter_deg": round(min_sep_mj, 3),
        "min_separation_moon_jupiter_arcmin": round(min_sep_mj * 60.0, 1),
        "separation_moon_mars_deg": round(sep_moon_mars, 3),
        "separation_jupiter_mars_deg": round(sep_jup_mars, 3),
        "trio_maximum_span_deg": round(max_span, 3),
        "binocular_fov_fit": binocular_fit_7deg,
        "moon_phase_pct": round(moon.phase, 1),
        "moon_altitude_deg": round(math.degrees(moon.alt), 1),
        "moon_azimuth_deg": round(math.degrees(moon.az), 1),
        "jupiter_altitude_deg": round(math.degrees(jup.alt), 1),
        "jupiter_magnitude": round(float(jup.mag), 2),
        "mars_altitude_deg": round(math.degrees(mars.alt), 1),
        "mars_magnitude": round(float(mars.mag), 2),
        "sun_altitude_deg": round(math.degrees(sun.alt), 1),
        "twilight_schedule_cst": {
            "astronomical_dawn": astro_twilight_cst.strftime("%H:%M:%S"),
            "nautical_dawn": naut_twilight_cst.strftime("%H:%M:%S"),
            "civil_dawn": civ_twilight_cst.strftime("%H:%M:%S"),
            "sunrise": sunrise_cst.strftime("%H:%M:%S"),
        },
        "optimal_observation_window_cst": f"{civ_twilight_cst.strftime('%H:%M')}–{sunrise_cst.strftime('%H:%M')}",
    }


def calculate_all_cities_summary() -> Dict[str, Any]:
    """计算全国代表城市的晨曦三星聚会对比数据。"""
    results = {}
    for c in CITIES:
        results[c["name"]] = calculate_gathering_ephemeris(city_key=c["name"])
    return {
        "event": "2026-11-03 晨曦三星聚会 (Dawn Trio Gathering)",
        "date": "2026-11-03",
        "description": "下弦残月与木星极近相切、火星5°同框之晨曦奇观",
        "cities": results,
    }


def main():
    summary = calculate_all_cities_summary()
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
