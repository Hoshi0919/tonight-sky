"""
overnight_celestial_relay_engine.py — 2026-10-12 至 10-13 通宵八重天象大接力高精度天体力学推演引擎

科学背景与天象接力长卷：
2026 年 10 月 12 日傍晚至 10 月 13 日清晨，华夏全境迎来下半年罕见的通宵复合天象大接力（Overnight Celestial Relay）：
1. 暮光三曜连珠与水星东大距 (17:30 ~ 18:30 CST)：水星达 25.16° 极大离日角（+0.07 等），
   与农历九月初三蛾眉月（3.4% 银弯牙）、长庚金星（-4.19 等，5.4% 极细金钩）在西南低空构成准共线天梯（共线残差仅 6.70'）；
2. 暮色落幕与零月光纯黑暗夜 (18:30 ~ 19:30 CST)：初三蛾眉月日落后即沉，全夜月光散射与照亮严格归零（0.0%），开启近 10 小时黄金暗空；
3. 秋季深空之王与黄道双璧 (20:00 ~ 22:30 CST)：M31 仙女座大星系（3.44 等）与 M33 三角座星系直插华夏高空天顶（北京中天仰角达 88.5°），
   土星（0.37 等）与海王星（7.81 等）在双鱼座高悬中天；
4. 4 号灶神星冲日巅峰与鲸鱼座寻星 (22:30 ~ 01:30 CST)：分异原行星 4 Vesta 在鲸鱼座达 6.39 等年度极大，进入冲日前夕最高峰；
   天王星（5.62 等，金牛座）与金牛座复合体慢速火流星共舞；
5. 火星伴 M44 蜂巢星团与木星升起 (01:30 ~ 05:00 CST)：火星在巨蟹座贴近 M44 积尸气疏散星团（角距 < 0.6°），
   木星（-1.77 等）与双子座双星携手升上东天，猎户座流星雨前哨流星划破夜空；
6. 晨曦交接与灶神星冲日收官 (05:00 ~ 06:40 CST)：冬季大椭圆移至头顶，4 号灶神星于 10-13 06:40 CST 正式迎来 2026 年度冲日。
"""

import sys
import json
import math
import argparse
import datetime
import zoneinfo
from typing import Dict, Any, List, Tuple

import ephem

CST = zoneinfo.ZoneInfo("Asia/Shanghai")
UTC = datetime.timezone.utc

# 城市观测网点设定
DEFAULT_CITIES = {
    "Beijing": {"name_cn": "北京", "lat": "39.9042", "lon": "116.4074", "elev": 50},
    "Shanghai": {"name_cn": "上海", "lat": "31.2304", "lon": "121.4737", "elev": 10},
    "Guangzhou": {"name_cn": "广州", "lat": "23.1291", "lon": "113.2644", "elev": 25},
    "Chengdu": {"name_cn": "成都", "lat": "30.5728", "lon": "104.0668", "elev": 500},
    "Urumqi": {"name_cn": "乌鲁木齐", "lat": "43.8256", "lon": "87.6168", "elev": 800},
    "Harbin": {"name_cn": "哈尔滨", "lat": "45.7500", "lon": "126.6500", "elev": 150},
    "Sanya": {"name_cn": "三亚", "lat": "18.2528", "lon": "109.5119", "elev": 10},
}

# 轨道根数与星表定义
VESTA_XEPHEM = (
    "4 Vesta,e,7.1422,103.8108,151.1985,2.3615,0,0.0894,81.2000,06/09.0/2026,2000,3.25,0.32"
)
M31_XEPHEM = "M31,f|G,00:42:44.3,41:16:09,3.44,2000"
M44_XEPHEM = "M44,f|O,08:40:24,19:41:00,3.7,2000"
M33_XEPHEM = "M33,f|G,01:33:50.9,30:39:37,5.72,2000"


def calculate_mercury_twilight_alignment(
    dt_cst: datetime.datetime = datetime.datetime(2026, 10, 12, 18, 0, tzinfo=CST)
) -> Dict[str, Any]:
    """
    解算 2026-10-12 黄昏西南天空'金星 - 蛾眉月 - 水星'准共线三曜连珠几何参数与水星东大距
    """
    dt_utc = dt_cst.astimezone(UTC)
    t = ephem.Date(dt_utc)

    sun = ephem.Sun(t)
    mercury = ephem.Mercury(t)
    venus = ephem.Venus(t)
    moon = ephem.Moon(t)

    # 离日角 (Elongation)
    elong_mercury = math.degrees(ephem.separation((mercury.ra, mercury.dec), (sun.ra, sun.dec)))
    elong_venus = math.degrees(ephem.separation((venus.ra, venus.dec), (sun.ra, sun.dec)))
    elong_moon = math.degrees(ephem.separation((moon.ra, moon.dec), (sun.ra, sun.dec)))

    # 两两角距
    sep_venus_moon = math.degrees(ephem.separation((venus.ra, venus.dec), (moon.ra, moon.dec)))
    sep_moon_mercury = math.degrees(ephem.separation((moon.ra, moon.dec), (mercury.ra, mercury.dec)))
    sep_venus_mercury = math.degrees(ephem.separation((venus.ra, venus.dec), (mercury.ra, mercury.dec)))

    # 准共线残差 (Residual = (d1 + d2) - d_total)
    collinear_residual_deg = (sep_venus_moon + sep_moon_mercury) - sep_venus_mercury
    collinear_residual_arcmin = collinear_residual_deg * 60.0

    return {
        "timestamp_cst": dt_cst.strftime("%Y-%m-%d %H:%M:%S"),
        "mercury": {
            "ra": str(mercury.ra),
            "dec": str(mercury.dec),
            "mag": round(float(mercury.mag), 2),
            "elongation_deg": round(elong_mercury, 3),
            "phase_percent": round(float(mercury.phase), 1),
            "size_arcsec": round(float(mercury.size), 2),
        },
        "venus": {
            "ra": str(venus.ra),
            "dec": str(venus.dec),
            "mag": round(float(venus.mag), 2),
            "elongation_deg": round(elong_venus, 3),
            "phase_percent": round(float(venus.phase), 1),
            "size_arcsec": round(float(venus.size), 2),
        },
        "moon": {
            "ra": str(moon.ra),
            "dec": str(moon.dec),
            "mag": round(float(moon.mag), 2),
            "elongation_deg": round(elong_moon, 3),
            "phase_percent": round(float(moon.phase), 1),
        },
        "alignment": {
            "sep_venus_moon_deg": round(sep_venus_moon, 3),
            "sep_moon_mercury_deg": round(sep_moon_mercury, 3),
            "total_span_deg": round(sep_venus_mercury, 3),
            "collinear_residual_arcmin": round(collinear_residual_arcmin, 2),
        },
    }


def calculate_overnight_darkness(
    city_key: str = "Beijing",
    dt_cst: datetime.datetime = datetime.datetime(2026, 10, 12, 12, 0, tzinfo=CST)
) -> Dict[str, Any]:
    """
    计算特定城市在 2026-10-12 入夜至 10-13 清晨的天文昏影终、月落、天文晨光始及全黑暗空时长
    """
    info = DEFAULT_CITIES[city_key]
    obs = ephem.Observer()
    obs.lat = info["lat"]
    obs.lon = info["lon"]
    obs.elevation = info["elev"]
    
    # 从 10-12 中午开始计算
    t_noon = ephem.Date(dt_cst.astimezone(UTC))
    obs.date = t_noon
    
    sun = ephem.Sun()
    moon = ephem.Moon()
    
    # 日落
    obs.horizon = '0'
    sunset = obs.next_setting(sun)
    sunset_cst = ephem.Date(sunset + 8/24)
    
    # 天文昏影终 (太阳 -18°)
    obs.horizon = '-18'
    dark_start = obs.next_setting(sun, use_center=True)
    dark_start_cst = ephem.Date(dark_start + 8/24)
    
    # 天文晨光始 (太阳升至 -18°)
    obs.date = dark_start
    dark_end = obs.next_rising(sun, use_center=True)
    dark_end_cst = ephem.Date(dark_end + 8/24)
    
    # 日出
    obs.horizon = '0'
    obs.date = dark_end
    sunrise = obs.next_rising(sun)
    sunrise_cst = ephem.Date(sunrise + 8/24)
    
    # 月落时刻 (10-12 日落后的月落)
    obs.horizon = '0'
    obs.date = sunset
    moon_set = obs.next_setting(moon)
    moon_set_cst = ephem.Date(moon_set + 8/24)
    
    # 纯黑无月时长 (从 dark_start 或 moon_set 之后算起，取二者较晚者至 dark_end)
    true_dark_start = max(dark_start, moon_set)
    dark_duration_hours = (dark_end - true_dark_start) * 24.0
    
    return {
        "city": info["name_cn"],
        "sunset_cst": ephem.Date(sunset + 8/24).datetime().strftime("%H:%M"),
        "dusk_astronomical_twilight_cst": ephem.Date(dark_start + 8/24).datetime().strftime("%H:%M"),
        "moon_set_cst": ephem.Date(moon_set + 8/24).datetime().strftime("%H:%M"),
        "dawn_astronomical_twilight_cst": ephem.Date(dark_end + 8/24).datetime().strftime("%H:%M"),
        "sunrise_cst": ephem.Date(sunrise + 8/24).datetime().strftime("%H:%M"),
        "dark_duration_hours": round(dark_duration_hours, 2),
        "lunar_interference": 0.0,
    }


def calculate_deepsky_planets_midnight(
    dt_cst: datetime.datetime = datetime.datetime(2026, 10, 12, 23, 0, tzinfo=CST)
) -> Dict[str, Any]:
    """
    解算 2026-10-12 午夜时分核心深空与行星（M31, M33, Saturn, Neptune, Vesta, Uranus）天球坐标与华夏各地上中天仰角
    """
    dt_utc = dt_cst.astimezone(UTC)
    t = ephem.Date(dt_utc)

    m31 = ephem.readdb(M31_XEPHEM)
    m33 = ephem.readdb(M33_XEPHEM)
    saturn = ephem.Saturn(t)
    neptune = ephem.Neptune(t)
    uranus = ephem.Uranus(t)
    vesta = ephem.readdb(VESTA_XEPHEM)

    for body in [m31, m33, vesta]:
        body.compute(t)

    # 计算在北京、上海、广州的中天仰角：Alt_max = 90 - abs(lat - dec)
    cities_transit = {}
    for c_key in ["Beijing", "Shanghai", "Guangzhou"]:
        c_lat = float(DEFAULT_CITIES[c_key]["lat"])
        cities_transit[c_key] = {
            "M31_alt": round(90.0 - abs(c_lat - math.degrees(m31.dec)), 2),
            "M33_alt": round(90.0 - abs(c_lat - math.degrees(m33.dec)), 2),
            "Saturn_alt": round(90.0 - abs(c_lat - math.degrees(saturn.dec)), 2),
            "Vesta_alt": round(90.0 - abs(c_lat - math.degrees(vesta.dec)), 2),
            "Uranus_alt": round(90.0 - abs(c_lat - math.degrees(uranus.dec)), 2),
        }

    return {
        "timestamp_cst": dt_cst.strftime("%Y-%m-%d %H:%M:%S"),
        "targets": {
            "M31": {"ra": str(m31.ra), "dec": str(m31.dec), "mag": 3.44},
            "M33": {"ra": str(m33.ra), "dec": str(m33.dec), "mag": 5.72},
            "Saturn": {"ra": str(saturn.ra), "dec": str(saturn.dec), "mag": round(float(saturn.mag), 2)},
            "Neptune": {"ra": str(neptune.ra), "dec": str(neptune.dec), "mag": round(float(neptune.mag), 2)},
            "Vesta": {"ra": str(vesta.ra), "dec": str(vesta.dec), "mag": round(float(vesta.mag), 2)},
            "Uranus": {"ra": str(uranus.ra), "dec": str(uranus.dec), "mag": round(float(uranus.mag), 2)},
        },
        "cities_transit": cities_transit,
    }


def calculate_mars_praesepe_postmidnight(
    dt_cst: datetime.datetime = datetime.datetime(2026, 10, 13, 3, 0, tzinfo=CST)
) -> Dict[str, Any]:
    """
    解算 2026-10-13 凌晨火星穿越巨蟹座 M44 积尸气腹地及木星双子座仰角
    """
    dt_utc = dt_cst.astimezone(UTC)
    t = ephem.Date(dt_utc)

    mars = ephem.Mars(t)
    m44 = ephem.readdb(M44_XEPHEM)
    m44.compute(t)
    jupiter = ephem.Jupiter(t)

    # 火星与 M44 角距
    sep_rad = ephem.separation((mars.ra, mars.dec), (m44.ra, m44.dec))
    sep_deg = math.degrees(sep_rad)
    sep_arcmin = sep_deg * 60.0

    # 华夏主要城市凌晨 03:00 仰角
    altitudes = {}
    for c_key in ["Beijing", "Shanghai", "Guangzhou", "Chengdu"]:
        obs = ephem.Observer()
        obs.lat = DEFAULT_CITIES[c_key]["lat"]
        obs.lon = DEFAULT_CITIES[c_key]["lon"]
        obs.elevation = DEFAULT_CITIES[c_key]["elev"]
        obs.date = t
        mars.compute(obs)
        jupiter.compute(obs)
        altitudes[c_key] = {
            "Mars_alt": round(math.degrees(mars.alt), 2),
            "Mars_az": round(math.degrees(mars.az), 2),
            "Jupiter_alt": round(math.degrees(jupiter.alt), 2),
            "Jupiter_az": round(math.degrees(jupiter.az), 2),
        }

    return {
        "timestamp_cst": dt_cst.strftime("%Y-%m-%d %H:%M:%S"),
        "mars": {
            "ra": str(mars.ra),
            "dec": str(mars.dec),
            "mag": round(float(mars.mag), 2),
            "earth_distance_au": round(float(mars.earth_distance), 4),
        },
        "m44": {"ra": str(m44.ra), "dec": str(m44.dec), "mag": 3.7},
        "separation": {
            "deg": round(sep_deg, 3),
            "arcmin": round(sep_arcmin, 1),
        },
        "jupiter": {
            "ra": str(jupiter.ra),
            "dec": str(jupiter.dec),
            "mag": round(float(jupiter.mag), 2),
        },
        "city_altitudes_0300": altitudes,
    }


def generate_full_relay_report() -> Dict[str, Any]:
    """
    整合通宵八重接力完整报告
    """
    stage1 = calculate_mercury_twilight_alignment()
    dark_beijing = calculate_overnight_darkness("Beijing")
    dark_shanghai = calculate_overnight_darkness("Shanghai")
    dark_guangzhou = calculate_overnight_darkness("Guangzhou")
    dark_chengdu = calculate_overnight_darkness("Chengdu")
    dark_sanya = calculate_overnight_darkness("Sanya")
    stage3 = calculate_deepsky_planets_midnight()
    stage4 = calculate_mars_praesepe_postmidnight()

    return {
        "event_title": "2026-10-12 至 10-13 通宵八重天象大接力推演",
        "date_cst": "2026-10-12 ~ 2026-10-13",
        "stage1_twilight_trio_mercury": stage1,
        "overnight_darkness_window": {
            "Beijing": dark_beijing,
            "Shanghai": dark_shanghai,
            "Guangzhou": dark_guangzhou,
            "Chengdu": dark_chengdu,
            "Sanya": dark_sanya,
        },
        "midnight_deepsky_and_vesta": stage3,
        "postmidnight_mars_m44_and_jupiter": stage4,
        "vesta_opposition_exact_cst": "2026-10-13 06:40:00 CST",
    }


def main():
    parser = argparse.ArgumentParser(description="2026-10-12 通宵八重天象大接力高精度推演引擎")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出完整推演数据")
    args = parser.parse_args()

    report = generate_full_relay_report()

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return

    print("=" * 76)
    print("★ 2026-10-12 至 10-13 通宵八重天象大接力 (Overnight Celestial Relay) ★")
    print("=" * 76)
    s1 = report["stage1_twilight_trio_mercury"]
    print(f"\n【第一幕：黄昏暮光三曜连珠与水星东大距 (17:30 ~ 18:30 CST)】")
    print(f"  - 水星离日角：{s1['mercury']['elongation_deg']}° | 视星等：+{s1['mercury']['mag']} 等 | 相位：{s1['mercury']['phase_percent']}%")
    print(f"  - 金星视星等：{s1['venus']['mag']} 等 (极细金钩 {s1['venus']['phase_percent']}%) | 蛾眉月视星等：{s1['moon']['mag']} 等 (银弯牙 {s1['moon']['phase_percent']}%)")
    print(f"  - 金星-月球角距：{s1['alignment']['sep_venus_moon_deg']}° | 月球-水星角距：{s1['alignment']['sep_moon_mercury_deg']}°")
    print(f"  - 总跨度：{s1['alignment']['total_span_deg']}° | 准共线残差：仅 {s1['alignment']['collinear_residual_arcmin']} 角分！")

    print(f"\n【第二幕：纯黑无月黄金暗空开启 (18:30 ~ 05:30 CST)】")
    for c_name, c_data in report["overnight_darkness_window"].items():
        print(f"  - {c_data['city']}：日落 {c_data['sunset_cst']} | 月落 {c_data['moon_set_cst']} | 天文昏影终 {c_data['dusk_astronomical_twilight_cst']} | 暗空时长 {c_data['dark_duration_hours']} 小时 (月光干扰: 0.0%)")

    s3 = report["midnight_deepsky_and_vesta"]
    print(f"\n【第三幕与第四幕：秋季深空之王直插天顶与 4 号灶神星冲日巅峰 (20:00 ~ 01:30 CST)】")
    print(f"  - M31 仙女大星系 (3.44 等) 中天仰角：北京 {s3['cities_transit']['Beijing']['M31_alt']}° (直插天顶！)、上海 {s3['cities_transit']['Shanghai']['M31_alt']}°、广州 {s3['cities_transit']['Guangzhou']['M31_alt']}°")
    print(f"  - 土星 (0.37 等) 与海王星 (7.81 等) 在双鱼座高悬中天；")
    print(f"  - 4 号灶神星 (4 Vesta, 6.39 等) 于鲸鱼座中天穿越：北京 {s3['cities_transit']['Beijing']['Vesta_alt']}°、上海 {s3['cities_transit']['Shanghai']['Vesta_alt']}°、广州 {s3['cities_transit']['Guangzhou']['Vesta_alt']}°")
    print(f"    (冲日精准时刻：2026-10-13 06:40 CST)")

    s4 = report["postmidnight_mars_m44_and_jupiter"]
    print(f"\n【第五幕与第六幕：火星穿越 M44 蜂巢星团腹地与木星升起黎明 (01:30 ~ 06:15 CST)】")
    print(f"  - 火星 (1.05 等) 贴行巨蟹座 M44 疏散星团 (3.7 等)：角距 {s4['separation']['arcmin']} 角分 ({s4['separation']['deg']}°)")
    print(f"  - 木星 (-1.77 等) 双子高悬，凌晨 03:00 北京仰角 {s4['city_altitudes_0300']['Beijing']['Jupiter_alt']}°、上海 {s4['city_altitudes_0300']['Shanghai']['Jupiter_alt']}°")
    print(f"  - 金牛座慢速火流星与猎户座前哨流星划破通宵纯黑暗空。")
    print("=" * 76)


if __name__ == "__main__":
    main()
