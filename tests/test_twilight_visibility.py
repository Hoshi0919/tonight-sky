"""
test_twilight_visibility.py — 暮光行星视见度与多体地平对峙推演测试集
"""

import sys
from pathlib import Path
import math
import datetime
import zoneinfo
import pytest

scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from twilight_visibility_engine import (
    airmass,
    twilight_limiting_mag,
    make_observer,
    compute_twilight_boundaries,
    run_twilight_simulation
)

CST = zoneinfo.ZoneInfo("Asia/Shanghai")


def test_airmass_kasten_young_properties():
    # 天顶 (alt=90°): 气团数严格接近 1.0
    x_90 = airmass(90.0)
    assert abs(x_90 - 1.0) < 0.01

    # alt=30°: sec(60°) = 2.0
    x_30 = airmass(30.0)
    assert abs(x_30 - 2.0) < 0.05

    # alt=10°: ~5.6
    x_10 = airmass(10.0)
    assert 5.0 < x_10 < 6.5

    # alt=4°: ~12.0
    x_4 = airmass(4.0)
    assert 10.0 < x_4 < 15.0

    # 地平截断保护
    x_0 = airmass(0.0)
    assert x_0 == 40.0
    x_neg = airmass(-5.0)
    assert x_neg == 40.0

    # 单调性检验：仰角越低，气团数单调递增
    alts = [80.0, 60.0, 45.0, 30.0, 15.0, 8.0, 3.0, 1.0]
    for i in range(len(alts) - 1):
        assert airmass(alts[i]) < airmass(alts[i + 1])


def test_twilight_limiting_mag_schaefer():
    # 太阳在地平线上：仅极亮天体可见
    assert twilight_limiting_mag(1.0, "naked_eye") == -4.5
    assert twilight_limiting_mag(0.0, "naked_eye") == -4.5

    # 民用暮光终点 (-6°): ~ +1.0 等
    m_civ = twilight_limiting_mag(-6.0, "naked_eye")
    assert abs(m_civ - 1.0) < 0.2

    # 航海暮光终点 (-12°): ~ +4.8 等
    m_naut = twilight_limiting_mag(-12.0, "naked_eye")
    assert abs(m_naut - 4.8) < 0.2

    # 天文暮光终点 (-18°): ~ +6.2 等
    m_astro = twilight_limiting_mag(-18.0, "naked_eye")
    assert abs(m_astro - 6.2) < 0.1

    # 深夜 (-25°): 稳定在暗空极限
    assert twilight_limiting_mag(-25.0, "naked_eye") == 6.2

    # 双筒望远镜增益：全量程严格稳定增加 +3.5 等
    for sun_alt in [0.0, -3.0, -6.0, -9.0, -12.0, -15.0, -20.0]:
        eye = twilight_limiting_mag(sun_alt, "naked_eye")
        bino = twilight_limiting_mag(sun_alt, "binoculars")
        assert round(bino - eye, 2) == 3.5

    # 单调性：随太阳下沉，天空极限星等单调变暗（星等数值单调递增）
    suns = [0.0, -2.0, -5.0, -8.0, -11.0, -14.0, -18.0]
    for i in range(len(suns) - 1):
        assert twilight_limiting_mag(suns[i]) < twilight_limiting_mag(suns[i + 1])


def test_twilight_boundaries_2026_09_28():
    obs = make_observer(lat="31.2304", lon="121.4737")
    date_cst = datetime.date(2026, 9, 28)
    b = compute_twilight_boundaries(obs, date_cst, mode="dusk")

    assert b["sunset"] < b["civil_dusk"]
    assert b["civil_dusk"] < b["nautical_dusk"]
    assert b["nautical_dusk"] < b["astro_dusk"]

    # 验证时刻合理区间 (CST)
    assert b["sunset"].hour == 17 and 40 <= b["sunset"].minute <= 55
    assert b["civil_dusk"].hour == 18 and 5 <= b["civil_dusk"].minute <= 15
    assert b["nautical_dusk"].hour == 18 and 30 <= b["nautical_dusk"].minute <= 42
    assert b["astro_dusk"].hour == 19 and 0 <= b["astro_dusk"].minute <= 10


def test_mercury_twilight_paradox_2026_09_28():
    obs = make_observer(lat="31.2304", lon="121.4737")
    date_cst = datetime.date(2026, 9, 28)
    res = run_twilight_simulation(obs, date_cst, mode="dusk", kv=0.25, step_minutes=1)

    mp = res["events"]["mercury_paradox"]
    # 核心天体力学判定：裸眼窗口为 0（被消光淹没），双筒望远镜窗口 > 20 分钟
    assert mp["paradox_active"] is True
    assert mp["eye_duration_min"] == 0
    assert mp["bino_duration_min"] >= 20


def test_dusk_horizon_triptych_2026_09_28():
    obs = make_observer(lat="31.2304", lon="121.4737")
    date_cst = datetime.date(2026, 9, 28)
    res = run_twilight_simulation(obs, date_cst, mode="dusk", kv=0.25, step_minutes=1)

    triptych = res["events"]["dusk_horizon_triptych"]
    assert triptych["active"] is True
    assert 10 <= triptych["duration_min"] <= 25
    assert triptych["start"] == "18:30"
    assert triptych["end"] == "18:45"


def test_simulation_data_structure():
    obs = make_observer(lat="31.2304", lon="121.4737")
    date_cst = datetime.date(2026, 9, 28)
    res = run_twilight_simulation(obs, date_cst, mode="dusk", kv=0.25, step_minutes=2)

    assert "date" in res
    assert "observer" in res
    assert "boundaries" in res
    assert "events" in res
    assert "timeline" in res
    assert len(res["timeline"]) > 30

    frame = res["timeline"][10]
    assert "time_cst" in frame
    assert "sun_alt" in frame
    assert "limiting_mag_eye" in frame
    assert "bodies" in frame
    for b in ["Moon", "Venus", "Mercury", "Saturn"]:
        assert b in frame["bodies"]
        assert "alt" in frame["bodies"][b]
        assert "extinct_mag" in frame["bodies"][b]
        assert "airmass" in frame["bodies"][b]
        assert "status" in frame["bodies"][b]
