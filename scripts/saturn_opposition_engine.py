"""
土星冲日与塞利格浪涌动力学引擎 (Saturn Opposition & Seeliger Surge Mechanics Engine)
精确推演 2026 年 10 月 4 日土星冲日的天体力学几何、光环倾角演化、
塞利格冲日浪涌效应 (Seeliger Opposition Surge) 辐射传输分解、
主要卫星视平面投影分布以及中国主要城市通宵观测窗口。
"""

import datetime
import math
from typing import Dict, List, Any, Tuple
import ephem

UTC = datetime.timezone.utc
TZ_CST = datetime.timezone(datetime.timedelta(hours=8))
KM_PER_AU = 149597870.7

# IAU 土星环北极 J2000 赤道坐标
ALPHA_0_DEG = 40.589
DELTA_0_DEG = 83.537
ALPHA_0_RAD = math.radians(ALPHA_0_DEG)
DELTA_0_RAD = math.radians(DELTA_0_DEG)

# 黄赤交角 J2000
EPS_RAD = math.radians(23.4392911)

# 土星及其光环系统物理参数 (千米)
SATURN_R_EQ = 60268.0      # 赤道半径
SATURN_R_POL = 54364.0     # 极半径
RING_A_OUT = 136775.0      # A 环外缘
RING_A_IN = 122170.0       # A 环内缘 (卡西尼缝外界)
CASSINI_WIDTH = 4590.0     # 卡西尼环缝宽度 (117,580 ~ 122,170 km)
RING_B_OUT = 117580.0      # B 环外缘
RING_B_IN = 92000.0        # B 环内缘
RING_C_IN = 74658.0        # C 环内缘 (可丽薄环)

# 卫星标准冲日光度
MOON_MAGS = {
    "Titan": 8.4,
    "Rhea": 9.7,
    "Tethys": 10.2,
    "Dione": 10.4,
    "Iapetus": 11.2,
}


def to_cst(ephem_date: ephem.Date) -> datetime.datetime:
    """将 ephem.Date 转换为 CST (UTC+8) datetime。"""
    return ephem_date.datetime().replace(tzinfo=UTC).astimezone(TZ_CST)


def get_observer(lat: str = "31.2304", lon: str = "121.4737", elevation: float = 4.0) -> ephem.Observer:
    """获取指定经纬度的地表观测站（默认上海）。"""
    obs = ephem.Observer()
    obs.lat = str(lat)
    obs.lon = str(lon)
    obs.elevation = elevation
    return obs


def compute_ring_geometry(saturn: ephem.Saturn, d: ephem.Date) -> Dict[str, float]:
    """
    基于 IAU J2000 土星自转轴北极坐标，精确解算光环几何：
    - 地球视倾角 B (Sub-Earth latitude，环开度)
    - 太阳照角 B_prime (Sub-Solar latitude)
    - 光环主轴方位角 P_ring (Position angle of ring major axis)
    - 光环北极方位角 P_pole
    - A/B/C 环与卡西尼缝在天空切平面上的长短轴视尺寸（角秒）
    """
    ra = float(saturn.ra)
    dec = float(saturn.dec)
    delta_au = saturn.earth_distance

    # 1. 地球视纬度 B (Sub-Earth latitude)
    sin_B = -math.sin(DELTA_0_RAD) * math.sin(dec) - math.cos(DELTA_0_RAD) * math.cos(dec) * math.cos(ra - ALPHA_0_RAD)
    sin_B = max(-1.0, min(1.0, sin_B))
    B_rad = math.asin(sin_B)
    B_deg = math.degrees(B_rad)

    # 2. 太阳照射纬度 B' (Sub-Solar latitude)
    # 太阳在土星处的日心黄道坐标：longitude = saturn.hlon + pi, latitude = -saturn.hlat
    l_sun = saturn.hlon + math.pi
    b_sun = -saturn.hlat
    sin_dec_sun = math.sin(b_sun) * math.cos(EPS_RAD) + math.cos(b_sun) * math.sin(EPS_RAD) * math.sin(l_sun)
    cos_dec_cos_ra = math.cos(b_sun) * math.cos(l_sun)
    cos_dec_sin_ra = -math.sin(b_sun) * math.sin(EPS_RAD) + math.cos(b_sun) * math.cos(EPS_RAD) * math.sin(l_sun)
    dec_sun = math.asin(max(-1.0, min(1.0, sin_dec_sun)))
    ra_sun = math.atan2(cos_dec_sin_ra, cos_dec_cos_ra)

    sin_B_prime = -math.sin(DELTA_0_RAD) * math.sin(dec_sun) - math.cos(DELTA_0_RAD) * math.cos(dec_sun) * math.cos(ra_sun - ALPHA_0_RAD)
    sin_B_prime = max(-1.0, min(1.0, sin_B_prime))
    B_prime_rad = math.asin(sin_B_prime)
    B_prime_deg = math.degrees(B_prime_rad)

    # 3. 方位角 Position Angle P of North Pole & Major Axis
    y = math.cos(DELTA_0_RAD) * math.sin(ALPHA_0_RAD - ra)
    x = math.sin(DELTA_0_RAD) * math.cos(dec) - math.cos(DELTA_0_RAD) * math.sin(dec) * math.cos(ALPHA_0_RAD - ra)
    P_pole_deg = (math.degrees(math.atan2(y, x)) + 360.0) % 360.0
    P_ring_major = (P_pole_deg + 90.0) % 180.0  # 环主轴东西走向方位角 (0~180°)

    # 4. 角尺寸计算 (arcseconds)
    # theta_arcsec = (2 * R_km / (delta_au * KM_PER_AU)) * (180 * 3600 / pi)
    rad_to_arcsec = 180.0 * 3600.0 / math.pi
    dist_km = delta_au * KM_PER_AU
    sin_abs_B = abs(sin_B)

    sat_eq_major = (2.0 * SATURN_R_EQ / dist_km) * rad_to_arcsec
    sat_pol_minor = (2.0 * SATURN_R_POL / dist_km) * rad_to_arcsec

    ring_a_major = (2.0 * RING_A_OUT / dist_km) * rad_to_arcsec
    ring_a_minor = ring_a_major * sin_abs_B

    ring_b_major = (2.0 * RING_B_OUT / dist_km) * rad_to_arcsec
    ring_b_minor = ring_b_major * sin_abs_B

    cassini_major = (2.0 * CASSINI_WIDTH / dist_km) * rad_to_arcsec
    cassini_minor = cassini_major * sin_abs_B

    return {
        "sub_earth_lat_deg": round(B_deg, 3),
        "sub_solar_lat_deg": round(B_prime_deg, 3),
        "ring_opening_abs_deg": round(abs(B_deg), 3),
        "pole_position_angle_deg": round(P_pole_deg, 2),
        "ring_major_axis_pa_deg": round(P_ring_major, 2),
        "saturn_equatorial_diam_arcsec": round(sat_eq_major, 2),
        "saturn_polar_diam_arcsec": round(sat_pol_minor, 2),
        "ring_a_major_arcsec": round(ring_a_major, 2),
        "ring_a_minor_arcsec": round(ring_a_minor, 2),
        "ring_b_major_arcsec": round(ring_b_major, 2),
        "ring_b_minor_arcsec": round(ring_b_minor, 2),
        "cassini_division_width_arcsec": round(cassini_major, 3),
        "cassini_division_minor_arcsec": round(cassini_minor, 3),
    }


def compute_phase_angle(saturn: ephem.Saturn, sun: ephem.Sun) -> float:
    """计算日-土-地相位角 alpha (度)。"""
    r = saturn.sun_distance
    delta = saturn.earth_distance
    R = sun.earth_distance
    cos_alpha = (r**2 + delta**2 - R**2) / (2.0 * r * delta)
    cos_alpha = max(-1.0, min(1.0, cos_alpha))
    return math.degrees(math.acos(cos_alpha))


def compute_seeliger_photometry(
    r_au: float,
    delta_au: float,
    alpha_deg: float,
    B_deg: float
) -> Dict[str, float]:
    """
    塞利格冲日浪涌效应 (Seeliger Opposition Surge) 辐射度分解：
    - Astronomical Almanac 标准视星等公式：
      V = -8.88 + 5 log10(r * delta) + 0.044 * alpha - 2.60 * sin|B| + 1.25 * sin^2(B)
    - 本体 (Globe) 星等贡献
    - 光环 (Ring) 几何展开增亮贡献
    - 冲日浪涌增量 (Shadow Hiding + Coherent Backscatter)
    """
    sin_abs_B = math.sin(math.radians(abs(B_deg)))
    dist_term = 5.0 * math.log10(r_au * delta_au)
    phase_term = 0.044 * alpha_deg
    ring_geometric_term = -2.60 * sin_abs_B + 1.25 * (sin_abs_B ** 2)

    # 1. AA 标准总星等
    v_total = -8.88 + dist_term + phase_term + ring_geometric_term

    # 2. 土星本体星等 (若无光环 B=0)
    v_globe_alone = -8.88 + dist_term + phase_term

    # 3. 光环几何反射增量 (星等与通量比)
    delta_m_ring = ring_geometric_term
    ring_flux_ratio = (10.0 ** (-0.4 * delta_m_ring)) - 1.0  # 相对本体多出的通量比

    # 4. 塞利格冲日浪涌非线性峰值模型 (Hapke / Deau 2013 双峰项)
    # 当 alpha 从 6° 下降到当前 alpha 时的非线性陡峭跃升
    # 阴影隐藏项 (SH) 半高宽 ~ 1.3°，相干背向散射 (CB) 半高宽 ~ 0.20°
    h_sh = math.tan(math.radians(1.3 / 2.0))
    h_cb = math.tan(math.radians(0.20 / 2.0))
    tan_half_a = math.tan(math.radians(alpha_deg / 2.0))
    tan_half_ref = math.tan(math.radians(6.0 / 2.0))

    b_sh_current = 0.16 / (1.0 + tan_half_a / h_sh)
    b_sh_ref = 0.16 / (1.0 + tan_half_ref / h_sh)
    surge_sh = b_sh_current - b_sh_ref

    b_cb_current = 0.12 / (1.0 + tan_half_a / h_cb)
    b_cb_ref = 0.12 / (1.0 + tan_half_ref / h_cb)
    surge_cb = b_cb_current - b_cb_ref

    total_surge_mag = surge_sh + surge_cb

    return {
        "v_total_aa": round(v_total, 3),
        "v_globe_alone": round(v_globe_alone, 3),
        "ring_brightness_boost_mag": round(abs(delta_m_ring), 3),
        "ring_to_globe_flux_ratio_pct": round(ring_flux_ratio * 100.0, 1),
        "surge_shadow_hiding_mag": round(surge_sh, 3),
        "surge_coherent_backscatter_mag": round(surge_cb, 3),
        "total_seeliger_surge_mag": round(total_surge_mag, 3),
        "apparent_mag_with_surge": round(v_total - total_surge_mag * (sin_abs_B / 0.1325), 3)
    }


def compute_saturnian_moons(d: ephem.Date, sat_radius_arcsec: float) -> List[Dict[str, Any]]:
    """
    计算五大主要土星卫星（Titan, Rhea, Tethys, Dione, Iapetus）在冲日时刻的视投影坐标。
    x, y 为以土星赤道半径为单位的视切平面坐标 (+x: 东, -x: 西, +y: 北, -y: 南)。
    """
    moon_objects = [
        ("Titan", ephem.Titan(d)),
        ("Rhea", ephem.Rhea(d)),
        ("Tethys", ephem.Tethys(d)),
        ("Dione", ephem.Dione(d)),
        ("Iapetus", ephem.Iapetus(d)),
    ]

    records = []
    for name, m in moon_objects:
        x = float(m.x)
        y = float(m.y)
        z = float(m.z)
        r_proj = math.sqrt(x**2 + y**2)
        sep_arcsec = r_proj * sat_radius_arcsec
        pa_deg = (math.degrees(math.atan2(x, y)) + 360.0) % 360.0
        side = "East" if x > 0 else "West"

        records.append({
            "name": name,
            "mag": MOON_MAGS.get(name, 10.0),
            "x_sat_radius": round(x, 2),
            "y_sat_radius": round(y, 2),
            "z_line_of_sight": round(z, 2),
            "separation_arcsec": round(sep_arcsec, 1),
            "position_angle_deg": round(pa_deg, 1),
            "side": side,
            "visibility": "双筒/微型望远镜可见" if name == "Titan" else "小型天文望远镜可见"
        })

    # 按与土星角距排序
    records.sort(key=lambda item: item["separation_arcsec"])
    return records


def find_saturn_opposition_event(year: int = 2026) -> Dict[str, Any]:
    """
    数值搜索指定年份土星冲日核心事件：
    - 冲日时刻 (Opposition: 地日黄经差 180°)
    - 近地点时刻 (Perigee: 地土距离极小值)
    - 最小相位角时刻 (Minimum Phase Angle)
    """
    sun = ephem.Sun()
    saturn = ephem.Saturn()

    start_utc = datetime.datetime(year, 9, 20, 0, 0, 0, tzinfo=UTC)
    total_minutes = 25 * 24 * 60

    min_lon_diff = 999.0
    opp_time = None

    min_dist_au = 999.0
    perigee_time = None

    min_alpha = 999.0
    min_alpha_time = None

    for m in range(0, total_minutes, 2):
        t = start_utc + datetime.timedelta(minutes=m)
        d = ephem.Date(t)
        sun.compute(d)
        saturn.compute(d)

        # 黄经差
        sun_lon = float(ephem.Ecliptic(sun).lon)
        sat_lon = float(ephem.Ecliptic(saturn).lon)
        diff = abs((sat_lon - sun_lon) % (2.0 * math.pi) - math.pi)
        if diff < min_lon_diff:
            min_lon_diff = diff
            opp_time = t

        # 地距
        if saturn.earth_distance < min_dist_au:
            min_dist_au = saturn.earth_distance
            perigee_time = t

        # 相位角
        alpha = compute_phase_angle(saturn, sun)
        if alpha < min_alpha:
            min_alpha = alpha
            min_alpha_time = t

    # 冲日时刻精密几何解算
    d_opp = ephem.Date(opp_time)
    saturn.compute(d_opp)
    sun.compute(d_opp)
    alpha_at_opp = compute_phase_angle(saturn, sun)
    ring_geom = compute_ring_geometry(saturn, d_opp)
    photometry = compute_seeliger_photometry(
        saturn.sun_distance,
        saturn.earth_distance,
        alpha_at_opp,
        ring_geom["sub_earth_lat_deg"]
    )
    moons = compute_saturnian_moons(d_opp, ring_geom["saturn_equatorial_diam_arcsec"] / 2.0)

    return {
        "year": year,
        "opposition_time_cst": opp_time.astimezone(TZ_CST).strftime("%Y-%m-%d %H:%M:%S"),
        "perigee_time_cst": perigee_time.astimezone(TZ_CST).strftime("%Y-%m-%d %H:%M:%S"),
        "min_distance_au": round(min_dist_au, 6),
        "min_distance_km": int(round(min_dist_au * KM_PER_AU)),
        "min_phase_angle_deg": round(min_alpha, 4),
        "min_phase_angle_arcmin": round(min_alpha * 60.0, 2),
        "min_phase_time_cst": min_alpha_time.astimezone(TZ_CST).strftime("%Y-%m-%d %H:%M:%S"),
        "constellation": ephem.constellation(saturn)[1],
        "apparent_magnitude": round(saturn.mag, 2),
        "equatorial_size_arcsec": ring_geom["saturn_equatorial_diam_arcsec"],
        "ring_geometry": ring_geom,
        "photometry_and_seeliger": photometry,
        "saturnian_moons": moons,
    }


def compute_city_observation_windows(date_str: str = "2026-10-04") -> List[Dict[str, Any]]:
    """
    计算中国代表性经纬度城市在冲日当夜的通宵观测天象窗口：
    上海、北京、广州、成都、乌鲁木齐。
    """
    cities = [
        {"city": "上海", "code": "SHA", "lat": "31.2304", "lon": "121.4737"},
        {"city": "北京", "code": "BJS", "lat": "39.9042", "lon": "116.4074"},
        {"city": "广州", "code": "CAN", "lat": "23.1291", "lon": "113.2644"},
        {"city": "成都", "code": "CTU", "lat": "30.6586", "lon": "104.0648"},
        {"city": "乌鲁木齐", "code": "URC", "lat": "43.8256", "lon": "87.6168"},
    ]

    base_dt = datetime.datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=TZ_CST)
    noon_cst = base_dt.replace(hour=12, minute=0, second=0)
    d_noon = ephem.Date(noon_cst.astimezone(UTC))

    results = []
    saturn = ephem.Saturn()
    sun = ephem.Sun()
    moon = ephem.Moon()

    for c in cities:
        obs = get_observer(c["lat"], c["lon"])
        obs.date = d_noon

        sun_set = to_cst(obs.next_setting(sun))
        sun_rise = to_cst(obs.next_rising(sun))
        sat_rise = to_cst(obs.next_rising(saturn))
        sat_tran = to_cst(obs.next_transit(saturn))
        sat_set = to_cst(obs.next_setting(saturn))

        # 上中天极大仰角
        obs.date = obs.next_transit(saturn)
        saturn.compute(obs)
        transit_alt = math.degrees(saturn.alt)

        # 月出时刻与无月夜观测时长
        obs.date = d_noon
        moon_rise = to_cst(obs.next_rising(moon))
        dark_window_hours = max(0.0, (moon_rise - sun_set).total_seconds() / 3600.0)
        total_visible_hours = (sat_set - sat_rise).total_seconds() / 3600.0

        results.append({
            "city": c["city"],
            "code": c["code"],
            "sun_set": sun_set.strftime("%H:%M"),
            "sun_rise": sun_rise.strftime("%H:%M"),
            "saturn_rise": sat_rise.strftime("%H:%M"),
            "saturn_transit": sat_tran.strftime("%H:%M"),
            "saturn_transit_alt_deg": round(transit_alt, 1),
            "saturn_set": sat_set.strftime("%H:%M"),
            "total_visible_hours": round(total_visible_hours, 1),
            "moon_rise": moon_rise.strftime("%H:%M"),
            "moonless_window_hours": round(dark_window_hours, 1),
        })

    return results


def format_text_report(opp_data: Dict[str, Any], city_data: List[Dict[str, Any]]) -> str:
    """生成格式化科学推演报告。"""
    rg = opp_data["ring_geometry"]
    ph = opp_data["photometry_and_seeliger"]
    moons = opp_data["saturnian_moons"]

    lines = []
    lines.append("=" * 72)
    lines.append("     2026 年土星冲日 (Opposition of Saturn) 与塞利格浪涌天体力学推演")
    lines.append("=" * 72)
    lines.append(f"【核心天象力学参数】")
    lines.append(f"  • 冲日时刻 (Opposition) : {opp_data['opposition_time_cst']} CST (黄经差 180.00°)")
    lines.append(f"  • 近地点时刻 (Perigee)  : {opp_data['perigee_time_cst']} CST")
    lines.append(f"  • 最近地距 (Distance)   : {opp_data['min_distance_au']} AU ({opp_data['min_distance_km']:,} km)")
    lines.append(f"  • 极小相位角 (Phase α)  : {opp_data['min_phase_angle_deg']}° ({opp_data['min_phase_angle_arcmin']}' 角分) 于 {opp_data['min_phase_time_cst']} CST")
    lines.append(f"  • 所在星座 (Constell)   : {opp_data['constellation']} (双鱼座/鲸鱼座天区)")
    lines.append(f"  • 视星等 (V-mag)        : +{opp_data['apparent_magnitude']} 等 (年度极大亮度)")
    lines.append(f"  • 本体现径 (Eq-diam)    : {opp_data['equatorial_size_arcsec']}\" 角秒\n")

    lines.append("【光环倾角演化与空间透视 (IAU J2000 旋轴定向)】")
    lines.append(f"  • 地球视倾角 (Ring Opening B) : {rg['sub_earth_lat_deg']}° (南半球光环展开朝向地球)")
    lines.append(f"  • 太阳照射角 (Sub-Solar B')   : {rg['sub_solar_lat_deg']}°")
    lines.append(f"  • 光环主轴方位角 (Major PA)   : {rg['ring_major_axis_pa_deg']}° / {rg['ring_major_axis_pa_deg'] + 180.0:.2f}° (近乎严格东西横向展开)")
    lines.append(f"  • A 环外缘视尺寸 (A-Ring)     : 长轴 {rg['ring_a_major_arcsec']}\" × 短轴 {rg['ring_a_minor_arcsec']}\"")
    lines.append(f"  • B 环外缘视尺寸 (B-Ring)     : 长轴 {rg['ring_b_major_arcsec']}\" × 短轴 {rg['ring_b_minor_arcsec']}\"")
    lines.append(f"  • 卡西尼缝视宽度 (Cassini)    : 主轴切向 {rg['cassini_division_width_arcsec']}\" (短轴投影 {rg['cassini_division_minor_arcsec']}\")\n")

    lines.append("【塞利格冲日浪涌效应 (Seeliger Opposition Surge) 辐射分解】")
    lines.append(f"  • 土星裸球本体视星等  : +{ph['v_globe_alone']} 等")
    lines.append(f"  • 光环倾角几何增亮贡献: -{ph['ring_brightness_boost_mag']} 等 (反射通量相对本体激增 +{ph['ring_to_globe_flux_ratio_pct']}%)")
    lines.append(f"  • 塞利格非线性浪涌跃升: -{ph['total_seeliger_surge_mag']} 等 (阴影隐藏 {ph['surge_shadow_hiding_mag']}等 + 相干背向散射 {ph['surge_coherent_backscatter_mag']}等)")
    lines.append(f"  • 迎光极端总视星等    : +{ph['apparent_mag_with_surge']} 等\n")

    lines.append("【冲日时刻五大主卫星视平面分布】")
    for m in moons:
        lines.append(f"  • {m['name']:<7}: 亮度 +{m['mag']} 等 | 角距 {m['separation_arcsec']:>5.1f}\" | PA {m['position_angle_deg']:>5.1f}° | 方位 {m['side']:<4} ({m['x_sat_radius']:>+5.1f} R_sat) | {m['visibility']}")
    lines.append("")

    lines.append("【中国核心台站冲日通宵观测窗口 (2026-10-04 当夜)】")
    lines.append(f"  {'城市':<4} | {'日落':<5} | {'土星升起':<5} | {'上中天 (仰角)':<14} | {'土星落下':<5} | {'总时长':<6} | {'月出':<5} | {'无月夜窗口'}")
    lines.append("  " + "-" * 68)
    for c in city_data:
        tran_str = f"{c['saturn_transit']} ({c['saturn_transit_alt_deg']}°)"
        lines.append(f"  {c['city']:<4} | {c['sun_set']:<5} | {c['saturn_rise']:<5} | {tran_str:<14} | {c['saturn_set']:<5} | {c['total_visible_hours']} h  | {c['moon_rise']:<5} | {c['moonless_window_hours']} 小时")
    lines.append("=" * 72)

    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    import json

    opp_result = find_saturn_opposition_event(2026)
    city_result = compute_city_observation_windows("2026-10-04")

    if "--json" in sys.argv:
        combined = {
            "opposition_event": opp_result,
            "city_observation_windows": city_result
        }
        print(json.dumps(combined, indent=2, ensure_ascii=False))
    else:
        print(format_text_report(opp_result, city_result))
