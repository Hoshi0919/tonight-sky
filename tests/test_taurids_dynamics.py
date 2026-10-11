"""
test_taurids_dynamics.py
========================
单元测试套件：2026 年金牛座流星群复合体（Taurid Complex）天体力学、
恩克彗星（2P/Encke）轨道动力学、木星 7:2 MMR 与平流层深穿透万圣节火流星物理验证
"""

import sys
from pathlib import Path
import pytest

# 添加 scripts 目录至 sys.path
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import taurids_dynamics_engine as engine


def test_encke_orbital_mechanics():
    """验证 2P/Encke 轨道参数、水星轨道深潜、木星 Tisserand 参量与 7:2 MMR 共振"""
    data = engine.calculate_encke_orbital_mechanics()
    
    # 周期 3.30 年
    assert 3.25 < data["period_yr"] < 3.35
    
    # 近日点深入水星轨道内侧 (q < 0.35 AU)
    assert 0.33 < data["perihelion_q_au"] < 0.34
    
    # 远日点小行星带外缘 (Q > 4.0 AU)
    assert 4.05 < data["aphelion_Q_au"] < 4.15
    
    # Tisserand 参量 T_J > 3.0 (木星族向阿波罗型过渡态)
    assert 3.01 < data["tisserand_parameter_tj"] < 3.05
    assert data["is_transition_object"] is True
    
    # 木星 7:2 平均运动共振
    assert 2.24 < data["mmr_7_2_semi_major_axis_au"] < 2.27
    assert data["delta_a_resonance_au"] < 0.05


def test_kinetic_energy_and_ablation_physics():
    """验证切入动能、自身重量 TNT 释放倍数及对比狮子座/猎户座超低烧蚀率"""
    data = engine.calculate_kinetic_and_ablation_physics()
    
    sta = data["STA"]
    nta = data["NTA"]
    
    # 速度与动能
    assert sta["entry_velocity_kms"] == 27.3
    assert nta["entry_velocity_kms"] == 29.0
    
    assert 370.0 < sta["kinetic_energy_mj_per_kg"] < 375.0
    assert 418.0 < nta["kinetic_energy_mj_per_kg"] < 423.0
    
    # TNT 释放倍数 (85 ~ 105 倍)
    assert 85.0 < sta["tnt_equivalent_ratio"] < 95.0
    assert 95.0 < nta["tnt_equivalent_ratio"] < 105.0
    
    # 烧蚀速率 (dm/dt ∝ v^3) 相比狮子座极低 (< 8%)
    assert sta["ablation_ratio_vs_leonids"] < 0.07
    assert nta["ablation_ratio_vs_leonids"] < 0.08
    
    # 相比猎户座也低 (< 10%)
    assert sta["ablation_ratio_vs_orionids"] < 0.08
    assert nta["ablation_ratio_vs_orionids"] < 0.09
    
    # 平流层穿透能力
    assert sta["can_penetrate_stratosphere"] is True
    assert nta["can_penetrate_stratosphere"] is True


def test_radiant_separations_and_m45_proximity():
    """验证南北群辐射点天球角距及其与昴星团 M45 的近邻同框关系"""
    data = engine.calculate_radiant_separations()
    
    # 南北群辐射点间距 ~ 11°
    assert 10.0 < data["separation_sta_nta_deg"] < 12.0
    
    # 北群辐射点与昴星团 (M45) 仅相距 2.36°
    assert 2.0 < data["separation_nta_m45_deg"] < 2.8
    assert data["nta_m45_binocular_field_compatible"] is True


def test_bolide_photometry_scaling():
    """验证不同质量碎屑的目视星等单调性、火球分级与平流层终点高度"""
    table = engine.calculate_bolide_photometry_by_mass()
    assert len(table) == 7
    
    # 质量递增，目视星等单调变亮（数值变小）
    mvs = [item["visual_magnitude_mv"] for item in table]
    assert all(x > y for x, y in zip(mvs, mvs[1:]))
    
    # 100g 碎石即达到金星级火流星 (M_v < -4.0)
    boulder_100g = [t for t in table if t["mass_label"] == "100 g"][0]
    assert boulder_100g["visual_magnitude_mv"] < -4.0
    
    # 1kg 岩块直穿平流层 (终止高度 < 50 km)
    rock_1kg = [t for t in table if t["mass_label"] == "1 kg"][0]
    assert rock_1kg["terminal_penetration_altitude_km"] <= 45.0
    assert rock_1kg["visual_magnitude_mv"] < -6.5


def test_chinese_cities_culmination_and_zenith():
    """验证华夏五大城市最高中天仰角、广州直插天顶顶心与整夜可见性"""
    cities = engine.calculate_chinese_cities_geometry()
    assert len(cities) == 5
    
    # 所有主要城市最高仰角均 > 60°
    for k, c in cities.items():
        assert c["sta_culmination_altitude_deg"] > 58.0
        assert c["nta_culmination_altitude_deg"] > 66.0
        assert c["sta_airmass"] < 1.20
        assert c["nta_airmass"] < 1.10
        assert c["all_night_visible_hours"] >= 10.0
        
    # 广州由于北纬 23.1°，北金牛座辐射点 (Dec +22.0°) 中天仰角直逼 89° 天顶
    gz = cities["Guangzhou"]
    assert gz["nta_culmination_altitude_deg"] > 88.5
    assert gz["reaches_near_zenith"] is True
    assert gz["nta_airmass"] < 1.002


def test_full_report_structure():
    """验证综合报告生成与数据结构完整性"""
    report = engine.generate_full_report()
    assert "encke_orbital_mechanics" in report
    assert "ablation_physics" in report
    assert "radiant_separations" in report
    assert "bolide_photometry_table" in report
    assert "chinese_cities_geometry" in report
