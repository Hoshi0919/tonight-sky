"""
测试旅行者 1 号 (Voyager 1) “一光日” 跨越与星际天体力学推演引擎
"""

import sys
import math
from pathlib import Path
from datetime import datetime, timezone, timedelta
import pytest

# 将 scripts 加入 Python 路径
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from voyager1_one_light_day_engine import (
    SPEED_OF_LIGHT,
    SECONDS_PER_DAY,
    AU_KM,
    LIGHT_DAY_KM,
    LIGHT_DAY_AU,
    MILESTONE_ONE_LIGHT_DAY_UTC,
    get_light_day_metric,
    compute_geocentric_state,
    compute_link_budget,
    compute_rtg_timeline,
    get_interstellar_chronology,
    generate_full_voyager1_report
)


def test_light_day_metric_constants():
    """验证一光日基准物理定义与单位换算"""
    metric = get_light_day_metric()
    expected_km = SPEED_OF_LIGHT * SECONDS_PER_DAY
    assert math.isclose(metric.distance_km, expected_km, rel_tol=1e-9)
    assert math.isclose(metric.distance_au, expected_km / AU_KM, rel_tol=1e-7)
    assert metric.light_time_seconds == 86400.0
    assert metric.one_way_light_time_hours == 24.0
    assert metric.round_trip_light_time_hours == 48.0
    # 距离在 259 亿公里量级
    assert 2.590e10 < metric.distance_km < 2.591e10
    # 约 173.14 AU
    assert 173.14 < metric.distance_au < 173.15


def test_milestone_exact_crossing():
    """验证 2026-11-18 10:16:07 UTC 精确交会达标"""
    state = compute_geocentric_state(MILESTONE_ONE_LIGHT_DAY_UTC)
    assert math.isclose(state.geocentric_distance_km, LIGHT_DAY_KM, abs_tol=1.0)
    assert math.isclose(state.one_way_light_time_sec, 86400.0, abs_tol=1e-3)
    assert state.days_to_one_light_day == 0.0
    assert "24h 00m 00.0s" == state.one_way_light_time_str
    assert "48h 00m 00.0s" == state.round_trip_light_time_str
    assert state.timestamp_cst.hour == 18
    assert state.timestamp_cst.minute == 16


def test_current_state_october_2026():
    """验证 2026 年 10 月中旬即时状态与倒计时"""
    oct_13 = datetime(2026, 10, 13, 23, 5, 0, tzinfo=timezone(timedelta(hours=8)))
    state = compute_geocentric_state(oct_13)
    
    # 倒计时应在 35~36 天区间
    assert 35.0 < state.days_to_one_light_day < 36.0
    # 地心距离在 257.5 亿公里至 258.5 亿公里之间
    assert 2.57e10 < state.geocentric_distance_km < 2.585e10
    # 单向光时已超过 23 小时 50 分钟
    assert state.one_way_light_time_sec > 23.8 * 3600
    # 地心视退行速度在秋季远离叠加下为 36~38 km/s
    assert 36.0 < state.geocentric_velocity_kms < 38.0
    # 每日地心距离增长约 300~350 万公里
    assert 3.0e6 < state.daily_distance_gain_km < 3.5e6


def test_link_budget_physics():
    """验证 X 波段 8.415 GHz 射频链路预算与阿瓦级接收功率"""
    lb = compute_link_budget(LIGHT_DAY_KM)
    
    assert lb.frequency_ghz == 8.415
    assert math.isclose(lb.wavelength_cm, 3.563, rel_tol=1e-2)
    # 自由空间路径损耗应在 319 dB 附近 (极其巨大)
    assert 318.0 < lb.free_space_loss_db < 321.0
    # 探测器发射功率 22.4 W
    assert lb.tx_power_w == 22.4
    # 地面 70m 天线接收电平应在 -156 至 -153 dBm
    assert -156.0 < lb.received_power_dbm < -153.0
    # 功率换算为阿瓦 (10^-18 W)，应在 0.2 ~ 0.6 aW
    assert 0.2 < lb.received_power_attowatts < 0.6
    # 在 160 bps 下，Eb/N0 应有正余量 (> 2.0 dB)
    assert lb.eb_n0_db > 8.0
    assert lb.link_margin_db > 2.0


def test_rtg_decay_timeline():
    """验证 RTG 钚-238 能源衰减与使命终章时间表"""
    rtg = compute_rtg_timeline(2026.78)
    
    assert rtg.initial_power_w == 470.0
    assert rtg.power_2026_w == 223.0
    # 每年衰减约 3.5 ~ 4.2 W
    assert 3.5 <= rtg.annual_loss_w <= 4.2
    # 最后一台科学仪器关闭在 2029~2033 年窗口
    assert 2029 <= rtg.estimated_science_cutoff_year <= 2033
    # 最终发射机静默在 2033~2037 年窗口
    assert 2033 <= rtg.estimated_silence_year <= 2037
    # 累计服役年数已近半个世纪
    assert rtg.total_mission_years > 48.5


def test_interstellar_chronology():
    """验证极长纪元奥尔特云穿越与恒星遭遇"""
    ch = get_interstellar_chronology()
    
    # 日球层顶穿越在 121.6 AU
    assert math.isclose(ch.heliopause_crossing_au, 121.6, abs_tol=0.5)
    # 内奥尔特云抵达约在公元 2200~2350 年
    assert 2200 <= ch.oort_cloud_inner_calendar_year <= 2350
    # 穿越奥尔特云耗时 2.0 万~3.5 万年
    assert 20000.0 < ch.oort_cloud_transit_duration_years < 35000.0
    # 掠过红矮星 Gliese 445 距离约 1.5~1.8 光年，耗时约 4 万年
    assert 1.5 < ch.gliese_445_encounter_distance_ly < 1.8
    assert math.isclose(ch.gliese_445_encounter_years, 40000.0, rel_tol=0.1)
    # 银河公转周期约 2.0~2.5 亿年
    assert 200.0 <= ch.galactic_orbit_period_myr <= 250.0
    # 金唱片物理寿命达 10 亿年
    assert ch.golden_record_durability_gyr >= 1.0


def test_full_report_generation():
    """验证报告数据生成与无异常执行"""
    rep = generate_full_voyager1_report()
    assert "light_metric" in rep
    assert "current_state" in rep
    assert "milestone_state" in rep
    assert "link_budget" in rep
    assert "rtg_timeline" in rep
    assert "chronology" in rep
    assert rep["current_state"].geocentric_distance_km > 2.5e10
