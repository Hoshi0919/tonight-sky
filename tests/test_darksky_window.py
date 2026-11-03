import sys
from pathlib import Path
import datetime
import pytest

scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from autumn_darksky_window import (
    make_observer,
    calculate_night_window,
    calculate_target_visibility,
    run_transition_analysis,
    CST,
)


def test_observer_and_twilight_hierarchy():
    """验证昏影序列严格单调递增：日落 < 民用昏影 < 航海昏影 < 天文昏影"""
    obs = make_observer(lat="31.2304", lon="121.4737")
    date_cst = datetime.date(2026, 10, 1)
    win = calculate_night_window(obs, date_cst)

    assert win["sunset"] < win["civil_dusk"]
    assert win["civil_dusk"] < win["nautical_dusk"]
    assert win["nautical_dusk"] < win["astro_dusk"]


def test_dark_sky_window_growth():
    """验证中秋望月后无月暗夜窗口逐日单调扩张"""
    obs = make_observer(lat="31.2304", lon="121.4737")

    win_0928 = calculate_night_window(obs, datetime.date(2026, 9, 28))
    win_0930 = calculate_night_window(obs, datetime.date(2026, 9, 30))
    win_1001 = calculate_night_window(obs, datetime.date(2026, 10, 1))
    win_1004 = calculate_night_window(obs, datetime.date(2026, 10, 4))

    # 09-28 强月光通宵
    assert win_0928["dark_window_minutes"] == 0.0
    # 09-30 初显暗空 (>30 分钟)
    assert win_0930["dark_window_minutes"] > 30.0
    # 10-01 超过 1.5 小时
    assert win_1001["dark_window_hours"] >= 1.5
    # 10-04 土星冲日当晚超过 4.5 小时
    assert win_1004["dark_window_hours"] >= 4.5
    # 验证单调增长
    assert win_0930["dark_window_minutes"] < win_1001["dark_window_minutes"]
    assert win_1001["dark_window_minutes"] < win_1004["dark_window_minutes"]


def test_m31_transit_altitude():
    """验证仙女座大星系 M31 在 31.2°N 纬度下的中天仰角接近 80°"""
    obs = make_observer(lat="31.2304", lon="121.4737")
    dt = datetime.datetime(2026, 10, 4, 21, 0, tzinfo=CST)
    tgts = calculate_target_visibility(obs, dt)

    assert "M31" in tgts
    m31 = tgts["M31"]
    # M31 赤纬 +41°16'，在 31.23°N 观测中天仰角 = 90 - (41.27 - 31.23) = 79.96°
    assert 78.0 <= m31["meridian_transit_alt_deg"] <= 81.0
    assert m31["visible"] is True


def test_saturn_opposition_window_metrics():
    """验证 2026-10-04 土星冲日当夜指标与暗空匹配度"""
    obs = make_observer(lat="31.2304", lon="121.4737")
    win = calculate_night_window(obs, datetime.date(2026, 10, 4))

    # 月出在子夜前夕 (23:45 以后)，暗空窗口超过 4 小时
    assert win["dark_window_hours"] > 4.5
    assert win["moon_illum_pct"] < 50.0  # 下弦亏月
    assert win["status"].startswith("PRISTINE")

    # 验证当晚 21:00 土星处于极佳仰角
    dt = datetime.datetime(2026, 10, 4, 21, 0, tzinfo=CST)
    tgts = calculate_target_visibility(obs, dt)
    sat = tgts["Saturn"]
    assert sat["altitude_deg"] > 40.0
    assert sat["mag"] <= 0.40  # 冲日最亮期


def test_full_pipeline_run_and_json():
    """验证全周期推演执行与结构化字典完备性"""
    res = run_transition_analysis("2026-09-28", days=7)
    assert len(res["nights"]) == 7
    first = res["nights"][0]
    assert first["date"] == "2026-09-28"
    assert "targets_at_sample" in first
    assert "M31" in first["targets_at_sample"]
    assert "Saturn" in first["targets_at_sample"]


def test_overnight_midnight_crossing_window_and_targets():
    """验证跨午夜月出（如 11 月上旬）暗夜窗口推演与目标仰角计算，防止采样时刻倒退至日间"""
    res = run_transition_analysis("2026-11-03", days=2)
    assert len(res["nights"]) == 2
    n1103 = res["nights"][0]
    assert n1103["date"] == "2026-11-03"
    assert n1103["dark_window_hours"] > 6.0
    assert n1103["status"].startswith("PRISTINE")

    # 采样时间必须在夜间 (18:26 到 01:02 之间)，不能倒退到上午
    sample_time_str = n1103["sample_observation_time"]
    hour = int(sample_time_str.split(":")[0])
    assert hour >= 18 or hour <= 1, f"采样时间 {sample_time_str} 不在暗夜窗口内"

    # 深空天体与土星仰角必须高悬，绝不能为负值 (地平线以下)
    tgts = n1103["targets_at_sample"]
    assert tgts["M31"]["altitude_deg"] > 70.0  # 接近中天
    assert tgts["M33"]["altitude_deg"] > 70.0
    assert tgts["Double_Cluster"]["altitude_deg"] > 50.0
    assert tgts["Saturn"]["altitude_deg"] > 50.0
