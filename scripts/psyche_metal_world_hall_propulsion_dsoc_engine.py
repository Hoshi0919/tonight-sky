"""
灵神星探测器 (Psyche) 金属世界探测、霍尔效应电推进 (SEP) 连续螺旋轨道动力学与
深空光通信 (DSOC) 量子光子链路推演引擎

覆盖：
1. (16) Psyche 金属小行星物理特性（Fe-Ni 暴露早期行星核、密度、表面引力、逃逸速度与发电机剩磁假说）
2. SPT-140 霍尔效应电推进系统（SEP）与连续低推力外螺旋动力学（比冲 1800s、240mN 微推力、齐奥尔科夫斯基工质质量比与化学推进对比）
3. 深空光通信 (DSOC) 1550nm 激光量子光子链路预算（帕洛马 200 英寸海尔望远镜、超导纳米线单光子探测、微弧度衍射极限与百倍微波射频带宽跃迁）
4. 2026-10-15 火星引力弹弓后 Cruise 2 巡航时空定位与 4 阶段科学探测轨道参数
5. 2026 人类深空九极黄金舰队 (The Grand Nonet) 宏伟时空矩阵与对偶极值体系
"""

import math
from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Dict, List, Any

# 基础物理与天文常数
AU_KM = 149597870.7          # 1 天文单位 (km)
C_LIGHT_KM_S = 299792.458    # 真空光速 (km/s)
C_LIGHT_M_S = 299792458.0    # 真空光速 (m/s)
G_CONST = 6.67430e-11        # 万有引力常数 (m^3 / (kg * s^2))
SOLAR_FLUX_1AU = 1361.0      # 1 AU 太阳常数 (W/m^2)
H_PLANCK = 6.62607015e-34    # 普朗克常数 (J*s)
G0 = 9.80665                 # 地球标准重力加速度 (m/s^2)


@dataclass
class PsycheAsteroidProperties:
    """(16) Psyche 目标天体物理特性"""
    name: str
    semi_major_axis_au: float
    eccentricity: float
    inclination_deg: float
    orbital_period_years: float
    triaxial_dimensions_km: tuple
    mean_diameter_km: float
    mass_kg: float
    volume_m3: float
    density_kg_m3: float
    surface_gravity_m_s2: float
    surface_gravity_g: float
    escape_velocity_m_s: float
    composition_type: str
    core_nature: str


@dataclass
class HallElectricPropulsionMetrics:
    """SPT-140 霍尔效应电推进动力学指标"""
    thruster_model: str
    active_thrusters_count: int
    input_power_kw: float
    thrust_mN: float
    thrust_N: float
    specific_impulse_s: float
    exhaust_velocity_m_s: float
    dry_mass_kg: float
    initial_xenon_mass_kg: float
    current_mass_kg: float
    mass_flow_rate_kg_s: float
    daily_xenon_consumption_kg: float
    current_accel_m_s2: float
    current_accel_mm_s2: float
    daily_delta_v_m_s: float
    target_transfer_delta_v_m_s: float
    hall_propellant_fraction_pct: float
    chemical_propellant_fraction_pct: float
    propellant_mass_saving_kg: float


@dataclass
class DsocPhotonLinkMetrics:
    """深空光通信 (DSOC) 1550nm 激光光子链路指标"""
    wavelength_nm: float
    wavelength_m: float
    optical_frequency_thz: float
    photon_energy_joules: float
    photon_energy_ev: float
    tx_aperture_m: float
    tx_power_w: float
    beam_divergence_urad: float
    beam_divergence_arcsec: float
    rf_xband_divergence_urad: float
    divergence_reduction_factor: float
    earth_distance_au: float
    earth_distance_km: float
    spot_radius_km: float
    spot_area_m2: float
    rx_telescope_name: str
    rx_aperture_m: float
    rx_area_m2: float
    optical_efficiency: float
    received_power_pw: float
    photon_arrival_rate_m_photons_s: float
    achievable_data_rate_mbps: float
    rf_typical_data_rate_kbps: float
    bandwidth_gain_factor: float


@dataclass
class PsycheCruiseCoordinates:
    """Psyche 2026-10-15 巡航坐标与时空状态"""
    ref_time_utc: datetime
    launch_date_utc: datetime
    mars_flyby_date_utc: datetime
    cruise2_start_date_utc: datetime
    arrival_date_utc: datetime
    days_post_launch: float
    days_post_mars_flyby: float
    days_to_arrival: float
    heliocentric_distance_au: float
    heliocentric_distance_km: float
    earth_distance_au: float
    earth_distance_km: float
    one_way_light_time_min: float
    round_trip_light_time_min: float
    solar_flux_w_m2: float
    solar_array_power_kw: float
    current_mission_phase: str


def calculate_psyche_asteroid_properties() -> PsycheAsteroidProperties:
    """解算 (16) Psyche 目标天体物理与引力场参数"""
    semi_major_axis_au = 2.924
    eccentricity = 0.134
    inclination_deg = 3.095
    orbital_period_years = 5.00

    # 椭球体三轴半径 (km): 279 x 232 x 189 km
    dim_a_km = 279.0 / 2.0
    dim_b_km = 232.0 / 2.0
    dim_c_km = 189.0 / 2.0
    mean_radius_km = (dim_a_km * dim_b_km * dim_c_km) ** (1.0 / 3.0)
    mean_diameter_km = mean_radius_km * 2.0

    mass_kg = 2.41e19  # 2.41 x 10^19 kg
    volume_m3 = (4.0 / 3.0) * math.pi * (dim_a_km * 1000.0) * (dim_b_km * 1000.0) * (dim_c_km * 1000.0)
    density_kg_m3 = mass_kg / volume_m3

    mean_radius_m = mean_radius_km * 1000.0
    surface_gravity_m_s2 = (G_CONST * mass_kg) / (mean_radius_m ** 2)
    surface_gravity_g = surface_gravity_m_s2 / G0
    escape_velocity_m_s = math.sqrt(2.0 * G_CONST * mass_kg / mean_radius_m)

    return PsycheAsteroidProperties(
        name="(16) Psyche (灵神星)",
        semi_major_axis_au=semi_major_axis_au,
        eccentricity=eccentricity,
        inclination_deg=inclination_deg,
        orbital_period_years=orbital_period_years,
        triaxial_dimensions_km=(279.0, 232.0, 189.0),
        mean_diameter_km=mean_diameter_km,
        mass_kg=mass_kg,
        volume_m3=volume_m3,
        density_kg_m3=density_kg_m3,
        surface_gravity_m_s2=surface_gravity_m_s2,
        surface_gravity_g=surface_gravity_g,
        escape_velocity_m_s=escape_velocity_m_s,
        composition_type="M 型金属富集小行星 (暴露的微行星铁镍核)",
        core_nature="早期分化行星核遭受灾难性剥离剥蚀残留物，具备发电机古剩磁假说"
    )


def calculate_hall_propulsion_metrics(
    current_mass_kg: float = 2320.0,
    target_dv_m_s: float = 4500.0
) -> HallElectricPropulsionMetrics:
    """解算 SPT-140 霍尔效应电推进系统与齐奥尔科夫斯基动力学对比"""
    thruster_model = "SPT-140 霍尔效应等离子体推进器"
    active_thrusters = 1
    input_power_kw = 4.5
    thrust_mN = 240.0
    thrust_N = thrust_mN / 1000.0
    isp_s = 1800.0
    exhaust_v_m_s = G0 * isp_s  # ~17651.97 m/s

    dry_mass_kg = 1660.0
    initial_xenon_kg = 1085.0

    # 质量流率
    mdot_kg_s = thrust_N / exhaust_v_m_s
    daily_xenon_kg = mdot_kg_s * 86400.0

    # 加速度与日化 delta v
    accel_m_s2 = thrust_N / current_mass_kg
    accel_mm_s2 = accel_m_s2 * 1000.0
    daily_dv = accel_m_s2 * 86400.0

    # 齐奥尔科夫斯基推进剂效率对比 (Target Δv = 4500 m/s)
    # 霍尔电推:
    mass_ratio_hall = math.exp(target_dv_m_s / exhaust_v_m_s)
    hall_prop_frac = 1.0 - (1.0 / mass_ratio_hall)
    hall_fuel_needed = current_mass_kg * (1.0 - math.exp(-target_dv_m_s / exhaust_v_m_s))

    # 经典双元化学火箭 (Isp = 310 s, MON-3/MMH, ve = 3040 m/s):
    isp_chem = 310.0
    exhaust_v_chem = G0 * isp_chem
    mass_ratio_chem = math.exp(target_dv_m_s / exhaust_v_chem)
    chem_prop_frac = 1.0 - (1.0 / mass_ratio_chem)
    chem_fuel_needed = current_mass_kg * (1.0 - math.exp(-target_dv_m_s / exhaust_v_chem))

    mass_saving_kg = chem_fuel_needed - hall_fuel_needed

    return HallElectricPropulsionMetrics(
        thruster_model=thruster_model,
        active_thrusters_count=active_thrusters,
        input_power_kw=input_power_kw,
        thrust_mN=thrust_mN,
        thrust_N=thrust_N,
        specific_impulse_s=isp_s,
        exhaust_velocity_m_s=exhaust_v_m_s,
        dry_mass_kg=dry_mass_kg,
        initial_xenon_mass_kg=initial_xenon_kg,
        current_mass_kg=current_mass_kg,
        mass_flow_rate_kg_s=mdot_kg_s,
        daily_xenon_consumption_kg=daily_xenon_kg,
        current_accel_m_s2=accel_m_s2,
        current_accel_mm_s2=accel_mm_s2,
        daily_delta_v_m_s=daily_dv,
        target_transfer_delta_v_m_s=target_dv_m_s,
        hall_propellant_fraction_pct=hall_prop_frac * 100.0,
        chemical_propellant_fraction_pct=chem_prop_frac * 100.0,
        propellant_mass_saving_kg=mass_saving_kg
    )


def calculate_dsoc_photon_link(
    earth_distance_au: float = 2.684,
    tx_power_w: float = 5.0,
    tx_aperture_m: float = 0.22,
    rx_aperture_m: float = 5.08,
    optical_efficiency: float = 0.40
) -> DsocPhotonLinkMetrics:
    """解算 DSOC 1550nm 激光光子链路物理与帕洛马山 200 英寸单光子探测"""
    wavelength_nm = 1550.0
    wavelength_m = wavelength_nm * 1e-9

    optical_freq_hz = C_LIGHT_M_S / wavelength_m
    optical_freq_thz = optical_freq_hz / 1e12
    photon_energy_j = H_PLANCK * optical_freq_hz
    photon_energy_ev = photon_energy_j / 1.602176634e-19

    # 衍射极限发散角 (Airy disk 艾里斑一阶零点角直径: theta = 1.22 lambda / D)
    beam_div_rad = 1.22 * wavelength_m / tx_aperture_m
    beam_div_urad = beam_div_rad * 1e6
    beam_div_arcsec = beam_div_rad * (180.0 / math.pi) * 3600.0

    # 对比 8.4 GHz X 频段深空射频 (lambda = 3.57 cm, 3m 抛物面天线)
    rf_wavelength_m = 0.0357
    rf_aperture_m = 3.0
    rf_div_rad = 1.22 * rf_wavelength_m / rf_aperture_m
    rf_div_urad = rf_div_rad * 1e6
    div_reduction = rf_div_urad / beam_div_urad

    # 接收端几何参数 (在指定地心距离)
    earth_dist_km = earth_distance_au * AU_KM
    earth_dist_m = earth_dist_km * 1000.0

    spot_radius_m = earth_dist_m * (beam_div_rad / 2.0)
    spot_radius_km = spot_radius_m / 1000.0
    spot_area_m2 = math.pi * (spot_radius_m ** 2)

    rx_area_m2 = math.pi * ((rx_aperture_m / 2.0) ** 2)

    # 接收功率与光子到达率
    p_rx_w = tx_power_w * optical_efficiency * (rx_area_m2 / spot_area_m2)
    p_rx_pw = p_rx_w * 1e12  # 皮瓦 (pW)

    photon_rate = p_rx_w / photon_energy_j
    photon_rate_m_s = photon_rate / 1e6  # 百万光子/秒 (Mphotons/s)

    # PPM 调制可达速率估算 (典型 64-PPM，每比特探测需 ~2.5 个光子)
    photons_per_bit = 2.5
    achievable_mbps = (photon_rate / photons_per_bit) / 1e6

    # 传统深空 X-band 在 2.7 AU 的典型码率
    rf_typical_kbps = 100.0
    bandwidth_gain = (achievable_mbps * 1000.0) / rf_typical_kbps

    return DsocPhotonLinkMetrics(
        wavelength_nm=wavelength_nm,
        wavelength_m=wavelength_m,
        optical_frequency_thz=optical_freq_thz,
        photon_energy_joules=photon_energy_j,
        photon_energy_ev=photon_energy_ev,
        tx_aperture_m=tx_aperture_m,
        tx_power_w=tx_power_w,
        beam_divergence_urad=beam_div_urad,
        beam_divergence_arcsec=beam_div_arcsec,
        rf_xband_divergence_urad=rf_div_urad,
        divergence_reduction_factor=div_reduction,
        earth_distance_au=earth_distance_au,
        earth_distance_km=earth_dist_km,
        spot_radius_km=spot_radius_km,
        spot_area_m2=spot_area_m2,
        rx_telescope_name="帕洛马山天文台 200 英寸 (5.08m) 海尔望远镜 (SNSPD 超导纳米线探测器)",
        rx_aperture_m=rx_aperture_m,
        rx_area_m2=rx_area_m2,
        optical_efficiency=optical_efficiency,
        received_power_pw=p_rx_pw,
        photon_arrival_rate_m_photons_s=photon_rate_m_s,
        achievable_data_rate_mbps=achievable_mbps,
        rf_typical_data_rate_kbps=rf_typical_kbps,
        bandwidth_gain_factor=bandwidth_gain
    )


def calculate_psyche_cruise_coordinates(
    ref_time_utc: datetime = datetime(2026, 10, 15, 8, 0, 0, tzinfo=timezone.utc)
) -> PsycheCruiseCoordinates:
    """计算 Psyche 探测器在 2026-10-15 巡航坐标与时空状态"""
    launch_date = datetime(2023, 10, 13, 14, 19, 0, tzinfo=timezone.utc)
    mars_flyby = datetime(2026, 5, 15, 12, 0, 0, tzinfo=timezone.utc)
    cruise2_start = datetime(2026, 5, 17, 0, 0, 0, tzinfo=timezone.utc)
    arrival_date = datetime(2029, 8, 1, 0, 0, 0, tzinfo=timezone.utc)

    days_post_launch = (ref_time_utc - launch_date).total_seconds() / 86400.0
    days_post_mars = (ref_time_utc - mars_flyby).total_seconds() / 86400.0
    days_to_arrival = (arrival_date - ref_time_utc).total_seconds() / 86400.0

    # 2026-10-15 日心与地心距离 (Cruise 2 阶段向小行星带外推)
    r_sun_au = 2.042
    r_sun_km = r_sun_au * AU_KM
    delta_earth_au = 2.684
    delta_earth_km = delta_earth_au * AU_KM

    one_way_light_sec = delta_earth_km / C_LIGHT_KM_S
    one_way_light_min = one_way_light_sec / 60.0
    round_trip_light_min = one_way_light_min * 2.0

    # 太阳辐射能流与 75 m^2 帆板输出功率
    solar_flux = SOLAR_FLUX_1AU / (r_sun_au ** 2)
    solar_array_area_m2 = 75.0
    cell_efficiency = 0.30  # 高效砷化镓三结太阳电池
    solar_power_kw = (solar_flux * solar_array_area_m2 * cell_efficiency) / 1000.0

    return PsycheCruiseCoordinates(
        ref_time_utc=ref_time_utc,
        launch_date_utc=launch_date,
        mars_flyby_date_utc=mars_flyby,
        cruise2_start_date_utc=cruise2_start,
        arrival_date_utc=arrival_date,
        days_post_launch=days_post_launch,
        days_post_mars_flyby=days_post_mars,
        days_to_arrival=days_to_arrival,
        heliocentric_distance_au=r_sun_au,
        heliocentric_distance_km=r_sun_km,
        earth_distance_au=delta_earth_au,
        earth_distance_km=delta_earth_km,
        one_way_light_time_min=one_way_light_min,
        round_trip_light_time_min=round_trip_light_min,
        solar_flux_w_m2=solar_flux,
        solar_array_power_kw=solar_power_kw,
        current_mission_phase="Cruise 2 连续霍尔电推进外螺旋巡航（火星借力后 153 天）"
    )


def generate_grand_nonet_fleet_summary() -> List[Dict[str, Any]]:
    """
    构建 2026 人类深空九极黄金舰队 (The Grand Nonet) 宏伟对比矩阵。
    """
    return [
        {
            "rank": 1,
            "name": "旅行者 1 号 (Voyager 1)",
            "agency": "NASA",
            "distance_au": 173.22,
            "domain": "恒星际极寒最远边界",
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
            "key_feature": "今日 (10-15) 实施 BRM-1 减速点火，Dimorphos 反冲动量放大因子 beta=3.7 原位实测",
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
        },
        {
            "rank": 9,
            "name": "灵神星探测器 (Psyche)",
            "agency": "NASA",
            "distance_au": 2.042,
            "domain": "金属核心世界、霍尔电推螺旋与激光通信极",
            "key_feature": "探测太阳系唯一暴露微行星铁镍核 (16) Psyche；SPT-140 霍尔电推 (Isp=1800s, 节油 1.2 吨)；DSOC 1550nm 激光 33.8 Mphotons/s 超百倍带宽跃迁",
            "speed_km_s": 21.5
        }
    ]


if __name__ == "__main__":
    ast = calculate_psyche_asteroid_properties()
    hall = calculate_hall_propulsion_metrics()
    dsoc = calculate_dsoc_photon_link()
    coord = calculate_psyche_cruise_coordinates()
    fleet = generate_grand_nonet_fleet_summary()

    print("================================================================================")
    print("灵神星探测器 (Psyche) 金属世界、霍尔电推连续外螺旋与 DSOC 激光光子链路推演引擎")
    print("================================================================================")
    print(f"目标天体: {ast.name}, 半长轴: {ast.semi_major_axis_au} AU, 周期: {ast.orbital_period_years} 年")
    print(f"三轴外包络: {ast.triaxial_dimensions_km[0]} x {ast.triaxial_dimensions_km[1]} x {ast.triaxial_dimensions_km[2]} km, 等效平均直径: {ast.mean_diameter_km:.1f} km")
    print(f"天体质量: {ast.mass_kg:.2e} kg, 估计体积: {ast.volume_m3:.2e} m³, 体密度: {ast.density_kg_m3:.1f} kg/m³")
    print(f"表面重力: {ast.surface_gravity_m_s2:.4f} m/s² ({ast.surface_gravity_g:.5f} g), 逃逸速度: {ast.escape_velocity_m_s:.2f} m/s")
    print(f"科学属性: {ast.composition_type} | {ast.core_nature}")
    print("--------------------------------------------------------------------------------")
    print(f"推进系统: {hall.thruster_model}, 在轨工作推力: {hall.thrust_mN:.1f} mN ({hall.input_power_kw:.1f} kW)")
    print(f"比冲: {hall.specific_impulse_s:.0f} s, 有效排气速度: {hall.exhaust_velocity_m_s:.1f} m/s ({hall.exhaust_velocity_m_s/1000.0:.2f} km/s)")
    print(f"工质流率: {hall.mass_flow_rate_kg_s:.4e} kg/s, 每日氙气消耗: {hall.daily_xenon_consumption_kg:.3f} kg/天")
    print(f"当前在轨质量: {hall.current_mass_kg:.1f} kg, 实时加速度: {hall.current_accel_mm_s2:.4f} mm/s²")
    print(f"日累积速度增量: {hall.daily_delta_v_m_s:.3f} m/s/天")
    print(f"Δv = {hall.target_transfer_delta_v_m_s:.0f} m/s 推进效率对比:")
    print(f"  - 霍尔电推推进剂占比: {hall.hall_propellant_fraction_pct:.1f}%")
    print(f"  - 传统双元化学推进剂占比: {hall.chemical_propellant_fraction_pct:.1f}%")
    print(f"  - 节省工质质量: {hall.propellant_mass_saving_kg:,.1f} kg (减重超 1.2 吨！)")
    print("--------------------------------------------------------------------------------")
    print(f"深空光通信 (DSOC): 波长 {dsoc.wavelength_nm:.0f} nm ({dsoc.optical_frequency_thz:.1f} THz), 发射口径: {dsoc.tx_aperture_m*100:.0f} cm")
    print(f"单光子能量: {dsoc.photon_energy_joules:.4e} J ({dsoc.photon_energy_ev:.3f} eV)")
    print(f"光束发散角: {dsoc.beam_divergence_urad:.2f} μrad ({dsoc.beam_divergence_arcsec:.2f} 角秒), 较微波 X 频段聚集提升 {dsoc.divergence_reduction_factor:.1f} 倍")
    print(f"地心距离 {dsoc.earth_distance_au:.3f} AU ({dsoc.earth_distance_km:,.1f} km) 处:")
    print(f"  - 地表光斑半径: {dsoc.spot_radius_km:,.1f} km (光斑面积 {dsoc.spot_area_m2:.2e} m²)")
    print(f"  - 帕洛马 200 英寸望远镜接收功率: {dsoc.received_power_pw:.2f} pW")
    print(f"  - 光子到达速率: {dsoc.photon_arrival_rate_m_photons_s:.2f} Mphotons/s")
    print(f"  - 可达下行数据率: {dsoc.achievable_data_rate_mbps:.2f} Mbps (较传统微波 {dsoc.rf_typical_data_rate_kbps:.0f} kbps 跃升 {dsoc.bandwidth_gain_factor:.1f} 倍)")
    print("--------------------------------------------------------------------------------")
    print(f"2026-10-15 巡航状态: {coord.current_mission_phase}")
    print(f"发射后第 {coord.days_post_launch:.1f} 天, 火星借力后第 {coord.days_post_mars_flyby:.1f} 天, 距灵神星抵达倒计时 {coord.days_to_arrival:.1f} 天 (约 2.8 年)")
    print(f"日心距: {coord.heliocentric_distance_au:.3f} AU, 地心距: {coord.earth_distance_au:.3f} AU, 单向光行时: {coord.one_way_light_time_min:.2f} 分钟 (往返 {coord.round_trip_light_time_min:.2f} 分钟)")
    print(f"太阳辐射能流: {coord.solar_flux_w_m2:.1f} W/m², 75m² 太阳帆板输出电功率: {coord.solar_array_power_kw:.2f} kW")
    print("================================================================================")
    print("2026 人类深空九极黄金舰队 (The Grand Nonet) 对比表:")
    for m in fleet:
        print(f"  [{m['rank']}] {m['name']:<30} | {m['agency']:<12} | {m['distance_au']:>8.3f} AU | {m['domain']:<22} | {m['key_feature']}")
    print("================================================================================")
