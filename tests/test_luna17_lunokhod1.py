import sys
from pathlib import Path
import pytest
import datetime

DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR / "scripts"))

from luna17_lunokhod1_first_planetary_rover_engine import Luna17Lunokhod1Engine


@pytest.fixture
def engine():
    return Luna17Lunokhod1Engine()


def test_luna17_anniversary(engine):
    res = engine.compute_mission_anniversary()
    assert res["anniversary_full_years"] == 56
    assert res["anniversary_exact_years"] >= 55.9
    assert "1970-11-10" in res["launch_utc"]
    assert "1970-11-17" in res["landing_utc"]
    assert "56 周年" in res["milestone_summary"]
    assert res["days_since_launch"] > 20000


def test_locomotion_and_soil_mechanics(engine):
    res = engine.compute_locomotion_and_soil_mechanics()
    assert res["rover_mass_kg"] == 756.0
    assert 7400.0 < res["weight_earth_n"] < 7430.0
    assert 1220.0 < res["weight_moon_n"] < 1235.0
    assert 0.16 < res["weight_reduction_ratio"] < 0.17
    
    # 钛合金网状轮月壤接地比压约 7.66 kPa
    assert 7.0 < res["ground_pressure_kpa"] < 8.5
    assert res["ground_pressure_earth_kpa"] > 40.0
    
    # 漫游总里程 10.54 km
    assert res["total_distance_traversed_km"] == 10.54
    assert res["operating_days_earth"] == 322.0
    assert res["design_lifetime_days_earth"] == 90.0
    assert res["lifetime_extension_ratio"] > 3.5
    assert 30.0 < res["avg_speed_m_per_day"] < 35.0
    
    # 爬坡极限 30°
    assert res["max_slope_deg"] == 30.0
    assert 0.57 < res["min_required_friction_mu"] < 0.58
    assert 600.0 < res["f_parallel_gravity_n"] < 620.0
    assert 1050.0 < res["f_normal_gravity_n"] < 1070.0


def test_po210_rhu_thermal_decay(engine):
    res = engine.compute_po210_rhu_thermal_decay()
    assert res["isotope"] == "Polonium-210 (^210Po)"
    assert res["half_life_days"] == 138.376
    assert res["initial_thermal_power_w"] == 1000.0
    
    timeline = res["powers_timeline"]
    assert timeline["day_0"] == 1000.0
    # 一个半衰期 (~138天) 降为 500W
    assert timeline["day_138"] == 500.0
    # 第 322 天任务结束时热功率降至约 199.3 W
    assert 195.0 < timeline["day_322"] < 205.0
    assert res["is_frozen_out"] is True
    assert 0.19 < res["fraction_remaining"] < 0.21


def test_laser_ranging_link_budget(engine):
    res = engine.compute_laser_ranging_link_budget(384400.0)
    assert "French CNES Corner-cube" in res["target"]
    coords = res["lunar_coordinates"]
    assert 38.3 < coords["latitude_deg"] < 38.4
    assert -35.1 < coords["longitude_deg"] < -35.0
    assert "Mare Imbrium" in coords["region"]
    
    # 双程光时往返时延约 2.564 秒
    assert 2.56 < res["round_trip_delay_s"] < 2.57
    assert 1.28 < res["one_way_time_s"] < 1.29
    
    # 毫米级测距分辨率
    assert res["range_resolution_mm"] < 2.0
    assert res["annual_recession_cm_per_year"] == 3.8
    assert res["apollo_telescope_recontact_year"] == 2010


def test_comprehensive_summary(engine):
    summary = engine.compute_comprehensive_summary()
    assert "anniversary" in summary
    assert "locomotion" in summary
    assert "thermal" in summary
    assert "laser_ranging" in summary
    assert summary["anniversary"]["anniversary_full_years"] == 56
