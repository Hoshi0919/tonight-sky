"""
test_hayabusa2_sharp_micro_asteroid_dynamics.py

单元测试集：验证隼鸟二号拓展任务 (Hayabusa2# / SHARP) 与 1998 KY26 超微型小行星动力学推演引擎。
"""

import sys
import os
import math
import pytest

# 将 scripts 目录加入 sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))

from hayabusa2_sharp_micro_asteroid_dynamics_engine import (
    get_hayabusa2_sharp_status,
    compute_torifune_flyby_metrics,
    compute_1998_ky26_micro_asteroid_physics,
    compute_hayabusa2_ion_propulsion_budget,
    get_grand_sedecet_fleet_metrics,
)


def test_hayabusa2_sharp_status_and_countdowns():
    """测试 2026-10-16 隼鸟二号拓展任务巡航状态与倒计时"""
    status = get_hayabusa2_sharp_status("2026-10-16")
    assert status["current_date"] == "2026-10-16"
    assert "Post-Torifune" in status["phase"]
    # 2026-07-05 飞掠至今恰好 103 天
    assert abs(status["days_since_torifune_flyby"] - 103.0) < 0.5
    # 倒计时 EGA-1 (2027-12-15) 约 425 天
    assert 420.0 <= status["days_to_ega1"] <= 430.0
    # 倒计时 1998 KY26 交会 (2031-07-15) 约 1733 天 (4.74 年)
    assert 1720.0 <= status["days_to_ky26_rendezvous"] <= 1745.0
    assert 4.70 <= status["years_to_ky26_rendezvous"] <= 4.80
    assert status["heliocentric_distance_au"] == 1.120


def test_torifune_flyby_ground_truth():
    """测试 98943 Torifune (2001 CC21) 744米掠飞关键实测数据"""
    torifune = compute_torifune_flyby_metrics()
    assert torifune["asteroid_name"] == "98943 Torifune (2001 CC21)"
    assert torifune["flyby_date"] == "2026-07-05"
    assert torifune["closest_approach_distance_m"] == 744.0
    assert torifune["relative_speed_km_s"] == 5.0
    assert "Contact Binary" in torifune["morphology"]
    assert torifune["mean_diameter_m"] == 540.0
    assert torifune["spectral_type"] == "Sq"
    assert torifune["rotation_period_hours"] == 5.0215
    # 峰值自主跟踪角速度 omega = 5000 / 744 = 6.72 rad/s = 385 deg/s
    assert torifune["peak_tracking_angular_rate_deg_s"] > 380.0


def test_1998_ky26_mass_and_microgravity():
    """测试 1998 KY26 直径 11m 极端微重力物理指标"""
    ky26 = compute_1998_ky26_micro_asteroid_physics(radius_m=5.5, density_kg_m3=2800.0, spin_period_min=5.3516)
    assert ky26["diameter_m"] == 11.0
    assert ky26["radius_m"] == 5.5
    # 质量约 1.95 x 10^6 kg
    assert abs(ky26["mass_kg"] - 1.951e6) < 0.05e6
    # 表面微引力约 4.305 um/s^2 (4.3 x 10^-6 m/s^2)
    assert 4.25 <= ky26["surface_gravity_um_s2"] <= 4.35
    # 逃逸速度极小，约 6.88 mm/s (< 1 cm/s)
    assert 6.80 <= ky26["escape_velocity_mm_s"] <= 6.95
    assert 0.68 <= ky26["escape_velocity_cm_s"] <= 0.70


def test_1998_ky26_superfast_spin_and_centrifugal_catapult():
    """测试 5.35分钟超快自转与赤道 490倍离心力弹射"""
    ky26 = compute_1998_ky26_micro_asteroid_physics()
    assert abs(ky26["spin_period_sec"] - 321.1) < 0.5
    assert abs(ky26["spin_rate_rad_s"] - 0.019568) < 0.0001
    # 赤道离心加速度约 2.106 mm/s^2 (2.1 x 10^-3 m/s^2)
    assert 2.05 <= ky26["centrifugal_accel_equator_mm_s2"] <= 2.15
    # 离心力对引力比值高达 489.1 倍
    assert 485.0 <= ky26["centrifugal_to_gravity_ratio"] <= 495.0


def test_1998_ky26_cohesive_strength():
    """测试内部维持连续介质不解体所需的 8.1 Pa 临界拉应力"""
    ky26 = compute_1998_ky26_micro_asteroid_physics()
    # 理论内聚抗拉强度约 8.11 Pa
    assert 8.0 <= ky26["required_cohesive_strength_pa"] <= 8.3
    # 验证普通岩石 (MPa) 可轻松承受，但无内聚力碎石堆必瓦解
    assert ky26["required_cohesive_strength_pa"] < 100.0


def test_critical_latitude_and_polar_sanctuary():
    """测试 87.41° 临界纬度与半径仅 24.9 cm 的极区重力庇护所"""
    ky26 = compute_1998_ky26_micro_asteroid_physics()
    # 临界纬度 87.41°
    assert 87.3 <= ky26["critical_latitude_deg"] <= 87.5
    # 极区半径仅 24.9 cm
    assert 24.0 <= ky26["polar_sanctuary_radius_cm"] <= 26.0
    # 全球 99.90% 表面处于离心排斥状态
    assert 99.85 <= ky26["repulsive_surface_percentage"] <= 99.95
    # 稳定重力庇护所占全表面约 0.102%
    assert 0.09 <= ky26["polar_sanctuary_surface_percentage"] <= 0.12


def test_net_radial_acceleration_profile():
    """测试不同纬度径向加速度分布（赤道向外排斥 vs 极区有效引力）"""
    ky26 = compute_1998_ky26_micro_asteroid_physics()
    # 赤道 0°：净向外弹射 2.102 mm/s^2 (负值)
    assert ky26["net_radial_accel_equator_mm_s2"] < -2.0
    # 45° 纬度：净向外弹射 1.049 mm/s^2
    assert ky26["net_radial_accel_45deg_mm_s2"] < -1.0
    # 80° 纬度：净向外弹射 0.059 mm/s^2
    assert ky26["net_radial_accel_80deg_mm_s2"] < 0.0
    # 极点 90°：离心力为 0，拥有完整向下微引力 +4.305 um/s^2 (正值)
    assert ky26["net_radial_accel_pole_um_s2"] > 4.25


def test_hayabusa2_ion_propulsion_budget():
    """测试 4台 μ10 微波离子电推 30kg 氙工质储备与 Δv 余量"""
    prop = compute_hayabusa2_ion_propulsion_budget()
    assert prop["xenon_propellant_kg"] == 30.0
    assert prop["specific_impulse_s"] == 2900.0
    # 齐奥尔科夫斯基可用速度增量约 1759.7 m/s
    assert 1750.0 <= prop["delta_v_available_mps"] <= 1770.0
    # 任务需求 1090 m/s，余量 669.7 m/s (+61.4%)
    assert prop["delta_v_required_mps"] == 1090.0
    assert 660.0 <= prop["delta_v_margin_mps"] <= 680.0
    assert 60.0 <= prop["margin_percentage"] <= 63.0
    assert prop["total_thrust_mn"] == 40.0


def test_grand_sedecet_fleet_completeness_and_extremes():
    """测试 2026 人类深空十六极黄金舰队完整性与极端物理对偶"""
    fleet = get_grand_sedecet_fleet_metrics()
    assert fleet["fleet_count"] == 16
    assert "Grand Sedecet" in fleet["fleet_name"]
    
    # 验证按日心距离降序排列
    distances = [m["distance_au"] for m in fleet["missions"]]
    for i in range(len(distances) - 1):
        assert distances[i] >= distances[i+1]
        
    # 最远为旅行者 1 号 (173.22 AU)，最近为帕克探测器 (0.046 AU)
    assert fleet["missions"][0]["name"] == "旅行者 1 号 (Voyager 1)"
    assert fleet["missions"][-1]["name"] == "帕克太阳探测器 (Parker Solar Probe)"
    
    # 极距跨度超 3765 倍，太阳辐射能流落差超 1400 万倍
    assert fleet["distance_span_ratio"] > 3700.0
    assert fleet["solar_flux_drop_ratio"] > 1.4e7
    
    # 验证隼鸟二号位列其中
    names = [m["name"] for m in fleet["missions"]]
    assert any("Hayabusa2" in name or "隼鸟二号" in name for name in names)
