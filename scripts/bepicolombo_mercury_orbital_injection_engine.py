"""
贝皮可伦坡 (BepiColombo) 水星捕获制动 (MOI) 天体力学推演引擎
============================================================

涵盖:
1. 太阳深引力井势能耗散与开普勒轨道特征 (0.3871 AU, 偏心率 0.2056, 近日点 0.3075 AU)
2. 八年九次行星引力助推剥离链 (1 地球 + 2 金星 + 6 水星, v_inf 由 9.61 km/s 削减至 1.84 km/s)
3. 2026-09-03 离子电推舱 (MTM) 功成身退分离与当前纯弹道自由落体滑行 (41 天前)
4. 2026-11-21 水星引力捕获制动 (MOI, 4×22N 双组元推进, 弱稳定性边界 WSB 捕获, 38 天倒计时)
5. 极端热力学与辐射环境 (近日点 10.58 太阳常数 / 14.4 kW/m², 昼夜温差 -180°C ~ +430°C)
6. 双星解耦架构 (JAXA Mio 磁层探测器自旋分离 vs ESA MPO 行星轨道器下降)
7. 2026 年深空四极对偶大冲刺 (旅行者1号 1光日、贝皮可伦坡 MOI、帕克 P30、欧罗巴快船 EGA 之 16 天黄金交汇)
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
MU_VENUS = 3.24859e5                        # 金星引力常数 GM_venus km^3/s^2
MU_MERCURY = 22032.09                       # 水星引力常数 GM_mercury km^3/s^2

EARTH_RADIUS_KM = 6378.137                  # 地球赤道半径 km
VENUS_RADIUS_KM = 6051.8                    # 金星赤道半径 km
MERCURY_RADIUS_KM = 2439.7                  # 水星赤道半径 km

SOLAR_CONSTANT_1AU = 1361.0                 # 1 AU 太阳辐射常数 W/m^2
STEFAN_BOLTZMANN = 5.670374419e-8           # 玻尔兹曼辐射常数 W/(m^2 K^4)
SECONDS_PER_DAY = 86400.0                   # 平太阳日秒数

# ---------------------------------------------------------
# 水星轨道与行星本征物理参量
# ---------------------------------------------------------
MERCURY_SEMI_MAJOR_AXIS_AU = 0.387098       # 半长轴 AU (~57,909,050 km)
MERCURY_ECCENTRICITY = 0.205630             # 偏心率 (八大行星之最)
MERCURY_PERIHELION_AU = 0.307499            # 近日点 AU (~45,996,000 km)
MERCURY_APHELION_AU = 0.466697              # 远日点 AU (~69,817,000 km)
MERCURY_ORBITAL_PERIOD_DAYS = 87.969        # 公转周期 日
MERCURY_ROTATION_PERIOD_DAYS = 58.646       # 自转周期 日 (3:2 轨道共振)
MERCURY_SOLAR_DAY_DAYS = 176.0              # 水星太阳日 日 (整整 2 个水星年)
MERCURY_MASS_KG = 3.3011e23                 # 水星质量 kg (0.0553 地球质量)
MERCURY_SURFACE_GRAVITY_MS2 = 3.70          # 表面重力加速度 m/s^2 (0.377 g)
MERCURY_ESCAPE_VELOCITY_KMS = math.sqrt(2.0 * MU_MERCURY / MERCURY_RADIUS_KM) # 4.25 km/s

# ---------------------------------------------------------
# 贝皮可伦坡 (BepiColombo) 关键里程碑时刻
# ---------------------------------------------------------
LAUNCH_UTC = datetime(2018, 10, 20, 1, 45, 28, tzinfo=timezone.utc)
MTM_SEP_UTC = datetime(2026, 9, 3, 14, 0, 0, tzinfo=timezone.utc)
MOI_CAPTURE_UTC = datetime(2026, 11, 21, 0, 0, 0, tzinfo=timezone.utc)
MIO_SEPARATION_UTC = datetime(2026, 12, 10, 0, 0, 0, tzinfo=timezone.utc)
MOSIF_JETTISON_UTC = datetime(2026, 12, 16, 0, 0, 0, tzinfo=timezone.utc)
MPO_FINAL_ORBIT_UTC = datetime(2027, 3, 10, 0, 0, 0, tzinfo=timezone.utc)
SCIENCE_START_UTC = datetime(2027, 4, 1, 0, 0, 0, tzinfo=timezone.utc)

# 2026 年深空四极对偶里程碑
VOYAGER1_LIGHTDAY_UTC = datetime(2026, 11, 18, 0, 0, 0, tzinfo=timezone.utc)
PSP_PERIHELION_P30_UTC = datetime(2026, 12, 2, 0, 0, 0, tzinfo=timezone.utc)
CLIPPER_EGA_UTC = datetime(2026, 12, 3, 21, 15, 0, tzinfo=timezone.utc)

# ---------------------------------------------------------
# 航天器构型与推进质量工程参量
# ---------------------------------------------------------
LAUNCH_MASS_TOTAL_KG = 4121.0               # 发射全叠构总质量 kg
MPO_DRY_MASS_KG = 1150.0                    # ESA MPO 干重 kg
MPO_PROPELLANT_MASS_KG = 610.0              # ESA MPO 双组元化学推进剂 kg
MIO_TOTAL_MASS_KG = 285.0                   # JAXA Mio 总质量 kg
MOSIF_MASS_KG = 215.0                       # 遮阳罩与适配结构 MOSIF kg
MTM_TOTAL_MASS_KG = 1861.0                  # MTM 推进舱 (干重 ~1100kg + 氙气 ~580kg + 联氨 ~180kg)

MPO_MCSA_MASS_KG = MPO_DRY_MASS_KG + MPO_PROPELLANT_MASS_KG + MIO_TOTAL_MASS_KG + MOSIF_MASS_KG # ~2260 kg (分离 MTM 后的进近叠构)
MPO_FINAL_MASS_KG = MPO_DRY_MASS_KG + (MPO_PROPELLANT_MASS_KG - 450.0) # 入轨消耗后的科学阶段质量


@dataclass
class GravityAssistMilestone:
    name: str
    body: str
    date_str: str
    altitude_km: float
    purpose: str


FLYBY_CHAIN: List[GravityAssistMilestone] = [
    GravityAssistMilestone("Earth-1", "Earth", "2020-04-10", 12688.0, "剥离日心轨道能量，切向金星轨道"),
    GravityAssistMilestone("Venus-1", "Venus", "2020-10-15", 10720.0, "降低近日点至水星轨道外侧"),
    GravityAssistMilestone("Venus-2", "Venus", "2021-08-11", 552.0, "大偏角重力助推，近日点完全压入水星公转轨"),
    GravityAssistMilestone("Mercury-1", "Mercury", "2021-10-01", 199.0, "首次近掠水星，验证导航，削减轨道能量"),
    GravityAssistMilestone("Mercury-2", "Mercury", "2022-06-23", 200.0, "第二次水星重力制动，共振轨道调整"),
    GravityAssistMilestone("Mercury-3", "Mercury", "2023-06-20", 236.0, "第三次水星重力制动，配合离子电推降轨"),
    GravityAssistMilestone("Mercury-4", "Mercury", "2024-09-04", 165.0, "第四次水星重力制动，低高度切入新轨道"),
    GravityAssistMilestone("Mercury-5", "Mercury", "2024-12-01", 300.0, "第五次水星重力制动，微调对准极区"),
    GravityAssistMilestone("Mercury-6", "Mercury", "2025-01-08", 295.0, "终极第六次重力助推，夜侧掠过北极，相对速度降至 1.84 km/s")
]


def compute_sun_gravity_well_depth() -> Dict[str, Any]:
    """
    计算从地球 1.0 AU 掉入水星轨道 0.3871 AU 的太阳引力势能阱深度与速度差
    """
    r_earth = 1.0 * AU_KM
    r_merc = MERCURY_SEMI_MAJOR_AXIS_AU * AU_KM

    # 比势能 ε = -GM / r (在 km 单位下为 km^2/s^2 = MJ/kg)
    pot_earth_mj_kg = -MU_SUN / r_earth
    pot_merc_mj_kg = -MU_SUN / r_merc
    delta_pot_mj_kg = pot_merc_mj_kg - pot_earth_mj_kg  # 负值，势能大幅降低 (掉入深阱)
    delta_pot_j_kg = delta_pot_mj_kg * 1e6

    # 地球与水星公转速度
    v_earth_circ = math.sqrt(MU_SUN / r_earth)
    v_merc_circ = math.sqrt(MU_SUN / r_merc)

    # 霍曼转移轨道到水星近日点速度
    a_hohmann = (r_earth + r_merc) / 2.0
    v_peri_hohmann = math.sqrt(MU_SUN * (2.0 / r_merc - 1.0 / a_hohmann))
    v_inf_direct = v_peri_hohmann - v_merc_circ

    # 若直接霍曼转移入水星 674 km 初始轨道所需 Delta-V
    r_peri_cap = MERCURY_RADIUS_KM + 674.0
    v_p_direct_hyp = math.sqrt(v_inf_direct**2 + 2.0 * MU_MERCURY / r_peri_cap)
    
    # 弱捕获轨道半长轴 (674 km x 178000 km)
    r_apo_cap = MERCURY_RADIUS_KM + 178000.0
    a_cap = (r_peri_cap + r_apo_cap) / 2.0
    v_p_cap_orbit = math.sqrt(MU_MERCURY * (2.0 / r_peri_cap - 1.0 / a_cap))

    delta_v_direct_capture = v_p_direct_hyp - v_p_cap_orbit

    return {
        "delta_potential_j_per_kg": delta_pot_j_kg,
        "delta_potential_mj_per_kg": delta_pot_mj_kg,
        "v_earth_circ_kms": v_earth_circ,
        "v_merc_circ_kms": v_merc_circ,
        "v_peri_hohmann_kms": v_peri_hohmann,
        "v_inf_direct_kms": v_inf_direct,
        "delta_v_direct_capture_kms": delta_v_direct_capture
    }


def compute_bepicolombo_capture_dynamics(v_inf_kms: float = 1.84) -> Dict[str, Any]:
    """
    计算贝皮可伦坡在削减后的 v_inf = 1.84 km/s 条件下的水星引力捕获动力学
    """
    r_p_cap = MERCURY_RADIUS_KM + 674.0       # 3113.7 km
    r_a_cap = MERCURY_RADIUS_KM + 178000.0    # 180439.7 km
    a_cap = (r_p_cap + r_a_cap) / 2.0         # 91776.7 km
    e_cap = (r_a_cap - r_p_cap) / (r_a_cap + r_p_cap) # ~0.966

    # 捕获椭圆轨道周期 P = 2*pi * sqrt(a^3 / mu)
    period_sec = 2.0 * math.pi * math.sqrt(a_cap**3 / MU_MERCURY)
    period_hours = period_sec / 3600.0

    # 双曲线近日点速度
    v_p_hyp = math.sqrt(v_inf_kms**2 + 2.0 * MU_MERCURY / r_p_cap)
    
    # 椭圆轨道近日点速度
    v_p_cap = math.sqrt(MU_MERCURY * (2.0 / r_p_cap - 1.0 / a_cap))

    # 水星引力捕获制动所需 Delta-V
    delta_v_capture = v_p_hyp - v_p_cap
    delta_v_capture_ms = delta_v_capture * 1000.0

    # 4 x 22N 化学推进器总推力 = 88 N
    thrust_n = 88.0
    mass_kg = MPO_MCSA_MASS_KG # ~2260 kg
    burn_time_sec = (mass_kg * delta_v_capture_ms) / thrust_n
    burn_time_min = burn_time_sec / 60.0

    return {
        "v_inf_kms": v_inf_kms,
        "r_periapsis_km": r_p_cap,
        "r_apoapsis_km": r_a_cap,
        "semi_major_axis_km": a_cap,
        "eccentricity": e_cap,
        "orbital_period_hours": period_hours,
        "v_p_hyperbolic_kms": v_p_hyp,
        "v_p_captured_orbit_kms": v_p_cap,
        "delta_v_capture_kms": delta_v_capture,
        "delta_v_capture_ms": delta_v_capture_ms,
        "burn_time_sec": burn_time_sec,
        "burn_time_min": burn_time_min
    }


def compute_science_orbits() -> Dict[str, Any]:
    """
    计算 Mio 与 MPO 最终科学轨道的动力学与几何特征
    """
    # 1. JAXA Mio (MMO): 590 km x 11640 km 极轨道
    mio_rp = MERCURY_RADIUS_KM + 590.0
    mio_ra = MERCURY_RADIUS_KM + 11640.0
    mio_a = (mio_rp + mio_ra) / 2.0
    mio_e = (mio_ra - mio_rp) / (mio_ra + mio_rp)
    mio_p_sec = 2.0 * math.pi * math.sqrt(mio_a**3 / MU_MERCURY)
    mio_p_hours = mio_p_sec / 3600.0
    mio_vp = math.sqrt(MU_MERCURY * (2.0 / mio_rp - 1.0 / mio_a))
    mio_va = math.sqrt(MU_MERCURY * (2.0 / mio_ra - 1.0 / mio_a))

    # 2. ESA MPO: 480 km x 1500 km 极轨道
    mpo_rp = MERCURY_RADIUS_KM + 480.0
    mpo_ra = MERCURY_RADIUS_KM + 1500.0
    mpo_a = (mpo_rp + mpo_ra) / 2.0
    mpo_e = (mpo_ra - mpo_rp) / (mpo_ra + mpo_rp)
    mpo_p_sec = 2.0 * math.pi * math.sqrt(mpo_a**3 / MU_MERCURY)
    mpo_p_hours = mpo_p_sec / 3600.0
    mpo_vp = math.sqrt(MU_MERCURY * (2.0 / mpo_rp - 1.0 / mpo_a))
    mpo_va = math.sqrt(MU_MERCURY * (2.0 / mpo_ra - 1.0 / mpo_a))

    # 转移到最终轨道的总理论 Delta-V 预算
    total_moi_phase_delta_v_budget_ms = 963.0

    return {
        "mio": {
            "name": "JAXA Mio (MMO) 磁层探测轨道",
            "pericenter_altitude_km": 590.0,
            "apocenter_altitude_km": 11640.0,
            "semi_major_axis_km": mio_a,
            "eccentricity": mio_e,
            "orbital_period_hours": mio_p_hours,
            "v_peri_kms": mio_vp,
            "v_apo_kms": mio_va,
            "inclination_deg": 90.0
        },
        "mpo": {
            "name": "ESA MPO 行星遥感轨道",
            "pericenter_altitude_km": 480.0,
            "apocenter_altitude_km": 1500.0,
            "semi_major_axis_km": mpo_a,
            "eccentricity": mpo_e,
            "orbital_period_hours": mpo_p_hours,
            "v_peri_kms": mpo_vp,
            "v_apo_kms": mpo_va,
            "inclination_deg": 90.0
        },
        "total_moi_phase_delta_v_budget_ms": total_moi_phase_delta_v_budget_ms
    }


def compute_thermal_flux_environment() -> Dict[str, Any]:
    """
    计算水星极限轨道热力学辐射通量与昼夜温差平衡
    """
    # 太阳辐射强度按距离平方反比衰减
    s_peri = SOLAR_CONSTANT_1AU / (MERCURY_PERIHELION_AU**2)
    s_aph = SOLAR_CONSTANT_1AU / (MERCURY_APHELION_AU**2)
    s_mean = SOLAR_CONSTANT_1AU / (MERCURY_SEMI_MAJOR_AXIS_AU**2)

    ratio_peri_earth = 1.0 / (MERCURY_PERIHELION_AU**2)
    ratio_aph_earth = 1.0 / (MERCURY_APHELION_AU**2)

    # 水星日下点表面热平衡 (设发射率 ε = 0.9, 反照率 A = 0.12)
    albedo = 0.12
    emissivity = 0.90
    # S_abs = (1 - A) * S = ε * σ * T^4  =>  T = ((1 - A)*S / (ε*σ))^(1/4)
    t_subsolar_peri_k = ((1.0 - albedo) * s_peri / (emissivity * STEFAN_BOLTZMANN))**0.25
    t_subsolar_peri_c = t_subsolar_peri_k - 273.15

    t_subsolar_aph_k = ((1.0 - albedo) * s_aph / (emissivity * STEFAN_BOLTZMANN))**0.25
    t_subsolar_aph_c = t_subsolar_aph_k - 273.15

    # 极区永久阴影区 (PSR) 极限低温
    t_psr_k = 90.0
    t_psr_c = t_psr_k - 273.15 # -183.15 °C

    # 水星表面红外热辐射对低轨航天器底面的二次辐射通量 (MPO 480km 轨道)
    # IR_flux ≈ ε * σ * T^4 * ViewFactor
    view_factor = 0.35 # 近表面视角几何因子
    mercury_ir_flux_peri = emissivity * STEFAN_BOLTZMANN * (t_subsolar_peri_k**4) * view_factor

    return {
        "perihelion_solar_flux_w_m2": s_peri,
        "perihelion_solar_ratio_to_earth": ratio_peri_earth,
        "aphelion_solar_flux_w_m2": s_aph,
        "aphelion_solar_ratio_to_earth": ratio_aph_earth,
        "mean_solar_flux_w_m2": s_mean,
        "subsolar_temp_perihelion_k": t_subsolar_peri_k,
        "subsolar_temp_perihelion_c": t_subsolar_peri_c,
        "subsolar_temp_aphelion_k": t_subsolar_aph_k,
        "subsolar_temp_aphelion_c": t_subsolar_aph_c,
        "psr_crater_temp_k": t_psr_k,
        "psr_crater_temp_c": t_psr_c,
        "mercury_ir_flux_peri_w_m2": mercury_ir_flux_peri
    }


def compute_grand_quad_alignment_2026(current_date: date = date(2026, 10, 14)) -> Dict[str, Any]:
    """
    计算 2026 年深空四极对偶大冲刺 (旅行者1号、贝皮可伦坡、帕克、欧罗巴快船) 的时间窗口对齐
    """
    v1_date = VOYAGER1_LIGHTDAY_UTC.date()
    bepi_date = MOI_CAPTURE_UTC.date()
    psp_date = PSP_PERIHELION_P30_UTC.date()
    clipper_date = CLIPPER_EGA_UTC.date()

    d_v1 = (v1_date - current_date).days
    d_bepi = (bepi_date - current_date).days
    d_psp = (psp_date - current_date).days
    d_clipper = (clipper_date - current_date).days

    window_span_days = (clipper_date - v1_date).days # 2026-11-18 到 2026-12-03 (15 天跨度 / 16 天窗口)

    events = [
        {
            "rank": 1,
            "name": "旅行者 1 号 (Voyager 1)",
            "date": "2026-11-18",
            "days_left": d_v1,
            "milestone": "跨越 1 光日人类深空最远物理边界 (173.22 AU / 259 亿公里)",
            "extreme": "深空极寒之极 (2.7 K, 太阳常数仅 0.35 aW/m²)"
        },
        {
            "rank": 2,
            "name": "贝皮可伦坡 (BepiColombo)",
            "date": "2026-11-21",
            "days_left": d_bepi,
            "milestone": "水星轨道捕获制动 (MOI, 4×22N 推进器决死点火, 开启双星分离)",
            "extreme": "内界重力井俘获之极 (掉入 1405 MJ/kg 势能深井, 10.6 太阳常数)"
        },
        {
            "rank": 3,
            "name": "帕克太阳探测器 (PSP)",
            "date": "2026-12-02",
            "days_left": d_psp,
            "milestone": "第 30 次近日点 (P30, 9.85 R_sun, 192 km/s 极限速度飞掠日冕)",
            "extreme": "恒星日冕炼狱之极 (1400°C 极限炙烤, 0.00064c 极速)"
        },
        {
            "rank": 4,
            "name": "欧罗巴快船 (Europa Clipper)",
            "date": "2026-12-03",
            "days_left": d_clipper,
            "milestone": "地球引力助推 (EGA, 3200 km 掠地, +3.9 km/s 弹弓甩向木星)",
            "extreme": "外行星生命探索巨舰 (30.5m 翼展, 5.2 AU 弱光光伏, 木卫二冰海)"
        }
    ]

    return {
        "current_date": current_date.isoformat(),
        "days_to_voyager1_lightday": d_v1,
        "days_to_bepicolombo_moi": d_bepi,
        "days_to_psp_perihelion_p30": d_psp,
        "days_to_clipper_ega": d_clipper,
        "grand_window_span_days": window_span_days,
        "events": events
    }


def get_full_bepicolombo_analysis(current_date: date = date(2026, 10, 14)) -> Dict[str, Any]:
    """
    综合汇总贝皮可伦坡水星捕获与 2026 年深空四极全景推演
    """
    days_post_mtm_sep = (current_date - MTM_SEP_UTC.date()).days
    days_to_moi = (MOI_CAPTURE_UTC.date() - current_date).days

    # 距离地球当前测控延迟 (水星在 1.33 AU 左右时单向时延约 11.1 分钟)
    earth_distance_au = 1.337
    earth_distance_km = earth_distance_au * AU_KM
    owlt_sec = earth_distance_km / SPEED_OF_LIGHT
    owlt_min = owlt_sec / 60.0
    rtlt_min = owlt_min * 2.0

    return {
        "analysis_date": current_date.isoformat(),
        "days_post_mtm_separation": days_post_mtm_sep,
        "days_to_mercury_orbit_insertion": days_to_moi,
        "communication_lag": {
            "earth_distance_au": earth_distance_au,
            "earth_distance_km": earth_distance_km,
            "one_way_light_time_minutes": owlt_min,
            "round_trip_light_time_minutes": rtlt_min
        },
        "sun_gravity_well": compute_sun_gravity_well_depth(),
        "capture_dynamics": compute_bepicolombo_capture_dynamics(v_inf_kms=1.84),
        "science_orbits": compute_science_orbits(),
        "thermal_environment": compute_thermal_flux_environment(),
        "grand_quad_alignment": compute_grand_quad_alignment_2026(current_date),
        "flybys": [
            {
                "name": f.name,
                "body": f.body,
                "date": f.date_str,
                "altitude_km": f.altitude_km,
                "purpose": f.purpose
            }
            for f in FLYBY_CHAIN
        ]
    }


if __name__ == "__main__":
    import pprint
    res = get_full_bepicolombo_analysis()
    pprint.pprint(res)
