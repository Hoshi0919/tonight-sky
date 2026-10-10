"""
test_leonids_dynamics.py
========================
2026 狮子座流星雨（Leonids 2026）天体力学、逆行超速切入、火木双星信标与
华夏观象交接动力学单元测试套件。
"""

import sys
import json
from pathlib import Path
import pytest

DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR))

from scripts.leonids_dynamics_engine import (
    calculate_comet_mechanics,
    calculate_hypervelocity_ablation,
    calculate_mars_jupiter_beacon,
    calculate_leo_sky_context,
    calculate_hourly_visible_rate,
    calculate_city_ephemeris,
    generate_full_report,
)


def test_comet_mechanics():
    """测试 55P/Tempel-Tuttle 轨道参数与逆行几何"""
    c = calculate_comet_mechanics()

    assert c["semi_major_axis_au"] == pytest.approx(10.334, abs=0.01)
    assert c["eccentricity"] == pytest.approx(0.9056, abs=0.005)
    assert c["inclination_deg"] == pytest.approx(162.49, abs=0.1)
    assert c["is_retrograde"] is True
    assert c["perihelion_q_au"] == pytest.approx(0.976, abs=0.02)
    assert c["aphelion_Q_au"] == pytest.approx(19.69, abs=0.1)
    assert c["period_years"] == pytest.approx(33.22, abs=0.1)
    assert c["entry_speed_km_s"] == pytest.approx(71.0, abs=0.5)
    assert 4.0 <= c["years_to_next_perihelion"] <= 5.0
    assert 4.5 <= c["est_heliocentric_distance_2026_au"] <= 5.2


def test_hypervelocity_ablation():
    """测试 71 km/s 超高切速动能密度、TNT 当量与高层消融特征"""
    m1 = calculate_hypervelocity_ablation(1.0)
    m10 = calculate_hypervelocity_ablation(10.0)
    m100 = calculate_hypervelocity_ablation(100.0)
    m500 = calculate_hypervelocity_ablation(500.0)

    # 单位动能释放约为 2.52 GJ/kg
    assert m1["kinetic_energy_per_kg_gj"] == pytest.approx(2.52, abs=0.05)
    # TNT 能量当量比约为 600 倍
    assert m1["tnt_equivalent_factor_per_kg"] == pytest.approx(602.4, abs=5.0)

    # 单调性：质量越大动能越高，星等越负（更亮）
    assert m1["kinetic_energy_j"] < m10["kinetic_energy_j"] < m100["kinetic_energy_j"] < m500["kinetic_energy_j"]
    assert m1["visual_magnitude"] > m10["visual_magnitude"] > m100["visual_magnitude"] > m500["visual_magnitude"]

    # 100 mg 砂粒产生亮流星 (V < -2.0)
    assert m100["visual_magnitude"] < -2.0

    # 500 mg (0.5 克) 产生耀眼火球 (V <= -3.0，达到 IAU 火流星门槛)
    assert m500["visual_magnitude"] < -3.0
    assert m500["is_fireball"] is True

    # 消融起始高度远高于常规流星 (>115 km)
    assert m1["ablation_start_alt_km"] > 115.0
    assert m1["terminal_ablation_alt_km"] >= 75.0

    # 持久余迹物理机制描述完整
    assert "557.7 nm" in m1["train_physics"]["initial_glow"]
    assert "NO + O3" in m1["train_physics"]["long_duration_persistent_train"]


def test_mars_jupiter_beacon():
    """测试极盛夜火星与木星超近会合与辐射点角距标尺"""
    b = calculate_mars_jupiter_beacon()

    # 火木相隔角距在 1.1° ~ 1.5° 之间
    assert 1.0 <= b["conjunction_min_separation_deg"] <= 1.3
    assert 1.2 <= b["peak_night_mars_jupiter_sep_deg"] <= 1.5

    # 亮行星视星等
    assert b["mars_magnitude"] < 1.0     # 约 +0.64 等
    assert b["jupiter_magnitude"] < -1.8 # 约 -1.99 等

    # 双星距辐射点在 10° 黄金视场内
    assert b["mars_to_radiant_sep_deg"] < 8.5
    assert b["jupiter_to_radiant_sep_deg"] < 10.0


def test_leo_sky_context():
    """测试狮子座头部参照恒星与辐射点距离"""
    stars = calculate_leo_sky_context()

    assert len(stars) == 6
    # 距离最近的核心参照星是 Algieba (轩辕十二)，角距约 3.5°
    assert stars[0]["name_cn"] == "轩辕十二"
    assert stars[0]["separation_to_radiant_deg"] == pytest.approx(3.53, abs=0.2)

    # 包含主星 Regulus (轩辕十四)
    regulus = next(s for s in stars if "Regulus" in s["name"])
    assert regulus["separation_to_radiant_deg"] == pytest.approx(10.03, abs=0.3)


def test_hourly_visible_rate():
    """测试目视流星率公式与月光抑制效应"""
    # 地平线以下为 0
    assert calculate_hourly_visible_rate(0.0, -10.0) == 0.0
    assert calculate_hourly_visible_rate(-5.0, -10.0) == 0.0

    # 仰角越高流星率越高
    hr_low = calculate_hourly_visible_rate(20.0, -10.0)
    hr_high = calculate_hourly_visible_rate(70.0, -10.0)
    assert hr_low < hr_high

    # 月光抑制：月亮在地平以上时有效率显著降低
    hr_dark = calculate_hourly_visible_rate(60.0, -20.0, nelm=6.5)
    hr_moon = calculate_hourly_visible_rate(60.0, 40.0, nelm=6.5)
    assert hr_moon < hr_dark


def test_city_ephemeris():
    """测试华夏五大城市观象交接与纯黑天窗"""
    cities = ["Beijing", "Shanghai", "Guangzhou", "Chengdu", "Urumqi"]
    for city_key in cities:
        c = calculate_city_ephemeris(city_key)
        assert c["city_key"] == city_key
        # 纯黑天窗时长必须在 5.0 ~ 6.0 小时之间
        assert 5.0 <= c["dark_sky_duration_hours"] <= 6.0
        # 辐射点升起与月落时刻必须在午夜前后 (23:00 ~ 02:00)
        assert c["moon_set_cst"] is not None
        assert c["radiant_rise_cst"] is not None
        assert c["dawn_twilight_cst"] is not None

    # 广州由于低纬度 (23.1°N)，天顶角极小，最高仰角接近 89°
    gz = calculate_city_ephemeris("Guangzhou")
    assert gz["max_radiant_alt_deg"] >= 88.0

    # 上海最高仰角 > 80°
    sh = calculate_city_ephemeris("Shanghai")
    assert sh["max_radiant_alt_deg"] >= 80.0


def test_full_report_structure():
    """测试完整全景报告的数据结构与 JSON 可序列化"""
    rep = generate_full_report()

    assert "parent_comet" in rep
    assert "ablation_physics_samples" in rep
    assert "mars_jupiter_beacon" in rep
    assert "leo_reference_stars" in rep
    assert "chinese_cities_geometry" in rep

    # 检验 JSON 导出无报错
    serialized = json.dumps(rep, ensure_ascii=False)
    assert len(serialized) > 1000
