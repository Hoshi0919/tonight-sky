"""
单元测试：ExoMars 痕量气体轨道器 (TGO) 在轨 10 周年整（十年锡婚 / Decennial）、
NOMAD 与 ACS 太阳掩星 50 pptv 甲烷检测极限与火星甲烷对立佯谬、
人类首次发现火星氯化氢 (HCl) 气体与同位素水汽逃逸、
FREND 准直超热中子望远镜与水手号大峡谷 40% 水冰绿洲、
火星现役七大功勋金刚 (The Martian Septet) 与深空二十八极黄金舰队 (The Grand Octovigintet / 深空二十八宿)
"""

import math
import datetime
import sys
from pathlib import Path
import pytest

DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR / "scripts"))

from exomars_tgo_atmosphere_water_engine import ExoMarsTGOEngine

@pytest.fixture
def engine():
    # 基准评估历元: 2026-10-18 00:45:00 UTC (08:45:00 CST)
    ref_dt = datetime.datetime(2026, 10, 18, 0, 45, 0, tzinfo=datetime.timezone.utc)
    return ExoMarsTGOEngine(current_dt=ref_dt)

def test_mission_timeline_and_decennial_countdown(engine):
    """
    1. 验证任务时间线与 10 周年锡婚倒计时：
       - 在轨时间超 3,645 天 (~9.99 地球年 / 5.3 火星年)
       - 距 2026-10-19 15:24 UTC 10 周年倒计时处于 48 小时冲线前夕
    """
    tl = engine.compute_mission_timeline()
    assert tl["days_in_orbit"] > 3645.0
    assert 9.95 < tl["years_in_orbit"] < 10.05
    assert 5.2 < tl["mars_years_in_orbit"] < 5.5
    assert tl["total_flight_days"] > 3800.0
    assert 0 < tl["countdown_to_10y_hours"] < 48.0
    assert tl["is_decennial_eve"] is True

def test_orbit_dynamics_and_high_inclination_coverage(engine):
    """
    2. 验证开普勒轨道动力学与绕火公转圈数：
       - 400 km 科学工作轨道圆速度约 3.36 km/s
       - 轨道周期约 118.0 分钟 (1.97 小时)
       - 每日公转约 12.2 圈
       - 累计绕火公转突破 44,000 圈
       - 轨道倾角 74.0° (高倾角大范围覆盖掩星)
    """
    od = engine.compute_orbit_dynamics()
    assert abs(od["orbital_altitude_km"] - 400.0) < 1.0
    assert abs(od["orbital_velocity_kms"] - 3.362) < 0.05
    assert abs(od["period_minutes"] - 118.04) < 0.5
    assert abs(od["period_hours"] - 1.967) < 0.02
    assert abs(od["orbits_per_earth_day"] - 12.20) < 0.1
    assert od["cumulative_orbits"] > 44000.0
    assert od["inclination_deg"] == 74.0

def test_aerobraking_energy_dissipation_and_fuel_savings(engine):
    """
    3. 验证气动减速 (Aerobraking) 物理与燃料节省：
       - 远火点从 98,000 km 压缩至 400 km
       - 节省等效推进剂 Delta-V 超 1200 m/s
       - 节省推进剂超 750 kg
       - 经历 950 余次掠飞，单圈平均消耗动能速度增量 ~1.37 m/s
    """
    ab = engine.compute_aerobraking_physics()
    assert ab["initial_apoapsis_km"] == 98000.0
    assert ab["final_circular_altitude_km"] == 400.0
    assert ab["equivalent_delta_v_saved_ms"] > 1200.0
    assert ab["propellant_saved_kg"] > 750.0
    assert ab["aerobraking_passes"] == 952
    assert 1.0 < ab["avg_delta_v_per_pass_ms"] < 2.0

def test_solar_occultation_path_enhancement_and_tangent_geometry(engine):
    """
    4. 验证太阳掩星几何放大效应：
       - 切向穿透火星大气的有效光程达 548 km
       - 相对垂直天底观测光程放大近 50 倍
    """
    meth = engine.compute_solar_occultation_and_methane_paradox()
    assert 530.0 < meth["tangent_path_length_km"] < 560.0
    assert 45.0 < meth["optical_path_enhancement_factor"] < 55.0

def test_methane_paradox_and_pptv_detection_limit(engine):
    """
    5. 验证火星甲烷对立佯谬与 pptv 级检测极限：
       - TGO 测得甲烷上限严格小于 0.05 ppbv (50 pptv)
       - 好奇号在盖尔坑测得的局地峰值 21 ppbv
       - 反差倍数超 400 倍
       - 标称光化学寿命 ~300 年
    """
    meth = engine.compute_solar_occultation_and_methane_paradox()
    assert meth["tgo_methane_upper_limit_ppbv"] == 0.05
    assert meth["tgo_methane_upper_limit_pptv"] == 50.0
    assert meth["curiosity_gale_crater_spike_ppbv"] == 21.0
    assert meth["methane_paradox_ratio"] >= 400.0
    assert meth["nominal_lifetime_years"] == 300.0

def test_hcl_gas_discovery_and_isotopic_water_escape(engine):
    """
    6. 验证火星氯化氢 (HCl) 气体发现与同位素水汽逃逸：
       - 首次测得 HCl 丰度范围 0.5~4.0 ppbv，标称 2.5 ppbv
       - 沙尘暴期间水汽突破冷阱上升到 80 km 高空
       - D/H 相对地球 VSMOW 富集 5.5 倍
       - 远古失水比例超 80%
    """
    hcl = engine.compute_hcl_and_water_escape_chemistry()
    assert hcl["hcl_abundance_range_ppbv"] == (0.5, 4.0)
    assert hcl["nominal_hcl_ppbv"] == 2.5
    assert hcl["water_lofting_altitude_km"] == 80.0
    assert hcl["dh_enrichment_vs_vsmow"] >= 5.0
    assert hcl["min_ancient_water_loss_fraction"] > 0.80

def test_frend_collimated_neutron_telescope_and_water_oasis(engine):
    """
    7. 验证 FREND 准直超热中子望远镜与水手号大峡谷浅表水冰绿洲：
       - 准直视场 ~75 km，分辨率提升超 5 倍
       - 坎多尔混沌区 (Candor Chaos) WEH 高达 40 wt%
       - 水冰富集倍数较赤道基线超 10 倍
       - 荷兰面积大小绿洲浅表 1 米水储量超 200 亿吨
    """
    frend = engine.compute_frend_candor_chaos_water_oasis()
    assert frend["frend_collimated_footprint_km"] == 75.0
    assert frend["resolution_gain_ratio"] > 5.0
    assert frend["candor_chaos_weh_wt_percent"] == 40.0
    assert frend["water_enrichment_factor"] > 10.0
    assert frend["estimated_water_ice_billion_tons"] > 20.0

def test_martian_septet_matrix_expansion(engine):
    """
    8. 验证火星现役七大功勋金刚 (The Martian Septet) 协同体系：
       - 正式包含 7 艘现役探测器
       - TGO 作为第 5 艘在轨，寿命整整 10.0 年
    """
    septet = engine.get_martian_septet_matrix()
    assert len(septet) == 7
    names = [p["name"] for p in septet]
    assert any("2001 火星奥德赛号" in n for n in names)
    assert any("火星快车号" in n for n in names)
    assert any("火星勘测轨道飞行器" in n for n in names)
    assert any("好奇号" in n for n in names)
    assert any("ExoMars 痕量气体轨道器" in n for n in names)
    assert any("毅力号" in n for n in names)
    assert any("天问一号" in n for n in names)

def test_grand_octovigintet_fleet_matrix_and_28_mansions(engine):
    """
    9. 验证 2026 人类深空二十八极黄金舰队 (The Grand Octovigintet / 深空二十八宿)：
       - 舰队总规模严格等于 28 艘
       - 严格按日心极距降序排列
       - 极距跨度超 3,700 倍，太阳辐射能流跨度超 1,400 万倍
       - 完美对齐华夏二十八宿天象序列
    """
    octo = engine.get_grand_octovigintet_fleet()
    assert octo["fleet_size"] == 28
    fleet = octo["fleet"]
    assert len(fleet) == 28

    # 验证单调非增日心极距
    for i in range(len(fleet) - 1):
        assert fleet[i]["heliocentric_dist_au"] >= fleet[i+1]["heliocentric_dist_au"]

    # 验证极值比例
    assert octo["extreme_ratios"]["distance_ratio"] > 3700.0
    assert octo["extreme_ratios"]["solar_flux_ratio"] > 1.4e7

    # 验证首尾与关键节点
    assert "旅行者 1 号" in fleet[0]["name"]
    assert "帕克太阳探测器" in fleet[-1]["name"]
    assert any("ExoMars" in p["name"] and "虚宿" in p["mansion"] for p in fleet)
