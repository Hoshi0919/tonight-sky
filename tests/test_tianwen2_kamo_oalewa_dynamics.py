"""
单元测试：中国天问二号 (Tianwen-2) 振天星 (469219 Kamoʻoalewa) 天体力学、月球起源与双目标跃迁引擎
"""

import sys
import math
from pathlib import Path
import pytest

scripts_dir = Path(__file__).parent.parent / "scripts"
repo_dir = Path(__file__).parent.parent
sys.path.insert(0, str(scripts_dir))
sys.path.insert(0, str(repo_dir))

from tianwen2_kamo_oalewa_dynamics_engine import (
    calculate_quasi_satellite_geometry,
    calculate_asteroid_physical_properties,
    calculate_lunar_ejecta_origin,
    calculate_tianwen2_flight_profile,
    generate_grand_octet_fleet_summary,
    AU_KM
)


def test_quasi_satellite_geometry():
    """测试 1:1 平均运动共振准卫星轨道与希尔球边界检验"""
    qs = calculate_quasi_satellite_geometry()
    
    # 半长轴极其接近 1.0 AU (1.00123 AU)
    assert 1.000 < qs.semi_major_axis_au < 1.005
    # 偏心率约 0.104
    assert 0.09 < qs.eccentricity < 0.12
    # 轨道倾角约 7.77°
    assert 7.0 < qs.inclination_deg < 8.5
    
    # 公转周期接近 1 个恒星年 (365.25 天左右)
    assert 364.0 < qs.orbital_period_days < 367.0
    
    # 地球希尔球半径约 150 万公里 (约 0.010 AU)
    assert 1.45e6 < qs.hill_sphere_radius_km < 1.55e6
    assert 0.0095 < qs.hill_sphere_radius_au < 0.0105
    
    # 相对位移振幅：沿轨长轴应约为径向短轴的 2 倍 (Hill/CW 相对运动特征)
    assert math.isclose(qs.intrack_amplitude_au, 2.0 * qs.radial_amplitude_au, rel_tol=1e-3)
    
    # 希尔球边界检验：Kamo'oalewa 最近距离远在地球希尔球之外 (10 倍以上)，未被地球引力捕获
    assert qs.min_dist_to_hill_ratio > 10.0
    assert qs.min_earth_dist_au > 0.10


def test_asteroid_physical_properties_and_centrifugal_paradox():
    """测试 469219 Kamoʻoalewa 物理参数与 28 分钟极速旋转离心崩解悖论"""
    props = calculate_asteroid_physical_properties()
    
    # 尺度校验 (68m x 46m x 39m)
    assert props.axis_a_m == 34.0
    assert props.axis_b_m == 23.0
    assert props.axis_c_m == 19.5
    
    # 质量约 1.66 x 10^8 kg (约 16.6 万吨)
    assert 1.5e8 < props.mass_kg < 1.8e8
    
    # 自转周期约为 27.66 分钟 (小于半小时，突破 2.2 小时碎石堆自转屏障)
    assert 25.0 < props.rotation_period_min < 30.0
    assert 3.5e-3 < props.angular_velocity_rad_s < 4.0e-3
    
    # 赤道离心加速度约为 4.87e-4 m/s²
    assert 4.5e-4 < props.centrifugal_accel_m_s2 < 5.2e-4
    
    # 表面自引力约为 9.59e-6 m/s²
    assert 8.0e-6 < props.surface_gravity_m_s2 < 1.1e-5
    
    # 核心物理推论：赤道离心加速度必须超过自引力 40 倍以上 (实测约 50.8 倍)
    # 这证明其不可能为纯引力结合的松散碎石堆，必须具备坚固内聚力或为单体月球岩石
    assert props.centrifugal_gravity_ratio > 45.0
    assert props.min_cohesion_pa > 15.0


def test_lunar_ejecta_origin():
    """测试乔尔达诺·布鲁诺撞击坑抛射动力学"""
    lunar = calculate_lunar_ejecta_origin()
    
    # 源撞击坑为 Giordano Bruno
    assert "Giordano Bruno" in lunar.source_crater_name
    assert lunar.crater_diameter_km == 22.0
    
    # 月球逃逸速度精确约为 2.375 km/s
    assert math.isclose(lunar.lunar_escape_velocity_km_s, 2.375, abs_tol=0.01)
    
    # 撞击体直径与速度
    assert 1.0 < lunar.impactor_diameter_km < 2.0
    assert 15.0 < lunar.impact_velocity_km_s < 20.0


def test_tianwen2_flight_profile():
    """测试天问二号双目标跨界跃迁飞行计划"""
    tw2 = calculate_tianwen2_flight_profile()
    
    # 发射于 2025 年 5 月
    assert "2025-05" in tw2.launch_date
    assert "长征三号乙" in tw2.carrier_rocket or "CZ-3B" in tw2.carrier_rocket
    
    # 400 天巡航后于 2026 年 7 月抵达 20 km 伴飞
    assert tw2.cruise_days >= 380.0
    assert "2026-07" in tw2.arrival_date
    assert tw2.hovering_distance_km == 20.0
    
    # 采样目标 >= 100 克
    assert tw2.sampling_mass_target_g >= 100.0
    
    # 2027 年返回地球，再入速度达到第二宇宙速度 (11.2 km/s)
    assert tw2.earth_return_year == 2027
    assert math.isclose(tw2.reentry_velocity_km_s, 11.2, abs_tol=0.1)
    
    # 第二目标为 311P/PANSTARRS 活跃彗星
    assert "311P" in tw2.secondary_target


def test_grand_octet_fleet_duality():
    """测试 2026 人类深空八极黄金舰队全景与时空跨度极值"""
    fleet = generate_grand_octet_fleet_summary()
    
    assert len(fleet) == 8
    
    # 检验极距最大跨度：旅行者 1 号 (> 170 AU) vs 帕克太阳探测器 (< 0.05 AU)
    voyager = next(p for p in fleet if "旅行者" in p["name"])
    parker = next(p for p in fleet if "帕克" in p["name"])
    tw2 = next(p for p in fleet if "天问二号" in p["name"])
    
    assert voyager["distance_au"] > 170.0
    assert parker["distance_au"] < 0.05
    assert 0.99 < tw2["distance_au"] < 1.02
    
    # 极距跨度比超 3700 倍
    ratio_dist = voyager["distance_au"] / parker["distance_au"]
    assert ratio_dist > 3700.0
    
    # 极速比检验：帕克 (192 km/s) vs 韦伯 (0.2 km/s) 超 900 倍
    jwst = next(p for p in fleet if "韦伯" in p["name"])
    ratio_speed = parker["speed_km_s"] / jwst["speed_km_s"]
    assert ratio_speed > 900.0


def test_cohesion_versus_rubble_pile_barrier():
    """测试 2.2 小时经典碎石堆自转屏障 (Spin Barrier) 突破与内聚抗拉强度下限"""
    props = calculate_asteroid_physical_properties()
    
    # 经典无内聚力碎石堆临界破裂周期 T_crit = sqrt(3 * pi / (G * rho))
    # 对于密度 2600 kg/m^3 的岩石:
    # T_crit = sqrt(3 * pi / (6.6743e-11 * 2600)) ≈ 7367 秒 ≈ 2.05 ~ 2.2 小时
    g_const = 6.67430e-11
    t_crit_sec = math.sqrt(3.0 * math.pi / (g_const * props.density_kg_m3))
    t_crit_hours = t_crit_sec / 3600.0
    
    assert 2.0 < t_crit_hours < 2.3
    
    # Kamo'oalewa 实际自转周期仅 0.461 小时 (27.66 分钟)，远远短于临界破裂周期
    t_actual_hours = props.rotation_period_min / 60.0
    assert t_actual_hours < t_crit_hours * 0.25
    
    # 这证明其必须具备非零内聚力，其内聚强度 > 20 Pa，彻底击碎碎石堆假说
    assert props.min_cohesion_pa > 20.0


def test_jacobi_and_vis_viva_energy():
    """测试活力公式 (Vis-viva) 与准卫星近日点/远日点轨道能量守恒"""
    qs = calculate_quasi_satellite_geometry()
    
    mu_sun = 1.32712440018e11 # km^3 / s^2
    a_km = qs.semi_major_axis_au * AU_KM
    
    # 近日点与远日点距离
    r_peri_km = a_km * (1.0 - qs.eccentricity)
    r_aph_km = a_km * (1.0 + qs.eccentricity)
    
    # 活力公式计算速度: v = sqrt(mu * (2/r - 1/a))
    v_peri = math.sqrt(mu_sun * (2.0 / r_peri_km - 1.0 / a_km))
    v_aph = math.sqrt(mu_sun * (2.0 / r_aph_km - 1.0 / a_km))
    
    # 检验开普勒角动量守恒: r_peri * v_peri == r_aph * v_aph
    h_peri = r_peri_km * v_peri
    h_aph = r_aph_km * v_aph
    assert math.isclose(h_peri, h_aph, rel_tol=1e-5)
    
    # 速度范围在 26 km/s ~ 33 km/s 之间
    assert 32.0 < v_peri < 34.0
    assert 26.0 < v_aph < 28.0


def test_lunar_spallation_crater_scale_coupling():
    """测试 Melosh 剥落力学与撞击坑尺度耦合关系"""
    lunar = calculate_lunar_ejecta_origin()
    
    # 撞击坑直径 22 km
    # 产生未碎裂巨石的剥落厚度约等于撞击体尺度的百分之几
    # 撞击体约 1.5 km，剥落厚度可达数十米，与 Kamo'oalewa 40~70m 尺度完全匹配
    assert lunar.impactor_diameter_km * 1000.0 > 1000.0
    assert lunar.spallation_intact_mass_ton > 1.0e5
