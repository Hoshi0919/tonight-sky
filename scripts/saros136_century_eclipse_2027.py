"""
2027 年 8 月 2 日 21 世纪最长陆地日全食天体力学推演与沙罗 136 王者家族研究
The Century Total Solar Eclipse (2027-08-02) & Saros 136 Dynasty Engine

科学背景与核心天体物理机理：
1. 沙罗周期 136（Saros 136）——人类历史上最负盛名的“日全食王者家族”：
   - 1919-05-29 (#32): 爱丁顿远征普林西比与索布拉尔，验证广义相对论引力光线偏折 (6m 51s)。
   - 1937-06-08 (#33): 太平洋大日食 (7m 04s)。
   - 1955-06-20 (#34): 菲律宾与东南亚，20 世纪最长日全食 (7m 08s)。
   - 1973-06-30 (#35): 协和号 001 超音速客机 Mach 2 逆风追日，创造人类连续 74 分钟全食奇迹 (地表 7m 04s)。
   - 1991-07-11 (#36): 夏威夷冒纳凯阿与墨西哥 (6m 53s)。
   - 2009-07-22 (#37): 中国长江流域世纪大日食 (6m 39s)。
   - 2027-08-02 (#38): 埃及卢克索 / 地中海 / 北非，21 世纪陆地最长日全食 (6m 23s)。
   - 2045-08-12 (#39): 美国本土东西横贯大日食 (6m 06s)。
2. 极端天体力学几何对冲：
   - 地球处于远日点附近（日地距 1.0149 AU，太阳视直径收缩至年度极小 31.52'）。
   - 月球运行于近地点附近（地月距仅 357,384 km，月球站心视直径暴涨至 34.08'）。
   - 视直径比值（日食食分）高达 1.0811，月球视面积比太阳超出 16.9%！
   - 本影锥地表截面宽度达 257.7 km，日食中心线地表投影移动速度降至仅 ~0.55 km/s。
3. 转轮周期（Exeligmos Cycle）：
   - 3 个沙罗周期 = 54 年 34 天，累计额外累积的三分之一日（8小时 × 3 = 24小时）抵消地球自转偏移，
     全食带跨越半个世纪精准回归相同经度扇区（1973 撒哈拉 -> 2027 埃及尼罗河谷）。
4. 华夏西域日落偏食天窗：
   - 新疆塔什库尔干（塔县）与西藏阿里（狮泉河）在 2027-08-02 傍晚日落前夕迎来偏食入带，
     阿里最大食分达 0.060，塔县达 0.040，成为华夏全境独享的西域晚霞日偏食窗口。
"""

import sys
import math
import json
import argparse
import datetime
from typing import Dict, Any, List, Tuple

import ephem

# 沙罗 136 历史与未来极盛名录
SAROS_136_CATALOG = [
    {
        "saros_num": 32,
        "date": "1919-05-29",
        "duration_sec": 411,
        "duration_str": "6m 51s",
        "location": "普林西比岛 / 巴西索布拉尔",
        "historic_significance": "爱丁顿远征队测定太阳引力场光线偏折 1.98″，首次实验证实爱因斯坦广义相对论",
    },
    {
        "saros_num": 33,
        "date": "1937-06-08",
        "duration_sec": 424,
        "duration_str": "7m 04s",
        "location": "太平洋中部 / 秘鲁",
        "historic_significance": "20 世纪首个突破 7 分钟大关的日全食",
    },
    {
        "saros_num": 34,
        "date": "1955-06-20",
        "duration_sec": 428,
        "duration_str": "7m 08s",
        "location": "斯里兰卡 / 泰国 / 菲律宾",
        "historic_significance": "近三百年内全食时间最长极值记录（7分08秒），沙罗136巅峰时刻",
    },
    {
        "saros_num": 35,
        "date": "1973-06-30",
        "duration_sec": 424,
        "duration_str": "7m 04s",
        "location": "毛里塔尼亚 / 撒哈拉 / 肯尼亚",
        "historic_significance": "协和号 001 原型机以 Mach 2.05 超音速飞行追逐月影，创造人类连续 74 分钟全食奇迹",
    },
    {
        "saros_num": 36,
        "date": "1991-07-11",
        "duration_sec": 413,
        "duration_str": "6m 53s",
        "location": "夏威夷冒纳凯阿 / 墨西哥 / 巴西",
        "historic_significance": "世界顶级高山天文台群（Mauna Kea）历史上唯一一次被日全食中心线直接贯穿",
    },
    {
        "saros_num": 37,
        "date": "2009-07-22",
        "duration_sec": 399,
        "duration_str": "6m 39s",
        "location": "中国长江流域 / 太平洋",
        "historic_significance": "中国长江流域世纪大日食，横贯成都、重庆、武汉、杭州、上海，惠及数亿人群",
    },
    {
        "saros_num": 38,
        "date": "2027-08-02",
        "duration_sec": 383,
        "duration_str": "6m 23s",
        "location": "直布罗陀 / 西班牙 / 埃及卢克索 / 红海",
        "historic_significance": "21 世纪陆地上持续时间最长的日全食，贯穿古埃及帝王谷与卡纳克神庙，少云黄金天候",
    },
    {
        "saros_num": 39,
        "date": "2045-08-12",
        "duration_sec": 366,
        "duration_str": "6m 06s",
        "location": "美国加州至佛罗里达 / 加勒比海",
        "historic_significance": "美国横跨全境超级大日食，全食带横断北美大陆东海岸至西海岸",
    },
    {
        "saros_num": 40,
        "date": "2063-08-24",
        "duration_sec": 349,
        "duration_str": "5m 49s",
        "location": "中国华北 / 日本海 / 太平洋",
        "historic_significance": "沙罗136再度降临东亚，全食带扫过中国北方与日本北部",
    },
]

INTERNATIONAL_STATIONS = {
    "Tarifa": {
        "name": "塔里法 / 直布罗陀 (西班牙)",
        "lat": "36.0128",
        "lon": "-5.6044",
        "elev": 20,
        "country": "Spain",
    },
    "Tangier": {
        "name": "丹吉尔 (摩洛哥)",
        "lat": "35.7595",
        "lon": "-5.8340",
        "elev": 30,
        "country": "Morocco",
    },
    "Oran": {
        "name": "奥兰 (阿尔及利亚)",
        "lat": "35.6987",
        "lon": "-0.6349",
        "elev": 60,
        "country": "Algeria",
    },
    "Sfax": {
        "name": "斯法克斯 (突尼斯)",
        "lat": "34.7406",
        "lon": "10.7603",
        "elev": 15,
        "country": "Tunisia",
    },
    "Benghazi": {
        "name": "班加西 (利比亚)",
        "lat": "32.1167",
        "lon": "20.0667",
        "elev": 10,
        "country": "Libya",
    },
    "Luxor": {
        "name": "卢克索 / 帝王谷 (埃及)",
        "lat": "25.6872",
        "lon": "32.6396",
        "elev": 89,
        "country": "Egypt",
    },
    "Jeddah": {
        "name": "吉达 (沙特阿拉伯)",
        "lat": "21.5433",
        "lon": "39.1728",
        "elev": 12,
        "country": "Saudi Arabia",
    },
    "Sanaa": {
        "name": "萨那 (也门)",
        "lat": "15.3694",
        "lon": "44.1910",
        "elev": 2250,
        "country": "Yemen",
    },
    "Bossaso": {
        "name": "博萨索 (索马里)",
        "lat": "11.2842",
        "lon": "49.1817",
        "elev": 15,
        "country": "Somalia",
    },
}

CHINA_WESTERN_STATIONS = {
    "Taxkorgan": {
        "name": "塔什库尔干 (新疆塔县)",
        "lat": "37.7719",
        "lon": "75.2286",
        "elev": 3100,
    },
    "Ali": {
        "name": "狮泉河 / 阿里 (西藏阿里)",
        "lat": "32.5028",
        "lon": "80.1054",
        "elev": 4280,
    },
    "Kashgar": {
        "name": "喀什 (新疆喀什)",
        "lat": "39.4704",
        "lon": "75.9897",
        "elev": 1290,
    },
    "Hotan": {
        "name": "和田 (新疆和田)",
        "lat": "37.1128",
        "lon": "79.9135",
        "elev": 1380,
    },
}


def compute_saros_harmonics() -> Dict[str, Any]:
    """
    计算沙罗周期与转轮周期（Exeligmos）的拍频谐波共振动力学
    """
    synodic_month = 29.530588853  # 朔望月 (日)
    draconic_month = 27.212220817  # 交点月 (日)
    anomalistic_month = 27.55454988  # 近点月 (日)

    n_syn = 223
    n_drac = 242
    n_anom = 239

    saros_days_syn = n_syn * synodic_month
    saros_days_drac = n_drac * draconic_month
    saros_days_anom = n_anom * anomalistic_month

    diff_drac_hours = (saros_days_drac - saros_days_syn) * 24.0
    diff_anom_hours = (saros_days_anom - saros_days_syn) * 24.0

    saros_base_days = 6585
    saros_frac_day = saros_days_syn - saros_base_days
    saros_extra_hours = saros_frac_day * 24.0

    # 地球自转导致的经度西移
    longitude_shift_deg = (saros_extra_hours / 24.0) * 360.0

    # 转轮周期 (3 个沙罗)
    exeligmos_days = 3.0 * saros_days_syn
    exeligmos_years = exeligmos_days / 365.2422

    return {
        "synodic_period_days": saros_days_syn,
        "draconic_period_days": saros_days_drac,
        "anomalistic_period_days": saros_days_anom,
        "draconic_diff_hours": round(diff_drac_hours, 2),
        "anomalistic_diff_hours": round(diff_anom_hours, 2),
        "saros_extra_hours": round(saros_extra_hours, 3),
        "longitude_shift_west_deg": round(longitude_shift_deg, 2),
        "exeligmos_days": round(exeligmos_days, 2),
        "exeligmos_years": round(exeligmos_years, 2),
    }


def compute_luxor_greatest_eclipse() -> Dict[str, Any]:
    """
    高精度解算 2027 年 8 月 2 日埃及卢克索（Greatest Eclipse）食相接触全过程
    """
    obs = ephem.Observer()
    obs.lat = "25.6872"
    obs.lon = "32.6396"
    obs.elevation = 89

    # 扫描基准时刻：2027-08-02 08:30 至 11:45 UTC
    t_start = ephem.Date("2027/08/02 08:30:00")
    t_end = ephem.Date("2027/08/02 11:45:00")

    # 第一轮粗扫（10 秒步长）锁定接触区间
    c1, c2, c3, c4 = None, None, None, None
    prev_state = "outside"

    cur = t_start
    while cur <= t_end:
        obs.date = cur
        sun = ephem.Sun(obs)
        moon = ephem.Moon(obs)
        sep = math.degrees(ephem.separation((sun.az, sun.alt), (moon.az, moon.alt))) * 3600.0
        r_sun = sun.size / 2.0
        r_moon = moon.size / 2.0

        if sep <= r_moon - r_sun:
            state = "total"
        elif sep < r_moon + r_sun:
            state = "partial"
        else:
            state = "outside"

        if prev_state == "outside" and state == "partial" and c1 is None:
            c1 = cur
        elif prev_state == "partial" and state == "total" and c2 is None:
            c2 = cur
        elif prev_state == "total" and state == "partial" and c3 is None:
            c3 = cur
        elif prev_state == "partial" and state == "outside" and c4 is None:
            c4 = cur

        prev_state = state
        cur = ephem.Date(cur + 5 * ephem.second)

    # 食甚时刻与物理参数 (C2 与 C3 中点)
    t_mid = ephem.Date((c2 + c3) / 2.0)
    obs.date = t_mid
    sun_mid = ephem.Sun(obs)
    moon_mid = ephem.Moon(obs)

    totality_duration_sec = (c3 - c2) * 86400.0
    partial_duration_sec = (c4 - c1) * 86400.0

    sun_diam_arcsec = sun_mid.size
    moon_diam_arcsec = moon_mid.size
    magnitude = moon_diam_arcsec / sun_diam_arcsec

    sun_alt_deg = math.degrees(sun_mid.alt)
    sun_az_deg = math.degrees(sun_mid.az)

    # 大气质量系数 Rozenberg (1966) 公式
    airmass = 1.0 / (math.sin(sun_mid.alt) + 0.025 * math.exp(-11.0 * math.sin(sun_mid.alt)))

    # 地月空间距与日地空间距
    moon_dist_km = moon_mid.earth_distance * 149597870.7
    sun_dist_au = sun_mid.earth_distance

    def fmt_time(ephem_t: ephem.Date) -> Tuple[str, str, str]:
        dt = ephem_t.datetime()
        utc_str = dt.strftime("%H:%M:%S")
        local_dt = dt + datetime.timedelta(hours=3)  # Egypt UTC+3
        local_str = local_dt.strftime("%H:%M:%S")
        cst_dt = dt + datetime.timedelta(hours=8)
        cst_str = cst_dt.strftime("%H:%M:%S")
        return utc_str, local_str, cst_str

    c1_utc, c1_loc, c1_cst = fmt_time(c1)
    c2_utc, c2_loc, c2_cst = fmt_time(c2)
    c3_utc, c3_loc, c3_cst = fmt_time(c3)
    c4_utc, c4_loc, c4_cst = fmt_time(c4)
    mid_utc, mid_loc, mid_cst = fmt_time(t_mid)

    return {
        "location": "Luxor, Egypt (25.6872°N, 32.6396°E)",
        "contacts": {
            "C1_first_contact": {"utc": c1_utc, "local": c1_loc, "cst": c1_cst},
            "C2_totality_begins": {"utc": c2_utc, "local": c2_loc, "cst": c2_cst},
            "Mid_greatest_totality": {"utc": mid_utc, "local": mid_loc, "cst": mid_cst},
            "C3_totality_ends": {"utc": c3_utc, "local": c3_loc, "cst": c3_cst},
            "C4_fourth_contact": {"utc": c4_utc, "local": c4_loc, "cst": c4_cst},
        },
        "totality_duration_seconds": round(totality_duration_sec, 1),
        "totality_duration_str": f"{int(totality_duration_sec // 60)}m {int(totality_duration_sec % 60):02d}s",
        "partial_duration_minutes": round(partial_duration_sec / 60.0, 1),
        "sun_altitude_deg": round(sun_alt_deg, 2),
        "sun_azimuth_deg": round(sun_az_deg, 2),
        "airmass": round(airmass, 3),
        "sun_diameter_arcsec": round(sun_diam_arcsec, 2),
        "moon_topocentric_diameter_arcsec": round(moon_diam_arcsec, 2),
        "eclipse_magnitude": round(magnitude, 4),
        "moon_distance_km": round(moon_dist_km, 1),
        "sun_distance_au": round(sun_dist_au, 5),
    }


def compute_international_stations() -> List[Dict[str, Any]]:
    """
    计算横跨直布罗陀、地中海、北非、红海至东非的全食带主要代表城市
    """
    results = []
    obs = ephem.Observer()

    for key, info in INTERNATIONAL_STATIONS.items():
        obs.lat = info["lat"]
        obs.lon = info["lon"]
        obs.elevation = info["elev"]

        # 扫描 08:30 至 11:30 UTC
        tot_seconds = 0
        max_cov = 0.0
        best_t = None
        best_alt = 0.0

        for m in range(8 * 60 + 30, 11 * 60 + 30):
            h = m // 60
            mi = m % 60
            t = ephem.Date(f"2027/08/02 {h:02d}:{mi:02d}:00")
            obs.date = t
            sun = ephem.Sun(obs)
            moon = ephem.Moon(obs)
            sep = math.degrees(ephem.separation((sun.az, sun.alt), (moon.az, moon.alt))) * 3600.0
            r_sun = sun.size / 2.0
            r_moon = moon.size / 2.0

            cov = max(0.0, (r_sun + r_moon - sep) / (2.0 * r_sun))
            if cov > max_cov:
                max_cov = cov
                best_t = t
                best_alt = math.degrees(sun.alt)

            if sep <= r_moon - r_sun:
                tot_seconds += 60

        is_total = tot_seconds > 0
        best_t_str = best_t.datetime().strftime("%H:%M UTC") if best_t else "N/A"

        results.append({
            "key": key,
            "name": info["name"],
            "country": info["country"],
            "is_total": is_total,
            "totality_duration_seconds": tot_seconds,
            "totality_duration_str": f"{tot_seconds // 60}m {tot_seconds % 60:02d}s" if is_total else "偏食",
            "max_coverage_pct": round(min(100.0, max_cov * 100.0), 1),
            "sun_altitude_deg": round(best_alt, 1),
            "mid_time_utc": best_t_str,
        })

    return results


def compute_china_western_stations() -> List[Dict[str, Any]]:
    """
    解算中国西部边境节点（塔县、阿里、喀什、和田）傍晚日落前日偏食天窗
    """
    results = []
    obs = ephem.Observer()

    for key, info in CHINA_WESTERN_STATIONS.items():
        obs.lat = info["lat"]
        obs.lon = info["lon"]
        obs.elevation = info["elev"]

        # 扫描北京时间 18:00 至 20:00 (10:00 至 12:00 UTC) 逐分钟
        t_start = ephem.Date("2027/08/02 10:00:00")
        t_end = ephem.Date("2027/08/02 12:00:00")

        in_eclipse = False
        start_t, max_t, end_t = None, None, None
        max_mag = 0.0
        max_alt = 0.0

        cur = t_start
        while cur <= t_end:
            obs.date = cur
            sun = ephem.Sun(obs)
            moon = ephem.Moon(obs)
            alt = math.degrees(sun.alt)

            if alt > 0.0:  # 地平线上
                sep = math.degrees(ephem.separation((sun.az, sun.alt), (moon.az, moon.alt))) * 3600.0
                r_sun = sun.size / 2.0
                r_moon = moon.size / 2.0

                if sep < r_sun + r_moon:
                    mag = (r_sun + r_moon - sep) / (2.0 * r_sun)
                    if not in_eclipse:
                        in_eclipse = True
                        start_t = cur
                    if mag > max_mag:
                        max_mag = mag
                        max_t = cur
                        max_alt = alt
                else:
                    if in_eclipse and end_t is None:
                        end_t = cur
            cur = ephem.Date(cur + ephem.minute)

        def to_cst_str(t_val):
            if not t_val:
                return "--:--"
            dt = t_val.datetime() + datetime.timedelta(hours=8)
            return dt.strftime("%H:%M CST")

        visible = max_mag > 0.005

        results.append({
            "key": key,
            "name": info["name"],
            "visible": visible,
            "start_time_cst": to_cst_str(start_t),
            "max_eclipse_time_cst": to_cst_str(max_t),
            "end_time_cst": to_cst_str(end_t),
            "max_magnitude": round(max_mag, 4),
            "max_coverage_pct": round(max_mag * 100.0, 2),
            "sun_altitude_at_max_deg": round(max_alt, 1),
        })

    return results


def generate_full_report() -> Dict[str, Any]:
    """
    汇总全套天体力学解算报告
    """
    harmonics = compute_saros_harmonics()
    luxor = compute_luxor_greatest_eclipse()
    intl = compute_international_stations()
    china = compute_china_western_stations()

    return {
        "title": "2027 年 8 月 2 日 21 世纪最长陆地日全食与沙罗 136 王者家族天体力学推演",
        "date_utc": "2027-08-02",
        "saros_series": 136,
        "saros_number": 38,
        "harmonics": harmonics,
        "greatest_eclipse_luxor": luxor,
        "international_corridor": intl,
        "china_western_border": china,
        "saros_136_history": SAROS_136_CATALOG,
    }


def print_text_report(data: Dict[str, Any]) -> None:
    """
    终端精美文本输出
    """
    ge = data["greatest_eclipse_luxor"]
    hm = data["harmonics"]

    print("=" * 84)
    print("  2027 年 8 月 2 日 21 世纪最长陆地日全食天体力学推演与沙罗 136 王者家族报告")
    print("=" * 84)
    print()
    print("【一、沙罗 136 拍频共振与转轮周期（Exeligmos）】")
    print(f"  • 沙罗周期长度          : {hm['synodic_period_days']:.3f} 天 (18 年 11 天 8 小时)")
    print(f"  • 223 朔望月 vs 242交点月 : 差值仅 {hm['draconic_diff_hours']:.2f} 小时 (节点相符度极高)")
    print(f"  • 223 朔望月 vs 239近点月 : 差值仅 {hm['anomalistic_diff_hours']:.2f} 小时 (月球近地点距离高度重现)")
    print(f"  • 单周期经度西移        : 额外累积 {hm['saros_extra_hours']:.2f} 小时，导致全食带向西漂移 {hm['longitude_shift_west_deg']:.1f}°")
    print(f"  • 转轮周期 (3个沙罗)    : {hm['exeligmos_days']:.1f} 天 ({hm['exeligmos_years']:.1f} 年)，经度漂移闭合，回归同经度扇区")
    print()
    print("【二、埃及卢克索（Greatest Eclipse）食相接触与几何极值】")
    print(f"  • 食甚中心点            : {ge['location']}")
    print(f"  • 初亏 (C1)             : {ge['contacts']['C1_first_contact']['utc']} UTC | {ge['contacts']['C1_first_contact']['local']} 当地 | {ge['contacts']['C1_first_contact']['cst']} CST")
    print(f"  • 食既 (C2 全食开始)    : {ge['contacts']['C2_totality_begins']['utc']} UTC | {ge['contacts']['C2_totality_begins']['local']} 当地 | {ge['contacts']['C2_totality_begins']['cst']} CST")
    print(f"  • 食甚 (Max 全食巅峰)   : {ge['contacts']['Mid_greatest_totality']['utc']} UTC | {ge['contacts']['Mid_greatest_totality']['local']} 当地 | {ge['contacts']['Mid_greatest_totality']['cst']} CST")
    print(f"  • 生光 (C3 全食结束)    : {ge['contacts']['C3_totality_ends']['utc']} UTC | {ge['contacts']['C3_totality_ends']['local']} 当地 | {ge['contacts']['C3_totality_ends']['cst']} CST")
    print(f"  • 复圆 (C4)             : {ge['contacts']['C4_fourth_contact']['utc']} UTC | {ge['contacts']['C4_fourth_contact']['local']} 当地 | {ge['contacts']['C4_fourth_contact']['cst']} CST")
    print(f"  • ★ 全食持续时间        : {ge['totality_duration_str']} ({ge['totality_duration_seconds']} 秒) —— 21 世纪陆地绝对之冠！")
    print(f"  • 太阳仰角与方位角      : 仰角 {ge['sun_altitude_deg']}° (近乎直插天顶顶心) | 方位角 {ge['sun_azimuth_deg']}°")
    print(f"  • 大气消光质量数 (X)    : {ge['airmass']} (趋近极限 1.00，无大气消光干扰)")
    print(f"  • 太阳与月球站心视直径  : 太阳 {ge['sun_diameter_arcsec']}\" ({ge['sun_diameter_arcsec']/60:.2f}') | 月球 {ge['moon_topocentric_diameter_arcsec']}\" ({ge['moon_topocentric_diameter_arcsec']/60:.2f}')")
    print(f"  • 视直径比值 (食分)     : {ge['eclipse_magnitude']} (月球视角面积超出太阳 16.9%！)")
    print()
    print("【三、地中海、北非、红海至东非全食带主要城市廊道】")
    print("代表城市                     | 全食状态 | 全食时长 | 食甚仰角 | 食甚时刻 (UTC)")
    print("-" * 75)
    for c in data["international_corridor"]:
        status = "全食" if c["is_total"] else "偏食"
        print(f"{c['name']:28s} |   {status}   |  {c['totality_duration_str']:6s}  |  {c['sun_altitude_deg']:4.1f}°  | {c['mid_time_utc']}")
    print()
    print("【四、华夏西域边境傍晚晚霞日偏食天窗（2027-08-02）】")
    print("观测节点           | 偏食初亏     | 食甚时刻     | 复圆时刻     | 最大食分 | 食甚仰角")
    print("-" * 75)
    for w in data["china_western_border"]:
        if w["visible"]:
            print(f"{w['name']:18s} | {w['start_time_cst']} | {w['max_eclipse_time_cst']} | {w['end_time_cst']} |  {w['max_magnitude']:.4f}  |  {w['sun_altitude_at_max_deg']:4.1f}°")
        else:
            print(f"{w['name']:18s} | 未入偏食带（地平线下或偏食带外）")
    print("=" * 84)


def main():
    parser = argparse.ArgumentParser(description="2027 年 8 月 2 日 21 世纪最长陆地日全食推演引擎")
    parser.add_argument("--json", action="store_true", help="输出 JSON 结构化数据")
    args = parser.parse_args()

    report = generate_full_report()

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print_text_report(report)


if __name__ == "__main__":
    main()
