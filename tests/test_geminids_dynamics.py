"""
test_geminids_dynamics.py
=========================
2026 双子座流星雨（Geminids 2026）天体力学与观象动力学单元测试套件
"""

import sys
import math
import json
from pathlib import Path
import pytest

DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR))

from scripts.geminids_dynamics_engine import (
    calculate_phaethon_mechanics,
    calculate_meteoroid_ablation,
    calculate_hourly_visible_rate,
    calculate_city_ephemeris,
    calculate_winter_hexagon_context,
    generate_full_report,
)


def test_phaethon_mechanics():
    """测试 3200 Phaethon 轨道参量与极端近日点热物理状态"""
    p = calculate_phaethon_mechanics()
    
    assert p["perihelion_q_au"] == pytest.approx(0.14, abs=0.01)
    assert p["aphelion_Q_au"] == pytest.approx(2.40, abs=0.02)
    assert p["period_years"] == pytest.approx(1.43, abs=0.05)
    
    # 太阳辐射通量与地球比值 (>50 倍)
    assert p["solar_flux_ratio_to_earth"] == pytest.approx(51.0, abs=2.0)
    
    # 次太阳点温度 (>1000 K, ~770 °C)
    assert p["subsolar_equilibrium_temp_k"] == pytest.approx(1050.0, abs=20.0)
    assert p["subsolar_equilibrium_temp_c"] == pytest.approx(777.0, abs=20.0)
    
    # 轨道速度 (近日点极高，远日点极低)
    assert p["perihelion_velocity_km_s"] > 100.0
    assert p["aphelion_velocity_km_s"] < 10.0


def test_meteoroid_ablation_physics():
    """测试流星烧蚀动力学、质量-星等单调性与等效直径"""
    m_small = calculate_meteoroid_ablation(0.01)
    m_mid = calculate_meteoroid_ablation(1.0)
    m_large = calculate_meteoroid_ablation(100.0)
    
    # 质量越大，动能越大
    assert m_small["kinetic_energy_j"] < m_mid["kinetic_energy_j"] < m_large["kinetic_energy_j"]
    
    # 质量越大，亮度越高（绝对星等数值越小/更负）
    assert m_small["visual_magnitude"] > m_mid["visual_magnitude"] > m_large["visual_magnitude"]
    
    # 1.0 mg (芝麻粒大小) 直径约 0.91 mm，星等在 +1 ~ +2 等之间
    assert m_mid["diameter_mm"] == pytest.approx(0.914, abs=0.05)
    assert 1.0 <= m_mid["visual_magnitude"] <= 2.5
    
    # 100 mg (豌豆大小) 产生火流星 (Mag < -2)
    assert m_large["visual_magnitude"] < -2.0
    
    # 烧蚀穿透深度在合理大气高度 (45 ~ 85 km)
    assert 40.0 <= m_large["terminal_ablation_alt_km"] <= 85.0


def test_hourly_visible_rate():
    """测试不同仰角与极限星等下的实际目视流星率 (HVR)"""
    # 地平线以下无可见流星
    assert calculate_hourly_visible_rate(150, -5.0) == 0.0
    
    # 天顶正上方 (90°)，暗夜 (NELM 6.5) 达到极盛标称值 150
    hvr_zenith = calculate_hourly_visible_rate(150, 90.0, limiting_mag=6.5)
    assert hvr_zenith == pytest.approx(150.0, abs=0.1)
    
    # 仰角 30° 时，因天顶角几何衰减，HVR 约为 150 * sin(30°) = 75
    hvr_30 = calculate_hourly_visible_rate(150, 30.0, limiting_mag=6.5)
    assert hvr_30 == pytest.approx(75.0, abs=0.5)
    
    # 光污染影响：NELM 5.5 (郊区中度光害) 衰减
    hvr_light_polluted = calculate_hourly_visible_rate(150, 90.0, limiting_mag=5.5)
    assert hvr_light_polluted < hvr_zenith


def test_city_ephemeris_dark_sky():
    """测试华夏五大城市观测几何与纯黑无月暗空窗口"""
    cities = calculate_city_ephemeris()
    assert len(cities) == 5
    
    city_map = {c["city_key"]: c for c in cities}
    
    # 验证北京、上海、广州、成都、乌鲁木齐都在列表中
    for key in ["Beijing", "Shanghai", "Guangzhou", "Chengdu", "Urumqi"]:
        assert key in city_map
        c = city_map[key]
        
        # 月相照亮比例在 16% ~ 18% 之间 (蛾眉月)
        assert 15.0 <= c["moon_illum_percent"] <= 20.0
        
        # 中天仰角全部在 75° ~ 89° 之间 (极高天顶)
        assert 75.0 <= c["transit_altitude_deg"] <= 89.5
        
        # 纯黑无月暗夜时窗在 9 小时以上
        assert c["dark_sky_window_hours"] >= 9.0
        
        # 暗夜目视流星率在 140 以上
        assert c["hvr_dark_sky"] >= 140.0


def test_winter_hexagon_context():
    """测试辐射点与冬季大六角参照星角距离"""
    stars = calculate_winter_hexagon_context()
    assert len(stars) == 8
    
    # 最近的恒星应为 Castor (北河二)，距离小于 2.0°
    assert stars[0]["cn"] == "北河二"
    assert stars[0]["separation_from_radiant_deg"] < 2.0
    
    # 第二近的恒星应为 Pollux (北河三)，距离小于 6.0°
    assert stars[1]["cn"] == "北河三"
    assert stars[1]["separation_from_radiant_deg"] < 6.0


def test_full_report_structure():
    """测试完整数据集生成与 JSON 序列化合法性"""
    data = generate_full_report()
    assert "meta" in data
    assert "phaethon_mechanics" in data
    assert "ablation_physics" in data
    assert "city_ephemeris" in data
    assert "winter_hexagon_context" in data
    
    # 验证能无损转为 JSON 字符串并反序列化
    serialized = json.dumps(data)
    deserialized = json.loads(serialized)
    assert deserialized["meta"]["nominal_zhr"] == 150
