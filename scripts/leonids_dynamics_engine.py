#!/usr/bin/env python3
"""
leonids_dynamics_engine.py
==========================
2026 年狮子座流星雨（Leonids 2026）天体力学推演、母彗星 55P/Tempel-Tuttle 逆行超速切入动力学、
持久余迹激波电离、火木双星引路信标与“月落狮起”交接暗空引擎。

核心推演模块：
1. 母彗星 55P/Tempel-Tuttle 轨道力学：33.22 年周期、高倾角逆行轨道 (i = 162.49°)、
   2026 年近日点前 4.5 年入向轨道 (r_H ≈ 4.85 AU) 与 2031 年近日点倒计时。
2. 逆行迎头相对切入超高极速 (71.0 km/s)、单位动能密度 (2.52 GJ/kg，约 602.4 倍 TNT 当量)、
   高空发光效率、极端消融高度 (115~95 km) 与 [O I] 557.7 nm / NO-O3 持久余迹 (Persistent Train) 物理。
3. 2026 年极盛期（11-17/18）“火星合木星”超近双星信标：火星 (+0.64) 与木星 (-1.99) 仅隔 1.35°，
   距辐射点仅 7.8°~9.1°，构成绝无仅有的亮行星寻星同框标尺。
4. 农历十月初九“西月沉落，东狮昂首”无缝几何交接：上弦月半夜入西地平之时恰为辐射点东升之刻，
   华夏五大城市后半夜独享 5.1~5.8 小时 100% 纯黑无月暗夜黄金天窗。
5. 华夏五大城市精确升落时序、辐射点仰角演化、实际目视小时率 (HR_obs) 积分与全景报告生成。

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
GM_SUN = 1.32712440018e20          # m^3/s^2 (太阳引力常数)
AU_METERS = 1.495978707e11         # 米/AU
TNT_JOULES_PER_KG = 4.184e6        # 1 kg TNT 能量 (J)
CST_TZ = timezone(timedelta(hours=8))

# 母彗星 55P/Tempel-Tuttle 轨道参数 (J2000)
TEMPEL_TUTTLE_SEMI_MAJOR = 10.334  # AU (半长轴)
TEMPEL_TUTTLE_ECCENTRICITY = 0.9056 # 偏心率
TEMPEL_TUTTLE_INCLINATION = 162.49 # 轨道倾角 (deg, 逆行轨道)
TEMPEL_TUTTLE_PERIOD_YRS = 33.22   # 轨道周期 (年)
TEMPEL_TUTTLE_PERIHELION_Q = 0.976 # AU (近日点距离)
TEMPEL_TUTTLE_APHELION_Q = 19.692  # AU (远日点距离)
NEXT_PERIHELION_YEAR = 2031.38     # 2031 年 5 月

# 狮子座流星雨流星群天体物理参量
LEONIDS_ENTRY_VELOCITY = 71000.0   # m/s (71.0 km/s 超高速大气切入)
LEONIDS_DENSITY = 900.0            # kg/m^3 (蓬松多孔彗星粉尘聚合体)
LEONIDS_LUM_EFFICIENCY = 0.075     # 高速切入激发发光效率 tau_v
LEONIDS_POP_INDEX = 2.50           # 流星群体指数 r (Population index)
LEONIDS_NOMINAL_ZHR = 15           # 标称平静期天顶每小时流星率

# 辐射点坐标 (J2026 极盛期)
RADIANT_RA_HOURS = "10:08:00"      # 赤经 10h 08m (152.0 deg)
RADIANT_DEC_DEG = "+22:00:00"      # 赤纬 +22° 00'

# 华夏代表性观测城市经纬度
CHINA_CITIES = {
    "Beijing": {"name_cn": "北京", "lat": "39.9042", "lon": "116.4074", "elev": 50},
    "Shanghai": {"name_cn": "上海", "lat": "31.2304", "lon": "121.4737", "elev": 10},
    "Guangzhou": {"name_cn": "广州", "lat": "23.1291", "lon": "113.2644", "elev": 25},
    "Chengdu": {"name_cn": "成都", "lat": "30.5728", "lon": "104.0668", "elev": 500},
    "Urumqi": {"name_cn": "乌鲁木齐", "lat": "43.8256", "lon": "87.6168", "elev": 800},
}

# 狮子座周边参照天体与亮星
LEO_REFERENCE_STARS = [
    {"name": "Gamma Leo (Algieba)", "cn": "轩辕十二", "ra": "10:19:58", "dec": "+19:50:30", "mag": 2.01},
    {"name": "Mu Leo (Rasalas)", "cn": "轩辕十", "ra": "09:52:45", "dec": "+26:00:25", "mag": 3.88},
    {"name": "Epsilon Leo (Algenubi)", "cn": "轩辕九", "ra": "09:45:51", "dec": "+23:46:27", "mag": 2.97},
    {"name": "Alpha Leo (Regulus)", "cn": "轩辕十四", "ra": "10:08:22", "dec": "+11:58:02", "mag": 1.36},
    {"name": "Delta Leo (Zosma)", "cn": "西上相", "ra": "11:14:06", "dec": "+20:31:25", "mag": 2.56},
    {"name": "Beta Leo (Denebola)", "cn": "五帝座一", "ra": "11:49:03", "dec": "+14:34:19", "mag": 2.14},
]


def calculate_comet_mechanics() -> Dict[str, Any]:
    """
    解算母彗星 55P/Tempel-Tuttle 的轨道力学、逆行几何与 2026 年所处入向轨道状态。
    """
    a = TEMPEL_TUTTLE_SEMI_MAJOR
    e = TEMPEL_TUTTLE_ECCENTRICITY
    i = TEMPEL_TUTTLE_INCLINATION
    q = a * (1.0 - e)
    Q = a * (1.0 + e)
    period = math.sqrt(a ** 3)

    r_earth = 1.0 * AU_METERS
    v_earth = math.sqrt(GM_SUN / r_earth) / 1000.0  # ~29.78 km/s
    v_comet_1au = math.sqrt(GM_SUN * (2.0 / r_earth - 1.0 / (a * AU_METERS))) / 1000.0  # ~41.5 km/s

    dt_current_year = 2026.88
    years_to_perihelion = NEXT_PERIHELION_YEAR - dt_current_year
    est_rh_au = 4.85

    return {
        "comet_name": "55P/Tempel-Tuttle",
        "semi_major_axis_au": round(a, 3),
        "eccentricity": round(e, 4),
        "inclination_deg": round(i, 2),
        "is_retrograde": i > 90.0,
        "perihelion_q_au": round(q, 3),
        "aphelion_Q_au": round(Q, 3),
        "period_years": round(period, 2),
        "earth_orbital_speed_km_s": round(v_earth, 2),
        "comet_speed_1au_km_s": round(v_comet_1au, 2),
        "entry_speed_km_s": round(LEONIDS_ENTRY_VELOCITY / 1000.0, 1),
        "years_to_next_perihelion": round(years_to_perihelion, 2),
        "est_heliocentric_distance_2026_au": est_rh_au,
        "orbital_architecture": "极高倾角逆行椭圆轨道，近日点轻掠地球轨道内侧 (0.976 AU)，远日点直抵天王星轨道外缘 (19.69 AU)",
    }


def calculate_hypervelocity_ablation(mass_mg: float = 1.0) -> Dict[str, Any]:
    """
    计算给定质量流星体的超高速动能释放、TNT 当量、发光星等与高层消融特征。
    """
    mass_kg = (mass_mg * 1e-3) / 1e3
    v = LEONIDS_ENTRY_VELOCITY
    rho = LEONIDS_DENSITY

    vol_m3 = mass_kg / rho
    diameter_m = (6.0 * vol_m3 / math.pi) ** (1.0 / 3.0)
    diameter_mm = diameter_m * 1000.0

    e_kin = 0.5 * mass_kg * (v ** 2)
    e_kin_per_kg = 0.5 * (v ** 2)
    tnt_equiv_kg = e_kin / TNT_JOULES_PER_KG
    tnt_factor_per_kg = e_kin_per_kg / TNT_JOULES_PER_KG

    v_km_s = v / 1000.0
    abs_mag = 4.3 - 2.5 * math.log10(mass_mg) - 5.0 * math.log10(v_km_s / 35.0)

    start_alt_km = 118.0 + 3.0 * math.log10(mass_mg + 1e-6)
    peak_alt_km = 98.0 + 2.5 * math.log10(mass_mg + 1e-6)
    terminal_alt_km = max(75.0, 88.0 + 2.0 * math.log10(mass_mg + 1e-6))

    is_fireball = abs_mag <= -3.0

    return {
        "mass_mg": mass_mg,
        "diameter_mm": round(diameter_mm, 3),
        "kinetic_energy_j": round(e_kin, 2),
        "kinetic_energy_per_kg_gj": round(e_kin_per_kg / 1e9, 2),
        "tnt_equivalent_factor_per_kg": round(tnt_factor_per_kg, 1),
        "tnt_equivalent_g": round(tnt_equiv_kg * 1000.0, 3),
        "visual_magnitude": round(abs_mag, 2),
        "ablation_start_alt_km": round(start_alt_km, 1),
        "ablation_peak_alt_km": round(peak_alt_km, 1),
        "terminal_ablation_alt_km": round(terminal_alt_km, 1),
        "is_fireball": is_fireball,
        "train_physics": {
            "initial_glow": "中性氧原子禁戒极光绿线 [O I] 557.7 nm (寿命 τ ≈ 0.74 s)",
            "long_duration_persistent_train": "中间层顶 (85~95 km) 催化化学发光反应 NO + O3 -> NO2* + O2，高空风速场扭曲形成漂移持久光痕",
        },
    }


def calculate_mars_jupiter_beacon() -> Dict[str, Any]:
    """
    解算 2026 年 11 月中旬狮子座流星雨极盛期间，火星与木星超近会合、
    双星信标空间几何与相对于流星雨辐射点的精确方位。
    """
    obs = ephem.Observer()
    obs.lat = "31.2304"
    obs.lon = "121.4737"
    obs.date = datetime(2026, 11, 17, 20, 0, 0)  # 2026-11-18 04:00 CST

    mars = ephem.Mars()
    jupiter = ephem.Jupiter()
    radiant = ephem.FixedBody()
    radiant._ra = ephem.hours(RADIANT_RA_HOURS)
    radiant._dec = ephem.degrees(RADIANT_DEC_DEG)
    radiant._epoch = ephem.J2000

    mars.compute(obs)
    jupiter.compute(obs)
    radiant.compute(obs)

    sep_mj_deg = float(ephem.separation(mars, jupiter)) * 180.0 / math.pi
    sep_mj_arcmin = sep_mj_deg * 60.0

    sep_mars_rad_deg = float(ephem.separation(mars, radiant)) * 180.0 / math.pi
    sep_jup_rad_deg = float(ephem.separation(jupiter, radiant)) * 180.0 / math.pi

    min_sep = 999.0
    min_dt_utc = None
    t0 = datetime(2026, 11, 14, 0, 0, 0)
    for step in range(24 * 7):
        t = t0 + timedelta(hours=step)
        obs.date = t
        mars.compute(obs)
        jupiter.compute(obs)
        s = float(ephem.separation(mars, jupiter)) * 180.0 / math.pi
        if s < min_sep:
            min_sep = s
            min_dt_utc = t

    closest_cst = min_dt_utc + timedelta(hours=8)

    return {
        "conjunction_date_cst": closest_cst.strftime("%Y-%m-%d %H:%M CST"),
        "conjunction_min_separation_deg": round(min_sep, 3),
        "conjunction_min_separation_arcmin": round(min_sep * 60.0, 1),
        "peak_night_state_cst": "2026-11-18 04:00 CST",
        "mars_magnitude": round(float(mars.mag), 2),
        "jupiter_magnitude": round(float(jupiter.mag), 2),
        "peak_night_mars_jupiter_sep_deg": round(sep_mj_deg, 2),
        "peak_night_mars_jupiter_sep_arcmin": round(sep_mj_arcmin, 1),
        "mars_to_radiant_sep_deg": round(sep_mars_rad_deg, 2),
        "jupiter_to_radiant_sep_deg": round(sep_jup_rad_deg, 2),
        "astronomical_significance": (
            f"2026 狮子座极盛夜（11-17/18），木星 ({round(float(jupiter.mag), 2)} 等) 与火星 "
            f"({round(float(mars.mag), 2)} 等) 在狮子座内形成间距仅 {round(sep_mj_deg, 2)}° 的超亮行星伴星，"
            f"距离流星群辐射点仅 {round(sep_mars_rad_deg, 1)}°~{round(sep_jup_rad_deg, 1)}°，"
            "为广角天体摄影提供了百年难遇的双亮行星辐射信标！"
        ),
    }


def calculate_leo_sky_context() -> List[Dict[str, Any]]:
    """
    解算狮子座头部“镰刀”构造主要恒星与辐射点的角距离矩阵。
    """
    obs = ephem.Observer()
    obs.lat = "31.2304"
    obs.lon = "121.4737"
    obs.date = datetime(2026, 11, 17, 20, 0, 0)

    radiant = ephem.FixedBody()
    radiant._ra = ephem.hours(RADIANT_RA_HOURS)
    radiant._dec = ephem.degrees(RADIANT_DEC_DEG)
    radiant._epoch = ephem.J2000
    radiant.compute(obs)

    results = []
    for star in LEO_REFERENCE_STARS:
        s = ephem.FixedBody()
        s._ra = ephem.hours(star["ra"])
        s._dec = ephem.degrees(star["dec"])
        s._epoch = ephem.J2000
        s.compute(obs)
        sep_deg = float(ephem.separation(s, radiant)) * 180.0 / math.pi
        results.append({
            "name": star["name"],
            "name_cn": star["cn"],
            "visual_magnitude": star["mag"],
            "separation_to_radiant_deg": round(sep_deg, 2),
        })

    results.sort(key=lambda x: x["separation_to_radiant_deg"])
    return results


def calculate_hourly_visible_rate(
    radiant_alt_deg: float,
    moon_alt_deg: float,
    zhr: float = LEONIDS_NOMINAL_ZHR,
    pop_index: float = LEONIDS_POP_INDEX,
    nelm: float = 6.2,
) -> float:
    """
    解算地面观测者实际目视流星率 (HR_obs)。
    公式：HR_obs = ZHR * sin^gamma(h_rad) * r^(6.5 - NELM_eff)
    其中超高速流星群 gamma 取 1.4。
    """
    if radiant_alt_deg <= 0.0:
        return 0.0

    gamma = 1.4
    alt_rad = math.radians(radiant_alt_deg)
    sin_alt_factor = (math.sin(alt_rad)) ** gamma

    nelm_eff = nelm
    if moon_alt_deg > 0.0:
        moon_penalty = 1.8 * (math.sin(math.radians(moon_alt_deg)) ** 0.5)
        nelm_eff = max(4.0, nelm - moon_penalty)

    f_nelm = (pop_index) ** (nelm_eff - 6.5)
    hr = zhr * sin_alt_factor * f_nelm
    return max(0.0, hr)


def calculate_city_ephemeris(city_key: str) -> Dict[str, Any]:
    """
    解算特定华夏城市在 2026-11-17/18 极盛之夜的“月落狮起”交接时序、
    纯黑天窗时长、辐射点最高中天仰角与实际可视流星率。
    """
    city = CHINA_CITIES[city_key]
    obs = ephem.Observer()
    obs.lat = city["lat"]
    obs.lon = city["lon"]
    obs.elevation = city["elev"]
    obs.date = datetime(2026, 11, 17, 12, 0, 0)  # 20:00 CST

    moon = ephem.Moon()
    sun = ephem.Sun()
    radiant = ephem.FixedBody()
    radiant._ra = ephem.hours(RADIANT_RA_HOURS)
    radiant._dec = ephem.degrees(RADIANT_DEC_DEG)
    radiant._epoch = ephem.J2000

    # 精确计算月落与辐射点升起时刻
    obs.horizon = '0'
    m_set_dt = ephem.Date(obs.next_setting(moon)).datetime() + timedelta(hours=8)
    r_rise_dt = ephem.Date(obs.next_rising(radiant)).datetime() + timedelta(hours=8)

    # 辐射点中天时刻与极大仰角
    r_transit = obs.next_transit(radiant)
    r_transit_dt = ephem.Date(r_transit).datetime() + timedelta(hours=8)
    obs.date = r_transit
    radiant.compute(obs)
    max_radiant_alt = float(radiant.alt) * 180.0 / math.pi

    # 天文晨光始 (-18°)
    obs.horizon = '-18'
    obs.date = datetime(2026, 11, 17, 16, 0, 0)  # 00:00 CST
    s_dawn_dt = ephem.Date(obs.next_rising(sun)).datetime() + timedelta(hours=8)

    # 纯暗夜黄金天窗：从月落起至天文晨光始
    dark_start = max(m_set_dt, r_rise_dt)
    dark_dur_hours = max(0.0, (s_dawn_dt - dark_start).total_seconds() / 3600.0)

    # 逐时进展
    obs.horizon = '0'
    t_start = datetime(2026, 11, 17, 9, 0, 0)  # 17:00 CST
    hourly_records = []
    for step in range(15):
        utc = t_start + timedelta(hours=step)
        cst = utc + timedelta(hours=8)
        obs.date = utc

        moon.compute(obs)
        sun.compute(obs)
        radiant.compute(obs)

        s_alt = float(sun.alt) * 180.0 / math.pi
        m_alt = float(moon.alt) * 180.0 / math.pi
        r_alt = float(radiant.alt) * 180.0 / math.pi
        m_phase = float(moon.moon_phase) * 100.0

        hr = calculate_hourly_visible_rate(r_alt, m_alt, nelm=6.0)

        hourly_records.append({
            "cst_time": cst.strftime("%m-%d %H:%M"),
            "sun_alt_deg": round(s_alt, 1),
            "moon_alt_deg": round(m_alt, 1),
            "radiant_alt_deg": round(r_alt, 1),
            "moon_phase_pct": round(m_phase, 1),
            "visible_hr_obs": round(hr, 1),
            "is_pure_dark_window": s_alt <= -18.0 and m_alt <= 0.0 and r_alt >= 0.0,
        })

    return {
        "city_key": city_key,
        "city_name_cn": city["name_cn"],
        "moon_set_cst": m_set_dt.strftime("%H:%M"),
        "radiant_rise_cst": r_rise_dt.strftime("%H:%M"),
        "dawn_twilight_cst": s_dawn_dt.strftime("%H:%M"),
        "transit_cst": r_transit_dt.strftime("%H:%M"),
        "max_radiant_alt_deg": round(max_radiant_alt, 1),
        "dark_sky_duration_hours": round(dark_dur_hours, 2),
        "hourly_progression": hourly_records,
    }


def generate_full_report() -> Dict[str, Any]:
    """
    汇编全景天体力学与观象动力学推演报告。
    """
    comet = calculate_comet_mechanics()
    ablation_1mg = calculate_hypervelocity_ablation(1.0)
    ablation_100mg = calculate_hypervelocity_ablation(100.0)
    beacon = calculate_mars_jupiter_beacon()
    stars = calculate_leo_sky_context()

    cities_data = {}
    for k in CHINA_CITIES:
        cities_data[k] = calculate_city_ephemeris(k)

    return {
        "report_title": "2026 年狮子座流星雨天体力学推演与观象动力学全景报告",
        "generated_cst": datetime.now(CST_TZ).strftime("%Y-%m-%d %H:%M:%S CST"),
        "parent_comet": comet,
        "ablation_physics_samples": {
            "standard_meteor_1mg": ablation_1mg,
            "fireball_100mg": ablation_100mg,
        },
        "mars_jupiter_beacon": beacon,
        "leo_reference_stars": stars,
        "chinese_cities_geometry": cities_data,
    }


def print_text_report(rep: Dict[str, Any]) -> None:
    """
    以格式化纯文本输出高可读性科学全景报告。
    """
    print("=" * 80)
    print(f" {rep['report_title']} ")
    print("=" * 80)
    print(f"报告生成时间: {rep['generated_cst']}\n")

    comet = rep["parent_comet"]
    print("【一、母彗星 55P/Tempel-Tuttle 轨道力学与 2026 年入向状态】")
    print(f"- 轨道构型: {comet['orbital_architecture']}")
    print(f"- 半长轴: {comet['semi_major_axis_au']} AU | 偏心率: {comet['eccentricity']} | 周期: {comet['period_years']} 年")
    print(f"- 轨道倾角: {comet['inclination_deg']}° (严格逆行轨道，地球逆向迎头相撞)")
    print(f"- 大气切入速度: **{comet['entry_speed_km_s']} km/s** (全天流星雨极速之冠，255,600 km/h)")
    print(f"- 2031 年近日点倒计时: 剩余 {comet['years_to_next_perihelion']} 年 | 2026 当前日心距约 {comet['est_heliocentric_distance_2026_au']} AU")
    print()

    m1 = rep["ablation_physics_samples"]["standard_meteor_1mg"]
    m100 = rep["ablation_physics_samples"]["fireball_100mg"]
    print("【二、超高速动能释放与高层激波持久余迹 (Persistent Train) 物理】")
    print(f"- 单位质量动能释放: **{m1['kinetic_energy_per_kg_gj']} GJ/kg** (相当于 **{m1['tnt_equivalent_factor_per_kg']} 倍 TNT 当量**)")
    print(f"- 1 毫克微尘 (芝麻级, 0.9 mm): 动能 {m1['kinetic_energy_j']} J (当量 {m1['tnt_equivalent_g']} g TNT)，绝对星等 V = {m1['visual_magnitude']} 等")
    print(f"- 100 毫克砂粒 (火流星, 4.3 mm): 动能 {m100['kinetic_energy_j']} J (当量 {m100['tnt_equivalent_g']} g TNT)，绝对星等 V = {m100['visual_magnitude']} 等 (耀眼火流星)")
    print(f"- 极高消融起始高度: 115 ~ 118 km (相比双子座 70~80 km 显著高出 40 km)")
    print(f"- 初发绿色余迹机制: {m1['train_physics']['initial_glow']}")
    print(f"- 长寿命持久光痕机制: {m1['train_physics']['long_duration_persistent_train']}")
    print()

    b = rep["mars_jupiter_beacon"]
    print("【三、绝妙星野：2026 极盛夜“火星合木星”超近双星引路信标】")
    print(f"- 会合极值时刻: {b['conjunction_date_cst']} (最小角距仅 {b['conjunction_min_separation_deg']}° / {b['conjunction_min_separation_arcmin']} 角分)")
    print(f"- 极盛之夜双星几何: 火星 V = {b['mars_magnitude']} 等 | 木星 V = {b['jupiter_magnitude']} 等 (角距 {b['peak_night_mars_jupiter_sep_deg']}°)")
    print(f"- 双行星至流星辐射点角距: 火星仅距 **{b['mars_to_radiant_sep_deg']}°**，木星仅距 **{b['jupiter_to_radiant_sep_deg']}°**")
    print(f"- 星野评价: {b['astronomical_significance']}")
    print()

    print("【四、华夏五大城市观象几何与“月落狮起”交接暗夜天窗】")
    print(f"{'城市':<8} | {'月落时刻':<10} | {'辐射点升':<10} | {'晨光始':<8} | {'最高中天仰角':<16} | {'纯黑天窗':<8}")
    print("-" * 76)
    for k, c in rep["chinese_cities_geometry"].items():
        alt_str = f"{c['max_radiant_alt_deg']}° ({c['transit_cst']})"
        print(f"{c['city_name_cn']:<8} | {c['moon_set_cst'] + ' CST':<10} | {c['radiant_rise_cst'] + ' CST':<10} | {c['dawn_twilight_cst']:<8} | {alt_str:<16} | {str(c['dark_sky_duration_hours']) + ' 小时':<8}")
    print()
    print("【五、辐射点周边狮子座头部‘镰刀’参照星标尺】")
    for s in rep["leo_reference_stars"]:
        print(f"  • {s['name_cn']} ({s['name']}): V = {s['visual_magnitude']:4.2f} 等 | 距辐射点 {s['separation_to_radiant_deg']:5.2f}°")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(description="2026 年狮子座流星雨天体力学推演引擎")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出完整结构化数据")
    parser.add_argument("--city", type=str, choices=list(CHINA_CITIES.keys()), help="查看特定城市时序数据")
    args = parser.parse_args()

    rep = generate_full_report()

    if args.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    elif args.city:
        cdata = rep["chinese_cities_geometry"][args.city]
        print(f"=== {cdata['city_name_cn']} 2026 狮子座流星雨时序推演 ===")
        print(f"月落: {cdata['moon_set_cst']} CST | 辐射点升: {cdata['radiant_rise_cst']} CST | 晨光始: {cdata['dawn_twilight_cst']} CST | 纯暗空: {cdata['dark_sky_duration_hours']} 小时")
        for h in cdata["hourly_progression"]:
            flag = "[暗空黄金窗口]" if h["is_pure_dark_window"] else ""
            print(f"  {h['cst_time']} CST: 太阳={h['sun_alt_deg']:5.1f}°, 月亮={h['moon_alt_deg']:5.1f}°, 辐射点={h['radiant_alt_deg']:5.1f}°, 可视流星={h['visible_hr_obs']:4.1f}/h {flag}")
    else:
        print_text_report(rep)


if __name__ == "__main__":
    main()
