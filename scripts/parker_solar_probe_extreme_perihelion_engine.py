"""
帕克太阳探测器 (Parker Solar Probe) 极限近日点与日冕穿越天体力学推演引擎
======================================================================

涵盖:
1. 开普勒极端偏心率轨道动力学与日心活力公式 (Vis-Viva, vp = 191 km/s, 0.00064c)
2. 金星 7 次引力助推 (VGA-1 ~ VGA-7) 轨道能量衰减与 88 天共振终极构型
3. 极端热力学辐射通量 (647 kW/m², 475 倍地球日照) 与防热罩 (TPS, 1400°C -> 30°C)
4. 太阳阿尔芬临界表面 (Alfvén Critical Surface, <10 R_sun) 穿越与亚阿尔芬流物理
5. 广义相对论引力场近日点进动 (184.6"/世纪, 4.3 倍水星进动)
6. 2026 年交会历表与今日 (2026-10-14) 远日点前夕 (距 10-19 远日点仅 5 天) 实时轨道几何
7. 人类航天双极对偶: 帕克 (0.046 AU / 1400°C) 对称 旅行者1号 (173.1 AU / 2.7K)
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
SOLAR_RADIUS_KM = 696340.0                  # 太阳平均物理半径 R_sun km
MU_SUN = 1.32712440018e11                   # 太阳引力常数 GM_sun km^3/s^2
SOLAR_CONSTANT_1AU = 1361.0                 # 1 AU 太阳常数 W/m^2
STEFAN_BOLTZMANN_SIGMA = 5.670374419e-8     # 斯特藩-玻尔兹曼常数 W/(m^2 · K^4)
SECONDS_PER_DAY = 86400.0                   # 平太阳日秒数

# ---------------------------------------------------------
# 帕克太阳探测器任务基准与终极轨道参量 (NASA / JHUAPL 标定)
# ---------------------------------------------------------
LAUNCH_UTC = datetime(2018, 8, 12, 7, 31, 0, tzinfo=timezone.utc)
VGA7_UTC = datetime(2024, 11, 6, 22, 0, 0, tzinfo=timezone.utc)   # 第 7 次也是最后一次金星引力助推
FINAL_ORBIT_PERIOD_DAYS = 88.0                                    # 终极公转周期 (天)

# 极限近日点与远日点几何参数
PERIHELION_SURFACE_ALT_KM = 6164960.0       # 距太阳光球表面高度 km (约 3.83 百万英里)
PERIHELION_RADIUS_KM = SOLAR_RADIUS_KM + PERIHELION_SURFACE_ALT_KM # 日心近日点距 (~6,861,300 km)
PERIHELION_RADIUS_AU = PERIHELION_RADIUS_KM / AU_KM                # ~0.045865 AU
PERIHELION_SOLAR_RADII = PERIHELION_RADIUS_KM / SOLAR_RADIUS_KM   # ~9.853 R_sun

# 半长轴与偏心率 (由开普勒第三定律推导)
PERIOD_SECONDS = FINAL_ORBIT_PERIOD_DAYS * SECONDS_PER_DAY
SEMI_MAJOR_AXIS_KM = (MU_SUN * (PERIOD_SECONDS / (2.0 * math.pi))**2)**(1.0 / 3.0) # ~57,922,626 km
SEMI_MAJOR_AXIS_AU = SEMI_MAJOR_AXIS_KM / AU_KM                                    # ~0.38719 AU
ORBIT_ECCENTRICITY = 1.0 - (PERIHELION_RADIUS_KM / SEMI_MAJOR_AXIS_KM)             # ~0.88155
APHELION_RADIUS_KM = SEMI_MAJOR_AXIS_KM * (1.0 + ORBIT_ECCENTRICITY)              # ~108,983,952 km
APHELION_RADIUS_AU = APHELION_RADIUS_KM / AU_KM                                    # ~0.72851 AU

# 开普勒活力公式推导速度
PERIHELION_VELOCITY_KMS = math.sqrt(MU_SUN * (2.0 / PERIHELION_RADIUS_KM - 1.0 / SEMI_MAJOR_AXIS_KM)) # ~190.77 km/s
APHELION_VELOCITY_KMS = math.sqrt(MU_SUN * (2.0 / APHELION_RADIUS_KM - 1.0 / SEMI_MAJOR_AXIS_KM))     # ~12.01 km/s

# ---------------------------------------------------------
# 防热罩 (Thermal Protection System, TPS) 工程参量
# ---------------------------------------------------------
TPS_DIAMETER_M = 2.43                       # 防热罩直径 m (8 英尺)
TPS_THICKNESS_M = 0.1143                    # 防热罩厚度 m (4.5 英寸)
TPS_MASS_KG = 73.0                          # 防热罩总质量 kg
TPS_ABSORPTIVITY_ALPHA = 0.35               # 白色氧化铝陶瓷面太阳吸收率 alpha
TPS_EMISSIVITY_EPSILON = 0.85               # 红外热辐射发射率 epsilon
TPS_THERMAL_CONDUCTIVITY = 0.06             # 碳泡沫等效热导率 W/(m · K)
INSTRUMENT_BUS_TARGET_TEMP_C = 28.0         # 仪器舱目标维持温度 °C

# ---------------------------------------------------------
# 2026 年关键近日点历表 (Perihelion 27 ~ 30)
# ---------------------------------------------------------
PERIHELION_2026_EVENTS = [
    {"num": 27, "date_utc": date(2026, 3, 11), "dist_rsun": 9.85, "speed_kms": 191.0},
    {"num": 28, "date_utc": date(2026, 6, 8),  "dist_rsun": 9.85, "speed_kms": 191.0},
    {"num": 29, "date_utc": date(2026, 9, 5),  "dist_rsun": 9.85, "speed_kms": 191.0},
    {"num": 30, "date_utc": date(2026, 12, 2), "dist_rsun": 9.85, "speed_kms": 191.0},
]


@dataclass(frozen=True)
class OrbitalMetrics:
    """终极公转轨道参量"""
    period_days: float
    semi_major_axis_km: float
    semi_major_axis_au: float
    eccentricity: float
    perihelion_km: float
    perihelion_au: float
    perihelion_rsun: float
    perihelion_surface_alt_km: float
    aphelion_km: float
    aphelion_au: float
    aphelion_rsun: float
    perihelion_speed_kms: float
    perihelion_speed_kmh: float
    perihelion_speed_c_fraction: float
    aphelion_speed_kms: float
    speed_ratio: float


@dataclass(frozen=True)
class ThermalMetrics:
    """近日点热力学与防热罩指标"""
    perihelion_flux_w_m2: float
    flux_ratio_to_earth: float
    equilibrium_temp_k: float
    equilibrium_temp_c: float
    bus_temp_c: float
    temperature_drop_c: float
    temperature_gradient_c_per_m: float
    conductive_heat_flux_w_m2: float


@dataclass(frozen=True)
class RelativisticMetrics:
    """广义相对论引力效应指标"""
    precession_rad_per_orbit: float
    precession_arcsec_per_orbit: float
    precession_arcsec_per_year: float
    precession_arcsec_per_century: float
    ratio_to_mercury_precession: float


@dataclass(frozen=True)
class InstantaneousOrbitalState:
    """瞬时开普勒状态 (任意日期)"""
    target_date: date
    days_since_last_perihelion: float
    days_to_next_perihelion: float
    days_to_aphelion: float
    last_perihelion_num: int
    next_perihelion_num: int
    mean_anomaly_deg: float
    eccentric_anomaly_deg: float
    true_anomaly_deg: float
    heliocentric_distance_km: float
    heliocentric_distance_au: float
    heliocentric_distance_rsun: float
    heliocentric_velocity_kms: float
    heliocentric_velocity_kmh: float
    solar_flux_w_m2: float
    flux_ratio_to_earth: float
    current_shield_temp_c: float


@dataclass(frozen=True)
class DualExtremesComparison:
    """人类航天深空极值对偶 (帕克 vs 旅行者1号)"""
    distance_ratio: float
    solar_flux_ratio: float
    velocity_ratio: float
    psp_perihelion_au: float
    v1_milestone_au: float
    psp_perihelion_speed_kms: float
    v1_escape_speed_kms: float
    psp_temp_c: float
    v1_temp_k: float


def get_orbital_metrics() -> OrbitalMetrics:
    """获取终极 88 天高偏心率轨道指标"""
    p_speed_kmh = PERIHELION_VELOCITY_KMS * 3600.0
    c_fraction = PERIHELION_VELOCITY_KMS / SPEED_OF_LIGHT
    return OrbitalMetrics(
        period_days=FINAL_ORBIT_PERIOD_DAYS,
        semi_major_axis_km=SEMI_MAJOR_AXIS_KM,
        semi_major_axis_au=SEMI_MAJOR_AXIS_AU,
        eccentricity=ORBIT_ECCENTRICITY,
        perihelion_km=PERIHELION_RADIUS_KM,
        perihelion_au=PERIHELION_RADIUS_AU,
        perihelion_rsun=PERIHELION_SOLAR_RADII,
        perihelion_surface_alt_km=PERIHELION_SURFACE_ALT_KM,
        aphelion_km=APHELION_RADIUS_KM,
        aphelion_au=APHELION_RADIUS_AU,
        aphelion_rsun=APHELION_RADIUS_KM / SOLAR_RADIUS_KM,
        perihelion_speed_kms=PERIHELION_VELOCITY_KMS,
        perihelion_speed_kmh=p_speed_kmh,
        perihelion_speed_c_fraction=c_fraction,
        aphelion_speed_kms=APHELION_VELOCITY_KMS,
        speed_ratio=PERIHELION_VELOCITY_KMS / APHELION_VELOCITY_KMS
    )


def compute_thermal_metrics() -> ThermalMetrics:
    """计算近日点极端辐射通量与防热罩热平衡"""
    # 通量反比于距离平方
    flux_perihelion = SOLAR_CONSTANT_1AU / (PERIHELION_RADIUS_AU ** 2)
    flux_ratio = flux_perihelion / SOLAR_CONSTANT_1AU
    
    # 表面辐射平衡温度: alpha * S = epsilon * sigma * T^4
    t_eq_k = ((TPS_ABSORPTIVITY_ALPHA / TPS_EMISSIVITY_EPSILON) * (flux_perihelion / STEFAN_BOLTZMANN_SIGMA)) ** 0.25
    t_eq_c = t_eq_k - 273.15
    
    # 温差与梯度
    temp_drop = t_eq_c - INSTRUMENT_BUS_TARGET_TEMP_C
    temp_gradient = temp_drop / TPS_THICKNESS_M
    conductive_flux = TPS_THERMAL_CONDUCTIVITY * temp_gradient
    
    return ThermalMetrics(
        perihelion_flux_w_m2=flux_perihelion,
        flux_ratio_to_earth=flux_ratio,
        equilibrium_temp_k=t_eq_k,
        equilibrium_temp_c=t_eq_c,
        bus_temp_c=INSTRUMENT_BUS_TARGET_TEMP_C,
        temperature_drop_c=temp_drop,
        temperature_gradient_c_per_m=temp_gradient,
        conductive_heat_flux_w_m2=conductive_flux
    )


def compute_relativistic_precession() -> RelativisticMetrics:
    """计算广义相对论引力场近日点进动 (爱因斯坦公式)"""
    # dphi = 6 * pi * GM / (c^2 * a * (1 - e^2)) = 6 * pi * GM / (c^2 * rp * (1 + e))
    dphi_rad = (6.0 * math.pi * MU_SUN) / (SPEED_OF_LIGHT**2 * PERIHELION_RADIUS_KM * (1.0 + ORBIT_ECCENTRICITY))
    dphi_arcsec = math.degrees(dphi_rad) * 3600.0
    
    orbits_per_year = 365.25 / FINAL_ORBIT_PERIOD_DAYS
    dphi_arcsec_year = dphi_arcsec * orbits_per_year
    dphi_arcsec_century = dphi_arcsec_year * 100.0
    
    # 水星进动基准 42.98"/世纪
    mercury_base = 42.98
    ratio_to_mercury = dphi_arcsec_century / mercury_base
    
    return RelativisticMetrics(
        precession_rad_per_orbit=dphi_rad,
        precession_arcsec_per_orbit=dphi_arcsec,
        precession_arcsec_per_year=dphi_arcsec_year,
        precession_arcsec_per_century=dphi_arcsec_century,
        ratio_to_mercury_precession=ratio_to_mercury
    )


def compute_instantaneous_state(target_date: date) -> InstantaneousOrbitalState:
    """基于开普勒方程精确解算任意日期的轨道与物理状态"""
    p29_date = date(2026, 9, 5)
    delta_days = (target_date - p29_date).days
    
    phase = (delta_days % FINAL_ORBIT_PERIOD_DAYS)
    days_since_peri = float(phase)
    days_to_next_peri = FINAL_ORBIT_PERIOD_DAYS - days_since_peri
    days_to_aphelion = (FINAL_ORBIT_PERIOD_DAYS / 2.0) - days_since_peri
    
    last_peri_num = 29 + int(delta_days // FINAL_ORBIT_PERIOD_DAYS)
    next_peri_num = last_peri_num + 1
    
    # 平近点角 M
    mean_motion = 2.0 * math.pi / FINAL_ORBIT_PERIOD_DAYS
    m_rad = mean_motion * days_since_peri
    
    # 牛顿迭代求解开普勒方程 E - e*sin(E) = M
    e_val = ORBIT_ECCENTRICITY
    e_rad = m_rad
    for _ in range(60):
        f = e_rad - e_val * math.sin(e_rad) - m_rad
        f_prime = 1.0 - e_val * math.cos(e_rad)
        step = -f / f_prime
        e_rad += step
        if abs(step) < 1e-12:
            break
            
    # 真近点角 nu
    tan_half_nu = math.sqrt((1.0 + e_val) / (1.0 - e_val)) * math.tan(e_rad / 2.0)
    nu_rad = 2.0 * math.atan(tan_half_nu)
    if nu_rad < 0:
        nu_rad += 2.0 * math.pi
        
    # 日心距离 r
    r_km = SEMI_MAJOR_AXIS_KM * (1.0 - e_val * math.cos(e_rad))
    r_au = r_km / AU_KM
    r_rsun = r_km / SOLAR_RADIUS_KM
    
    # 活力公式日心速度 v
    v_kms = math.sqrt(MU_SUN * (2.0 / r_km - 1.0 / SEMI_MAJOR_AXIS_KM))
    v_kmh = v_kms * 3600.0
    
    # 太阳辐射通量与防热罩瞬时平衡温度
    flux = SOLAR_CONSTANT_1AU / (r_au ** 2)
    flux_ratio = flux / SOLAR_CONSTANT_1AU
    t_eq_k = ((TPS_ABSORPTIVITY_ALPHA / TPS_EMISSIVITY_EPSILON) * (flux / STEFAN_BOLTZMANN_SIGMA)) ** 0.25
    t_eq_c = t_eq_k - 273.15
    
    return InstantaneousOrbitalState(
        target_date=target_date,
        days_since_last_perihelion=days_since_peri,
        days_to_next_perihelion=days_to_next_peri,
        days_to_aphelion=days_to_aphelion,
        last_perihelion_num=last_peri_num,
        next_perihelion_num=next_peri_num,
        mean_anomaly_deg=math.degrees(m_rad),
        eccentric_anomaly_deg=math.degrees(e_rad),
        true_anomaly_deg=math.degrees(nu_rad),
        heliocentric_distance_km=r_km,
        heliocentric_distance_au=r_au,
        heliocentric_distance_rsun=r_rsun,
        heliocentric_velocity_kms=v_kms,
        heliocentric_velocity_kmh=v_kmh,
        solar_flux_w_m2=flux,
        flux_ratio_to_earth=flux_ratio,
        current_shield_temp_c=t_eq_c
    )


def compare_with_voyager1() -> DualExtremesComparison:
    """人类航天深空极值对偶: 帕克 (极内极热极速) vs 旅行者1号 (极外极冷极弱)"""
    v1_distance_au = 173.1446
    v1_speed_kms = 16.90
    v1_env_temp_k = 2.7
    
    dist_ratio = v1_distance_au / PERIHELION_RADIUS_AU
    flux_ratio = (v1_distance_au / PERIHELION_RADIUS_AU) ** 2
    vel_ratio = PERIHELION_VELOCITY_KMS / v1_speed_kms
    
    return DualExtremesComparison(
        distance_ratio=dist_ratio,
        solar_flux_ratio=flux_ratio,
        velocity_ratio=vel_ratio,
        psp_perihelion_au=PERIHELION_RADIUS_AU,
        v1_milestone_au=v1_distance_au,
        psp_perihelion_speed_kms=PERIHELION_VELOCITY_KMS,
        v1_escape_speed_kms=v1_speed_kms,
        psp_temp_c=1200.0,
        v1_temp_k=v1_env_temp_k
    )


def generate_full_psp_report(target_date: date = date(2026, 10, 14)) -> str:
    """生成帕克太阳探测器全景学术报告"""
    orb = get_orbital_metrics()
    therm = compute_thermal_metrics()
    rel = compute_relativistic_precession()
    cur = compute_instantaneous_state(target_date)
    dual = compare_with_voyager1()
    
    lines = [
        "=" * 78,
        "帕克太阳探测器 (Parker Solar Probe) 极限近日点与日冕穿越天体力学全景",
        f"标定基准日期: {target_date.isoformat()} (中国标准时间 CST)",
        "=" * 78,
        "",
        "【一、 终极 88 天开普勒轨道与活力公式速度】",
        f"  - 轨道周期 P              : {orb.period_days:.2f} 天 (88.00 天，与水星公转接近 1:1 轨道共振)",
        f"  - 轨道半长轴 a            : {orb.semi_major_axis_km:,.1f} km ({orb.semi_major_axis_au:.5f} AU)",
        f"  - 轨道偏心率 e            : {orb.eccentricity:.5f} (高度扁平极端椭圆)",
        f"  - 极限近日点距 r_p        : {orb.perihelion_km:,.1f} km ({orb.perihelion_au:.5f} AU · {orb.perihelion_rsun:.2f} R_sun)",
        f"    * 距太阳光球表面高度    : {orb.perihelion_surface_alt_km:,.1f} km (约 3.83 百万英里)",
        f"  - 远日点距 r_a            : {orb.aphelion_km:,.1f} km ({orb.aphelion_au:.5f} AU · {orb.aphelion_rsun:.2f} R_sun)",
        f"  - 近日点峰值速度 v_p      : {orb.perihelion_speed_kms:.2f} km/s ({orb.perihelion_speed_kmh:,.0f} km/h · {orb.perihelion_speed_c_fraction:.6f} c)",
        f"    * 人类文明有史以来最快造物 (1 秒跨越上海到杭州 / 3 秒穿越北京到上海)",
        f"  - 远日点速度 v_a          : {orb.aphelion_speed_kms:.2f} km/s ({orb.aphelion_speed_kms*3600:,.0f} km/h)",
        f"  - 极近/极远速度比 v_p/v_a : {orb.speed_ratio:.2f} 倍",
        "",
        "【二、 极端热力学辐射与防热罩 (TPS) 物理】",
        f"  - 近日点太阳辐射通量      : {therm.perihelion_flux_w_m2:,.1f} W/m² ({therm.perihelion_flux_w_m2/1000:.1f} kW/m²)",
        f"  - 辐射通量相对地球比值    : {therm.flux_ratio_to_earth:.1f} 倍 (承受 475 倍地球日照炙烤)",
        f"  - 防热罩迎日面平衡温度    : {therm.equilibrium_temp_k:.1f} K ({therm.equilibrium_temp_c:.1f} °C / 约 2,500 °F)",
        f"  - 仪器舱工作温度          : {therm.bus_temp_c:.1f} °C (背阴面宜人室温)",
        f"  - 11.4 cm 绝热温降        : {therm.temperature_drop_c:.1f} °C",
        f"  - 径向温度梯度            : {therm.temperature_gradient_c_per_m:,.1f} °C/m (超万度梯度阻热屏障)",
        f"  - 传导热通量              : {therm.conductive_heat_flux_w_m2:,.1f} W/m²",
        "",
        "【三、 爱因斯坦广义相对论近日点进动】",
        f"  - 单圈轨道进动量          : {rel.precession_arcsec_per_orbit:.4f} 角秒 / 轨道",
        f"  - 每年进动量              : {rel.precession_arcsec_per_year:.4f} 角秒 / 年",
        f"  - 世纪进动率              : {rel.precession_arcsec_per_century:.2f} 角秒 / 世纪 ({rel.precession_arcsec_per_century/3600:.4f}°/世纪)",
        f"  - 相对水星进动比值        : {rel.ratio_to_mercury_precession:.2f} 倍 (宏观人造物体最显著广义相对论时空弯曲效应)",
        "",
        "【四、 2026-10-14 今日实时轨道几何标定】",
        f"  - 距上次近日点 (P29, 09-05): {cur.days_since_last_perihelion:.1f} 天 (已运行半周期 88.6%)",
        f"  - 距本次远日点 (10-19)    : {cur.days_to_aphelion:.1f} 天 (仅剩 5 天达到最远端)",
        f"  - 距下次近日点 (P30, 12-02): {cur.days_to_next_perihelion:.1f} 天 (倒计时 49 天)",
        f"  - 真近点角 ν              : {cur.true_anomaly_deg:.2f}° (极度逼近 180° 远日点对称点)",
        f"  - 当前日心距离            : {cur.heliocentric_distance_km:,.1f} km ({cur.heliocentric_distance_au:.4f} AU · {cur.heliocentric_distance_rsun:.1f} R_sun)",
        f"  - 当前日心速度            : {cur.heliocentric_velocity_kms:.2f} km/s ({cur.heliocentric_velocity_kmh:,.0f} km/h)",
        f"  - 当前太阳辐射通量        : {cur.solar_flux_w_m2:,.1f} W/m² (约 {cur.flux_ratio_to_earth:.2f} 倍地球日照)",
        f"  - 当前防热罩表面温度      : {cur.current_shield_temp_c:.1f} °C",
        "",
        "【五、 人类航天双极对偶 (帕克 vs 旅行者1号)】",
        f"  - 空间距离对偶比 (V1 / PSP): {dual.distance_ratio:,.1f} 倍 (173.14 AU vs 0.0459 AU)",
        f"  - 太阳光强对偶比 (PSP / V1): {dual.solar_flux_ratio:,.1f} 倍 (1420 万倍差距！0.045 mW/m² 永夜 vs 647 kW/m² 炼狱)",
        f"  - 运动速度对偶比 (PSP / V1): {dual.velocity_ratio:.2f} 倍 (近日点 190.8 km/s vs 逃逸 16.9 km/s)",
        f"  - 热力学极端对偶          : 迎日面 1,400 °C 熔金热浪  vs  深空 2.7 K 绝对宇宙冷寂",
        "=" * 78
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    print(generate_full_psp_report())
