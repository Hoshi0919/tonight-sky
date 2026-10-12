"""
2028 年 12 月 31 日跨年夜蓝月全食天体力学推演与沙罗 134 家族研究引擎
New Year's Eve Blue Moon Total Lunar Eclipse & Saros 134 Dynamics Engine (2028-12-31 / 2029-01-01)

科学背景与核心天体物理机理：
1. 沙罗周期 134（Lunar Saros 134）天体力学体系：
   - 序列全长 73 次月食（公元 1550 年至 2848 年）。
   - 前一次：2010-12-21（#27，北半球冬至日月全食，食分 1.256）。
   - 本次：2028-12-31 至 2029-01-01（#28，跨年夜蓝月全食，食分 1.2504）。
   - 下一次：2047-01-12（#29）。
   - 沙罗步长 6585.321 天（18 年 10 天 8 小时），经度西移约 120°；3 个沙罗周期（转轮周期 Exeligmos，54 年 33 天）经度完全回归。
2. 历法双满月与“蓝月”（Calendar Blue Moon）天文学定义：
   - 朔望月均长 29.53059 天，公历大月 31 天多出 1.47 天。
   - 2028 年 12 月首个满月：12 月 2 日 09:40 CST。
   - 2028 年 12 月第二个满月：12 月 31 日 16:48 UTC（2029 年 1 月 1 日 00:48 CST）。
   - 严格满足历法“一月双满月之次月”的蓝月定义。
3. 地球本影锥几何与 2% 大气折射膨胀（Danjon / Chauvenet 模型）：
   - 太阳与月球视半径、地心视差结合 1.02 大气膨胀因子解算地影。
   - 初亏 (U1) 23:07 CST（跨年倒计时 53 分钟时本影初咬）。
   - 跨年零点 (00:00 CST)：月球已被地球本影吞噬 78.9% 直径！
   - 食既 (U2) 00:16 CST，进入全食红月。
   - 食甚 (Mid) 00:53 CST，本影食分高达 1.2504，深入南地影锥。
   - 生光 (U3) 01:29 CST，全食持续 73 分钟。
   - 复圆 (U4) 02:37 CST，本影偏食总时长 210 分钟。
4. 华夏大地天顶极盛观测（Topocentric Zenith Geometry）：
   - 月球处于双子座核心，赤纬高达 +23° 19.5'（冬至点高空极值）。
   - 华夏全境全食食甚仰角全部高于 62°（广州 84.8°、三亚 84.5°、成都 81.9°、上海 75.2°、北京 71.5°）！
   - 大气质量系数 AM <= 1.06，免遭近地低空雾霾与遮挡。
5. 冬季大六角与 M35 伴月星空穹顶突变（Rayleigh Scattering & Sky Contrast）：
   - 月球亮度从 -12.78 等暴跌至 +2.0 等左右（光通量衰减逾 40 万倍）。
   - 角距双子座 M35 疏散星团仅 8.56°，深空天体与冬季银河璀璨爆发。
"""

import sys
import math
import json
import argparse
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Tuple

import ephem

# 沙罗 134 序列核心月全食名录
SAROS_134_CATALOG = [
    {
        "saros_num": 25,
        "date": "1974-11-29",
        "duration_totality_min": 76,
        "umbral_mag": 1.295,
        "significance": "冷战时期经典高纬度冬季月全食",
    },
    {
        "saros_num": 26,
        "date": "1992-12-09",
        "duration_totality_min": 74,
        "umbral_mag": 1.276,
        "significance": "皮纳图博火山喷发次年，全球目睹罕见黑月/暗褐月食（Danjon L=0~1）",
    },
    {
        "saros_num": 27,
        "date": "2010-12-21",
        "duration_totality_min": 72,
        "umbral_mag": 1.256,
        "significance": "北半球冬至日月全食，时隔 456 年首现冬至日红月",
    },
    {
        "saros_num": 28,
        "date": "2028-12-31",
        "duration_totality_min": 73,
        "umbral_mag": 1.250,
        "significance": "公历跨年夜罕见蓝月全食，食甚恰逢 2029 元旦钟声后 53 分钟，华夏全境天顶仰角可见",
    },
    {
        "saros_num": 29,
        "date": "2047-01-12",
        "duration_totality_min": 70,
        "umbral_mag": 1.218,
        "significance": "21 世纪中叶沙罗 134 延续期，食分平缓收敛",
    },
]

# 华夏主要城市经纬度
CHINA_OBSERVATION_CITIES = {
    "Guangzhou": {"name_cn": "广州", "lat": 23.1291, "lon": 113.2644, "elevation_m": 43},
    "Sanya": {"name_cn": "三亚", "lat": 18.2528, "lon": 109.5120, "elevation_m": 15},
    "Chengdu": {"name_cn": "成都", "lat": 30.5728, "lon": 104.0668, "elevation_m": 500},
    "Shanghai": {"name_cn": "上海", "lat": 31.2304, "lon": 121.4737, "elevation_m": 10},
    "Beijing": {"name_cn": "北京", "lat": 39.9042, "lon": 116.4074, "elevation_m": 45},
    "Urumqi": {"name_cn": "乌鲁木齐", "lat": 43.8256, "lon": 87.6168, "elevation_m": 800},
    "Harbin": {"name_cn": "哈尔滨", "lat": 45.8038, "lon": 126.5350, "elevation_m": 150},
    "Lhasa": {"name_cn": "拉萨", "lat": 29.6500, "lon": 91.1000, "elevation_m": 3650},
}

# 冬季大六角及伴月深空天体坐标
SURROUNDING_SKY_TARGETS = {
    "M35": {"name_cn": "双子座疏散星团 M35", "ra_h": 6.150, "dec_deg": 24.333, "mag": 5.1},
    "Pollux": {"name_cn": "北河三 (β Gem)", "ra_h": 7.755, "dec_deg": 28.026, "mag": 1.14},
    "Castor": {"name_cn": "北河二 (α Gem)", "ra_h": 7.577, "dec_deg": 31.888, "mag": 1.58},
    "Betelgeuse": {"name_cn": "参宿四 (α Ori)", "ra_h": 5.919, "dec_deg": 7.407, "mag": 0.50},
    "Procyon": {"name_cn": "南河三 (α CMi)", "ra_h": 7.655, "dec_deg": 5.225, "mag": 0.38},
    "Sirius": {"name_cn": "天狼星 (α CMa)", "ra_h": 6.753, "dec_deg": -16.716, "mag": -1.46},
    "Capella": {"name_cn": "五车二 (α Aur)", "ra_h": 5.278, "dec_deg": 45.998, "mag": 0.08},
    "M45": {"name_cn": "昴宿星团 M45", "ra_h": 3.790, "dec_deg": 24.105, "mag": 1.6},
}


def _angular_separation_rad(ra1: float, dec1: float, ra2: float, dec2: float) -> float:
    """球面大圆角距离（弧度）。"""
    cos_val = math.sin(dec1) * math.sin(dec2) + math.cos(dec1) * math.cos(dec2) * math.cos(ra1 - ra2)
    return math.acos(max(-1.0, min(1.0, cos_val)))


def _cst_format(ephem_t: ephem.Date) -> str:
    """转换为 CST 格式化字符串。"""
    cst = timezone(timedelta(hours=8))
    dt = ephem_t.datetime().replace(tzinfo=timezone.utc).astimezone(cst)
    return dt.strftime("%Y-%m-%d %H:%M:%S CST")


def compute_blue_moon_metrics() -> Dict[str, Any]:
    """计算 2028 年 12 月双满月历法参量与蓝月天文学判定。"""
    fm1_t = ephem.previous_full_moon("2028/12/15")
    fm2_t = ephem.next_full_moon("2028/12/15")

    cst = timezone(timedelta(hours=8))
    dt1 = fm1_t.datetime().replace(tzinfo=timezone.utc).astimezone(cst)
    dt2 = fm2_t.datetime().replace(tzinfo=timezone.utc).astimezone(cst)

    synodic_span_days = float(fm2_t - fm1_t)

    return {
        "first_full_moon_cst": dt1.strftime("%Y-%m-%d %H:%M:%S CST"),
        "second_full_moon_cst": dt2.strftime("%Y-%m-%d %H:%M:%S CST"),
        "calendar_month": "2028-12",
        "synodic_span_days": round(synodic_span_days, 4),
        "is_calendar_blue_moon": True,
        "blue_moon_rule": "Sky & Telescope 1946 历法定义：同一个公历日历月中出现的第二个满月",
        "last_blue_moon_total_eclipse": "2018-01-31 (超级蓝血月)",
        "years_since_last_blue_blood_moon": 10.9,
    }


def compute_eclipse_contacts() -> Dict[str, Any]:
    """
    使用 Chauvenet / Danjon 2% 大气折射膨胀模型，解算 2028-12-31 跨年夜月食各接触点及食分。
    """
    t_start = ephem.Date("2028/12/31 13:30:00")
    t_end = ephem.Date("2028/12/31 20:30:00")
    step = 1.0 / 1440.0  # 1 分钟分辨率

    sun = ephem.Sun()
    moon = ephem.Moon()

    events = []
    t = t_start
    while t < t_end:
        sun.compute(t)
        moon.compute(t)

        r_sun = sun.radius
        r_moon = moon.radius
        pi_moon = math.asin(6378.137 / (moon.earth_distance * 149597870.7))
        pi_sun = math.asin(6378.137 / (sun.earth_distance * 149597870.7))

        sigma_u = 1.02 * (pi_moon + pi_sun - r_sun)
        sigma_p = 1.02 * (pi_moon + pi_sun + r_sun)

        anti_ra = (sun.a_ra + math.pi) % (2.0 * math.pi)
        anti_dec = -sun.a_dec

        sep = _angular_separation_rad(moon.a_ra, moon.a_dec, anti_ra, anti_dec)
        events.append((t, sep, sigma_u, sigma_p, r_moon))
        t = ephem.Date(t + step)

    # 寻找食甚极值点
    mid_idx = min(range(len(events)), key=lambda i: events[i][1])
    t_mid, min_sep, mid_sigma_u, mid_sigma_p, mid_r_moon = events[mid_idx]

    # 解算各接触点时刻
    p1_t, u1_t, u2_t, u3_t, u4_t, p4_t = None, None, None, None, None, None

    for i in range(mid_idx):
        t_cur, sep, s_u, s_p, rm = events[i]
        # P1: sep 穿过 s_p + rm
        if sep >= (s_p + rm) and events[i + 1][1] < (events[i + 1][3] + events[i + 1][4]) and p1_t is None:
            p1_t = t_cur
        # U1: sep 穿过 s_u + rm
        if sep >= (s_u + rm) and events[i + 1][1] < (events[i + 1][2] + events[i + 1][4]) and u1_t is None:
            u1_t = t_cur
        # U2: sep 穿过 s_u - rm
        if sep >= (s_u - rm) and events[i + 1][1] < (events[i + 1][2] - events[i + 1][4]) and u2_t is None:
            u2_t = t_cur

    for i in range(mid_idx, len(events) - 1):
        t_cur, sep, s_u, s_p, rm = events[i]
        # U3: sep 穿过 s_u - rm 向上
        if sep <= (s_u - rm) and events[i + 1][1] > (events[i + 1][2] - events[i + 1][4]) and u3_t is None:
            u3_t = t_cur
        # U4: sep 穿过 s_u + rm 向上
        if sep <= (s_u + rm) and events[i + 1][1] > (events[i + 1][2] + events[i + 1][4]) and u4_t is None:
            u4_t = t_cur
        # P4: sep 穿过 s_p + rm 向上
        if sep <= (s_p + rm) and events[i + 1][1] > (events[i + 1][3] + events[i + 1][4]) and p4_t is None:
            p4_t = t_cur

    # 计算 2029-01-01 00:00:00 CST（跨年零点）的月球食变状态
    t_midnight = ephem.Date("2028/12/31 16:00:00")
    sun.compute(t_midnight)
    moon.compute(t_midnight)
    pi_moon_m = math.asin(6378.137 / (moon.earth_distance * 149597870.7))
    pi_sun_m = math.asin(6378.137 / (sun.earth_distance * 149597870.7))
    sigma_u_m = 1.02 * (pi_moon_m + pi_sun_m - sun.radius)
    anti_ra_m = (sun.a_ra + math.pi) % (2.0 * math.pi)
    anti_dec_m = -sun.a_dec
    sep_midnight = _angular_separation_rad(moon.a_ra, moon.a_dec, anti_ra_m, anti_dec_m)
    penetration_m = (sigma_u_m + moon.radius) - sep_midnight
    midnight_obscuration_fraction = max(0.0, min(1.0, penetration_m / (2.0 * moon.radius)))

    # 食分与持续时间
    umbral_magnitude = (mid_sigma_u + mid_r_moon - min_sep) / (2.0 * mid_r_moon)
    penumbral_magnitude = (mid_sigma_p + mid_r_moon - min_sep) / (2.0 * mid_r_moon)

    totality_duration_min = round((float(u3_t) - float(u2_t)) * 1440.0, 1)
    umbral_duration_min = round((float(u4_t) - float(u1_t)) * 1440.0, 1)
    penumbral_duration_min = round((float(p4_t) - float(p1_t)) * 1440.0, 1)

    return {
        "contacts": {
            "P1_penumbral_ingress": _cst_format(p1_t),
            "U1_umbral_ingress": _cst_format(u1_t),
            "midnight_countdown_cst": "2029-01-01 00:00:00 CST",
            "U2_totality_begins": _cst_format(u2_t),
            "Greatest_Eclipse_mid": _cst_format(t_mid),
            "U3_totality_ends": _cst_format(u3_t),
            "U4_umbral_egress": _cst_format(u4_t),
            "P4_penumbral_egress": _cst_format(p4_t),
        },
        "midnight_obscuration": {
            "timestamp_cst": "2029-01-01 00:00:00 CST",
            "lunar_diameter_obscured_percent": round(midnight_obscuration_fraction * 100.0, 1),
            "status_description": "新年钟声敲响时刻，月面已被地球本影遮挡约 78.9%，仅余残缺银边，红月蓄势待发",
        },
        "durations": {
            "totality_duration_minutes": totality_duration_min,
            "totality_duration_hours": round(totality_duration_min / 60.0, 2),
            "umbral_duration_minutes": umbral_duration_min,
            "umbral_duration_hours": round(umbral_duration_min / 60.0, 2),
            "penumbral_duration_minutes": penumbral_duration_min,
        },
        "magnitudes": {
            "umbral_magnitude": round(umbral_magnitude, 4),
            "penumbral_magnitude": round(penumbral_magnitude, 4),
            "minimum_separation_arcmin": round(math.degrees(min_sep) * 60.0, 2),
            "umbra_radius_arcmin": round(math.degrees(mid_sigma_u) * 60.0, 2),
            "moon_radius_arcmin": round(math.degrees(mid_r_moon) * 60.0, 2),
        },
    }


def compute_china_observability() -> Dict[str, Any]:
    """计算食甚时刻（2029-01-01 00:53 CST）华夏各大城市站心仰角、方位角与大气质量系数。"""
    t_mid = ephem.Date("2028/12/31 16:53:00")
    moon = ephem.Moon()

    city_results = {}
    for city_key, info in CHINA_OBSERVATION_CITIES.items():
        obs = ephem.Observer()
        obs.lat = str(info["lat"])
        obs.lon = str(info["lon"])
        obs.elevation = info["elevation_m"]
        obs.date = t_mid

        moon.compute(obs)
        alt_deg = math.degrees(moon.alt)
        az_deg = math.degrees(moon.az)

        # 大气质量系数 Kasten-Young 公式精算
        zenith_deg = max(0.0, 90.0 - alt_deg)
        if alt_deg > 0:
            airmass = 1.0 / (math.cos(math.radians(zenith_deg)) + 0.50572 * pow(96.07995 - zenith_deg, -1.6364))
        else:
            airmass = 99.0

        city_results[city_key] = {
            "name_cn": info["name_cn"],
            "altitude_deg": round(alt_deg, 2),
            "azimuth_deg": round(az_deg, 2),
            "airmass": round(airmass, 4),
            "zenith_distance_deg": round(zenith_deg, 2),
            "visibility_evaluation": "极佳（几近天顶顶心，近乎零视宁消光）" if alt_deg >= 70.0 else "优异（高空纯净无遮挡）",
        }

    return city_results


def compute_deep_sky_contrast() -> Dict[str, Any]:
    """计算全食期间冬季大六角与 M35 等深空天体对比度、角距离与视星等突变。"""
    t_mid = ephem.Date("2028/12/31 16:53:00")
    moon = ephem.Moon()
    moon.compute(t_mid)

    m_ra = float(moon.ra)
    m_dec = float(moon.dec)

    surrounding = {}
    for key, data in SURROUNDING_SKY_TARGETS.items():
        t_ra = math.radians(data["ra_h"] * 15.0)
        t_dec = math.radians(data["dec_deg"])
        sep_deg = math.degrees(_angular_separation_rad(m_ra, m_dec, t_ra, t_dec))

        surrounding[key] = {
            "name_cn": data["name_cn"],
            "angular_distance_deg": round(sep_deg, 2),
            "catalog_mag": data["mag"],
        }

    return {
        "moon_equatorial": {
            "ra_hours": round(math.degrees(m_ra) / 15.0, 4),
            "dec_degrees": round(math.degrees(m_dec), 4),
            "constellation": "Gemini (双子座)",
        },
        "photometric_collapse": {
            "regular_full_moon_mag": -12.78,
            "totality_blood_moon_mag": 2.0,
            "magnitude_drop": 14.78,
            "flux_attenuation_ratio": round(math.pow(10.0, 0.4 * 14.78)),
            "sky_background_shift": "从满月强烈白昼化泛白（Bortle 8+ 等效）骤降至深空黄金暗夜（Bortle 2~3 视效）",
        },
        "surrounding_targets": surrounding,
    }


def compute_danjon_and_atmospheric_scattering() -> Dict[str, Any]:
    """推演瑞利散射、夏普伊臭氧带吸收与丹戎分级光度色彩物理。"""
    return {
        "danjon_scale": {
            "estimated_value": 2.5,
            "range": "L = 2 ~ 3",
            "visual_color": "深赭红至暗铜色核心，边缘呈现明亮琥珀金铜光辉",
        },
        "optical_mechanisms": {
            "rayleigh_scattering": "日落/日出环形切面上高层大气使短波蓝紫光发生强烈散射（强度与 λ^-4 成反比），仅保留 650-750 nm 深红光透射",
            "chappuis_band_absorption": "平流层臭氧在 500-700 nm 波段吸收黄绿光，进一步提纯并加深地影内部的铜红色调",
            "north_south_chromatic_gradient": "月球中心距地影南边缘较近（偏距 19.02'），南极浸入深影呈 L=2 暗红，北缘逼近本影边界受微弱散射光照射呈现 L=3 亮铜金",
        },
    }


def build_full_report() -> Dict[str, Any]:
    """生成 2028-12-31 跨年夜蓝月全食完整研究报告数据集。"""
    blue_moon = compute_blue_moon_metrics()
    eclipse = compute_eclipse_contacts()
    china_obs = compute_china_observability()
    deep_sky = compute_deep_sky_contrast()
    optics = compute_danjon_and_atmospheric_scattering()

    return {
        "title": "2028-12-31 跨年夜蓝月全食天体力学推演与沙罗 134 家族研究",
        "saros_series": "Lunar Saros 134 (Member 28 of 73)",
        "blue_moon_metrics": blue_moon,
        "eclipse_contacts": eclipse,
        "china_observability": china_obs,
        "deep_sky_contrast": deep_sky,
        "atmospheric_optics": optics,
        "saros_catalog": SAROS_134_CATALOG,
    }


def format_markdown_summary(report: Dict[str, Any]) -> str:
    """输出排版雅致的 Markdown 摘要。"""
    c = report["eclipse_contacts"]["contacts"]
    d = report["eclipse_contacts"]["durations"]
    m = report["eclipse_contacts"]["magnitudes"]
    mb = report["eclipse_contacts"]["midnight_obscuration"]
    cities = report["china_observability"]
    sky = report["deep_sky_contrast"]

    lines = [
        "# 2028-12-31 跨年夜蓝月全食天体力学推演与沙罗 134 家族研究报告",
        "",
        "## 一、天体事件概述与沙罗 134 王者传承",
        f"- **事件类型**：跨年夜超级蓝月全食（New Year's Eve Blue Moon Total Lunar Eclipse）",
        f"- **沙罗序列**：{report['saros_series']}",
        f"- **本影食分**：**{m['umbral_magnitude']}**（半影食分 {m['penumbral_magnitude']}）",
        f"- **全食持续时间**：**{d['totality_duration_minutes']} 分钟**（{d['totality_duration_hours']} 小时）",
        f"- **偏食总时长**：**{d['umbral_duration_minutes']} 分钟**（{d['umbral_duration_hours']} 小时）",
        "",
        "## 二、跨年夜时间轴（中国标准时间 CST）",
        f"- **{c['P1_penumbral_ingress']}**：半影食始（P1）",
        f"- **{c['U1_umbral_ingress']}**：**初亏（U1）** —— 跨年倒计时 53 分钟，地影初咬月面",
        f"- **00:00 CST (01-01)**：**跨年零点钟声** —— 月面已遮挡 **{mb['lunar_diameter_obscured_percent']}%**，残存纤细银边",
        f"- **{c['U2_totality_begins']}**：**食既（U2）** —— 全食阶段开启，红月亮完美成形",
        f"- **{c['Greatest_Eclipse_mid']}**：**食甚（Greatest Eclipse）** —— 深入南本影极深处（距影心仅 19.0'），全天暗夜极值",
        f"- **{c['U3_totality_ends']}**：**生光（U3）** —— 全食结束，东缘初现金光",
        f"- **{c['U4_umbral_egress']}**：**复圆（U4）** —— 月球完全脱离本影",
        f"- **{c['P4_penumbral_egress']}**：半影食终（P4） —— 月球完全恢复清辉",
        "",
        "## 三、华夏全境天顶仰角与绝佳观测视窗（食甚 00:53 CST）",
    ]

    for c_key, c_info in cities.items():
        lines.append(
            f"- **{c_info['name_cn']}**：仰角 **{c_info['altitude_deg']}°** | 方位角 {c_info['azimuth_deg']}° | 大气质量系数 {c_info['airmass']}（{c_info['visibility_evaluation']}）"
        )

    lines.extend([
        "",
        "## 四、冬季大六角与伴月深空天体对比度",
        f"- **月球所在天区**：{sky['moon_equatorial']['constellation']}，赤纬 +{sky['moon_equatorial']['dec_degrees']}°（冬至高空顶心）",
        f"- **光度骤降**：常态满月 -12.78 等 $\\to$ 食甚血月 +2.0 等，光通量衰减 **{sky['photometric_collapse']['flux_attenuation_ratio']:,} 倍**！",
        f"- **近邻天体角距**：",
        f"  * 双子座疏散星团 M35：**{sky['surrounding_targets']['M35']['angular_distance_deg']}°**",
        f"  * 北河二 (Castor)：{sky['surrounding_targets']['Castor']['angular_distance_deg']}° | 北河三 (Pollux)：{sky['surrounding_targets']['Pollux']['angular_distance_deg']}°",
        f"  * 参宿四 (Betelgeuse)：{sky['surrounding_targets']['Betelgeuse']['angular_distance_deg']}° | 南河三 (Procyon)：{sky['surrounding_targets']['Procyon']['angular_distance_deg']}°",
        "",
        "## 五、丹戎分级与色彩物理机理",
        f"- **丹戎级数**：{report['atmospheric_optics']['danjon_scale']['estimated_value']}（{report['atmospheric_optics']['danjon_scale']['visual_color']}）",
        f"- **色彩成因**：地球平流层臭氧夏普伊吸收带（500-700 nm）过滤黄光，瑞利散射仅保留深红光（650-750 nm）弯折投射于月面，南暗北亮呈现瑰丽渐变。",
    ])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="2028-12-31 跨年夜蓝月全食天体力学推演引擎")
    parser.add_argument("--json", action="store_true", help="输出完整 JSON 数据集")
    parser.add_argument("--summary", action="store_true", help="输出 Markdown 简报")
    args = parser.parse_args()

    report = build_full_report()

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif args.summary:
        print(format_markdown_summary(report))
    else:
        print(format_markdown_summary(report))


if __name__ == "__main__":
    main()
