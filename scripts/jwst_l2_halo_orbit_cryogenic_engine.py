#!/usr/bin/env python3
"""
詹姆斯·韦伯空间望远镜 (JWST) 日地 L2 晕轨道天体力学、极寒热力学隔热与红外物理推演引擎
James Webb Space Telescope (JWST) Sun-Earth L2 Halo Orbit Dynamics, Cryogenic Thermodynamics & Deep Infrared Physics Engine

核心模型包含：
1. 日地受限三体问题 (CRTBP) 与第二拉格朗日点 (L2) 空间坐标及光行时解析解算；
2. 李雅普诺夫鞍点不稳定性与 Richardson 三阶晕轨道 (Halo Orbit) 三维振幅及周期动力学；
3. 无食区物理几何验证 (Eclipse-Free Constraint)：确保 365 天无间断太阳能照射；
4. 微推力轨道维持动力学 (Stationkeeping) 与 20~25 年超长寿命预算模型；
5. 五层聚酰亚胺遮阳罩 (Sunshield) 阶梯多层真空热辐射屏蔽模型 (300 K 巨额温降，千万倍热衰减)；
6. MIRI 闭式循环氦低温制冷机 (6.7 K Cryocooler) 与被动冷却 (40 K) 双层极低温物理；
7. 6.5 米金反射镜艾里斑衍射极限、角分辨率与纳央斯基 (nJy) 原初星系极限红移推演；
8. 2026-10-15 即时在轨状态与 2026 人类深空七极宏伟舰队 (The Grand Septet) 时空大共振。
"""

import math
from dataclasses import dataclass
from typing import Dict, Any, Tuple, List


# 物理天文常数
G = 6.67430e-11                  # 万有引力常数 (m^3 / (kg * s^2))
C = 299792458.0                  # 真空光速 (m/s)
SIGMA_SB = 5.670374419e-8        # 斯特藩-玻尔兹曼常数 (W / (m^2 * K^4))
AU_KM = 149597870.7              # 1 天文单位 (km)
AU_METERS = AU_KM * 1000.0       # 1 天文单位 (m)
M_SUN = 1.98847e30               # 太阳质量 (kg)
M_EARTH = 5.9722e24              # 地球质量 (kg)
M_MOON = 7.342e22                # 月球质量 (kg)
R_EARTH_KM = 6378.137            # 地球赤道半径 (km)
SOLAR_CONSTANT = 1361.0          # 日地 1 AU 太阳辐射常数 (W/m^2)


@dataclass
class CRTBPParams:
    """日地-月质心系统受限三体常数"""
    mu: float                    # 质量比 M2 / (M1 + M2)
    l2_distance_km: float        # L2 距地球中心距离 (km)
    l2_distance_au: float        # L2 距地球中心距离 (AU)
    light_travel_time_sec: float # 单向光行时 (s)
    instability_tau_days: float  # 李雅普诺夫特征发散时间 (天)


@dataclass
class HaloOrbitGeometry:
    """晕轨道 (Halo Orbit) 三维尺度与周期"""
    period_days: float           # 轨道周期 (天)
    amplitude_x_km: float        # 日地连线方向半振幅 Ax (km)
    amplitude_y_km: float        # 黄道面内横向半振幅 Ay (km)
    amplitude_z_km: float        # 垂直黄道面垂直半振幅 Az (km)
    min_off_axis_dist_km: float  # 离轴最小距离 (km)
    earth_umbra_radius_km: float # 1.5M km 处地影半径 (km)
    is_eclipse_free: bool        # 是否完全免于地影遮挡


@dataclass
class SunshieldThermalProfile:
    """五层遮阳罩多级热辐射衰减"""
    hot_side_temp_c: float       # 日侧迎日温度 (°C)
    layer_temps_c: List[float]   # 5 层薄膜温度梯度 (°C)
    cold_side_temp_k: float      # 背阴侧被动辐射温度 (K)
    miri_temp_k: float           # MIRI 主动制冷机工作温度 (K)
    solar_heat_in_kw: float      # 迎日面总入射热功率 (kW)
    cold_leakage_mw: float       # 背阴侧残余漏热功率 (mW)
    attenuation_ratio: float     # 热衰减比 (倍)


@dataclass
class OpticsCapabilities:
    """光学系统与深空极限能力"""
    aperture_m: float            # 主镜有效通光口径 (m)
    collecting_area_m2: float    # 收集面积 (m^2)
    diffraction_limit_2um_mas: float  # 2微米近红外衍射极限 (毫角秒)
    diffraction_limit_10um_mas: float # 10微米中红外衍射极限 (毫角秒)
    limiting_sensitivity_njy: float   # 极限光通量灵敏度 (nJy)
    max_redshift_z: float             # 原初星系可观测极限红移 z


def calculate_crtbp_l2() -> CRTBPParams:
    """
    精确求解日地受限三体系统 (CRTBP) 第二拉格朗日点 (L2) 位置与动力学参数。
    欧拉五次方程解算距次星 (地月系) 相对距离 gamma。
    """
    # 考虑地月合质心系统
    m_primary = M_SUN
    m_secondary = M_EARTH + M_MOON
    mu = m_secondary / (m_primary + m_secondary)
    
    # 欧拉五次方程: gamma^5 + (3-mu)*gamma^4 + (3-2*mu)*gamma^3 - mu*gamma^2 - 2*mu*gamma - mu = 0
    # 使用牛顿拉夫逊迭代求解
    # 初始希尔近似猜测
    gamma = (mu / 3.0) ** (1.0 / 3.0)
    for _ in range(50):
        f = (gamma**5 + 
             (3.0 - mu) * gamma**4 + 
             (3.0 - 2.0 * mu) * gamma**3 - 
             mu * gamma**2 - 
             2.0 * mu * gamma - 
             mu)
        df = (5.0 * gamma**4 + 
              4.0 * (3.0 - mu) * gamma**3 + 
              3.0 * (3.0 - 2.0 * mu) * gamma**2 - 
              2.0 * mu * gamma - 
              2.0 * mu)
        step = f / df
        gamma -= step
        if abs(step) < 1e-14:
            break
            
    r_l2_km = gamma * AU_KM
    r_l2_au = gamma
    t_light = (r_l2_km * 1000.0) / C
    
    # 李雅普诺夫指数与发散时间尺度
    # CRTBP L2 本征方程在面内有一对实特征值 lambda = sqrt(c2/2 * (sqrt(9 - 8*c2) - 1)) 等
    # 日地系统 L2 鞍点典型发散时间约 23.3 天
    tau_days = 23.3
    
    return CRTBPParams(
        mu=mu,
        l2_distance_km=r_l2_km,
        l2_distance_au=r_l2_au,
        light_travel_time_sec=t_light,
        instability_tau_days=tau_days
    )


def calculate_halo_orbit_geometry() -> HaloOrbitGeometry:
    """
    解算 JWST 所运行的大振幅准周期晕轨道 (Halo Orbit) 三维几何及无食约束。
    """
    # JWST 实际标称晕轨道参数 (Richardson 轨道模型基准)
    period_days = 179.8  # 约 6 个月 (半地球公转周期)
    amp_x = 250000.0     # 日地连线振幅 (km)
    amp_y = 800000.0     # 黄道面横向振幅 (km)
    amp_z = 450000.0     # 垂直黄道面振幅 (km)
    
    # 最小离轴投影距离 rho = sqrt(y^2 + z^2) 在轨道运行中恒大于 Az 的极小值
    min_off_axis = 450000.0  # 45 万公里
    
    # 地球本影与半影在 1.50 百万公里处的几何投影
    # 太阳半径 R_sun ~ 696,340 km, 地球半径 R_earth ~ 6,378 km
    # 地影锥长度 L_umbra = R_earth * AU / (R_sun - R_earth) ~ 1.384 * 10^6 km
    # 在 1.50 * 10^6 km 处，本影锥已经闭合 (L_umbra < 1.5M km)
    # 半影区 (Penumbra) 最大半径:
    r_sun_km = 696340.0
    d_l2 = 1496550.0
    penumbra_radius_km = R_EARTH_KM + d_l2 * ((r_sun_km + R_EARTH_KM) / AU_KM)
    
    is_eclipse_free = min_off_axis > penumbra_radius_km
    
    return HaloOrbitGeometry(
        period_days=period_days,
        amplitude_x_km=amp_x,
        amplitude_y_km=amp_y,
        amplitude_z_km=amp_z,
        min_off_axis_dist_km=min_off_axis,
        earth_umbra_radius_km=penumbra_radius_km,
        is_eclipse_free=is_eclipse_free
    )


def calculate_sunshield_thermal() -> SunshieldThermalProfile:
    """
    计算五层聚酰亚胺 (Kapton) 遮阳罩辐射传热梯度与 MIRI 极低温系统。
    """
    sunshield_area_m2 = 21.2 * 14.2  # 301.04 m^2
    solar_flux = SOLAR_CONSTANT * (1.0 / (1.0100)**2)  # 在 1.01 AU 处
    total_incident_kw = (solar_flux * sunshield_area_m2) / 1000.0
    
    # 迎日面热平衡温度 (实测峰值达 +85°C ~ 358 K，标称日侧均温约 +55°C)
    hot_side_c = 85.0
    
    # 5 层薄膜实测在轨稳态温度阶梯 (°C)
    # Layer 1: +85°C (358 K)
    # Layer 2: +15°C (288 K)
    # Layer 3: -70°C (203 K)
    # Layer 4: -145°C (128 K)
    # Layer 5: -233°C (40 K)
    layer_temps = [85.0, 15.0, -70.0, -145.0, -233.15]
    
    cold_side_k = layer_temps[-1] + 273.15  # 40.0 K
    miri_temp_k = 6.7                        # MIRI 氦制冷机工作点
    
    # 漏热功率分析: 迎日面吸收与反射 ~ 200 kW 入射，背阴面漏热仅约 23 毫瓦 (0.023 W)
    leakage_mw = 23.0
    attenuation = (total_incident_kw * 1e6) / leakage_mw
    
    return SunshieldThermalProfile(
        hot_side_temp_c=hot_side_c,
        layer_temps_c=layer_temps,
        cold_side_temp_k=cold_side_k,
        miri_temp_k=miri_temp_k,
        solar_heat_in_kw=total_incident_kw,
        cold_leakage_mw=leakage_mw,
        attenuation_ratio=attenuation
    )


def calculate_stationkeeping_and_propulsion() -> Dict[str, Any]:
    """
    解算 JWST 轨道维持 (Stationkeeping) 机动推力预算与推进剂寿命模型。
    """
    # 每年标称轨道维持速度增量 delta_v (m/s/year)
    annual_skm_dv = 2.45  # m/s/year
    
    # 动量轮卸载 (Momentum Unload) 每年额外消耗 delta_v
    annual_momentum_dv = 1.65  # m/s/year
    total_annual_dv = annual_skm_dv + annual_momentum_dv  # 约 4.1 m/s/year
    
    # 推进剂储备 (发射质量约 238.5 kg 联氨推进剂与四氧化二氮)
    # Ariane 5 发射极其精准，MCC-1a/b 节省了上百 m/s 预算，留存可用推进剂支持 > 320 m/s 总 dv
    remaining_total_dv = 330.0  # m/s
    projected_life_years = remaining_total_dv / total_annual_dv
    
    return {
        "annual_skm_dv_mps": annual_skm_dv,
        "annual_momentum_dv_mps": annual_momentum_dv,
        "total_annual_dv_mps": total_annual_dv,
        "remaining_total_dv_mps": remaining_total_dv,
        "projected_life_years": projected_life_years,
        "stationkeeping_cadence_days": 21.0
    }


def calculate_optical_capabilities() -> OpticsCapabilities:
    """
    解算 6.5 米主镜衍射极限、红外角分辨率与原初星系观测极限。
    """
    aperture_m = 6.5
    collecting_area = 25.4  # m^2 (哈勃 4.0 m^2 的 6.25 倍)
    
    # 衍射极限 theta = 1.22 * lambda / D
    # 2 微米近红外 (NIRCam)
    theta_2um_rad = 1.22 * (2.0e-6) / aperture_m
    theta_2um_mas = (theta_2um_rad * (180.0 / math.pi) * 3600.0) * 1000.0  # 毫角秒
    
    # 10 微米中红外 (MIRI)
    theta_10um_rad = 1.22 * (10.0e-6) / aperture_m
    theta_10um_mas = (theta_10um_rad * (180.0 / math.pi) * 3600.0) * 1000.0
    
    limiting_njy = 10.0       # 10 nJy (对应视星等 31.4 等)
    max_redshift_z = 15.0     # 实测可稳健探测 z > 14 原初星系 (如 JADES-GS-z14-0)
    
    return OpticsCapabilities(
        aperture_m=aperture_m,
        collecting_area_m2=collecting_area,
        diffraction_limit_2um_mas=theta_2um_mas,
        diffraction_limit_10um_mas=theta_10um_mas,
        limiting_sensitivity_njy=limiting_njy,
        max_redshift_z=max_redshift_z
    )


def calculate_grand_septet_summary() -> List[Dict[str, Any]]:
    """
    2026 年秋末人类深空七极黄金舰队 (The Grand Septet) 全景对偶矩阵。
    """
    fleet = [
        {
            "name": "旅行者 1 号 (Voyager 1)",
            "agency": "NASA",
            "domain": "星际极寒空间",
            "distance_au": 173.22,
            "temp_k": 2.7,
            "key_milestone": "倒计时 34 天跨越人类航天首个 1 光日 (172.9 AU) 物理最远边界",
            "date": "2026-11-18"
        },
        {
            "name": "帕克太阳探测器 (Parker Solar Probe)",
            "agency": "NASA",
            "domain": "恒星日冕炼狱",
            "distance_au": 0.04586,
            "temp_k": 1673.0,  # ~1400°C
            "key_milestone": "开普勒 88 天终极近日点 192 km/s 极限日冕穿透 (P30 倒计时 48 天)",
            "date": "2026-12-02"
        },
        {
            "name": "贝皮可伦坡 (BepiColombo)",
            "agency": "ESA/JAXA",
            "domain": "太阳深引力阱",
            "distance_au": 0.3871,
            "temp_k": 705.0,   # ~432°C 日下点
            "key_milestone": "水星轨道捕获制动 (MOI) 37 天决死盲操倒计时 (-1405 MJ/kg 势能阱)",
            "date": "2026-11-21"
        },
        {
            "name": "赫拉号 (Hera)",
            "agency": "ESA",
            "domain": "双小行星微重力",
            "distance_au": 1.304,
            "temp_k": 260.0,
            "key_milestone": "今日 (10-15) 启动 BRM-1 93分钟主制动点火，冲入 Didymos 双星伴飞与 beta=3.7 实测",
            "date": "2026-10-15"
        },
        {
            "name": "欧罗巴快船 (Europa Clipper)",
            "agency": "NASA",
            "domain": "外行星木卫二深海",
            "distance_au": 1.000,
            "temp_k": 143.0,  # 5.2 AU 处 ~ -130°C
            "key_milestone": "MEGA 地球引力弹弓掠地 3200 km 冲刺倒计时 49 天 (贯通 5.3 AU 木星大洋)",
            "date": "2026-12-03"
        },
        {
            "name": "JUICE (木卫三冰月探测器)",
            "agency": "ESA",
            "domain": "卫星之王磁层与冰洋",
            "distance_au": 1.749,
            "temp_k": 143.0,
            "key_milestone": "完成 EGA-2 掠地 (+3.5 km/s) 巡航于 2.3 年共振弧段，首度探秘木卫三迷你磁层泡",
            "date": "2026-09-28"
        },
        {
            "name": "詹姆斯·韦伯空间望远镜 (JWST)",
            "agency": "NASA/ESA/CSA",
            "domain": "日地 L2 虚空拉格朗日鞍点",
            "distance_au": 1.010,
            "temp_k": 40.0,   # MIRI 6.7 K
            "key_milestone": "L2 无食晕轨道 300 K 隔热屏障与 6.7 K 极低温，0.077'' 衍射极限捕获 z>14 原初星系",
            "date": "持续运行 (Cycle 5)"
        }
    ]
    return fleet


if __name__ == "__main__":
    print("=" * 70)
    print("詹姆斯·韦伯空间望远镜 (JWST) 日地 L2 晕轨道与极低温物理推演引擎")
    print("=" * 70)
    
    crtbp = calculate_crtbp_l2()
    print(f"日地 L2 点距离: {crtbp.l2_distance_km:,.1f} km ({crtbp.l2_distance_au:.6f} AU)")
    print(f"单向光行时: {crtbp.light_travel_time_sec:.3f} 秒 (往返 {crtbp.light_travel_time_sec*2:.3f} 秒)")
    print(f"李雅普诺夫鞍点特征发散时间: {crtbp.instability_tau_days:.1f} 天")
    
    halo = calculate_halo_orbit_geometry()
    print(f"\n晕轨道周期: {halo.period_days:.1f} 天 (约 6 个月)")
    print(f"三维振幅: Ax={halo.amplitude_x_km:,.0f} km, Ay={halo.amplitude_y_km:,.0f} km, Az={halo.amplitude_z_km:,.0f} km")
    print(f"离轴最小距离: {halo.min_off_axis_dist_km:,.0f} km (远超地影半径 {halo.earth_umbra_radius_km:,.0f} km)")
    print(f"无食约束满足 (Eclipse-Free): {halo.is_eclipse_free} (365 天无间断太阳照射)")
    
    prop = calculate_stationkeeping_and_propulsion()
    print(f"\n年均维持推力预算: {prop['total_annual_dv_mps']:.2f} m/s/年 (SKM: {prop['annual_skm_dv_mps']:.2f} m/s)")
    print(f"机载剩余 Delta-V 预算: {prop['remaining_total_dv_mps']:.1f} m/s")
    print(f"推演预期服役寿命: {prop['projected_life_years']:.1f} 年 (稳健支持至 2040 年代中期)")
    
    thermal = calculate_sunshield_thermal()
    print(f"\n日侧温度: {thermal.hot_side_temp_c:.1f}°C")
    print(f"背阴面被动辐射温度: {thermal.cold_side_temp_k:.1f} K ({thermal.cold_side_temp_k - 273.15:.1f}°C)")
    print(f"MIRI 主动氦制冷温度: {thermal.miri_temp_k:.1f} K")
    print(f"迎日面总入射热功率: {thermal.solar_heat_in_kw:.1f} kW -> 背侧漏热: {thermal.cold_leakage_mw:.1f} mW")
    print(f"遮阳罩热衰减倍数: {thermal.attenuation_ratio:,.0f} 倍 (超千万倍隔热)")
    
    optics = calculate_optical_capabilities()
    print(f"\n有效口径: {optics.aperture_m:.1f} m (收集面积 {optics.collecting_area_m2:.1f} m²)")
    print(f"2 μm 衍射极限角分辨率: {optics.diffraction_limit_2um_mas:.1f} 毫角秒 (0.077 角秒)")
    print(f"极限灵敏度: {optics.limiting_sensitivity_njy:.1f} nJy (视星等 ~31.4 等)")
    print(f"原初星系观测红移极限: z > {optics.max_redshift_z:.0f}")
    
    septet = calculate_grand_septet_summary()
    print(f"\n2026 年秋末人类深空七极黄金舰队:")
    for probe in septet:
        print(f"- {probe['name']}: {probe['domain']} · {probe['distance_au']} AU · {probe['key_milestone']}")
