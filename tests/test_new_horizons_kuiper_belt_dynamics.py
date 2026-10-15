"""
新视野号 (New Horizons) 柯伊伯带深空巡航动力学、COB 绝尘测定与
太阳风减速推演引擎单元测试集
"""

import sys
import math
from pathlib import Path
from datetime import datetime, timezone
import pytest

scripts_dir = Path(__file__).parent.parent / "scripts"
repo_dir = Path(__file__).parent.parent
sys.path.insert(0, str(scripts_dir))
sys.path.insert(0, str(repo_dir))

from new_horizons_kuiper_belt_dynamics_engine import (
    calculate_new_horizons_trajectory,
    calculate_deep_space_link_budget,
    calculate_rtg_power_metrics,
    calculate_cosmic_optical_background,
    calculate_solar_wind_pui_metrics,
    calculate_student_dust_counter_metrics,
    generate_grand_decet_fleet_summary
)


def test_trajectory_hyperbolic_escape():
    """验证新视野号双曲线逃逸动力学与星历几何状态"""
    traj = calculate_new_horizons_trajectory()
    assert traj.days_post_launch > 7500.0
    assert 20.0 < traj.years_post_launch < 22.0
    assert 64.0 <= traj.heliocentric_distance_au <= 68.0
    assert 63.0 <= traj.earth_distance_au <= 67.0
    assert 13.0 <= traj.heliocentric_speed_km_s <= 14.5
    assert 2.5 <= traj.heliocentric_annual_rate_au_year <= 3.2
    assert 5.0 <= traj.local_escape_velocity_km_s <= 5.5
    assert traj.is_orbit_hyperbolic is True
    assert 12.0 <= traj.hyperbolic_excess_velocity_km_s <= 13.5
    assert "Sagittarius" in traj.constellation_direction


def test_deep_space_link_budget():
    """验证深空网 (DSN) 65 AU 下行极限微波链路预算"""
    link = calculate_deep_space_link_budget()
    assert 8.8 <= link.one_way_light_time_hours <= 9.5
    assert 17.6 <= link.round_trip_light_time_hours <= 19.0
    assert link.downlink_freq_ghz == pytest.approx(8.438, rel=1e-3)
    assert link.spacecraft_tx_power_w == 12.0
    assert link.spacecraft_tx_power_dbm == pytest.approx(40.79, abs=0.1)
    assert 40.0 <= link.spacecraft_antenna_gain_dbi <= 45.0
    assert 70.0 <= link.ground_antenna_gain_dbi <= 76.0
    assert link.free_space_path_loss_db > 305.0
    assert -165.0 <= link.received_power_dbm <= -145.0
    assert link.typical_downlink_data_rate_bps == 1000.0


def test_rtg_power_metrics():
    """验证 GPHS-RTG 同位素放射性衰变与硅锗热电偶老化退化模型"""
    rtg = calculate_rtg_power_metrics()
    assert rtg.pu238_half_life_years == 87.74
    assert 20.0 <= rtg.mission_elapsed_years <= 22.0
    assert 3600.0 <= rtg.current_thermal_power_w <= 3800.0
    assert 0.82 <= rtg.thermal_power_remaining_ratio <= 0.88
    assert 0.80 <= rtg.thermocouple_degradation_factor <= 0.90
    assert 165.0 <= rtg.current_electric_power_w <= 190.0
    assert rtg.avionics_baseline_power_w == 115.0
    assert rtg.twta_tx_power_draw_w == 32.0
    assert rtg.science_power_margin_w > 0.0


def test_cosmic_optical_background():
    """验证宇宙光学背景 (COB) 绝尘测定与黄道光百万倍消退机制"""
    cob = calculate_cosmic_optical_background()
    assert cob.heliocentric_distance_au >= 65.0
    assert cob.inner_solar_system_zodiacal_light_1au_nw_m2_sr == 150.0
    assert cob.zodiacal_attenuation_factor > 900000.0
    assert cob.local_zodiacal_light_nw_m2_sr < 0.001
    assert cob.integrated_galactic_light_nw_m2_sr == 8.2
    assert cob.total_measured_diffuse_flux_nw_m2_sr == 17.5
    assert 8.5 <= cob.unexplained_excess_flux_nw_m2_sr <= 10.0
    assert cob.excess_fraction_of_known_galaxies_pct > 100.0
    assert "未解超额" in cob.scientific_implication


def test_solar_wind_pui_metrics():
    """验证太阳风拾起离子 (PUI) 质量加载与外日球层宏观减速动量守恒"""
    pui = calculate_solar_wind_pui_metrics()
    assert pui.heliocentric_distance_au >= 65.0
    assert pui.vlism_neutral_h_density_m3 == pytest.approx(1.0e5)
    assert 0.15 <= pui.momentum_attenuation_optical_depth <= 0.25
    assert 340.0 <= pui.current_solar_wind_speed_km_s <= 380.0
    assert 60.0 <= pui.speed_drop_km_s <= 90.0
    assert 15.0 <= pui.speed_drop_percentage <= 22.0
    assert "Termination Shock" in pui.dynamical_significance


def test_student_dust_counter_metrics():
    """验证学生尘埃计数器 (SDC) 柯伊伯带尘埃通量与第二扩展环"""
    sdc = calculate_student_dust_counter_metrics()
    assert sdc.sensor_area_m2 == 0.10
    assert sdc.measured_impact_rate_per_day > 1.8
    assert sdc.measured_impact_rate_per_day / sdc.expected_cliff_impact_rate_per_day > 20.0
    assert sdc.estimated_kbo_dust_density_m3 > 1.0e-9
    assert sdc.inferred_disk_outer_boundary_au >= 75.0
    assert "80 AU" in sdc.paradigm_shift_summary


def test_grand_decet_fleet_summary():
    """验证 2026 人类深空十极黄金舰队 (The Grand Decet) 完整覆盖体系"""
    fleet = generate_grand_decet_fleet_summary()
    assert len(fleet) == 10
    ranks = [m["rank"] for m in fleet]
    assert ranks == list(range(1, 11))

    names = [m["name"] for m in fleet]
    assert any("旅行者 1 号" in n for n in names)
    assert any("新视野号" in n for n in names)
    assert any("JUICE" in n for n in names)
    assert any("Europa Clipper" in n for n in names)
    assert any("Psyche" in n for n in names)
    assert any("Hera" in n for n in names)
    assert any("Tianwen-2" in n for n in names)
    assert any("JWST" in n for n in names)
    assert any("BepiColombo" in n for n in names)
    assert any("Parker" in n for n in names)


def test_extreme_physical_span_decet():
    """验证人类深空十极黄金舰队在空间、能流、速度与温差维度的极端跨度"""
    fleet = generate_grand_decet_fleet_summary()
    v1 = next(m for m in fleet if "旅行者 1 号" in m["name"])
    psp = next(m for m in fleet if "Parker" in m["name"])
    nh = next(m for m in fleet if "新视野号" in m["name"])

    # 日心极距跨度比 (Voyager 1 173.22 AU vs PSP 0.046 AU)
    distance_ratio = v1["distance_au"] / psp["distance_au"]
    assert distance_ratio > 3700.0

    # 太阳辐射能流反平方律极端跨度 (PSP 近日点 0.046 AU vs Voyager 1 173.22 AU)
    flux_psp = 1361.0 / (psp["distance_au"] ** 2)
    flux_v1 = 1361.0 / (v1["distance_au"] ** 2)
    flux_ratio = flux_psp / flux_v1
    assert flux_ratio > 1.4e7  # 超过 1400 万倍！

    # 速度极值比 (PSP 192 km/s vs New Horizons 13.68 km/s)
    speed_ratio = psp["speed_km_s"] / nh["speed_km_s"]
    assert speed_ratio > 13.0
