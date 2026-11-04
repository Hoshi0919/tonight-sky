"""
test_published_sun_twilight.py — 外部公开年历 (sunrise-sunset.org) 太阳与暮光锚点回归

期望数据来源：sunrise-sunset.org API（基于 USNO 美国海军天文台算法），覆盖 2026 年 11 月 30 天整月。
用于严格验证 tonight-sky 在上海观测点（31.2304°N, 121.4737°E）算出的太阳升落与暮光各阶段
与国际权威外部天文年历具备秒级一致性，杜绝双重折射等理论模型偏航。
"""

import sys
from pathlib import Path
import pytest

DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR / "scripts"))

ephem = pytest.importorskip("ephem", reason="需要 ephem，uv run --with ephem pytest")

import verify_sun_twilight as vst


@pytest.fixture(scope="module")
def sun_twilight_accuracy():
    return vst.evaluate_accuracy(use_correct_horizon=True)


def test_sunset_matches_external_calendar(sun_twilight_accuracy):
    """日落时刻 30 天与外部年历平均误差 < 8s，最大误差 < 15s"""
    sunset_stats = sun_twilight_accuracy["sunset"]
    assert sunset_stats["mean_s"] < 8.0, f"日落平均误差超标: {sunset_stats['mean_s']}s"
    assert sunset_stats["max_s"] < 15.0, f"日落最大误差超标: {sunset_stats['max_s']}s"


def test_sunrise_matches_external_calendar(sun_twilight_accuracy):
    """日出时刻 30 天与外部年历平均误差 < 25s，最大误差 < 30s"""
    sunrise_stats = sun_twilight_accuracy["sunrise"]
    assert sunrise_stats["mean_s"] < 25.0, f"日出平均误差超标: {sunrise_stats['mean_s']}s"
    assert sunrise_stats["max_s"] < 30.0, f"日出最大误差超标: {sunrise_stats['max_s']}s"


def test_astronomical_dusk_matches_external_calendar(sun_twilight_accuracy):
    """天文昏影终（完全暗夜起点）平均误差 < 10s，最大误差 < 20s"""
    astro_dusk = sun_twilight_accuracy["astro_dusk"]
    assert astro_dusk["mean_s"] < 10.0, f"天文昏影终平均误差超标: {astro_dusk['mean_s']}s"
    assert astro_dusk["max_s"] < 20.0, f"天文昏影终最大误差超标: {astro_dusk['max_s']}s"


def test_astronomical_dawn_matches_external_calendar(sun_twilight_accuracy):
    """天文晨光始平均误差 < 15s，最大误差 < 20s"""
    astro_dawn = sun_twilight_accuracy["astro_dawn"]
    assert astro_dawn["mean_s"] < 15.0, f"天文晨光始平均误差超标: {astro_dawn['mean_s']}s"
    assert astro_dawn["max_s"] < 20.0, f"天文晨光始最大误差超标: {astro_dawn['max_s']}s"


def test_nautical_dusk_matches_external_calendar(sun_twilight_accuracy):
    """航海昏影终平均误差 < 10s，最大误差 < 15s"""
    naut_dusk = sun_twilight_accuracy["nautical_dusk"]
    assert naut_dusk["mean_s"] < 10.0, f"航海昏影终平均误差超标: {naut_dusk['mean_s']}s"
    assert naut_dusk["max_s"] < 15.0, f"航海昏影终最大误差超标: {naut_dusk['max_s']}s"
