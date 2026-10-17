"""
单元测试：2001 火星奥德赛号 (2001 Mars Odyssey) 在轨 25 周年银禧、
GRS 浅表水冰反演、THEMIS 全球热惯量、火星现役六大金刚与深空二十七极黄金舰队
"""

import math
import datetime
import sys
from pathlib import Path
import pytest

DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR / "scripts"))

from mars_odyssey_quarter_century_engine import MarsOdysseyEngine

@pytest.fixture
def engine():
    # 固定基准测试时间: 2026-10-18 04:30 UTC
    ref_dt = datetime.datetime(2026, 10, 18, 4, 30, tzinfo=datetime.timezone.utc)
    return MarsOdysseyEngine(current_dt=ref_dt)

def test_mission_timeline_and_silver_jubilee_countdown(engine):
    """
    1. 验证任务时间线与 25 周年银禧倒计时：
       - 在轨时间超 9,120 天 (24.98 地球年 / 13.2 火星年)
       - 距 2026-10-24 25 周年银禧倒计时 5.9 天 (约 142 小时)
    """
    tl = engine.compute_mission_timeline()
    assert tl["days_in_orbit"] > 9120.0
    assert 24.9 < tl["years_in_orbit"] < 25.1
    assert 13.0 < tl["mars_years_in_orbit"] < 13.5
    assert tl["total_flight_days"] > 9300.0
    assert 5.5 < tl["countdown_to_25y_days"] < 6.2
    assert 130.0 < tl["countdown_to_25y_hours"] < 150.0
    assert tl["is_silver_jubilee_near"] is True

def test_orbit_dynamics_and_cumulative_orbits(engine):
    """
    2. 验证开普勒轨道动力学与绕火公转圈数：
       - 400 km 制图轨道圆速度约 3.36 km/s
       - 轨道周期约 118.0 分钟 (1.97 小时)
       - 每日公转约 12.2 圈
       - 累计绕火公转突破 100,000 圈大关 (达 11.1 万圈)
    """
    od = engine.compute_orbit_dynamics()
    assert abs(od["orbital_altitude_km"] - 400.0) < 1.0
    assert abs(od["orbital_velocity_kms"] - 3.362) < 0.05
    assert abs(od["period_minutes"] - 118.04) < 0.5
    assert abs(od["period_hours"] - 1.967) < 0.02
    assert abs(od["orbits_per_earth_day"] - 12.20) < 0.1
    assert od["cumulative_orbits"] > 100000.0  # 历史性突破十万圈
    assert od["cumulative_orbits"] > 110000.0

def test_aerobraking_energy_and_fuel_savings(engine):
    """
    3. 验证气动减速 (Aerobraking) 物理与燃料节省：
       - 远火点从 27,000 km 压缩至 400 km
       - 节省等效推进剂 Delta-V 超 1100 m/s
       - 节省肼类推进剂超 150 kg (占探测器干重超 40%)
    """
    ab = engine.compute_aerobraking_physics()
    assert ab["initial_apoapsis_km"] == 27000.0
    assert ab["final_apoapsis_km"] == 400.0
    assert ab["equivalent_delta_v_saved_ms"] > 1100.0
    assert ab["propellant_saved_kg"] > 160.0
    assert ab["fuel_mass_ratio_saved_pct"] > 40.0

def test_grs_neutron_moderation_physics(engine):
    """
    4. 验证 GRS 中子谱仪中子热化减速与 2.223 MeV 伽马捕获物理：
       - 氢核与中子质量匹配，弹性碰撞动能转移率接近 100%
       - 氢核中子减速效率相较硅 (Si-28) 超出近 7.5 倍以上
       - 氢核热中子辐射俘获产生 2.223 MeV 特征伽马光子
    """
    grs = engine.compute_grs_subsurface_ice_physics()
    assert abs(grs["h_capture_gamma_energy_mev"] - 2.2233) < 0.001
    assert grs["energy_transfer_fraction_hydrogen"] > 0.999 # 接近 1.0
    assert grs["hydrogen_collision_efficiency_vs_silicon"] > 7.0

def test_polar_subsurface_ice_distribution(engine):
    """
    5. 验证极区地下浅表水冰分布参数：
       - 埋深在 30~60 cm 之间
       - 质量占比在 20%~50% 之间
       - 体积占比超 50% ("冰中带土")
       - 水冰当量体积超密歇根湖 2 倍 (>9800 km³)
    """
    grs = engine.compute_grs_subsurface_ice_physics()
    depth_min, depth_max = grs["polar_ice_depth_range_cm"]
    assert depth_min == 30.0 and depth_max == 60.0
    frac_min, frac_max = grs["polar_ice_mass_fraction_range"]
    assert frac_min == 0.20 and frac_max == 0.50
    assert grs["polar_ice_volume_fraction_pct"] > 50.0
    assert grs["equivalent_water_ice_volume_km3"] >= 9840.0

def test_themis_thermal_inertia_contrast(engine):
    """
    6. 验证 THEMIS 热惯量 (Thermal Inertia) 物理与矿物学：
       - 细尘热惯量约为 130 tiu，基岩超 2300 tiu，具有近 18 倍巨大热物理反差
       - 红外 9 波段 + 可见光 5 波段
       - 发现大面积橄榄石玄武岩与氯化物盐沉积
    """
    th = engine.compute_themis_thermal_inertia_physics()
    ti = th["thermal_inertia_tiu"]
    assert ti["Fine Dust / Silt"] < 150.0
    assert ti["Solid Basalt Bedrock"] > 2000.0
    ratio = ti["Solid Basalt Bedrock"] / ti["Fine Dust / Silt"]
    assert ratio > 15.0
    assert th["ir_bands_count"] == 9
    assert th["vis_bands_count"] == 5
    assert "Chloride" in th["major_mineral_discovery"]

def test_martian_hexad_cooperative_network(engine):
    """
    7. 验证火星现役六大金刚 (The Martian Hexad / Sextet) 协同体系：
       - 包含 Odyssey, MEX, MRO, Curiosity, Perseverance, Tianwen-1
       - 涵盖近圆极轨、准极区火卫一穿透轨、大椭圆遥感轨与地表巡视
       - 寿命覆盖从 5.7 年至 25.0 年
    """
    hexad = engine.get_martian_hexad_matrix()
    assert len(hexad) == 6
    names = [craft["name"] for craft in hexad]
    assert any("Odyssey" in n for n in names)
    assert any("Mars Express" in n for n in names)
    assert any("MRO" in n for n in names)
    assert any("Curiosity" in n for n in names)
    assert any("Perseverance" in n for n in names)
    assert any("Tianwen-1" in n for n in names)

def test_grand_septemvigintet_fleet_completeness(engine):
    """
    8. 验证 2026 人类深空二十七极黄金舰队 (The Grand Septemvigintet)：
       - 严格包含 27 艘现役/活跃深空探测器
       - 严格按日心极距降序排列
       - 涵盖旅行者 1/2 号、新视野号、木星三极、火星六重奏、水星与太阳三极
    """
    res = engine.get_grand_septemvigintet_fleet()
    assert res["fleet_size"] == 27
    fleet = res["fleet"]
    assert len(fleet) == 27
    
    # 严格降序检查
    for i in range(len(fleet) - 1):
        assert fleet[i]["heliocentric_dist_au"] >= fleet[i+1]["heliocentric_dist_au"]
    
    # 首尾确认
    assert "Voyager 1" in fleet[0]["name"]
    assert "Parker" in fleet[-1]["name"]

def test_extreme_astrophysical_duality_ratios(engine):
    """
    9. 验证深空二十七极极端物理对偶比：
       - 日心极距跨度超 3760 倍 (旅行者 1 号 173.22 AU vs 帕克 0.046 AU)
       - 太阳辐射能流落差超 1400 万倍
    """
    res = engine.get_grand_septemvigintet_fleet()
    ratios = res["extreme_ratios"]
    assert ratios["distance_ratio"] > 3760.0
    assert ratios["solar_flux_ratio"] > 1.4e7
