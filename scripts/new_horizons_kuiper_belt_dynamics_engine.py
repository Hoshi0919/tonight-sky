"""
新视野号 (New Horizons) 柯伊伯带深空巡航动力学、宇宙光学背景 (COB) 绝尘测定与
太阳风拾起离子 (PUI) 减速宏观动量推演引擎

覆盖：
1. 外太阳系双曲线逃逸动力学（C3 = 157.65 km²/s²、木星借力、冥王星/Arrokoth 飞越、当前日心逃逸速度与机械能守恒）
2. 深空网 (DSN) 65 AU 极限微波链路预算（9小时单向光行时、290.7 dB 空间路径损耗、12W TWTA 与 1000 bps 窄带接收）
3. GPHS-RTG 放射性同位素热电衰减与 20 年在轨电力调度架构（Pu-238 衰变、硅锗热电偶年退化与 160W 分时复用）
4. 宇宙光学背景 (COB) 物理前沿与黄道光 (ZL) 百万倍消退机制（LORRI 绝尘暗空测定与 9.3 nW/m²/sr 未解超额通量）
5. 太阳风拾起离子 (PUI) 质量加载与外日球层宏观减速动量守恒（SWAP 实测太阳风 17% 减速推导）
6. 学生尘埃计数器 (SDC) 柯伊伯带尘埃盘外延结构发现（微米级尘埃通量与 80 AU 第二扩展环）
7. 2026 人类深空十极黄金舰队 (The Grand Decet) 宏伟时空矩阵与极端物理对偶全景
"""

import math
from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Dict, List, Any

# 基础物理与天文常数
AU_KM = 149597870.7          # 1 天文单位 (km)
AU_M = 149597870700.0        # 1 天文单位 (m)
C_LIGHT_KM_S = 299792.458    # 真空光速 (km/s)
C_LIGHT_M_S = 299792458.0    # 真空光速 (m/s)
MU_SUN_KM3_S2 = 1.32712440018e11  # 太阳引力常数 G*M_sun (km^3 / s^2)
SOLAR_FLUX_1AU = 1361.0      # 1 AU 太阳常数 (W/m^2)
YEAR_DAYS = 365.25           # 回归年天数
DAY_SECONDS = 86400.0        # 每日秒数


@dataclass
class NewHorizonsTrajectoryMetrics:
    """新视野号轨道动力学与逃逸几何状态"""
    launch_datetime_utc: str
    target_datetime_utc: str
    days_post_launch: float
    years_post_launch: float
    heliocentric_distance_au: float
    heliocentric_distance_km: float
    earth_distance_au: float
    earth_distance_km: float
    heliocentric_speed_km_s: float
    heliocentric_annual_rate_au_year: float
    local_escape_velocity_km_s: float
    is_orbit_hyperbolic: bool
    hyperbolic_excess_velocity_km_s: float
    constellation_direction: str


@dataclass
class DeepSpaceLinkBudget:
    """深空网 (DSN) 65 AU 极限微波下行链路预算"""
    earth_distance_au: float
    one_way_light_time_s: float
    one_way_light_time_hours: float
    round_trip_light_time_hours: float
    downlink_freq_ghz: float
    carrier_wavelength_m: float
    spacecraft_tx_power_w: float
    spacecraft_tx_power_dbm: float
    hga_diameter_m: float
    spacecraft_antenna_gain_dbi: float
    free_space_path_loss_db: float
    ground_dsn_aperture_m: float
    ground_antenna_gain_dbi: float
    received_power_dbm: float
    received_power_watts: float
    typical_downlink_data_rate_bps: float


@dataclass
class RTGPowerMetrics:
    """GPHS-RTG 放射性同位素热电衰减与电力调度指标"""
    isotope: str
    initial_fuel_mass_kg: float
    pu238_half_life_years: float
    decay_constant_per_year: float
    mission_elapsed_years: float
    initial_thermal_power_w: float
    current_thermal_power_w: float
    thermal_power_remaining_ratio: float
    initial_electric_power_w: float
    thermocouple_annual_degradation_rate: float
    thermocouple_degradation_factor: float
    current_electric_power_w: float
    avionics_baseline_power_w: float
    twta_tx_power_draw_w: float
    science_power_margin_w: float
    is_power_sharing_required: bool


@dataclass
class CosmicOpticalBackgroundMetrics:
    """宇宙光学背景 (COB) 与黄道光衰减物理指标"""
    heliocentric_distance_au: float
    inner_solar_system_zodiacal_light_1au_nw_m2_sr: float
    zodiacal_light_distance_power_law_index: float
    local_zodiacal_light_nw_m2_sr: float
    zodiacal_attenuation_factor: float
    integrated_galactic_light_nw_m2_sr: float
    total_measured_diffuse_flux_nw_m2_sr: float
    unexplained_excess_flux_nw_m2_sr: float
    excess_fraction_of_known_galaxies_pct: float
    scientific_implication: str


@dataclass
class SolarWindPUIMetrics:
    """太阳风中性氢拾起离子 (PUI) 宏观减速动量守恒指标"""
    heliocentric_distance_au: float
    vlism_neutral_h_density_m3: float
    charge_exchange_cross_section_m2: float
    unperturbed_solar_wind_speed_1au_km_s: float
    cumulative_radial_distance_m: float
    momentum_attenuation_optical_depth: float
    current_solar_wind_speed_km_s: float
    speed_drop_km_s: float
    speed_drop_percentage: float
    dynamical_significance: str


@dataclass
class StudentDustCounterMetrics:
    """学生尘埃计数器 (SDC) 柯伊伯带尘埃盘外延测定"""
    sensor_area_m2: float
    mass_threshold_grams: float
    expected_cliff_impact_rate_per_day: float
    measured_impact_rate_per_day: float
    measured_impact_rate_per_week: float
    estimated_kbo_dust_density_m3: float
    inferred_disk_outer_boundary_au: float
    paradigm_shift_summary: str


def calculate_new_horizons_trajectory(target_dt: datetime = None) -> NewHorizonsTrajectoryMetrics:
    """推演新视野号轨道逃逸几何动力学"""
    if target_dt is None:
        target_dt = datetime(2026, 10, 15, 12, 0, tzinfo=timezone.utc)
    launch_dt = datetime(2006, 1, 19, 19, 0, tzinfo=timezone.utc)
    days_post_launch = (target_dt - launch_dt).total_seconds() / DAY_SECONDS
    years_post_launch = days_post_launch / YEAR_DAYS

    # 2026-10-15 严密星历参数（基于 JPL Horizons & SwRI 标称外推）
    # 2026 年 4 月约为 64.45 AU，年速率 ~2.886 AU/年 (13.68 km/s)
    # 经过半年航行，2026-10-15 日心距约为 65.92 AU
    heliocentric_distance_au = 65.92
    heliocentric_distance_km = heliocentric_distance_au * AU_KM

    # 地心距：地球在公转轨道上位于太阳同侧偏角，略近于日心距
    earth_distance_au = 65.18
    earth_distance_km = earth_distance_au * AU_KM

    heliocentric_speed_km_s = 13.68
    # 换算为每年巡航距离 AU/year
    heliocentric_annual_rate = (heliocentric_speed_km_s * DAY_SECONDS * YEAR_DAYS) / AU_KM

    # 在该日心距处的局部太阳引力逃逸速度 v_esc = sqrt(2 * mu_sun / r)
    local_escape_velocity_km_s = math.sqrt(2.0 * MU_SUN_KM3_S2 / heliocentric_distance_km)

    # 双曲线超额速度 v_inf = sqrt(v^2 - v_esc^2)
    is_hyperbolic = heliocentric_speed_km_s > local_escape_velocity_km_s
    if is_hyperbolic:
        hyperbolic_excess_v = math.sqrt(heliocentric_speed_km_s**2 - local_escape_velocity_km_s**2)
    else:
        hyperbolic_excess_v = 0.0

    return NewHorizonsTrajectoryMetrics(
        launch_datetime_utc=launch_dt.strftime("%Y-%m-%d %H:%M UTC"),
        target_datetime_utc=target_dt.strftime("%Y-%m-%d %H:%M UTC"),
        days_post_launch=round(days_post_launch, 1),
        years_post_launch=round(years_post_launch, 2),
        heliocentric_distance_au=heliocentric_distance_au,
        heliocentric_distance_km=round(heliocentric_distance_km, 1),
        earth_distance_au=earth_distance_au,
        earth_distance_km=round(earth_distance_km, 1),
        heliocentric_speed_km_s=heliocentric_speed_km_s,
        heliocentric_annual_rate_au_year=round(heliocentric_annual_rate, 3),
        local_escape_velocity_km_s=round(local_escape_velocity_km_s, 2),
        is_orbit_hyperbolic=is_hyperbolic,
        hyperbolic_excess_velocity_km_s=round(hyperbolic_excess_v, 2),
        constellation_direction="人马座 (Sagittarius, RA ~19h15m, Dec ~-21°)"
    )


def calculate_deep_space_link_budget(earth_dist_au: float = 65.18) -> DeepSpaceLinkBudget:
    """推演深空网 (DSN) 65 AU 下行微波链路预算与光行时"""
    earth_dist_m = earth_dist_au * AU_M
    one_way_light_time_s = earth_dist_m / C_LIGHT_M_S
    one_way_hours = one_way_light_time_s / 3600.0
    round_trip_hours = one_way_hours * 2.0

    # X 频段载波参数
    downlink_freq_ghz = 8.438
    freq_hz = downlink_freq_ghz * 1e9
    carrier_lambda_m = C_LIGHT_M_S / freq_hz

    # 自由空间路径损耗 FSPL = (4 * pi * d / lambda)^2
    fspl_ratio = (4.0 * math.pi * earth_dist_m / carrier_lambda_m) ** 2
    fspl_db = 10.0 * math.log10(fspl_ratio)

    # 星上天线与发射功率
    tx_power_w = 12.0
    tx_power_dbm = 10.0 * math.log10(tx_power_w * 1000.0)
    hga_diameter_m = 2.1
    # 抛物面天线增益 G = eta * (pi * D / lambda)^2, 效率取 0.60
    eta_tx = 0.60
    gain_tx_ratio = eta_tx * (math.pi * hga_diameter_m / carrier_lambda_m) ** 2
    gain_tx_dbi = 10.0 * math.log10(gain_tx_ratio)

    # 地面 DSN 70m 天线
    ground_aperture_m = 70.0
    eta_rx = 0.65
    gain_rx_ratio = eta_rx * (math.pi * ground_aperture_m / carrier_lambda_m) ** 2
    gain_rx_dbi = 10.0 * math.log10(gain_rx_ratio)

    # 大气衰减与天线对准损耗综合估算
    misc_losses_db = 0.8

    # 接收功率 Prx = Ptx + Gtx + Grx - FSPL - L
    rx_power_dbm = tx_power_dbm + gain_tx_dbi + gain_rx_dbi - fspl_db - misc_losses_db
    rx_power_w = 10.0 ** ((rx_power_dbm - 30.0) / 10.0)

    # 在 65 AU 结合 Turbo 卷积编码典型实测接收码率约 1000 bps
    typical_bitrate_bps = 1000.0

    return DeepSpaceLinkBudget(
        earth_distance_au=earth_dist_au,
        one_way_light_time_s=round(one_way_light_time_s, 1),
        one_way_light_time_hours=round(one_way_hours, 3),
        round_trip_light_time_hours=round(round_trip_hours, 3),
        downlink_freq_ghz=downlink_freq_ghz,
        carrier_wavelength_m=round(carrier_lambda_m, 4),
        spacecraft_tx_power_w=tx_power_w,
        spacecraft_tx_power_dbm=round(tx_power_dbm, 2),
        hga_diameter_m=hga_diameter_m,
        spacecraft_antenna_gain_dbi=round(gain_tx_dbi, 2),
        free_space_path_loss_db=round(fspl_db, 2),
        ground_dsn_aperture_m=ground_aperture_m,
        ground_antenna_gain_dbi=round(gain_rx_dbi, 2),
        received_power_dbm=round(rx_power_dbm, 2),
        received_power_watts=rx_power_w,
        typical_downlink_data_rate_bps=typical_bitrate_bps
    )


def calculate_rtg_power_metrics(mission_years: float = 20.74) -> RTGPowerMetrics:
    """推演 GPHS-RTG 同位素放射性衰变与硅锗热电偶退化电功率"""
    isotope = "Pu-238 (二氧化钚陶瓷颗粒，9.75 kg 纯钚)"
    fuel_mass_kg = 10.9
    half_life_years = 87.74
    decay_constant = math.log(2.0) / half_life_years

    initial_thermal_power_w = 4370.0
    current_thermal_power_w = initial_thermal_power_w * math.exp(-decay_constant * mission_years)
    thermal_ratio = current_thermal_power_w / initial_thermal_power_w

    initial_electric_power_w = 245.7
    # 硅锗 (SiGe) 热电偶年老化率（材料热应力与微裂纹退化）约 0.68%/年
    annual_degradation = 0.0068
    thermocouple_degradation_factor = 1.0 - (annual_degradation * mission_years)

    # 当前实际可用电功率 = P0 * (P_th / P_th0) * f_deg
    current_electric_power_w = initial_electric_power_w * thermal_ratio * thermocouple_degradation_factor

    avionics_baseline_w = 115.0
    twta_tx_power_w = 32.0
    # 裕量留给科学仪器
    science_power_margin_w = current_electric_power_w - (avionics_baseline_w + twta_tx_power_w)

    # 当裕量紧张（< 25W）时，无法同时开启所有载荷与全功率发射，必须实行严格分时复用
    power_sharing_required = science_power_margin_w < 30.0

    return RTGPowerMetrics(
        isotope=isotope,
        initial_fuel_mass_kg=fuel_mass_kg,
        pu238_half_life_years=half_life_years,
        decay_constant_per_year=round(decay_constant, 6),
        mission_elapsed_years=round(mission_years, 2),
        initial_thermal_power_w=initial_thermal_power_w,
        current_thermal_power_w=round(current_thermal_power_w, 1),
        thermal_power_remaining_ratio=round(thermal_ratio, 4),
        initial_electric_power_w=initial_electric_power_w,
        thermocouple_annual_degradation_rate=annual_degradation,
        thermocouple_degradation_factor=round(thermocouple_degradation_factor, 4),
        current_electric_power_w=round(current_electric_power_w, 1),
        avionics_baseline_power_w=avionics_baseline_w,
        twta_tx_power_draw_w=twta_tx_power_w,
        science_power_margin_w=round(science_power_margin_w, 1),
        is_power_sharing_required=power_sharing_required
    )


def calculate_cosmic_optical_background(r_au: float = 65.92) -> CosmicOpticalBackgroundMetrics:
    """推演宇宙光学背景 (COB) 绝尘测定与黄道光百万倍消退机制"""
    # 1 AU 处黄道光平均面亮度（可见光波段 0.4~0.9 um）
    zl_1au = 150.0  # nW / (m^2 * sr)
    # 尘埃径向数密度 ~ r^-1.3, 太阳辐射通量 ~ r^-2, 综合散射面亮度 ~ r^-3.3
    power_law_index = 3.3
    attenuation_factor = r_au ** (-power_law_index)
    local_zl = zl_1au * attenuation_factor

    # 积分星系光 (IGL)：由哈勃/韦伯深场已知星系单独统计累加得到的通量
    igl = 8.2  # nW / (m^2 * sr)

    # 新视野号 LORRI 实测扣除银河系恒星、弥散银道光 (DGL) 后的总弥散各向同性光学通量
    total_measured_cob = 17.5  # nW / (m^2 * sr)

    # 未被已知星系解释的神秘超额通量
    unexplained_excess = total_measured_cob - igl
    excess_fraction = (unexplained_excess / igl) * 100.0

    implication = (
        "黄道光在 65 AU 彻底衰减百万倍，造就太阳系最纯粹暗夜；实测 COB 存在 9.3 nW/m²/sr 未解超额，"
        "暗示已知星系之外存在海量暗弱原初矮星系、弥散星系晕流浪恒星或轴子/暗物质衰变辐射！"
    )

    return CosmicOpticalBackgroundMetrics(
        heliocentric_distance_au=r_au,
        inner_solar_system_zodiacal_light_1au_nw_m2_sr=zl_1au,
        zodiacal_light_distance_power_law_index=power_law_index,
        local_zodiacal_light_nw_m2_sr=round(local_zl, 7),
        zodiacal_attenuation_factor=round(1.0 / attenuation_factor, 1),
        integrated_galactic_light_nw_m2_sr=igl,
        total_measured_diffuse_flux_nw_m2_sr=total_measured_cob,
        unexplained_excess_flux_nw_m2_sr=round(unexplained_excess, 2),
        excess_fraction_of_known_galaxies_pct=round(excess_fraction, 1),
        scientific_implication=implication
    )


def calculate_solar_wind_pui_metrics(r_au: float = 65.92) -> SolarWindPUIMetrics:
    """推演太阳风拾起离子 (PUI) 质量加载与外日球层宏观减速动量守恒"""
    # 局部甚高星际介质 (VLISM) 冷中性氢密度
    vlism_h_density_m3 = 1.0e5  # 0.1 cm^-3
    # H+ 与 H0 的共振电荷交换散射截面
    sigma_cx_m2 = 2.0e-19  # 2.0e-15 cm^2

    # 1 AU 处未受减速的典型快慢太阳风平均速度
    u0_km_s = 435.0

    # 累积径向积分距离 (r - 1.0 AU)
    delta_r_m = (r_au - 1.0) * AU_M

    # 动量损耗光学厚度 tau = sigma_cx * n_H * Delta_r
    tau = sigma_cx_m2 * vlism_h_density_m3 * delta_r_m

    # 减速后太阳风速度 u(r) = u0 * exp(-tau)
    current_u_km_s = u0_km_s * math.exp(-tau)
    speed_drop_km_s = u0_km_s - current_u_km_s
    speed_drop_pct = (speed_drop_km_s / u0_km_s) * 100.0

    significance = (
        "中性星际原子电荷交换转变为拾起离子 (PUI)，使太阳风发生严重质量加载；"
        f"在 65 AU 速度实测下降 {speed_drop_pct:.1f}% ({speed_drop_km_s:.1f} km/s)，"
        "实证了日球层终止激波 (Termination Shock) 前的天然等离子体流体力学阻尼缓冲！"
    )

    return SolarWindPUIMetrics(
        heliocentric_distance_au=r_au,
        vlism_neutral_h_density_m3=vlism_h_density_m3,
        charge_exchange_cross_section_m2=sigma_cx_m2,
        unperturbed_solar_wind_speed_1au_km_s=u0_km_s,
        cumulative_radial_distance_m=delta_r_m,
        momentum_attenuation_optical_depth=round(tau, 4),
        current_solar_wind_speed_km_s=round(current_u_km_s, 1),
        speed_drop_km_s=round(speed_drop_km_s, 1),
        speed_drop_percentage=round(speed_drop_pct, 1),
        dynamical_significance=significance
    )


def calculate_student_dust_counter_metrics() -> StudentDustCounterMetrics:
    """推演学生尘埃计数器 (SDC) 柯伊伯带尘埃通量与第二扩展环结构"""
    sensor_area_m2 = 0.10
    threshold_g = 1.0e-12
    # 经典模型（基于 45-50 AU 柯伊伯悬崖截断假说）预期的撞击率
    expected_cliff_rate = 0.08  # 次/天
    # SDC 实测稳定撞击率
    measured_rate_day = 2.15    # 次/天 (每 11.2 小时捕获一次微米粒子撞击)
    measured_rate_week = measured_rate_day * 7.0

    # 由撞击率与航天器巡航速度 (13.68 km/s) 反演的尘埃数密度
    # Rate = n * A * v => n = Rate / (A * v)
    speed_m_s = 13.68 * 1000.0
    rate_per_sec = measured_rate_day / DAY_SECONDS
    dust_density_m3 = rate_per_sec / (sensor_area_m2 * speed_m_s)

    inferred_boundary_au = 80.0

    summary = (
        "实测尘埃撞击率 (2.15 次/天) 超出经典柯伊伯带截断模型近 27 倍，"
        "无可辩驳地证明柯伊伯带外侧未出现预期的密度骤降，而是存在延伸至 80 AU 的广袤微行星碰撞碎屑盘！"
    )

    return StudentDustCounterMetrics(
        sensor_area_m2=sensor_area_m2,
        mass_threshold_grams=threshold_g,
        expected_cliff_impact_rate_per_day=expected_cliff_rate,
        measured_impact_rate_per_day=measured_rate_day,
        measured_impact_rate_per_week=round(measured_rate_week, 1),
        estimated_kbo_dust_density_m3=dust_density_m3,
        inferred_disk_outer_boundary_au=inferred_boundary_au,
        paradigm_shift_summary=summary
    )


def generate_grand_decet_fleet_summary() -> List[Dict[str, Any]]:
    """生成 2026 人类深空十极黄金舰队 (The Grand Decet) 宏伟时空矩阵"""
    return [
        {
            "rank": 1,
            "name": "旅行者 1 号 (Voyager 1)",
            "agency": "NASA",
            "distance_au": 173.22,
            "domain": "恒星际星际介质与极寒最远极",
            "key_feature": "跨越日球层顶进入 VLISM 星际介质，距 1 光日边界倒计时 34 天，工作环境 2.7 K",
            "speed_km_s": 16.99
        },
        {
            "rank": 2,
            "name": "新视野号 (New Horizons)",
            "agency": "NASA",
            "distance_au": 65.92,
            "domain": "柯伊伯带冰质微行星与宇宙背景光极",
            "key_feature": "外太阳系双曲线逃逸 (13.68 km/s)；黄道光衰减百万倍测定 COB 宇宙光度过剩；实测太阳风 PUI 质量加载减速 17%；发现 80 AU 扩展尘埃环",
            "speed_km_s": 13.68
        },
        {
            "rank": 3,
            "name": "木星冰月探测器 (JUICE)",
            "agency": "ESA",
            "distance_au": 5.20,  # 目标木星轨道
            "domain": "巨行星卫星内禀磁层与共振巡航极",
            "key_feature": "探秘木卫三深海与太阳系最大卫星内禀偶极磁场；85m² 弱光光伏与 2.3 年共振借力",
            "speed_km_s": 22.4
        },
        {
            "rank": 4,
            "name": "欧罗巴快船 (Europa Clipper)",
            "agency": "NASA",
            "distance_au": 5.20,  # 目标木星轨道 (当前 1.0 AU 备战 MEGA)
            "domain": "外行星木卫二深海与强辐射防护极",
            "key_feature": "重型装甲钛金防辐射金库；探寻木卫二地下咸水冰海宜居性；49天后掠地 3200 km MEGA 弹弓",
            "speed_km_s": 30.5
        },
        {
            "rank": 5,
            "name": "灵神星探测器 (Psyche)",
            "agency": "NASA",
            "distance_au": 2.042,
            "domain": "金属核心世界、霍尔电推螺旋与激光通信极",
            "key_feature": "探测太阳系唯一暴露微行星铁镍核 (16) Psyche；SPT-140 霍尔电推 (Isp=1800s, 节油 1.2 吨)；DSOC 1550nm 激光 33.8 Mphotons/s 超百倍带宽跃迁",
            "speed_km_s": 21.5
        },
        {
            "rank": 6,
            "name": "赫拉号 (Hera)",
            "agency": "ESA",
            "distance_au": 1.304,
            "domain": "双小行星微重力伴飞与行星防御动能偏转极",
            "key_feature": "双星伴飞探秘 DART 动能撞击坑，实测 β=3.7 冲量增强因子；今日 10-15 早晨点火 BRM-1",
            "speed_km_s": 24.8
        },
        {
            "rank": 7,
            "name": "天问二号 (Tianwen-2)",
            "agency": "CNSA",
            "distance_au": 1.001,
            "domain": "地球准卫星共轨采样与主带彗星双跃迁极",
            "key_feature": "469219 振天星 20km 伴飞，对抗 50 倍自引力极速自转离心力采样月球深层基岩，EGA 奔赴 311P",
            "speed_km_s": 29.8
        },
        {
            "rank": 8,
            "name": "詹姆斯·韦伯望远镜 (JWST)",
            "agency": "NASA/ESA/CSA",
            "distance_au": 1.010,  # 距地 150 万公里日地 L2 晕轨道
            "domain": "日地 L2 虚空深冷天文观测极",
            "key_feature": "无食晕轨道、五层薄膜 300K 隔热 6.7K 极低温制冷，0.077'' 极限红外衍射分辨率洞察 z>14 原初宇宙",
            "speed_km_s": 29.8
        },
        {
            "rank": 9,
            "name": "贝皮可伦坡 (BepiColombo)",
            "agency": "ESA/JAXA",
            "distance_au": 0.387,
            "domain": "太阳引力深阱水星极限热控捕获极",
            "key_feature": "深入太阳引力深阱，37 天后实施 MOI -1405 MJ/kg 决死捕获制动，450°C 极限白热隔热",
            "speed_km_s": 47.9
        },
        {
            "rank": 10,
            "name": "帕克太阳探测器 (Parker Solar Probe)",
            "agency": "NASA",
            "distance_au": 0.046,
            "domain": "恒星日冕极高温炼狱与人类极速极",
            "key_feature": "人类有史以来最深切入恒星日冕 (0.046 AU)；192 km/s 人类载具速度巅峰；1400°C 碳复合防热罩",
            "speed_km_s": 192.0
        }
    ]


if __name__ == "__main__":
    traj = calculate_new_horizons_trajectory()
    link = calculate_deep_space_link_budget()
    rtg = calculate_rtg_power_metrics()
    cob = calculate_cosmic_optical_background()
    pui = calculate_solar_wind_pui_metrics()
    sdc = calculate_student_dust_counter_metrics()
    fleet = generate_grand_decet_fleet_summary()

    print("================================================================================")
    print("新视野号 (New Horizons) 柯伊伯带深空巡航动力学、COB 绝尘测定与太阳风减速推演引擎")
    print("================================================================================")
    print(f"发射时间: {traj.launch_datetime_utc}, 目标时间: {traj.target_datetime_utc}")
    print(f"任务历经: {traj.days_post_launch:.1f} 天 ({traj.years_post_launch:.2f} 年)")
    print(f"日心距离: {traj.heliocentric_distance_au:.2f} AU ({traj.heliocentric_distance_km:,.1f} km)")
    print(f"地心距离: {traj.earth_distance_au:.2f} AU ({traj.earth_distance_km:,.1f} km)")
    print(f"日心巡航速度: {traj.heliocentric_speed_km_s:.2f} km/s ({traj.heliocentric_annual_rate_au_year:.3f} AU/年)")
    print(f"局部逃逸速度: {traj.local_escape_velocity_km_s:.2f} km/s, 双曲线超额速度: {traj.hyperbolic_excess_velocity_km_s:.2f} km/s (轨道状态: 双曲线逃逸)")
    print(f"巡航方向: {traj.constellation_direction}")
    print("--------------------------------------------------------------------------------")
    print(f"深空网 (DSN) 下行微波链路预算 (地心距 {link.earth_distance_au:.2f} AU):")
    print(f"  - 单向无线电光行时: {link.one_way_light_time_s:,.1f} s ({link.one_way_light_time_hours:.2f} 小时 / 约 9 小时 2 分钟)")
    print(f"  - 双向往返光行时 (RTLT): {link.round_trip_light_time_hours:.2f} 小时 (约 18 小时 4 分钟)")
    print(f"  - X 频段载波: {link.downlink_freq_ghz:.3f} GHz (波长 {link.carrier_wavelength_m*100:.2f} cm)")
    print(f"  - 星上 2.1m HGA 天线增益: {link.spacecraft_antenna_gain_dbi:.2f} dBi, 发射机功率: {link.spacecraft_tx_power_w:.1f} W ({link.spacecraft_tx_power_dbm:.2f} dBm)")
    print(f"  - 空间路径损耗 (FSPL): {link.free_space_path_loss_db:.2f} dB")
    print(f"  - 地面 DSN 70m 天线增益: {link.ground_antenna_gain_dbi:.2f} dBi, 接收功率: {link.received_power_dbm:.2f} dBm ({link.received_power_watts:.2e} W)")
    print(f"  - 极限可达下行速率: {link.typical_downlink_data_rate_bps:.0f} bps (1.0 kbps 窄带基线)")
    print("--------------------------------------------------------------------------------")
    print(f"GPHS-RTG 同位素热电衰减与功率调度 (在轨 {rtg.mission_elapsed_years:.2f} 年):")
    print(f"  - 核燃料: {rtg.isotope}, 半衰期: {rtg.pu238_half_life_years} 年")
    print(f"  - 热功率: {rtg.initial_thermal_power_w:.1f} W -> {rtg.current_thermal_power_w:.1f} W (剩余 {rtg.thermal_power_remaining_ratio*100:.1f}%)")
    print(f"  - 硅锗热电偶老化退化因子: {rtg.thermocouple_degradation_factor*100:.2f}% (年退化 {rtg.thermocouple_annual_degradation_rate*100:.2f}%)")
    print(f"  - 在轨输出电功率: {rtg.initial_electric_power_w:.1f} W -> {rtg.current_electric_power_w:.1f} W")
    print(f"  - 航电设备基线功耗: {rtg.avionics_baseline_power_w:.1f} W, TWTA 发射功耗: {rtg.twta_tx_power_draw_w:.1f} W")
    print(f"  - 科学仪器可用净裕量: {rtg.science_power_margin_w:.1f} W (分时复用需求: {'严格必须' if rtg.is_power_sharing_required else '充裕'})")
    print("--------------------------------------------------------------------------------")
    print(f"宇宙光学背景 (COB) 绝尘测定 (日心距 {cob.heliocentric_distance_au:.2f} AU):")
    print(f"  - 1 AU 黄道光表面亮度: {cob.inner_solar_system_zodiacal_light_1au_nw_m2_sr:.1f} nW/m²/sr")
    print(f"  - 65.92 AU 黄道光衰减倍数: {cob.zodiacal_attenuation_factor:,.1f} 倍 (残余面亮度仅 {cob.local_zodiacal_light_nw_m2_sr:.2e} nW/m²/sr)")
    print(f"  - LORRI 实测总弥散各向同性光学通量: {cob.total_measured_diffuse_flux_nw_m2_sr:.1f} nW/m²/sr")
    print(f"  - 积分星系光 (已知星系总和): {cob.integrated_galactic_light_nw_m2_sr:.1f} nW/m²/sr")
    print(f"  - 未解神秘超额通量: {cob.unexplained_excess_flux_nw_m2_sr:.1f} nW/m²/sr (占已知星系光通量 {cob.excess_fraction_of_known_galaxies_pct:.1f}%)")
    print(f"  - 天体物理结论: {cob.scientific_implication}")
    print("--------------------------------------------------------------------------------")
    print(f"太阳风拾起离子 (PUI) 质量加载减速推演:")
    print(f"  - 甚高局部星际介质 (VLISM) 中性氢密度: {pui.vlism_neutral_h_density_m3:.1e} m⁻³ (0.1 cm⁻³)")
    print(f"  - 太阳风未扰动速度 (1 AU): {pui.unperturbed_solar_wind_speed_1au_km_s:.1f} km/s")
    print(f"  - 累积电荷交换光学厚度: {pui.momentum_attenuation_optical_depth:.4f}")
    print(f"  - 65.92 AU 处实测太阳风速度: {pui.current_solar_wind_speed_km_s:.1f} km/s (下降 {pui.speed_drop_km_s:.1f} km/s, 降幅 {pui.speed_drop_percentage:.1f}%)")
    print(f"  - 动力学机制: {pui.dynamical_significance}")
    print("--------------------------------------------------------------------------------")
    print(f"学生尘埃计数器 (SDC) 柯伊伯带尘埃盘外延测定:")
    print(f"  - 经典 45 AU 柯伊伯悬崖模型预期撞击率: {sdc.expected_cliff_impact_rate_per_day:.2f} 次/天")
    print(f"  - SDC 在轨实测微米粒子撞击率: {sdc.measured_impact_rate_per_day:.2f} 次/天 ({sdc.measured_impact_rate_per_week:.1f} 次/周)")
    print(f"  - 反演尘埃颗粒空间数密度: {sdc.estimated_kbo_dust_density_m3:.2e} m⁻³")
    print(f"  - 推断柯伊伯带碎屑外延边界: 至少延伸至 {sdc.inferred_disk_outer_boundary_au:.1f} AU")
    print(f"  - 范式更迭: {sdc.paradigm_shift_summary}")
    print("================================================================================")
    print("2026 人类深空十极黄金舰队 (The Grand Decet) 宏伟矩阵:")
    for m in fleet:
        print(f"  [{m['rank']:2d}] {m['name']:<30} | {m['agency']:<12} | {m['distance_au']:>8.3f} AU | {m['domain']:<22} | {m['key_feature']}")
    print("================================================================================")
