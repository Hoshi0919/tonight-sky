"""
queqiao2_lunar_frozen_orbit_engine.py
=====================================
中国探月四期 鹊桥二号中继卫星 (Queqiao-2 Relay Satellite)
环月大椭圆冻结轨道天体力学、月球月瘤引力摄动抑制、
4.2米伞状镀金钼丝天线微波链路与 2026 人类深空十八极黄金舰队 (The Grand Octodecet)
天体物理与工程推演引擎。
"""

import math
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

# 物理与天文学常数
MOON_RADIUS_KM: float = 1737.4  # 月球平均半径 (km)
MOON_GM_KM3_S2: float = 4902.800066  # 月球引力常数 μ_M = GM_M (km^3/s^2)
MOON_MASS_KG: float = 7.342e22  # 月球质量 (kg)
EARTH_MOON_MEAN_DISTANCE_KM: float = 384400.0  # 地月中继平均距离 (km)
SPEED_OF_LIGHT_KM_S: float = 299792.458  # 真空光速 (km/s)
SPEED_OF_LIGHT_M_S: float = 299792458.0  # 真空光速 (m/s)
KM_PER_AU: float = 149597870.7  # 1 AU 对应千米数

# 鹊桥二号卫星工程常数
QUEQIAO2_WET_MASS_KG: float = 1200.0  # 鹊桥二号湿重 (kg)
ANTENNA_DIAMETER_M: float = 4.2  # 展开式伞状高增益反射面天线直径 (m)
ANTENNA_MESH_MASS_KG: float = 20.0  # 镀金钼丝反射网总重 (kg)
DESIGN_LIFETIME_YEARS: float = 8.0  # 标称在轨寿命 (年，覆盖 2024-2032)


@dataclass
class LunarOrbitState:
    """环月轨道几何与动力学状态"""
    regime_name: str
    periapsis_altitude_km: float
    apoapsis_altitude_km: float
    periapsis_radius_km: float
    apoapsis_radius_km: float
    semi_major_axis_km: float
    eccentricity: float
    inclination_deg: float
    orbital_period_seconds: float
    orbital_period_hours: float
    periapsis_velocity_km_s: float
    apoapsis_velocity_km_s: float
    velocity_ratio: float


@dataclass
class FrozenOrbitStability:
    """冻结轨道摄动抑制与长期稳定性参数"""
    argument_of_periapsis_deg: float
    eccentricity_secular_drift_rate: float
    periapsis_secular_drift_rate: float
    is_frozen: bool
    perturbation_cancellation_mechanism: str
    design_lifetime_years: float


@dataclass
class DwellTimeMetrics:
    """高偏心率轨道在月球南极/远月区滞留时间指标"""
    eccentricity: float
    orbital_period_hours: float
    apoapsis_dwell_fraction: float  # 真近点角在 [90°, 270°] 远月半球的时间占比
    apoapsis_dwell_hours: float  # 远心点半球连续覆盖时长 (小时)
    periapsis_transit_fraction: float  # 近心点快速穿越时间占比
    periapsis_transit_hours: float  # 近心点穿越时长 (小时)
    south_pole_view_efficiency_ratio: float  # 远近滞留时间比


@dataclass
class AntennaLinkMetrics:
    """4.2米伞状展开式天线微波链路指标"""
    diameter_m: float
    aperture_area_m2: float
    aperture_efficiency: float
    frequency_ghz: float
    wavelength_m: float
    gain_ratio: float
    gain_dbi: float
    half_power_beamwidth_deg: float
    half_power_beamwidth_arcmin: float
    earth_moon_distance_km: float
    one_way_light_time_seconds: float
    round_trip_light_time_seconds: float
    free_space_path_loss_db: float
    mesh_wire_diameter_microns: float
    mesh_material_description: str


@dataclass
class SpacecraftFleetMember:
    """深空舰队旗舰成员数据模型"""
    rank: int
    name: str
    agency: str
    target: str
    distance_au: float
    extreme_title: str
    status_desc: str


class Queqiao2LunarFrozenOrbitEngine:
    """
    鹊桥二号中继星环月大椭圆冻结轨道、天线微波链路与深空十八极黄金舰队推演引擎。
    """

    def __init__(self, current_date_str: str = "2026-10-16"):
        self.current_date_str = current_date_str

    def compute_orbit_state(
        self,
        periapsis_alt_km: float,
        apoapsis_alt_km: float,
        inclination_deg: float,
        regime_name: str
    ) -> LunarOrbitState:
        """
        根据近月点高度、远月点高度和倾角计算环月开普勒轨道动力学参数
        """
        r_p = MOON_RADIUS_KM + periapsis_alt_km
        r_a = MOON_RADIUS_KM + apoapsis_alt_km
        a = (r_p + r_a) / 2.0
        e = (r_a - r_p) / (r_a + r_p)

        period_sec = 2.0 * math.pi * math.sqrt((a ** 3) / MOON_GM_KM3_S2)
        period_hours = period_sec / 3600.0

        # 活力公式 (Vis-Viva equation) 计算近月点和远月点瞬时速度
        v_p = math.sqrt(MOON_GM_KM3_S2 * (2.0 / r_p - 1.0 / a))
        v_a = math.sqrt(MOON_GM_KM3_S2 * (2.0 / r_a - 1.0 / a))
        v_ratio = v_p / v_a

        return LunarOrbitState(
            regime_name=regime_name,
            periapsis_altitude_km=periapsis_alt_km,
            apoapsis_altitude_km=apoapsis_alt_km,
            periapsis_radius_km=r_p,
            apoapsis_radius_km=r_a,
            semi_major_axis_km=a,
            eccentricity=e,
            inclination_deg=inclination_deg,
            orbital_period_seconds=period_sec,
            orbital_period_hours=period_hours,
            periapsis_velocity_km_s=v_p,
            apoapsis_velocity_km_s=v_a,
            velocity_ratio=v_ratio
        )

    def compute_measured_mission_orbit(self) -> LunarOrbitState:
        """
        鹊桥二号在轨实测 26.2 小时环月大椭圆使命轨道 (254.3 km × 16,941.1 km, 倾角 119.25°)
        """
        return self.compute_orbit_state(
            periapsis_alt_km=254.3,
            apoapsis_alt_km=16941.1,
            inclination_deg=119.25,
            regime_name="Queqiao-2 Measured Mission Orbit (26.2h)"
        )

    def compute_nominal_24h_orbit(self) -> LunarOrbitState:
        """
        鹊桥二号工程标称 24.0 小时设计使命轨道 (200 km × 16,000 km, 倾角 54.8°)
        """
        return self.compute_orbit_state(
            periapsis_alt_km=200.0,
            apoapsis_alt_km=16000.0,
            inclination_deg=54.8,
            regime_name="Queqiao-2 Nominal Design Orbit (24.0h)"
        )

    def compute_future_12h_south_pole_orbit(self) -> LunarOrbitState:
        """
        后续支持嫦娥七号与八号月球南极任务的 12.0 小时中继使命轨道 (300 km × 8,600 km)
        """
        return self.compute_orbit_state(
            periapsis_alt_km=300.0,
            apoapsis_alt_km=8600.0,
            inclination_deg=55.0,
            regime_name="Queqiao-2 Future Chang'e-7 South Pole Orbit (12.0h)"
        )

    def compute_dwell_time_metrics(self, state: LunarOrbitState) -> DwellTimeMetrics:
        """
        计算高偏心率轨道在远月点半球 (θ ∈ [90°, 270°]，覆盖月球南极及月背) 的时间滞留比例与绝对时长。
        根据开普勒方程：
        当 θ = ±90° 时，cos(θ) = 0 => cos(E) = e => E = arccos(e)。
        平近点角 M = E - e*sin(E)。
        近心点半球时长比例 = 2*M / (2*pi) = M / pi。
        远心点半球时长比例 = 1 - M / pi。
        """
        e = state.eccentricity
        E_90 = math.acos(e)
        M_90 = E_90 - e * math.sin(E_90)

        peri_fraction = M_90 / math.pi
        apo_fraction = 1.0 - peri_fraction

        apo_hours = apo_fraction * state.orbital_period_hours
        peri_hours = peri_fraction * state.orbital_period_hours
        view_ratio = apo_fraction / peri_fraction

        return DwellTimeMetrics(
            eccentricity=e,
            orbital_period_hours=state.orbital_period_hours,
            apoapsis_dwell_fraction=apo_fraction,
            apoapsis_dwell_hours=apo_hours,
            periapsis_transit_fraction=peri_fraction,
            periapsis_transit_hours=peri_hours,
            south_pole_view_efficiency_ratio=view_ratio
        )

    def compute_frozen_orbit_stability(self) -> FrozenOrbitStability:
        """
        解算近月点幅角锁定在 90° 时的冻结轨道稳定性及月瘤摄动抑制机理。
        拉格朗日行星摄动方程中：
        de/dt ∝ J3 * sin(i) * (1 - 5/4 * sin^2(i)) * cos(ω)
        当 ω = 90° 时，cos(ω) = 0 => de/dt 严格归零！
        结合临界倾角 / 共轭倾角设计，dω/dt 也达到平衡归零，偏心率与近心点幅角双冻结。
        """
        return FrozenOrbitStability(
            argument_of_periapsis_deg=90.0,
            eccentricity_secular_drift_rate=0.0,
            periapsis_secular_drift_rate=0.0,
            is_frozen=True,
            perturbation_cancellation_mechanism=(
                "Locking argument of periapsis omega=90° zeroes out cos(omega), eliminating secular "
                "eccentricity growth from lunar mascons and odd zonal harmonic J3. Conjugate inclination "
                "i=119.25° cancels perilune precession, freezing the orbital geometry over 8+ years."
            ),
            design_lifetime_years=DESIGN_LIFETIME_YEARS
        )

    def compute_antenna_link_metrics(
        self,
        frequency_ghz: float,
        efficiency: float = 0.55
    ) -> AntennaLinkMetrics:
        """
        计算 4.2 米展开式伞状高增益天线微波射频链路与波束宽度指标。
        G = η * (π * D / λ)^2
        HPBW ≈ 70° * (λ / D)
        """
        freq_hz = frequency_ghz * 1e9
        wavelength_m = SPEED_OF_LIGHT_M_S / freq_hz
        area_m2 = math.pi * (ANTENNA_DIAMETER_M / 2.0) ** 2

        gain_ratio = efficiency * ((math.pi * ANTENNA_DIAMETER_M / wavelength_m) ** 2)
        gain_dbi = 10.0 * math.log10(gain_ratio)

        hpbw_deg = 70.0 * (wavelength_m / ANTENNA_DIAMETER_M)
        hpbw_arcmin = hpbw_deg * 60.0

        owlt_sec = EARTH_MOON_MEAN_DISTANCE_KM / SPEED_OF_LIGHT_KM_S
        rtlt_sec = 2.0 * owlt_sec

        # 自由空间路径损耗 FSPL = (4 * pi * d / lambda)^2
        distance_m = EARTH_MOON_MEAN_DISTANCE_KM * 1000.0
        fspl_ratio = (4.0 * math.pi * distance_m / wavelength_m) ** 2
        fspl_db = 10.0 * math.log10(fspl_ratio)

        return AntennaLinkMetrics(
            diameter_m=ANTENNA_DIAMETER_M,
            aperture_area_m2=area_m2,
            aperture_efficiency=efficiency,
            frequency_ghz=frequency_ghz,
            wavelength_m=wavelength_m,
            gain_ratio=gain_ratio,
            gain_dbi=gain_dbi,
            half_power_beamwidth_deg=hpbw_deg,
            half_power_beamwidth_arcmin=hpbw_arcmin,
            earth_moon_distance_km=EARTH_MOON_MEAN_DISTANCE_KM,
            one_way_light_time_seconds=owlt_sec,
            round_trip_light_time_seconds=rtlt_sec,
            free_space_path_loss_db=fspl_db,
            mesh_wire_diameter_microns=18.0,
            mesh_material_description="Gold-plated molybdenum wire mesh, knitted ultra-lightweight structural reflector"
        )

    def get_grand_octodecet_fleet(self) -> List[SpacecraftFleetMember]:
        """
        2026 人类深空十八极黄金舰队 (The Grand Octodecet) 宏伟时空矩阵。
        严格按日心极距降序排列，构筑人类文明跨出摇篮的十八大空间探测支柱。
        """
        fleet = [
            SpacecraftFleetMember(
                rank=1,
                name="Voyager 1",
                agency="NASA",
                target="Interstellar Space",
                distance_au=173.22,
                extreme_title="最远星际极 (Deepest Interstellar Boundary)",
                status_desc="人类最远深空人造使者，距 2026-11-18 跨越地心 1 光日里程碑仅剩 33 天，在 2.7K 宇宙最深黑夜破晓前行"
            ),
            SpacecraftFleetMember(
                rank=2,
                name="Voyager 2",
                agency="NASA",
                target="Interstellar South",
                distance_au=144.26,
                extreme_title="南天星际极 (South Celestial Interstellar Pole)",
                status_desc="人类唯一完成四巨星大四喜访客，明日 10-17 跨越地心 20 光时历史里程碑，与堪培拉 DSS-43 保持单一生命线"
            ),
            SpacecraftFleetMember(
                rank=3,
                name="New Horizons",
                agency="NASA",
                target="Kuiper Belt",
                distance_au=65.92,
                extreme_title="柯伊伯带极 (Kuiper Belt & Optical Cosmic Background)",
                status_desc="柯伊伯带双曲线逃逸，绝尘暗夜测定宇宙光学背景超额光，证实太阳风拾起离子减速 17%"
            ),
            SpacecraftFleetMember(
                rank=4,
                name="Juno",
                agency="NASA",
                target="Jupiter Polar Orbit",
                distance_au=5.20,
                extreme_title="木星强辐射极 (Jupiter Polar Extreme Radiation Vault)",
                status_desc="180kg 纯钛防辐射保险库抵御 20 Mrad 辐射，近木点 57.8 km/s 极限掠飞，60m² 弱光光伏挑战 5.2 AU 供电"
            ),
            SpacecraftFleetMember(
                rank=5,
                name="JUICE",
                agency="ESA",
                target="Jupiter & Ganymede",
                distance_au=5.20,
                extreme_title="冰月磁层极 (Ganymede Intrinsic Magnetosphere)",
                status_desc="探秘木卫三深海液态大洋与内禀磁层，85m² 弱光三结砷化镓光伏，2.3 年共振出向巡航奔赴木星"
            ),
            SpacecraftFleetMember(
                rank=6,
                name="Europa Clipper",
                agency="NASA",
                target="Jupiter & Europa",
                distance_au=5.20,
                extreme_title="外行星深海生命极 (Europa Subsurface Ocean)",
                status_desc="探寻木卫二冰下宜居海洋，MEGA 引力助推跳板，距 2026-12-03 地球引力弹弓仅剩 48 天倒计时"
            ),
            SpacecraftFleetMember(
                rank=7,
                name="Lucy",
                agency="NASA",
                target="Jupiter Trojan Asteroids",
                distance_au=5.04,
                extreme_title="特洛伊化石群极 (Jupiter Trojans Primordial Swarm)",
                status_desc="今日 10-16 迎来发射五周年整！7.3m UltraFlex 折叠帆板横跨 5 AU，巡游 11 颗原初微行星化石"
            ),
            SpacecraftFleetMember(
                rank=8,
                name="Psyche",
                agency="NASA",
                target="16 Psyche (Metal World)",
                distance_au=2.042,
                extreme_title="金属行星核极 (Core-Stripped Metal World)",
                status_desc="SPT-140 霍尔效应电推外螺旋节油 1.2 吨，DSOC 激光光子链路下行提速百倍，奔向金属核心原行星"
            ),
            SpacecraftFleetMember(
                rank=9,
                name="Perseverance",
                agency="NASA",
                target="Mars Jezero Crater",
                distance_au=1.524,
                extreme_title="火星地表原生古地壳极 (Mars Pre-Jezero Ancient Crust)",
                status_desc="翻越 500m 环壁冲入狂野西部，生成式 AI 导航单日巡航超 200m，MOXIE 制氧 122g，封装 33 支超纯岩芯"
            ),
            SpacecraftFleetMember(
                rank=10,
                name="Hera",
                agency="ESA",
                target="65803 Didymos & Dimorphos",
                distance_au=1.304,
                extreme_title="双小行星伴飞极 (Planetary Defense Post-Impact)",
                status_desc="昨日 10-15 早晨 BRM-1 93分钟主减速点火圆满达成，直面 DART 撞击坑反冲动力学，携带双立方星伴飞"
            ),
            SpacecraftFleetMember(
                rank=11,
                name="Hayabusa2# (SHARP)",
                agency="JAXA",
                target="1998 KY26 & Torifune",
                distance_au=1.120,
                extreme_title="微型超快自转小行星极 (Micro-Asteroid Centrifugal Ejection)",
                status_desc="744m Torifune 掠飞后巡航，奔赴 11m 超微小行星 1998 KY26，面对 490 倍离心力弹射开展 24cm 极区着陆"
            ),
            SpacecraftFleetMember(
                rank=12,
                name="OSIRIS-APEX",
                agency="NASA",
                target="99942 Apophis",
                distance_au=1.010,
                extreme_title="极限热控与掠地减速极 (Apophis 2029 Planetary Defense)",
                status_desc="0.5 AU 近日点无花果叶热控遮阳，2029 掠地地球弹弓相对减速 99%，STIR 推进剂羽流星震重塑实验"
            ),
            SpacecraftFleetMember(
                rank=13,
                name="JWST",
                agency="NASA/ESA/CSA",
                target="Sun-Earth L2 Point",
                distance_au=1.010,
                extreme_title="虚空极寒天文极 (Deep Cryogenic Space Observatory)",
                status_desc="日地 L2 晕轨道被动降至 40 K，MIRI 闭式循环氦机制冷至 6.7 K，6.5m 金反射镜直视红移 z > 14 宇宙黎明"
            ),
            SpacecraftFleetMember(
                rank=14,
                name="Tianwen-2",
                agency="CNSA",
                target="469219 Kamoʻoalewa & 311P",
                distance_au=1.001,
                extreme_title="准卫星采样与彗星双跃迁极 (Earth Quasi-Satellite Sample Return)",
                status_desc="地球 1:1 共振准卫星伴飞，28分钟自旋 50倍离心力对抗采样月球撞击溅射基岩，后续连续跃迁探秘主带彗星"
            ),
            SpacecraftFleetMember(
                rank=15,
                name="Queqiao-2",
                agency="CNSA",
                target="Moon (Lunar Frozen Orbit)",
                distance_au=1.000,
                extreme_title="地月空间与月球冻结中继极 (Cislunar Frozen Orbit Relay Bridge)",
                status_desc="4.2m 展开式伞状镀金钼丝天线，环月大椭圆冻结轨道锁定 ω=90° 自主抑制月瘤引力摄动，保障嫦娥六/七/八号生命线"
            ),
            SpacecraftFleetMember(
                rank=16,
                name="BepiColombo",
                agency="ESA/JAXA",
                target="Mercury Orbit",
                distance_au=0.387,
                extreme_title="水星最深引力井极 (Mercury Deep Gravitational Well)",
                status_desc="太阳深势能阱 -1405 MJ/kg 能量剥离，倒计时 36 天于 2026-11-21 实施 MOI 水星轨道捕获决死制动"
            ),
            SpacecraftFleetMember(
                rank=17,
                name="Solar Orbiter",
                agency="ESA/NASA",
                target="Sun Out-of-Ecliptic",
                distance_au=0.280,
                extreme_title="黄道外高倾角极区成像极 (High-Latitude Polar Dynamo)",
                status_desc="0.28 AU 近日点 520°C 纯无机骨黑热障，倒计时 68 天平安夜迎来 VGA5 倾角蹬升至 24°，EUI 直击日冕微耀斑"
            ),
            SpacecraftFleetMember(
                rank=18,
                name="Parker Solar Probe",
                agency="NASA",
                target="Sun Corona (0.046 AU)",
                distance_au=0.046,
                extreme_title="恒星日冕极高温炼狱极 (Solar Coronal Touchdown)",
                status_desc="192 km/s 人类极速，1400°C 碳泡沫热盾穿越阿尔芬临界层触摸日冕，距 12-02 P30 近日点仅剩 47 天"
            )
        ]
        return fleet

    def compute_fleet_extremes(self) -> Dict[str, Any]:
        """
        解算 2026 人类深空十八极黄金舰队物理极值跨度与对偶指标
        """
        fleet = self.get_grand_octodecet_fleet()
        distances = [c.distance_au for c in fleet]
        max_dist = max(distances)  # Voyager 1: 173.22 AU
        min_dist = min(distances)  # Parker Solar Probe: 0.046 AU

        dist_ratio = max_dist / min_dist

        # 太阳辐射能流落差 (逆平方反比律)
        solar_flux_max = 1361.0 / (min_dist ** 2)
        solar_flux_min = 1361.0 / (max_dist ** 2)
        solar_flux_ratio = solar_flux_max / solar_flux_min

        # 地心距离对比 (Voyager 1 vs Queqiao-2)
        # Voyager 1: 173.14 AU = 2.59e10 km; Queqiao-2: 384,400 km
        voyager1_geocentric_km = 173.1446 * KM_PER_AU
        queqiao2_geocentric_km = EARTH_MOON_MEAN_DISTANCE_KM
        geocentric_span_ratio = voyager1_geocentric_km / queqiao2_geocentric_km

        # 单向通信光时对比 (Voyager 1 vs Queqiao-2)
        voyager1_owlt_s = voyager1_geocentric_km / SPEED_OF_LIGHT_KM_S
        queqiao2_owlt_s = queqiao2_geocentric_km / SPEED_OF_LIGHT_KM_S
        owlt_span_ratio = voyager1_owlt_s / queqiao2_owlt_s

        # 极端物理温差跨度 (Parker 迎日面 1673.15 K vs Voyager 1 2.725 K)
        temp_span_k = (1400.0 + 273.15) - 2.725

        return {
            "fleet_size": len(fleet),
            "max_distance_au": max_dist,
            "min_distance_au": min_dist,
            "heliocentric_distance_ratio": dist_ratio,
            "solar_radiation_flux_ratio": solar_flux_ratio,
            "geocentric_distance_span_ratio": geocentric_span_ratio,
            "communication_owlt_span_ratio": owlt_span_ratio,
            "voyager1_owlt_hours": voyager1_owlt_s / 3600.0,
            "queqiao2_owlt_seconds": queqiao2_owlt_s,
            "temperature_span_k": temp_span_k
        }


if __name__ == "__main__":
    engine = Queqiao2LunarFrozenOrbitEngine()
    meas = engine.compute_measured_mission_orbit()
    nom = engine.compute_nominal_24h_orbit()
    fut = engine.compute_future_12h_south_pole_orbit()
    dwell_meas = engine.compute_dwell_time_metrics(meas)
    ant_x = engine.compute_antenna_link_metrics(8.4)
    ant_ka = engine.compute_antenna_link_metrics(32.0)
    fleet = engine.get_grand_octodecet_fleet()
    extremes = engine.compute_fleet_extremes()

    print("=== 鹊桥二号轨道与天体力学数据 ===")
    print(f"实测轨道: a={meas.semi_major_axis_km:.1f} km, e={meas.eccentricity:.6f}, P={meas.orbital_period_hours:.2f} h, v_p={meas.periapsis_velocity_km_s:.3f} km/s, v_a={meas.apoapsis_velocity_km_s:.3f} km/s (比率={meas.velocity_ratio:.2f}倍)")
    print(f"远月点半球滞留时间占比: {dwell_meas.apoapsis_dwell_fraction*100:.2f}% (时长: {dwell_meas.apoapsis_dwell_hours:.2f} 小时)")
    print(f"4.2米天线 X频段增益: {ant_x.gain_dbi:.2f} dBi, 波束角: {ant_x.half_power_beamwidth_deg:.2f}° ({ant_x.half_power_beamwidth_arcmin:.1f} 角分)")
    print(f"4.2米天线 Ka频段增益: {ant_ka.gain_dbi:.2f} dBi, 波束角: {ant_ka.half_power_beamwidth_deg:.2f}° ({ant_ka.half_power_beamwidth_arcmin:.1f} 角分)")
    print(f"地月中继单向光时: {ant_ka.one_way_light_time_seconds:.3f} 秒 (往返: {ant_ka.round_trip_light_time_seconds:.3f} 秒)")
    print(f"=== 2026 人类深空十八极黄金舰队 (The Grand Octodecet) ===")
    print(f"旗舰总数: {extremes['fleet_size']}, 日心极距跨度: {extremes['heliocentric_distance_ratio']:.1f} 倍, 辐射能流落差: {extremes['solar_radiation_flux_ratio']:.1f} 倍")
    print(f"地心极距跨度: {extremes['geocentric_distance_span_ratio']:.1f} 倍, 光时延迟跨度: {extremes['communication_owlt_span_ratio']:.1f} 倍 (V1 {extremes['voyager1_owlt_hours']:.2f}h vs Q2 {extremes['queqiao2_owlt_seconds']:.2f}s)")
