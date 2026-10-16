"""
欧几里得空间望远镜 (Euclid Space Telescope) 日地 L2 晕轨道天体力学、
全碳化硅 (SiC) 柯尔施光学系统、6.09 亿像素 VIS 弱引力透镜宇宙剪切、
NISP 近红外重子声学振荡 (BAO) 与 2026 人类深空二十二极黄金舰队 (The Grand Duovigintet) 全景推演测试集
"""

import sys
from pathlib import Path
import pytest
import math

scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from euclid_dark_universe_weak_lensing_engine import (
    get_sel2_orbit_dynamics,
    get_sic_optics_spec,
    get_detector_instruments_matrix,
    get_cosmology_probes_and_dark_energy,
    get_survey_progress_and_telemetry,
    get_jwst_euclid_l2_duality,
    get_grand_duovigintet_fleet,
)


def test_sel2_orbit_dynamics():
    """测试日地第二拉格朗日点 (SEL2) 与 Euclid 晕轨道天体力学"""
    sel2 = get_sel2_orbit_dynamics()

    # L2 地心距离应在 149 万 ~ 151 万公里之间 (~0.01 AU)
    assert 1490000.0 < sel2["r_l2_km"] < 1510000.0
    assert 0.0099 < sel2["r_l2_au"] < 0.0101
    assert 1.0099 < sel2["r_helio_au"] < 1.0102

    # 单向光时在 4.9 ~ 5.1 秒之间，往返在 9.8 ~ 10.2 秒之间
    assert 4.9 < sel2["one_way_light_time_s"] < 5.1
    assert 9.8 < sel2["round_trip_light_time_s"] < 10.2

    # Halo 轨道周期约 180 天
    assert sel2["halo_period_days"] == 180.0

    # 避阴影判据: 离轴垂直距离必须大幅超越半影半径 (安全系数 > 20x)
    assert sel2["is_eclipse_free"] is True
    assert sel2["eclipse_safety_margin"] > 30.0


def test_sic_optics_spec():
    """测试全碳化硅 (SiC) TMA 望远镜光学与材料物理特性"""
    optics = get_sic_optics_spec()

    # 口径 1.2m，焦距 24.5m，光圈 f/20.4 左右
    assert optics["diameter_m"] == 1.20
    assert optics["effective_collecting_area_m2"] == 1.00
    assert optics["focal_length_m"] == 24.50
    assert 20.0 < optics["f_number"] < 21.0

    # SiC 材料力学: 杨氏模量 420 GPa，密度 3.15 g/cm³，比刚度 > 130 GPa*cm³/g
    assert optics["young_modulus_gpa"] == 420.0
    assert optics["density_g_cm3"] == 3.15
    assert optics["specific_stiffness_gpa_cm3_g"] > 130.0

    # 超低热膨胀系数 CTE ~ 2.2e-6 K^-1
    assert optics["cte_k_inv"] == 2.20e-6

    # 800nm 衍射极限 ~ 0.168"，实测 PSF FWHM < 0.18"
    assert 0.16 < optics["theta_diff_arcsec"] < 0.18
    assert optics["measured_psf_fwhm_arcsec"] < 0.18

    # 二色分光波段划分
    assert optics["vis_band_nm"] == (550.0, 900.0)
    assert optics["nisp_band_nm"] == (920.0, 2020.0)


def test_detector_instruments_matrix():
    """测试 VIS (可见光) 与 NISP (近红外) 两大科学载荷工程矩阵"""
    det = get_detector_instruments_matrix()

    # VIS 相机: 36 块 CCD，总像素超过 6 亿 (609 Mpix)
    vis = det["vis"]
    assert vis["total_ccds"] == 36
    assert vis["megapixels"] > 600.0
    assert vis["pixel_scale_arcsec"] == 0.101
    assert vis["fov_deg2"] == 0.53
    assert vis["limiting_mag_5sigma"] >= 24.5
    assert vis["multiplicative_bias_target"] <= 2.0e-3
    assert vis["additive_bias_target"] <= 1.0e-4

    # NISP 光谱与光度计: 16 块 H2RG，总像素超过 65 Mpix
    nisp = det["nisp"]
    assert nisp["total_detectors"] == 16
    assert nisp["megapixels"] > 65.0
    assert nisp["pixel_scale_arcsec"] == 0.300
    assert len(nisp["photo_bands"]) == 3
    assert nisp["grism_band_nm"] == (1250.0, 1850.0)
    assert nisp["grism_spectral_resolution"] == 450.0
    assert nisp["ha_redshift_range"] == (0.9, 1.8)
    assert nisp["spec_z_accuracy"] <= 0.001

    # 综合焦平面总像素规模突破 6.7 亿
    assert det["combined_megapixels"] > 670.0


def test_cosmology_probes_and_dark_energy():
    """测试弱引力透镜宇宙剪切与重子声学振荡 (BAO) 宇宙学模型"""
    cosmo = get_cosmology_probes_and_dark_energy()

    # 弱透镜星系样本 15 亿，统计增益 > 38000x
    assert cosmo["total_target_galaxies_weak_lensing"] == 1.50e9
    assert cosmo["statistical_snr_gain"] > 38000.0
    assert cosmo["shear_mean_error"] < 1.0e-5

    # BAO 标准尺 147.5 Mpc，光谱星系 3500 万
    assert cosmo["sound_horizon_mpc"] == 147.5
    assert cosmo["total_target_galaxies_bao"] == 3.50e7

    # 暗能量状态方程约束与品质因数
    assert cosmo["w0_lcdm"] == -1.00
    assert cosmo["wa_lcdm"] == 0.00
    assert cosmo["expected_fom"] >= 400.0
    assert cosmo["expected_sigma_w0"] < 0.02
    assert cosmo["expected_sigma_wa"] < 0.08


def test_survey_progress_and_telemetry():
    """测试 2026-10-17 巡天进度与科学数据下行链路"""
    prog = get_survey_progress_and_telemetry("2026-10-17T07:25:00Z")

    # 空间在轨时间突破 1200 天 (3.2+ 年)
    assert prog["total_days_in_space"] > 1200.0
    assert prog["survey_days"] > 970.0

    # 巡天目标天区 15,000 deg² (全天 36% 以上)
    assert prog["target_wide_survey_deg2"] == 15000.0
    assert 35.0 < prog["sky_fraction_pct"] < 38.0

    # 截至今日完成度在 40% ~ 50% 之间 (接近半程)
    assert 40.0 < prog["completion_pct"] < 50.0
    assert prog["completed_wide_survey_deg2"] > 6000.0
    assert prog["galaxies_observed_so_far"] > 7.0e8

    # 科学数据流: 每日 850 Gbits (~106 GB)，K 波段 73 Mbps 下行裕量充足
    assert prog["daily_science_data_gbits"] == 850.0
    assert 100.0 < prog["daily_science_data_gbytes"] < 115.0
    assert prog["downlink_freq_ghz"] == 26.0
    assert prog["downlink_data_rate_mbps"] == 73.0
    assert prog["daily_contact_hours"] == 4.0
    assert prog["downlink_margin_pct"] > 15.0


def test_jwst_euclid_l2_duality():
    """测试日地 L2 拉格朗日点双极对偶：JWST vs Euclid"""
    duality = get_jwst_euclid_l2_duality()

    # 同居日地 L2
    assert duality["distance_from_earth_km"] == 1500000.0
    assert duality["light_time_delay_s"] == 5.0

    # Euclid 视场是 JWST NIRCam 的 190 倍以上
    assert duality["fov_ratio_euclid_to_jwst"] > 190.0

    # 口径与探测深度对比
    assert duality["jwst"]["aperture_m"] == 6.50
    assert duality["euclid"]["aperture_m"] == 1.20
    assert duality["jwst"]["limiting_mag_ab"] > duality["euclid"]["limiting_mag_ab"]


def test_grand_duovigintet_fleet_structure():
    """测试 2026 人类深空二十二极黄金舰队 (The Grand Duovigintet) 完整结构"""
    data = get_grand_duovigintet_fleet()
    fleet = data["fleet"]

    # 严格 22 大深空旗舰
    assert data["fleet_count"] == 22
    assert len(fleet) == 22

    # 验证严格按日心极距降序排列
    for i in range(len(fleet) - 1):
        assert (
            fleet[i]["helio_dist_au"] >= fleet[i + 1]["helio_dist_au"]
        ), f"Fleet order violation at {fleet[i]['name']} vs {fleet[i+1]['name']}"

    # 验证关键旗舰在编
    names = [f["name"] for f in fleet]
    assert any("旅行者 1 号" in n for n in names)
    assert any("旅行者 2 号" in n for n in names)
    assert any("新视野号" in n for n in names)
    assert any("朱诺号" in n for n in names)
    assert any("JUICE" in n for n in names)
    assert any("欧罗巴快船" in n for n in names)
    assert any("露西号" in n for n in names)
    assert any("灵神星" in n for n in names)
    assert any("好奇号" in n for n in names)
    assert any("毅力号" in n for n in names)
    assert any("天问一号" in n for n in names)
    assert any("赫拉号" in n for n in names)
    assert any("隼鸟二号" in n for n in names)
    assert any("OSIRIS-APEX" in n for n in names)
    assert any("JWST" in n for n in names)
    assert any("Euclid" in n for n in names)
    assert any("天问二号" in n for n in names)
    assert any("鹊桥二号" in n for n in names)
    assert any("嫦娥四号" in n for n in names)
    assert any("贝皮可伦坡" in n for n in names)
    assert any("太阳轨道" in n for n in names)
    assert any("帕克" in n for n in names)


def test_grand_duovigintet_extremes():
    """测试二十二极黄金舰队极端物理跨度"""
    data = get_grand_duovigintet_fleet()

    # 日心极距跨度超 3700 倍 (173.22 AU vs 0.046 AU)
    assert data["helio_dist_span_ratio"] > 3700.0

    # 太阳辐射能流跨度超 1400 万倍
    assert data["solar_flux_drop_ratio"] > 1.4e7
