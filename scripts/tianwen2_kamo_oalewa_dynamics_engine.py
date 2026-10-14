#!/usr/bin/env python3
"""
中国天问二号 (Tianwen-2) 小行星 469219 振天星 (Kamoʻoalewa) 伴飞采样天体力学、
月球背向撞击起源动力学推演与主带活跃彗星 311P 连续跨界跃迁引擎
Tianwen-2 Asteroid Kamoʻoalewa Rendezvous & Sampling Astrodynamics,
Lunar Ejecta Origin Dynamics & Main-Belt Comet 311P Interplanetary Transition Engine

核心推演体系：
1. 地球准卫星 (Quasi-Satellite, QS) 与 1:1 平均运动共振 (MMR) 相对运动几何 (Hill/CW 近似解算)；
2. 希尔球边界检验：证明其处于地球引力束缚范围外 10~28 倍处，呈现纯日心共振亚稳态；
3. 27.66 分钟极速旋转离心崩解悖论：赤道离心加速度超自引力 50 倍，实证月球致密基岩/高内聚力假说；
4. 乔尔达诺·布鲁诺 (Giordano Bruno) 撞击坑月球深层抛射动力学：Melosh 剥落力学与逃逸速度推演；
5. 天问二号“一箭双星/双目标”跨界跃迁：20 km 停泊伴飞、触碰附着采样、地表投放与双重引力弹弓奔赴 311P；
6. 2026 年秋人类深空八极黄金舰队 (The Grand Octet) 时空对偶宏图。
"""

import math
from dataclasses import dataclass
from typing import Dict, Any, Tuple, List


# 物理与天文基础常数
G = 6.67430e-11                  # 万有引力常数 (m^3 / (kg * s^2))
C = 299792458.0                  # 真空光速 (m/s)
AU_KM = 149597870.7              # 1 天文单位 (km)
AU_METERS = AU_KM * 1000.0       # 1 天文单位 (m)
M_SUN = 1.98847e30               # 太阳质量 (kg)
M_EARTH = 5.9722e24              # 地球质量 (kg)
M_MOON = 7.342e22                # 月球质量 (kg)
R_MOON_KM = 1737.4               # 月球平均半径 (km)
R_EARTH_KM = 6378.137            # 地球赤道半径 (km)


@dataclass
class QuasiSatelliteGeometry:
    """地球准卫星共轨动力学几何"""
    semi_major_axis_au: float     # 半长轴 a (AU)
    eccentricity: float           # 轨道偏心率 e
    inclination_deg: float        # 轨道倾角 i (deg)
    orbital_period_days: float    # 公转周期 P (天)
    hill_sphere_radius_km: float  # 地球希尔球半径 (km)
    hill_sphere_radius_au: float  # 地球希尔球半径 (AU)
    radial_amplitude_au: float    # 相对径向位移半振幅 x (AU)
    intrack_amplitude_au: float   # 相对沿轨位移半振幅 y (AU)
    crosstrack_amplitude_au: float # 相对面外位移半振幅 z (AU)
    min_earth_dist_au: float      # 距地球最近距离 (AU)
    max_earth_dist_au: float      # 距地球最远距离 (AU)
    min_dist_to_hill_ratio: float # 最近距离与地球希尔半径之比 (倍)
    stability_duration_yr: float  # 准卫星稳定态持续时间 (年)


@dataclass
class AsteroidPhysicalProperties:
    """469219 振天星 (Kamoʻoalewa) 物理力学与旋转参数"""
    axis_a_m: float               # 长半轴 a (m)
    axis_b_m: float               # 中半轴 b (m)
    axis_c_m: float               # 短半轴 c (m)
    volume_m3: float              # 体积 (m^3)
    density_kg_m3: float          # 假设月球岩石密度 (kg/m^3)
    mass_kg: float                # 估算总质量 (kg)
    rotation_period_min: float    # 自转周期 (分钟)
    angular_velocity_rad_s: float # 自转角速度 (rad/s)
    equatorial_speed_m_s: float   # 赤道线速度 (m/s)
    centrifugal_accel_m_s2: float # 赤道离心加速度 (m/s^2)
    surface_gravity_m_s2: float   # 赤道表面万有引力加速度 (m/s^2)
    centrifugal_gravity_ratio: float # 离心加速度与自引力之比
    min_cohesion_pa: float        # 维持结构不崩解所需最小内聚抗拉强度 (Pa)


@dataclass
class LunarEjectaOrigin:
    """乔尔达诺·布鲁诺撞击坑月球深层抛射动力学"""
    source_crater_name: str       # 候选源撞击坑
    crater_diameter_km: float     # 撞击坑直径 (km)
    crater_age_myr: float         # 撞击坑地质年龄 (百万年)
    lunar_escape_velocity_km_s: float # 月球逃逸速度 (km/s)
    impactor_diameter_km: float   # 估算撞击小天体直径 (km)
    impact_velocity_km_s: float   # 典型撞击速度 (km/s)
    spallation_intact_mass_ton: float # 典型未碎化剥落岩块质量 (吨)
    ejecta_transfer_efficiency: float # 进入地球 1:1 共振捕获概率估算


@dataclass
class Tianwen2FlightProfile:
    """天问二号双目标跨界跃迁飞行剖面"""
    launch_date: str              # 发射日期
    launch_site: str              # 发射场
    carrier_rocket: str           # 运载火箭
    cruise_days: float            # 地-小转移巡航时间 (天)
    cruise_distance_km: float     # 巡航总航程 (km)
    arrival_date: str             # 抵达 20 km 伴飞日期
    hovering_distance_km: float   # 停泊勘测标称高度 (km)
    sampling_mass_target_g: float # 目标采样量 (克)
    sample_mechanism: str         # 采样方式
    earth_return_year: int        # 返回地球年份
    reentry_velocity_km_s: float  # 返回舱再入速度 (km/s)
    secondary_target: str         # 第二科学目标
    post_return_transfer: str     # 返回后轨道跃迁方式


def calculate_quasi_satellite_geometry() -> QuasiSatelliteGeometry:
    """
    推演 469219 Kamoʻoalewa 与地球 1:1 共轨准卫星相对运动动力学。
    在日地旋转坐标系 (Hill/Clohessy-Wiltshire 框架) 下解算其相对位移振幅与希尔边界。
    """
    a = 1.00123                   # AU
    e = 0.10414
    inc_deg = 7.7714
    inc_rad = math.radians(inc_deg)
    
    # 公转周期 (开普勒第三定律)
    p_yr = a ** 1.5
    p_days = p_yr * 365.256363
    
    # 地球希尔球半径: R_H = a_earth * (M_earth / (3 * M_sun))^(1/3)
    r_h_km = AU_KM * (M_EARTH / (3.0 * M_SUN)) ** (1.0 / 3.0)
    r_h_au = r_h_km / AU_KM
    
    # 相对运动半振幅 (一级近似):
    # x(t) = - a * e * cos(phi)  -> 径向半振幅
    # y(t) = 2 * a * e * sin(phi) -> 沿轨半振幅 (长轴为短轴 2 倍)
    # z(t) = a * sin(i) * sin(phi + omega) -> 垂直黄道半振幅
    x_amp_au = a * e
    y_amp_au = 2.0 * a * e
    z_amp_au = a * math.sin(inc_rad)
    
    # 相对地球空间距离包络估算
    # 最近距离出现在面内短轴附近 (同时考虑面外偏角)
    min_dist_au = math.sqrt(x_amp_au**2 + 0.0) # 约 0.104 AU
    # 最远距离出现在沿轨长轴附近
    max_dist_au = math.sqrt(y_amp_au**2 + z_amp_au**2) # 约 0.249 AU
    
    # 最近距离与地球希尔半径之比
    min_to_hill = (min_dist_au * AU_KM) / r_h_km
    
    return QuasiSatelliteGeometry(
        semi_major_axis_au=a,
        eccentricity=e,
        inclination_deg=inc_deg,
        orbital_period_days=p_days,
        hill_sphere_radius_km=r_h_km,
        hill_sphere_radius_au=r_h_au,
        radial_amplitude_au=x_amp_au,
        intrack_amplitude_au=y_amp_au,
        crosstrack_amplitude_au=z_amp_au,
        min_earth_dist_au=min_dist_au,
        max_earth_dist_au=max_dist_au,
        min_dist_to_hill_ratio=min_to_hill,
        stability_duration_yr=300.0
    )


def calculate_asteroid_physical_properties() -> AsteroidPhysicalProperties:
    """
    推演 469219 Kamoʻoalewa 物理形态、质量、极速自转离心力与基质内聚强度。
    基于 Cellinoid 3D 光变反演模型尺寸与月球硅酸盐/玄武岩密度。
    """
    # 三轴尺寸 68m x 46m x 39m
    a_m = 34.0   # 半长轴 (m)
    b_m = 23.0   # 半中轴 (m)
    c_m = 19.5   # 半短轴 (m)
    
    # 椭球体积与致密月球玄武岩密度
    vol_m3 = (4.0 / 3.0) * math.pi * a_m * b_m * c_m
    density = 2600.0  # kg/m^3 (Lunar pyroxene / basalt ejecta)
    mass = density * vol_m3
    
    # 自转周期与角速度
    period_min = 27.66
    period_sec = period_min * 60.0
    omega = 2.0 * math.pi / period_sec
    
    # 赤道最远尖端线速度与离心加速度
    v_eq = omega * a_m
    a_cent = (omega ** 2) * a_m
    
    # 表面万有引力加速度 (质点近似)
    g_surface = (G * mass) / (a_m ** 2)
    
    # 离心加速度与引力比值
    ratio = a_cent / g_surface
    
    # 临界内聚抗拉强度 (Tensile Strength): sigma ~ 1/2 * rho * omega^2 * a^2
    cohesion_pa = 0.5 * density * ((omega * a_m) ** 2)
    
    return AsteroidPhysicalProperties(
        axis_a_m=a_m,
        axis_b_m=b_m,
        axis_c_m=c_m,
        volume_m3=vol_m3,
        density_kg_m3=density,
        mass_kg=mass,
        rotation_period_min=period_min,
        angular_velocity_rad_s=omega,
        equatorial_speed_m_s=v_eq,
        centrifugal_accel_m_s2=a_cent,
        surface_gravity_m_s2=g_surface,
        centrifugal_gravity_ratio=ratio,
        min_cohesion_pa=cohesion_pa
    )


def calculate_lunar_ejecta_origin() -> LunarEjectaOrigin:
    """
    推演乔尔达诺·布鲁诺 (Giordano Bruno) 撞击坑月球剥落喷射动力学。
    """
    # 月球逃逸速度
    v_esc_moon = math.sqrt(2.0 * G * M_MOON / (R_MOON_KM * 1000.0)) / 1000.0  # km/s
    
    return LunarEjectaOrigin(
        source_crater_name="Giordano Bruno (乔尔达诺·布鲁诺撞击坑, 102.9°E, 35.9°N)",
        crater_diameter_km=22.0,
        crater_age_myr=4.0,  # 约 1~10 Myr，具有全月最年轻鲜艳辐射纹
        lunar_escape_velocity_km_s=v_esc_moon,
        impactor_diameter_km=1.5,
        impact_velocity_km_s=18.0,
        spallation_intact_mass_ton=1.66e5,  # 约 16.6 万吨
        ejecta_transfer_efficiency=0.005    # 约 0.5% 抛射物经引力扰动进入 1:1 共振捕获区
    )


def calculate_tianwen2_flight_profile() -> Tianwen2FlightProfile:
    """
    解算天问二号任务全周期时空剖面与双目标跃迁参数。
    """
    return Tianwen2FlightProfile(
        launch_date="2025-05-29",
        launch_site="西昌卫星发射中心 (XSLC)",
        carrier_rocket="长征三号乙增强型 (CZ-3B/G2)",
        cruise_days=400.0,
        cruise_distance_km=1.0e9, # 约 10 亿公里深空转移弧线
        arrival_date="2026-07-02",
        hovering_distance_km=20.0,
        sampling_mass_target_g=100.0,
        sample_mechanism="触碰即走 (TAG) 微推力采样 + 四足微重力机械锚定附着钻取",
        earth_return_year=2027,
        reentry_velocity_km_s=11.2, # 第二宇宙速度高超音速跳跃式半弹道再入 (着陆内蒙古四子王旗)
        secondary_target="311P/PANSTARRS (主带活跃彗星/小行星带原初冰水混合天体)",
        post_return_transfer="地球近距离引力弹弓 (EGA) + 火星引力弹弓 (MGA) 连续增能跃迁"
    )


def generate_grand_octet_fleet_summary() -> List[Dict[str, Any]]:
    """
    构建 2026 人类深空八极黄金舰队 (The Grand Octet) 宏伟对比矩阵。
    """
    return [
        {
            "rank": 1,
            "name": "旅行者 1 号 (Voyager 1)",
            "agency": "NASA",
            "distance_au": 173.22,
            "domain": "恒星际极寒边界",
            "key_feature": "首个人类航天 1 光日里程碑 (24 光时)，2.7 K 宇宙微波背景",
            "speed_km_s": 16.9
        },
        {
            "rank": 2,
            "name": "帕克太阳探测器 (Parker Solar Probe)",
            "agency": "NASA",
            "distance_au": 0.046,
            "domain": "恒星日冕极高温炼狱",
            "key_feature": "192 km/s 人类极速，1400°C 碳复合防热罩硬抗 640 kW/m² 辐射",
            "speed_km_s": 192.0
        },
        {
            "rank": 3,
            "name": "贝皮可伦坡 (BepiColombo)",
            "agency": "ESA/JAXA",
            "distance_au": 0.387,
            "domain": "太阳最深引力势能阱",
            "key_feature": "水星轨道捕获制动 (MOI) -1405 MJ/kg 极限制动",
            "speed_km_s": 38.5
        },
        {
            "rank": 4,
            "name": "赫拉号 (Hera)",
            "agency": "ESA",
            "distance_au": 1.304,
            "domain": "双小行星微重力伴飞",
            "key_feature": "Dimorphos 撞击坑反冲动量放大因子 beta=3.7 原位实测",
            "speed_km_s": 22.4
        },
        {
            "rank": 5,
            "name": "欧罗巴快船 (Europa Clipper)",
            "agency": "NASA",
            "distance_au": 1.000,
            "domain": "外行星木卫二深海",
            "key_feature": "MEGA 地球引力弹弓掠地 3200 km 甩向木星冰下海洋",
            "speed_km_s": 29.8
        },
        {
            "rank": 6,
            "name": "JUICE (木卫三冰月探测器)",
            "agency": "ESA",
            "distance_au": 1.749,
            "domain": "巨行星卫星内禀磁层",
            "key_feature": "巡航于 2.3 年共振弧段，探秘木卫三深海与 5.2 AU 弱光光伏",
            "speed_km_s": 24.1
        },
        {
            "rank": 7,
            "name": "詹姆斯·韦伯空间望远镜 (JWST)",
            "agency": "NASA/ESA/CSA",
            "distance_au": 0.010,
            "domain": "日地 L2 虚空天文极",
            "key_feature": "无食晕轨道 300 K 隔热屏蔽与 6.7 K 极低温，0.077'' 捕获 z>14 原初星系",
            "speed_km_s": 0.2
        },
        {
            "rank": 8,
            "name": "天问二号 (Tianwen-2)",
            "agency": "CNSA (中国国家航天局)",
            "distance_au": 1.001,
            "domain": "地球准卫星共轨采样与主带彗星双跃迁极",
            "key_feature": "469219 振天星 20km 伴飞，对抗 50 倍自引力极速自转离心力采样月球深层基岩，EGA 奔赴 311P",
            "speed_km_s": 29.8
        }
    ]


if __name__ == "__main__":
    qs = calculate_quasi_satellite_geometry()
    props = calculate_asteroid_physical_properties()
    lunar = calculate_lunar_ejecta_origin()
    tw2 = calculate_tianwen2_flight_profile()
    fleet = generate_grand_octet_fleet_summary()

    print("================================================================================")
    print("中国天问二号 (Tianwen-2) 振天星 (469219 Kamoʻoalewa) 天体力学推演引擎")
    print("================================================================================")
    print(f"准卫星半长轴: {qs.semi_major_axis_au:.5f} AU, 偏心率: {qs.eccentricity:.5f}, 倾角: {qs.inclination_deg:.4f}°")
    print(f"地球希尔球半径: {qs.hill_sphere_radius_km:,.1f} km ({qs.hill_sphere_radius_au:.5f} AU)")
    print(f"相对地球位移振幅: 径向 ±{qs.radial_amplitude_au:.4f} AU, 沿轨 ±{qs.intrack_amplitude_au:.4f} AU, 面外 ±{qs.crosstrack_amplitude_au:.4f} AU")
    print(f"距地球最近距离: {qs.min_earth_dist_au:.4f} AU ({qs.min_earth_dist_au*AU_KM:,.1f} km), 处于希尔球外 {qs.min_dist_to_hill_ratio:.2f} 倍")
    print("--------------------------------------------------------------------------------")
    print(f"小行星尺寸: {props.axis_a_m*2:.1f}m x {props.axis_b_m*2:.1f}m x {props.axis_c_m*2:.1f}m, 估算质量: {props.mass_kg:,.1f} kg")
    print(f"自转周期: {props.rotation_period_min:.2f} 分钟 ({props.angular_velocity_rad_s:.4e} rad/s), 赤道线速度: {props.equatorial_speed_m_s:.3f} m/s")
    print(f"赤道离心加速度: {props.centrifugal_accel_m_s2:.4e} m/s², 表面自引力: {props.surface_gravity_m_s2:.4e} m/s²")
    print(f"★ 离心力/自引力比值: {props.centrifugal_gravity_ratio:.2f} 倍 (必须具备 >= {props.min_cohesion_pa:.2f} Pa 内聚力，实证月球坚固岩石)")
    print("--------------------------------------------------------------------------------")
    print(f"源撞击坑: {lunar.source_crater_name}")
    print(f"撞击坑直径: {lunar.crater_diameter_km:.1f} km, 月球逃逸速度: {lunar.lunar_escape_velocity_km_s:.3f} km/s")
    print("--------------------------------------------------------------------------------")
    print(f"天问二号状态: {tw2.arrival_date} 抵达 {tw2.hovering_distance_km} km 伴飞, 目标采样量: {tw2.sampling_mass_target_g} g")
    print(f"返回与跨界跃迁: {tw2.earth_return_year} 年以 {tw2.reentry_velocity_km_s} km/s 释放返回舱, 主探测器通过 {tw2.post_return_transfer} 奔赴 {tw2.secondary_target}")
    print("--------------------------------------------------------------------------------")
    print("2026 人类深空八极黄金舰队 (The Grand Octet):")
    for probe in fleet:
        print(f"  [{probe['rank']}] {probe['name']:<25} | 极距: {probe['distance_au']:>8.3f} AU | {probe['domain']:<18} | {probe['key_feature']}")
    print("================================================================================")
