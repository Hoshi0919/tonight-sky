"""
朱诺号 (Juno) 木星极轨道动力学、180公斤纯钛防辐射保险库、
5.2 AU 弱光太阳能极限与 PJ88/PJ89 极近掠飞推演引擎
======================================================================

涵盖:
1. 开普勒高偏心率 33 天极轨道 (i ≈ 90°) 天体力学与近木点 57.8 km/s 极限掠飞极速
2. 2026-10-12 PJ88 掠飞 (刚刚过去 4 天) 与 2026-11-13 PJ89 倒计时 28 天
3. 180 公斤 1 厘米厚纯钛防辐射保险库 (Titanium Vault) 与 800 倍辐射剂量强力压制物理
4. 5.2 AU 外行星 60 m² 三叶巨型太阳能帆板与 450 W 极弱光电能调度奇迹
5. 木星深空物理大发现: 0.5 R_J 弥散稀释核心、300~500 km 扎根大红斑与极区正多边形稳定气旋群
"""

import math
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Tuple

# ---------------------------------------------------------
# 基础物理与木星常数 (IAU / CODATA 2018 标定)
# ---------------------------------------------------------
SPEED_OF_LIGHT = 299792.458                 # 真空光速 c, km/s
SECONDS_PER_DAY = 86400                     # 平太阳日秒数
AU_KM = 149597870.7                         # 1 天文单位 (AU) km
SOLAR_CONSTANT_1AU = 1361.0                 # 地球 1 AU 太阳常数 W/m²

# 木星物理常数
GM_JUPITER = 1.26686534e17                  # 木星引力常数 μ_J, m³/s² (1.26686534e8 km³/s²)
R_JUPITER_EQUATORIAL_KM = 71492.0           # 木星赤道半径 km
R_JUPITER_POLAR_KM = 66854.0                # 木星极半径 km
MASS_JUPITER_KG = 1.89813e27                # 木星质量 kg (地球的 317.8 倍)
JUPITER_HELIOCENTRIC_AU = 5.204             # 木星平均日心距 AU

# ---------------------------------------------------------
# 朱诺号轨道与结构参数 (NASA JPL Juno Mission)
# ---------------------------------------------------------
LAUNCH_UTC = datetime(2011, 8, 5, 16, 25, 0, tzinfo=timezone.utc)
JOI_UTC = datetime(2016, 7, 5, 3, 53, 0, tzinfo=timezone.utc)

# 2026 年近木点周期历表 (33 天科学极轨道)
PJ86_UTC = datetime(2026, 8, 7, 14, 51, 48, tzinfo=timezone.utc)
PJ87_UTC = datetime(2026, 9, 9, 6, 25, 37, tzinfo=timezone.utc)
PJ88_UTC = datetime(2026, 10, 12, 11, 42, 0, tzinfo=timezone.utc)   # 4 天前刚过
PJ89_UTC = datetime(2026, 11, 13, 14, 57, 59, tzinfo=timezone.utc)  # 下一次近木点
PJ90_UTC = datetime(2026, 12, 16, 7, 25, 9, tzinfo=timezone.utc)

JUNO_ORBIT_PERIOD_DAYS = 33.0               # 当前公转周期 (天)
JUNO_PERIJOVE_ALTITUDE_KM = 3500.0          # 近木点掠过云顶高度 km
JUNO_INCLINATION_DEG = 89.8                 # 极轨道倾角 deg

# 钛辐射保险库参数
VAULT_MASS_KG = 180.0                       # 纯钛保险库质量 kg
VAULT_WALL_THICKNESS_CM = 1.0               # 纯钛壁厚 cm (0.4 英寸)
EXTERNAL_TOTAL_IONIZING_DOSE_RAD = 20.0e6   # 外部累积高能辐射剂量 20 Mrad
INTERNAL_MAX_SHIELDED_DOSE_RAD = 25000.0    # 内部允许耐受剂量 25 krad
RADIATION_ATTENUATION_RATIO = 800.0         # 辐射衰减比率

# 太阳能帆板与能效
SOLAR_ARRAY_AREA_M2 = 60.0                  # 3 块阵列总采光面积 m²
SOLAR_ARRAY_EFFICIENCY_LILT = 0.28          # 弱光低温 (LILT, -100°C) 初始转换效率
RADIATION_AGING_FACTOR_2026 = 0.54          # 10 年在轨极端辐射累积衰减系数
BASE_HOUSEKEEPING_POWER_W = 150.0           # 航电温控基准巡航功耗 W


@dataclass(frozen=True)
class PolarOrbitState:
    """木星极轨道动力学状态"""
    periapsis_radius_km: float
    apoapsis_radius_km: float
    semi_major_axis_km: float
    eccentricity: float
    period_days: float
    periapsis_velocity_kms: float
    periapsis_velocity_kmh: float
    apoapsis_velocity_kms: float
    speed_ratio_peri_apo: float


@dataclass(frozen=True)
class PerijoveCountdown:
    """近木点掠飞倒计时与时序"""
    current_utc: datetime
    last_perijove_number: int
    last_perijove_utc: datetime
    days_since_last_pj: float
    next_perijove_number: int
    next_perijove_utc: datetime
    days_until_next_pj: float
    true_anomaly_approx_deg: float


@dataclass(frozen=True)
class RadiationVaultShielding:
    """钛合金辐射保险库屏蔽效能"""
    vault_mass_kg: float
    vault_thickness_cm: float
    external_dose_rad: float
    internal_dose_rad: float
    attenuation_factor: float
    is_safe_for_rad750: bool


@dataclass(frozen=True)
class LowIntensitySolarPower:
    """5.2 AU 弱光太阳能物理与功率预算"""
    heliocentric_distance_au: float
    solar_flux_w_m2: float
    flux_ratio_to_earth: float
    array_area_m2: float
    generated_power_w: float
    housekeeping_power_w: float
    net_science_margin_w: float
    power_margin_percentage: float


@dataclass(frozen=True)
class JovianInteriorAtmosphereInsights:
    """木星内部结构与大气深空发现"""
    dilute_core_radius_rj: float
    great_red_spot_depth_km: float
    north_polar_cyclone_geometry: str
    south_polar_cyclone_geometry: str
    magnetic_field_dynamo_origin: str


class JunoJupiterPolarEngine:
    """朱诺号木星极轨道动力学与工程物理推演引擎"""

    def __init__(self, observation_time: datetime = None):
        if observation_time is None:
            self.obs_time = datetime(2026, 10, 16, 6, 0, 0, tzinfo=timezone.utc)
        else:
            self.obs_time = observation_time

    def compute_polar_orbit_dynamics(self) -> PolarOrbitState:
        """解算 33 天木星极轨道开普勒几何与近木点极速"""
        # 近地点半径 r_p = R_J + h_p
        r_p_km = R_JUPITER_EQUATORIAL_KM + JUNO_PERIJOVE_ALTITUDE_KM  # 74,992 km
        r_p_m = r_p_km * 1000.0

        # 由公转周期反解半长轴 a = (GM * P^2 / (4*pi^2))^(1/3)
        p_sec = JUNO_ORBIT_PERIOD_DAYS * SECONDS_PER_DAY
        semi_major_axis_m = (GM_JUPITER * (p_sec ** 2) / (4.0 * (math.pi ** 2))) ** (1.0 / 3.0)
        semi_major_axis_km = semi_major_axis_m / 1000.0

        # 偏心率 e = 1 - r_p / a
        ecc = 1.0 - (r_p_km / semi_major_axis_km)

        # 远地点半径 r_a = 2a - r_p
        r_a_km = 2.0 * semi_major_axis_km - r_p_km
        r_a_m = r_a_km * 1000.0

        # 活力公式解算近地点与远地点速度
        # v = sqrt(GM * (2/r - 1/a))
        v_p_ms = math.sqrt(GM_JUPITER * (2.0 / r_p_m - 1.0 / semi_major_axis_m))
        v_p_kms = v_p_ms / 1000.0
        v_p_kmh = v_p_kms * 3600.0

        v_a_ms = math.sqrt(GM_JUPITER * (2.0 / r_a_m - 1.0 / semi_major_axis_m))
        v_a_kms = v_a_ms / 1000.0

        speed_ratio = v_p_kms / v_a_kms

        return PolarOrbitState(
            periapsis_radius_km=r_p_km,
            apoapsis_radius_km=r_a_km,
            semi_major_axis_km=semi_major_axis_km,
            eccentricity=ecc,
            period_days=JUNO_ORBIT_PERIOD_DAYS,
            periapsis_velocity_kms=v_p_kms,
            periapsis_velocity_kmh=v_p_kmh,
            apoapsis_velocity_kms=v_a_kms,
            speed_ratio_peri_apo=speed_ratio
        )

    def compute_perijove_countdown(self) -> PerijoveCountdown:
        """解算 2026-10-16 瞬时近木点前后时序与掠飞倒计时"""
        days_since_pj88 = (self.obs_time - PJ88_UTC).total_seconds() / SECONDS_PER_DAY
        days_to_pj89 = (PJ89_UTC - self.obs_time).total_seconds() / SECONDS_PER_DAY

        # 轨道相位与真近点角近似: 刚过近木点 4 天, 正在向远地点爬升
        orbit_fraction = days_since_pj88 / JUNO_ORBIT_PERIOD_DAYS
        # 椭圆轨道均近点角 M = 2*pi * fraction
        m_rad = 2.0 * math.pi * orbit_fraction
        # 粗略真近点角近似 (高偏心率下前几天真近点角迅速增大)
        approx_true_anomaly_deg = min(170.0, math.degrees(m_rad * 3.5))

        return PerijoveCountdown(
            current_utc=self.obs_time,
            last_perijove_number=88,
            last_perijove_utc=PJ88_UTC,
            days_since_last_pj=days_since_pj88,
            next_perijove_number=89,
            next_perijove_utc=PJ89_UTC,
            days_until_next_pj=days_to_pj89,
            true_anomaly_approx_deg=approx_true_anomaly_deg
        )

    def evaluate_radiation_vault(self) -> RadiationVaultShielding:
        """评估 180 公斤纯钛保险库的电离辐射衰减能力"""
        ext_dose = EXTERNAL_TOTAL_IONIZING_DOSE_RAD
        int_dose = ext_dose / RADIATION_ATTENUATION_RATIO
        is_safe = int_dose <= INTERNAL_MAX_SHIELDED_DOSE_RAD

        return RadiationVaultShielding(
            vault_mass_kg=VAULT_MASS_KG,
            vault_thickness_cm=VAULT_WALL_THICKNESS_CM,
            external_dose_rad=ext_dose,
            internal_dose_rad=int_dose,
            attenuation_factor=RADIATION_ATTENUATION_RATIO,
            is_safe_for_rad750=is_safe
        )

    def compute_solar_power_budget(self) -> LowIntensitySolarPower:
        """解算 5.2 AU 处弱光太阳能物理与功率裕度"""
        dist_au = JUPITER_HELIOCENTRIC_AU
        flux_w_m2 = SOLAR_CONSTANT_1AU / (dist_au ** 2)
        flux_ratio = flux_w_m2 / SOLAR_CONSTANT_1AU

        # 输出电力 P = Flux * Area * Efficiency * Aging
        p_gen = flux_w_m2 * SOLAR_ARRAY_AREA_M2 * SOLAR_ARRAY_EFFICIENCY_LILT * RADIATION_AGING_FACTOR_2026
        net_margin = p_gen - BASE_HOUSEKEEPING_POWER_W
        margin_pct = (net_margin / BASE_HOUSEKEEPING_POWER_W) * 100.0

        return LowIntensitySolarPower(
            heliocentric_distance_au=dist_au,
            solar_flux_w_m2=flux_w_m2,
            flux_ratio_to_earth=flux_ratio,
            array_area_m2=SOLAR_ARRAY_AREA_M2,
            generated_power_w=p_gen,
            housekeeping_power_w=BASE_HOUSEKEEPING_POWER_W,
            net_science_margin_w=net_margin,
            power_margin_percentage=margin_pct
        )

    def evaluate_interior_atmosphere_discoveries(self) -> JovianInteriorAtmosphereInsights:
        """评估朱诺号对木星内部发电机、大红斑与极区气旋的里程碑科学发现"""
        return JovianInteriorAtmosphereInsights(
            dilute_core_radius_rj=0.50,
            great_red_spot_depth_km=400.0,
            north_polar_cyclone_geometry="1 Central + 8 Surrounding Nonagon (正九边形气旋群)",
            south_polar_cyclone_geometry="1 Central + 5 Surrounding Pentagon/Hexagon (正五/六边形气旋群)",
            magnetic_field_dynamo_origin="Metallic Hydrogen Layer (金属氢对流发电机)"
        )


if __name__ == "__main__":
    engine = JunoJupiterPolarEngine()
    orbit = engine.compute_polar_orbit_dynamics()
    print(f"Juno 33-day Polar Orbit: a={orbit.semi_major_axis_km:,.1f} km, e={orbit.eccentricity:.4f}")
    print(f"Periapsis Radius: {orbit.periapsis_radius_km:,.1f} km, Speed: {orbit.periapsis_velocity_kms:.2f} km/s ({orbit.periapsis_velocity_kmh:,.1f} km/h)")
    print(f"Apoapsis Radius: {orbit.apoapsis_radius_km:,.1f} km, Speed: {orbit.apoapsis_velocity_kms:.2f} km/s")
    print(f"Speed Ratio: {orbit.speed_ratio_peri_apo:.1f}x")

    cd = engine.compute_perijove_countdown()
    print(f"Last PJ: PJ{cd.last_perijove_number} ({cd.days_since_last_pj:.2f} days ago)")
    print(f"Next PJ: PJ{cd.next_perijove_number} (in {cd.days_until_next_pj:.2f} days)")

    vault = engine.evaluate_radiation_vault()
    print(f"Radiation Vault: {vault.vault_mass_kg} kg, {vault.vault_thickness_cm} cm Ti, Attenuation: {vault.attenuation_factor:.0f}x")
    print(f"Dose: {vault.external_dose_rad/1e6:.1f} Mrad -> {vault.internal_dose_rad} rad (Safe: {vault.is_safe_for_rad750})")

    pwr = engine.compute_solar_power_budget()
    print(f"Solar Flux at {pwr.heliocentric_distance_au} AU: {pwr.solar_flux_w_m2:.2f} W/m² ({pwr.flux_ratio_to_earth*100:.2f}%)")
    print(f"Generated Power: {pwr.generated_power_w:.1f} W (Net Margin: {pwr.net_science_margin_w:.1f} W / +{pwr.power_margin_percentage:.1f}%)")
