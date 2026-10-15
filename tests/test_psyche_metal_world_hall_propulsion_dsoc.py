"""
单元测试：灵神星探测器 (Psyche) 金属世界探测、霍尔电推 (SEP) 与深空光通信 (DSOC) 量子光子链路引擎
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

from psyche_metal_world_hall_propulsion_dsoc_engine import (
    calculate_psyche_asteroid_properties,
    calculate_hall_propulsion_metrics,
    calculate_dsoc_photon_link,
    calculate_psyche_cruise_coordinates,
    generate_grand_nonet_fleet_summary,
    AU_KM,
    C_LIGHT_KM_S
)


def test_psyche_asteroid_properties():
    """测试 (16) Psyche 目标天体物理特性与微行星金属核参数"""
    props = calculate_psyche_asteroid_properties()

    # 轨道要素
    assert math.isclose(props.semi_major_axis_au, 2.924, rel_tol=1e-3)
    assert math.isclose(props.eccentricity, 0.134, rel_tol=1e-3)
    assert math.isclose(props.inclination_deg, 3.095, rel_tol=1e-3)
    assert math.isclose(props.orbital_period_years, 5.0, rel_tol=0.05)

    # 三轴尺度与平均直径
    assert props.triaxial_dimensions_km == (279.0, 232.0, 189.0)
    assert 225.0 < props.mean_diameter_km < 235.0

    # 质量与密度 (金属富集 M 型小行星，体密度明显高于普通硅酸盐碎石堆 ~2000 kg/m³)
    assert math.isclose(props.mass_kg, 2.41e19, rel_tol=1e-3)
    assert 3500.0 < props.density_kg_m3 < 4200.0

    # 表面重力与逃逸速度
    assert 0.11 < props.surface_gravity_m_s2 < 0.14
    assert 0.010 < props.surface_gravity_g < 0.015
    assert 150.0 < props.escape_velocity_m_s < 180.0


def test_hall_electric_propulsion_mechanics():
    """测试 SPT-140 霍尔效应电推进工质动力学与推力加速度"""
    hall = calculate_hall_propulsion_metrics(current_mass_kg=2320.0, target_dv_m_s=4500.0)

    # 推进器推力与功率
    assert hall.thrust_mN == 240.0
    assert math.isclose(hall.thrust_N, 0.24, rel_tol=1e-4)
    assert hall.input_power_kw == 4.5

    # 比冲与排气速度 (比冲 1800s，排气速度约 17.65 km/s，为化学火箭的近 6 倍)
    assert hall.specific_impulse_s == 1800.0
    assert math.isclose(hall.exhaust_velocity_m_s, 17652.0, rel_tol=1e-3)

    # 工质质量流率与每日消耗 (每日消耗约 1.175 kg 氙气)
    assert 1.3e-5 < hall.mass_flow_rate_kg_s < 1.4e-5
    assert 1.15 < hall.daily_xenon_consumption_kg < 1.20

    # 实时加速度与日化速度增量
    assert 0.09 < hall.current_accel_mm_s2 < 0.12
    assert 8.5 < hall.daily_delta_v_m_s < 9.5


def test_tsiolkovsky_propellant_efficiency_comparison():
    """测试齐奥尔科夫斯基公式下电推进对比双元化学推进的革命性节油效应"""
    hall = calculate_hall_propulsion_metrics(current_mass_kg=2320.0, target_dv_m_s=4500.0)

    # 霍尔电推进工质占比仅约 22.5%
    assert 20.0 < hall.hall_propellant_fraction_pct < 25.0

    # 传统双元化学推进剂占比高达 77.2%
    assert 75.0 < hall.chemical_propellant_fraction_pct < 80.0

    # 节省推进剂质量超过 1.2 吨 (约 1270 kg)
    assert hall.propellant_mass_saving_kg > 1200.0


def test_dsoc_photon_energy_and_beam_divergence():
    """测试 DSOC 1550nm 激光光子能量、微弧度衍射极限与射频发散角对比"""
    dsoc = calculate_dsoc_photon_link(earth_distance_au=2.684)

    # 光波长与光子能量 (1550 nm, ~193.4 THz, ~0.80 eV)
    assert dsoc.wavelength_nm == 1550.0
    assert math.isclose(dsoc.optical_frequency_thz, 193.4, rel_tol=1e-2)
    assert math.isclose(dsoc.photon_energy_ev, 0.80, rel_tol=1e-2)

    # 22 cm 发射口径衍射发散角 (~8.60 μrad，即 1.77 角秒)
    assert 8.0 < dsoc.beam_divergence_urad < 9.0
    assert 1.6 < dsoc.beam_divergence_arcsec < 1.9

    # 相比 8.4 GHz X 频段深空微波天线，光束聚焦集中度提高 1600 倍以上
    assert dsoc.divergence_reduction_factor > 1500.0


def test_dsoc_link_budget_at_2_684_au():
    """测试在 2.684 AU 极限距离处帕洛马山 200 英寸单光子链路预算与数据率"""
    dsoc = calculate_dsoc_photon_link(earth_distance_au=2.684)

    # 地心距离约 4.015 亿公里
    assert 4.0e8 < dsoc.earth_distance_km < 4.05e8

    # 地面光斑半径约 1726 km (光斑面积约 9.35e12 m²)
    assert 1600.0 < dsoc.spot_radius_km < 1850.0
    assert 8.0e12 < dsoc.spot_area_m2 < 1.1e13

    # 帕洛马山 5.08 米海尔望远镜接收功率约 4.33 pW
    assert 3.5 < dsoc.received_power_pw < 5.5

    # 光子到达速率超 3000 万光子/秒 (约 33.8 Mphotons/s)
    assert 30.0 < dsoc.photon_arrival_rate_m_photons_s < 40.0

    # 支持超 10 Mbps 宽带下行，较传统微波 100 kbps 提升超百倍
    assert dsoc.achievable_data_rate_mbps > 10.0
    assert dsoc.bandwidth_gain_factor > 100.0


def test_psyche_cruise_coordinates_and_solar_power():
    """测试 2026-10-15 巡航时空状态、双向光行时与 75 m² 太阳帆板输出电功率"""
    ref_time = datetime(2026, 10, 15, 8, 0, 0, tzinfo=timezone.utc)
    coord = calculate_psyche_cruise_coordinates(ref_time_utc=ref_time)

    # 时间里程碑 (距发射约 1098 天，距火星借力约 153 天，距抵达约 1021 天)
    assert 1090.0 < coord.days_post_launch < 1110.0
    assert 150.0 < coord.days_post_mars_flyby < 156.0
    assert 1000.0 < coord.days_to_arrival < 1050.0

    # 日心距与地心距
    assert math.isclose(coord.heliocentric_distance_au, 2.042, rel_tol=1e-3)
    assert math.isclose(coord.earth_distance_au, 2.684, rel_tol=1e-3)

    # 单向光行时约 22.3 分钟，双向往返约 44.6 分钟
    assert 21.0 < coord.one_way_light_time_min < 24.0
    assert 42.0 < coord.round_trip_light_time_min < 48.0

    # 太阳辐射能流与 75 m² 太阳电池阵输出功率 (在 2.04 AU 仍有 > 7 kW，完全满足 4.5 kW 电推需求)
    assert 310.0 < coord.solar_flux_w_m2 < 340.0
    assert 6.5 < coord.solar_array_power_kw < 8.5


def test_grand_nonet_fleet_completeness():
    """测试 2026 人类深空九极黄金舰队 (The Grand Nonet) 宏伟矩阵完备性与极值跨度"""
    fleet = generate_grand_nonet_fleet_summary()

    # 必须包含整整 9 艘旗舰探测器
    assert len(fleet) == 9

    ranks = [m["rank"] for m in fleet]
    assert ranks == list(range(1, 10))

    names = [m["name"] for m in fleet]
    assert any("旅行者 1 号" in n for n in names)
    assert any("帕克太阳探测器" in n for n in names)
    assert any("贝皮可伦坡" in n for n in names)
    assert any("赫拉号" in n for n in names)
    assert any("欧罗巴快船" in n for n in names)
    assert any("JUICE" in n for n in names)
    assert any("詹姆斯·韦伯" in n for n in names)
    assert any("天问二号" in n for n in names)
    assert any("灵神星探测器" in n for n in names)

    # 空间极距跨度：
    # 标称距离最小为 JWST (0.010 AU 地心距)，最大为旅行者 1 号 (173.22 AU)，跨度超 17,000 倍
    min_dist = min(m["distance_au"] for m in fleet)
    max_dist = max(m["distance_au"] for m in fleet)
    assert min_dist == 0.010
    assert max_dist == 173.22
    assert (max_dist / min_dist) > 17000.0

    # 日心极距对比：帕克 (0.046 AU) 到旅行者 1 号 (173.22 AU)，跨度超 3700 倍
    parker_dist = next(m["distance_au"] for m in fleet if "帕克" in m["name"])
    assert parker_dist == 0.046
    assert (max_dist / parker_dist) > 3700.0

    # 速度极值跨度：JWST (0.2 km/s) 到帕克 (192 km/s)，跨度达 960 倍
    min_speed = min(m["speed_km_s"] for m in fleet)
    max_speed = max(m["speed_km_s"] for m in fleet)
    assert min_speed == 0.2
    assert max_speed == 192.0
    assert (max_speed / min_speed) == 960.0


def test_mission_phase_and_timelines():
    """测试关键任务时间序列与阶段转移的单调递增性"""
    coord = calculate_psyche_cruise_coordinates()

    assert coord.launch_date_utc < coord.mars_flyby_date_utc
    assert coord.mars_flyby_date_utc < coord.cruise2_start_date_utc
    assert coord.cruise2_start_date_utc < coord.ref_time_utc
    assert coord.ref_time_utc < coord.arrival_date_utc
