"""
欧罗巴快船 (Europa Clipper) MEGA 引力助推天体力学推演引擎
=========================================================

涵盖:
1. 发射动力学与初始轨道能量 (Falcon Heavy, C3 = 41.69 km²/s², v_inf = 6.457 km/s)
2. 火星引力助推 (March 1, 2025, 884 km, Delta-V = 1.8 km/s, 轨道重构)
3. 地球引力助推 (EGA, December 3, 2026, 3,200 km, 双曲线偏转 63.18°, 冲向木星)
4. 木星捕获与木卫三引力制动 (JOI, April 11, 2030, 6 小时减速, 木卫三剥离 400 m/s)
5. 5.2 AU 太阳能逆平方反比衰减与超大阵列动力学 (30.5m 翼展, 102 m², 50.3 W/m² -> 700 W)
6. 木卫二海洋学与 4:2:1 拉普拉斯潮汐共振热力学 (2.2 倍地球水体, 10^12 W 潮汐加热)
7. 今日 (2026-10-14) 发射两周年整暨回地 EGA 50 天火线冲刺即时轨道几何标定
"""

import math
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta, date
from typing import Dict, Any, List, Tuple

# ---------------------------------------------------------
# 基础物理与天体动力学常数 (IAU / CODATA 2018 标定)
# ---------------------------------------------------------
SPEED_OF_LIGHT = 299792.458                 # 真空光速 c, km/s
AU_KM = 149597870.7                         # 1 天文单位 (AU) km
MU_SUN = 1.32712440018e11                   # 太阳引力常数 GM_sun km^3/s^2
MU_EARTH = 3.986004418e5                    # 地球引力常数 GM_earth km^3/s^2
MU_MARS = 42828.37                          # 火星引力常数 GM_mars km^3/s^2
MU_JUPITER = 1.26686534e8                   # 木星引力常数 GM_jupiter km^3/s^2
MU_GANYMEDE = 9887.83                       # 木卫三引力常数 GM_ganymede km^3/s^2
MU_EUROPA = 3202.73                         # 木卫二引力常数 GM_europa km^3/s^2

EARTH_RADIUS_KM = 6378.137                  # 地球赤道半径 km
MARS_RADIUS_KM = 3389.5                     # 火星赤道半径 km
JUPITER_RADIUS_KM = 71492.0                 # 木星赤道半径 km
GANYMEDE_RADIUS_KM = 2634.1                 # 木卫三半径 km
EUROPA_RADIUS_KM = 1560.8                   # 木卫二半径 km

SOLAR_CONSTANT_1AU = 1361.0                 # 1 AU 太阳辐射常数 W/m^2
SECONDS_PER_DAY = 86400.0                   # 平太阳日秒数
EARTH_ORBITAL_SPEED_KMS = 29.78             # 地球平均公转速度 km/s
JUPITER_ORBITAL_SPEED_KMS = 13.07           # 木星平均公转速度 km/s

# ---------------------------------------------------------
# 欧罗巴快船 (Europa Clipper) 任务与航天器基准工程参量
# ---------------------------------------------------------
LAUNCH_UTC = datetime(2024, 10, 14, 16, 6, 0, tzinfo=timezone.utc)
MARS_FLYBY_UTC = datetime(2025, 3, 1, 17, 57, 0, tzinfo=timezone.utc)
EARTH_FLYBY_UTC = datetime(2026, 12, 3, 21, 15, 0, tzinfo=timezone.utc)
JUPITER_ARRIVAL_UTC = datetime(2030, 4, 11, 0, 0, 0, tzinfo=timezone.utc)

LAUNCH_MASS_KG = 6065.0                     # 发射湿重 kg (NASA 有史以来最大行星际探测器)
DRY_MASS_KG = 3315.0                        # 结构与载荷干重 kg
PROPELLANT_MASS_KG = 2750.0                 # 推进剂装载量 kg

LAUNCH_C3_KM2_S2 = 41.69                    # 发射特征能量 C3 km^2/s^2
LAUNCH_V_INF_KMS = math.sqrt(LAUNCH_C3_KM2_S2) # ~6.4568 km/s
LAUNCH_DLA_DEG = 31.6                       # 发射渐近线赤纬 deg

# 太阳翼物理尺寸与能效
SOLAR_ARRAY_SPAN_M = 30.5                   # 展开总翼展 m (超过 100 英尺 / 篮球场长度)
SOLAR_ARRAY_AREA_M2 = 102.0                 # 有效受光面积 m²
SOLAR_CELL_EFFICIENCY_5AU = 0.138           # 极低照度极低温 (LILT) 下实测光电效率 ~13.8%

# 木卫二海洋物理
EUROPA_ICE_SHELL_THICKNESS_KM = 20.0        # 浮冰外壳标称厚度 km (15~25 km)
EUROPA_OCEAN_DEPTH_KM = 100.0               # 液态水海洋深度 km (60~150 km)
EUROPA_OCEAN_VOLUME_M3 = 3.0e18             # 木卫二液态水总体积 m³ (~2.2 倍地球全海洋总和 1.335e18 m³)
EUROPA_TIDAL_HEATING_POWER_W = 1.0e12       # 拉普拉斯共振潮汐耗散发热功率 W (~1 TW)


@dataclass
class HyperbolicFlybyResult:
    """双曲线引力助推解析结果"""
    body_name: str
    altitude_km: float
    periapsis_radius_km: float
    v_infinity_kms: float
    eccentricity: float
    turn_angle_deg: float
    periapsis_speed_kms: float
    deflection_delta_v_kms: float
    heliocentric_delta_v_kms: float


@dataclass
class HeliocentricTransferOrbit:
    """日心转移轨道参量"""
    perihelion_au: float
    aphelion_au: float
    semi_major_axis_au: float
    eccentricity: float
    period_years: float
    perihelion_speed_kms: float
    aphelion_speed_kms: float


@dataclass
class InstantaneousStatus:
    """即时飞行状态数据 (2026-10-14)"""
    current_time_utc: datetime
    days_since_launch: float
    years_since_launch: float
    days_until_earth_flyby: float
    days_since_mars_flyby: float
    geocentric_distance_au: float
    geocentric_distance_km: float
    light_travel_time_seconds: float
    light_travel_time_str: str
    target_constellation: str
    approx_heliocentric_radius_au: float
    solar_flux_w_m2: float
    available_solar_power_w: float


def compute_hyperbolic_flyby(body_name: str, mu_body: float, body_radius_km: float,
                            altitude_km: float, v_inf_kms: float,
                            heliocentric_delta_v_boost_kms: float) -> HyperbolicFlybyResult:
    """高精度闭式求解双曲线相遇轨道与引力偏转几何"""
    r_p = body_radius_km + altitude_km
    # 双曲线偏心率 e_hyp = 1 + (r_p * v_inf^2) / mu
    e_hyp = 1.0 + (r_p * (v_inf_kms ** 2)) / mu_body
    # 偏折角 delta = 2 * arcsin(1 / e_hyp)
    sin_half_delta = 1.0 / e_hyp
    turn_angle_rad = 2.0 * math.asin(sin_half_delta)
    turn_angle_deg = math.degrees(turn_angle_rad)
    # 近心点极速 v_p = sqrt(v_inf^2 + 2 * mu / r_p)
    v_p = math.sqrt(v_inf_kms ** 2 + 2.0 * mu_body / r_p)
    # 双曲线速度矢量偏转模长 |Delta V| = 2 * v_inf * sin(delta / 2)
    deflection_delta_v = 2.0 * v_inf_kms * sin_half_delta

    return HyperbolicFlybyResult(
        body_name=body_name,
        altitude_km=altitude_km,
        periapsis_radius_km=r_p,
        v_infinity_kms=v_inf_kms,
        eccentricity=e_hyp,
        turn_angle_deg=turn_angle_deg,
        periapsis_speed_kms=v_p,
        deflection_delta_v_kms=deflection_delta_v,
        heliocentric_delta_v_kms=heliocentric_delta_v_boost_kms
    )


def compute_heliocentric_orbit(r_perihelion_au: float, r_aphelion_au: float) -> HeliocentricTransferOrbit:
    """解算开普勒日心椭圆轨道力学"""
    r_p_km = r_perihelion_au * AU_KM
    r_a_km = r_aphelion_au * AU_KM
    a_km = (r_p_km + r_a_km) / 2.0
    a_au = a_km / AU_KM
    e = (r_a_km - r_p_km) / (r_a_km + r_p_km)
    p_seconds = 2.0 * math.pi * math.sqrt((a_km ** 3) / MU_SUN)
    p_years = p_seconds / (SECONDS_PER_DAY * 365.25)
    
    # 开普勒活力公式求解近远日点极速
    v_p = math.sqrt(MU_SUN * (2.0 / r_p_km - 1.0 / a_km))
    v_a = math.sqrt(MU_SUN * (2.0 / r_a_km - 1.0 / a_km))

    return HeliocentricTransferOrbit(
        perihelion_au=r_perihelion_au,
        aphelion_au=r_aphelion_au,
        semi_major_axis_au=a_au,
        eccentricity=e,
        period_years=p_years,
        perihelion_speed_kms=v_p,
        aphelion_speed_kms=v_a
    )


def compute_instantaneous_state(target_dt: datetime) -> InstantaneousStatus:
    """标定 2026-10-14 发射两周年整即时状态"""
    dt_launch = (target_dt - LAUNCH_UTC).total_seconds() / SECONDS_PER_DAY
    dt_earth = (EARTH_FLYBY_UTC - target_dt).total_seconds() / SECONDS_PER_DAY
    dt_mars = (target_dt - MARS_FLYBY_UTC).total_seconds() / SECONDS_PER_DAY
    
    # 2026-10-14 航天器距地球地心距标定
    # 结合 TheSkyLive 与 JPL Horizons 标定: 约 0.4679 AU (69,998,659 km)
    geo_dist_au = 0.467912
    geo_dist_km = geo_dist_au * AU_KM
    light_time_sec = geo_dist_km / SPEED_OF_LIGHT
    m = int(light_time_sec // 60)
    s = light_time_sec % 60
    light_str = f"{m}分{s:.1f}秒"

    # 日心距离标定 (从火星回落地球途中，约 1.25 AU)
    r_helio_au = 1.250
    solar_flux = SOLAR_CONSTANT_1AU / (r_helio_au ** 2)
    # 当前发电能力 (由于过热，阵列通常大角度偏转 feather off-sun 限制在 ~2 kW)
    available_power = solar_flux * SOLAR_ARRAY_AREA_M2 * SOLAR_CELL_EFFICIENCY_5AU

    return InstantaneousStatus(
        current_time_utc=target_dt,
        days_since_launch=dt_launch,
        years_since_launch=dt_launch / 365.25,
        days_until_earth_flyby=dt_earth,
        days_since_mars_flyby=dt_mars,
        geocentric_distance_au=geo_dist_au,
        geocentric_distance_km=geo_dist_km,
        light_travel_time_seconds=light_time_sec,
        light_travel_time_str=light_str,
        target_constellation="天蝎座 (Scorpius)",
        approx_heliocentric_radius_au=r_helio_au,
        solar_flux_w_m2=solar_flux,
        available_solar_power_w=available_power
    )


def get_full_europa_clipper_analysis(ref_dt: datetime = None) -> Dict[str, Any]:
    """生成欧罗巴快船 MEGA 轨道与天体力学完整综合分析包"""
    if ref_dt is None:
        ref_dt = datetime(2026, 10, 14, 0, 0, 0, tzinfo=timezone.utc)

    # 1. 发射分析
    launch_info = {
        "launch_time_utc": LAUNCH_UTC.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "launch_vehicle": "SpaceX Falcon Heavy (全消耗构型)",
        "launch_site": "肯尼迪航天中心 LC-39A",
        "launch_wet_mass_kg": LAUNCH_MASS_KG,
        "dry_mass_kg": DRY_MASS_KG,
        "propellant_mass_kg": PROPELLANT_MASS_KG,
        "c3_km2_s2": LAUNCH_C3_KM2_S2,
        "v_infinity_kms": round(LAUNCH_V_INF_KMS, 4),
        "dla_deg": LAUNCH_DLA_DEG,
        "significance": "NASA 有史以来为行星探测建造的最大尺度旗舰航天器"
    }

    # 2. 火星引力助推 (March 1, 2025)
    mars_flyby = compute_hyperbolic_flyby(
        body_name="Mars (火星)",
        mu_body=MU_MARS,
        body_radius_km=MARS_RADIUS_KM,
        altitude_km=884.0,
        v_inf_kms=4.12,
        heliocentric_delta_v_boost_kms=1.80
    )

    # 3. 地球引力助推 (December 3, 2026)
    earth_flyby = compute_hyperbolic_flyby(
        body_name="Earth (地球)",
        mu_body=MU_EARTH,
        body_radius_km=EARTH_RADIUS_KM,
        altitude_km=3200.0,
        v_inf_kms=6.15,
        heliocentric_delta_v_boost_kms=3.90
    )

    # 4. 转移轨道演化
    # 第一段: 地球 -> 火星 (1.00 -> 1.52 AU)
    orbit_leg1 = compute_heliocentric_orbit(1.00, 1.524)
    # 第二段: 火星助推后回地回路 (1.00 -> 1.85 AU)
    orbit_leg2 = compute_heliocentric_orbit(1.00, 1.85)
    # 第三段: 地球 EGA 助推后直奔木星终极转移轨道 (1.00 -> 5.30 AU)
    orbit_final = compute_heliocentric_orbit(1.00, 5.30)

    # 5. 木星交会与捕获 (April 11, 2030)
    jupiter_info = {
        "joi_date_utc": JUPITER_ARRIVAL_UTC.strftime("%Y-%m-%d"),
        "total_transit_years": round((JUPITER_ARRIVAL_UTC - LAUNCH_UTC).total_seconds() / (SECONDS_PER_DAY * 365.25), 2),
        "total_transit_km": "29 亿公里 (2.9 billion km / 1.8 billion miles)",
        "ganymede_assist_alt_km": 500.0,
        "ganymede_braking_delta_v_ms": 400.0,
        "main_engine_burn_duration_hours": 6.0,
        "planned_europa_flybys": 49,
        "min_europa_flyby_altitude_km": 25.0,
        "radiation_vault_thickness_mm": "9.2 mm 钛铝合金屏蔽屏蔽舱",
        "end_of_mission_destination": "2034 年受控撞击木卫三 (Ganymede) 实施严格行星保护"
    }

    # 6. 5.2 AU 太阳能逆平方反比衰减
    solar_flux_earth = SOLAR_CONSTANT_1AU
    solar_flux_jupiter = SOLAR_CONSTANT_1AU / (5.2 ** 2)
    solar_power_jupiter = solar_flux_jupiter * SOLAR_ARRAY_AREA_M2 * SOLAR_CELL_EFFICIENCY_5AU

    solar_physics = {
        "array_span_m": SOLAR_ARRAY_SPAN_M,
        "array_area_m2": SOLAR_ARRAY_AREA_M2,
        "solar_flux_1au_w_m2": solar_flux_earth,
        "solar_flux_5_2au_w_m2": round(solar_flux_jupiter, 2),
        "solar_flux_ratio_percent": round((solar_flux_jupiter / solar_flux_earth) * 100.0, 2),
        "power_output_at_jupiter_w": round(solar_power_jupiter, 1),
        "power_output_baseline_requirement_w": 700.0,
        "array_structural_note": "巨型挠性太阳翼在轨道机动主发动机点火时面临严苛共振姿控挑战"
    }

    # 7. 木卫二海洋学与拉普拉斯共振
    europa_ocean = {
        "radius_km": EUROPA_RADIUS_KM,
        "surface_gravity_m_s2": 1.315,
        "ice_shell_thickness_km": EUROPA_ICE_SHELL_THICKNESS_KM,
        "ocean_depth_km": EUROPA_OCEAN_DEPTH_KM,
        "ocean_volume_m3": EUROPA_OCEAN_VOLUME_M3,
        "earth_ocean_volume_m3": 1.335e18,
        "water_volume_multiple_of_earth": round(EUROPA_OCEAN_VOLUME_M3 / 1.335e18, 2),
        "laplace_resonance_ratio": "木卫一(Io) 1 : 木卫二(Europa) 2 : 木卫三(Ganymede) 4",
        "orbital_periods_days": "Io (1.77d) : Europa (3.55d) : Ganymede (7.15d)",
        "forced_eccentricity": 0.009,
        "tidal_heating_power_w": EUROPA_TIDAL_HEATING_POWER_W,
        "seafloor_hydrothermal_vent_potential": "高可能存在海底热液喷口，具备生命所需能量源、液态溶剂与生物必要元素 (CHNOPS)"
    }

    # 8. 今日即时标定
    today_status = compute_instantaneous_state(ref_dt)

    return {
        "launch": launch_info,
        "mars_gravity_assist": mars_flyby.__dict__,
        "earth_gravity_assist": earth_flyby.__dict__,
        "transfer_orbits": {
            "leg1_earth_to_mars": orbit_leg1.__dict__,
            "leg2_mars_to_earth_loop": orbit_leg2.__dict__,
            "leg3_post_ega_to_jupiter": orbit_final.__dict__
        },
        "jupiter_capture": jupiter_info,
        "solar_power_physics": solar_physics,
        "europa_ocean_physics": europa_ocean,
        "instantaneous_today": today_status.__dict__
    }


def print_clipper_report(data: Dict[str, Any]):
    """打印终端格式化综合推演报告"""
    today = data["instantaneous_today"]
    ega = data["earth_gravity_assist"]
    mga = data["mars_gravity_assist"]
    post_ega = data["transfer_orbits"]["leg3_post_ega_to_jupiter"]
    solar = data["solar_power_physics"]
    ocean = data["europa_ocean_physics"]
    jup = data["jupiter_capture"]

    print("=" * 80)
    print(" 欧罗巴快船 (Europa Clipper) MEGA 引力助推天体力学推演报告")
    print(f" 基准时间: 2026-10-14 (发射两周年整纪念日 · 距 12-03 地球引力助推 50 天倒计时)")
    print("=" * 80)

    print("\n【一、发射两周年整 (2024-10-14 -> 2026-10-14) 即时航向标定】")
    print(f" • 任务运行时间: 距发射整整 {today['days_since_launch']:.1f} 天 ({today['years_since_launch']:.2f} 年)")
    print(f" • 回地火线冲刺: 距离 2026-12-03 地球引力助推 (EGA) 仅剩最后 {today['days_until_earth_flyby']:.1f} 天！")
    print(f" • 距地几何距离: {today['geocentric_distance_au']:.4f} AU ({today['geocentric_distance_km']:,.0f} 公里)")
    print(f" • 单向光行时:   {today['light_travel_time_str']} ({today['light_travel_time_seconds']:.2f} 秒)")
    print(f" • 天球背景天区: {today['target_constellation']}")
    print(f" • 太阳日心距离: 约 {today['approx_heliocentric_radius_au']:.2f} AU (辐射通量 {today['solar_flux_w_m2']:.1f} W/m²)")

    print("\n【二、MEGA 引力助推链条核心动力学 (Mars-Earth Gravity Assist)】")
    print(f" 1. 火星跳板 (2025-03-01):")
    print(f"    - 近掠高度: {mga['altitude_km']} km (距火星心 {mga['periapsis_radius_km']:,.1f} km)")
    print(f"    - 双曲线偏心率: e = {mga['eccentricity']:.3f} | 渐近线偏转角: {mga['turn_angle_deg']:.2f}°")
    print(f"    - 赋予日心速度增量: +{mga['heliocentric_delta_v_kms']:.2f} km/s (重构为 1.75 年回地共振弧段)")
    print(f" 2. 地球弹弓 (2026-12-03 21:15 UTC):")
    print(f"    - 近掠高度: {ega['altitude_km']:,} km (距地心 {ega['periapsis_radius_km']:,.1f} km · 1.50 R⊕)")
    print(f"    - 地心无穷远速度: v_inf = {ega['v_infinity_kms']:.2f} km/s")
    print(f"    - 近地点极速: v_p = {ega['periapsis_speed_kms']:.3f} km/s ({ega['periapsis_speed_kms']*3600:,.0f} km/h)")
    print(f"    - 双曲线偏折角: δ = {ega['turn_angle_deg']:.2f}° | 偏心率 e_hyp = {ega['eccentricity']:.4f}")
    print(f"    - 地心速度矢量差: |Δv| = {ega['deflection_delta_v_kms']:.3f} km/s")
    print(f"    - 赋予日心速度跃升: +{ega['heliocentric_delta_v_kms']:.2f} km/s，远日点直接抬升至木星公转轨道！")

    print("\n【三、后助推日心转移轨道 (Post-EGA to Jupiter)】")
    print(f" • 轨道半长轴: a = {post_ega['semi_major_axis_au']:.2f} AU | 偏心率: e = {post_ega['eccentricity']:.4f}")
    print(f" • 近日点: {post_ega['perihelion_au']:.2f} AU (地球) -> 远日点: {post_ega['aphelion_au']:.2f} AU (木星)")
    print(f" • 绕日公转周期: {post_ega['period_years']:.2f} 年 | 奔木转移历时: 3.35 年 (约 1,225 天)")
    print(f" • 木星交会时刻: 2030-04-11 (JOI) · 总旅程 29 亿公里 (5.5 年)")

    print("\n【四、5.2 AU 太阳能逆平方反比衰减与超大阵列】")
    print(f" • 阵列规模: 展开翼展 {solar['array_span_m']} 米 (超 100 英尺) | 受光面积: {solar['array_area_m2']} m²")
    print(f" • 日照通量衰减: 1 AU 处 {solar['solar_flux_1au_w_m2']} W/m² -> 5.2 AU 处仅剩 {solar['solar_flux_5_2au_w_m2']} W/m² ({solar['solar_flux_ratio_percent']}%)")
    print(f" • 木星处输出电功率: ~{solar['power_output_at_jupiter_w']} W (充裕保障 9 套科学载荷与热控体系)")

    print("\n【五、木卫二 (Europa) 冰下海洋与拉普拉斯共振热机】")
    print(f" • 浮冰厚度: {ocean['ice_shell_thickness_km']} km | 冰下海洋深度: {ocean['ocean_depth_km']} km")
    print(f" • 液态水总量: {ocean['ocean_volume_m3']:,.2e} m³ (相当于地球全部大洋水量的 {ocean['water_volume_multiple_of_earth']} 倍！)")
    print(f" • 拉普拉斯轨道共振: {ocean['laplace_resonance_ratio']} (周期 1.77d : 3.55d : 7.15d)")
    print(f" • 强迫偏心率: e = {ocean['forced_eccentricity']} | 潮汐耗散产热: ~{ocean['tidal_heating_power_w']:,.1e} W (1 TW)")
    print(f" • 探测方案: 49 次 25~100 km 极低空掠飞 + 9.2 mm 钛铝防辐射保险库保护")
    print("=" * 80)


if __name__ == "__main__":
    data = get_full_europa_clipper_analysis()
    print_clipper_report(data)
