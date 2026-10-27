"""test_published_moon_phases.py — 外部锚点回归

与其它测试的区别：这里的期望值不是我自己写的断言，而是 lunaf.com
2026 年月相公开时刻表（UTC，分钟精度）。测试问的是"我的话能不能跟
外面的世界对上"，不是"我的代码是否按我的想法运行"。

数据：tests/data/moon_phases_2026_lunaf.json
"""
import sys
from pathlib import Path

import pytest

DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR / "scripts"))

ephem = pytest.importorskip("ephem", reason="需要 ephem，uv run --with ephem pytest")

import verify_published_phases as vpp

# 公开表精确到分钟 → 先按 30s 舍入误差留余量，60s 作为上限。
TOLERANCE_S = 60.0


@pytest.fixture(scope="module")
def result():
    return vpp.check()


def test_table_has_full_year(result):
    assert result["n"] == 50
    phases = {r["phase"] for r in result["rows"]}
    assert phases == {"New Moon", "First Quarter", "Full Moon", "Last Quarter"}


def test_every_published_phase_matches_within_a_minute(result):
    bad = [r for r in result["rows"] if r["error_s"] > TOLERANCE_S]
    assert not bad, f"{len(bad)} 条与外部时刻表相差超过 {TOLERANCE_S}s: {bad[:3]}"


def test_error_distribution_is_rounding_only(result):
    """误差如果只是分钟舍入，中位数应该在 30s 以内、没有系统偏移。"""
    assert result["median_s"] < 30.0
    assert result["max_s"] < 45.0


def test_hunters_moon_anchor():
    """2026-10-26 猎人满月：公开表 04:12 UTC，我算的是 04:11:44。"""
    err = vpp.nearest_phase("2026-10-26 04:12:00", "Full Moon")
    assert err < 30.0
