"""
欧几里得空间望远镜 (Euclid Space Telescope) 日地 L2 晕轨道天体力学、
全碳化硅 (SiC) 柯尔施光学系统、6.09 亿像素 VIS 弱引力透镜宇宙剪切、
NISP 近红外重子声学振荡 (BAO) 与 2026 人类深空二十二极黄金舰队 (The Grand Duovigintet) 全景推演引擎

核心物理与工程建模：
1. 日地第二拉格朗日点 (SEL2) 晕轨道 (Halo Orbit) 天体力学与光行时延迟 (150 万公里 / 5.0 秒光时 / 180 天周期 / 零日食避阴影判据)；
2. 全碳化硅 (Silicon Carbide / SiC) 柯尔施三镜消像差 (TMA) 光学系统 (1.2m 口径、高比刚度 133.3 GPa·cm³/g、超低热膨胀 CTE 2.2e-6 K⁻¹、衍射极限 0.168"、PSF < 0.18"、二色分光双通道同步成像)；
3. 两大致密科学相机阵列工程矩阵：
   - VIS (Visible Instrument): 36 块 e2v CCD273-84 阵列，609 Megapixels (6.09 亿像素)，0.53 deg² 巨视场，0.101"/px，测定 15 亿星系弱透镜椭圆率，乘性偏差 m < 2e-3；
   - NISP (Near-Infrared Spectrometer and Photometer): 16 块 H2RG HgCdTe 红外阵列，67.1 Megapixels，Y/J/H 宽带测光与无缝红外光栅光谱 (1250~1850 nm)，测定 3500 万星系 Hα 光谱红移 (z=0.9~1.8)，红移精度 σ_z / (1+z) <= 0.001；
4. 宇宙学双重探针：弱引力透镜宇宙剪切 (Cosmic Shear γ) 与重子声学振荡 (BAO 147.5 Mpc 标准尺)，阿尔科克-帕钦斯基效应与暗能量状态方程 w(a) = w0 + wa(1-a) 品质因数 (FoM > 400)；
5. 2026-10-17 巡天进度与数据流拓扑：在轨 1204 天，宽场巡天完成 6,820 deg² (45.47% 近半程突破)，捕获 7.65 亿星系，K 波段 26 GHz 以 73 Mbps 下行每日 850 Gbits 科学数据；
6. 日地 L2 宇宙学双极对偶大交响：JWST (红外手术刀 0.0027 deg² 深剖析) vs Euclid (暗宇宙广角制图师 0.53 deg² 宏观 3D 宇宙网扫描，视场达 JWST 的 196.7 倍)；
7. 2026 人类深空二十二极黄金舰队 (The Grand Duovigintet) 宏伟时空矩阵与极端物理对偶全景 (涵盖从旅行者 1 号 173.22 AU 至帕克探测器 0.046 AU 的全天域 22 大深空支柱)。
"""

import math
from datetime import datetime, timezone

# 物理与天文基准常数
C_LIGHT = 299792.458  # 真空光速 (km/s)
AU_KM = 149597870.7  # 1 天文单位 (km)
G_CONST = 6.67430e-11  # 万有引力常数 (m^3 / (kg * s^2))
M_SUN = 1.98847e30  # 太阳质量 (kg)
M_EARTH = 5.9722e24  # 地球质量 (kg)
R_EARTH_KM = 6378.137  # 地球赤道半径 (km)
R_SUN_KM = 696340.0  # 太阳半径 (km)


def get_sel2_orbit_dynamics():
    """
    计算日地第二拉格朗日点 (SEL2) 与 Euclid 晕轨道 (Halo Orbit) 天体力学参数
    """
    mu = M_EARTH / (M_SUN + M_EARTH)
    # L2 距离地球质心理论近似解: r_L2 = R * (mu / 3)^(1/3)
    r_l2_km = AU_KM * math.pow(mu / 3.0, 1.0 / 3.0)
    r_l2_au = r_l2_km / AU_KM
    r_helio_au = 1.0 + r_l2_au

    # 单向通信光行时延迟与往返光时
    one_way_light_time_s = r_l2_km / C_LIGHT
    round_trip_light_time_s = 2.0 * one_way_light_time_s

    # Euclid Halo 轨道参数
    halo_period_days = 180.0
    ax_km = 200000.0  # 日地连线方向半振幅 (km)
    ay_km = 400000.0  # 面内横向半振幅 (km)
    az_km = 400000.0  # 面外垂直黄道半振幅 (km)
    orbit_radius_perp_km = math.sqrt(ay_km**2 + az_km**2)

    # 地球半影在 L2 处的截面半径: R_pen = R_earth + r_l2 * (R_sun - R_earth) / AU_KM
    penumbra_radius_l2_km = R_EARTH_KM + r_l2_km * (R_SUN_KM - R_EARTH_KM) / AU_KM
    # 避阴影安全系数 (离轴距离 / 半影半径)
    eclipse_safety_margin = orbit_radius_perp_km / penumbra_radius_l2_km

    return {
        "mu": mu,
        "r_l2_km": round(r_l2_km, 1),
        "r_l2_au": round(r_l2_au, 6),
        "r_helio_au": round(r_helio_au, 6),
        "one_way_light_time_s": round(one_way_light_time_s, 4),
        "round_trip_light_time_s": round(round_trip_light_time_s, 4),
        "halo_period_days": halo_period_days,
        "ax_km": ax_km,
        "ay_km": ay_km,
        "az_km": az_km,
        "orbit_radius_perp_km": round(orbit_radius_perp_km, 1),
        "penumbra_radius_l2_km": round(penumbra_radius_l2_km, 1),
        "eclipse_safety_margin": round(eclipse_safety_margin, 2),
        "is_eclipse_free": orbit_radius_perp_km > penumbra_radius_l2_km,
    }


def get_sic_optics_spec():
    """
    计算全碳化硅 (Silicon Carbide / SiC) TMA 望远镜光学与材料物理特性
    """
    diameter_m = 1.20
    effective_collecting_area_m2 = 1.00  # 扣除次镜遮挡后的净有效采光面积
    focal_length_m = 24.50
    f_number = focal_length_m / diameter_m  # f/20.42

    # 材料力学与热物理参数
    young_modulus_gpa = 420.0  # 弹性杨氏模量 (GPa)
    density_g_cm3 = 3.15  # 密度 (g/cm^3)
    specific_stiffness = young_modulus_gpa / density_g_cm3  # 比刚度 (GPa*cm^3/g)
    cte_k_inv = 2.20e-6  # 热膨胀系数 (K^-1)
    thermal_conductivity_w_m_k = 180.0  # 热导率 (W/(m*K))

    # 衍射极限角分辨率 (800 nm 标称波长)
    lambda_ref_m = 800.0e-9
    theta_diff_rad = 1.22 * lambda_ref_m / diameter_m
    theta_diff_arcsec = theta_diff_rad * (180.0 / math.pi) * 3600.0
    measured_psf_fwhm_arcsec = 0.175  # 实测点扩散函数半高全宽 (< 0.18")

    # 二色分光系统 (Dichroic Beam Splitter)
    vis_band_nm = (550.0, 900.0)
    nisp_band_nm = (920.0, 2020.0)

    return {
        "diameter_m": diameter_m,
        "effective_collecting_area_m2": effective_collecting_area_m2,
        "focal_length_m": focal_length_m,
        "f_number": round(f_number, 2),
        "young_modulus_gpa": young_modulus_gpa,
        "density_g_cm3": density_g_cm3,
        "specific_stiffness_gpa_cm3_g": round(specific_stiffness, 2),
        "cte_k_inv": cte_k_inv,
        "thermal_conductivity_w_m_k": thermal_conductivity_w_m_k,
        "theta_diff_arcsec": round(theta_diff_arcsec, 4),
        "measured_psf_fwhm_arcsec": measured_psf_fwhm_arcsec,
        "vis_band_nm": vis_band_nm,
        "nisp_band_nm": nisp_band_nm,
    }


def get_detector_instruments_matrix():
    """
    计算 VIS (可见光) 与 NISP (近红外) 两大科学载荷工程阵列矩阵
    """
    # 1. VIS 仪器 (Visible Instrument)
    vis_num_ccd_x = 6
    vis_num_ccd_y = 6
    vis_total_ccds = vis_num_ccd_x * vis_num_ccd_y  # 36 块 CCD
    vis_ccd_pixels_x = 4096
    vis_ccd_pixels_y = 4132
    vis_total_pixels = vis_total_ccds * vis_ccd_pixels_x * vis_ccd_pixels_y
    vis_megapixels = vis_total_pixels / 1.0e6
    vis_pixel_pitch_um = 12.0
    vis_pixel_scale_arcsec = 0.101  # 角分辨率 (arcsec/pixel)
    vis_fov_deg2 = 0.53  # 净科学有效视场 (deg^2)
    vis_limiting_mag_5sigma = 24.5  # 5-sigma 点源极限星等
    vis_multiplicative_bias_target = 2.0e-3  # 椭圆率乘性偏差指标 |m| < 2e-3
    vis_additive_bias_target = 1.0e-4  # 椭圆率加性偏差指标 |c| < 1e-4

    # 2. NISP 仪器 (Near-Infrared Spectrometer and Photometer)
    nisp_num_detector_x = 4
    nisp_num_detector_y = 4
    nisp_total_detectors = nisp_num_detector_x * nisp_num_detector_y  # 16 块 H2RG
    nisp_detector_pixels_x = 2048
    nisp_detector_pixels_y = 2048
    nisp_total_pixels = nisp_total_detectors * nisp_detector_pixels_x * nisp_detector_pixels_y
    nisp_megapixels = nisp_total_pixels / 1.0e6
    nisp_pixel_pitch_um = 18.0
    nisp_pixel_scale_arcsec = 0.300
    nisp_fov_deg2 = 0.53
    nisp_photo_bands = ["Y (920-1146 nm)", "J (1146-1372 nm)", "H (1372-2000 nm)"]
    nisp_grism_band_nm = (1250.0, 1850.0)
    nisp_grism_spectral_resolution = 450.0  # R = lambda / delta_lambda
    nisp_ha_redshift_range = (0.9, 1.8)  # 测定 H-alpha 发射线红移窗口
    nisp_spec_z_accuracy = 0.001  # sigma_z / (1 + z) <= 0.001

    return {
        "vis": {
            "total_ccds": vis_total_ccds,
            "total_pixels": vis_total_pixels,
            "megapixels": round(vis_megapixels, 1),
            "pixel_pitch_um": vis_pixel_pitch_um,
            "pixel_scale_arcsec": vis_pixel_scale_arcsec,
            "fov_deg2": vis_fov_deg2,
            "limiting_mag_5sigma": vis_limiting_mag_5sigma,
            "multiplicative_bias_target": vis_multiplicative_bias_target,
            "additive_bias_target": vis_additive_bias_target,
        },
        "nisp": {
            "total_detectors": nisp_total_detectors,
            "total_pixels": nisp_total_pixels,
            "megapixels": round(nisp_megapixels, 1),
            "pixel_pitch_um": nisp_pixel_pitch_um,
            "pixel_scale_arcsec": nisp_pixel_scale_arcsec,
            "fov_deg2": nisp_fov_deg2,
            "photo_bands": nisp_photo_bands,
            "grism_band_nm": nisp_grism_band_nm,
            "grism_spectral_resolution": nisp_grism_spectral_resolution,
            "ha_redshift_range": nisp_ha_redshift_range,
            "spec_z_accuracy": nisp_spec_z_accuracy,
        },
        "combined_megapixels": round(vis_megapixels + nisp_megapixels, 1),
    }


def get_cosmology_probes_and_dark_energy():
    """
    计算弱引力透镜宇宙剪切 (Cosmic Shear) 与重子声学振荡 (BAO) 双重宇宙学探针模型
    """
    # 弱透镜统计参数
    total_target_galaxies_weak_lensing = 1.50e9  # 15 亿星系
    intrinsic_ellipticity_dispersion = 0.30  # 内禀椭圆率色散 sigma_eps
    typical_cosmic_shear = 0.015  # 典型宇宙剪切量 gamma ~ 1.5%
    # 全局平均剪切统计信噪比提升倍数 sqrt(N_gal)
    statistical_snr_gain = math.sqrt(total_target_galaxies_weak_lensing)
    shear_mean_error = intrinsic_ellipticity_dispersion / statistical_snr_gain

    # BAO 标准尺参数
    sound_horizon_mpc = 147.5  # 声视界标尺 r_s (Mpc)
    total_target_galaxies_bao = 3.50e7  # 3500 万光谱红移星系

    # 暗能量状态方程参数化: w(a) = w0 + wa * (1 - a)
    # Lambda-CDM 基准值
    w0_lcdm = -1.00
    wa_lcdm = 0.00
    # Euclid 预计品质因数 (Figure of Merit: FoM = 1 / sqrt(det(Cov(w0, wa))))
    expected_fom = 450.0  # FoM > 400
    expected_sigma_w0 = 0.012  # w0 约束精度 < 1.5%
    expected_sigma_wa = 0.065  # wa 约束精度 < 0.08

    return {
        "total_target_galaxies_weak_lensing": total_target_galaxies_weak_lensing,
        "intrinsic_ellipticity_dispersion": intrinsic_ellipticity_dispersion,
        "typical_cosmic_shear": typical_cosmic_shear,
        "statistical_snr_gain": round(statistical_snr_gain, 1),
        "shear_mean_error": shear_mean_error,
        "sound_horizon_mpc": sound_horizon_mpc,
        "total_target_galaxies_bao": total_target_galaxies_bao,
        "w0_lcdm": w0_lcdm,
        "wa_lcdm": wa_lcdm,
        "expected_fom": expected_fom,
        "expected_sigma_w0": expected_sigma_w0,
        "expected_sigma_wa": expected_sigma_wa,
    }


def get_survey_progress_and_telemetry(current_time_str="2026-10-17T07:25:00Z"):
    """
    计算截至 2026-10-17 Euclid 巡天进度、空间几何拓扑与深空通信数据流
    """
    launch_time = datetime(2023, 7, 1, 15, 12, tzinfo=timezone.utc)
    survey_start_time = datetime(2024, 2, 14, 0, 0, tzinfo=timezone.utc)
    now = datetime.fromisoformat(current_time_str.replace("Z", "+00:00"))

    total_days_in_space = (now - launch_time).total_seconds() / 86400.0
    survey_days = (now - survey_start_time).total_seconds() / 86400.0

    # 巡天面积与天球比例
    full_sky_deg2 = 4.0 * math.pi * ((180.0 / math.pi) ** 2)  # 41,252.96 deg^2
    target_wide_survey_deg2 = 15000.0  # 宽场巡天目标 (deg^2)
    target_deep_fields_deg2 = 53.0  # 深度场目标 (deg^2)
    sky_fraction_pct = (target_wide_survey_deg2 / full_sky_deg2) * 100.0

    # 截至 2026-10-17 巡天完成度推演
    # 平均日均净覆盖约 7.0 ~ 9.0 deg^2 (考虑校准与深度场)
    completed_wide_survey_deg2 = 6820.0
    completion_pct = (completed_wide_survey_deg2 / target_wide_survey_deg2) * 100.0
    remaining_wide_survey_deg2 = target_wide_survey_deg2 - completed_wide_survey_deg2

    # 捕获星系估算
    galaxies_observed_so_far = 7.65e8  # 约 7.65 亿个星系

    # 科学数据流与深空链路
    daily_science_data_gbits = 850.0  # 每日压缩科学数据 (Gbits)
    daily_science_data_gbytes = daily_science_data_gbits / 8.0  # 约 106.25 GB
    downlink_freq_ghz = 26.0  # K 波段 (26 GHz)
    downlink_data_rate_mbps = 73.0  # 下行传输速率 (Mbps)
    daily_contact_hours = 4.0  # 每日地面站联系窗口 (小时)
    contact_seconds = daily_contact_hours * 3600.0
    daily_downlink_capacity_gbits = (downlink_data_rate_mbps * contact_seconds) / 1000.0
    downlink_margin_pct = (
        (daily_downlink_capacity_gbits - daily_science_data_gbits) / daily_science_data_gbits
    ) * 100.0

    return {
        "launch_date": "2023-07-01",
        "survey_start_date": "2024-02-14",
        "total_days_in_space": round(total_days_in_space, 1),
        "survey_days": round(survey_days, 1),
        "full_sky_deg2": round(full_sky_deg2, 2),
        "target_wide_survey_deg2": target_wide_survey_deg2,
        "sky_fraction_pct": round(sky_fraction_pct, 2),
        "completed_wide_survey_deg2": completed_wide_survey_deg2,
        "completion_pct": round(completion_pct, 2),
        "remaining_wide_survey_deg2": round(remaining_wide_survey_deg2, 1),
        "galaxies_observed_so_far": galaxies_observed_so_far,
        "daily_science_data_gbits": daily_science_data_gbits,
        "daily_science_data_gbytes": round(daily_science_data_gbytes, 2),
        "downlink_freq_ghz": downlink_freq_ghz,
        "downlink_data_rate_mbps": downlink_data_rate_mbps,
        "daily_contact_hours": daily_contact_hours,
        "daily_downlink_capacity_gbits": round(daily_downlink_capacity_gbits, 1),
        "downlink_margin_pct": round(downlink_margin_pct, 2),
    }


def get_jwst_euclid_l2_duality():
    """
    计算日地第二拉格朗日点 (SEL2) 宇宙学双极对偶：JWST (红外手术刀) vs Euclid (暗宇宙广角制图师)
    """
    jwst_aperture_m = 6.50
    euclid_aperture_m = 1.20

    # 视场对比 (FOV)
    jwst_nircam_fov_arcmin2 = 9.7  # NIRCam 视场约 9.7 平方角分
    jwst_nircam_fov_deg2 = jwst_nircam_fov_arcmin2 / 3600.0  # 约 0.002694 deg^2
    euclid_fov_deg2 = 0.53  # 约 1908 平方角分

    fov_ratio_euclid_to_jwst = euclid_fov_deg2 / jwst_nircam_fov_deg2

    # 巡天范式与物理目标
    return {
        "location": "Sun-Earth Lagrange Point 2 (SEL2)",
        "distance_from_earth_km": 1500000.0,
        "light_time_delay_s": 5.0,
        "jwst": {
            "name": "James Webb Space Telescope (JWST)",
            "role": "Cosmic Scalpel / Targeted Deep Physics",
            "aperture_m": jwst_aperture_m,
            "primary_mirror_material": "Gold-coated Beryllium (18 hexagonal segments)",
            "nircam_fov_deg2": round(jwst_nircam_fov_deg2, 6),
            "limiting_mag_ab": 31.5,
            "target_redshift_max": "z > 14",
            "primary_focus": "First stars, galaxy assembly, AGN, exoplanet atmospheres",
        },
        "euclid": {
            "name": "Euclid Space Telescope",
            "role": "Cosmic Web Cartographer / Macro Statistical Survey",
            "aperture_m": euclid_aperture_m,
            "primary_mirror_material": "Sintered Silicon Carbide (SiC TMA)",
            "fov_deg2": euclid_fov_deg2,
            "limiting_mag_ab": 24.5,
            "target_redshift_max": "z ~ 2.0 (10 billion years lookback)",
            "primary_focus": "Dark energy equation of state, dark matter cosmic shear, BAO expansion",
        },
        "fov_ratio_euclid_to_jwst": round(fov_ratio_euclid_to_jwst, 1),
    }


def get_grand_duovigintet_fleet():
    """
    构建 2026 人类深空二十二极黄金舰队 (The Grand Duovigintet) 宏伟时空矩阵
    按日心极距降序严密排列
    """
    fleet = [
        {
            "rank": 1,
            "name": "旅行者 1 号 (Voyager 1)",
            "agency": "NASA",
            "helio_dist_au": 173.22,
            "role": "恒星际最远深空边界极 (1 光日冲线倒计时 32 天, 2.7 K 极寒星际)",
        },
        {
            "rank": 2,
            "name": "旅行者 2 号 (Voyager 2)",
            "agency": "NASA",
            "helio_dist_au": 144.26,
            "role": "恒星际南天天球星际极 (20 光时冲线倒计时今日仅剩 17 小时跨越)",
        },
        {
            "rank": 3,
            "name": "新视野号 (New Horizons)",
            "agency": "NASA",
            "helio_dist_au": 65.92,
            "role": "柯伊伯带双曲线逃逸极 (COB 绝尘暗夜超额光, PUI 减速 17%)",
        },
        {
            "rank": 4,
            "name": "朱诺号 (Juno)",
            "agency": "NASA",
            "helio_dist_au": 5.20,
            "role": "木星极轨高能辐射极 (180kg 钛金保险库, 掠木 57.8 km/s, 弱光光伏)",
        },
        {
            "rank": 5,
            "name": "木星冰月探测器 (JUICE)",
            "agency": "ESA",
            "helio_dist_au": 5.20,
            "role": "巨行星卫星内禀磁层极 (探秘木卫三深海, 85m² 弱光光伏, 2.3 年共振巡航)",
        },
        {
            "rank": 6,
            "name": "欧罗巴快船 (Europa Clipper)",
            "agency": "NASA",
            "helio_dist_au": 5.20,
            "role": "外行星木卫二深海生命极 (MEGA 地球引力弹弓倒计时 47 天)",
        },
        {
            "rank": 7,
            "name": "露西号 (Lucy)",
            "agency": "NASA",
            "helio_dist_au": 5.04,
            "role": "木星特洛伊群原始微行星极 (7.3m UltraFlex 折叠帆板, 发射五周年)",
        },
        {
            "rank": 8,
            "name": "灵神星探测器 (Psyche)",
            "agency": "NASA",
            "helio_dist_au": 2.042,
            "role": "金属核心微行星极 (SPT-140 霍尔电推, DSOC 激光光子链路百倍跃迁)",
        },
        {
            "rank": 9,
            "name": "好奇号 (Curiosity)",
            "agency": "NASA",
            "helio_dist_au": 1.524,
            "role": "火星盖尔撞击坑与夏普山麓极 (14 年漫游 33.6km, 盖迪兹谷纯单质硫突破, MMRTG)",
        },
        {
            "rank": 10,
            "name": "毅力号 (Perseverance)",
            "agency": "NASA",
            "helio_dist_au": 1.524,
            "role": "火星地表古湖泊与40亿年原生古地壳原位探测极 (翻越500m环壁冲入狂野西部、生成式AI导航与33支岩芯密封)",
        },
        {
            "rank": 11,
            "name": "天问一号环绕器 (Tianwen-1)",
            "agency": "CNSA",
            "helio_dist_au": 1.524,
            "role": "火星极轨全域遥感极 (76m 全球彩色正射图, MOSIR 雷达探冰, 3I/ATLAS 星际观测, 3.5 TB 数据公开)",
        },
        {
            "rank": 12,
            "name": "赫拉号 (Hera)",
            "agency": "ESA",
            "helio_dist_au": 1.304,
            "role": "双小行星微重力伴飞极 (BRM-1 93分钟主减速点火圆满达成)",
        },
        {
            "rank": 13,
            "name": "隼鸟二号 (Hayabusa2# / SHARP)",
            "agency": "JAXA",
            "helio_dist_au": 1.120,
            "role": "十米级超快自转微小行星极 (744m Torifune 掠飞后巡航, 1998 KY26 极区着陆, 490倍离心力对抗, μ10 离子电推)",
        },
        {
            "rank": 14,
            "name": "OSIRIS-APEX",
            "agency": "NASA",
            "helio_dist_au": 1.010,
            "role": "毁神星伴飞与极限热控无花果叶极 (4倍太阳热流, 2029 掠地 1153km 减速 99%, STIR 羽流吹扫)",
        },
        {
            "rank": 15,
            "name": "詹姆斯·韦伯望远镜 (JWST)",
            "agency": "NASA/ESA/CSA",
            "helio_dist_au": 1.010,
            "role": "日地 L2 虚空深空红外极 (6.5m 铍金镜, 300 K 隔热 6.7 K 制冷, 0.077'' 捕获 z > 14 原初星系)",
        },
        {
            "rank": 16,
            "name": "欧几里得望远镜 (Euclid)",
            "agency": "ESA",
            "helio_dist_au": 1.010,
            "role": "日地 L2 暗宇宙与大尺度三维宇宙网宏观极 (1.2m SiC TMA, 0.53 deg² 巨视场, 6.09亿像素 VIS + 6500万像素 NISP, 测定暗能量方程 w(a))",
        },
        {
            "rank": 17,
            "name": "天问二号 (Tianwen-2)",
            "agency": "CNSA",
            "helio_dist_au": 1.001,
            "role": "地球准卫星共轨采样与彗星双跃迁极 (28分钟自旋 50倍离心力对抗采样, 布鲁诺撞击坑月球基岩)",
        },
        {
            "rank": 18,
            "name": "鹊桥二号 (Queqiao-2)",
            "agency": "CNSA",
            "helio_dist_au": 1.000,
            "role": "地月空间与月球南极/月背冻结中继极 (4.2米伞状天线、月瘤摄动抑制、嫦娥六/七/八号生命线)",
        },
        {
            "rank": 19,
            "name": "嫦娥四号与玉兔二号 (Chang'e-4 / Yutu-2)",
            "agency": "CNSA",
            "helio_dist_au": 1.000,
            "role": "月背南极-艾特肯盆地原位巡视极 (人类唯一月背软着陆、96月昼7.79年超长巡视、-180°C钚-238 RHU核热源冬眠、月背射电静默区)",
        },
        {
            "rank": 20,
            "name": "贝皮可伦坡 (BepiColombo)",
            "agency": "ESA/JAXA",
            "helio_dist_au": 0.387,
            "role": "太阳最深引力势能阱水星捕获极 (-1405 MJ/kg MOI 盲操倒计时 35 天)",
        },
        {
            "rank": 21,
            "name": "太阳轨道飞行器 (Solar Orbiter)",
            "agency": "ESA/NASA",
            "helio_dist_au": 0.280,
            "role": "黄道外高倾角极区成像与日冕加热极 (金星 4:3 借力 24°, 520°C 骨黑隔热罩, 微耀斑篝火, 倒计时 68 天平安夜 VGA5)",
        },
        {
            "rank": 22,
            "name": "帕克太阳探测器 (Parker Solar Probe)",
            "agency": "NASA",
            "helio_dist_au": 0.046,
            "role": "恒星日冕极高温炼狱原位极 (192 km/s 人类极速, 1400°C 防热罩, P30 倒计时 46 天)",
        },
    ]

    r_max = fleet[0]["helio_dist_au"]
    r_min = fleet[-1]["helio_dist_au"]
    span_ratio = r_max / r_min
    flux_ratio = (r_max / r_min) ** 2

    return {
        "fleet_count": len(fleet),
        "fleet": fleet,
        "helio_dist_span_ratio": round(span_ratio, 2),
        "solar_flux_drop_ratio": round(flux_ratio, 1),
    }


if __name__ == "__main__":
    sel2 = get_sel2_orbit_dynamics()
    optics = get_sic_optics_spec()
    det = get_detector_instruments_matrix()
    cosmo = get_cosmology_probes_and_dark_energy()
    prog = get_survey_progress_and_telemetry()
    duality = get_jwst_euclid_l2_duality()
    fleet = get_grand_duovigintet_fleet()

    print("=== Euclid SEL2 Orbit Dynamics ===")
    print(
        f"L2 Dist: {sel2['r_l2_km']} km ({sel2['r_l2_au']} AU), Helio Dist: {sel2['r_helio_au']} AU"
    )
    print(
        f"Light time: {sel2['one_way_light_time_s']} s (1-way), Eclipse Safety: {sel2['eclipse_safety_margin']}x"
    )

    print("\n=== Silicon Carbide TMA Optics ===")
    print(
        f"Diameter: {optics['diameter_m']} m, Focal length: {optics['focal_length_m']} m (f/{optics['f_number']})"
    )
    print(
        f"SiC Specific stiffness: {optics['specific_stiffness_gpa_cm3_g']} GPa*cm^3/g, PSF: {optics['measured_psf_fwhm_arcsec']}\""
    )

    print("\n=== Detector Matrix ===")
    print(
        f"VIS: {det['vis']['megapixels']} Megapixels (36 CCDs), Pixel scale: {det['vis']['pixel_scale_arcsec']}\"/px"
    )
    print(
        f"NISP: {det['nisp']['megapixels']} Megapixels (16 H2RG), Grism: {det['nisp']['grism_band_nm']} nm"
    )
    print(f"Combined: {det['combined_megapixels']} Megapixels")

    print("\n=== Cosmology & Survey Progress ===")
    print(f"FoM: {cosmo['expected_fom']}, Weak Lensing Galaxies: {cosmo['total_target_galaxies_weak_lensing']:.1e}")
    print(f"Survey Completed: {prog['completed_wide_survey_deg2']} deg^2 ({prog['completion_pct']}%)")
    print(f"Downlink Margin: {prog['downlink_margin_pct']}% at {prog['downlink_data_rate_mbps']} Mbps")

    print("\n=== JWST vs Euclid L2 Duality ===")
    print(f"FOV Ratio (Euclid / JWST): {duality['fov_ratio_euclid_to_jwst']}x")

    print(f"\n=== Grand Duovigintet Fleet: {fleet['fleet_count']} Probes ===")
    print(
        f"Span: {fleet['helio_dist_span_ratio']}x, Flux Drop: {fleet['solar_flux_drop_ratio']:.1e}x"
    )
