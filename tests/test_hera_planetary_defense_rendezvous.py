"""
赫拉号 (Hera) 行星防御双小行星交会与 2026 秋末深空五极黄金大冲刺测试集
========================================================================
验证:
1. Didymos 微重力场、逃逸速度与自转临界瓦解极限
2. Dimorphos 极微重力、9.2 cm/s 逃逸速度与伴星希尔球撕裂约束 (<200 m)
3. DART 动能撞击动能 (~10.9 GJ) 与超音速动量传递
4. 开普勒周期缩短 (32.8 min)、轨道半长轴缩水 (36.4 m) 与反冲增强因子 beta (2.2 ~ 4.0)
5. 赫拉号 10-15 BRM-1 制动点火 (93 分钟, 30N 推力, Delta_V ~ 190 m/s)
6. BRM-2 补充精修制动 (31 分钟, Delta_V ~ 67 m/s)
7. 2026 年秋末人类深空五极黄金大冲刺 (Grand Quintet) 50 天时序与距离对偶
8. 综合推演报告生成与格式完整性
"""

import math
from datetime import datetime, timezone
import pytest

from scripts.hera_planetary_defense_rendezvous_engine import (
    HeraPlanetaryDefenseRendezvousEngine,
    DIDYMOS_DIAMETER_M,
    DIDYMOS_MASS_KG,
    DIDYMOS_ROTATION_PERIOD_HOURS,
    DIMORPHOS_DIAMETER_M,
    DIMORPHOS_MASS_KG,
    DART_SPACECRAFT_MASS_KG,
    DART_IMPACT_SPEED_MS,
    DART_PERIOD_REDUCTION_SECONDS,
    DART_PRE_SEMI_MAJOR_AXIS_M,
)


@pytest.fixture
def engine():
    ref_time = datetime(2026, 10, 14, 16, 0, 0, tzinfo=timezone.utc)
    return HeraPlanetaryDefenseRendezvousEngine(ref_time_utc=ref_time)


def test_didymos_system_microgravity(engine):
    """测试主星 Didymos 表面重力、逃逸速度与极速自转临界瓦解特征"""
    metrics = engine.compute_asteroid_microgravity_metrics()

    # 表面重力 ~ 0.000228 m/s^2 (约 0.023 mG)
    assert 0.00020 < metrics.didymos_surface_gravity_ms2 < 0.00025
    assert 0.020 < metrics.didymos_surface_gravity_milli_g < 0.026

    # 表面逃逸速度 ~ 0.422 m/s
    assert 0.40 < metrics.didymos_escape_velocity_ms < 0.45

    # 自转周期 2.26 小时，临界瓦解周期约 2.28 小时 (极其接近离心瓦解边缘)
    assert 2.25 < DIDYMOS_ROTATION_PERIOD_HOURS < 2.27
    assert 2.15 < metrics.didymos_spin_critical_period_hours < 2.40

    # 赤道自转线速度约 0.30 m/s
    assert 0.28 < metrics.didymos_equatorial_spin_velocity_ms < 0.32


def test_dimorphos_microgravity_and_hill_sphere(engine):
    """测试伴星 Dimorphos 极微重力与极为狭窄的伴星希尔球约束"""
    metrics = engine.compute_asteroid_microgravity_metrics()

    # 表面重力 ~ 5.6e-5 m/s^2 (约 0.0057 mG)
    assert 5.0e-5 < metrics.dimorphos_surface_gravity_ms2 < 6.5e-5

    # 表面逃逸速度 ~ 0.092 m/s (9.2 cm/s)
    assert 0.085 < metrics.dimorphos_escape_velocity_ms < 0.100

    # 双星系统在日心轨道 (1.644 AU) 上的希尔半径 ~ 109.4 km
    assert 100.0 < metrics.system_hill_radius_km < 120.0

    # Dimorphos 相对主星的伴星希尔半径 ~ 171.6 m (仅比星体半径 75.5m 大不到 100m)
    assert 150.0 < metrics.dimorphos_hill_radius_m < 190.0

    # 撞击前公转速度 ~ 17.2 cm/s
    assert 0.16 < metrics.dimorphos_orbital_speed_pre_ms < 0.19


def test_dart_impact_energy_and_momentum(engine):
    """测试 DART 航天器动能撞击能量与动量"""
    dart = engine.compute_dart_impact_kinematics()

    # 撞击质量 580 kg，速度 6.14 km/s
    assert DART_SPACECRAFT_MASS_KG == 580.0
    assert DART_IMPACT_SPEED_MS == 6140.0

    # 动能 ~ 10.93 GJ (约 2.61 吨 TNT)
    assert 1.05e10 < dart.impact_energy_joules < 1.15e10
    assert 2.50 < dart.impact_energy_tnt_equivalent_tons < 2.75

    # 撞击初始动量 ~ 3.56e6 kg*m/s
    assert 3.50e6 < dart.dart_initial_momentum_kg_ms < 3.65e6


def test_dart_orbital_shrinkage_and_beta(engine):
    """测试 DART 撞击引起开普勒半长轴收缩与反冲动量增强因子 beta"""
    dart = engine.compute_dart_impact_kinematics()

    # 周期缩短 32.8 分钟 (1968 秒)
    assert abs(dart.orbital_period_reduction_minutes - 32.8) < 0.1

    # 开普勒半长轴缩水 ~ 36.4 米 (由 1180 m 减至 ~1143.6 m)
    assert 35.0 < dart.orbital_semi_major_axis_shrinkage_m < 38.0
    assert 1140.0 < dart.post_impact_semi_major_axis_m < 1146.0

    # 瞬时轨道减速增量 ~ 2.76 mm/s
    assert 0.0020 < dart.dimorphos_orbit_speed_delta_ms < 0.0035

    # 动量增强因子 beta 处于真实科学标定区间 [2.2, 4.0] (理论名义计算 ~3.7)
    assert 2.2 < dart.beta_momentum_enhancement_factor < 4.0


def test_hera_brm1_propulsion_and_delta_v(engine):
    """测试赫拉号明日 (10-15) BRM-1 主制动点火物理参量"""
    brm = engine.compute_hera_brm1_manoeuvre()

    # 点火时间 93.0 分钟 = 5580 秒
    assert brm.burn_duration_minutes == 93.0
    assert brm.burn_duration_seconds == 5580.0

    # 3 台 10N 轨控推力器同时点火，总推力 30.0 N
    assert brm.total_thrust_n == 30.0
    # 总冲量 167.4 kN*s
    assert abs(brm.total_impulse_ns - 167400.0) < 1.0

    # 消耗推进剂 ~ 75.9 kg 肼
    assert 72.0 < brm.propellant_consumed_kg < 80.0

    # 理论速度变化量 Delta_V 位于 180 ~ 200 m/s (与 ESA 官方公布的数百年速度减量完全吻合)
    assert 180.0 < brm.theoretical_delta_v_ms < 200.0


def test_hera_brm2_refinement(engine):
    """测试赫拉号 BRM-2 (10-22) 补充精修点火参量"""
    brm = engine.compute_hera_brm1_manoeuvre()

    # BRM-2 点火 31.0 分钟
    assert brm.brm2_burn_duration_minutes == 31.0

    # 速度增量 Delta_V ~ 65 ~ 72 m/s
    assert 60.0 < brm.brm2_theoretical_delta_v_ms < 75.0


def test_deep_space_quintet_chronology(engine):
    """测试 2026 年秋末人类深空五极黄金大冲刺矩阵时序与空间跨度"""
    quintet = engine.get_deep_space_quintet_schedule()

    # 包含全部 5 大探测器
    assert len(quintet) == 5

    # 验证按时间先后严格排序
    for i in range(len(quintet) - 1):
        assert quintet[i].milestone_utc <= quintet[i+1].milestone_utc

    # 验证冲刺时间窗口紧密 (从 10-15 到 12-03 全部发生于 51 天之内)
    first_event = quintet[0]
    last_event = quintet[-1]
    span_days = (last_event.milestone_utc - first_event.milestone_utc).total_seconds() / 86400.0
    assert 45.0 < span_days < 52.0

    # 验证日心距离跨越 4 个数量级 (帕克 0.046 AU 到 旅行者1号 173.22 AU)
    min_dist = min(q.heliocentric_distance_au for q in quintet)
    max_dist = max(q.heliocentric_distance_au for q in quintet)
    assert min_dist < 0.05
    assert max_dist > 170.0
    assert (max_dist / min_dist) > 3700.0


def test_summary_report_generation(engine):
    """测试综合推演报告生成与关键内容包含完整性"""
    report = engine.get_summary_report()

    assert "赫拉号 (Hera) 行星防御双小行星交会" in report
    assert "Didymos" in report
    assert "Dimorphos" in report
    assert "DART 动能撞击力学" in report
    assert "BRM-1 初始主制动点火" in report
    assert "深空五极黄金大冲刺" in report
    assert "旅行者 1 号" in report
    assert "贝皮可伦坡" in report
    assert "帕克太阳探测器" in report
    assert "欧罗巴快船" in report
    assert len(report.splitlines()) > 35
