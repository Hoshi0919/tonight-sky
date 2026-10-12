"""
Unit tests for 99942 Apophis 2029 Earth Flyby Orbital Mechanics Engine.
"""

import sys
import math
from pathlib import Path
import pytest

# 将 scripts 加入 Python 路径
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from apophis_2029_flyby_engine import (
    Apophis2029FlybyEngine,
    MU_EARTH,
    R_EARTH,
    GEO_RADIUS
)

@pytest.fixture
def engine():
    return Apophis2029FlybyEngine()

def test_hyperbolic_energy_conservation_and_perigee_velocity(engine):
    """验证双曲线轨道活力公式能量守恒与近地点速度"""
    flyby = engine.compute_hyperbolic_flyby()
    
    # 活力公式理论值: v_p^2 = v_inf^2 + 2*mu/r_p
    expected_vp_sq = (5850.0**2) + 2.0 * MU_EARTH / (38010.0e3)
    expected_vp = math.sqrt(expected_vp_sq) / 1000.0 # km/s
    
    assert abs(flyby.v_perigee - expected_vp) < 1e-4
    assert 7.0 < flyby.v_perigee < 8.0 # 理论在 7.43 km/s 附近
    assert flyby.altitude_km > 30000.0 # 高度大于 3 万公里
    assert flyby.altitude_km < 35000.0

def test_geo_belt_penetration_geometry(engine):
    """验证阿波菲斯掠地高度深入地球同步轨道 (GEO Belt) 内部"""
    flyby = engine.compute_hyperbolic_flyby()
    
    # GEO 轨道地心距 42,164 km，阿波菲斯地心距 38,010 km
    assert flyby.r_perigee_km < (GEO_RADIUS / 1000.0)
    assert flyby.inside_geo_km > 4000.0 # 深入 GEO 内部超 4000 km
    assert flyby.inside_geo_km < 4300.0

def test_hyperbolic_deflection_angle(engine):
    """验证地球引力弹弓渐近线偏转角 delta"""
    flyby = engine.compute_hyperbolic_flyby()
    
    # 偏心率应大于 1 (双曲线轨道)
    assert flyby.e_hyperbolic > 1.0
    assert 4.0 < flyby.e_hyperbolic < 4.5
    
    # 渐近线偏转角应在 26° ~ 28° 之间
    assert 26.0 < flyby.deflection_deg < 28.0

def test_orbital_class_transition_aten_to_apollo(engine):
    """验证掠地前后轨道根数跃迁: Aten 类跃迁为 Apollo 类"""
    trans = engine.compute_orbital_transition()
    
    assert "Aten" in trans.pre_class
    assert trans.pre_semi_major_au < 1.0 # Aten 特征: a < 1.0 AU
    assert 300.0 < trans.pre_period_days < 340.0
    
    assert "Apollo" in trans.post_class
    assert trans.post_semi_major_au > 1.0 # Apollo 特征: a > 1.0 AU
    assert trans.post_period_days > 400.0
    
    # 轨道周期显著被地球加速甩大，公转周期增加近 100 天
    assert 80.0 < trans.period_increase_days < 110.0

def test_roche_limit_and_tidal_seismic_risk(engine):
    """验证洛希极限边界与表面星震力学判据"""
    tidal = engine.compute_tidal_physics()
    
    # 不会整体碎裂: 近地点距 (38,010 km) > 流体洛希极限 (~20,800 km)
    assert not tidal.is_tidally_disrupted
    assert tidal.fluid_roche_limit_km < 25000.0
    assert tidal.rigid_roche_limit_km < 18000.0
    
    # 但潮汐引力差占自身表面重力比例超过 1%，足以打破松散沙石休止角
    assert tidal.tidal_to_gravity_ratio > 1.0
    assert tidal.tidal_to_gravity_ratio < 3.0
    assert "高风险强星震" in tidal.seismic_shaking_risk

def test_naked_eye_visibility_and_extreme_angular_velocity(engine):
    """验证峰值肉眼可见性与极端天球视运动角速度"""
    vis = engine.compute_visibility_and_dynamics()
    
    # 峰值视星等小于 4.0 等，肉眼清晰可见
    assert vis.naked_eye_visible is True
    assert 2.5 < vis.peak_v_mag < 3.8
    
    # 峰值角速度超 40°/h
    assert vis.peak_ang_speed_deg_hr > 40.0
    assert vis.peak_ang_speed_deg_hr < 55.0
    
    # 跨越一个满月视直径 (0.5°) 仅需数十秒
    assert 25.0 < vis.moon_diameter_traversal_sec < 50.0

def test_chinese_cities_observational_coverage(engine):
    """验证华夏代表性城市时空窗口完整性与时序自洽"""
    cities = engine.get_chinese_cities_windows()
    assert len(cities) >= 5
    
    city_names = [c["city"] for c in cities]
    assert "北京" in city_names
    assert "上海" in city_names
    assert "广州" in city_names
    assert "成都" in city_names
    assert "乌鲁木齐" in city_names
    
    # 乌鲁木齐拥有后半夜极盛深黑天窗
    urumqi = next(c for c in cities if c["city"] == "乌鲁木齐")
    assert "极佳纯黑暗空" in urumqi["dark_sky_status"]
