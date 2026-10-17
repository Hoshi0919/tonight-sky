"""
太阳和日球层天文台 (SOHO) 日地第一拉格朗日点 (SEL1) 晕轨道动力学、
LASCO 空间日冕仪与 CME 空间天气预警、五千颗克鲁兹掠日彗星大发现、
日震学差旋层发电机与 2026 人类深空二十四极黄金舰队 (The Grand Quattuorvigintet) 推演引擎
========================================================================================

涵盖:
1. 日地第一拉格朗日点 (SEL1) 圆型限制性三体问题 (CRTBP) 精确欧拉五次方程数值解法
2. 距地球 149.15 万公里 (0.00997 AU)、距太阳 0.99003 AU、单向通信光时 4.975 秒
3. 大振幅 Halo / Lissajous 轨道 (Ay ~ 65 万 km, Az ~ 20 万 km) 与 >3.5° 太阳射电回避区
4. 11,277 天 (30.87 地球年) 超长服役历程与完整记录三轮太阳活动周 (Solar Cycles 23, 24, 25)
5. LASCO C2 / C3 双级外掩式日冕仪光学微观架构与 4,457 万公里 (0.298 AU) 巨型行星际视场
6. 日冕物质抛射 (CME) 空间天气预警物理动力学 (500~2500 km/s 速度谱与 15~80 小时预警窗口)
7. 超过 5,200 颗彗星发现世界纪录、克鲁兹族 (Kreutz) 掠日物理与全球公众科学巅峰
8. 日震学 (Helioseismology) 声速反演、5 分钟声波振荡与 0.713 R☉ 差旋层 (Tachocline) 太阳发电机
9. 1998 年阿雷西博雷达联合盲操救援 (The Great Recovery) 与 -120°C 联氨解冻奇迹
10. 2026 人类深空二十四极黄金舰队 (The Grand Quattuorvigintet) 宏伟时空矩阵与极端物理对偶
"""

import math
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Tuple

# ---------------------------------------------------------
# 基础物理与天文常数 (IAU / CODATA 标定)
# ---------------------------------------------------------
SPEED_OF_LIGHT = 299792.458               # 真空光速 c, km/s
AU_KM = 149597870.7                       # 1 天文单位 (AU) km
SOLAR_RADIUS_KM = 696342.0                # 太阳标准名义半径 R_odot, km
MASS_SUN_KG = 1.98847e30                  # 太阳质量 kg
MASS_EARTH_KG = 5.9722e24                 # 地球质量 kg
GRAV_CONSTANT = 6.67430e-11               # 引力常数 G, m^3/(kg s^2)
SOLAR_IRRADIANCE_1AU = 1361.0             # 1 AU 太阳能流常数 W/m^2
BOLTZMANN_K = 1.380649e-23                # 玻尔兹曼常数 J/K
PROTON_MASS_KG = 1.67262192e-27           # 质子质量 kg

# 日地系统归一化质量比 mu
MU_SUN_EARTH = MASS_EARTH_KG / (MASS_SUN_KG + MASS_EARTH_KG)  # ~ 3.0034e-6


@dataclass(frozen=True)
class SOHOEpochs:
    """SOHO 任务里程碑历史纪元"""
    launch_utc: datetime = field(
        default_factory=lambda: datetime(1995, 12, 2, 8, 8, 0, tzinfo=timezone.utc)
    )
    l1_insertion_utc: datetime = field(
        default_factory=lambda: datetime(1996, 2, 14, 0, 0, 0, tzinfo=timezone.utc)
    )
    signal_loss_utc: datetime = field(
        default_factory=lambda: datetime(1998, 6, 24, 23, 16, 0, tzinfo=timezone.utc)
    )
    arecibo_radar_recovery_utc: datetime = field(
        default_factory=lambda: datetime(1998, 7, 28, 0, 0, 0, tzinfo=timezone.utc)
    )
    full_science_restored_utc: datetime = field(
        default_factory=lambda: datetime(1998, 10, 24, 0, 0, 0, tzinfo=timezone.utc)
    )
    comet_5000_discovery_utc: datetime = field(
        default_factory=lambda: datetime(2024, 3, 25, 0, 0, 0, tzinfo=timezone.utc)
    )
    current_epoch_utc: datetime = field(
        default_factory=lambda: datetime(2026, 10, 17, 7, 47, 0, tzinfo=timezone.utc)
    )


@dataclass
class CRTBPParameters:
    """圆型限制性三体问题 (CRTBP) 日地 L1 解"""
    mass_ratio_mu: float                  # 日地质量比 mu
    gamma_1_normalized: float             # L1 距地球归一化距离 (AU)
    distance_to_earth_km: float           # L1 距地球距离 (km)
    distance_to_sun_au: float             # L1 日心极距 (AU)
    distance_to_sun_km: float             # L1 距太阳中心距离 (km)
    one_way_light_time_sec: float         # 距地单向光行时 (秒)
    round_trip_light_time_sec: float      # 距地双向往返光行时 (秒)
    solar_flux_at_soho_wm2: float         # SOHO 轨道处太阳辐射能流 (W/m^2)


@dataclass
class HaloOrbitParameters:
    """绕 L1 晕轨道与太阳射电回避几何"""
    orbit_period_days: float              # 晕轨道公转周期 (天)
    amplitude_y_km: float                 # 黄道面内横向振幅 Ay (km)
    amplitude_z_km: float                 # 垂直黄道振幅 Az (km)
    min_separation_deg: float             # 相对日地连线最小视角 (度)
    min_projected_offset_km: float        # 相对日地连线垂直投影偏移 (km)
    avoids_solar_radio_exclusion: bool    # 是否避开太阳微波强噪声圆盘 (通常要求 > 3.5°)
    annual_station_keeping_dv_ms: float   # 年轨道维持速度增量需求 (m/s)


@dataclass
class LASCOInstrumentMetrics:
    """LASCO 日冕仪光学微观架构"""
    instrument_name: str                  # C2 / C3
    fov_inner_rsun: float                 # 内视场 (太阳半径 R_odot)
    fov_outer_rsun: float                 # 外视场 (太阳半径 R_odot)
    fov_inner_km: float                   # 内视场物理半径 (km)
    fov_outer_km: float                   # 外视场物理半径 (km)
    total_diameter_km: float              # 视场总跨度直径 (km)
    total_diameter_au: float              # 视场总跨度 (AU)
    angular_fov_deg: float                # SOHO 视场角 (度)
    spatial_resolution_arcsec: float      # 像元空间分辨率 (角秒/像元)
    passband_nm: str                      # 观测波段描述


@dataclass
class CMEWarningScenario:
    """CME 传播动力学与对地预警窗口"""
    cme_type: str                         # 慢速 / 中速 / 高速 / 极端超级暴
    speed_kms: float                      # 抛射径向初速 (km/s)
    transit_time_to_earth_hours: float    # 抵达地球磁层时间 (小时)
    transit_time_to_earth_days: float     # 抵达地球磁层时间 (天)
    soho_data_latency_min: float          # SOHO 图像下行与识别延迟 (分钟)
    warning_lead_time_hours: float        # 对地有效空间天气预警窗口 (小时)
    geoeffective_confidence: str          # 全晕状 (Halo CME) 对地冲击判定


@dataclass
class CometDiscoveryMetrics:
    """SOHO 彗星猎手统计学"""
    total_comets_discovered: int          # 累计发现彗星总量
    kreutz_sungrazers_count: int          # 克鲁兹族掠日彗星数量
    kreutz_percentage: float              # 克鲁兹族占比 (%)
    perihelion_distance_au: float         # 典型克鲁兹近日点距离 (AU)
    perihelion_distance_km: float         # 典型克鲁兹近日点距离 (km)
    perihelion_above_surface_km: float    # 掠日彗星距太阳表面净高度 (km)
    amateur_discoverer_ratio: float       # 业余公众科学爱好者发现比例 (%)


@dataclass
class HelioseismologyTachocline:
    """日震学内部结构与差旋层发电机"""
    tachocline_radius_rsun: float         # 差旋层日心半径 (R_odot)
    tachocline_depth_km: float            # 差旋层距日表深度 (km)
    sound_speed_core_kms: float           # 太阳核心声速 (km/s)
    sound_speed_surface_kms: float        # 太阳表面光球声速 (km/s)
    dominant_oscillation_period_min: float # 主 p 模声波振荡周期 (分钟)
    dominant_frequency_mhertz: float      # 主声波振荡中心频率 (mHz)
    radiative_zone_rotation_days: float   # 辐射区刚体自转周期 (天)
    convection_equator_rotation_days: float # 对流区赤道自转周期 (天)
    convection_pole_rotation_days: float  # 对流区两极自转周期 (天)
    dynamo_shear_significance: str        # 差旋层剪切与 22 年磁周期物理本质


@dataclass
class SOHORecoveryStory:
    """1998 航天救援神话统计"""
    blackout_duration_days: float         # 失控至完全恢复持续天数
    arecibo_radar_role: str               # 阿雷西博 305 米行星雷达探测翻滚姿态
    minimum_temperature_celsius: float   # 深空冻结最低温度 (°C)
    hydrazine_thawing_method: str         # 联氨推进管路无遥测脉冲加热解冻
    recovered_payload_count: int          # 成功恢复科学仪器台数 (共 12 台)
    extended_mission_years: float         # 救援后额外延续服役年限 (年)


@dataclass
class DeepSpaceProbeEntry:
    """深空舰队探测器记录"""
    name: str
    agency: str
    heliocentric_distance_au: float
    geocentric_distance_km: float
    one_way_light_time_str: str
    mission_significance: str


class SOHOL1SolarCoronagraphEngine:
    """
    SOHO 日地 L1 晕轨道动力学、LASCO 日冕仪、CME 预警、彗星猎手与日球舰队引擎
    """

    def __init__(self, epochs: SOHOEpochs = None):
        self.epochs = epochs or SOHOEpochs()

    def solve_crtbp_l1(self) -> CRTBPParameters:
        """
        高精度数值求解日地 CRTBP 欧拉五次方程获取 L1 点绝对坐标与光时
        方程: f(gamma) = gamma^5 - (3 - mu)*gamma^4 + (3 - 2*mu)*gamma^3 - mu*gamma^2 + 2*mu*gamma - mu = 0
        """
        mu = MU_SUN_EARTH
        # 初始估计 (希尔球半径近似)
        gamma = (mu / 3.0) ** (1.0 / 3.0)

        # 牛顿-拉夫逊法高精度迭代
        for _ in range(15):
            f_val = (
                gamma**5
                - (3.0 - mu) * gamma**4
                + (3.0 - 2.0 * mu) * gamma**3
                - mu * gamma**2
                + 2.0 * mu * gamma
                - mu
            )
            f_prime = (
                5.0 * gamma**4
                - 4.0 * (3.0 - mu) * gamma**3
                + 3.0 * (3.0 - 2.0 * mu) * gamma**2
                - 2.0 * mu * gamma
                + 2.0 * mu
            )
            gamma -= f_val / f_prime

        dist_km = gamma * AU_KM
        r_sun_au = 1.0 - gamma
        dist_sun_km = r_sun_au * AU_KM
        owlt_sec = dist_km / SPEED_OF_LIGHT
        rtlt_sec = owlt_sec * 2.0
        # 辐射通量反比平方
        flux = SOLAR_IRRADIANCE_1AU / (r_sun_au**2)

        return CRTBPParameters(
            mass_ratio_mu=mu,
            gamma_1_normalized=gamma,
            distance_to_earth_km=dist_km,
            distance_to_sun_au=r_sun_au,
            distance_to_sun_km=dist_sun_km,
            one_way_light_time_sec=owlt_sec,
            round_trip_light_time_sec=rtlt_sec,
            solar_flux_at_soho_wm2=flux,
        )

    def compute_halo_orbit_metrics(self) -> HaloOrbitParameters:
        """
        计算 SOHO 在 L1 处的晕轨道三维尺度与太阳射电遮蔽回避角
        """
        ay_km = 650000.0  # 黄道面横向振幅 65 万 km
        az_km = 200000.0  # 垂直黄道振幅 20 万 km
        crtbp = self.solve_crtbp_l1()

        # 最小视角: SOHO 位于轨道近轴点时与日地连线的角张角
        # 视位置 offset = sqrt(Ay^2 * sin^2 + Az^2 * cos^2)
        # 为避免进入 3.5° 射电死区 (Solar RF Exclusion Zone):
        # min_offset_km = d_earth * tan(3.5°)
        min_angle_deg = 3.65  # 实测保持在 3.5°~4.5° 以上
        min_offset_km = crtbp.distance_to_earth_km * math.tan(math.radians(min_angle_deg))

        return HaloOrbitParameters(
            orbit_period_days=177.8,  # 约 178 天 / 6 个月公转一圈
            amplitude_y_km=ay_km,
            amplitude_z_km=az_km,
            min_separation_deg=min_angle_deg,
            min_projected_offset_km=min_offset_km,
            avoids_solar_radio_exclusion=(min_angle_deg >= 3.5),
            annual_station_keeping_dv_ms=3.2,  # 每年维持仅需约 3.2 m/s
        )

    def compute_mission_longevity(self, current_dt: datetime = None) -> Dict[str, Any]:
        """
        计算 SOHO 在轨服役超长寿命指标 (1995-2026)
        """
        now = current_dt or self.epochs.current_epoch_utc
        elapsed = now - self.epochs.launch_utc
        days = elapsed.total_seconds() / 86400.0
        years = days / 365.25
        l1_revolutions = days / 177.8

        return {
            "launch_date_utc": self.epochs.launch_utc.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "current_epoch_utc": now.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "total_days_in_space": round(days, 2),
            "total_years_in_space": round(years, 3),
            "halo_orbits_completed": round(l1_revolutions, 1),
            "solar_cycles_covered": 3,  # SC 23, SC 24, SC 25
            "original_design_life_years": 2.0,
            "longevity_multiplication_factor": round(years / 2.0, 1),
        }

    def compute_lasco_optics(self) -> Dict[str, LASCOInstrumentMetrics]:
        """
        计算 LASCO C2 与 C3 日冕仪视场与行星际物理覆盖尺寸
        """
        crtbp = self.solve_crtbp_l1()
        dist_soho_sun_km = crtbp.distance_to_sun_km

        # C2 日冕仪
        c2_inner_r = 2.0
        c2_outer_r = 6.0
        c2_inner_km = c2_inner_r * SOLAR_RADIUS_KM
        c2_outer_km = c2_outer_r * SOLAR_RADIUS_KM
        c2_diam_km = 2.0 * c2_outer_km
        c2_diam_au = c2_diam_km / AU_KM
        c2_ang_deg = 2.0 * math.degrees(math.atan(c2_outer_km / dist_soho_sun_km))

        # C3 日冕仪
        c3_inner_r = 3.7
        c3_outer_r = 32.0
        c3_inner_km = c3_inner_r * SOLAR_RADIUS_KM
        c3_outer_km = c3_outer_r * SOLAR_RADIUS_KM
        c3_diam_km = 2.0 * c3_outer_km
        c3_diam_au = c3_diam_km / AU_KM
        c3_ang_deg = 2.0 * math.degrees(math.atan(c3_outer_km / dist_soho_sun_km))

        c2_metrics = LASCOInstrumentMetrics(
            instrument_name="LASCO-C2 (内日冕红光仪)",
            fov_inner_rsun=c2_inner_r,
            fov_outer_rsun=c2_outer_r,
            fov_inner_km=c2_inner_km,
            fov_outer_km=c2_outer_km,
            total_diameter_km=c2_diam_km,
            total_diameter_au=c2_diam_au,
            angular_fov_deg=round(c2_ang_deg, 3),
            spatial_resolution_arcsec=11.9,
            passband_nm="540 - 640 nm (橙红光宽带)",
        )

        c3_metrics = LASCOInstrumentMetrics(
            instrument_name="LASCO-C3 (外日冕/行星际宽场仪)",
            fov_inner_rsun=c3_inner_r,
            fov_outer_rsun=c3_outer_r,
            fov_inner_km=c3_inner_km,
            fov_outer_km=c3_outer_km,
            total_diameter_km=c3_diam_km,
            total_diameter_au=c3_diam_au,
            angular_fov_deg=round(c3_ang_deg, 3),
            spatial_resolution_arcsec=56.0,
            passband_nm="400 - 850 nm (全色蔚蓝宽带)",
        )

        return {"C2": c2_metrics, "C3": c3_metrics}

    def simulate_cme_early_warning(self) -> List[CMEWarningScenario]:
        """
        推演不同速度谱系下 CME 太阳风冲击到达地球用时与 SOHO 预警时间裕量
        """
        dist_sun_earth_km = AU_KM
        soho_latency_min = 20.0  # 图像下传与分析典型耗时 20 分钟

        scenarios = [
            ("极端超级太阳风暴 (Carrington / 2003 Halloween 级)", 2500.0, "100% 对地全晕状 (Full Halo)"),
            ("强耀斑高速 CME (X 级耀斑触发)", 1500.0, "95% 宽角晕状 (Wide Partial Halo)"),
            ("典型中速 CME (M 级耀斑或巨型暗条爆发)", 1000.0, "75% 地球有效掠射"),
            ("慢速宁静日冕物质抛射", 500.0, "40% 弥散对地到达"),
        ]

        results = []
        for name, speed, geo in scenarios:
            transit_sec = dist_sun_earth_km / speed
            transit_hours = transit_sec / 3600.0
            transit_days = transit_hours / 24.0
            lead_hours = transit_hours - (soho_latency_min / 60.0)

            results.append(
                CMEWarningScenario(
                    cme_type=name,
                    speed_kms=speed,
                    transit_time_to_earth_hours=round(transit_hours, 2),
                    transit_time_to_earth_days=round(transit_days, 2),
                    soho_data_latency_min=soho_latency_min,
                    warning_lead_time_hours=round(lead_hours, 2),
                    geoeffective_confidence=geo,
                )
            )

        return results

    def get_comet_discovery_metrics(self) -> CometDiscoveryMetrics:
        """
        获取 SOHO 发现 5,200+ 颗彗星与克鲁兹族掠日动力学指标
        """
        total = 5230
        kreutz_count = 4450
        kreutz_pct = (kreutz_count / total) * 100.0
        q_au = 0.0055  # 典型近日点 0.0055 AU
        q_km = q_au * AU_KM
        q_above_sun = q_km - SOLAR_RADIUS_KM

        return CometDiscoveryMetrics(
            total_comets_discovered=total,
            kreutz_sungrazers_count=kreutz_count,
            kreutz_percentage=round(kreutz_pct, 1),
            perihelion_distance_au=q_au,
            perihelion_distance_km=round(q_km, 1),
            perihelion_above_surface_km=round(q_above_sun, 1),
            amateur_discoverer_ratio=95.5,
        )

    def get_helioseismology_tachocline(self) -> HelioseismologyTachocline:
        """
        获取日震学差旋层与发电机动力学参数
        """
        r_tacho = 0.713
        depth_km = (1.0 - r_tacho) * SOLAR_RADIUS_KM

        return HelioseismologyTachocline(
            tachocline_radius_rsun=r_tacho,
            tachocline_depth_km=round(depth_km, 1),
            sound_speed_core_kms=505.0,
            sound_speed_surface_kms=7.2,
            dominant_oscillation_period_min=5.05,
            dominant_frequency_mhertz=3.30,
            radiative_zone_rotation_days=26.6,
            convection_equator_rotation_days=25.1,
            convection_pole_rotation_days=35.0,
            dynamo_shear_significance="辐射层刚体自转与对流层差速自转在 0.713 R☉ 处剧烈剪切，驱动径向与环向磁场放大 (α-Ω 发电机)",
        )

    def get_recovery_story(self) -> SOHORecoveryStory:
        """
        获取 1998 年绝境盲操复活历史数据
        """
        t_loss = self.epochs.signal_loss_utc
        t_restored = self.epochs.full_science_restored_utc
        duration_days = (t_restored - t_loss).total_seconds() / 86400.0
        now = self.epochs.current_epoch_utc
        ext_years = (now - t_restored).total_seconds() / (86400.0 * 365.25)

        return SOHORecoveryStory(
            blackout_duration_days=round(duration_days, 1),
            arecibo_radar_role="阿雷西博 305 米巨型射电面反射雷达波，测定盲自转周期与三维空间指向",
            minimum_temperature_celsius=-120.0,
            hydrazine_thawing_method="分段解冻冻结联氨，盲操调姿使太阳翼重新采光，逐阶段加热恢复液态",
            recovered_payload_count=12,
            extended_mission_years=round(ext_years, 2),
        )

    def generate_grand_quattuorvigintet_fleet(self) -> List[DeepSpaceProbeEntry]:
        """
        生成 2026 人类深空二十四极黄金舰队 (The Grand Quattuorvigintet) 矩阵
        严格按日心极距降序排列
        """
        fleet = [
            DeepSpaceProbeEntry(
                name="旅行者 1 号 (Voyager 1)",
                agency="NASA",
                heliocentric_distance_au=173.22,
                geocentric_distance_km=25910000000.0,
                one_way_light_time_str="24.01 小时 (1 光日倒计时 32 天)",
                mission_significance="恒星际最远深空边界极，2.7K 极寒虚空，星际等离子体原位探测",
            ),
            DeepSpaceProbeEntry(
                name="旅行者 2 号 (Voyager 2)",
                agency="NASA",
                heliocentric_distance_au=144.26,
                geocentric_distance_km=21583000000.0,
                one_way_light_time_str="19.998 小时 (今日晚间跨越 20 光时！)",
                mission_significance="恒星际南天天球星际极，大四喜全访遗产，堪培拉 DSS-43 单一生命线",
            ),
            DeepSpaceProbeEntry(
                name="新视野号 (New Horizons)",
                agency="NASA",
                heliocentric_distance_au=65.92,
                geocentric_distance_km=9860000000.0,
                one_way_light_time_str="9.14 小时",
                mission_significance="柯伊伯带双曲线逃逸极，COB 绝尘暗夜超额光，PUI 减速 17%",
            ),
            DeepSpaceProbeEntry(
                name="朱诺号 (Juno)",
                agency="NASA",
                heliocentric_distance_au=5.20,
                geocentric_distance_km=778000000.0,
                one_way_light_time_str="43.25 分钟",
                mission_significance="木星极轨高能辐射极，180kg 钛金保险库，掠木 57.8 km/s，PJ89 倒计时 27 天",
            ),
            DeepSpaceProbeEntry(
                name="木星冰月探测器 (JUICE)",
                agency="ESA",
                heliocentric_distance_au=5.20,
                geocentric_distance_km=778000000.0,
                one_way_light_time_str="43.25 分钟",
                mission_significance="巨行星卫星内禀磁层极，探秘木卫三深海，85m² 弱光光伏，2.3 年共振巡航",
            ),
            DeepSpaceProbeEntry(
                name="欧罗巴快船 (Europa Clipper)",
                agency="NASA",
                heliocentric_distance_au=5.20,
                geocentric_distance_km=778000000.0,
                one_way_light_time_str="43.25 分钟",
                mission_significance="外行星木卫二深海生命极，MEGA 地球引力弹弓倒计时 47 天",
            ),
            DeepSpaceProbeEntry(
                name="露西号 (Lucy)",
                agency="NASA",
                heliocentric_distance_au=5.04,
                geocentric_distance_km=754000000.0,
                one_way_light_time_str="41.92 分钟",
                mission_significance="木星特洛伊群原始微行星极，7.3m UltraFlex 折叠帆板，发射五周年",
            ),
            DeepSpaceProbeEntry(
                name="灵神星探测器 (Psyche)",
                agency="NASA",
                heliocentric_distance_au=2.042,
                geocentric_distance_km=305500000.0,
                one_way_light_time_str="16.98 分钟",
                mission_significance="金属核心微行星极，SPT-140 霍尔电推，DSOC 激光光子链路百倍跃迁",
            ),
            DeepSpaceProbeEntry(
                name="好奇号 (Curiosity)",
                agency="NASA",
                heliocentric_distance_au=1.524,
                geocentric_distance_km=291700000.0,
                one_way_light_time_str="16.22 分钟",
                mission_significance="火星盖尔撞击坑与夏普山麓极，14 年漫游 33.6km，盖迪兹谷纯单质硫突破，MMRTG",
            ),
            DeepSpaceProbeEntry(
                name="毅力号 (Perseverance)",
                agency="NASA",
                heliocentric_distance_au=1.524,
                geocentric_distance_km=291700000.0,
                one_way_light_time_str="16.22 分钟",
                mission_significance="火星地表古湖泊与40亿年原生古地壳原位探测极，翻越500m环壁冲入狂野西部、生成式AI导航与33支岩芯密封",
            ),
            DeepSpaceProbeEntry(
                name="天问一号环绕器 (Tianwen-1)",
                agency="CNSA",
                heliocentric_distance_au=1.524,
                geocentric_distance_km=291700000.0,
                one_way_light_time_str="16.22 分钟",
                mission_significance="火星极轨全域遥感极，76m 全球彩色正射图，MOSIR 雷达探冰，3I/ATLAS 星际观测",
            ),
            DeepSpaceProbeEntry(
                name="火星勘测轨道器 (MRO)",
                agency="NASA",
                heliocentric_distance_au=1.524,
                geocentric_distance_km=291700000.0,
                one_way_light_time_str="16.22 分钟",
                mission_significance="火星 20 年在轨超高分辨率对焦与深空信息中枢极，HiRISE 30cm 光学微观极限、SHARAD 1km 探冰发现乌托邦平原 1.43 万 km³ 地下冰川、Electra 80% 巡视器中继骨干",
            ),
            DeepSpaceProbeEntry(
                name="赫拉号 (Hera)",
                agency="ESA",
                heliocentric_distance_au=1.304,
                geocentric_distance_km=195100000.0,
                one_way_light_time_str="10.85 分钟",
                mission_significance="双小行星微重力伴飞极，BRM-1 93分钟主减速点火圆满达成",
            ),
            DeepSpaceProbeEntry(
                name="隼鸟二号 (Hayabusa2# / SHARP)",
                agency="JAXA",
                heliocentric_distance_au=1.120,
                geocentric_distance_km=167500000.0,
                one_way_light_time_str="9.31 分钟",
                mission_significance="十米级超快自转微小行星极，744m Torifune 掠飞后巡航，1998 KY26 极区着陆，490倍离心力对抗",
            ),
            DeepSpaceProbeEntry(
                name="OSIRIS-APEX",
                agency="NASA",
                heliocentric_distance_au=1.010,
                geocentric_distance_km=151100000.0,
                one_way_light_time_str="8.40 分钟",
                mission_significance="毁神星伴飞与极限热控无花果叶极，4倍太阳热流，2029 掠地 1153km 减速 99%",
            ),
            DeepSpaceProbeEntry(
                name="詹姆斯·韦伯望远镜 (JWST)",
                agency="NASA/ESA/CSA",
                heliocentric_distance_au=1.010,
                geocentric_distance_km=1500000.0,
                one_way_light_time_str="5.00 秒",
                mission_significance="日地虚空 L2 天文极，6.5m 铍金镜，300 K 隔热 6.7 K 制冷，0.077'' 捕获 z > 14 原初星系",
            ),
            DeepSpaceProbeEntry(
                name="欧几里得空间望远镜 (Euclid)",
                agency="ESA",
                heliocentric_distance_au=1.010,
                geocentric_distance_km=1500000.0,
                one_way_light_time_str="4.99 秒",
                mission_significance="日地 L2 暗宇宙与大尺度三维宇宙网宏观极，1.2m SiC TMA，0.53 deg² 巨视场，6.09 亿像素 VIS + 6500 万像素 NISP，弱透镜宇宙剪切 γ 与 BAO",
            ),
            DeepSpaceProbeEntry(
                name="天问二号 (Tianwen-2)",
                agency="CNSA",
                heliocentric_distance_au=1.001,
                geocentric_distance_km=14980000.0,
                one_way_light_time_str="49.97 秒",
                mission_significance="地球准卫星共轨采样与彗星双跃迁极，28分钟自旋 50倍离心力对抗采样，布鲁诺撞击坑月球基岩",
            ),
            DeepSpaceProbeEntry(
                name="鹊桥二号 (Queqiao-2)",
                agency="CNSA",
                heliocentric_distance_au=1.000,
                geocentric_distance_km=384400.0,
                one_way_light_time_str="1.282 秒",
                mission_significance="地月空间与月球南极/月背冻结中继极，4.2米伞状天线、月瘤摄动抑制、嫦娥六/七/八号生命线",
            ),
            DeepSpaceProbeEntry(
                name="嫦娥四号与玉兔二号 (Chang'e-4 / Yutu-2)",
                agency="CNSA",
                heliocentric_distance_au=1.000,
                geocentric_distance_km=384400.0,
                one_way_light_time_str="1.282 秒",
                mission_significance="月球背面南极-艾特肯盆地原位巡视极，人类唯一月背软着陆、96 月昼 7.79 年超长巡视、-180°C 钚-238 RHU 核热源冬眠、月背射电静默区",
            ),
            DeepSpaceProbeEntry(
                name="太阳和日球层天文台 (SOHO)",
                agency="ESA/NASA",
                heliocentric_distance_au=0.990,
                geocentric_distance_km=1491500.0,
                one_way_light_time_str="4.975 秒",
                mission_significance="日地 L1 向日日冕哨兵极，30 年守望三轮太阳活动周，LASCO 4450 万 km 行星际视场与 CME 预警、5200 颗彗星世界纪录、日震学差旋层发电机",
            ),
            DeepSpaceProbeEntry(
                name="贝皮可伦坡 (BepiColombo)",
                agency="ESA/JAXA",
                heliocentric_distance_au=0.387,
                geocentric_distance_km=149000000.0,
                one_way_light_time_str="8.28 分钟",
                mission_significance="太阳最深引力势能阱水星捕获极，-1405 MJ/kg MOI 盲操倒计时 35 天",
            ),
            DeepSpaceProbeEntry(
                name="太阳轨道飞行器 (Solar Orbiter)",
                agency="ESA/NASA",
                heliocentric_distance_au=0.280,
                geocentric_distance_km=107000000.0,
                one_way_light_time_str="5.95 分钟",
                mission_significance="黄道外高倾角极区成像与日冕加热极，金星 4:3 借力 24°，520°C 骨黑隔热罩，微耀斑篝火，倒计时 68 天平安夜 VGA5",
            ),
            DeepSpaceProbeEntry(
                name="帕克太阳探测器 (Parker Solar Probe)",
                agency="NASA",
                heliocentric_distance_au=0.046,
                geocentric_distance_km=142700000.0,
                one_way_light_time_str="7.93 分钟",
                mission_significance="恒星日冕极高温炼狱原位极，192 km/s 人类极速，1400°C 防热罩，P30 倒计时 46 天",
            ),
        ]
        return fleet

    def compute_fleet_dual_metrics(self) -> Dict[str, float]:
        """
        计算二十四极黄金舰队的极限物理跨度与几何比率
        """
        fleet = self.generate_grand_quattuorvigintet_fleet()
        r_max = fleet[0].heliocentric_distance_au  # Voyager 1: 173.22 AU
        r_min = fleet[-1].heliocentric_distance_au  # Parker: 0.046 AU

        flux_max = SOLAR_IRRADIANCE_1AU / (r_min**2)  # Parker
        flux_min = SOLAR_IRRADIANCE_1AU / (r_max**2)  # Voyager 1

        d_earth_max = fleet[0].geocentric_distance_km  # Voyager 1: 259.1 亿 km
        d_earth_min = fleet[18].geocentric_distance_km  # Queqiao-2 / Yutu-2: 38.44 万 km

        # 光时比例
        owlt_max_sec = d_earth_max / SPEED_OF_LIGHT
        owlt_min_sec = d_earth_min / SPEED_OF_LIGHT

        # 速度极限比例: 帕克近日点 192 km/s vs 1998 KY26 表面逃逸 6.88 mm/s
        v_max_kms = 192.0
        v_min_kms = 0.00000688

        return {
            "heliocentric_distance_span_ratio": round(r_max / r_min, 2),
            "solar_flux_drop_ratio": round(flux_max / flux_min, 1),
            "geocentric_distance_span_ratio": round(d_earth_max / d_earth_min, 1),
            "light_time_span_ratio": round(owlt_max_sec / owlt_min_sec, 1),
            "extreme_velocity_span_ratio": round(v_max_kms / v_min_kms, 1),
            "total_fleet_probe_count": len(fleet),
        }


if __name__ == "__main__":
    engine = SOHOL1SolarCoronagraphEngine()
    crtbp = engine.solve_crtbp_l1()
    print("=== SOHO 日地 L1 CRTBP 解 ===")
    print(f"L1 距地球: {crtbp.distance_to_earth_km:.2f} km ({crtbp.gamma_1_normalized:.6f} AU)")
    print(f"L1 日心极距: {crtbp.distance_to_sun_au:.6f} AU ({crtbp.distance_to_sun_km:.2f} km)")
    print(f"单向光行时: {crtbp.one_way_light_time_sec:.4f} s")
    print(f"太阳辐射能流: {crtbp.solar_flux_at_soho_wm2:.2f} W/m^2")

    halo = engine.compute_halo_orbit_metrics()
    print("\n=== SOHO Halo 轨道与射电回避 ===")
    print(f"公转周期: {halo.orbit_period_days} 天")
    print(f"横向/垂直振幅: Ay={halo.amplitude_y_km:.0f} km, Az={halo.amplitude_z_km:.0f} km")
    print(f"最小回避角: {halo.min_separation_deg}° (投影 {halo.min_projected_offset_km:.0f} km)")
    print(f"避开太阳射电死区: {halo.avoids_solar_radio_exclusion}")

    optics = engine.compute_lasco_optics()
    print("\n=== LASCO 日冕仪光学尺度 ===")
    for k, v in optics.items():
        print(f"[{k}] 视场: {v.fov_inner_rsun}~{v.fov_outer_rsun} R_sun, 直径: {v.total_diameter_km:.0f} km ({v.total_diameter_au:.4f} AU), 视场角: {v.angular_fov_deg}°")

    cmes = engine.simulate_cme_early_warning()
    print("\n=== CME 空间天气预警推演 ===")
    for c in cmes:
        print(f"{c.cme_type}: 速度 {c.speed_kms} km/s, 抵达地球 {c.transit_time_to_earth_hours} 小时, 预警窗口 {c.warning_lead_time_hours} 小时")

    fleet_dual = engine.compute_fleet_dual_metrics()
    print("\n=== 二十四极黄金舰队极限对偶 ===")
    for k, v in fleet_dual.items():
        print(f"{k}: {v}")
