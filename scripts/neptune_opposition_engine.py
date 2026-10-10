#!/usr/bin/env python3
"""
2026 年海王星冲日天体力学推演与海卫一逆行捕获动力学引擎
Neptune Opposition 2026 & Triton Retrograde Capture Dynamics Engine

天体物理与科学推演核心：
1. 2026 年冲日与近地极值：
   - 精确冲日时刻：2026-09-25 08:00:00 CST (地心黄经差严格达到 180°)。
   - 最近地心距离 (Perigee)：28.875559 AU (43.197 亿千米)，单向光行时 240.15 分钟 (4 小时 0 分 9 秒)。
   - 冲日视星等 V = +7.81 等，视直径 2.37 角秒。
2. 跨越春分点与天赤道：
   - 冲日坐标位于双鱼座 (RA 00h 13m 22s, Dec -00° 05' 55")。
   - 距离春分点 (Vernal Equinox, 00h 00m, 00° 00') 仅 3.34° (200.7')。
   - 处于海王星自 1846 年被人类发现后第二次跨越春分点周期。
3. 逆行周期与动力学跨度：
   - 留一点 (顺转逆)：2026-07-08 12:16 CST。
   - 留二点 (逆转顺)：2026-12-13 18:41 CST。
   - 逆行总历时 158.3 天 (~5.2 个月)，天球逆行角跨度达 2.80° (168.3')。
4. 海卫一 (Triton) 逆行轨道动力学与捕获演化：
   - 质量 2.14e22 kg (占海王星系统卫星总质量 99.5%)。
   - 逆行轨道倾角 156.8°，轨道半长轴 354,759 km。
   - 在 28.876 AU 冲日点处，海卫一极大角距离为 16.94 角秒 (海王星视半径的 14.3 倍)。
   - 流体洛希极限 d_fluid ≈ 55,600 km (2.26 R_N)，刚体洛希极限 d_rigid ≈ 32,800 km (1.33 R_N)。
   - 潮汐拖拽导致半长轴持续衰减，预期寿命 1.4 ~ 3.6 Gyr 后瓦解并形成媲美土星的超级光环系统。
   - 地表温度 38 K (-235°C)，旅行者 2 号探测到高达 8 km 的氮冰火山间歇泉。
5. 华夏五大城市通宵观测几何：
   - 因赤纬 Dec ≈ -0.1° 贴近天赤道，华夏全境通宵可见时长几乎严格平分为 12.0 小时。
   - 广州中天仰角 66.8°、成都 59.3°、上海 58.7°、北京 50.0°、乌鲁木齐 46.1°。
"""

import sys
import math
import json
import argparse
import datetime
from typing import Dict, Any, List, Tuple

import ephem

# 物理常数与海王星/海卫一系统参数
AU_KM = 149597870.7
LIGHT_SPEED_KM_S = 299792.458

NEPTUNE_SYSTEM = {
    "name": "Neptune",
    "chinese_name": "海王星",
    "discovery_date": "1846-09-23",
    "discoverers": "Urbain Le Verrier & Johann Gottfried Galle",
    "equatorial_radius_km": 24764.0,
    "polar_radius_km": 24341.0,
    "mean_radius_km": 24622.0,
    "mass_kg": 1.02413e26,
    "bulk_density_g_cm3": 1.638,
    "rotation_period_hours": 16.11,
    "orbital_period_years": 164.79,
    "atmospheric_methane_percent": 1.5,
    "geometric_albedo": 0.442,
    "rings": ["Galle (41900 km)", "Le Verrier (53200 km)", "Lassell (63900 km)", "Arago (62900 km)", "Adams (62930 km, 拥有特征弧星环)"]
}

TRITON_SYSTEM = {
    "name": "Triton (Neptune I)",
    "chinese_name": "海卫一",
    "discovery_date": "1846-10-10",
    "discoverer": "William Lassell",
    "semimajor_axis_km": 354759.0,
    "orbital_period_days": -5.876854,  # 负号表示逆行
    "orbital_inclination_deg": 156.83, # 逆行轨道
    "orbital_eccentricity": 0.000016,  # 潮汐圆化后极正圆
    "radius_km": 1353.4,
    "mass_kg": 2.1408e22,
    "bulk_density_g_cm3": 2.061,
    "system_mass_percentage": 99.5,
    "v_mag": 13.5,
    "surface_temp_k": 38.0,
    "surface_temp_c": -235.15,
    "cryovolcanism_plume_height_km": 8.0,
    "cryovolcanism_drift_km": 150.0,
    "capture_origin": "Kuiper Belt Binary Exchange Capture",
    "roche_limit_fluid_km": 55600.0,
    "roche_limit_rigid_km": 32800.0,
    "decay_lifetime_gyr_range": [1.4, 3.6]
}

DEFAULT_CITIES = {
    "Shanghai": {"name": "上海", "lat": "31.2304", "lon": "121.4737", "elevation": 10},
    "Beijing": {"name": "北京", "lat": "39.9042", "lon": "116.4074", "elevation": 50},
    "Guangzhou": {"name": "广州", "lat": "23.1291", "lon": "113.2644", "elevation": 20},
    "Chengdu": {"name": "成都", "lat": "30.5728", "lon": "104.0668", "elevation": 500},
    "Urumqi": {"name": "乌鲁木齐", "lat": "43.8256", "lon": "87.6168", "elevation": 800}
}

SPRING_EQUINOX_J2000 = {
    "name": "春分点 (Vernal Equinox)",
    "ra": "00:00:00",
    "dec": "+00:00:00"
}

GUIDE_STARS = {
    "29 Psc": {"ra": "00:14:55.9", "dec": "-03:01:40", "mag": 5.13},
    "24 Psc": {"ra": "00:09:59.2", "dec": "-03:17:28", "mag": 5.93},
    "27 Psc": {"ra": "00:11:32.0", "dec": "-03:28:02", "mag": 4.88},
    "20 Psc": {"ra": "00:02:57.6", "dec": "+02:52:50", "mag": 5.49},
    "33 Psc": {"ra": "00:16:05.9", "dec": "-05:37:42", "mag": 4.61}
}


def cst_to_utc(dt_cst: datetime.datetime) -> datetime.datetime:
    return dt_cst - datetime.timedelta(hours=8)


def utc_to_cst(dt_utc: datetime.datetime) -> datetime.datetime:
    return dt_utc + datetime.timedelta(hours=8)


def get_ecliptic_separation(t: ephem.Date) -> float:
    """计算海王星与太阳的地心黄经差 (0 ~ 360 deg)"""
    obs = ephem.Observer()
    obs.date = t
    nep = ephem.Neptune(obs)
    sun = ephem.Sun(obs)
    ecl_n = ephem.Ecliptic(nep)
    ecl_s = ephem.Ecliptic(sun)
    diff = (float(ecl_n.lon) - float(ecl_s.lon)) * 180.0 / math.pi
    return (diff + 360.0) % 360.0


def compute_opposition_point() -> Dict[str, Any]:
    """高精度求解 2026 海王星精确冲日时刻、近地心极值与光行时"""
    l = ephem.Date("2026-09-24 12:00:00")
    r = ephem.Date("2026-09-25 12:00:00")
    for _ in range(50):
        mid = (l + r) / 2
        diff = get_ecliptic_separation(mid)
        if diff < 180.0:
            l = mid
        else:
            r = mid
    opp_date = (l + r) / 2
    opp_utc = ephem.Date(opp_date).datetime().replace(tzinfo=datetime.timezone.utc)
    opp_cst = opp_utc.astimezone(datetime.timezone(datetime.timedelta(hours=8)))

    # 计算冲日时刻海王星物理参数
    obs = ephem.Observer()
    obs.date = opp_date
    nep = ephem.Neptune(obs)
    dist_au = float(nep.earth_distance)
    dist_km = dist_au * AU_KM
    light_time_s = dist_km / LIGHT_SPEED_KM_S
    light_time_m = light_time_s / 60.0

    # 与春分点角距离
    eq_ra = ephem.hours(SPRING_EQUINOX_J2000["ra"])
    eq_dec = ephem.degrees(SPRING_EQUINOX_J2000["dec"])
    sep_equinox_rad = ephem.separation((nep.ra, nep.dec), (eq_ra, eq_dec))
    sep_equinox_deg = math.degrees(sep_equinox_rad)

    return {
        "opposition_time_cst": opp_cst.strftime("%Y-%m-%d %H:%M:%S"),
        "opposition_time_utc": opp_utc.strftime("%Y-%m-%d %H:%M:%S"),
        "earth_distance_au": round(dist_au, 6),
        "earth_distance_km": round(dist_km, 1),
        "light_travel_time_seconds": round(light_time_s, 2),
        "light_travel_time_minutes": round(light_time_m, 2),
        "v_magnitude": round(float(nep.mag), 2),
        "angular_diameter_arcsec": round(float(nep.size), 2),
        "ra_j2000": str(nep.ra),
        "dec_j2000": str(nep.dec),
        "ra_deg": round(math.degrees(float(nep.ra)), 4),
        "dec_deg": round(math.degrees(float(nep.dec)), 4),
        "equinox_separation_deg": round(sep_equinox_deg, 2),
        "equinox_separation_arcmin": round(sep_equinox_deg * 60.0, 1),
    }


def compute_retrograde_cycle() -> Dict[str, Any]:
    """求解 2026 年海王星逆行周期与留点"""
    def daily_ra_motion(date):
        obs = ephem.Observer()
        obs.date = date - 0.5
        n1 = ephem.Neptune(obs)
        obs.date = date + 0.5
        n2 = ephem.Neptune(obs)
        return float(n2.ra) - float(n1.ra)

    # 留一点 (顺转逆, ~2026-07)
    t = ephem.Date("2026-06-20")
    s1_date = None
    while t < ephem.Date("2026-07-25"):
        if daily_ra_motion(t) >= 0 and daily_ra_motion(t + 0.2) < 0:
            s1_date = t
            break
        t += 0.2

    l, r = s1_date - 1.0, s1_date + 1.0
    for _ in range(35):
        mid = (l + r) / 2
        if daily_ra_motion(mid) > 0:
            l = mid
        else:
            r = mid
    s1_utc = ephem.Date(mid).datetime().replace(tzinfo=datetime.timezone.utc)
    s1_cst = s1_utc.astimezone(datetime.timezone(datetime.timedelta(hours=8)))

    # 留二点 (逆转顺, ~2026-12)
    t = ephem.Date("2026-11-25")
    s2_date = None
    while t < ephem.Date("2026-12-25"):
        if daily_ra_motion(t) <= 0 and daily_ra_motion(t + 0.2) > 0:
            s2_date = t
            break
        t += 0.2

    l, r = s2_date - 1.0, s2_date + 1.0
    for _ in range(35):
        mid = (l + r) / 2
        if daily_ra_motion(mid) < 0:
            l = mid
        else:
            r = mid
    s2_utc = ephem.Date(mid).datetime().replace(tzinfo=datetime.timezone.utc)
    s2_cst = s2_utc.astimezone(datetime.timezone(datetime.timedelta(hours=8)))

    # 计算逆行角跨度
    obs = ephem.Observer()
    obs.date = ephem.Date(s1_utc)
    n1 = ephem.Neptune(obs)
    obs.date = ephem.Date(s2_utc)
    n2 = ephem.Neptune(obs)
    arc_rad = ephem.separation((n1.ra, n1.dec), (n2.ra, n2.dec))
    arc_deg = math.degrees(arc_rad)
    retrograde_days = (s2_cst - s1_cst).total_seconds() / 86400.0

    return {
        "stationary_1_cst": s1_cst.strftime("%Y-%m-%d %H:%M:%S"),
        "stationary_2_cst": s2_cst.strftime("%Y-%m-%d %H:%M:%S"),
        "retrograde_duration_days": round(retrograde_days, 1),
        "retrograde_duration_months": round(retrograde_days / 30.4375, 2),
        "retrograde_arc_deg": round(arc_deg, 2),
        "retrograde_arc_arcmin": round(arc_deg * 60.0, 1),
    }


def compute_triton_dynamics(earth_dist_au: float) -> Dict[str, Any]:
    """求解海卫一 (Triton) 逆行轨道几何、极大视距与洛希极限演化"""
    a_km = TRITON_SYSTEM["semimajor_axis_km"]
    dist_km = earth_dist_au * AU_KM
    # 极大视投影角距 (弧度 -> 角秒)
    theta_rad = a_km / dist_km
    theta_arcsec = theta_rad * 206264.806

    # 海王星视半径 (角秒)
    r_nep_km = NEPTUNE_SYSTEM["mean_radius_km"]
    r_nep_arcsec = (r_nep_km / dist_km) * 206264.806
    separation_in_planet_radii = theta_arcsec / r_nep_arcsec

    # 理论洛希极限解析
    rho_n = NEPTUNE_SYSTEM["bulk_density_g_cm3"]
    rho_t = TRITON_SYSTEM["bulk_density_g_cm3"]
    # 流体洛希极限: d = 2.44 * R_N * (rho_n / rho_t)^(1/3)
    fluid_roche_km = 2.44 * r_nep_km * ((rho_n / rho_t) ** (1.0 / 3.0))
    # 刚体洛希极限: d = 1.44 * R_N * (rho_n / rho_t)^(1/3)
    rigid_roche_km = 1.44 * r_nep_km * ((rho_n / rho_t) ** (1.0 / 3.0))

    return {
        "semimajor_axis_km": a_km,
        "max_angular_separation_arcsec": round(theta_arcsec, 2),
        "separation_in_planet_radii": round(separation_in_planet_radii, 1),
        "orbital_inclination_deg": TRITON_SYSTEM["orbital_inclination_deg"],
        "orbital_period_days": TRITON_SYSTEM["orbital_period_days"],
        "v_magnitude": TRITON_SYSTEM["v_mag"],
        "mass_ratio_system_percent": TRITON_SYSTEM["system_mass_percentage"],
        "fluid_roche_limit_km": round(fluid_roche_km, 1),
        "rigid_roche_limit_km": round(rigid_roche_km, 1),
        "fluid_roche_in_planet_radii": round(fluid_roche_km / r_nep_km, 2),
        "current_distance_to_fluid_roche_ratio": round(a_km / fluid_roche_km, 2),
        "decay_lifetime_min_gyr": TRITON_SYSTEM["decay_lifetime_gyr_range"][0],
        "decay_lifetime_max_gyr": TRITON_SYSTEM["decay_lifetime_gyr_range"][1],
        "surface_temp_k": TRITON_SYSTEM["surface_temp_k"],
        "cryovolcanism_plume_height_km": TRITON_SYSTEM["cryovolcanism_plume_height_km"],
    }


def compute_guide_star_separations() -> List[Dict[str, Any]]:
    """求解冲日点与双鱼座周边对比导星的角距离"""
    nep_ra = ephem.hours("00:13:22.38")
    nep_dec = ephem.degrees("-00:05:54.9")
    results = []
    for name, star in GUIDE_STARS.items():
        s_ra = ephem.hours(star["ra"])
        s_dec = ephem.degrees(star["dec"])
        sep_deg = math.degrees(ephem.separation((nep_ra, nep_dec), (s_ra, s_dec)))
        results.append({
            "name": name,
            "v_mag": star["mag"],
            "ra": star["ra"],
            "dec": star["dec"],
            "separation_deg": round(sep_deg, 2),
            "separation_arcmin": round(sep_deg * 60.0, 1),
        })
    results.sort(key=lambda x: x["separation_deg"])
    return results


def compute_city_geometry() -> Dict[str, Any]:
    """求解 2026-09-25 冲日夜华夏主要城市观象几何"""
    city_reports = {}
    nep = ephem.Neptune()
    for city_key, city in DEFAULT_CITIES.items():
        obs = ephem.Observer()
        obs.lat = city["lat"]
        obs.lon = city["lon"]
        obs.elevation = city["elevation"]
        obs.date = ephem.Date("2026-09-25 08:00:00")  # UTC

        r = obs.next_rising(nep)
        t = obs.next_transit(nep)
        s = obs.next_setting(nep)

        r_cst = r.datetime().replace(tzinfo=datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=8)))
        t_cst = t.datetime().replace(tzinfo=datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=8)))
        s_cst = s.datetime().replace(tzinfo=datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=8)))

        obs.date = t
        nep.compute(obs)
        max_alt = math.degrees(float(nep.alt))
        vis_hours = (s_cst - r_cst).total_seconds() / 3600.0

        city_reports[city_key] = {
            "name": city["name"],
            "rising_cst": r_cst.strftime("%H:%M"),
            "transit_cst": t_cst.strftime("%H:%M"),
            "setting_cst": s_cst.strftime("%H:%M"),
            "transit_altitude_deg": round(max_alt, 1),
            "visibility_hours": round(vis_hours, 1)
        }
    return city_reports


def generate_full_report() -> Dict[str, Any]:
    opp = compute_opposition_point()
    retro = compute_retrograde_cycle()
    triton = compute_triton_dynamics(opp["earth_distance_au"])
    stars = compute_guide_star_separations()
    cities = compute_city_geometry()

    return {
        "title": "2026 年海王星冲日天体力学推演与海卫一逆行捕获动力学综合矩阵",
        "generated_cst": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "neptune_opposition": opp,
        "retrograde_cycle": retro,
        "triton_dynamics": triton,
        "guide_stars": stars,
        "city_observational_geometry": cities
    }


def print_text_report(data: Dict[str, Any]) -> None:
    opp = data["neptune_opposition"]
    retro = data["retrograde_cycle"]
    triton = data["triton_dynamics"]
    stars = data["guide_stars"]
    cities = data["city_observational_geometry"]

    print("=" * 80)
    print(" 2026 年海王星冲日天体力学推演与海卫一逆行捕获动力学综合报告 ")
    print("=" * 80)
    print(f"报告生成时间: {data['generated_cst']} CST\n")

    print("【一、精确冲日时刻与天体测量极值】")
    print(f"- 精确冲日时刻 (CST): {opp['opposition_time_cst']} (地心黄经差 180°)")
    print(f"- 最近地心距离 (Perigee): {opp['earth_distance_au']} AU ({opp['earth_distance_km']:,} km)")
    print(f"- 单向光行时间: {opp['light_travel_time_minutes']} 分钟 ({opp['light_travel_time_seconds']} 秒, 约 4.0 小时)")
    print(f"- 视星等与视直径: V = +{opp['v_magnitude']} 等 | 视直径 {opp['angular_diameter_arcsec']}\"")
    print(f"- 天球坐标 (J2000): RA {opp['ra_j2000']} | Dec {opp['dec_j2000']} (双鱼座)")
    print(f"- 春分点角距离: 距春分点仅 {opp['equinox_separation_deg']}° ({opp['equinox_separation_arcmin']} 角分)")
    print()

    print("【二、逆行周期与动力学跨度】")
    print(f"- 留一点 (顺转逆 CST): {retro['stationary_1_cst']}")
    print(f"- 留二点 (逆转顺 CST): {retro['stationary_2_cst']}")
    print(f"- 逆行总历时: {retro['retrograde_duration_days']} 天 (~{retro['retrograde_duration_months']} 个月)")
    print(f"- 天球逆行角跨度: {retro['retrograde_arc_deg']}° ({retro['retrograde_arc_arcmin']} 角分)")
    print()

    print("【三、海卫一 (Triton) 逆行轨道动力学与潮汐衰减演化】")
    print(f"- 轨道半长轴: {triton['semimajor_axis_km']:,} km | 公转周期: {triton['orbital_period_days']} 天 (负号表示逆行)")
    print(f"- 轨道倾角: {triton['orbital_inclination_deg']}° (经典逆行轨道，柯伊伯带双星交换捕获证据)")
    print(f"- 冲日点极大视投影角距: {triton['max_angular_separation_arcsec']}\" ({triton['separation_in_planet_radii']} 倍海王星视半径)")
    print(f"- 视星等: V = +{triton['v_magnitude']} 等 (业余 200mm 口径望远镜 CCD/肉眼挑战目标)")
    print(f"- 质量占海王星全系统卫星总质量: {triton['mass_ratio_system_percent']}%")
    print(f"- 洛希极限计算: 流体 {triton['fluid_roche_limit_km']:,} km ({triton['fluid_roche_in_planet_radii']} R_N) | 刚体 {triton['rigid_roche_limit_km']:,} km")
    print(f"- 轨道演化与终局: 潮汐减速正持续拉近轨道，预计 {triton['decay_lifetime_min_gyr']} ~ {triton['decay_lifetime_max_gyr']} Gyr 后突破洛希极限瓦解为超级光环")
    print(f"- 极端低温与冰火山: 表面温度 {triton['surface_temp_k']} K (-235.2 °C)，活跃着喷高 {triton['cryovolcanism_plume_height_km']} km 的固态氮冰喷泉")
    print()

    print("【四、双鱼座周边对比导星跳板】")
    print(f"{'对比星':<12} | {'视星等':<6} | {'赤道坐标 (J2000)':<25} | {'角距离 (deg / arcmin)':<20}")
    print("-" * 70)
    for s in stars:
        coord = f"{s['ra']}  {s['dec']}"
        sep = f"{s['separation_deg']}° ({s['separation_arcmin']}')"
        print(f"{s['name']:<12} | {s['v_mag']:<6} | {coord:<25} | {sep:<20}")
    print()

    print("【五、华夏主要城市通宵观测几何 (2026-09-25 冲日夜)】")
    print(f"{'城市':<10} | {'升起 (CST)':<10} | {'中天 (CST)':<10} | {'中天仰角':<10} | {'落下 (CST)':<10} | {'通宵可见':<10}")
    print("-" * 70)
    for c in cities.values():
        print(f"{c['name']:<10} | {c['rising_cst']:<10} | {c['transit_cst']:<10} | {c['transit_altitude_deg']}°{'':<5} | {c['setting_cst']:<10} | {c['visibility_hours']} 小时")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(description="2026 Neptune Opposition & Triton Dynamics Engine")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出数据矩阵")
    args = parser.parse_args()

    data = generate_full_report()
    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print_text_report(data)


if __name__ == "__main__":
    main()
