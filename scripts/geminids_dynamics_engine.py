#!/usr/bin/env python3
"""
geminids_dynamics_engine.py
===========================
2026 年双子座流星雨（Geminids 2026）天体力学推演与观测物理引擎

包含：
1. 母天体 3200 Phaethon（法厄同）极端近日点热物理与碎屑破裂力学
2. 流星切入速度、动能密度、质量-星等幂律与烧蚀穿透物理
3. 2026 年农历初五/初六极盛期月光衰退几何与纯黑无月观测黄金时窗
4. 辐射点日周运动、华夏五大区域天顶仰角与实际可视流星率 (HVR) 解算
5. 冬季大六角（Winter Hexagon）星野构型与角距离矩阵

作者: Hoshi
日期: 2026-10-10
"""

import math
import json
import argparse
from typing import Dict, List, Any, Tuple
import ephem

# ---------------------------------------------------------
# 天体物理与轨道常数
# ---------------------------------------------------------
SOLAR_CONSTANT = 1361.0            # W/m^2 (1 AU 处日地太阳常数)
SIGMA_SB = 5.670374e-8             # Stefan-Boltzmann 常数 W/(m^2 K^4)
GM_SUN = 1.32712440018e20          # m^3/s^2 (太阳引力常数)
AU_METERS = 1.495978707e11         # 米/AU

# 3200 Phaethon 轨道参数 (J2000)
PHAETHON_SEMI_MAJOR = 1.2713       # AU
PHAETHON_ECCENTRICITY = 0.8899     # 偏心率
PHAETHON_INCLINATION = 22.25       # 轨道倾角 (deg)
PHAETHON_ALBEDO = 0.106            # 几何反照率
PHAETHON_EMISSIVITY = 0.90         # 热辐射发射率

# 双子座流星群天体物理参量
GEMINIDS_ENTRY_VELOCITY = 35600.0  # m/s (35.6 km/s 大气切入速度)
GEMINIDS_DENSITY = 2500.0          # kg/m^3 (岩石小行星颗粒体密度)
GEMINIDS_LUM_EFFICIENCY = 0.05     # 发光效率 tau_v
GEMINIDS_POP_INDEX = 2.45          # 流星群体指数 r (Population index)
GEMINIDS_NOMINAL_ZHR = 150         # 极盛标称天顶每小时流星率

# 辐射点坐标 (J2026 极盛期)
RADIANT_RA_HOURS = "07:28:00"      # 赤经 07h 28m (~112.0 deg)
RADIANT_DEC_DEG = "+32:30:00"      # 赤纬 +32° 30'

# 华夏代表性观测城市经纬度
CHINA_CITIES = {
    "Beijing": {"name_cn": "北京", "lat": "39.9042", "lon": "116.4074", "elev": 50},
    "Shanghai": {"name_cn": "上海", "lat": "31.2304", "lon": "121.4737", "elev": 10},
    "Guangzhou": {"name_cn": "广州", "lat": "23.1291", "lon": "113.2644", "elev": 25},
    "Chengdu": {"name_cn": "成都", "lat": "30.5728", "lon": "104.0668", "elev": 500},
    "Urumqi": {"name_cn": "乌鲁木齐", "lat": "43.8256", "lon": "87.6168", "elev": 800},
}

# 冬季大六角主要参照亮星
WINTER_HEXAGON_STARS = [
    {"name": "Castor (Alpha Gem)", "cn": "北河二", "ra": "07:34:36", "dec": "31:53:18", "mag": 1.58},
    {"name": "Pollux (Beta Gem)", "cn": "北河三", "ra": "07:45:19", "dec": "28:01:34", "mag": 1.14},
    {"name": "Capella (Alpha Aur)", "cn": "五车二", "ra": "05:16:41", "dec": "45:59:53", "mag": 0.08},
    {"name": "Aldebaran (Alpha Tau)", "cn": "毕宿五", "ra": "04:35:55", "dec": "16:30:33", "mag": 0.85},
    {"name": "Rigel (Beta Ori)", "cn": "参宿七", "ra": "05:14:32", "dec": "-08:12:06", "mag": 0.13},
    {"name": "Betelgeuse (Alpha Ori)", "cn": "参宿四", "ra": "05:55:10", "dec": "07:24:25", "mag": 0.50},
    {"name": "Sirius (Alpha CMa)", "cn": "天狼星", "ra": "06:45:09", "dec": "-16:42:58", "mag": -1.46},
    {"name": "Procyon (Alpha CMi)", "cn": "南河三", "ra": "07:39:18", "dec": "05:13:30", "mag": 0.38},
]


def calculate_phaethon_mechanics() -> Dict[str, Any]:
    """
    解算 3200 Phaethon（法厄同）的轨道动力学与近日点热物理状态
    """
    a = PHAETHON_SEMI_MAJOR
    e = PHAETHON_ECCENTRICITY
    q = a * (1.0 - e)
    Q = a * (1.0 + e)
    period_years = math.sqrt(a ** 3)
    
    # 近日点太阳辐射通量
    s_perihelion = SOLAR_CONSTANT / (q ** 2)
    s_ratio_earth = s_perihelion / SOLAR_CONSTANT
    
    # 向阳面次太阳点平衡温度 (Subsolar equilibrium temperature)
    # T_ss = [ (1 - A) * S / (eps * sigma) ]^(1/4)
    t_subsolar = (((1.0 - PHAETHON_ALBEDO) * s_perihelion) / (PHAETHON_EMISSIVITY * SIGMA_SB)) ** 0.25
    t_subsolar_celsius = t_subsolar - 273.15
    
    # 近日点轨道速度 v_q = sqrt( GM * (2/r_q - 1/a) )
    r_q_m = q * AU_METERS
    a_m = a * AU_METERS
    v_perihelion = math.sqrt(GM_SUN * (2.0 / r_q_m - 1.0 / a_m)) / 1000.0  # km/s
    
    # 远日点轨道速度
    r_Q_m = Q * AU_METERS
    v_aphelion = math.sqrt(GM_SUN * (2.0 / r_Q_m - 1.0 / a_m)) / 1000.0   # km/s
    
    return {
        "semi_major_axis_au": round(a, 4),
        "eccentricity": round(e, 4),
        "inclination_deg": PHAETHON_INCLINATION,
        "perihelion_q_au": round(q, 4),
        "aphelion_Q_au": round(Q, 4),
        "period_years": round(period_years, 2),
        "perihelion_velocity_km_s": round(v_perihelion, 2),
        "aphelion_velocity_km_s": round(v_aphelion, 2),
        "perihelion_solar_flux_w_m2": round(s_perihelion, 1),
        "solar_flux_ratio_to_earth": round(s_ratio_earth, 1),
        "subsolar_equilibrium_temp_k": round(t_subsolar, 1),
        "subsolar_equilibrium_temp_c": round(t_subsolar_celsius, 1),
    }


def calculate_meteoroid_ablation(mass_mg: float) -> Dict[str, Any]:
    """
    解算特定质量流星体的动能、发光功率、烧蚀持续时间与目视绝对星等
    """
    m_kg = mass_mg * 1e-6
    v = GEMINIDS_ENTRY_VELOCITY
    
    # 初始动能 E_k = 0.5 * m * v^2
    e_k = 0.5 * m_kg * (v ** 2)
    
    # 发光能量与发光持续时间估算 (Verniani 经验模型: dt 随质量弱相关)
    dt = 0.30 * (mass_mg ** 0.20)
    e_lum = e_k * GEMINIDS_LUM_EFFICIENCY
    power_watts = e_lum / dt if dt > 0 else 0.0
    
    # 目视星等标定: Verniani 0 等星对应约 484 W 发光通量
    if power_watts > 0:
        mag_v = -2.5 * math.log10(power_watts / 484.0)
    else:
        mag_v = 99.0
        
    # 等效球形微粒直径 (假设密度 2500 kg/m^3)
    radius_m = ((3.0 * m_kg) / (4.0 * math.pi * GEMINIDS_DENSITY)) ** (1.0 / 3.0)
    diameter_mm = 2.0 * radius_m * 1000.0
    
    # 典型烧蚀终止高度 (高度致密岩石颗粒深入至 45~75 km)
    # 质量越大，穿透越深
    penetration_alt_km = max(40.0, 75.0 - 5.0 * math.log10(max(0.01, mass_mg)))
    
    return {
        "mass_mg": mass_mg,
        "diameter_mm": round(diameter_mm, 3),
        "kinetic_energy_j": round(e_k, 2),
        "luminous_power_w": round(power_watts, 2),
        "duration_sec": round(dt, 2),
        "visual_magnitude": round(mag_v, 2),
        "terminal_ablation_alt_km": round(penetration_alt_km, 1),
    }


def calculate_hourly_visible_rate(
    zhr: float,
    radiant_alt_deg: float,
    limiting_mag: float = 6.5,
    pop_index: float = GEMINIDS_POP_INDEX,
    gamma: float = 1.0
) -> float:
    """
    计算特定辐射点仰角与极限星等下的实际目视每小时流星率 (HVR)
    HVR = ZHR * sin^gamma(h_R) * r^(6.5 - NELM)^(-1)
    """
    if radiant_alt_deg <= 0:
        return 0.0
    sin_h = math.sin(math.radians(radiant_alt_deg))
    rad_factor = sin_h ** gamma
    nelm_factor = pop_index ** (limiting_mag - 6.5)
    return max(0.0, zhr * rad_factor * nelm_factor)


def calculate_city_ephemeris(date_str: str = "2026/12/13") -> List[Dict[str, Any]]:
    """
    解算华夏主要代表性城市在 2026 年双子座流星雨极盛夜的天文观测几何
    """
    results = []
    
    for city_key, info in CHINA_CITIES.items():
        obs = ephem.Observer()
        obs.lat = info["lat"]
        obs.lon = info["lon"]
        obs.elevation = info["elev"]
        # 设置观测起始时间为 CST 18:00 (UTC 10:00)
        obs.date = ephem.Date(f"{date_str} 10:00:00")
        
        sun = ephem.Sun()
        moon = ephem.Moon()
        
        radiant = ephem.FixedBody()
        radiant._ra = ephem.hours(RADIANT_RA_HOURS)
        radiant._dec = ephem.degrees(RADIANT_DEC_DEG)
        radiant._epoch = ephem.Date(date_str)
        
        sunset_utc = obs.next_setting(sun)
        sunrise_utc = obs.next_rising(sun)
        moonset_utc = obs.next_setting(moon)
        
        rad_rise_utc = obs.next_rising(radiant)
        rad_transit_utc = obs.next_transit(radiant)
        
        # 计算中天时仰角
        obs.date = rad_transit_utc
        radiant.compute(obs)
        transit_alt_deg = float(radiant.alt) * 180.0 / math.pi
        
        # 计算月落时的月相照亮比例
        obs.date = moonset_utc
        moon.compute(obs)
        moon_illum_pct = float(moon.phase)
        
        # UTC 转 CST 字符串辅助函数
        def _to_cst_str(ep_dt: ephem.Date) -> str:
            import datetime
            d = ep_dt.datetime() + datetime.timedelta(hours=8)
            return d.strftime("%H:%M")
        
        # 计算纯黑无月观测窗口时长 (月落至日出晨光始)
        # 简化为月落到日出的时间差
        dark_window_hours = (sunrise_utc - moonset_utc) * 24.0
        
        # 计算中天时的理论目视流星率 (暗夜 NELM=6.5)
        hvr_transit = calculate_hourly_visible_rate(
            GEMINIDS_NOMINAL_ZHR, transit_alt_deg, limiting_mag=6.5
        )
        # 郊区中度光害 NELM=5.5
        hvr_suburban = calculate_hourly_visible_rate(
            GEMINIDS_NOMINAL_ZHR, transit_alt_deg, limiting_mag=5.5
        )
        
        results.append({
            "city_key": city_key,
            "city_cn": info["name_cn"],
            "lat": float(info["lat"]),
            "lon": float(info["lon"]),
            "sunset_cst": _to_cst_str(sunset_utc),
            "sunrise_cst": _to_cst_str(sunrise_utc),
            "moonset_cst": _to_cst_str(moonset_utc),
            "moon_illum_percent": round(moon_illum_pct, 1),
            "radiant_rise_cst": _to_cst_str(rad_rise_utc),
            "radiant_transit_cst": _to_cst_str(rad_transit_utc),
            "transit_altitude_deg": round(transit_alt_deg, 1),
            "dark_sky_window_hours": round(dark_window_hours, 1),
            "hvr_dark_sky": round(hvr_transit, 1),
            "hvr_suburban": round(hvr_suburban, 1),
        })
        
    return results


def calculate_winter_hexagon_context() -> List[Dict[str, Any]]:
    """
    解算辐射点与冬季大六角/大三角主要恒星的角距离矩阵
    """
    radiant = ephem.FixedBody()
    radiant._ra = ephem.hours(RADIANT_RA_HOURS)
    radiant._dec = ephem.degrees(RADIANT_DEC_DEG)
    radiant._epoch = ephem.Date("2026/12/14")
    radiant.compute()
    
    star_contexts = []
    for s_info in WINTER_HEXAGON_STARS:
        star = ephem.FixedBody()
        star._ra = ephem.hours(s_info["ra"])
        star._dec = ephem.degrees(s_info["dec"])
        star._epoch = ephem.Date("2026/12/14")
        star.compute()
        
        sep_deg = ephem.separation(radiant, star) * 180.0 / math.pi
        star_contexts.append({
            "name": s_info["name"],
            "cn": s_info["cn"],
            "visual_magnitude": s_info["mag"],
            "separation_from_radiant_deg": round(sep_deg, 2),
        })
        
    star_contexts.sort(key=lambda x: x["separation_from_radiant_deg"])
    return star_contexts


def generate_full_report() -> Dict[str, Any]:
    """
    生成完整的 2026 双子座流星雨动力学分析数据集
    """
    phaethon = calculate_phaethon_mechanics()
    ablation_samples = [
        calculate_meteoroid_ablation(m)
        for m in [0.01, 0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0]
    ]
    city_ephemeris = calculate_city_ephemeris()
    hexagon_stars = calculate_winter_hexagon_context()
    
    return {
        "meta": {
            "title": "2026 双子座流星雨（Geminids）天体力学与观象动力学解算",
            "peak_window_cst": "2026-12-14 02:00 ~ 08:00 CST",
            "nominal_zhr": GEMINIDS_NOMINAL_ZHR,
            "radiant_coords": {
                "ra": RADIANT_RA_HOURS,
                "dec": RADIANT_DEC_DEG,
                "constellation": "Gemini (双子座)",
                "anchor_star": "Castor (北河二)",
            },
        },
        "phaethon_mechanics": phaethon,
        "ablation_physics": ablation_samples,
        "city_ephemeris": city_ephemeris,
        "winter_hexagon_context": hexagon_stars,
    }


def print_cli_report(data: Dict[str, Any]):
    """
    以终端排版格式输出研究报告
    """
    meta = data["meta"]
    p = data["phaethon_mechanics"]
    
    print("=" * 76)
    print(f" ✨ {meta['title']}")
    print("=" * 76)
    print(f"极盛时间窗: {meta['peak_window_cst']} | 标称 ZHR: {meta['nominal_zhr']}")
    print(f"辐射点定位: 赤经 {meta['radiant_coords']['ra']} / 赤纬 {meta['radiant_coords']['dec']} (双子座北河二西北 1.5°)")
    print("-" * 76)
    print("【1. 母天体 3200 Phaethon 轨道动力学与近日点热破裂】")
    print(f"  • 轨道根数: 半长轴 a = {p['semi_major_axis_au']} AU, 偏心率 e = {p['eccentricity']}, 倾角 i = {p['inclination_deg']}°")
    print(f"  • 近日点距离: q = {p['perihelion_q_au']} AU (约 2094 万 km, 深达水星轨道以里!)")
    print(f"  • 近日点太阳辐射通量: {p['perihelion_solar_flux_w_m2']} W/m² ({p['solar_flux_ratio_to_earth']} 倍地球日地通量)")
    print(f"  • 向阳面次太阳点平衡温度: {p['subsolar_equilibrium_temp_k']} K ({p['subsolar_equilibrium_temp_c']} °C)")
    print(f"  • 破裂机制: 硅酸盐岩石在 >770°C 剧烈热应力下爆裂崩解 (Thermal Spallation)，高密度致密岩石颗粒")
    print("-" * 76)
    print("【2. 流星烧蚀物理与质量-星等幂律 (入层速度 35.6 km/s, 密度 2500 kg/m³)】")
    print(f"{'质量(mg)':>10} | {'等效直径(mm)':>12} | {'动能(J)':>10} | {'光功率(W)':>10} | {'绝对星等':>8} | {'终止高度(km)':>12}")
    print("-" * 76)
    for a in data["ablation_physics"]:
        print(f"{a['mass_mg']:10.2f} | {a['diameter_mm']:12.3f} | {a['kinetic_energy_j']:10.1f} | {a['luminous_power_w']:10.1f} | {a['visual_magnitude']:8.2f} | {a['terminal_ablation_alt_km']:12.1f}")
    print("-" * 76)
    print("【3. 华夏各大区域 2026-12-13/14 极盛夜观测几何与纯黑无月窗口】")
    print(f"{'城市':<6} | {'月落(CST)':<9} | {'月相照亮':<8} | {'辐射点中天':<10} | {'中天仰角':<8} | {'无月暗夜时窗':<12} | {'暗夜HVR':<8}")
    print("-" * 76)
    for c in data["city_ephemeris"]:
        print(f"{c['city_cn']:<6} | {c['moonset_cst']:<9} | {c['moon_illum_percent']:>6.1f}% | {c['radiant_transit_cst']:<10} | {c['transit_altitude_deg']:>6.1f}° | {c['dark_sky_window_hours']:>10.1f} 小时 | {c['hvr_dark_sky']:>8.1f}")
    print("-" * 76)
    print("【4. 冬季大六角星野衬托角距离】")
    for s in data["winter_hexagon_context"]:
        print(f"  • {s['cn']} ({s['name']}, V={s['visual_magnitude']:+.2f}): 距辐射点 {s['separation_from_radiant_deg']:.2f}°")
    print("=" * 76)


def main():
    parser = argparse.ArgumentParser(description="2026 双子座流星雨天体力学推演引擎")
    parser.add_argument("--json", action="store_true", help="输出完整 JSON 数据")
    args = parser.parse_args()
    
    data = generate_full_report()
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print_cli_report(data)


if __name__ == "__main__":
    main()
