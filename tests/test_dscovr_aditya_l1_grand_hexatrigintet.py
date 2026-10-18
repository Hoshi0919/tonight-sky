"""
test_dscovr_aditya_l1_grand_hexatrigintet.py
============================================
单元测试集：日地 L1 空间天气与日地三杰 (DSCOVR, Aditya-L1)、太阳风磁暴预警模型、
以及 2026 人类深空三十六极黄金舰队 (The Grand Hexatrigintet) 全景动力学矩阵。
"""

import sys
from pathlib import Path
import pytest

# 添加 scripts 目录至 Python 路径
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from dscovr_aditya_l1_grand_hexatrigintet_engine import (
    compute_dscovr_state,
    compute_aditya_l1_state,
    compute_solar_wind_warning_lead_time,
    the_grand_hexatrigintet_fleet_census,
    sun_earth_l1_armada_summary,
    EPOCH_2026_10_18
)


def test_dscovr_orbital_and_payload_physics():
    """测试 DSCOVR 深空气候观测台在轨服役参数、日地 L1 利萨如轨道与五大科学载荷"""
    state = compute_dscovr_state(EPOCH_2026_10_18)
    
    # 1. 轨道与在轨时长断言
    assert state.name.startswith("DSCOVR")
    assert state.agency == "NASA/NOAA/USAF"
    assert state.heliocentric_distance_au == pytest.approx(0.990, abs=0.01)
    assert state.distance_from_earth_km == pytest.approx(1500000.0, abs=1000.0)
    assert state.cumulative_years_in_space > 11.5  # 2015-02-11 发射，超 11.6 年
    assert state.cumulative_days_in_l1_orbit > 4100.0
    
    # 2. 核心科学载荷断言
    payload_names = " ".join(state.core_payloads)
    assert "EPIC" in payload_names
    assert "PlasMag Faraday Cup" in payload_names
    assert "PlasMag Fluxgate Magnetometer" in payload_names
    assert "NISTAR" in payload_names
    
    # 3. 科学成就
    highlights = " ".join(state.scientific_highlights)
    assert "full sunlit Earth disk" in highlights
    assert "Earth-Moon transits" in highlights
    assert "early warning" in highlights


def test_aditya_l1_orbital_and_payload_physics():
    """测试 Aditya-L1 太阳神天文台在轨服役参数、L1 大晕轨道与七大科学载荷"""
    state = compute_aditya_l1_state(EPOCH_2026_10_18)
    
    # 1. 轨道与在轨时长断言
    assert state.name == "Aditya-L1"
    assert "ISRO" in state.agency
    assert state.heliocentric_distance_au == pytest.approx(0.990, abs=0.01)
    assert state.cumulative_years_in_space > 3.0  # 2023-09-02 发射，超 3.1 年
    assert state.cumulative_days_in_l1_orbit > 1000.0  # 2024-01-06 注入 L1 晕轨道超 1000 天
    assert "Halo Orbit" in state.orbit_type
    
    # 2. 核心科学载荷断言
    payload_names = " ".join(state.core_payloads)
    assert "VELC" in payload_names
    assert "Fe XIV 530.3nm" in payload_names
    assert "Fe X 637.4nm" in payload_names
    assert "SUIT" in payload_names
    assert "ASPEX" in payload_names
    assert "PAPA" in payload_names
    assert "MAG" in payload_names


def test_solar_wind_warning_lead_time_models():
    """测试日地 L1 哨位对地球磁层的太阳风暴/CME 提前预警时间窗口物理模型"""
    warning = compute_solar_wind_warning_lead_time()
    
    # 有效传播距离 (150 万公里 - 磁层顶 6.4 万公里 = 143.6 万公里)
    assert warning["effective_travel_distance_km"] == pytest.approx(1436000.0, abs=100.0)
    
    # 慢速太阳风 (400 km/s): 提前预警约 59.8 分钟 (近 1 小时)
    assert warning["typical_slow_wind_warning_mins"] == pytest.approx(59.83, abs=0.5)
    
    # 快速太阳风 / 中等 CME (800 km/s): 提前预警约 29.9 分钟 (约半小时)
    assert warning["typical_fast_wind_warning_mins"] == pytest.approx(29.92, abs=0.5)
    
    # 极端超级太阳风暴 / 强 CME (2000 km/s): 提前预警约 12.0 分钟
    assert warning["extreme_cme_warning_mins"] == pytest.approx(11.97, abs=0.5)


def test_grand_hexatrigintet_fleet_count_and_completeness():
    """测试人类深空三十六极黄金舰队旗舰数量严格等于 36 艘，且按日心极距降序严格单调非递增"""
    fleet_data = the_grand_hexatrigintet_fleet_census()
    fleet = fleet_data["fleet"]
    
    # 严格 36 艘主力深空探测器
    assert fleet_data["probe_count"] == 36
    assert len(fleet) == 36
    
    # 验证单调降序排列
    for i in range(len(fleet) - 1):
        assert fleet[i]["dist_au"] >= fleet[i+1]["dist_au"], (
            f"Ordering violation at rank {fleet[i]['rank']}: {fleet[i]['name']} ({fleet[i]['dist_au']} AU) "
            f"< {fleet[i+1]['name']} ({fleet[i+1]['dist_au']} AU)"
        )
    
    # 验证新加入的 DSCOVR 与 Aditya-L1 排名
    names = [p["name"] for p in fleet]
    assert "DSCOVR" in names
    assert "Aditya-L1" in names
    assert "SOHO" in names
    assert names.index("DSCOVR") == 30   # Rank 31
    assert names.index("Aditya-L1") == 31 # Rank 32


def test_fleet_arenas_distribution():
    """测试三十六极黄金舰队全面覆盖深空各大竞技场"""
    fleet_data = the_grand_hexatrigintet_fleet_census()
    arenas = {p["arena"] for p in fleet_data["fleet"]}
    
    # 涵盖深空各大竞技场
    assert "Interstellar Frontier" in arenas
    assert "Kuiper Belt & Beyond" in arenas
    assert "Jovian System" in arenas
    assert "Jupiter Trojan Swarms" in arenas
    assert "Main Asteroid Belt Cruise" in arenas
    assert "Martian Orbit" in arenas
    assert "Martian Surface" in arenas
    assert "Sun-Earth L2 Halo Orbit" in arenas
    assert "Lunar Polar Orbit" in arenas
    assert "Cislunar NRHO" in arenas
    assert "Lunar Farside Surface" in arenas
    assert "Sun-Earth L1 Halo Orbit" in arenas
    assert "Sun-Earth L1 Lissajous Orbit" in arenas
    assert "Solar Corona In-Situ" in arenas


def test_extreme_physical_ratios_hexatrigintet():
    """测试三十六极黄金舰队宏伟极端物理对偶落差"""
    fleet_data = the_grand_hexatrigintet_fleet_census()
    extremes = fleet_data["extremes"]
    
    # 1. 日心跨度超 3,700 倍
    assert extremes["distance_span_ratio"] > 3700.0
    
    # 2. 太阳辐射通量落差超 1400 万倍
    assert extremes["solar_flux_drop_ratio"] > 14000000.0
    
    # 3. 极端温差超 1,600 K
    assert extremes["temperature_span_k"] > 1650.0
    
    # 4. 旅行者1号通信延迟 24 小时 vs 地月通信 1.28 秒 (比率超 67,000 倍)
    assert extremes["voyager1_one_way_light_hours"] > 24.0
    assert extremes["lunar_one_way_light_seconds"] == pytest.approx(1.282, abs=0.01)
    assert extremes["communication_latency_ratio"] > 67000.0
    
    # 5. 极端速度比超 2700 万倍
    assert extremes["velocity_ratio"] > 27000000.0


def test_l1_trio_synergy():
    """测试日地 L1 点三大深空前哨（SOHO + DSCOVR + Aditya-L1）协同体系"""
    fleet_data = the_grand_hexatrigintet_fleet_census()
    l1_probes = [p for p in fleet_data["fleet"] if "L1" in p["arena"]]
    
    assert len(l1_probes) == 3
    l1_names = [p["name"] for p in l1_probes]
    assert "SOHO" in l1_names
    assert "DSCOVR" in l1_names
    assert "Aditya-L1" in l1_names
    
    agencies = {p["agency"] for p in l1_probes}
    assert "ESA/NASA" in agencies
    assert "NASA/NOAA/USAF" in agencies
    assert "ISRO" in agencies


def test_sun_earth_l1_armada_summary_structure():
    """测试综合分析摘要数据结构完整性"""
    summary = sun_earth_l1_armada_summary()
    
    assert "system_name" in summary
    assert "dscovr" in summary
    assert "aditya_l1" in summary
    assert "space_weather_early_warning" in summary
    assert "fleet_status" in summary
    assert summary["fleet_status"]["probe_count"] == 36


def test_inner_outer_fleet_boundary_consistency():
    """测试最外边界（旅行者1号）与最内边界（帕克探测器）极限对偶一致性"""
    fleet_data = the_grand_hexatrigintet_fleet_census()
    first = fleet_data["fleet"][0]
    last = fleet_data["fleet"][-1]
    
    assert first["name"] == "Voyager 1"
    assert first["dist_au"] == 173.22
    assert last["name"] == "Parker Solar Probe"
    assert last["dist_au"] == 0.046
