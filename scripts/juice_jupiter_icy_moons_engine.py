"""
木卫三冰月探测器 (JUICE) 天体力学推演引擎与 2026 深空六极黄金舰队全景
========================================================================

涵盖:
1. 欧空局木卫三冰月探测器 (JUICE) 任务总览与双星对偶 (JUICE vs Europa Clipper)
2. 2026-09-28 第二次地球引力助推 (EGA-2) 双曲线解析天体力学 (8,640 km 高空掠过、20° 偏折、+3.5 km/s 增速、8.65h 地影电池严苛考验)
3. 2.3 年共振出向椭圆转移轨道动力学 (2026-09-28 至 2029-01-20 EGA-3, 远日点 2.50 AU 小行星带 223 Rosa 区域)
4. 5.2 AU 弱光低温光伏物理 (85 m² LILT GaAs 太阳翼、逆平方通量衰减至 3.69% 与百瓦级微功耗天体物理)
5. 太阳系最大卫星木卫三 (Ganymede) 本征物理、内置发电机偶极磁层与三明治液态大洋 (水储量超地球全海洋 2.5 倍)
6. 2026 年秋末人类深空六极黄金大冲刺全景 (The Grand Sextet: JUICE, Hera, Voyager 1, BepiColombo, Parker Solar Probe, Europa Clipper)
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
MU_JUPITER = 1.26686534e8                   # 木星引力常数 GM_jupiter km^3/s^2
SOLAR_CONSTANT_1AU = 1361.0                 # 1 AU 太阳辐射常数 W/m^2
STANDARD_GRAVITY = 9.80665                  # 地球标准重力加速度 g0, m/s^2

# 地球参量
EARTH_EQUATORIAL_RADIUS_KM = 6378.137       # 地球赤道半径 km
EARTH_ORBITAL_SPEED_KMS = 29.78             # 地球公转平均线速度 km/s

# 木星与伽利略冰卫星物理参量
JUPITER_RADIUS_KM = 71492.0                 # 木星赤道半径 km
JUPITER_SEMI_MAJOR_AXIS_AU = 5.2044         # 木星日心半长轴 AU

# 木卫三 (Ganymede, 太阳系卫星之王)
GANYMEDE_RADIUS_KM = 2634.1                 # 木卫三半径 km (直径 5268.2 km, 大于水星 4879 km 与泰坦 5150 km)
GANYMEDE_MASS_KG = 1.4819e23                # 木卫三质量 kg (约 0.0248 地球质量)
MU_GANYMEDE = 9887.8                        # 木卫三引力常数 km^3/s^2
GANYMEDE_SURFACE_GRAVITY_MS2 = 1.428        # 木卫三表面重力 m/s^2 (~0.146 g)
GANYMEDE_ORBIT_RADIUS_KM = 1070400.0        # 绕木轨道半长轴 km (~14.97 R_J)
GANYMEDE_ORBIT_PERIOD_DAYS = 7.155          # 绕木公转周期 天 (与木卫一、木卫二构成 1:2:4 拉普拉斯共振)
GANYMEDE_MAGNETIC_DIPOLE_TM3 = 1.3e13       # 木卫三本征内禀磁偶极矩 T*m^3
GANYMEDE_EQUATORIAL_B_NT = 719.0            # 木卫三表面赤道磁场强度 nT
JUPITER_AMBIENT_B_AT_GANYMEDE_NT = 120.0    # 木星在木卫三轨道处的背景环境磁场强度 nT

# 木卫二 (Europa, 快船主力勘查目标)
EUROPA_RADIUS_KM = 1560.8                   # 木卫二半径 km
EUROPA_MASS_KG = 4.80e22                    # 木卫二质量 kg
EUROPA_ORBIT_RADIUS_KM = 670900.0           # 绕木轨道半长轴 km (~9.38 R_J)

# 木卫四 (Callisto)
CALLISTO_RADIUS_KM = 2410.3                 # 木卫四半径 km
CALLISTO_MASS_KG = 1.0759e23                # 木卫四质量 kg
CALLISTO_ORBIT_RADIUS_KM = 1882700.0        # 绕木轨道半长轴 km (~26.33 R_J)

# JUICE 航天器系统物理参量
JUICE_LAUNCH_MASS_KG = 6070.0               # 发射湿重 kg (Ariane 5 发射)
JUICE_DRY_MASS_KG = 2420.0                  # 干重 kg
JUICE_PROPELLANT_MASS_KG = 3650.0           # 推进剂质量 kg
JUICE_SOLAR_ARRAY_AREA_M2 = 85.0            # 十字形双翼 10 块光伏阵列总面积 m²
JUICE_SOLAR_EFFICIENCY_LILT = 0.28          # 低温弱光 (LILT) 三结砷化镓电池效率 (~28% at -130°C)


@dataclass
class JuiceHyperbolicEga2Metrics:
    """JUICE 2026-09-28 第二次掠地引力助推 (EGA-2) 动力学指标"""
    flyby_datetime_utc: str
    perigee_altitude_km: float
    perigee_radius_km: float
    perigee_radius_earth_radii: float
    deflection_angle_deg: float
    hyperbolic_eccentricity: float
    hyperbolic_semi_major_axis_km: float
    hyperbolic_excess_velocity_kms: float
    perigee_velocity_kms: float
    perigee_velocity_kmh: float
    delta_v_vector_magnitude_kms: float
    heliocentric_velocity_boost_kms: float
    eclipse_duration_hours: float


@dataclass
class JuiceResonantOrbitMetrics:
    """JUICE EGA-2 至 EGA-3 共振转移动力学指标"""
    ega2_date: str
    ega3_target_date: str
    transfer_duration_days: float
    transfer_duration_years: float
    semi_major_axis_au: float
    semi_major_axis_km: float
    perihelion_distance_au: float
    aphelion_distance_au: float
    aphelion_distance_km: float
    orbital_eccentricity: float
    aphelion_target_region: str


@dataclass
class JuicePhotovoltaicMetrics:
    """弱光低温光伏能量转换指标"""
    distance_au: float
    solar_flux_wm2: float
    solar_flux_ratio_earth: float
    raw_intercepted_power_kw: float
    electric_power_output_w: float
    operating_temperature_c: float


@dataclass
class GanymedeSpacePhysicsMetrics:
    """木卫三空间物理与内部大洋特征指标"""
    radius_km: float
    mass_kg: float
    surface_gravity_ms2: float
    surface_gravity_earth_g: float
    equatorial_b_field_nt: float
    jupiter_background_b_nt: float
    magnetopause_standoff_radius_km: float
    magnetopause_altitude_km: float
    magnetopause_standoff_ganymede_radii: float
    ocean_layer_thickness_km: float
    ocean_volume_m3: float
    ocean_to_earth_oceans_ratio: float


@dataclass
class GrandSextetMissionStatus:
    """深空六极中单一旗舰任务即时态势"""
    mission_id: str
    mission_name: str
    agency: str
    target_event: str
    event_date: str
    countdown_days: float
    heliocentric_distance_au: float
    heliocentric_distance_km: float
    heliocentric_speed_kms: float
    solar_flux_wm2: float
    scientific_frontier: str


@dataclass
class GrandSextetOverview:
    """2026 年秋末深空六极黄金舰队总览"""
    reference_date_utc: str
    time_window_start: str
    time_window_end: str
    total_window_span_days: float
    missions: List[GrandSextetMissionStatus]
    min_heliocentric_distance_au: float
    max_heliocentric_distance_au: float
    distance_dynamic_range_ratio: float
    min_solar_flux_wm2: float
    max_solar_flux_wm2: float
    flux_dynamic_range_ratio: float
    min_speed_kms: float
    max_speed_kms: float
    speed_dynamic_range_ratio: float


class JuiceJupiterIcyMoonsEngine:
    """JUICE 木星冰月与 2026 深空六极综合天体力学推演引擎"""

    def __init__(self, ref_time_utc: datetime = None):
        if ref_time_utc is None:
            self.ref_time_utc = datetime(2026, 10, 14, 20, 0, 0, tzinfo=timezone.utc)
        else:
            self.ref_time_utc = ref_time_utc

    def compute_ega2_hyperbolic_metrics(self, altitude_km: float = 8640.0,
                                        deflection_deg: float = 20.0,
                                        heliocentric_boost_kms: float = 3.50,
                                        eclipse_hours: float = 8.65) -> JuiceHyperbolicEga2Metrics:
        """
        解算 2026-09-28 JUICE 第二次掠地引力助推 (EGA-2) 双曲线弹道参量
        """
        r_p = EARTH_EQUATORIAL_RADIUS_KM + altitude_km
        delta_rad = math.radians(deflection_deg)

        # 双曲线几何: sin(delta/2) = 1 / e_hyp
        e_hyp = 1.0 / math.sin(delta_rad / 2.0)
        a_hyp = r_p / (1.0 - e_hyp)  # 双曲线半长轴 (负值)

        # 渐近双曲线过剩速度 v_inf
        v_inf = math.sqrt(-MU_EARTH / a_hyp)

        # 近地点极速 v_p = sqrt(v_inf^2 + 2 * mu / r_p)
        v_p = math.sqrt(v_inf**2 + (2.0 * MU_EARTH / r_p))
        v_p_kmh = v_p * 3600.0

        # 地心速度增量矢量大小: |Delta v| = 2 * v_inf * sin(delta/2)
        delta_v_vec = 2.0 * v_inf * math.sin(delta_rad / 2.0)

        return JuiceHyperbolicEga2Metrics(
            flyby_datetime_utc="2026-09-28 11:45:00 UTC",
            perigee_altitude_km=altitude_km,
            perigee_radius_km=r_p,
            perigee_radius_earth_radii=r_p / EARTH_EQUATORIAL_RADIUS_KM,
            deflection_angle_deg=deflection_deg,
            hyperbolic_eccentricity=e_hyp,
            hyperbolic_semi_major_axis_km=a_hyp,
            hyperbolic_excess_velocity_kms=v_inf,
            perigee_velocity_kms=v_p,
            perigee_velocity_kmh=v_p_kmh,
            delta_v_vector_magnitude_kms=delta_v_vec,
            heliocentric_velocity_boost_kms=heliocentric_boost_kms,
            eclipse_duration_hours=eclipse_hours
        )

    def compute_outbound_resonant_orbit(self, transfer_days: float = 845.0) -> JuiceResonantOrbitMetrics:
        """
        解算 EGA-2 (2026-09-28) 至 EGA-3 (2029-01-20) 2.3 年共振出向椭圆轨道
        """
        transfer_years = transfer_days / 365.25
        # 开普勒第三定律: a = P^(2/3) (单位: AU)
        a_au = transfer_years ** (2.0 / 3.0)
        a_km = a_au * AU_KM

        # 近日点在地球公转轨道附近 r_peri = 1.00 AU
        r_peri_au = 1.000
        # 远日点 r_aph = 2*a - r_peri
        r_aph_au = 2.0 * a_au - r_peri_au
        r_aph_km = r_aph_au * AU_KM

        # 偏心率 e = (r_aph - r_peri) / (r_aph + r_peri)
        ecc = (r_aph_au - r_peri_au) / (r_aph_au + r_peri_au)

        return JuiceResonantOrbitMetrics(
            ega2_date="2026-09-28",
            ega3_target_date="2029-01-20",
            transfer_duration_days=transfer_days,
            transfer_duration_years=transfer_years,
            semi_major_axis_au=a_au,
            semi_major_axis_km=a_km,
            perihelion_distance_au=r_peri_au,
            aphelion_distance_au=r_aph_au,
            aphelion_distance_km=r_aph_km,
            orbital_eccentricity=ecc,
            aphelion_target_region="主小行星带外缘 (接近 223 Rosa 区域, 2.50 AU)"
        )

    def compute_photovoltaic_power(self, distance_au: float) -> JuicePhotovoltaicMetrics:
        """
        计算指定日心距离处的太阳辐射通量与 JUICE 85 m² 光伏阵列输出功率
        """
        flux = SOLAR_CONSTANT_1AU / (distance_au ** 2)
        ratio = 1.0 / (distance_au ** 2)
        intercepted_kw = (flux * JUICE_SOLAR_ARRAY_AREA_M2) / 1000.0

        # 温度与 LILT 效率建模:
        # 在 1 AU 处 T ~ +20°C, 效率 ~24%; 在 5.2 AU 处 T ~ -130°C, LILT 效率提升至 ~28%
        if distance_au <= 1.0:
            temp_c = 60.0 - 40.0 * distance_au
            eff = 0.24
        else:
            temp_c = 20.0 - 35.0 * (distance_au - 1.0)
            eff = 0.28

        electric_w = flux * JUICE_SOLAR_ARRAY_AREA_M2 * eff

        return JuicePhotovoltaicMetrics(
            distance_au=distance_au,
            solar_flux_wm2=flux,
            solar_flux_ratio_earth=ratio,
            raw_intercepted_power_kw=intercepted_kw,
            electric_power_output_w=electric_w,
            operating_temperature_c=temp_c
        )

    def compute_ganymede_space_physics(self) -> GanymedeSpacePhysicsMetrics:
        """
        推演木卫三 (Ganymede) 内禀发电机磁偶极层与三明治液态大洋物理指标
        """
        # 偶极磁场抵御木星磁层压强平衡: R_mp / R_G ~ (2 * B_0 / B_J)^(1/3)
        b_ratio = (2.0 * GANYMEDE_EQUATORIAL_B_NT) / JUPITER_AMBIENT_B_AT_GANYMEDE_NT
        standoff_ratio = b_ratio ** (1.0 / 3.0)
        standoff_radius_km = GANYMEDE_RADIUS_KM * standoff_ratio
        standoff_altitude_km = standoff_radius_km - GANYMEDE_RADIUS_KM

        # 液态水海洋估算:
        # 外层 Ice I 壳厚度 ~150 km, 下方液态海水层厚度 ~100 km (夹在 Ice I 与高压冰相之间)
        r_outer = (GANYMEDE_RADIUS_KM - 150.0) * 1000.0  # 米
        r_inner = (GANYMEDE_RADIUS_KM - 250.0) * 1000.0  # 米
        ocean_vol_m3 = (4.0 / 3.0) * math.pi * (r_outer**3 - r_inner**3)

        # 地球全部大洋水体积约 1.35e18 m^3
        earth_oceans_vol_m3 = 1.35e18
        ocean_ratio = ocean_vol_m3 / earth_oceans_vol_m3

        return GanymedeSpacePhysicsMetrics(
            radius_km=GANYMEDE_RADIUS_KM,
            mass_kg=GANYMEDE_MASS_KG,
            surface_gravity_ms2=GANYMEDE_SURFACE_GRAVITY_MS2,
            surface_gravity_earth_g=GANYMEDE_SURFACE_GRAVITY_MS2 / STANDARD_GRAVITY,
            equatorial_b_field_nt=GANYMEDE_EQUATORIAL_B_NT,
            jupiter_background_b_nt=JUPITER_AMBIENT_B_AT_GANYMEDE_NT,
            magnetopause_standoff_radius_km=standoff_radius_km,
            magnetopause_altitude_km=standoff_altitude_km,
            magnetopause_standoff_ganymede_radii=standoff_ratio,
            ocean_layer_thickness_km=100.0,
            ocean_volume_m3=ocean_vol_m3,
            ocean_to_earth_oceans_ratio=ocean_ratio
        )

    def compute_2026_grand_sextet_timeline(self) -> GrandSextetOverview:
        """
        构建 2026 年秋末人类深空六极 (The Grand Sextet) 黄金舰队即时态势与全景联立
        """
        # 基准时间: 2026-10-14 20:00:00 UTC
        ref_dt = self.ref_time_utc

        missions_data = [
            # 1. ESA JUICE
            {
                "id": "juice",
                "name": "ESA 木卫三冰月探测器 (JUICE)",
                "agency": "ESA (欧洲航天局)",
                "target_event": "第二次掠地引力助推 (EGA-2, 8640 km 高空掠过)",
                "event_date": "2026-09-28 11:45 UTC",
                "event_dt": datetime(2026, 9, 28, 11, 45, tzinfo=timezone.utc),
                "r_au": 1.050,
                "speed_kms": 32.5,
                "scientific_frontier": "2031 木星与 2034 首次入轨地外卫星 (木卫三磁层与三明治液态大洋探测)"
            },
            # 2. ESA Hera
            {
                "id": "hera",
                "name": "ESA 赫拉号双小行星勘验器 (Hera)",
                "agency": "ESA (欧洲航天局)",
                "target_event": "BRM-1 93分钟主制动点火冲入交会圈 (明日早晨！)",
                "event_date": "2026-10-15 06:00 UTC",
                "event_dt": datetime(2026, 10, 15, 6, 0, tzinfo=timezone.utc),
                "r_au": 1.304,
                "speed_kms": 22.1,
                "scientific_frontier": "行星防御撞击坑勘查、碎石堆微重力与反冲放大因子 beta 闭环实测"
            },
            # 3. NASA Voyager 1
            {
                "id": "voyager1",
                "name": "NASA 旅行者 1 号 (Voyager 1)",
                "agency": "NASA (美国国家航空航天局)",
                "target_event": "历史性跨越 1 光日 (24 光时) 物理边界",
                "event_date": "2026-11-18 12:00 UTC",
                "event_dt": datetime(2026, 11, 18, 12, 0, tzinfo=timezone.utc),
                "r_au": 173.22,
                "speed_kms": 16.9,
                "scientific_frontier": "人类最远恒星际介质直接原位采样、极微弱信号与半个世纪星际续航"
            },
            # 4. ESA/JAXA BepiColombo
            {
                "id": "bepicolombo",
                "name": "ESA/JAXA 贝皮可伦坡水星双星 (BepiColombo)",
                "agency": "ESA / JAXA (欧日联合)",
                "target_event": "水星轨道捕获制动 (MOI 196分钟主减速点火)",
                "event_date": "2026-11-21 09:00 UTC",
                "event_dt": datetime(2026, 11, 21, 9, 0, tzinfo=timezone.utc),
                "r_au": 0.3871,
                "speed_kms": 47.9,
                "scientific_frontier": "克服 1405 MJ/kg 势能阱、10 倍太阳常数炙烤与水星发电机解耦"
            },
            # 5. NASA Parker Solar Probe
            {
                "id": "parker",
                "name": "NASA 帕克太阳探测器 (Parker Solar Probe)",
                "agency": "NASA (美国国家航空航天局)",
                "target_event": "第 30 次极限近日点穿透日冕 (P30, 9.85 R_sun)",
                "event_date": "2026-12-02 18:00 UTC",
                "event_dt": datetime(2026, 12, 2, 18, 0, tzinfo=timezone.utc),
                "r_au": 0.04586,
                "speed_kms": 192.2,
                "scientific_frontier": "192 km/s 人类极速、1400°C 隔热屏障与触摸日冕亚阿尔芬流区"
            },
            # 6. NASA Europa Clipper
            {
                "id": "clipper",
                "name": "NASA 欧罗巴快船 (Europa Clipper)",
                "agency": "NASA (美国国家航空航天局)",
                "target_event": "MEGA 地球引力弹弓掠地 (3200 km 高空, +3.9 km/s)",
                "event_date": "2026-12-03 21:15 UTC",
                "event_dt": datetime(2026, 12, 3, 21, 15, tzinfo=timezone.utc),
                "r_au": 0.4679,
                "speed_kms": 34.2,
                "scientific_frontier": "2030 抵达木星、49 次超低空掠飞刺探木卫二冰下宜居海洋"
            }
        ]

        mission_statuses = []
        r_list = []
        flux_list = []
        speed_list = []

        for m in missions_data:
            dt_diff = (m["event_dt"] - ref_dt).total_seconds() / 86400.0
            r = m["r_au"]
            speed = m["speed_kms"]
            flux = SOLAR_CONSTANT_1AU / (r ** 2)

            r_list.append(r)
            flux_list.append(flux)
            speed_list.append(speed)

            mission_statuses.append(GrandSextetMissionStatus(
                mission_id=m["id"],
                mission_name=m["name"],
                agency=m["agency"],
                target_event=m["target_event"],
                event_date=m["event_date"],
                countdown_days=dt_diff,
                heliocentric_distance_au=r,
                heliocentric_distance_km=r * AU_KM,
                heliocentric_speed_kms=speed,
                solar_flux_wm2=flux,
                scientific_frontier=m["scientific_frontier"]
            ))

        min_r, max_r = min(r_list), max(r_list)
        min_flux, max_flux = min(flux_list), max(flux_list)
        min_spd, max_spd = min(speed_list), max(speed_list)

        return GrandSextetOverview(
            reference_date_utc=ref_dt.strftime("%Y-%m-%d %H:%M:%S UTC"),
            time_window_start="2026-09-28",
            time_window_end="2026-12-03",
            total_window_span_days=66.4,
            missions=mission_statuses,
            min_heliocentric_distance_au=min_r,
            max_heliocentric_distance_au=max_r,
            distance_dynamic_range_ratio=max_r / min_r,
            min_solar_flux_wm2=min_flux,
            max_solar_flux_wm2=max_flux,
            flux_dynamic_range_ratio=max_flux / min_flux,
            min_speed_kms=min_spd,
            max_speed_kms=max_spd,
            speed_dynamic_range_ratio=max_spd / min_spd
        )

    def generate_comprehensive_report(self) -> str:
        """
        生成学术推演与工程报告完整 Markdown 文本
        """
        ega2 = self.compute_ega2_hyperbolic_metrics()
        res_orbit = self.compute_outbound_resonant_orbit()
        pv_earth = self.compute_photovoltaic_power(1.0)
        pv_jup = self.compute_photovoltaic_power(5.2044)
        pv_aph = self.compute_photovoltaic_power(res_orbit.aphelion_distance_au)
        ganymede = self.compute_ganymede_space_physics()
        sextet = self.compute_2026_grand_sextet_timeline()

        lines = [
            "# 欧空局木卫三冰月探测器 (JUICE) 天体力学推演与 2026 秋末深空六极黄金舰队全景报告",
            f"> 推演基准时间: {self.ref_time_utc.strftime('%Y-%m-%d %H:%M:%S UTC')} | 报告作者: Hoshi",
            "",
            "## 1. 2026-09-28 JUICE 第二次掠地引力助推 (EGA-2) 双曲线天体力学解析",
            f"- **近掠高度与地心距**: 掠地高度 $h_p = {ega2.perigee_altitude_km:.1f}\\text{{ km}}$，地心径向距离 $r_p = {ega2.perigee_radius_km:.2f}\\text{{ km}}$（相当于 **${ega2.perigee_radius_earth_radii:.3f} R_\\oplus$**）；",
            f"- **双曲线偏转角与偏心率**: 渐近线偏折角 $\\delta = {ega2.deflection_angle_deg:.1f}^\\circ$，双曲线偏心率 $e_{{\\text{{hyp}}}} = 1 / \\sin(\\delta/2) = \\mathbf{{{ega2.hyperbolic_eccentricity:.4f}}}$；",
            f"- **渐近双曲线过剩速度**: $v_\\infty = \\sqrt{{-\\mu_\\oplus / a}} = \\mathbf{{{ega2.hyperbolic_excess_velocity_kms:.3f}\\text{{ km/s}}}}$；",
            f"- **近地点极速**: $v_p = \\sqrt{{v_\\infty^2 + 2\\mu_\\oplus/r_p}} = \\mathbf{{{ega2.perigee_velocity_kms:.3f}\\text{{ km/s}}}}$（**{ega2.perigee_velocity_kmh:,.1f} km/h**）；",
            f"- **地心速度偏转矢量**: $|\\Delta \\vec{{v}}| = 2 v_\\infty \\sin(\\delta/2) = \\mathbf{{{ega2.delta_v_vector_magnitude_kms:.3f}\\text{{ km/s}}}}$；",
            f"- **日心速度净增益**: 顺向地球公转轨道增益 $\\mathbf{{+{ega2.heliocentric_velocity_boost_kms:.2f}\\text{{ km/s}}}}$；",
            f"- **地影电池极限考验**: 持续长达 **{ega2.eclipse_duration_hours:.2f} 小时** 零光照全日食暗区，完全依托机载锂电池维持科学与姿控生命体征。",
            "",
            "## 2. EGA-2 至 EGA-3 共振出向椭圆轨道动力学 (2026-09-28 -> 2029-01-20)",
            f"- **共振转移周期**: 共计 $\\Delta t = {res_orbit.transfer_duration_days:.1f}\\text{{ 天}} \\approx \\mathbf{{{res_orbit.transfer_duration_years:.3f}\\text{{ 年}}}}$；",
            f"- **日心半长轴**: $a = P^{{2/3}} = \\mathbf{{{res_orbit.semi_major_axis_au:.4f}\\text{{ AU}}}}$（约 ${res_orbit.semi_major_axis_km:,.0f}\\text{{ km}}$）；",
            f"- **远日点与近日点**: 近日点 $r_p = {res_orbit.perihelion_distance_au:.3f}\\text{{ AU}}$，远日点深潜至 **${res_orbit.aphelion_distance_au:.3f}\\text{{ AU}}$**（**{res_orbit.aphelion_distance_km:,.0f} km**，{res_orbit.aphelion_target_region}）；",
            f"- **轨道偏心率**: $e = \\mathbf{{{res_orbit.orbital_eccentricity:.4f}}}$。",
            "",
            "## 3. 弱光低温光伏物理 (LILT 85 m² 太阳翼逆平方衰减)",
            f"- **地球 1.0 AU 处**: 辐射通量 **{pv_earth.solar_flux_wm2:.1f} W/m²**，截获辐射功率 {pv_earth.raw_intercepted_power_kw:.1f} kW，输出电功率 **{pv_earth.electric_power_output_w:.1f} W**；",
            f"- **小行星带远日点 2.50 AU 处**: 通量衰减至 **{pv_aph.solar_flux_wm2:.1f} W/m²**（地球的 {pv_aph.solar_flux_ratio_earth*100:.2f}%），阵列功率 {pv_aph.electric_power_output_w:.1f} W；",
            f"- **木星 5.20 AU 处**: 通量暴跌至 **{pv_jup.solar_flux_wm2:.2f} W/m²**（仅为地球的 **{pv_jup.solar_flux_ratio_earth*100:.2f}%**！）；",
            f"- **低温增益机制**: 凭借三结 GaAs LILT 电池在 $-130^\\circ\\text{{C}}$ 低温下的带隙优化，仍实现稳定 **{pv_jup.electric_power_output_w:.1f} W** 纯电供应。",
            "",
            "## 4. 太阳系卫星之王木卫三 (Ganymede) 空间物理与三明治液态大洋",
            f"- **几何与重力**: 半径 $R_G = {ganymede.radius_km:.1f}\\text{{ km}}$（超越水星 4,879 km），表面重力 $g = {ganymede.surface_gravity_ms2:.3f}\\text{{ m/s}}^2$（**{ganymede.surface_gravity_earth_g:.3f} g_\\oplus$**）；",
            f"- **偶极内禀磁层**: 表面赤道磁场 **{ganymede.equatorial_b_field_nt:.1f} nT**，木星背景磁场 {ganymede.jupiter_background_b_nt:.1f} nT；",
            f"- **磁层顶驻点距离**: 磁阻平衡距离 $R_{{mp}} = \\mathbf{{{ganymede.magnetopause_standoff_radius_km:,.1f}\\text{{ km}}}}$（相当于 **${ganymede.magnetopause_standoff_ganymede_radii:.2f} R_G$**，高度 ${ganymede.magnetopause_altitude_km:,.1f}\\text{{ km}}$），构成“木星巨磁层包裹中的微型磁层泡”；",
            f"- **三明治大洋储量**: 夹持于 Ice I 壳（150 km）与高压冰层间厚达 **{ganymede.ocean_layer_thickness_km:.0f} km** 的液态水海水层，估算总体积高达 **{ganymede.ocean_volume_m3:.2e} m³**，达到**地球全部大洋水量的 {ganymede.ocean_to_earth_oceans_ratio:.2f} 倍**！",
            "",
            "## 5. 2026 年秋末人类深空六极 (The Grand Sextet) 黄金舰队时空大交响",
            f"在 2026 年 9 月 28 日至 12 月 3 日短短 **{sextet.total_window_span_days:.1f} 天**（约 2 个月）历史性窗口内，人类现役六大旗舰汇聚巅峰时刻：",
            ""
        ]

        for idx, m in enumerate(sextet.missions, 1):
            cd_str = f"倒计时 {m.countdown_days:.1f} 天" if m.countdown_days >= 0 else f"已过去 {-m.countdown_days:.1f} 天"
            lines.append(f"### {idx}. {m.mission_name} [{cd_str}]")
            lines.append(f"- **机构与事件**: {m.agency} · {m.target_event} ({m.event_date})")
            lines.append(f"- **即时日心状态**: 日心距 **{m.heliocentric_distance_au:.4f} AU** ({m.heliocentric_distance_km:,.0f} km) · 速度 **{m.heliocentric_speed_kms:.1f} km/s** · 能流 **{m.solar_flux_wm2:.2f} W/m²**")
            lines.append(f"- **科学与探索前沿**: {m.scientific_frontier}")
            lines.append("")

        lines.extend([
            "## 6. 六极物理极限张力全景对比",
            f"- **空间距离跨度**: 从帕克近日点 **{sextet.min_heliocentric_distance_au:.5f} AU** 到旅行者 1 号 **{sextet.max_heliocentric_distance_au:.2f} AU**，极距比高达 **{sextet.distance_dynamic_range_ratio:,.1f} 倍**；",
            f"- **辐射能流跨度**: 从旅行者 1 号的微弱星际辐射 **{sextet.min_solar_flux_wm2:.3e} W/m²** 到帕克近日点的灼热炼狱 **{sextet.max_solar_flux_wm2:,.0f} W/m²**，跨越整整 **{sextet.flux_dynamic_range_ratio:,.0f} 倍**（超 1,438 万倍！）；",
            f"- **航天极速跨度**: 从旅行者 1 号的 **{sextet.min_speed_kms:.1f} km/s** 到帕克的 **{sextet.max_speed_kms:.1f} km/s**，跨越 **{sextet.speed_dynamic_range_ratio:.2f} 倍**；",
            "- **终极科学对偶**: 极热恒星日冕、极寒星际边界、水星深引力势能陷阱、极微重力双小行星、以及木卫二与木卫三两大外行星冰下浩瀚生命之海。",
            ""
        ])

        return "\n".join(lines)


if __name__ == "__main__":
    engine = JuiceJupiterIcyMoonsEngine()
    print(engine.generate_comprehensive_report())
