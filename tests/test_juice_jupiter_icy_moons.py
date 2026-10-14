"""
木卫三冰月探测器 (JUICE) 天体力学与 2026 深空六极黄金舰队测试集
========================================================================

验证:
1. 2026-09-28 EGA-2 双曲线掠地弹道解析解 (8,640 km 高空、20° 偏折、v_inf 11.2 km/s、v_p 13.4 km/s、+3.5 km/s 增速)
2. EGA-2 至 EGA-3 共振出向椭圆转移轨道 (845 天、a=1.75 AU、远日点 2.50 AU 主小行星带 223 Rosa 区域)
3. 弱光低温光伏能量转换物理 (85 m² LILT 阵列、5.2 AU 处 50.2 W/m² 极弱通量与千瓦级电能维持)
4. 木卫三 (Ganymede) 空间物理与磁层顶驻点距离 (~2.29 R_G 迷你磁层泡) 及液态大洋储量 (>3.5 倍地球总大洋)
5. 2026 年秋末深空六极 (Grand Sextet) 黄金舰队 66 天时序联立、3770 倍极距跨越与千万倍辐射能流对偶
6. 综合学术报告生成质量与完整性
"""

import sys
import math
from pathlib import Path
from datetime import datetime, timezone
import pytest

# 将 scripts 与项目根目录加入 sys.path
scripts_dir = Path(__file__).parent.parent / "scripts"
repo_dir = Path(__file__).parent.parent
sys.path.insert(0, str(scripts_dir))
sys.path.insert(0, str(repo_dir))

from juice_jupiter_icy_moons_engine import (
    JuiceJupiterIcyMoonsEngine,
    GANYMEDE_RADIUS_KM,
    GANYMEDE_MASS_KG,
    GANYMEDE_SURFACE_GRAVITY_MS2,
    GANYMEDE_EQUATORIAL_B_NT,
    JUPITER_AMBIENT_B_AT_GANYMEDE_NT,
    SOLAR_CONSTANT_1AU,
    EARTH_EQUATORIAL_RADIUS_KM,
)


@pytest.fixture
def engine():
    ref_time = datetime(2026, 10, 14, 20, 0, 0, tzinfo=timezone.utc)
    return JuiceJupiterIcyMoonsEngine(ref_time_utc=ref_time)


def test_ega2_hyperbolic_metrics(engine):
    """测试 2026-09-28 JUICE 第二次掠地引力助推双曲线解析弹道"""
    ega2 = engine.compute_ega2_hyperbolic_metrics(
        altitude_km=8640.0,
        deflection_deg=20.0,
        heliocentric_boost_kms=3.50,
        eclipse_hours=8.65
    )

    # 近地点地心距约 15018 km (2.355 地球半径)
    assert 15010.0 < ega2.perigee_radius_km < 15025.0
    assert 2.35 < ega2.perigee_radius_earth_radii < 2.36

    # 偏转角 20 度与偏心率 e_hyp = 1 / sin(10°) ~ 5.7588
    assert ega2.deflection_angle_deg == 20.0
    assert 5.75 < ega2.hyperbolic_eccentricity < 5.77

    # 渐近双曲线过剩速度 v_inf ~ 11.238 km/s
    assert 11.20 < ega2.hyperbolic_excess_velocity_kms < 11.28

    # 近地点极速 v_p ~ 13.394 km/s (> 48,000 km/h)
    assert 13.35 < ega2.perigee_velocity_kms < 13.45
    assert ega2.perigee_velocity_kmh > 48000.0

    # 地心速度增量矢量大小 ~ 3.903 km/s
    assert 3.85 < ega2.delta_v_vector_magnitude_kms < 3.95

    # 顺向地球公转日心增速 +3.50 km/s
    assert ega2.heliocentric_velocity_boost_kms == 3.50

    # 地影持续时间 8.65 小时
    assert ega2.eclipse_duration_hours == 8.65


def test_outbound_resonant_orbit(engine):
    """测试 EGA-2 至 EGA-3 共振出向椭圆轨道参量"""
    res_orbit = engine.compute_outbound_resonant_orbit(transfer_days=845.0)

    # 转移耗时约 2.313 年
    assert 2.30 < res_orbit.transfer_duration_years < 2.33
    assert res_orbit.transfer_duration_days == 845.0

    # 日心半长轴 a = P^(2/3) ~ 1.749 AU
    assert 1.74 < res_orbit.semi_major_axis_au < 1.76

    # 近日点 1.00 AU，远日点深潜至 ~2.50 AU (主小行星带外缘 223 Rosa 区域)
    assert res_orbit.perihelion_distance_au == 1.000
    assert 2.48 < res_orbit.aphelion_distance_au < 2.52
    assert res_orbit.aphelion_distance_km > 3.7e8

    # 轨道偏心率 e ~ 0.428
    assert 0.42 < res_orbit.orbital_eccentricity < 0.44


def test_photovoltaic_power(engine):
    """测试 1 AU、小行星带远日点与木星 5.2 AU 处的弱光光伏物理"""
    # 1.0 AU 处
    pv_1au = engine.compute_photovoltaic_power(1.0)
    assert pv_1au.solar_flux_wm2 == SOLAR_CONSTANT_1AU
    assert pv_1au.solar_flux_ratio_earth == 1.0
    assert pv_1au.raw_intercepted_power_kw > 110.0
    assert pv_1au.electric_power_output_w > 25000.0

    # 2.498 AU 小行星带远日点
    pv_aph = engine.compute_photovoltaic_power(2.498)
    assert 210.0 < pv_aph.solar_flux_wm2 < 225.0
    assert 0.15 < pv_aph.solar_flux_ratio_earth < 0.17

    # 5.2044 AU 木星轨道
    pv_jup = engine.compute_photovoltaic_power(5.2044)
    # 通量暴跌至 50.25 W/m² (约地球的 3.69%)
    assert 49.5 < pv_jup.solar_flux_wm2 < 51.0
    assert 0.035 < pv_jup.solar_flux_ratio_earth < 0.038
    # 凭借三结 GaAs LILT 电池效率仍能输出超 1000 W
    assert pv_jup.electric_power_output_w > 1000.0
    assert pv_jup.operating_temperature_c < -100.0


def test_ganymede_space_physics(engine):
    """测试木卫三物理特征、内禀发电机迷你磁层与三明治液态大洋储量"""
    phys = engine.compute_ganymede_space_physics()

    # 尺寸超越水星 (水星半径 2439.7 km)
    assert phys.radius_km == 2634.1
    assert phys.radius_km > 2439.7
    assert phys.mass_kg == GANYMEDE_MASS_KG

    # 表面重力约 1.428 m/s^2 (~0.146 g)
    assert 1.42 < phys.surface_gravity_ms2 < 1.44
    assert 0.14 < phys.surface_gravity_earth_g < 0.15

    # 磁层顶驻点距离约 2.25 ~ 2.35 个木卫三半径 (约 6000 km)
    assert 2.25 < phys.magnetopause_standoff_ganymede_radii < 2.35
    assert 5950.0 < phys.magnetopause_standoff_radius_km < 6100.0
    assert 3300.0 < phys.magnetopause_altitude_km < 3500.0

    # 三明治液态大洋总体积超过地球所有大洋总水量的 3.5 倍以上
    assert phys.ocean_layer_thickness_km == 100.0
    assert phys.ocean_volume_m3 > 5.0e18
    assert phys.ocean_to_earth_oceans_ratio > 3.5


def test_grand_sextet_timeline(engine):
    """测试 2026 年秋末深空六极 (The Grand Sextet) 黄金舰队时序与对偶极值"""
    sextet = engine.compute_2026_grand_sextet_timeline()

    # 历史性时间窗口约 66.4 天
    assert 65.0 < sextet.total_window_span_days < 68.0

    # 必须收录完整的现役六大旗舰
    mission_ids = [m.mission_id for m in sextet.missions]
    assert mission_ids == ["juice", "hera", "voyager1", "bepicolombo", "parker", "clipper"]

    # 验证即时状态与倒计时
    # JUICE: 已完成掠地 16 天
    juice_status = next(m for m in sextet.missions if m.mission_id == "juice")
    assert -17.0 < juice_status.countdown_days < -15.0

    # Hera: 明日早晨 BRM-1 点火 (倒计时 < 1 天)
    hera_status = next(m for m in sextet.missions if m.mission_id == "hera")
    assert 0.0 < hera_status.countdown_days < 1.0

    # Voyager 1: 跨越 1 光日 (倒计时 34~36 天)
    v1_status = next(m for m in sextet.missions if m.mission_id == "voyager1")
    assert 34.0 < v1_status.countdown_days < 36.0

    # BepiColombo: 水星捕获 MOI (倒计时 37~39 天)
    bepi_status = next(m for m in sextet.missions if m.mission_id == "bepicolombo")
    assert 37.0 < bepi_status.countdown_days < 39.0

    # Parker: 第 30 次极限近日点 (倒计时 48~50 天)
    parker_status = next(m for m in sextet.missions if m.mission_id == "parker")
    assert 48.0 < parker_status.countdown_days < 50.0

    # Clipper: 地球引力助推掠地 (倒计时 49~51 天)
    clipper_status = next(m for m in sextet.missions if m.mission_id == "clipper")
    assert 49.0 < clipper_status.countdown_days < 51.0

    # 验证物理极限张力
    # 空间极距跨度超 3,700 倍
    assert sextet.distance_dynamic_range_ratio > 3700.0

    # 辐射能流跨度超 14,000,000 倍 (1400 万倍)
    assert sextet.flux_dynamic_range_ratio > 1.4e7

    # 速度跨度超 11 倍
    assert sextet.speed_dynamic_range_ratio > 11.0


def test_comprehensive_report_generation(engine):
    """测试完整推演报告生成与格式规范"""
    report = engine.generate_comprehensive_report()

    assert len(report) > 2000
    assert "木卫三冰月探测器 (JUICE)" in report
    assert "EGA-2" in report
    assert "8640.0" in report
    assert "The Grand Sextet" in report or "深空六极" in report
    assert "旅行者 1 号" in report
    assert "帕克太阳探测器" in report
    assert "欧罗巴快船" in report
    assert "贝皮可伦坡" in report
    assert "赫拉号" in report
    assert "主小行星带" in report
