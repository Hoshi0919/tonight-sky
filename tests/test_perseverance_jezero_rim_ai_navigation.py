"""
test_perseverance_jezero_rim_ai_navigation.py
=============================================
NASA 毅力号火星车 (Perseverance Rover) 杰泽罗撞击坑环壁攀爬、
生成式 AI 导航、MOXIE 固态电解制氧与十七极深空黄金舰队动力学测试集。
"""

import sys
import os
import math
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))

from perseverance_jezero_rim_ai_navigation_engine import (
    PerseveranceJezeroRimEngine,
    MARS_SEMI_MAJOR_AXIS_AU,
    MARS_SURFACE_GRAVITY,
    TOTAL_SAMPLE_TUBES,
    SEALED_SAMPLE_TUBES_2026
)


@pytest.fixture
def engine():
    return PerseveranceJezeroRimEngine(current_mars_distance_au=1.524)


def test_mars_orbital_mechanics_and_light_time(engine):
    """测试 1: 验证火星轨道几何、偏心率、会合周期与通讯单向光时延迟"""
    state = engine.compute_mars_orbital_state()
    assert state.heliocentric_distance_au == 1.524
    assert 1.38 <= state.perihelion_au <= 1.39
    assert 1.66 <= state.aphelion_au <= 1.67
    assert 680.0 <= state.orbital_period_days <= 695.0
    assert 770.0 <= state.synodic_period_days <= 790.0  # 约 780 天会合周期
    assert 580.0 <= state.solar_flux_w_m2 <= 590.0
    assert 0.42 <= state.solar_flux_ratio_to_earth <= 0.44

    owlt_min, owlt_max = state.one_way_light_time_min_range
    assert 2.5 <= owlt_min <= 3.5  # 冲日最近约 3 分钟
    assert 21.0 <= owlt_max <= 23.5  # 合日最远约 22 分钟


def test_jezero_rim_climb_dynamics_and_slope_forces(engine):
    """测试 2: 验证 500米悬崖攀爬、20% 坡度分解力学与高地标定"""
    climb = engine.compute_jezero_rim_climb_dynamics(grade_percent=20.0)
    assert climb.vertical_elevation_gain_m == 500.0
    assert climb.nominal_grade_percent == 20.0
    assert 11.2 <= climb.slope_angle_deg <= 11.4

    # 1025 kg 在火星上的重量与正交分解检验
    expected_weight = 1025.0 * MARS_SURFACE_GRAVITY
    assert abs(climb.rover_weight_on_mars_n - expected_weight) < 1.0

    # 勾股定理验算分解力合力
    resultant = math.sqrt(climb.parallel_gravity_force_n ** 2 + climb.normal_gravity_force_n ** 2)
    assert abs(resultant - climb.rover_weight_on_mars_n) < 1.0

    assert climb.crest_location_name == "Lookout Hill"
    assert climb.max_measured_slip_ratio == 0.60


def test_ai_navigation_vlm_and_snapdragon_speedup(engine):
    """测试 3: 验证骁龙801相比RAD750算力跃迁、自主定位耗时与VLM规划里程"""
    ai = engine.compute_ai_navigation_metrics()
    assert ai.speedup_ratio >= 15.0  # 2.26 GHz vs 133 MHz 提升超 15 倍
    assert ai.localization_time_seconds <= 120.0  # 2 分钟内完成自主全局定位
    assert ai.localization_accuracy_cm <= 25.0  # 25 厘米精度
    assert ai.vlm_sol1707_drive_m == 210.0
    assert ai.vlm_sol1709_drive_m == 246.0
    assert ai.two_day_total_drive_m == 456.0


def test_moxie_soec_electrolysis_faraday_yield(engine):
    """测试 4: 验证 800°C 固态氧化物电解槽 10 单元堆栈法拉第产氧与纯度指标"""
    moxie = engine.compute_moxie_electrolysis_physics(cell_current_amperes=3.55)
    assert moxie.operating_temp_c == 800.0
    assert moxie.stack_cells_count == 10
    assert 35.0 <= moxie.effective_total_current_amperes <= 36.0
    assert 10.0 <= moxie.mean_rate_grams_per_hour <= 11.0  # 标称 10.4 g/h
    assert moxie.total_successful_runs == 16
    assert moxie.total_oxygen_produced_grams == 122.0
    assert moxie.oxygen_purity_percent >= 99.6


def test_sample_cache_diversity_and_depot_distribution(engine):
    """测试 5: 验证 43 支超纯钛合金样品管岩相分布与三叉口地面备份守恒"""
    cache = engine.compute_sample_cache_distribution()
    assert cache.total_capacity == TOTAL_SAMPLE_TUBES
    assert cache.sealed_count == SEALED_SAMPLE_TUBES_2026
    assert cache.available_remaining == 10
    assert cache.sealed_count + cache.available_remaining == cache.total_capacity

    # 各类岩性与背景对照管总和严格守恒
    core_sum = (cache.igneous_cores + cache.sedimentary_cores +
                cache.carbonate_cores + cache.regolith_breccia_cores +
                cache.witness_blank_tubes)
    assert core_sum == cache.sealed_count

    # 三叉口地面缓存与车载主样本守恒
    assert cache.three_forks_depot_tubes + cache.onboard_priority_tubes == cache.sealed_count


def test_grand_septendecet_fleet_cardinality_and_ordering(engine):
    """测试 6: 验证十七极深空黄金舰队旗舰数量严格为 17 且日心距离单调递减"""
    fleet = engine.get_grand_septendecet_fleet()
    assert len(fleet) == 17

    distances = [craft.distance_au for craft in fleet]
    for i in range(len(distances) - 1):
        assert distances[i] >= distances[i + 1], f"舰队未按距离降序排列: {fleet[i].name} < {fleet[i+1].name}"

    names = [c.name for c in fleet]
    assert "Perseverance" in names
    assert "Voyager 1" in names
    assert "Parker Solar Probe" in names
    assert "Hayabusa2# (SHARP)" in names
    assert "Voyager 2" in names


def test_grand_septendecet_fleet_extremes_ratios(engine):
    """测试 7: 验证十七极黄金舰队极端物理解算比值跨度"""
    extremes = engine.compute_fleet_extremes()
    assert extremes["fleet_size"] == 17
    assert extremes["max_distance_au"] == 173.22  # Voyager 1
    assert extremes["min_distance_au"] == 0.046   # Parker Solar Probe
    assert extremes["heliocentric_distance_ratio"] > 3700.0
    assert extremes["solar_radiation_flux_ratio"] > 1.4e7  # 能流落差超 1400 万倍
    assert extremes["temperature_span_k"] > 1650.0


def test_perseverance_lookout_hill_geological_transition(engine):
    """测试 8: 验证守望丘翻越进入 Wild West、地质年代跃升至 40 亿年前原生火成古地壳"""
    climb = engine.compute_jezero_rim_climb_dynamics(20.0)
    assert climb.target_geological_age_ga == 4.0
    assert "Pre-Jezero" in climb.crust_type
    assert climb.crest_location_name == "Lookout Hill"


def test_mars_surface_environmental_extremes(engine):
    """测试 9: 验证火星表面重力加速度与太阳能流比率物理基准"""
    assert abs(MARS_SURFACE_GRAVITY - 3.72076) < 1e-4
    state = engine.compute_mars_orbital_state()
    # 火星太阳能流落差约为地球的 43%
    assert 0.40 <= state.solar_flux_ratio_to_earth <= 0.45
