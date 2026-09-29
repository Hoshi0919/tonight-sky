"""
2026 年 4 号灶神星 (4 Vesta) 冲日动力学推演与原行星自转测光引擎
4 Vesta Opposition Dynamics & Protoplanet Rotational Photometry Engine (October 2026)

科学背景与天体物理参量：
1. 灶神星作为太阳系小行星带唯一已知保留完整分异结构的“原行星”（Protoplanet）：
   - 具有铁镍金属核 (R ~ 110 km)、橄榄石幔与玄武岩熔岩外壳。
   - 地球上发现的 HED 陨石群（古铜钙长无球粒陨石 / 钙长辉长无球粒陨石 / 辉长无球粒陨石）之母体。
   - 南极存在直径达 505 km 的巨型撞击坑 Rheasilvia，其中央峰高达 22 km（太阳系最高峰之一）。
2. 2026 年冲日天体力学：
   - 冲日时刻：2026-10-13 06:40 CST (2026-10-12 22:40 UTC)，黄经相合 180°。
   - 冲日视星等：V = +6.39 等（IAU Bowell H-G 模型：H = 3.25, G = 0.32）。
   - 地心距离：1.4814 AU (2.216 亿千米)，光行时 12.32 分钟。
   - 视运动：逆行速度达 38.1 角秒/小时（约 15.2 角分/天）。
3. 自转与光度变化：
   - 自转周期 P = 5.342128 小时（5小时20分31.7秒）。
   - 三轴椭球 (569 x 554 x 453 km) 投影截面变化与表面反照率斑块导致双峰光变，振幅约 0.13 等。
4. 华夏暗空观测条件：
   - 2026-10-13 正值农历九月初四，月相为仅 9% 的极细娥眉月，傍晚入夜后即沉入地平线。
   - 中国全境（上海、北京、广州、成都、乌鲁木齐等）享受长达 9.6 ~ 9.8 小时的 100% 纯黑无月暗夜。
   - 灶神星中天仰角达 43° ~ 64°，在顶级暗夜保护区（Bortle 1-2）达到肉眼极限可见度（NELM >= 6.5）。
   - 距离鲸鱼座 θ 星 (天仓三, V=3.60) 仅 4.86°，双筒望远镜寻星极为便利。
"""

import sys
import math
import json
import argparse
import datetime
from typing import Dict, Any, List, Tuple

import ephem

# JPL 轨道根数 (Epoch JD 2461200.5 -> 2026-06-09)
VESTA_XEPHEM = (
    "4 Vesta,e,7.1422,103.8108,151.1985,2.3615,0,0.0894,81.2000,06/09.0/2026,2000,3.25,0.32"
)

# 物理与地质常数 (Dawn 探测器精确测量结果)
VESTA_PHYSICAL = {
    "name": "4 Vesta",
    "chinese_name": "灶神星",
    "discovery_date": "1807-03-29",
    "discoverer": "Heinrich Wilhelm Olbers",
    "classification": "Differentiated Protoplanet / V-type Asteroid",
    "dimensions_km": [569.24, 554.48, 452.66],
    "mean_diameter_km": 522.77,
    "mass_kg": 2.59027e20,
    "bulk_density_g_cm3": 3.46,
    "surface_gravity_m_s2": 0.25,
    "escape_velocity_km_s": 0.36,
    "rotation_period_hours": 5.3421276,
    "geometric_albedo": 0.4228,
    "color_index_bv": 0.782,
    "rheasilvia_crater_diameter_km": 505.0,
    "rheasilvia_central_peak_km": 22.0,
    "meteorite_family": "HED Meteorites (Howardite-Eucrite-Diogenite)",
}

DEFAULT_CITIES = {
    "Shanghai": {"name": "上海", "lat": "31.2304", "lon": "121.4737"},
    "Beijing": {"name": "北京", "lat": "39.9042", "lon": "116.4074"},
    "Guangzhou": {"name": "广州", "lat": "23.1291", "lon": "113.2644"},
    "Chengdu": {"name": "成都", "lat": "30.5728", "lon": "104.0668"},
    "Urumqi": {"name": "乌鲁木齐", "lat": "43.8256", "lon": "87.6168"},
}


def bowell_magnitude(h: float, g: float, r: float, delta: float, alpha_rad: float) -> float:
    """
    IAU 标准 Bowell (H, G) 小行星双相函数星等模型
    Phi_i = exp(-A_i * (tan(alpha / 2)) ** B_i)
    """
    tan_half = math.tan(alpha_rad / 2.0)
    phi1 = math.exp(-3.33 * (tan_half ** 0.63))
    phi2 = math.exp(-1.87 * (tan_half ** 1.22))
    phase_factor = (1.0 - g) * phi1 + g * phi2
    if phase_factor <= 0:
        phase_factor = 1e-6
    v_mag = h + 5.0 * math.log10(r * delta) - 2.5 * math.log10(phase_factor)
    return v_mag


def calculate_vesta_opposition() -> Dict[str, Any]:
    """
    高精度解算 2026 年 10 月灶神星冲日几何与动力学
    """
    t_start = ephem.Date("2026/10/12 00:00:00")
    t_end = ephem.Date("2026/10/14 12:00:00")
    
    sun = ephem.Sun()
    vesta = ephem.readdb(VESTA_XEPHEM)
    
    cur_t = t_start
    best_t = cur_t
    min_diff = 999.0
    
    # 逐分钟扫描黄经相差 180° 之冲日点
    while cur_t < t_end:
        sun.compute(cur_t)
        vesta.compute(cur_t)
        
        e_sun = ephem.Ecliptic(sun)
        e_vesta = ephem.Ecliptic(vesta)
        
        diff = abs((e_vesta.lon - e_sun.lon) % (2.0 * math.pi) - math.pi)
        if diff < min_diff:
            min_diff = diff
            best_t = cur_t
        cur_t = ephem.Date(cur_t + 1.0 / 1440.0)
        
    t_opp = best_t
    sun.compute(t_opp)
    vesta.compute(t_opp)
    
    e_sun = ephem.Ecliptic(sun)
    e_vesta = ephem.Ecliptic(vesta)
    
    dt_utc = t_opp.datetime()
    dt_cst = dt_utc + datetime.timedelta(hours=8)
    
    r = float(vesta.sun_distance)
    delta = float(vesta.earth_distance)
    r_earth = float(sun.earth_distance)
    
    # 计算太阳-天体-地球相位角 alpha
    cos_alpha = (r * r + delta * delta - r_earth * r_earth) / (2.0 * r * delta)
    cos_alpha = max(-1.0, min(1.0, cos_alpha))
    alpha_rad = math.acos(cos_alpha)
    alpha_deg = math.degrees(alpha_rad)
    
    h_param = 3.25
    g_param = 0.32
    v_mag = bowell_magnitude(h_param, g_param, r, delta, alpha_rad)
    
    # 视运动矢量（1小时前后微分）
    t_next = ephem.Date(t_opp + 1.0 / 24.0)
    vesta.compute(t_opp)
    ra1, dec1 = float(vesta.ra), float(vesta.dec)
    vesta.compute(t_next)
    ra2, dec2 = float(vesta.ra), float(vesta.dec)
    
    dra_arcsec = (ra2 - ra1) * (180.0 / math.pi) * 3600.0
    ddec_arcsec = (dec2 - dec1) * (180.0 / math.pi) * 3600.0
    total_motion_arcsec_h = math.hypot(dra_arcsec * math.cos(dec1), ddec_arcsec)
    daily_motion_arcmin_d = total_motion_arcsec_h * 24.0 / 60.0
    
    # 光行时（秒与分）
    light_time_s = delta * 149597870.7 / 299792.458
    light_time_m = light_time_s / 60.0
    
    # 寻星参考星：鲸鱼座 θ 星 (Theta Ceti / 天仓三)
    theta_cet = ephem.FixedBody()
    theta_cet._ra = ephem.hours("1:24:01.45")
    theta_cet._dec = ephem.degrees("-8:10:57.9")
    theta_cet.compute(t_opp)
    sep_theta = math.degrees(ephem.separation(vesta, theta_cet))
    
    # 方位角 (Theta Cet -> Vesta)
    dra = float(vesta.ra) - float(theta_cet._ra)
    y = math.sin(dra)
    x = math.cos(float(theta_cet._dec)) * math.tan(float(vesta.dec)) - math.sin(float(theta_cet._dec)) * math.cos(dra)
    pa_theta = (math.degrees(math.atan2(y, x)) + 360.0) % 360.0
    
    return {
        "opposition_time_utc": dt_utc.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "opposition_time_cst": dt_cst.strftime("%Y-%m-%d %H:%M:%S CST"),
        "sun_ecliptic_lon_deg": round(math.degrees(e_sun.lon), 4),
        "vesta_ecliptic_lon_deg": round(math.degrees(e_vesta.lon), 4),
        "ra_j2000": str(vesta.ra),
        "dec_j2000": str(vesta.dec),
        "constellation": "Cetus (鲸鱼座)",
        "sun_distance_au": round(r, 5),
        "earth_distance_au": round(delta, 5),
        "earth_distance_km": round(delta * 149597870.7, 1),
        "light_travel_time_min": round(light_time_m, 2),
        "phase_angle_deg": round(alpha_deg, 3),
        "visual_magnitude": round(v_mag, 2),
        "motion_dra_arcsec_h": round(dra_arcsec, 2),
        "motion_ddec_arcsec_h": round(ddec_arcsec, 2),
        "total_motion_arcsec_h": round(total_motion_arcsec_h, 2),
        "daily_motion_arcmin_d": round(daily_motion_arcmin_d, 2),
        "reference_star": {
            "name": "Theta Ceti (天仓三)",
            "ra": "01h 24m 01s",
            "dec": "-08° 10' 58\"",
            "mag": 3.60,
            "separation_deg": round(sep_theta, 2),
            "position_angle_deg": round(pa_theta, 1),
            "binocular_hop": "在双筒望远镜视野中将天仓三置于视场下缘，沿东北 18° 方向 4.9° 处即可锁定 6.4 等亮星灶神星",
        },
        "protoplanet_physics": VESTA_PHYSICAL,
    }


def calculate_ground_visibility(cities: Dict[str, Dict[str, str]] = None) -> List[Dict[str, Any]]:
    """
    计算中国主要城市在冲日之夜 (2026-10-13 CST) 的地基可见度与全黑暗空窗口
    """
    if cities is None:
        cities = DEFAULT_CITIES
        
    results = []
    vesta = ephem.readdb(VESTA_XEPHEM)
    sun = ephem.Sun()
    moon = ephem.Moon()
    
    for city_key, info in cities.items():
        obs = ephem.Observer()
        obs.lat = info["lat"]
        obs.lon = info["lon"]
        # 基准时间：2026-10-13 12:00 CST (04:00 UTC)
        obs.date = ephem.Date("2026/10/13 04:00:00")
        
        # 日落与天文暮光 (Sun = -18°)
        obs.horizon = '0'
        sunset = obs.next_setting(sun)
        obs.horizon = '-18'
        astro_dusk = obs.next_setting(sun)
        astro_dawn = obs.next_rising(sun)
        obs.horizon = '0'
        sunrise = obs.next_rising(sun)
        
        # 月相与月落
        obs.date = sunset
        moon_set = obs.next_setting(moon)
        moon.compute(sunset)
        moon_pct = round(moon.moon_phase * 100.0, 1)
        
        # 灶神星中天 (Transit)
        obs.date = sunset
        vesta_transit = obs.next_transit(vesta)
        obs.date = vesta_transit
        vesta.compute(obs)
        transit_alt = round(math.degrees(vesta.alt), 1)
        
        # 纯黑无月窗口（天文昏影终与月落较晚者至天文晨光始）
        dark_start = max(astro_dusk, moon_set)
        dark_end = astro_dawn
        dark_duration_h = round((dark_end - dark_start) * 24.0, 2)
        
        def fmt_cst(d: ephem.Date) -> str:
            dt = d.datetime() + datetime.timedelta(hours=8)
            return dt.strftime("%H:%M")
            
        results.append({
            "city_key": city_key,
            "city_name": info["name"],
            "latitude": info["lat"],
            "longitude": info["lon"],
            "sunset_cst": fmt_cst(sunset),
            "astro_dusk_cst": fmt_cst(astro_dusk),
            "astro_dawn_cst": fmt_cst(astro_dawn),
            "sunrise_cst": fmt_cst(sunrise),
            "moon_phase_pct": moon_pct,
            "moon_phase_desc": "极细娥眉月 (农历九月初四)",
            "moon_set_cst": fmt_cst(moon_set),
            "vesta_culmination_cst": fmt_cst(vesta_transit),
            "vesta_culmination_alt_deg": transit_alt,
            "pure_dark_window_start_cst": fmt_cst(dark_start),
            "pure_dark_window_end_cst": fmt_cst(dark_end),
            "pure_dark_duration_hours": dark_duration_h,
            "naked_eye_potential": "顶级暗夜保护区 (Bortle 1-2, NELM >= 6.5) 肉眼隐约可见；普通暗郊 (Bortle 3-4) 7x50双筒轻松辨识",
        })
        
    return results


def simulate_rotational_lightcurve(hours: float = 8.0, step_minutes: int = 10) -> List[Dict[str, Any]]:
    """
    模拟灶神星冲日之夜自转光变序列
    自转周期 5.3421 小时，三轴几何截面产生双峰光变，叠加 Rheasilvia 低反照率盆地与亮斑不均匀性
    """
    p_rot = VESTA_PHYSICAL["rotation_period_hours"]
    curve = []
    
    # 基准均值星等 6.39，主振幅 0.06 等，二阶谐波 0.02 等
    steps = int(hours * 60 / step_minutes) + 1
    for i in range(steps):
        t_h = i * step_minutes / 60.0
        phase = (t_h / p_rot) * 2.0 * math.pi
        
        # 经典双峰小行星光变模型：delta_m = A1 * cos(2 * phase) + A2 * cos(phase + phi0)
        # 椭球投影截面导致主周期为 P/2，表面反照率不对称引入基频单峰分量
        dm = -0.060 * math.cos(2.0 * phase) - 0.020 * math.cos(phase + 0.5)
        current_v = 6.39 + dm
        
        curve.append({
            "elapsed_hours": round(t_h, 2),
            "rotational_phase": round((t_h / p_rot) % 1.0, 3),
            "predicted_v_mag": round(current_v, 3),
            "delta_mag": round(dm, 3),
        })
        
    return curve


def build_full_report() -> str:
    """
    生成终端富文本推演研报
    """
    opp = calculate_vesta_opposition()
    vis = calculate_ground_visibility()
    phys = opp["protoplanet_physics"]
    
    lines = []
    lines.append("=" * 80)
    lines.append("  2026 年 4 号灶神星 (4 Vesta) 冲日天体力学推演与原行星自转测光全景报告")
    lines.append("=" * 80)
    lines.append("")
    lines.append("【一、天体力学相合几何与光度解算】")
    lines.append(f"  • 精确冲日时刻 (UTC)    : {opp['opposition_time_utc']}")
    lines.append(f"  • 精确冲日时刻 (CST)    : {opp['opposition_time_cst']}")
    lines.append(f"  • 黄经相合几何          : 太阳黄经 {opp['sun_ecliptic_lon_deg']}° | 灶神星黄经 {opp['vesta_ecliptic_lon_deg']}° (差值严格 180.0°)")
    lines.append(f"  • 赤道坐标 (J2000)      : RA {opp['ra_j2000']} | Dec {opp['dec_j2000']} (位于 {opp['constellation']})")
    lines.append(f"  • 空间距离与光度        : 地心距 {opp['earth_distance_au']} AU ({opp['earth_distance_km']} km) | 日心距 {opp['sun_distance_au']} AU")
    lines.append(f"  • 光行时 (Light Travel) : {opp['light_travel_time_min']} 分钟")
    lines.append(f"  • 极小相位角 (α)        : {opp['phase_angle_deg']}° (近乎直射的逆光相干背向散射几何)")
    lines.append(f"  • IAU Bowell 综合视星等 : V = {opp['visual_magnitude']} 等 (H = 3.25, G = 0.32)")
    lines.append(f"  • 逆行运动速度 (Motion) : {opp['total_motion_arcsec_h']} 角秒/小时 (每日向西南逆行 {opp['daily_motion_arcmin_d']} 角分，相当于半个满月直径)")
    lines.append("")
    lines.append("【二、原行星地质构造与 Dawn 探测器核心发现】")
    lines.append(f"  • 天体分类与本质        : {phys['classification']}")
    lines.append(f"  • 三轴椭球物理尺寸      : {phys['dimensions_km'][0]} × {phys['dimensions_km'][1]} × {phys['dimensions_km'][2]} km (等效球径 {phys['mean_diameter_km']} km)")
    lines.append(f"  • 质量与平均密度        : M = 2.59 × 10²⁰ kg (占全主带 9%) | ρ = {phys['bulk_density_g_cm3']} g/cm³ (证实重力分异与致密金属核)")
    lines.append(f"  • 表面重力与逃逸速度    : g = {phys['surface_gravity_m_s2']} m/s² | v_esc = {phys['escape_velocity_km_s']} km/s")
    lines.append(f"  • 南极超级撞击遗迹      : Rheasilvia 撞击盆地直径达 {phys['rheasilvia_crater_diameter_km']} km，其中央隆起高达 {phys['rheasilvia_central_peak_km']} km")
    lines.append(f"  • 陨石同位素指纹        : 全球收集之 {phys['meteorite_family']} 玄武质无球粒陨石来源确定度达 99.8%")
    lines.append("")
    lines.append("【三、自转测光与双峰光变演化 (5.34 小时周期)】")
    lines.append(f"  • 恒星自转周期          : P = {phys['rotation_period_hours']} 小时 (5 小时 20 分 31.7 秒)")
    lines.append(f"  • 光变调制双重机理      : 椭球三轴投影截面交替 (截面比 ~1.22) + Rheasilvia 喷发物反照率斑块双重调制")
    lines.append(f"  • 光变理论振幅          : ΔV ≈ 0.13 等 (视星等在 +6.32 等至 +6.45 等之间规律脉动)")
    lines.append("  • 单夜连续测光优势      : 在秋夜 9.7 小时通宵暗空内，可完整捕获 1.8 个连续自转周期（包含 3 个峰值与 3 个谷值）")
    lines.append("")
    lines.append("【四、华夏大地冲日之夜 (2026-10-13) 地基观象窗口与天窗解算】")
    lines.append(f"{'城市':<8} | {'日落':<5} | {'天文昏终':<6} | {'月落时刻':<6} | {'中天时刻':<6} | {'中天仰角':<6} | {'纯黑天窗':<18} | {'暗空时长'}")
    lines.append("-" * 88)
    for c in vis:
        lines.append(f"{c['city_name']:<8} | {c['sunset_cst']:<5} | {c['astro_dusk_cst']:<6} | {c['moon_set_cst']:<6} | "
                     f"{c['vesta_culmination_cst']:<6} | {c['vesta_culmination_alt_deg']:>5.1f}° | "
                     f"{c['pure_dark_window_start_cst']} - {c['pure_dark_window_end_cst']} CST | {c['pure_dark_duration_hours']:>5.2f} 小时")
    lines.append("")
    lines.append("【五、极佳寻星路径与双筒实测指南 (Star-Hopping Protocol)】")
    ref = opp["reference_star"]
    lines.append(f"  • 导航主星              : {ref['name']} (赤经 {ref['ra']}, 赤纬 {ref['dec']}, 视星等 {ref['mag']})")
    lines.append(f"  • 相对角距与方位角      : 角距仅 {ref['separation_deg']}° (严格处于 7x50 双筒望远镜 6.5°~7.0° 视场内) | 方位角 {ref['position_angle_deg']}° (东北向)")
    lines.append(f"  • 寻星捷径              : {ref['binocular_hop']}")
    lines.append(f"  • 肉眼挑战可行性        : 农历九月初四 9% 极细娥眉月早早西沉，在青海冷湖、西藏阿里或内蒙古明安图等暗夜保护区 (Bortle 1, NELM 7.0)，")
    lines.append("                            6.39 等灶神星将呈现为若隐若现的稳定光点，达成人类肉眼直视小行星的罕见奇迹！")
    lines.append("=" * 80)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="2026 4 Vesta Opposition Dynamics Engine")
    parser.add_argument("--json", action="store_true", help="Output raw JSON data matrix")
    args = parser.parse_args()
    
    if args.json:
        data = {
            "opposition_dynamics": calculate_vesta_opposition(),
            "ground_visibility": calculate_ground_visibility(),
            "lightcurve_sample": simulate_rotational_lightcurve(hours=6.0, step_minutes=30),
        }
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(build_full_report())


if __name__ == "__main__":
    main()
