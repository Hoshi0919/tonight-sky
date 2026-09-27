import sys
from pathlib import Path
import pytest

scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from five_planet_relay import compute_planet_relay, get_observer


@pytest.fixture(scope="module")
def relay_data():
    return compute_planet_relay("2026-09-27")


def test_planet_relay_completeness(relay_data):
    stats = relay_data["statistics"]
    assert stats["relay_complete"] is True
    assert stats["seen_planets_count"] == 5
    expected_planets = ["Jupiter", "Mars", "Mercury", "Saturn", "Venus"]
    assert sorted(stats["seen_planets"]) == expected_planets


def test_planet_relay_acts_order(relay_data):
    timeline = relay_data["timeline"]
    time_map = {row["hour"]: row for row in timeline}

    # 1. 18:00 CST 黄昏：水星与金星可见
    dusk_18 = time_map["18:00"]
    assert dusk_18["is_dark"] is True
    assert "Mercury" in dusk_18["visible_planets"]
    assert "Venus" in dusk_18["visible_planets"]
    assert dusk_18["planets_detail"]["Venus"]["alt"] > 5.0
    assert dusk_18["planets_detail"]["Mercury"]["alt"] > 5.0

    # 2. 00:00 CST 子夜：土星高悬上中天附近（仰角 > 55°）
    midnight = time_map["00:00"]
    assert "Saturn" in midnight["visible_planets"]
    assert midnight["planets_detail"]["Saturn"]["alt"] > 55.0

    # 3. 04:00 CST 黎明前：火星、木星、土星三星同时在天
    dawn_04 = time_map["04:00"]
    assert "Mars" in dawn_04["visible_planets"]
    assert "Jupiter" in dawn_04["visible_planets"]
    assert "Saturn" in dawn_04["visible_planets"]
    assert len(dawn_04["visible_planets"]) >= 3


def test_mercury_venus_dusk_parameters(relay_data):
    bodies = relay_data["bodies_info"]
    venus = bodies["Venus"]
    mercury = bodies["Mercury"]

    assert venus["magnitude"] < -4.0
    assert mercury["magnitude"] < 0.5
    assert venus["constellation_zh"] == "室女座"
    assert mercury["constellation_zh"] == "室女座"


def test_mars_jupiter_dawn_parameters(relay_data):
    bodies = relay_data["bodies_info"]
    mars = bodies["Mars"]
    jupiter = bodies["Jupiter"]

    assert mars["magnitude"] < 1.5
    assert jupiter["magnitude"] < -1.5
    assert mars["constellation_zh"] == "巨蟹座"
    assert jupiter["constellation_zh"] == "狮子座"

    # 角距验证
    timeline = relay_data["timeline"]
    time_map = {row["hour"]: row for row in timeline}
    dawn_04 = time_map["04:00"]
    sep = dawn_04["separations"]["mars_jupiter_deg"]
    assert 18.0 <= sep <= 21.0
