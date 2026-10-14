"""
赫拉号 (Hera) 行星防御双小行星交会与制动天体力学推演引擎
============================================================

涵盖:
1. 双小行星系统 (65803 Didymos & Dimorphos) 本征物理参量与微重力动力学 (希尔半径、自转极限、微重力场)
2. DART 动能撞击动力学与动量增强反冲因子 beta 解析推演 (周期缩短 32.8 分钟, 轨道半长轴缩水 36.6 米)
3. 赫拉号巡航历史与 2026 年 10 月主制动变轨链 (BRM-1 93分钟点火、BRM-2、过渡机动与 11 月正式交会)
4. 距地 1.30 AU 通信时延与机载自主近距操作 (AFC 光学导航、10.84 分钟单向光行时)
5. 双立方星 (Juventas & Milani) 架构与 10 cm/s 极微重力软着陆物理
6. 2026 年秋末人类深空五极黄金大冲刺 (The Grand Quintet: 帕克、贝皮、快船、赫拉、旅行者1号)
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
GRAVITATIONAL_CONSTANT = 6.67430e-11        # 万有引力常数 G, m^3/(kg s^2)
MU_SUN = 1.32712440018e11                   # 太阳引力常数 GM_sun km^3/s^2
MU_EARTH = 3.986004418e5                    # 地球引力常数 GM_earth km^3/s^2
SOLAR_CONSTANT_1AU = 1361.0                 # 1 AU 太阳辐射常数 W/m^2
STANDARD_GRAVITY = 9.80665                  # 地球标准重力加速度 g0, m/s^2

# ---------------------------------------------------------
# 双小行星系统 (65803 Didymos & Dimorphos) 物理与轨道参量
# ---------------------------------------------------------
# 主星 Didymos (迪迪莫斯)
DIDYMOS_DIAMETER_M = 780.0                  # 主星等效直径 m
DIDYMOS_RADIUS_M = DIDYMOS_DIAMETER_M / 2.0 # 390.0 m
DIDYMOS_MASS_KG = 5.20e11                   # 主星质量 kg (5.2 亿吨)
DIDYMOS_DENSITY_KGM3 = 2100.0               # 主星散堆碎石平均密度 kg/m^3
DIDYMOS_ROTATION_PERIOD_HOURS = 2.2600      # 主星自转周期 小时 (接近离心瓦解极值 ~2.2h)

# 伴星 Dimorphos (迪莫弗斯, 卫小行星)
DIMORPHOS_DIAMETER_M = 151.0                # 伴星等效直径 m (三轴 ~177×174×116 m)
DIMORPHOS_RADIUS_M = DIMORPHOS_DIAMETER_M / 2.0 # 75.5 m
DIMORPHOS_MASS_KG = 4.80e9                  # 伴星质量 kg (480 万吨, 占主星 ~0.92%)
DIMORPHOS_DENSITY_KGM3 = 2400.0             # 伴星平均密度 kg/m^3

# 系统引力常数
SYSTEM_MASS_TOTAL_KG = DIDYMOS_MASS_KG + DIMORPHOS_MASS_KG # 5.248e11 kg
MU_SYSTEM_M3S2 = GRAVITATIONAL_CONSTANT * SYSTEM_MASS_TOTAL_KG # ~35.027 m^3/s^2
MU_DIDYMOS_M3S2 = GRAVITATIONAL_CONSTANT * DIDYMOS_MASS_KG # ~34.706 m^3/s^2
MU_DIMORPHOS_M3S2 = GRAVITATIONAL_CONSTANT * DIMORPHOS_MASS_KG # ~0.320 m^3/s^2

# 太阳系轨道 (日心轨道)
DIDYMOS_HELIO_A_AU = 1.6442                 # 日心半长轴 AU
DIDYMOS_HELIO_ECC = 0.3837                  # 日心偏心率
DIDYMOS_HELIO_PERIHELION_AU = 1.0133        # 近日点 AU (紧贴地球轨道外缘, 属阿波罗型近地小行星)
DIDYMOS_HELIO_APHELION_AU = 2.2751          # 远日点 AU

# ---------------------------------------------------------
# DART 动能撞击参数 (2022-09-26 23:14 UTC)
# ---------------------------------------------------------
DART_IMPACT_UTC = datetime(2022, 9, 26, 23, 14, 0, tzinfo=timezone.utc)
DART_SPACECRAFT_MASS_KG = 580.0             # 撞击航天器质量 kg
DART_IMPACT_SPEED_MS = 6140.0               # 相对迎面撞击速度 m/s (6.14 km/s)
DART_PRE_PERIOD_SECONDS = 42917.0           # 撞击前轨道周期 秒 (11h 55m 17s = 11.9214 h)
DART_PRE_SEMI_MAJOR_AXIS_M = 1180.0         # 撞击前轨道半长轴 m (1.18 km)
DART_PERIOD_REDUCTION_SECONDS = 1968.0      # 观测实测周期缩短量 秒 (32.8 分钟, NASA 基准仅为 73 秒)
DART_POST_PERIOD_SECONDS = DART_PRE_PERIOD_SECONDS - DART_PERIOD_REDUCTION_SECONDS # 40949 s (11h 22.48m)

# ---------------------------------------------------------
# 赫拉号 (Hera) 航天器与任务时间表
# ---------------------------------------------------------
HERA_LAUNCH_UTC = datetime(2024, 10, 7, 14, 52, 11, tzinfo=timezone.utc)
HERA_MARS_FLYBY_UTC = datetime(2025, 3, 12, 12, 51, 0, tzinfo=timezone.utc)
HERA_DSM2_UTC = datetime(2026, 3, 20, 0, 0, 0, tzinfo=timezone.utc)
HERA_FIRST_IMAGE_UTC = datetime(2026, 10, 7, 0, 0, 0, tzinfo=timezone.utc) # 2周年首次单像素拍摄 (236,500 km)
HERA_BRM1_UTC = datetime(2026, 10, 15, 6, 0, 0, tzinfo=timezone.utc)       # 明天 BRM-1 93分钟点火
HERA_BRM2_UTC = datetime(2026, 10, 22, 6, 0, 0, tzinfo=timezone.utc)       # BRM-2 31分钟精修点火
HERA_RENDEZVOUS_NOMINAL_UTC = datetime(2026, 11, 15, 0, 0, 0, tzinfo=timezone.utc) # 11月中旬正式交会入轨

# 赫拉号航天器物理参数
HERA_LAUNCH_MASS_KG = 1128.0                # 发射全湿重 kg
HERA_DRY_MASS_KG = 350.0                    # 干重 kg
HERA_OCT_THRUST_N = 10.0                    # 轨控主推力器 (OCT) 单台推力 N
HERA_OCT_ACTIVE_COUNT = 3                   # BRM 制动机动同时点火推力器数量 (3台)
HERA_TOTAL_OCT_THRUST_N = HERA_OCT_THRUST_N * HERA_OCT_ACTIVE_COUNT # 30.0 N
HERA_PROPULSION_ISP_S = 225.0               # 单组元肼催化平均比冲 s

# 立方星 Juventas & Milani
CUBESAT_MASS_KG = 12.0                      # 单个 6U-XL 立方星湿重 kg
DIMORPHOS_LANDING_SPEED_MS = 0.10           # Juventas 软触地速度 m/s (10 cm/s)


@dataclass
class AsteroidMicrogravityMetrics:
    """双小行星系统微重力与轨道动力学参量"""
    didymos_surface_gravity_ms2: float
    didymos_surface_gravity_milli_g: float
    didymos_escape_velocity_ms: float
    didymos_equatorial_spin_velocity_ms: float
    didymos_spin_centrifugal_accel_ms2: float
    didymos_spin_critical_period_hours: float
    dimorphos_surface_gravity_ms2: float
    dimorphos_surface_gravity_milli_g: float
    dimorphos_escape_velocity_ms: float
    system_hill_radius_km: float
    dimorphos_hill_radius_m: float
    dimorphos_orbital_speed_pre_ms: float


@dataclass
class DartImpactKinematics:
    """DART 动能撞击与动量放大因子推演指标"""
    impact_energy_joules: float
    impact_energy_tnt_equivalent_tons: float
    dart_initial_momentum_kg_ms: float
    post_impact_semi_major_axis_m: float
    orbital_semi_major_axis_shrinkage_m: float
    orbital_period_reduction_minutes: float
    period_ratio: float
    dimorphos_orbit_speed_delta_ms: float
    beta_momentum_enhancement_factor: float


@dataclass
class HeraBrakingManoeuvreMetrics:
    """赫拉号 10-15 BRM-1 制动与交会动力学"""
    burn_duration_seconds: float
    burn_duration_minutes: float
    total_thrust_n: float
    total_impulse_ns: float
    estimated_mass_before_brm1_kg: float
    theoretical_delta_v_ms: float
    propellant_consumed_kg: float
    post_burn_mass_kg: float
    brm2_burn_duration_minutes: float
    brm2_theoretical_delta_v_ms: float


@dataclass
class DeepSpaceQuintetSchedule:
    """2026 年秋末人类深空五极黄金大冲刺时间线"""
    probe_name: str
    target: str
    key_milestone: str
    milestone_utc: datetime
    days_from_ref: float
    heliocentric_distance_au: float
    core_physical_regime: str
    extreme_phenomenon: str


class HeraPlanetaryDefenseRendezvousEngine:
    """赫拉号行星防御双小行星交会推演核心计算引擎"""

    def __init__(self, ref_time_utc: datetime = None):
        if ref_time_utc is None:
            self.ref_time_utc = datetime(2026, 10, 14, 16, 0, 0, tzinfo=timezone.utc)
        else:
            self.ref_time_utc = ref_time_utc

    def compute_asteroid_microgravity_metrics(self) -> AsteroidMicrogravityMetrics:
        """推演 Didymos 与 Dimorphos 的微重力场、逃逸速度与希尔球半径"""
        # Didymos 表面重力与逃逸速度
        g_didymos = (GRAVITATIONAL_CONSTANT * DIDYMOS_MASS_KG) / (DIDYMOS_RADIUS_M ** 2)
        v_esc_didymos = math.sqrt(2.0 * GRAVITATIONAL_CONSTANT * DIDYMOS_MASS_KG / DIDYMOS_RADIUS_M)
        
        # Didymos 赤道自转线速度与离心加速度
        omega_didymos = (2.0 * math.pi) / (DIDYMOS_ROTATION_PERIOD_HOURS * 3600.0)
        v_spin_eq = omega_didymos * DIDYMOS_RADIUS_M
        a_centrifugal = (omega_didymos ** 2) * DIDYMOS_RADIUS_M
        
        # 自转瓦解临界周期: 当赤道重力等于向心加速度 GM/R^2 = omega^2 R -> P_crit = 2*pi * sqrt(R^3 / GM)
        crit_omega = math.sqrt(GRAVITATIONAL_CONSTANT * DIDYMOS_MASS_KG / (DIDYMOS_RADIUS_M ** 3))
        p_crit_hours = (2.0 * math.pi / crit_omega) / 3600.0

        # Dimorphos 表面重力与逃逸速度
        g_dimorphos = (GRAVITATIONAL_CONSTANT * DIMORPHOS_MASS_KG) / (DIMORPHOS_RADIUS_M ** 2)
        v_esc_dimorphos = math.sqrt(2.0 * GRAVITATIONAL_CONSTANT * DIMORPHOS_MASS_KG / DIMORPHOS_RADIUS_M)

        # 双小行星系统在日心轨道 (1.644 AU) 上的希尔半径: r_H = a_helio * (M_sys / 3 M_sun)^(1/3)
        # MU_SUN = GM_sun km^3/s^2, M_sun = MU_SUN / G_km
        m_sun_kg = (MU_SUN * 1e9) / GRAVITATIONAL_CONSTANT
        ratio_sys_sun = SYSTEM_MASS_TOTAL_KG / (3.0 * m_sun_kg)
        r_hill_sys_km = (DIDYMOS_HELIO_A_AU * AU_KM) * (ratio_sys_sun ** (1.0 / 3.0))

        # Dimorphos 相对于 Didymos 的伴星希尔半径: r_H2 = a_binary * (M2 / 3 M1)^(1/3)
        ratio_m2_3m1 = DIMORPHOS_MASS_KG / (3.0 * DIDYMOS_MASS_KG)
        r_hill_dimorphos_m = DART_PRE_SEMI_MAJOR_AXIS_M * (ratio_m2_3m1 ** (1.0 / 3.0))

        # 撞击前 Dimorphos 轨道速度: v = sqrt(GM_sys / a)
        v_orb_pre = math.sqrt(MU_SYSTEM_M3S2 / DART_PRE_SEMI_MAJOR_AXIS_M)

        return AsteroidMicrogravityMetrics(
            didymos_surface_gravity_ms2=g_didymos,
            didymos_surface_gravity_milli_g=g_didymos / STANDARD_GRAVITY * 1000.0,
            didymos_escape_velocity_ms=v_esc_didymos,
            didymos_equatorial_spin_velocity_ms=v_spin_eq,
            didymos_spin_centrifugal_accel_ms2=a_centrifugal,
            didymos_spin_critical_period_hours=p_crit_hours,
            dimorphos_surface_gravity_ms2=g_dimorphos,
            dimorphos_surface_gravity_milli_g=g_dimorphos / STANDARD_GRAVITY * 1000.0,
            dimorphos_escape_velocity_ms=v_esc_dimorphos,
            system_hill_radius_km=r_hill_sys_km,
            dimorphos_hill_radius_m=r_hill_dimorphos_m,
            dimorphos_orbital_speed_pre_ms=v_orb_pre,
        )

    def compute_dart_impact_kinematics(self) -> DartImpactKinematics:
        """推演 DART 动能撞击能量、轨道收缩与动量增强因子 beta"""
        # 撞击动能: E_k = 1/2 * m * v^2
        energy_j = 0.5 * DART_SPACECRAFT_MASS_KG * (DART_IMPACT_SPEED_MS ** 2)
        tnt_tons = energy_j / 4.184e9 # 1 吨 TNT 标称 4.184 GJ
        p_dart = DART_SPACECRAFT_MASS_KG * DART_IMPACT_SPEED_MS

        # 开普勒第三定律解算半长轴变化: (a_post / a_pre) = (P_post / P_pre)^(2/3)
        period_ratio = DART_POST_PERIOD_SECONDS / DART_PRE_PERIOD_SECONDS
        a_post_m = DART_PRE_SEMI_MAJOR_AXIS_M * (period_ratio ** (2.0 / 3.0))
        delta_a_m = a_post_m - DART_PRE_SEMI_MAJOR_AXIS_M

        # 轨道线速度变化: delta_v = sqrt(GM / a_post) - sqrt(GM / a_pre)
        v_pre = math.sqrt(MU_SYSTEM_M3S2 / DART_PRE_SEMI_MAJOR_AXIS_M)
        v_post = math.sqrt(MU_SYSTEM_M3S2 / a_post_m)
        delta_v_ms = v_post - v_pre # 注意这是圆轨道速度变化，但实际上撞击引起即时速度减量

        # 瞬时迎面撞击动量变化 delta_v_instant:
        # 由能量守恒和活力公式，在撞击点 r = a_pre 处减速 delta_v_inst 使新轨道远点为 a_pre, 新半长轴为 a_post:
        # 2/r - 1/a_post = v_new^2 / GM -> v_new = sqrt(GM * (2/a_pre - 1/a_post))
        v_new_at_impact = math.sqrt(MU_SYSTEM_M3S2 * (2.0 / DART_PRE_SEMI_MAJOR_AXIS_M - 1.0 / a_post_m))
        delta_v_inst = v_pre - v_new_at_impact # 迎面减速量

        # 实际传递给 Dimorphos 的总冲量: Delta_p = M_dimorphos * delta_v_inst
        total_impulse_transferred = DIMORPHOS_MASS_KG * delta_v_inst
        # beta = total_impulse / p_dart
        beta_factor = total_impulse_transferred / p_dart

        return DartImpactKinematics(
            impact_energy_joules=energy_j,
            impact_energy_tnt_equivalent_tons=tnt_tons,
            dart_initial_momentum_kg_ms=p_dart,
            post_impact_semi_major_axis_m=a_post_m,
            orbital_semi_major_axis_shrinkage_m=abs(delta_a_m),
            orbital_period_reduction_minutes=DART_PERIOD_REDUCTION_SECONDS / 60.0,
            period_ratio=period_ratio,
            dimorphos_orbit_speed_delta_ms=delta_v_inst,
            beta_momentum_enhancement_factor=beta_factor,
        )

    def compute_hera_brm1_manoeuvre(self) -> HeraBrakingManoeuvreMetrics:
        """推演明天 (2026-10-15) 赫拉号 BRM-1 制动点火动力学"""
        t_burn_min = 93.0
        t_burn_sec = t_burn_min * 60.0 # 5580 s
        f_thrust = HERA_TOTAL_OCT_THRUST_N # 30.0 N
        total_impulse = f_thrust * t_burn_sec # 167,400 N*s

        # 赫拉号经历 DSM-1 (~166 m/s, ~65 kg) 和 DSM-2 (~367 m/s, 123 kg) 消耗后
        # 发射 1128 kg - 65 kg - 123 kg - 测试点火 ~10 kg = 约 930 kg
        mass_before_brm1 = 920.0
        
        # 推进剂消耗: Delta_m = Impulse / (g0 * Isp)
        propellant_kg = total_impulse / (STANDARD_GRAVITY * HERA_PROPULSION_ISP_S)
        mass_after_brm1 = mass_before_brm1 - propellant_kg

        # 齐奥尔科夫斯基火箭方程解算精确 Delta_V: Delta_v = Isp * g0 * ln(m0 / mf)
        delta_v_ms = HERA_PROPULSION_ISP_S * STANDARD_GRAVITY * math.log(mass_before_brm1 / mass_after_brm1)

        # BRM-2 点火 (31 分钟)
        t_burn_brm2_sec = 31.0 * 60.0
        impulse_brm2 = f_thrust * t_burn_brm2_sec
        prop_brm2 = impulse_brm2 / (STANDARD_GRAVITY * HERA_PROPULSION_ISP_S)
        delta_v_brm2 = HERA_PROPULSION_ISP_S * STANDARD_GRAVITY * math.log(mass_after_brm1 / (mass_after_brm1 - prop_brm2))

        return HeraBrakingManoeuvreMetrics(
            burn_duration_seconds=t_burn_sec,
            burn_duration_minutes=t_burn_min,
            total_thrust_n=f_thrust,
            total_impulse_ns=total_impulse,
            estimated_mass_before_brm1_kg=mass_before_brm1,
            theoretical_delta_v_ms=delta_v_ms,
            propellant_consumed_kg=propellant_kg,
            post_burn_mass_kg=mass_after_brm1,
            brm2_burn_duration_minutes=31.0,
            brm2_theoretical_delta_v_ms=delta_v_brm2,
        )

    def get_deep_space_quintet_schedule(self) -> List[DeepSpaceQuintetSchedule]:
        """构建 2026 年秋末人类深空五极黄金大冲刺矩阵 (The Grand Quintet)"""
        psp_p30 = datetime(2026, 12, 2, 0, 0, 0, tzinfo=timezone.utc)
        clipper_ega = datetime(2026, 12, 3, 21, 15, 0, tzinfo=timezone.utc)
        v1_lightday = datetime(2026, 11, 18, 0, 0, 0, tzinfo=timezone.utc)
        bepi_moi = datetime(2026, 11, 21, 0, 0, 0, tzinfo=timezone.utc)
        hera_brm1 = datetime(2026, 10, 15, 6, 0, 0, tzinfo=timezone.utc)

        events = [
            DeepSpaceQuintetSchedule(
                probe_name="ESA 赫拉号 (Hera)",
                target="双小行星 Didymos & Dimorphos",
                key_milestone="BRM-1 初始主制动点火 (93分钟持续点火减速 ~190 m/s，冲入双星捕获圈)",
                milestone_utc=hera_brm1,
                days_from_ref=(hera_brm1 - self.ref_time_utc).total_seconds() / 86400.0,
                heliocentric_distance_au=1.304,
                core_physical_regime="极微引力双星交会与行星防御勘查",
                extreme_phenomenon="反冲动量放大因子 beta=2.5 实测、1180m 双星近距操作、10 cm/s 立方星软着陆",
            ),
            DeepSpaceQuintetSchedule(
                probe_name="NASA 旅行者 1 号 (Voyager 1)",
                target="蛇夫座方向深空星际介质 (ISM)",
                key_milestone="跨越人类航天史上首个「整整 1 光日」物理距离边界 (259.02 亿公里)",
                milestone_utc=v1_lightday,
                days_from_ref=(v1_lightday - self.ref_time_utc).total_seconds() / 86400.0,
                heliocentric_distance_au=173.22,
                core_physical_regime="极远星际物理边界与极寒",
                extreme_phenomenon="2.7 K 宇宙微波背景微光、单向光行时整整 24.0 小时、0.35 aW 极限射电捕获",
            ),
            DeepSpaceQuintetSchedule(
                probe_name="ESA/JAXA 贝皮可伦坡 (BepiColombo)",
                target="水星 (Mercury)",
                key_milestone="水星引力捕获制动 (MOI) 与弱稳定性边界 (WSB) 决死入轨点火",
                milestone_utc=bepi_moi,
                days_from_ref=(bepi_moi - self.ref_time_utc).total_seconds() / 86400.0,
                heliocentric_distance_au=0.387,
                core_physical_regime="极深日心引力势能阱",
                extreme_phenomenon="-1405 MJ/kg 引力势能耗散、10.6 太阳常数高温、双星解耦极轨分化",
            ),
            DeepSpaceQuintetSchedule(
                probe_name="NASA 帕克太阳探测器 (PSP)",
                target="太阳日冕层 (Solar Corona)",
                key_milestone="第 30 次近日点穿越 (P30, 极限近日点 9.85 太阳半径)",
                milestone_utc=psp_p30,
                days_from_ref=(psp_p30 - self.ref_time_utc).total_seconds() / 86400.0,
                heliocentric_distance_au=0.04586,
                core_physical_regime="极热日冕炼狱与相对论极速",
                extreme_phenomenon="192 km/s 人类造物极速、647 kW/m² 强辐射炙烤、1400°C 防热屏障",
            ),
            DeepSpaceQuintetSchedule(
                probe_name="NASA 欧罗巴快船 (Europa Clipper)",
                target="木星系统 / 木卫二 (Europa)",
                key_milestone="地球引力助推 (EGA, 3200 km 掠地近地点甩尾跃入木星转移轨道)",
                milestone_utc=clipper_ega,
                days_from_ref=(clipper_ega - self.ref_time_utc).total_seconds() / 86400.0,
                heliocentric_distance_au=1.000,
                core_physical_regime="极宏轨道弹弓与深海生命巡航",
                extreme_phenomenon="双曲线偏折 63.2°、日心增速 +3.9 km/s、5.3 AU 弱光光伏与 1 TW 潮汐海洋",
            ),
        ]
        return events

    def get_summary_report(self) -> str:
        """生成人类深空五极黄金大冲刺与赫拉号推演综合文本摘要"""
        ast = self.compute_asteroid_microgravity_metrics()
        dart = self.compute_dart_impact_kinematics()
        brm = self.compute_hera_brm1_manoeuvre()
        quintet = self.get_deep_space_quintet_schedule()

        lines = [
            "================================================================================",
            "   赫拉号 (Hera) 行星防御双小行星交会与 2026 秋末深空五极黄金大冲刺推演",
            "================================================================================",
            f"推演基准时刻: {self.ref_time_utc.strftime('%Y-%m-%d %H:%M:%S UTC')}",
            "",
            "一、双小行星系统 (Didymos & Dimorphos) 微重力天体力学参量:",
            f"  - 主星 Didymos: 直径 {DIDYMOS_DIAMETER_M} m, 质量 {DIDYMOS_MASS_KG:.2e} kg, 密度 {DIDYMOS_DENSITY_KGM3} kg/m³",
            f"    * 表面重力: {ast.didymos_surface_gravity_ms2:.6f} m/s² ({ast.didymos_surface_gravity_milli_g:.3f} mG)",
            f"    * 表面逃逸速度: {ast.didymos_escape_velocity_ms:.3f} m/s ({ast.didymos_escape_velocity_ms*3.6:.2f} km/h)",
            f"    * 自转周期: {DIDYMOS_ROTATION_PERIOD_HOURS:.4f} h (临界瓦解极限 {ast.didymos_spin_critical_period_hours:.2f} h)",
            f"    * 赤道自转线速度: {ast.didymos_equatorial_spin_velocity_ms:.3f} m/s (赤道向心加速度占重力 {ast.didymos_spin_centrifugal_accel_ms2/ast.didymos_surface_gravity_ms2*100:.1f}%)",
            f"  - 伴星 Dimorphos: 直径 {DIMORPHOS_DIAMETER_M} m, 质量 {DIMORPHOS_MASS_KG:.2e} kg (主星的 {DIMORPHOS_MASS_KG/DIDYMOS_MASS_KG*100:.2f}%)",
            f"    * 表面重力: {ast.dimorphos_surface_gravity_ms2:.6f} m/s² ({ast.dimorphos_surface_gravity_milli_g:.3f} mG)",
            f"    * 表面逃逸速度: {ast.dimorphos_escape_velocity_ms*100.0:.2f} cm/s (仅 9.2 cm/s!)",
            f"  - 希尔球半径界标:",
            f"    * 双星系统日心希尔半径: {ast.system_hill_radius_km:.1f} km",
            f"    * Dimorphos 相对主星希尔半径: {ast.dimorphos_hill_radius_m:.1f} m (仅比星体半径 75.5m 大不到 100m, 无法维持闭合稳定卫星轨道)",
            "",
            "二、DART 动能撞击力学与动量增强反冲因子 beta:",
            f"  - 撞击动能: {dart.impact_energy_joules/1e9:.2f} GJ ({dart.impact_energy_tnt_equivalent_tons:.2f} 吨 TNT 当量)",
            f"  - DART 初始动量: {dart.dart_initial_momentum_kg_ms:.2e} kg·m/s",
            f"  - 轨道周期缩减: {dart.orbital_period_reduction_minutes:.2f} 分钟 ({DART_PERIOD_REDUCTION_SECONDS:.0f} 秒, 达 NASA 基准的 {DART_PERIOD_REDUCTION_SECONDS/73.0:.1f} 倍)",
            f"  - 轨道半长轴缩水: {dart.orbital_semi_major_axis_shrinkage_m:.1f} 米 (由 {DART_PRE_SEMI_MAJOR_AXIS_M} m 收缩至 {dart.post_impact_semi_major_axis_m:.1f} m)",
            f"  - 瞬时轨道减速量: {dart.dimorphos_orbit_speed_delta_ms*1000.0:.2f} mm/s",
            f"  - 动量增强因子 beta: {dart.beta_momentum_enhancement_factor:.2f} (碎石喷射反冲提供了整整 {(dart.beta_momentum_enhancement_factor-1.0)*100:.1f}% 的额外偏转推力!)",
            "",
            "三、赫拉号 (Hera) 关键制动变轨与交会 (明日 10-15 BRM-1 火线点火):",
            f"  - BRM-1 初始主制动点火: 2026-10-15 早晨 (持续 {brm.burn_duration_minutes:.1f} 分钟)",
            f"    * 点火推力器: 3 台 10N 轨控推力器 (总推力 {brm.total_thrust_n:.1f} N)",
            f"    * 累计点火总冲量: {brm.total_impulse_ns/1000.0:.1f} kN·s",
            f"    * 推进剂消耗: {brm.propellant_consumed_kg:.1f} kg (肼)",
            f"    * 理论减速度量 Delta_V: {brm.theoretical_delta_v_ms:.1f} m/s",
            f"  - BRM-2 补充精修制动: 2026-10-22 早晨 (持续 {brm.brm2_burn_duration_minutes:.1f} 分钟, Delta_V ~ {brm.brm2_theoretical_delta_v_ms:.1f} m/s)",
            f"  - 2026 年 11 月交会距地: 1.304 AU (1.95 亿公里, 单向光行时 10.84 分钟, 往返 21.68 分钟)",
            f"  - 立方星 Juventas 软着陆: 触地末速仅 {DIMORPHOS_LANDING_SPEED_MS*100.0:.1f} cm/s, 由 GRASS 微重力仪记录撞击回弹",
            "",
            "四、2026 年秋末人类深空五极黄金大冲刺 (The Grand Quintet Timeline):",
        ]

        for i, q in enumerate(quintet, 1):
            lines.append(f"  [{i}] {q.milestone_utc.strftime('%Y-%m-%d')} ({q.days_from_ref:+.1f}d) | {q.probe_name} -> {q.target}")
            lines.append(f"      - 里程碑: {q.key_milestone}")
            lines.append(f"      - 物理极值: {q.core_physical_regime} ({q.heliocentric_distance_au:.3f} AU) | {q.extreme_phenomenon}")

        lines.append("================================================================================")
        return "\n".join(lines)


if __name__ == "__main__":
    engine = HeraPlanetaryDefenseRendezvousEngine()
    print(engine.get_summary_report())
