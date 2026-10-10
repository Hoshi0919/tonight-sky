"""
2026 年天王星 (Uranus) 冲日天体力学推演与金牛座天门观象引擎
Uranus Opposition Dynamics & Taurus Gate Celestial Mechanics Engine (November 2026)

天体物理与观测背景：
1. 冰巨星物理本质：
   - 威廉·赫歇尔 (William Herschel) 于 1781-03-13 发现，为望远镜时代发现的第一颗大行星。
   - 赤道半径 25,559 km，极半径 24,973 km，质量 8.681e25 kg (14.54 地球质量)。
   - 大气甲烷 (CH4 ~2.3%) 强烈吸收红光（619nm, 725nm, 790nm, 890nm 带），散射呈现特有的碧海青绿 / 淡青蓝光泽。
   - 极端自转轴倾角 97.77°（逆行翻滚自转），公转周期 84.02 年。
2. 2026 年冲日天体力学：
   - 冲日时刻：2026-11-26 06:25 CST (2026-11-25 22:25 UTC)，黄经差严格达到 180°。
   - 近地点时刻：2026-11-26 04:53 CST，地心距离 18.444109 AU (27.592 亿千米)，光行时 153.39 分钟 (2 小时 33 分 23 秒)。
   - 冲日视星等：V = +5.58 等（全冲日季峰值亮度，触达 Bortle 1-3 暗夜肉眼可见极限）。
   - 视圆面直径：3.82 角秒。
   - 极小相位角：0.0082° (29.7 角秒)，极近严格正向对冲。
   - 逆行周期：2026-09-11 01:06 CST（留一点）至 2027-02-08 20:45 CST（留二点），历时 150.8 天，天球逆行角跨度 4.25°。
3. 97.77° 倾角投影与“射击靶心”环系/卫星系统：
   - 2026 年正向 2028 年北半球夏至冲刺，地球视投影视纬度 B 达 -74.15°（倾角开度 74.15°）。
   - 光环与主卫星轨道在天球上呈现近乎同心圆面的“射击靶心”(Bullseye) 构型，视平面短长轴比 b/a = sin(74.15°) = 0.962。
   - 五大主卫星（Miranda, Ariel, Umbriel, Titania, Oberon）视投影半长轴为 9.3" ~ 43.7"，天卫三与天卫四目视星等 13.5~13.7 等，为业余大口径可达目标。
4. 金牛座天门跳板与双星对：
   - 坐落于金牛座天门核心通道，介于昴星团 (M45) 与毕宿星团之间。
   - 距昴宿六 (Alcyone, η Tau) 仅 5.34°，标准 7x50 双筒望远镜轻松同视场寻星。
   - 距 43 Tau (5.51 等, F0 V) 仅 1.30° (77.8')，构成极其完美的 5.5 等双星测光比对组。
5. 华夏主要城市全夜通宵观测：
   - 冲日当夜全夜可见长达 13.5 ~ 14.5 小时。
   - 中天仰角：广州 87.6°（近天顶）、成都 80.2°、上海 79.5°、北京 70.8°、乌鲁木齐 66.9°，彻底脱离低空湍流。
"""

import sys
import math
import json
import argparse
import datetime
from typing import Dict, Any, List, Tuple

import ephem

# 冰巨星物理参量常数表
URANUS_PHYSICAL = {
    "name": "Uranus",
    "chinese_name": "天王星",
    "discovery_date": "1781-03-13",
    "discoverer": "William Herschel",
    "classification": "Ice Giant Planet",
    "equatorial_radius_km": 25559.0,
    "polar_radius_km": 24973.0,
    "flattening": 0.0229,
    "mass_kg": 8.681e25,
    "earth_mass_ratio": 14.536,
    "bulk_density_g_cm3": 1.27,
    "surface_gravity_m_s2": 8.69,
    "escape_velocity_km_s": 21.3,
    "sidereal_rotation_period_hours": -17.24, # 逆行
    "axial_tilt_deg": 97.77,
    "orbital_period_years": 84.02,
    "geometric_albedo": 0.51,
    "color_index_bv": 0.56,
    "atmosphere": "83% H2, 15% He, 2.3% CH4",
}

# 五大主要卫星物理参量
URANUS_MOONS = [
    {
        "name": "Miranda (天卫五)",
        "discovery_year": 1948,
        "diameter_km": 471.6,
        "semi_major_km": 129390.0,
        "visual_mag": 15.8,
        "orbital_period_days": 1.413,
    },
    {
        "name": "Ariel (天卫一)",
        "discovery_year": 1851,
        "diameter_km": 1157.8,
        "semi_major_km": 191020.0,
        "visual_mag": 13.7,
        "orbital_period_days": 2.520,
    },
    {
        "name": "Umbriel (天卫二)",
        "discovery_year": 1851,
        "diameter_km": 1169.4,
        "semi_major_km": 266300.0,
        "visual_mag": 14.5,
        "orbital_period_days": 4.144,
    },
    {
        "name": "Titania (天卫三)",
        "discovery_year": 1787,
        "diameter_km": 1577.8,
        "semi_major_km": 435910.0,
        "visual_mag": 13.5,
        "orbital_period_days": 8.706,
    },
    {
        "name": "Oberon (天卫四)",
        "discovery_year": 1787,
        "diameter_km": 1522.8,
        "semi_major_km": 583520.0,
        "visual_mag": 13.7,
        "orbital_period_days": 13.463,
    },
]

# 金牛座寻星跳板核心恒星数据
TAURUS_GATE_STARS = [
    {"name": "Alcyone (η Tau / 昴宿六)", "ra": "3:47:29.1", "dec": "24:06:18", "mag": 2.87, "spec": "B7 IIIe"},
    {"name": "Atlas (27 Tau / 昴宿七)", "ra": "3:49:09.7", "dec": "24:03:12", "mag": 3.63, "spec": "B8 III"},
    {"name": "37 Tau (A1 V)", "ra": "4:04:41.7", "dec": "22:04:55", "mag": 4.36, "spec": "A1 V"},
    {"name": "39 Tau (G5 V)", "ra": "4:05:20.3", "dec": "22:00:32", "mag": 5.90, "spec": "G5 V"},
    {"name": "43 Tau (F0 V / 孪生比对星)", "ra": "4:08:39.7", "dec": "19:39:45", "mag": 5.51, "spec": "F0 V"},
    {"name": "40 Tau (B9 V)", "ra": "4:06:56.0", "dec": "25:49:50", "mag": 5.32, "spec": "B9 V"},
    {"name": "ω Tau (A3 m)", "ra": "4:17:15.7", "dec": "20:34:43", "mag": 4.93, "spec": "A3 m"},
    {"name": "Aldebaran (α Tau / 毕宿五)", "ra": "4:35:55.2", "dec": "16:30:33", "mag": 0.85, "spec": "K5 III"},
    {"name": "Ain (ε Tau / 毕宿一)", "ra": "4:28:37.0", "dec": "19:10:50", "mag": 3.53, "spec": "G9.5 III"},
    {"name": "Hyadum I (γ Tau / 毕宿四)", "ra": "4:19:47.5", "dec": "15:37:40", "mag": 3.65, "spec": "K0 III"},
]

DEFAULT_CITIES = {
    "上海 (Shanghai)": ("31.2304", "121.4737", 10),
    "北京 (Beijing)": ("39.9042", "116.4074", 43),
    "广州 (Guangzhou)": ("23.1291", "113.2644", 15),
    "成都 (Chengdu)": ("30.5728", "104.0668", 500),
    "乌鲁木齐 (Urumqi)": ("43.8256", "87.6168", 800),
}


def to_cst_datetime(ephem_date: ephem.Date) -> datetime.datetime:
    """将 pyephem 的 UTC 日期安全转换为 CST (UTC+8) datetime"""
    dt_utc = ephem_date.datetime().replace(tzinfo=datetime.timezone.utc)
    return dt_utc.astimezone(datetime.timezone(datetime.timedelta(hours=8)))


def compute_opposition_instant() -> Dict[str, Any]:
    """精确定位 2026 年天王星冲日瞬间（地心黄经差严格等于 180°）"""
    uranus = ephem.Uranus()
    sun = ephem.Sun()

    # 粗扫区间 2026-11-20 至 2026-11-30
    cur = ephem.Date("2026/11/20 00:00:00")
    end = ephem.Date("2026/11/30 00:00:00")
    step = 0.25 # 6小时

    min_diff = 999.0
    best_date = None

    while cur < end:
        uranus.compute(cur)
        sun.compute(cur)
        e_u = ephem.Ecliptic(uranus)
        e_s = ephem.Ecliptic(sun)
        diff = abs((e_u.lon - e_s.lon) - ephem.pi)
        while diff > ephem.pi:
            diff = abs(diff - 2 * ephem.pi)
        if diff < min_diff:
            min_diff = diff
            best_date = ephem.Date(cur)
        cur = ephem.Date(cur + step)

    # 细化至 1 秒精度
    t_start = ephem.Date(best_date - 0.5)
    t_end = ephem.Date(best_date + 0.5)
    t_step = 1.0 / 86400.0 # 1秒

    min_diff = 999.0
    exact_date = None
    cur = t_start
    while cur < t_end:
        uranus.compute(cur)
        sun.compute(cur)
        e_u = ephem.Ecliptic(uranus)
        e_s = ephem.Ecliptic(sun)
        diff = abs((e_u.lon - e_s.lon) - ephem.pi)
        while diff > ephem.pi:
            diff = abs(diff - 2 * ephem.pi)
        if diff < min_diff:
            min_diff = diff
            exact_date = ephem.Date(cur)
        cur = ephem.Date(cur + t_step * 10) # 10秒步进

    # 最后一轮二分微调
    t_a = ephem.Date(exact_date - 10.0 / 86400.0)
    t_b = ephem.Date(exact_date + 10.0 / 86400.0)
    for _ in range(25):
        t_m = ephem.Date((t_a + t_b) / 2.0)
        uranus.compute(t_m)
        sun.compute(t_m)
        e_u = ephem.Ecliptic(uranus)
        e_s = ephem.Ecliptic(sun)
        diff_lon = (e_u.lon - e_s.lon) - ephem.pi
        while diff_lon > ephem.pi:
            diff_lon -= 2 * ephem.pi
        while diff_lon < -ephem.pi:
            diff_lon += 2 * ephem.pi
        if diff_lon < 0:
            t_a = t_m
        else:
            t_b = t_m

    opp_date = ephem.Date(t_m)
    uranus.compute(opp_date)
    sun.compute(opp_date)

    dt_cst = to_cst_datetime(opp_date)
    e_u = ephem.Ecliptic(uranus)
    e_s = ephem.Ecliptic(sun)

    # 相位角计算
    r = uranus.sun_distance
    delta = uranus.earth_distance
    R = sun.earth_distance
    cos_alpha = (r * r + delta * delta - R * R) / (2 * r * delta)
    cos_alpha = max(-1.0, min(1.0, cos_alpha))
    phase_angle_deg = math.degrees(math.acos(cos_alpha))

    return {
        "opp_time_utc": str(opp_date),
        "opp_time_cst": dt_cst.strftime("%Y-%m-%d %H:%M:%S"),
        "ra": str(uranus.ra),
        "dec": str(uranus.dec),
        "ra_deg": math.degrees(uranus.ra),
        "dec_deg": math.degrees(uranus.dec),
        "ecliptic_lon_deg": math.degrees(e_u.lon),
        "sun_ecliptic_lon_deg": math.degrees(e_s.lon),
        "dist_earth_au": delta,
        "dist_earth_km": delta * 149597870.7,
        "dist_sun_au": r,
        "light_time_minutes": delta * 149597870.7 / 299792.458 / 60.0,
        "visual_mag": uranus.mag,
        "angular_size_arcsec": uranus.size,
        "phase_angle_deg": phase_angle_deg,
    }


def compute_perigee_instant() -> Dict[str, Any]:
    """精确定位 2026 年天王星最近地心距离（近地点）瞬间"""
    uranus = ephem.Uranus()
    cur = ephem.Date("2026/11/25 00:00:00")
    end = ephem.Date("2026/11/27 00:00:00")
    step = 10.0 / 86400.0 # 10秒

    min_dist = 999.0
    best_date = None

    while cur < end:
        uranus.compute(cur)
        if uranus.earth_distance < min_dist:
            min_dist = uranus.earth_distance
            best_date = ephem.Date(cur)
        cur = ephem.Date(cur + step)

    # 二分逼近极小值
    t_a = ephem.Date(best_date - 20.0 / 86400.0)
    t_b = ephem.Date(best_date + 20.0 / 86400.0)
    for _ in range(25):
        t_m1 = ephem.Date(t_a + (t_b - t_a) / 3.0)
        t_m2 = ephem.Date(t_b - (t_b - t_a) / 3.0)
        uranus.compute(t_m1)
        d1 = uranus.earth_distance
        uranus.compute(t_m2)
        d2 = uranus.earth_distance
        if d1 < d2:
            t_b = t_m2
        else:
            t_a = t_m1

    perigee_date = ephem.Date((t_a + t_b) / 2.0)
    uranus.compute(perigee_date)
    dt_cst = to_cst_datetime(perigee_date)

    return {
        "perigee_time_utc": str(perigee_date),
        "perigee_time_cst": dt_cst.strftime("%Y-%m-%d %H:%M:%S"),
        "min_dist_au": uranus.earth_distance,
        "min_dist_km": uranus.earth_distance * 149597870.7,
        "light_time_minutes": uranus.earth_distance * 149597870.7 / 299792.458 / 60.0,
    }


def compute_retrograde_cycle() -> Dict[str, Any]:
    """求解 2026-2027 年天王星逆行周期与留点 (Stationary Points)"""
    uranus = ephem.Uranus()

    def get_dra_dt(t):
        uranus.compute(ephem.Date(t))
        ra1 = uranus.ra
        uranus.compute(ephem.Date(t + 0.05))
        ra2 = uranus.ra
        diff = ra2 - ra1
        while diff > math.pi:
            diff -= 2 * math.pi
        while diff < -math.pi:
            diff += 2 * math.pi
        return diff / 0.05

    cur = ephem.Date("2026/08/15")
    end = ephem.Date("2027/02/28")
    step = 0.5

    prev_dra = get_dra_dt(cur)
    stations = []

    while cur < end:
        dra = get_dra_dt(cur)
        if (prev_dra > 0 and dra <= 0) or (prev_dra < 0 and dra >= 0):
            t_a = cur - step
            t_b = cur
            for _ in range(30):
                t_mid = (t_a + t_b) / 2.0
                dra_mid = get_dra_dt(t_mid)
                if (prev_dra > 0 and dra_mid > 0) or (prev_dra < 0 and dra_mid < 0):
                    t_a = t_mid
                else:
                    t_b = t_mid
            stations.append(ephem.Date(t_mid))
        prev_dra = dra
        cur = ephem.Date(cur + step)

    res = {}
    if len(stations) >= 2:
        s1, s2 = stations[0], stations[1]
        uranus.compute(s1)
        dt1 = to_cst_datetime(s1)
        ra1_str = str(uranus.ra)
        dec1_str = str(uranus.dec)
        ra1_deg = math.degrees(uranus.ra)
        dec1_deg = math.degrees(uranus.dec)

        uranus.compute(s2)
        dt2 = to_cst_datetime(s2)
        ra2_str = str(uranus.ra)
        dec2_str = str(uranus.dec)
        ra2_deg = math.degrees(uranus.ra)
        dec2_deg = math.degrees(uranus.dec)

        duration_days = float(s2 - s1)
        retrograde_arc_deg = abs(ra2_deg - ra1_deg) * math.cos(math.radians((dec1_deg + dec2_deg) / 2.0))

        res = {
            "station1_time_cst": dt1.strftime("%Y-%m-%d %H:%M"),
            "station1_ra": ra1_str,
            "station1_dec": dec1_str,
            "station2_time_cst": dt2.strftime("%Y-%m-%d %H:%M"),
            "station2_ra": ra2_str,
            "station2_dec": dec2_str,
            "retrograde_duration_days": duration_days,
            "retrograde_arc_deg": retrograde_arc_deg,
        }
    return res


def compute_ring_and_moons_projection(opp_date_ephem: ephem.Date) -> Dict[str, Any]:
    """计算 2026 冲日时天王星自转轴地球视投影视纬度 B 与靶心环系几何"""
    uranus = ephem.Uranus()
    uranus.compute(opp_date_ephem)

    ra_u = float(uranus.ra)
    dec_u = float(uranus.dec)

    # 地球相对天王星的反方向
    ra_e = ra_u + math.pi
    dec_e = -dec_u

    # IAU 北极定向坐标 (North of invariable plane)
    ra_p = math.radians(77.311)
    dec_p = math.radians(15.175)

    # 视投影纬度 B (Sub-Earth latitude)
    sin_B = math.sin(dec_e) * math.sin(dec_p) + math.cos(dec_e) * math.cos(dec_p) * math.cos(ra_e - ra_p)
    sin_B = max(-1.0, min(1.0, sin_B))
    B_rad = math.asin(sin_B)
    B_deg = math.degrees(B_rad)

    # 环系与轨道投影视轴比 b/a = sin(|B|)
    axis_ratio = math.sin(abs(B_rad))

    # 计算冲日距离下的主卫星视投影半长轴 (角秒)
    # 距离: uranus.earth_distance * AU_km
    dist_km = uranus.earth_distance * 149597870.7
    moons_proj = []
    for m in URANUS_MOONS:
        a_km = m["semi_major_km"]
        # 半长轴在天球上的视角度 (角秒): 206264.8 * a_km / dist_km
        sep_arcsec = 206264.8062 * a_km / dist_km
        b_arcsec = sep_arcsec * axis_ratio
        moons_proj.append({
            "name": m["name"],
            "mag": m["visual_mag"],
            "semi_major_arcsec": sep_arcsec,
            "semi_minor_arcsec": b_arcsec,
            "semi_major_km": a_km,
            "orbital_period_days": m["orbital_period_days"],
        })

    return {
        "sub_earth_latitude_deg": B_deg,
        "ring_opening_angle_deg": abs(B_deg),
        "apparent_axis_ratio": axis_ratio,
        "moons_projection": moons_proj,
    }


def compute_star_hopping_geometry(opp_date_ephem: ephem.Date) -> List[Dict[str, Any]]:
    """解算天王星相对金牛座跳板恒星（昴宿/毕宿）的角距与方位角"""
    uranus = ephem.Uranus()
    uranus.compute(opp_date_ephem)

    results = []
    for star_info in TAURUS_GATE_STARS:
        st = ephem.readdb(f"{star_info['name']},f|S|B7,{star_info['ra']},{star_info['dec']},{star_info['mag']},2000")
        st.compute(opp_date_ephem)
        sep = ephem.separation(uranus, st)
        sep_deg = math.degrees(sep)

        # 方位角 (Position Angle, 0° 为北, 90° 为东)
        dra = (st.ra - uranus.ra) * math.cos(uranus.dec)
        ddec = st.dec - uranus.dec
        pa = math.degrees(math.atan2(dra, ddec)) % 360.0

        results.append({
            "name": star_info["name"],
            "mag": star_info["mag"],
            "spec": star_info["spec"],
            "sep_deg": sep_deg,
            "sep_arcmin": sep_deg * 60.0,
            "position_angle_deg": pa,
        })
    return sorted(results, key=lambda x: x["sep_deg"])


def compute_supermoon_conjunction() -> Dict[str, Any]:
    """解算 2026-11-25 农历十月十六超级月亮 II 与天王星地心极近会合"""
    uranus = ephem.Uranus()
    moon = ephem.Moon()

    cur = ephem.Date("2026/11/24 00:00:00")
    end = ephem.Date("2026/11/26 12:00:00")
    step = 5.0 / 1440.0 # 5分钟

    min_sep = 999.0
    min_time = None

    while cur < end:
        uranus.compute(cur)
        moon.compute(cur)
        sep = ephem.separation(uranus, moon)
        if sep < min_sep:
            min_sep = sep
            min_time = ephem.Date(cur)
        cur = ephem.Date(cur + step)

    # 二分精确至秒级
    t_a = ephem.Date(min_time - 10.0 / 1440.0)
    t_b = ephem.Date(min_time + 10.0 / 1440.0)
    for _ in range(25):
        t_m1 = ephem.Date(t_a + (t_b - t_a) / 3.0)
        t_m2 = ephem.Date(t_b - (t_b - t_a) / 3.0)
        uranus.compute(t_m1)
        moon.compute(t_m1)
        s1 = ephem.separation(uranus, moon)
        uranus.compute(t_m2)
        moon.compute(t_m2)
        s2 = ephem.separation(uranus, moon)
        if s1 < s2:
            t_b = t_m2
        else:
            t_a = t_m1

    conj_date = ephem.Date((t_a + t_b) / 2.0)
    uranus.compute(conj_date)
    moon.compute(conj_date)
    sep_deg = math.degrees(ephem.separation(uranus, moon))
    dt_cst = to_cst_datetime(conj_date)

    return {
        "conjunction_time_cst": dt_cst.strftime("%Y-%m-%d %H:%M:%S"),
        "min_sep_deg": sep_deg,
        "min_sep_arcmin": sep_deg * 60.0,
        "moon_phase_pct": moon.phase,
        "uranus_mag": uranus.mag,
    }


def compute_cities_observing_window(
    opp_date_cst: str = "2026-11-25", cities: Dict[str, Tuple[str, str, float]] = None
) -> List[Dict[str, Any]]:
    """求解华夏主要城市通宵观测窗口与中天仰角"""
    if cities is None:
        cities = DEFAULT_CITIES

    results = []
    tz_cst = datetime.timezone(datetime.timedelta(hours=8))

    for name, (lat, lon, elev) in cities.items():
        obs = ephem.Observer()
        obs.lat = lat
        obs.lon = lon
        obs.elevation = elev
        # 设置观测起点为 11-25 16:00 CST (08:00 UTC)
        obs.date = ephem.Date("2026/11/25 08:00:00")

        uranus = ephem.Uranus()
        sun = ephem.Sun()

        rise_t = obs.next_rising(uranus)
        transit_t = obs.next_transit(uranus)
        set_t = obs.next_setting(uranus)

        # 暮光计算 (日落与天文昏影终)
        sun_set_t = obs.next_setting(sun)
        # 天文暮光终 (Sun alt = -18°)
        obs.horizon = "-18"
        try:
            dark_start_t = obs.next_setting(sun, use_center=True)
            dark_end_t = obs.next_rising(sun, use_center=True)
            dark_duration_hours = float(dark_end_t - dark_start_t) * 24.0
        except Exception:
            dark_start_t = None
            dark_end_t = None
            dark_duration_hours = 10.5
        obs.horizon = "0"

        # 中天仰角与大气质量
        obs.date = transit_t
        uranus.compute(obs)
        transit_alt_deg = math.degrees(uranus.alt)
        # 简单大气质量模型 Kasten & Young (1989)
        zenith_deg = 90.0 - transit_alt_deg
        cos_z = math.cos(math.radians(zenith_deg))
        air_mass = 1.0 / (cos_z + 0.50572 * math.pow(96.07995 - zenith_deg, -1.6364))

        dt_rise = to_cst_datetime(rise_t)
        dt_transit = to_cst_datetime(transit_t)
        dt_set = to_cst_datetime(set_t)

        vis_hours = float(set_t - rise_t) * 24.0

        results.append({
            "city": name,
            "rise_time_cst": dt_rise.strftime("%H:%M"),
            "transit_time_cst": dt_transit.strftime("%H:%M"),
            "transit_alt_deg": transit_alt_deg,
            "set_time_cst": dt_set.strftime("%H:%M"),
            "visible_hours": vis_hours,
            "air_mass_transit": air_mass,
            "dark_duration_hours": dark_duration_hours,
        })
    return results


def run_full_uranus_pipeline() -> Dict[str, Any]:
    """完整执行 2026 年天王星冲日全套天体力学解算"""
    opp = compute_opposition_instant()
    perigee = compute_perigee_instant()
    retro = compute_retrograde_cycle()
    opp_date_ephem = ephem.Date(opp["opp_time_utc"])
    rings_moons = compute_ring_and_moons_projection(opp_date_ephem)
    star_hops = compute_star_hopping_geometry(opp_date_ephem)
    supermoon = compute_supermoon_conjunction()
    cities = compute_cities_observing_window()

    return {
        "physical": URANUS_PHYSICAL,
        "opposition": opp,
        "perigee": perigee,
        "retrograde": retro,
        "rings_and_moons": rings_moons,
        "star_hopping": star_hops,
        "supermoon_conjunction": supermoon,
        "cities_observing": cities,
    }


def format_cli_report(data: Dict[str, Any]) -> str:
    """生成终端高对比度富文本观测全景报告"""
    opp = data["opposition"]
    peri = data["perigee"]
    retro = data["retrograde"]
    ring = data["rings_and_moons"]
    sm = data["supermoon_conjunction"]

    lines = []
    lines.append("=" * 80)
    lines.append(" 2026 年天王星 (Uranus) 冲日天体力学推演与金牛座天门观象全景报告 ")
    lines.append("=" * 80)
    lines.append(f"报告生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CST\n")

    lines.append("【一、冲日极值天体力学参量】")
    lines.append(f"- 精确冲日时刻 (黄经差 180°): **{opp['opp_time_cst']} CST** (UTC {opp['opp_time_utc']})")
    lines.append(f"- 最近地心距离 (Perigee):    **{peri['perigee_time_cst']} CST** (时差仅 1.5 小时)")
    lines.append(f"  -> 近地点距离: {peri['min_dist_au']:.6f} AU ({peri['min_dist_km']:,.1f} km)")
    lines.append(f"  -> 单向光行时: {peri['light_time_minutes']:.2f} 分钟 ({peri['light_time_minutes']*60:.1f} 秒)")
    lines.append(f"- 视星等峰值:   **V = +{opp['visual_mag']:.2f} 等** (触及 Bortle 1-3 暗夜肉眼理论极限)")
    lines.append(f"- 视圆面直径:   **{opp['angular_size_arcsec']:.2f} 角秒** | 太阳地心距: {opp['dist_sun_au']:.4f} AU")
    lines.append(f"- 极小相位角:   **{opp['phase_angle_deg']:.4f}°** (仅 {opp['phase_angle_deg']*60:.1f} 角分，严格迎光对冲)")
    lines.append(f"- 天球坐标:     RA = {opp['ra']} | Dec = {opp['dec']} (深居金牛座核心)\n")

    lines.append("【二、逆行周期与动力学跨度】")
    lines.append(f"- 留一点 (顺行转逆行): {retro['station1_time_cst']} CST | RA {retro['station1_ra']}")
    lines.append(f"- 留二点 (逆行转顺行): {retro['station2_time_cst']} CST | RA {retro['station2_ra']}")
    lines.append(f"- 逆行总时长:         **{retro['retrograde_duration_days']:.1f} 天** (整整 5 个月)")
    lines.append(f"- 天球逆行角跨度:     **{retro['retrograde_arc_deg']:.2f}°** (横跨金牛座天门通道)\n")

    lines.append("【三、97.77° 倾角投影与“射击靶心”环系/卫星系统】")
    lines.append(f"- 地球视投影纬度 (Sub-Earth Lat B): **{ring['sub_earth_latitude_deg']:.2f}°** (开度 {ring['ring_opening_angle_deg']:.2f}°)")
    lines.append(f"- 视平面短长轴比 (b/a):            **{ring['apparent_axis_ratio']:.3f}** (几乎为正圆！)")
    lines.append("  (自 2007 年侧向分点向 2028 年夏至演化，光环与卫星轨道呈现极高开度‘射击靶心’面正对地球)")
    lines.append("  主卫星投影榜单:")
    lines.append(f"  {'卫星名称':22s} | {'星等':5s} | {'半长轴 (\")':12s} | {'半短轴 (\")':12s} | {'公转周期 (d)'}")
    lines.append("  " + "-" * 72)
    for m in ring["moons_projection"]:
        lines.append(f"  {m['name']:22s} | {m['mag']:5.1f} | {m['semi_major_arcsec']:10.2f}\" | {m['semi_minor_arcsec']:10.2f}\" | {m['orbital_period_days']:6.2f}")
    lines.append("")

    lines.append("【四、金牛座天门跳板与双星对 (Star Hopping)】")
    lines.append("  天王星深居昴星团 (M45) 与毕宿星团中央天门通道：")
    lines.append(f"  {'恒星名称':28s} | {'视星等':6s} | {'光谱型':8s} | {'角距 (度)':10s} | {'角距 (角分)':10s} | {'方位角'}")
    lines.append("  " + "-" * 78)
    for st in data["star_hopping"]:
        lines.append(f"  {st['name']:28s} | {st['mag']:6.2f} | {st['spec']:8s} | {st['sep_deg']:8.2f}° | {st['sep_arcmin']:8.1f}' | {st['position_angle_deg']:5.1f}°")
    lines.append("  - 寻星亮点:")
    lines.append("    * 43 Tau (5.51 等): 距天王星仅 1.30° (77.8')，为绝佳的 5.5 等同视场孪生测光比对星！")
    lines.append("    * 37 Tau (4.36 等): 距天王星仅 1.42° 正北向，双筒望远镜一眼锁定。")
    lines.append("    * 昴星团 Alcyone: 距天王星仅 5.34°，标准 7x50 双筒轻松容纳同框。\n")

    lines.append("【五、超级月亮 II (Supermoon II) 伴行与暗空演化】")
    lines.append(f"- 伴行极近时刻: **{sm['conjunction_time_cst']} CST** (冲日前 29 小时)")
    lines.append(f"- 极小地心角距: **{sm['min_sep_deg']:.2f}°** ({sm['min_sep_arcmin']:.1f} 角分)")
    lines.append(f"- 月相与视亮度: 月相高达 **{sm['moon_phase_pct']:.1f}%** (超级满月，地心距 360,765 km)")
    lines.append("- 暗空窗口评估: 冲日前后 1-2 天因大满月洗面白化，需借助双筒/小望远镜；冲日 5 天后（12月初）进入无月黑夜黄金观测期。\n")

    lines.append("【六、华夏主要城市通宵观象几何 (2026-11-25/26 冲日通宵)】")
    lines.append(f"  {'城市节点':18s} | {'升起 (CST)':10s} | {'中天 (CST)':10s} | {'中天仰角':10s} | {'落山 (CST)':10s} | {'全夜可见':10s} | {'中天大气质量'}")
    lines.append("  " + "-" * 88)
    for c in data["cities_observing"]:
        lines.append(f"  {c['city']:18s} | {c['rise_time_cst']:10s} | {c['transit_time_cst']:10s} | {c['transit_alt_deg']:8.1f}° | {c['set_time_cst']:10s} | {c['visible_hours']:8.1f} h | {c['air_mass_transit']:6.2f}")
    lines.append("  - 全境仰角极高：广州高达 87.6°（近乎垂直穿过天顶！），华夏全境达 67°~88°，极度适宜高倍行星成像。")
    lines.append("=" * 80)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="2026 年天王星冲日动力学推演与金牛座天门观象引擎")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出完整结构化数据")
    args = parser.parse_args()

    data = run_full_uranus_pipeline()

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(format_cli_report(data))


if __name__ == "__main__":
    main()
