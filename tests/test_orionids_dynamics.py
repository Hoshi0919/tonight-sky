"""
test_orionids_dynamics.py
=========================
单元测试集：2026 猎户座流星雨（Orionids）天体力学推演引擎、母彗星 1P/Halley 状态与华夏暗空天窗解算。
"""

import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
import pytest

# 添加 scripts 目录至 Python 路径
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from orionids_dynamics_engine import (
    compute_halley_state,
    compute_atmospheric_physics,
    compute_zhr_profile,
    compute_china_observation_windows,
    generate_full_report,
    HALLEY_SEMI_MAJOR_AU,
    HALLEY_ECCENTRICITY,
    HALLEY_INCLINATION_DEG,
    ORIONIDS_ENTRY_VELOCITY,
    ORIONIDS_PEAK_ZHR,
    CST_TZ
)


def test_halley_orbital_mechanics():
    """测试 1P/Halley 逆行轨道几何与 2026 年日心状态"""
    dt_cst = datetime(2026, 10, 21, 23, 0, tzinfo=CST_TZ)
    state = compute_halley_state(dt_cst)

    # 1. 轨道基本参量断言
    assert HALLEY_SEMI_MAJOR_AU == pytest.approx(17.834, abs=0.01)
    assert HALLEY_ECCENTRICITY == pytest.approx(0.9671, abs=0.001)
    assert HALLEY_INCLINATION_DEG > 160.0  # 逆行轨道

    # 2. 远日点几何断言
    assert state['aphelion_distance_au'] == pytest.approx(35.08, abs=0.1)
    assert state['aphelion_speed_kms'] == pytest.approx(0.912, abs=0.05)

    # 3. 2026 年 10 月实时状态断言（刚过远日点，向内太阳系沉降）
    assert state['heliocentric_distance_au'] == pytest.approx(34.94, abs=0.1)
    assert state['orbital_speed_kms'] == pytest.approx(1.02, abs=0.05)
    assert state['true_anomaly_deg'] == pytest.approx(180.96, abs=0.5)
    assert "Inbound" in state['orbit_state']
    assert state['years_to_next_perihelion_2061'] == pytest.approx(34.77, abs=0.5)


def test_atmospheric_hypervelocity_physics():
    """测试 66.0 km/s 超高速大气层消融物理与能量密度"""
    physics = compute_atmospheric_physics(mass_kg=1.0e-6)

    # 1. 切入初速与动能密度
    assert physics['entry_velocity_kms'] == 66.0
    assert physics['kinetic_energy_density_gj_per_kg'] == pytest.approx(2.178, abs=0.01)
    assert physics['tnt_equivalent_mass_multiplier'] == pytest.approx(520.6, abs=1.0)

    # 2. 1 毫克流星微粒能量释放
    assert physics['single_particle_energy_joules'] == pytest.approx(2178.0, abs=1.0)

    # 3. 激波温度与消融几何
    assert physics['shock_stagnation_temp_k'] >= 8000.0
    assert physics['ablation_start_altitude_km'] == 115.0
    assert physics['peak_luminosity_altitude_km'] == 93.0
    assert physics['ablation_end_altitude_km'] == 82.0

    # 4. 持续余迹特征
    assert physics['persistent_train_fraction'] >= 0.45
    assert "[O I]" in physics['persistent_train_fast_line']
    assert "NO + O3" in physics['persistent_train_chem_reaction']


def test_zhr_profile_and_flux_curve():
    """测试基于太阳视黄经的高斯流量模型"""
    zhr_peak, r_peak = compute_zhr_profile(208.50)
    assert zhr_peak == ORIONIDS_PEAK_ZHR
    assert r_peak == 2.50

    # 偏离峰值 3° 黄经
    zhr_off, r_off = compute_zhr_profile(205.50)
    assert zhr_off < zhr_peak
    assert r_off > r_peak


def test_china_observation_windows_completeness():
    """测试华夏五大城市观测几何解算完整性与时序逻辑"""
    windows = compute_china_observation_windows("2026-10-21")
    assert len(windows) == 5
    for city_key in ['shanghai', 'beijing', 'guangzhou', 'chengdu', 'urumqi']:
        assert city_key in windows
        row = windows[city_key]
        assert 'sunset_cst' in row
        assert 'moonset_cst' in row
        assert 'astronomical_dawn_cst' in row
        assert 'radiant_transit_cst' in row
        assert 'culmination_altitude_deg' in row
        assert 'dark_window_hours' in row


def test_moonset_dawn_dark_sky_window():
    """测试核心科学发现：各主要城市独享 2.7~3.1 小时零月光纯黑天窗"""
    windows = compute_china_observation_windows("2026-10-21")
    for city_key, row in windows.items():
        # 月落发生在后半夜 01:30 至 04:00 CST 之间
        assert "01:" in row['moonset_cst'] or "02:" in row['moonset_cst'] or "03:" in row['moonset_cst']
        # 暗空天窗时长在 2.7 至 3.15 小时之间
        assert 2.7 <= row['dark_window_hours'] <= 3.15
        # 月相为盈凸月 (~78%)
        assert row['moon_phase_percent'] > 70.0


def test_transit_culmination_in_dark_window():
    """测试核心科学发现：辐射点最高中天（天顶掠过）100% 严格落在纯黑暗空天窗内"""
    windows = compute_china_observation_windows("2026-10-21")
    for city_key, row in windows.items():
        assert row['is_transit_in_dark_window'] is True


def test_culmination_zenith_geometry():
    """测试各城市中天顶空仰角与大气质量系数"""
    windows = compute_china_observation_windows("2026-10-21")
    # 广州中天仰角高达 82.7°（直插天顶顶心）
    assert windows['guangzhou']['culmination_altitude_deg'] > 82.0
    assert windows['guangzhou']['airmass_transit'] == pytest.approx(1.01, abs=0.02)

    # 上海与成都中天仰角约 74°~76°
    assert windows['shanghai']['culmination_altitude_deg'] > 74.0
    assert windows['chengdu']['culmination_altitude_deg'] > 74.0

    # 北京与乌鲁木齐中天仰角 > 60°
    assert windows['beijing']['culmination_altitude_deg'] > 65.0
    assert windows['urumqi']['culmination_altitude_deg'] > 61.0


def test_generate_full_report_structure():
    """测试全景报告文本生成格式与关键科学结论"""
    dt_cst = datetime(2026, 10, 21, 23, 0, tzinfo=CST_TZ)
    report = generate_full_report(dt_cst)
    assert "1P/Halley" in report
    assert "66.0 km/s" in report
    assert "2.178 GJ/kg" in report
    assert "2061" in report
    assert "上海" in report
    assert "北京" in report
    assert "广州" in report
    assert "成都" in report
    assert "乌鲁木齐" in report
    assert "黄金暗空天窗" in report
