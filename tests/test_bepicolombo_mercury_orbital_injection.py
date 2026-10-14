"""
贝皮可伦坡 (BepiColombo) 水星捕获制动 (MOI) 天体力学推演单元测试集
"""

import sys
import math
from pathlib import Path
from datetime import datetime, timezone, date
import pytest

# 将 scripts 加入 Python 路径
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from bepicolombo_mercury_orbital_injection_engine import (
    get_full_bepicolombo_analysis,
    compute_sun_gravity_well_depth,
    compute_bepicolombo_capture_dynamics,
    compute_science_orbits,
    compute_thermal_flux_environment,
    compute_grand_quad_alignment_2026,
    FLYBY_CHAIN,
    LAUNCH_UTC,
    MTM_SEP_UTC,
    MOI_CAPTURE_UTC,
    MIO_SEPARATION_UTC,
    MOSIF_JETTISON_UTC,
    MPO_FINAL_ORBIT_UTC,
    VOYAGER1_LIGHTDAY_UTC,
    PSP_PERIHELION_P30_UTC,
    CLIPPER_EGA_UTC,
    MERCURY_RADIUS_KM,
    MERCURY_MASS_KG,
    MERCURY_SURFACE_GRAVITY_MS2,
    MERCURY_ESCAPE_VELOCITY_KMS,
    MERCURY_SEMI_MAJOR_AXIS_AU,
    MERCURY_PERIHELION_AU,
    MERCURY_APHELION_AU
)


def test_mission_timeline_and_countdown():
    """验证任务里程碑时间轴与当前关键倒计时 (2026-10-14 锚定)"""
    today = date(2026, 10, 14)
    res = get_full_bepicolombo_analysis(today)

    # 距 2026-09-03 MTM 分离过去 41 天
    assert res["days_post_mtm_separation"] == 41
    # 距 2026-11-21 水星捕获制动 (MOI) 倒计时恰好 38 天
    assert res["days_to_mercury_orbit_insertion"] == 38

    # 验证测控单向与双向光行时时延 (约 11.1 分钟 / 22.2 分钟)
    comm = res["communication_lag"]
    assert comm["earth_distance_au"] == pytest.approx(1.337, abs=0.01)
    assert 11.0 < comm["one_way_light_time_minutes"] < 11.3
    assert 22.0 < comm["round_trip_light_time_minutes"] < 22.6


def test_sun_gravity_well_and_direct_transfer_impossibility():
    """验证太阳引力深阱势能降落与未经助推直接转移的不可行性"""
    well = compute_sun_gravity_well_depth()

    # 掉入水星轨道的比势能释放深达 ~1400 MJ/kg
    assert well["delta_potential_mj_per_kg"] == pytest.approx(-1404.6, abs=5.0)

    # 地球平均公转速度 ~29.78 km/s，水星公转速度 ~47.87 km/s
    assert well["v_earth_circ_kms"] == pytest.approx(29.78, abs=0.1)
    assert well["v_merc_circ_kms"] == pytest.approx(47.87, abs=0.1)

    # 霍曼转移到达水星近日点的日心速度 ~57.48 km/s
    assert well["v_peri_hohmann_kms"] == pytest.approx(57.48, abs=0.1)

    # 直接转移到达时的双曲线无穷远速度 v_inf 高达 ~9.61 km/s
    assert well["v_inf_direct_kms"] == pytest.approx(9.61, abs=0.1)

    # 如此巨大的超速，直接入轨捕获制动 Delta-V 高达 ~6.59 km/s，化学火箭根本无法承受
    assert well["delta_v_direct_capture_kms"] == pytest.approx(6.59, abs=0.1)


def test_flyby_chain_integrity():
    """验证 8 年 9 次行星引力助推剥离链的完备性与拓扑顺序"""
    assert len(FLYBY_CHAIN) == 9

    # 1 地球
    earth_flybys = [f for f in FLYBY_CHAIN if f.body == "Earth"]
    assert len(earth_flybys) == 1
    assert earth_flybys[0].name == "Earth-1"

    # 2 金星
    venus_flybys = [f for f in FLYBY_CHAIN if f.body == "Venus"]
    assert len(venus_flybys) == 2
    assert venus_flybys[0].altitude_km == 10720.0
    assert venus_flybys[1].altitude_km == 552.0

    # 6 水星
    mercury_flybys = [f for f in FLYBY_CHAIN if f.body == "Mercury"]
    assert len(mercury_flybys) == 6
    # 终极第六次飞掠掠过北极 295 km
    assert mercury_flybys[-1].name == "Mercury-6"
    assert mercury_flybys[-1].altitude_km == 295.0


def test_moi_capture_dynamics_and_burn_parameters():
    """验证弱稳定性边界捕获制动力学与 4x22N 推力点火参数"""
    dyn = compute_bepicolombo_capture_dynamics(v_inf_kms=1.84)

    # 经过 9 次飞掠与电推，v_inf 降至 1.84 km/s
    assert dyn["v_inf_kms"] == 1.84

    # 近水点 674 km，远水点 178000 km
    assert dyn["r_periapsis_km"] == pytest.approx(MERCURY_RADIUS_KM + 674.0, abs=0.1)
    assert dyn["r_apoapsis_km"] == pytest.approx(MERCURY_RADIUS_KM + 178000.0, abs=0.1)

    # 初始捕获轨道离心率 ~0.966
    assert dyn["eccentricity"] == pytest.approx(0.966, abs=0.01)

    # 捕获制动 Delta-V 仅需 ~457.9 m/s
    assert dyn["delta_v_capture_ms"] == pytest.approx(457.9, abs=1.0)
    assert dyn["delta_v_capture_kms"] == pytest.approx(0.4579, abs=0.001)

    # 双曲进近速度 4.19 km/s 制动为 3.73 km/s
    assert dyn["v_p_hyperbolic_kms"] == pytest.approx(4.188, abs=0.01)
    assert dyn["v_p_captured_orbit_kms"] == pytest.approx(3.730, abs=0.01)

    # 4 台 22N 双组元推进器总推力 88N 对 2260kg 叠构点火时间约 196 分钟
    assert 190.0 < dyn["burn_time_min"] < 205.0


def test_science_orbits_decoupling():
    """验证 Mio (JAXA) 与 MPO (ESA) 目标科学轨道的双星分工力学"""
    orbits = compute_science_orbits()
    mio = orbits["mio"]
    mpo = orbits["mpo"]

    # Mio 高偏心率大磁层极轨道 (590 x 11640 km, P ~ 9.3h)
    assert mio["pericenter_altitude_km"] == 590.0
    assert mio["apocenter_altitude_km"] == 11640.0
    assert mio["eccentricity"] == pytest.approx(0.646, abs=0.01)
    assert mio["orbital_period_hours"] == pytest.approx(9.30, abs=0.1)
    assert mio["inclination_deg"] == 90.0

    # MPO 低高度近圆极轨道 (480 x 1500 km, P ~ 2.36h)
    assert mpo["pericenter_altitude_km"] == 480.0
    assert mpo["apocenter_altitude_km"] == 1500.0
    assert mpo["eccentricity"] == pytest.approx(0.149, abs=0.01)
    assert mpo["orbital_period_hours"] == pytest.approx(2.36, abs=0.05)
    assert mpo["inclination_deg"] == 90.0

    # 入轨全阶段总 Delta-V 预算 963 m/s
    assert orbits["total_moi_phase_delta_v_budget_ms"] == 963.0


def test_thermal_extremes_and_flux():
    """验证水星极限光热辐射、昼夜温差与反照/红外二次辐射环境"""
    therm = compute_thermal_flux_environment()

    # 水星近日点太阳常数高达 14,394 W/m² (地球的 10.58 倍)
    assert therm["perihelion_solar_flux_w_m2"] == pytest.approx(14394.0, abs=20.0)
    assert therm["perihelion_solar_ratio_to_earth"] == pytest.approx(10.58, abs=0.1)

    # 水星远日点太阳常数 6,249 W/m² (地球的 4.59 倍)
    assert therm["aphelion_solar_flux_w_m2"] == pytest.approx(6249.0, abs=20.0)
    assert therm["aphelion_solar_ratio_to_earth"] == pytest.approx(4.59, abs=0.1)

    # 日下点温度在近日点超过 430°C (705 K)
    assert therm["subsolar_temp_perihelion_c"] > 430.0
    assert therm["subsolar_temp_perihelion_k"] > 700.0

    # 极区永久阴影区 (PSR) 极限低温 90 K (-183°C)
    assert therm["psr_crater_temp_k"] == 90.0
    assert therm["psr_crater_temp_c"] == pytest.approx(-183.15, abs=0.1)

    # 行星表面对低轨航天器底部的二次红外辐射高达 4.4 kW/m²
    assert 4000.0 < therm["mercury_ir_flux_peri_w_m2"] < 5000.0


def test_grand_quad_alignment_late_2026():
    """验证 2026 年秋末深空四极对偶大冲刺之 16 天黄金交汇窗口"""
    align = compute_grand_quad_alignment_2026(date(2026, 10, 14))

    # 4 大事件全部在 2026 年 11-12 月发生
    assert align["days_to_voyager1_lightday"] == 35   # 2026-11-18
    assert align["days_to_bepicolombo_moi"] == 38     # 2026-11-21
    assert align["days_to_psp_perihelion_p30"] == 49  # 2026-12-02
    assert align["days_to_clipper_ega"] == 50         # 2026-12-03

    # 全体四大历史里程碑在 15 天时间跨度 (16 天时间窗口) 内齐聚
    assert align["grand_window_span_days"] == 15
    assert len(align["events"]) == 4

    # 验证四大极端领域覆盖
    names = [e["name"] for e in align["events"]]
    assert "旅行者 1 号 (Voyager 1)" in names[0]
    assert "贝皮可伦坡 (BepiColombo)" in names[1]
    assert "帕克太阳探测器 (PSP)" in names[2]
    assert "欧罗巴快船 (Europa Clipper)" in names[3]


def test_mercury_planetary_invariants():
    """验证水星基础天体动力学与自转共振不变量"""
    assert MERCURY_RADIUS_KM == 2439.7
    assert MERCURY_MASS_KG == pytest.approx(3.3011e23, rel=1e-3)
    assert MERCURY_SURFACE_GRAVITY_MS2 == pytest.approx(3.70, abs=0.05)
    assert MERCURY_ESCAPE_VELOCITY_KMS == pytest.approx(4.25, abs=0.05)

    # 3:2 自转公转轨道共振验证 (58.646 / 87.969 ≈ 2/3)
    ratio = 58.646 / 87.969
    assert ratio == pytest.approx(2.0 / 3.0, abs=1e-3)

    # 太阳日等于整整两个水星年 (176 天 ≈ 2 * 87.969 天)
    assert 176.0 == pytest.approx(2.0 * 87.969, abs=0.1)
