"""
旅行者 2 号 (Voyager 2) “20 光时” 里程碑与星际动力学测试集
================================================================

8 项严苛物理断言:
1. 20 光时定义严格性检验 (215.85 亿公里 / 144.29 AU / 72,000 秒)
2. 2026-10-16 瞬时地心距离与 20 光时冲线倒计时 (<= 3 天内跨越)
3. 视退行速度公转调制检验 (30 ~ 45 km/s 且日增距超 300 万公里)
4. 双子星天球与空间南北大张角对偶检验 (大圆角距 ~80°，日心黄纬一北一南)
5. 全球 DSN 几何盲区检验 (北半球仰角 < 0°，仅堪培拉 DSS-43 拥有上行发射能力)
6. 堪培拉 DSS-43 X 波段微弱下行链路预算检验 (FSPL > 315 dB，P_rx 在 0.1~1.0 aW 之间且信噪比拥有解码裕度)
7. RTG 钚-238 衰退模型与 2023-2024 电压调节器旁路电能正裕量检验 (P_sci > 20 W)
8. 人类唯一“大四喜”四巨星全访历史时序与星际介质原位 PLS 等离子体穿越检验
"""

import sys
import math
from pathlib import Path
from datetime import datetime, timezone
import pytest

# 将 scripts 加入 Python 路径
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from voyager2_twenty_light_hours_engine import (
    Voyager2TwentyLightHoursEngine,
    TWENTY_LIGHT_HOURS_KM,
    TWENTY_LIGHT_HOURS_AU,
    SPEED_OF_LIGHT,
    AU_KM,
    VOYAGER2_DEC_DEG,
    VOYAGER1_ECLIPTIC_LAT_DEG,
    VOYAGER2_ECLIPTIC_LAT_DEG,
    LAUNCH_UTC,
    JUPITER_FLYBY_UTC,
    SATURN_FLYBY_UTC,
    URANUS_FLYBY_UTC,
    NEPTUNE_FLYBY_UTC,
    HELIOPAUSE_UTC
)


def test_twenty_light_hours_metric_precision():
    """断言 1: 20 光时严格光速定义检验"""
    engine = Voyager2TwentyLightHoursEngine()
    m = engine.compute_light_metrics(20.0)

    expected_km = 20.0 * 3600.0 * SPEED_OF_LIGHT
    assert abs(m.distance_km - expected_km) < 1.0
    assert abs(m.distance_km - 21585056976.0) < 1.0
    assert abs(m.distance_au - 144.2872) < 0.005
    assert m.light_time_seconds == 72000.0
    assert m.one_way_light_time_hours == 20.0
    assert m.round_trip_light_time_hours == 40.0


def test_instantaneous_state_2026_countdown():
    """断言 2: 2026-10-16 瞬时地心距离与 20 光时倒计时"""
    engine = Voyager2TwentyLightHoursEngine(datetime(2026, 10, 16, 6, 0, 0, tzinfo=timezone.utc))
    state = engine.compute_instantaneous_state()

    # 地心距离应在 144.1 ~ 144.3 AU 之间
    assert 144.10 < state.geocentric_distance_au < 144.30
    assert state.one_way_light_time_hours > 19.95
    assert state.one_way_light_time_hours < 20.05

    # 离 20 光时仅差极短距离 (< 1000 万公里)
    assert 0 < state.remaining_distance_to_20lh_km < 10000000.0
    # 冲线倒计时处于极窄窗口 (0.5 ~ 3.0 天内，即 10-17 前后)
    assert 0.5 <= state.days_until_20_light_hours <= 3.0
    assert state.crossing_estimated_utc.year == 2026
    assert state.crossing_estimated_utc.month == 10
    assert state.crossing_estimated_utc.day in [16, 17, 18]


def test_recession_speed_earth_modulation():
    """断言 3: 地球公转调制退行速度检验"""
    engine = Voyager2TwentyLightHoursEngine()
    state = engine.compute_instantaneous_state()

    # 秋季地球背向孔雀座，视退行速度显著高于探测器日心速度 (15.34 km/s)
    assert 35.0 < state.apparent_recession_speed_kms < 42.0
    # 每日地心距离增加 300 ~ 360 万公里
    daily_growth_mkm = state.apparent_recession_speed_kms * 86400.0 / 1e6
    assert 3.0 < daily_growth_mkm < 3.6


def test_dual_probe_angular_geometry():
    """断言 4: Voyager 1 与 Voyager 2 天球与空间南北大张角检验"""
    engine = Voyager2TwentyLightHoursEngine()
    geom = engine.compute_dual_probe_angular_geometry()

    # 天球大圆角距在 75° ~ 85° 之间
    assert 75.0 < geom.great_circle_angle_deg < 85.0
    # 日心黄纬一北一南，且南北倾斜均超过 30°
    assert geom.north_probe_ecliptic_lat > 30.0
    assert geom.south_probe_ecliptic_lat < -30.0
    assert geom.north_probe_ecliptic_lat * geom.south_probe_ecliptic_lat < 0


def test_dsn_global_visibility_and_single_lifeline():
    """断言 5: 全球 DSN 几何盲区与堪培拉 DSS-43 单一发射生命线检验"""
    engine = Voyager2TwentyLightHoursEngine()
    vis_list = engine.evaluate_dsn_visibility()

    goldstone = next(v for v in vis_list if "Goldstone" in v.station_name)
    madrid = next(v for v in vis_list if "Madrid" in v.station_name)
    canberra = next(v for v in vis_list if "Canberra" in v.station_name)

    # 北半球站点完全在地平线以下
    assert not goldstone.is_visible
    assert goldstone.max_elevation_deg < 0.0
    assert not madrid.is_visible
    assert madrid.max_elevation_deg < 0.0

    # 南半球堪培拉站可视且仰角高 (> 60°)
    assert canberra.is_visible
    assert canberra.max_elevation_deg > 60.0
    # 全球仅堪培拉能发射上行指令
    assert canberra.can_transmit_uplink
    assert not goldstone.can_transmit_uplink
    assert not madrid.can_transmit_uplink


def test_rf_link_budget_attenuation():
    """断言 6: 堪培拉 DSS-43 接收 X 波段微弱信号链路预算检验"""
    engine = Voyager2TwentyLightHoursEngine()
    link = engine.compute_rf_link_budget()

    # 路径损耗巨大 (> 315 dB)
    assert 315.0 < link.path_loss_db < 320.0
    # 接收功率在阿瓦 (aW, 10^-18 W) 数量级
    assert 0.1 < link.received_power_attowatts < 1.0
    assert -156.0 < link.received_power_dbm < -150.0
    # 信噪比与解码门限拥有稳健正裕度
    assert link.snr_eb_n0_db > 8.0
    assert link.decoding_margin_db > 5.0


def test_rtg_power_and_reservoir_circuit():
    """断言 7: RTG 衰退动力学与电压调节器旁路电能余量检验"""
    engine = Voyager2TwentyLightHoursEngine()
    pwr = engine.compute_rtg_power_profile()

    # 在轨飞行年数超过 49 年
    assert pwr.years_in_flight > 49.0
    # 热功率剩余率约为 65% ~ 70% (Pu-238 87.7 年半衰期)
    assert 0.65 < pwr.thermal_power_ratio < 0.72
    # 2026 年电功率在 220 ~ 230 W
    assert 220.0 <= pwr.current_electric_power_w <= 230.0
    # 扣除平台基线后拥有正科学余量 (> 20 W)
    assert pwr.science_power_margin_w > 20.0
    assert pwr.is_reservoir_circuit_engaged


def test_grand_tour_and_heliopause_legacy():
    """断言 8: 四巨星大四喜全访与太阳风层顶 PLS 科学遗产检验"""
    # 严格时间序列: 发射 -> 木星 -> 土星 -> 天王星 -> 海王星 -> 日球层顶
    assert LAUNCH_UTC < JUPITER_FLYBY_UTC < SATURN_FLYBY_UTC < URANUS_FLYBY_UTC < NEPTUNE_FLYBY_UTC < HELIOPAUSE_UTC
    assert HELIOPAUSE_UTC.year == 2018
    assert HELIOPAUSE_UTC.month == 11
    assert HELIOPAUSE_UTC.day == 5
