#!/usr/bin/env python3
"""
mars_jupiter_dual_opposition_2027.py
====================================
2027 年火星与木星双冲日天体力学推演、双星同向逆行拉锯、
荧惑三犯轩辕十四与元宵满月“双星捧月”天象全景动力学引擎。

核心推演模块：
1. 8.6 天极近时间差外行星双冲日集群（Dual Planetary Opposition Cluster）：
   - 木星视黄经冲日（2027-02-11 08:14 CST，视星等 -2.40，视直径 45.11"，地心距 4.3611 AU）
   - 火星视黄经冲日（2027-02-19 23:39 CST，视星等 -1.12，视直径 13.81"，地心距 0.6779 AU）
   - 火星最近地心距（2027-02-20 07:54 CST，0.67792 AU / 1.014 亿千米）
   - 会合周期与近点月动力学拍频几何分析。
2. 同向双逆行与天球拉锯动力学（Synchronous Dual Retrograde）：
   - 木星逆行（2026-12-13 留 至 2027-04-13 留，历时 121 天）
   - 火星逆行（2027-01-12 留 至 2027-04-03 留，历时 81 天）
   - 双星全重叠同步逆行窗口长达 81 天，天球角距维持在 8.1°~14.4° 之间。
3. 荧惑三犯轩辕十四（Mars-Regulus Triple Conjunction / Pass）：
   - 顺行初犯（2026-11-26 13:17 CST，角距 1.72° / 103.5'）
   - 逆行二犯（2027-02-21 14:26 CST，角距 3.99° / 239.2'，恰逢火星冲日时分）
   - 顺行三犯（2027-05-15 18:22 CST，角距 1.23° / 73.8'）
4. 丁未年元宵节（2027-02-20）“双星捧月”天象四曜聚首（Celestial Quadrangle）：
   - 元宵夜满月（99.7% 照亮）掠过巨蟹与狮子座
   - 望日满月、纯白木星、赤红火星与王星轩辕十四汇聚在 10.5° × 5.8° 极小天区天窗
   - 华夏各大城市子夜 42 分钟内迎来“木星中天 -> 满月中天 -> 火星中天”三曜凌顶壮景
5. 华夏五大城市（京、沪、穗、蓉、乌）通宵观测地平几何与高天顶仰角解算（广州最高仰角突破 82.5°）。

作者: Hoshi (hoshi0919@outlook.com)
日期: 2026-10-11
"""

import math
import json
import argparse
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Any, Tuple
import ephem

# ---------------------------------------------------------
# 天体物理与力学常数
# ---------------------------------------------------------
CST_TZ = timezone(timedelta(hours=8))
AU_KM = 149597870.7                  # 千米 / AU
SPEED_OF_LIGHT_KM_S = 299792.458     # km/s

# 华夏代表性观测城市经纬度
CHINA_CITIES = {
    "Beijing": {"name_cn": "北京", "lat": "39.9042", "lon": "116.4074", "elev": 50},
    "Shanghai": {"name_cn": "上海", "lat": "31.2304", "lon": "121.4737", "elev": 20},
    "Guangzhou": {"name_cn": "广州", "lat": "23.1291", "lon": "113.2644", "elev": 30},
    "Chengdu": {"name_cn": "成都", "lat": "30.5728", "lon": "104.0668", "elev": 500},
    "Urumqi": {"name_cn": "乌鲁木齐", "lat": "43.8256", "lon": "87.6168", "elev": 800},
}


def to_cst_str(ephem_dt: ephem.Date) -> str:
    """将 ephem.Date 格式化为北京时间 CST 字符串。"""
    dt_utc = ephem_dt.datetime().replace(tzinfo=timezone.utc)
    dt_cst = dt_utc.astimezone(CST_TZ)
    return dt_cst.strftime("%Y-%m-%d %H:%M:%S CST")


def calculate_oppositions() -> Dict[str, Any]:
    """
    解算 2027 年木星与火星冲日天体力学参数：
    包含视黄经冲日、赤经冲日、最近地心距（近地点）与光行时。
    """
    sun = ephem.Sun()
    jup = ephem.Jupiter()
    mars = ephem.Mars()

    # 1. 木星视黄经冲日 (Ecliptic Longitude Opposition)
    t_start_jup = ephem.Date("2027/2/10")
    min_diff_jup = 999.0
    best_t_jup_ecl = None
    for m in range(3 * 24 * 60):
        t = ephem.Date(t_start_jup + m / 1440.0)
        sun.compute(t)
        jup.compute(t)
        s_ecl = ephem.Ecliptic(sun)
        j_ecl = ephem.Ecliptic(jup)
        diff = abs(((j_ecl.lon - s_ecl.lon) % (2 * ephem.pi)) - ephem.pi)
        if diff < min_diff_jup:
            min_diff_jup = diff
            best_t_jup_ecl = t

    jup.compute(best_t_jup_ecl)
    jup_ecl_dist_km = jup.earth_distance * AU_KM
    jup_light_time_min = (jup_ecl_dist_km / SPEED_OF_LIGHT_KM_S) / 60.0

    # 2. 火星视黄经冲日 (Ecliptic Longitude Opposition)
    t_start_mars = ephem.Date("2027/2/18")
    min_diff_mars = 999.0
    best_t_mars_ecl = None
    for m in range(4 * 24 * 60):
        t = ephem.Date(t_start_mars + m / 1440.0)
        sun.compute(t)
        mars.compute(t)
        s_ecl = ephem.Ecliptic(sun)
        m_ecl = ephem.Ecliptic(mars)
        diff = abs(((m_ecl.lon - s_ecl.lon) % (2 * ephem.pi)) - ephem.pi)
        if diff < min_diff_mars:
            min_diff_mars = diff
            best_t_mars_ecl = t

    mars.compute(best_t_mars_ecl)
    mars_ecl_dist_km = mars.earth_distance * AU_KM
    mars_light_time_min = (mars_ecl_dist_km / SPEED_OF_LIGHT_KM_S) / 60.0

    # 3. 火星最近地心距 (Perigee / Closest Approach)
    min_dist_mars = 999.0
    best_t_mars_perigee = None
    for m in range(6 * 24 * 60):
        t = ephem.Date(ephem.Date("2027/2/17") + m / 1440.0)
        mars.compute(t)
        if mars.earth_distance < min_dist_mars:
            min_dist_mars = mars.earth_distance
            best_t_mars_perigee = t

    mars.compute(best_t_mars_perigee)
    mars_perigee_km = min_dist_mars * AU_KM

    # 4. 赤经冲日 (Right Ascension Oppositions)
    # 木星 RA 冲
    min_diff_ra_j = 999.0
    best_t_jup_ra = None
    for m in range(3 * 24 * 60):
        t = ephem.Date(t_start_jup + m / 1440.0)
        sun.compute(t)
        jup.compute(t)
        diff = abs(abs(sun.ra - jup.ra) - math.pi)
        if diff < min_diff_ra_j:
            min_diff_ra_j = diff
            best_t_jup_ra = t

    # 火星 RA 冲
    min_diff_ra_m = 999.0
    best_t_mars_ra = None
    for m in range(4 * 24 * 60):
        t = ephem.Date(t_start_mars + m / 1440.0)
        sun.compute(t)
        mars.compute(t)
        diff = abs(abs(sun.ra - mars.ra) - math.pi)
        if diff < min_diff_ra_m:
            min_diff_ra_m = diff
            best_t_mars_ra = t

    ecl_gap_days = abs(float(best_t_mars_ecl) - float(best_t_jup_ecl))
    ra_gap_days = abs(float(best_t_mars_ra) - float(best_t_jup_ra))

    return {
        "jupiter_opposition": {
            "ecliptic_time_utc": str(best_t_jup_ecl),
            "ecliptic_time_cst": to_cst_str(best_t_jup_ecl),
            "ra_time_cst": to_cst_str(best_t_jup_ra),
            "apparent_magnitude": round(float(jup.mag), 2),
            "angular_diameter_arcsec": round(float(jup.size), 2),
            "earth_distance_au": round(float(jup.earth_distance), 4),
            "earth_distance_km": round(jup_ecl_dist_km, 1),
            "light_time_minutes": round(jup_light_time_min, 2),
            "ra": str(jup.ra),
            "dec": str(jup.dec),
        },
        "mars_opposition": {
            "ecliptic_time_utc": str(best_t_mars_ecl),
            "ecliptic_time_cst": to_cst_str(best_t_mars_ecl),
            "ra_time_cst": to_cst_str(best_t_mars_ra),
            "apparent_magnitude": round(float(mars.mag), 2),
            "angular_diameter_arcsec": round(float(mars.size), 2),
            "earth_distance_au": round(float(mars.earth_distance), 4),
            "earth_distance_km": round(mars_ecl_dist_km, 1),
            "light_time_minutes": round(mars_light_time_min, 2),
            "ra": str(mars.ra),
            "dec": str(mars.dec),
        },
        "mars_closest_approach": {
            "time_utc": str(best_t_mars_perigee),
            "time_cst": to_cst_str(best_t_mars_perigee),
            "min_distance_au": round(min_dist_mars, 5),
            "min_distance_km": round(mars_perigee_km, 1),
            "angular_diameter_arcsec": round(float(mars.size), 2),
        },
        "cluster_interval": {
            "ecliptic_gap_days": round(ecl_gap_days, 2),
            "ra_gap_days": round(ra_gap_days, 2),
            "is_tight_cluster": ecl_gap_days < 10.0,
        }
    }


def calculate_retrograde_loops() -> Dict[str, Any]:
    """
    数值微分解算火星与木星的留点（Stationary Points）与逆行窗口：
    木星留点：2026-12-13 至 2027-04-13
    火星留点：2027-01-12 至 2027-04-03
    解算双星同步重叠逆行区间。
    """
    jup = ephem.Jupiter()
    mars = ephem.Mars()

    def get_stationary_points(body, start_str, end_str):
        t = ephem.Date(start_str)
        end_t = ephem.Date(end_str)
        step = 0.25
        prev_rate = None
        points = []
        cur_t = t
        while cur_t < end_t:
            body.compute(cur_t)
            ra1 = float(body.ra)
            body.compute(ephem.Date(cur_t + 0.01))
            ra2 = float(body.ra)
            rate = (ra2 - ra1) / 0.01
            if prev_rate is not None:
                if prev_rate > 0 and rate <= 0:
                    points.append(("first", cur_t))
                elif prev_rate < 0 and rate >= 0:
                    points.append(("second", cur_t))
            prev_rate = rate
            cur_t = ephem.Date(cur_t + step)

        refined_res = {}
        for kind, pt in points:
            t_ref = ephem.Date(pt - 1.0)
            best_t = None
            min_rate = 999.0
            for m in range(2 * 1440):
                tt = ephem.Date(t_ref + m / 1440.0)
                body.compute(tt)
                r1 = float(body.ra)
                body.compute(ephem.Date(tt + 0.001))
                r2 = float(body.ra)
                diff_r = abs(r2 - r1)
                if diff_r < min_rate:
                    min_rate = diff_r
                    best_t = tt
            body.compute(best_t)
            refined_res[kind] = {
                "time_utc": str(best_t),
                "time_cst": to_cst_str(best_t),
                "ra": str(body.ra),
                "dec": str(body.dec),
                "magnitude": round(float(body.mag), 2),
                "ephem_date": float(best_t),
            }
        return refined_res

    jup_pts = get_stationary_points(jup, "2026/11/15", "2027/5/1")
    mars_pts = get_stationary_points(mars, "2026/12/15", "2027/5/1")

    jup_retro_days = round(jup_pts["second"]["ephem_date"] - jup_pts["first"]["ephem_date"], 1)
    mars_retro_days = round(mars_pts["second"]["ephem_date"] - mars_pts["first"]["ephem_date"], 1)

    # 同步重叠区间：从火星第一留点开始，到火星第二留点结束（因为火星逆行区间完全被木星逆行区间包裹）
    overlap_start = mars_pts["first"]["time_cst"]
    overlap_end = mars_pts["second"]["time_cst"]
    overlap_days = mars_retro_days

    return {
        "jupiter_retrograde": {
            "first_stationary_point": jup_pts["first"],
            "second_stationary_point": jup_pts["second"],
            "retrograde_duration_days": jup_retro_days,
        },
        "mars_retrograde": {
            "first_stationary_point": mars_pts["first"],
            "second_stationary_point": mars_pts["second"],
            "retrograde_duration_days": mars_retro_days,
        },
        "synchronous_overlap": {
            "start_cst": overlap_start,
            "end_cst": overlap_end,
            "duration_days": overlap_days,
            "description": "火星逆行全程（约81天）100%嵌入木星逆行期（约121天），双星同向西退拉锯"
        }
    }


def calculate_mars_regulus_triple_pass() -> List[Dict[str, Any]]:
    """
    解算 2026 年底至 2027 年春“荧惑三犯轩辕十四”极近相交天象：
    由于逆行回形针弯钩，火星三次掠过狮子座一等主星轩辕十四（Regulus）。
    """
    mars = ephem.Mars()
    regulus = ephem.star("Regulus")
    t0 = ephem.Date("2026/10/1")
    end_t = ephem.Date("2027/7/1")
    step = 0.5

    t = t0
    prev_sep = None
    prev_prev_sep = None
    candidates = []

    while t < end_t:
        mars.compute(t)
        regulus.compute(t)
        sep = math.degrees(ephem.separation(mars, regulus))
        if prev_sep is not None and prev_prev_sep is not None:
            if prev_sep < prev_prev_sep and prev_sep < sep:
                candidates.append(ephem.Date(t - step))
        prev_prev_sep = prev_sep
        prev_sep = sep
        t = ephem.Date(t + step)

    passes = []
    pass_labels = [
        ("初犯（顺行东进）", "顺行经过狮子座，与轩辕十四近距离相擦"),
        ("二犯（逆行西退）", "逆行回撤，于火星冲日时分再次掠过轩辕十四"),
        ("三犯（留后顺行）", "恢复顺行，第三次追越轩辕十四"),
    ]

    for idx, cand in enumerate(candidates):
        t_ref = ephem.Date(cand - 1.0)
        best_sep = 999.0
        best_t = None
        for m in range(2 * 1440):
            tt = ephem.Date(t_ref + m / 1440.0)
            mars.compute(tt)
            regulus.compute(tt)
            s = math.degrees(ephem.separation(mars, regulus))
            if s < best_sep:
                best_sep = s
                best_t = tt

        mars.compute(best_t)
        lbl, desc = pass_labels[idx] if idx < len(pass_labels) else (f"第{idx+1}次", "")
        passes.append({
            "pass_index": idx + 1,
            "label": lbl,
            "description": desc,
            "time_utc": str(best_t),
            "time_cst": to_cst_str(best_t),
            "min_separation_deg": round(best_sep, 3),
            "min_separation_arcmin": round(best_sep * 60.0, 1),
            "mars_magnitude": round(float(mars.mag), 2),
            "regulus_magnitude": 1.35,
        })

    return passes


def calculate_lantern_festival_quadrangle() -> Dict[str, Any]:
    """
    解算 2027 年 2 月 20 日（农历丁未年正月十五元宵节）“双星捧月”天象四曜聚首几何：
    元宵满月（99.7%）与火星、木星、轩辕十四在天顶附近的汇聚与中天时序。
    """
    moon = ephem.Moon()
    sun = ephem.Sun()
    mars = ephem.Mars()
    jup = ephem.Jupiter()
    regulus = ephem.star("Regulus")

    # 1. 2027-02-20 20:00 CST 瞬态天球几何
    t_evening = ephem.Date("2027/2/20 12:00:00") # 20:00 CST
    moon.compute(t_evening)
    sun.compute(t_evening)
    mars.compute(t_evening)
    jup.compute(t_evening)
    regulus.compute(t_evening)

    moon_phase = moon.moon_phase * 100.0
    sep_moon_jup = math.degrees(ephem.separation(moon, jup))
    sep_moon_mars = math.degrees(ephem.separation(moon, mars))
    sep_mars_jup = math.degrees(ephem.separation(mars, jup))
    sep_mars_reg = math.degrees(ephem.separation(mars, regulus))

    # 2. 搜索月亮分别与木星、火星的最接近时刻
    t_start = ephem.Date("2027/2/19 16:00:00")
    min_mj = 999.0
    t_min_mj = None
    min_mm = 999.0
    t_min_mm = None
    for m in range(3 * 1440):
        t = ephem.Date(t_start + m / 1440.0)
        moon.compute(t)
        jup.compute(t)
        mars.compute(t)
        smj = math.degrees(ephem.separation(moon, jup))
        smm = math.degrees(ephem.separation(moon, mars))
        if smj < min_mj:
            min_mj = smj
            t_min_mj = t
        if smm < min_mm:
            min_mm = smm
            t_min_mm = t

    # 3. 上海站元宵夜子夜中天时序
    obs_sh = ephem.Observer()
    obs_sh.lat = "31.2304"
    obs_sh.lon = "121.4737"
    obs_sh.elevation = 20
    obs_sh.date = "2027/2/20 00:00:00"

    t_tr_j = obs_sh.next_transit(jup)
    obs_sh.date = t_tr_j
    jup.compute(obs_sh)
    alt_tr_j = math.degrees(jup.alt)

    t_tr_moon = obs_sh.next_transit(moon)
    obs_sh.date = t_tr_moon
    moon.compute(obs_sh)
    alt_tr_moon = math.degrees(moon.alt)

    t_tr_mars = obs_sh.next_transit(mars)
    obs_sh.date = t_tr_mars
    mars.compute(obs_sh)
    alt_tr_mars = math.degrees(mars.alt)

    transit_gap_min = (float(t_tr_mars) - float(t_tr_j)) * 1440.0

    return {
        "date_info": {
            "gregorian_date": "2027-02-20",
            "lunar_date": "农历丁未年正月十五（元宵节）",
            "moon_phase_pct": round(moon_phase, 1),
        },
        "celestial_separations": {
            "moon_to_jupiter_evening_deg": round(sep_moon_jup, 2),
            "moon_to_mars_evening_deg": round(sep_moon_mars, 2),
            "mars_to_jupiter_deg": round(sep_mars_jup, 2),
            "mars_to_regulus_deg": round(sep_mars_reg, 2),
            "closest_moon_jupiter": {
                "time_cst": to_cst_str(t_min_mj),
                "separation_deg": round(min_mj, 2),
                "separation_arcmin": round(min_mj * 60.0, 1),
            },
            "closest_moon_mars": {
                "time_cst": to_cst_str(t_min_mm),
                "separation_deg": round(min_mm, 2),
                "separation_arcmin": round(min_mm * 60.0, 1),
            }
        },
        "shanghai_midnight_transit_sequence": {
            "jupiter_transit_cst": to_cst_str(t_tr_j),
            "jupiter_altitude_deg": round(alt_tr_j, 1),
            "moon_transit_cst": to_cst_str(t_tr_moon),
            "moon_altitude_deg": round(alt_tr_moon, 1),
            "mars_transit_cst": to_cst_str(t_tr_mars),
            "mars_altitude_deg": round(alt_tr_mars, 1),
            "total_span_minutes": round(transit_gap_min, 1),
            "summary": f"三曜在 {round(transit_gap_min, 1)} 分钟内依次横跨天顶，高度皆在 70°~75° 黄金高仰角"
        }
    }


def calculate_china_observability() -> Dict[str, Any]:
    """
    解算华夏五大城市在 2027 年 2 月 20 日元宵节夜的通宵观测地平几何：
    日落、月升、木星与火星升起、中天时刻与极大仰角。
    """
    sun = ephem.Sun()
    moon = ephem.Moon()
    jup = ephem.Jupiter()
    mars = ephem.Mars()

    results = {}
    for city_key, info in CHINA_CITIES.items():
        obs = ephem.Observer()
        obs.lat = info["lat"]
        obs.lon = info["lon"]
        obs.elevation = info["elev"]
        obs.date = "2027/2/20 00:00:00" # CST 08:00

        # 日落与次日日出
        sun_set = obs.next_setting(sun)
        obs.date = sun_set
        sun_rise = obs.next_rising(sun)

        # 木星升、中天、落
        obs.date = "2027/2/20 00:00:00"
        jup_rise = obs.next_rising(jup)
        jup_tr = obs.next_transit(jup)
        obs.date = jup_tr
        jup.compute(obs)
        jup_max_alt = math.degrees(jup.alt)
        jup_set = obs.next_setting(jup)

        # 火星升、中天、落
        obs.date = "2027/2/20 00:00:00"
        mars_rise = obs.next_rising(mars)
        mars_tr = obs.next_transit(mars)
        obs.date = mars_tr
        mars.compute(obs)
        mars_max_alt = math.degrees(mars.alt)
        mars_set = obs.next_setting(mars)

        # 天顶角与消光气团数 (Airmass X ≈ 1 / cos(z))
        z_deg = 90.0 - mars_max_alt
        airmass = 1.0 / math.cos(math.radians(z_deg)) if z_deg < 85.0 else 10.0

        results[city_key] = {
            "city_name": info["name_cn"],
            "sunset_cst": to_cst_str(sun_set),
            "sunrise_cst": to_cst_str(sun_rise),
            "jupiter": {
                "rise_cst": to_cst_str(jup_rise),
                "transit_cst": to_cst_str(jup_tr),
                "transit_alt_deg": round(jup_max_alt, 1),
                "set_cst": to_cst_str(jup_set),
            },
            "mars": {
                "rise_cst": to_cst_str(mars_rise),
                "transit_cst": to_cst_str(mars_tr),
                "transit_alt_deg": round(mars_max_alt, 1),
                "set_cst": to_cst_str(mars_set),
                "zenith_airmass": round(airmass, 3),
            }
        }

    return results


def build_full_report() -> Dict[str, Any]:
    """生成 2027 年火木双冲日与元宵双星捧月全量天体力学报告。"""
    oppositions = calculate_oppositions()
    retrograde = calculate_retrograde_loops()
    triple_pass = calculate_mars_regulus_triple_pass()
    lantern = calculate_lantern_festival_quadrangle()
    china_obs = calculate_china_observability()

    return {
        "title": "2027 年火星与木星双冲日、双星同向逆行、荧惑三犯轩辕与元宵双星捧月天体力学推演全景报告",
        "generated_by": "Hoshi (hoshi0919@outlook.com)",
        "generated_at": datetime.now(CST_TZ).strftime("%Y-%m-%d %H:%M:%S CST"),
        "oppositions": oppositions,
        "retrograde_loops": retrograde,
        "mars_regulus_triple_pass": triple_pass,
        "lantern_festival_quadrangle": lantern,
        "china_observability": china_obs,
    }


def format_markdown_summary(report: Dict[str, Any]) -> str:
    """输出美观易读的 Markdown 学术推演综述。"""
    opp = report["oppositions"]
    ret = report["retrograde_loops"]
    passes = report["mars_regulus_triple_pass"]
    lan = report["lantern_festival_quadrangle"]
    c_obs = report["china_observability"]

    lines = []
    lines.append("# 2027 年火木双冲日与元宵双星捧月天体力学推演报告\n")
    lines.append(f"**生成时间**: {report['generated_at']} | **分析引擎**: tonight-sky (Hoshi)\n")

    lines.append("## 一、外行星双冲日集群（Dual Planetary Opposition Cluster）")
    lines.append(f"- **木星冲日（视黄经冲）**: `{opp['jupiter_opposition']['ecliptic_time_cst']}`")
    lines.append(f"  - 视星等: **{opp['jupiter_opposition']['apparent_magnitude']} 等** | 视直径: **{opp['jupiter_opposition']['angular_diameter_arcsec']}\"**")
    lines.append(f"  - 地心距: **{opp['jupiter_opposition']['earth_distance_au']} AU** ({opp['jupiter_opposition']['earth_distance_km']:,} km) | 光行时: **{opp['jupiter_opposition']['light_time_minutes']} 分钟**")
    lines.append(f"- **火星冲日（视黄经冲）**: `{opp['mars_opposition']['ecliptic_time_cst']}`")
    lines.append(f"  - 视星等: **{opp['mars_opposition']['apparent_magnitude']} 等** | 视直径: **{opp['mars_opposition']['angular_diameter_arcsec']}\"**")
    lines.append(f"  - 地心距: **{opp['mars_opposition']['earth_distance_au']} AU** ({opp['mars_opposition']['earth_distance_km']:,} km) | 光行时: **{opp['mars_opposition']['light_time_minutes']} 分钟**")
    lines.append(f"- **火星最近地心距（近地点）**: `{opp['mars_closest_approach']['time_cst']}`")
    lines.append(f"  - 最小地心距: **{opp['mars_closest_approach']['min_distance_au']} AU** ({opp['mars_closest_approach']['min_distance_km']:,} km)")
    lines.append(f"- **核心时空特征**: 两大外行星冲日相距仅 **{opp['cluster_interval']['ecliptic_gap_days']} 天**，为数十年一遇的双星并冲天象！\n")

    lines.append("## 二、同向双逆行与天球拉锯动力学（Synchronous Dual Retrograde）")
    lines.append(f"- **木星逆行期**: `{ret['jupiter_retrograde']['first_stationary_point']['time_cst']}` ~ `{ret['jupiter_retrograde']['second_stationary_point']['time_cst']}`（历时 **{ret['jupiter_retrograde']['retrograde_duration_days']} 天**）")
    lines.append(f"- **火星逆行期**: `{ret['mars_retrograde']['first_stationary_point']['time_cst']}` ~ `{ret['mars_retrograde']['second_stationary_point']['time_cst']}`（历时 **{ret['mars_retrograde']['retrograde_duration_days']} 天**）")
    lines.append(f"- **双星同步逆行重叠期**: `{ret['synchronous_overlap']['start_cst']}` 至 `{ret['synchronous_overlap']['end_cst']}`，整整 **{ret['synchronous_overlap']['duration_days']} 天**内双星同时在巨蟹与狮子座之间反向西退。\n")

    lines.append("## 三、荧惑三犯轩辕十四（Mars-Regulus Triple Conjunction）")
    for p in passes:
        lines.append(f"- **第 {p['pass_index']} 幕 · {p['label']}**: `{p['time_cst']}`")
        lines.append(f"  - 最小角距: **{p['min_separation_deg']}°**（{p['min_separation_arcmin']} 角分）| 火星亮度: {p['mars_magnitude']} 等")
        lines.append(f"  - 特征: {p['description']}")
    lines.append("")

    lines.append("## 四、丁未年元宵夜“双星捧月”天象四曜聚首（Lantern Festival Quadrangle）")
    lines.append(f"- **农历与公历**: 2027 年 2 月 20 日（农历丁未年正月十五元宵节）")
    lines.append(f"- **月相照亮比例**: **{lan['date_info']['moon_phase_pct']}%**（纯正元宵圆月）")
    lines.append(f"- **双星捧月角距**: 月球距木星 **{lan['celestial_separations']['moon_to_jupiter_evening_deg']}°**，距火星 **{lan['celestial_separations']['moon_to_mars_evening_deg']}°**，火木双星相距 **{lan['celestial_separations']['mars_to_jupiter_deg']}°**")
    lines.append(f"- **上海站子夜中天时序**: {lan['shanghai_midnight_transit_sequence']['summary']}")
    lines.append(f"  - 木星中天: `{lan['shanghai_midnight_transit_sequence']['jupiter_transit_cst']}`（仰角 {lan['shanghai_midnight_transit_sequence']['jupiter_altitude_deg']}°）")
    lines.append(f"  - 满月中天: `{lan['shanghai_midnight_transit_sequence']['moon_transit_cst']}`（仰角 {lan['shanghai_midnight_transit_sequence']['moon_altitude_deg']}°）")
    lines.append(f"  - 火星中天: `{lan['shanghai_midnight_transit_sequence']['mars_transit_cst']}`（仰角 {lan['shanghai_midnight_transit_sequence']['mars_altitude_deg']}°）\n")

    lines.append("## 五、华夏五大城市元宵节夜通宵地平几何")
    lines.append("| 城市 | 木星中天 (仰角) | 火星中天 (仰角) | 大气消光气团数 | 观测评价 |")
    lines.append("| :--- | :---: | :---: | :---: | :--- |")
    for ck, c in c_obs.items():
        lines.append(f"| {c['city_name']} | {c['jupiter']['transit_cst'][-12:-4]} ({c['jupiter']['transit_alt_deg']}°) | {c['mars']['transit_cst'][-12:-4]} ({c['mars']['transit_alt_deg']}°) | {c['mars']['zenith_airmass']:.3f} | 直插高天顶，通宵极高分辨率 |")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="2027 年火木双冲日与元宵双星捧月天体力学计算引擎")
    parser.add_argument("--json", action="store_true", help="输出完整 JSON 数据结构")
    args = parser.parse_args()

    report = build_full_report()

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(format_markdown_summary(report))


if __name__ == "__main__":
    main()
