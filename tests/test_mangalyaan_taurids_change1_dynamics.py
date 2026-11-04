"""
test_mangalyaan_taurids_change1_dynamics.py
===========================================
单元测试套件：
1. 印度火星轨道探测器 Mangalyaan (MOM) 13 周年发射与轨道动力学
2. 嫦娥一号 (Chang'e-1) 19 周年环月制动 (LOI-1) 动力学与月球科学遗产
3. 2026-11-05 南金牛座流星雨 (STA) 极大期天顶过境、深潜平流层火流星物理与 7.7 小时纯黑天窗
4. 11月05日 航天历史里程碑网络联动
"""

import sys
from pathlib import Path
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from mangalyaan_taurids_change1_dynamics_engine import MangalyaanTauridsChange1DynamicsEngine


@pytest.fixture
def engine():
    return MangalyaanTauridsChange1DynamicsEngine()


def test_mangalyaan_launch_and_initial_orbit(engine):
    """验证 Mangalyaan 发射 13 周年、PSLV-C25 入轨及大椭圆初轨物理参数。"""
    res = engine.compute_mangalyaan_dynamics()
    assert res["anniversary_years"] == 13
    assert "PSLV-C25" in res["launcher"]
    assert "Sriharikota" in res["launch_site"]
    assert res["mass_wet_kg"] == 1337.0
    assert res["lam_thrust_n"] == 440.0
    assert res["lam_isp_s"] == 310.0

    init = res["initial_orbit"]
    assert pytest.approx(init["hp_km"], rel=1e-3) == 246.9
    assert pytest.approx(init["ha_km"], rel=1e-3) == 23566.0
    assert pytest.approx(init["inclination_deg"], rel=1e-3) == 19.27
    assert 6.7 < init["period_hours"] < 6.9
    assert pytest.approx(init["v_perigee_km_s"], abs=0.05) == 9.93
    assert pytest.approx(init["v_apogee_km_s"], abs=0.05) == 2.20


def test_mangalyaan_earth_bound_burn_sequence_and_oberth(engine):
    """验证 Mangalyaan 6 次地心近地点升轨序列与奥伯斯效应能效比。"""
    res = engine.compute_mangalyaan_dynamics()
    seq = res["burn_sequence"]
    assert len(seq) == 6

    # 验证远地点阶梯抬升
    assert seq[0]["achieved_apogee_km"] == 28825.0
    assert seq[1]["achieved_apogee_km"] == 40186.0
    assert seq[2]["achieved_apogee_km"] == 71636.0
    assert seq[3]["achieved_apogee_km"] == 78276.0  # partial burn
    assert seq[4]["achieved_apogee_km"] == 118642.0 # supplementary
    assert seq[5]["achieved_apogee_km"] == 192874.0 # final

    # 近地点奥伯斯效应机械能增量比高于 4.5 倍
    assert res["energy_gain_ratio_oberth"] > 4.5


def test_mangalyaan_tmi_cruise_and_moi(engine):
    """验证 Mangalyaan 地火转移轨道注入 (TMI)、霍曼巡航与火星捕获 (MOI)。"""
    res = engine.compute_mangalyaan_dynamics()
    
    tmi = res["tmi"]
    assert pytest.approx(tmi["burn_duration_s"], abs=1.0) == 1328.89
    assert pytest.approx(tmi["delta_v_m_s"], abs=0.5) == 647.96
    assert pytest.approx(tmi["v_hyperbolic_excess_km_s"], abs=0.05) == 2.97
    assert pytest.approx(tmi["c3_energy_km2_s2"], abs=0.1) == 8.82

    cruise = res["cruise"]
    assert cruise["duration_days"] == 298.0
    assert cruise["distance_km"] == 6.8e8

    moi = res["moi"]
    assert pytest.approx(moi["burn_duration_s"], abs=1.0) == 1388.67
    assert pytest.approx(moi["delta_v_m_s"], abs=0.5) == 1098.7
    assert pytest.approx(moi["hp_km"], abs=0.5) == 421.7
    assert pytest.approx(moi["ha_km"], abs=5.0) == 76993.6
    assert pytest.approx(moi["inclination_deg"], abs=0.1) == 150.0
    assert 72.0 < moi["period_hours"] < 73.5


def test_mangalyaan_payloads_frugal_budget_and_longevity(engine):
    """验证 Mangalyaan 5 大科学仪器、紧凑质量与 7.5 年超长寿命服役。"""
    res = engine.compute_mangalyaan_dynamics()
    payloads = res["payloads"]
    assert len(payloads) == 5
    assert res["total_payload_mass_kg"] == 13.4
    
    instruments = {p["instrument"] for p in payloads}
    assert instruments == {"MCC", "TIS", "MSM", "MENCA", "LAP"}

    assert res["cost_million_usd"] == 73.0
    assert res["designed_life_months"] == 6.0
    assert res["actual_operating_years"] > 7.5


def test_change1_loi_and_polar_circularization(engine):
    """验证嫦娥一号 19 周年第一次近月制动 (LOI-1) 与三阶入轨动力学。"""
    res = engine.compute_change1_loi_dynamics()
    assert res["anniversary_years"] == 19
    assert "2007-11-05 11:15" in res["loi1_time_cst"]

    steps = res["loi_steps"]
    assert len(steps) == 3
    assert steps[0]["step"] == "LOI-1"
    assert steps[0]["period_hours"] == 12.0
    assert steps[2]["step"] == "LOI-3"
    assert "200 km" in steps[2]["orbit_desc"]

    polar = res["polar_orbit"]
    assert polar["altitude_km"] == 200.0
    assert pytest.approx(polar["velocity_km_s"], abs=0.01) == 1.591
    assert pytest.approx(polar["period_min"], abs=0.5) == 127.54
    assert polar["inclination_deg"] == 90.0

    assert res["broadcast_music_total"] == 30
    assert "《我的祖国》" in res["broadcast_music_samples"]
    assert "《高山流水》" in res["broadcast_music_samples"]
    assert res["laser_altimeter_points"] > 9000000
    assert res["dem_resolution_m"] == 120.0
    assert len(res["celms_frequencies_ghz"]) == 4
    assert "丰富海" in res["impact_site"]


def test_taurids_peak_zenith_geometry_and_dark_window(engine):
    """验证南金牛座流星雨 2026-11-05 极大期天顶过境与 7.7 小时纯黑天窗。"""
    res = engine.compute_taurids_peak_mechanics()
    assert res["peak_date"] == "2026-11-05"
    assert res["parent_comet"] == "2P/Encke"
    assert "7:2" in res["resonance"]

    sta = res["sta"]
    assert pytest.approx(sta["transit_alt_deg"], abs=0.1) == 74.27
    assert "00:29:54 CST" in sta["transit_time_cst"]
    assert sta["v_entry_km_s"] == 27.3

    nta = res["nta"]
    assert pytest.approx(nta["transit_alt_deg"], abs=0.1) == 80.87
    assert "00:51:55 CST" in nta["transit_time_cst"]
    assert nta["v_entry_km_s"] == 29.0

    m45 = res["celestial_co_transit"]["m45_pleiades"]
    assert pytest.approx(m45["transit_alt_deg"], abs=0.1) == 82.87

    uranus = res["celestial_co_transit"]["uranus"]
    assert pytest.approx(uranus["transit_alt_deg"], abs=0.1) == 79.67

    dark = res["dark_window"]
    assert dark["duration_hours"] == 7.70
    assert dark["duration_minutes"] == 462.0
    assert dark["moon_phase_pct"] == 20.4
    assert "18:25:32" in dark["astronomical_twilight_end_cst"]
    assert "02:07:36" in dark["moonrise_cst"]


def test_taurids_ablation_thermodynamics_and_stratosphere_penetration(engine):
    """验证南金牛座流星雨超慢速切入动能密度、平流层深潜与极低烧蚀率。"""
    res = engine.compute_taurids_peak_mechanics()
    thermo = res["ablation_thermodynamics"]

    assert pytest.approx(thermo["e_kinetic_mj_kg"], abs=0.5) == 372.6
    assert pytest.approx(thermo["tnt_equivalent_ratio"], abs=0.5) == 89.1
    assert thermo["stagnation_temp_real_gas_k"] == 3700.0
    assert thermo["ablation_ratio_vs_leonids_pct"] < 6.0
    
    depth_min, depth_max = thermo["deep_penetration_alt_range_km"]
    assert depth_min == 40.0
    assert depth_max == 50.0


def test_november_5_space_network(engine):
    """验证 11 月 5 日全历史深空与航天里程碑纪念网络联动。"""
    network = engine.get_november_5_space_network()
    assert len(network) == 4

    missions = {item["mission"] for item in network}
    assert any("Mariner 3" in m for m in missions)
    assert any("ATS-3" in m for m in missions)
    assert any("Chang'e-1" in m for m in missions)
    assert any("Mangalyaan" in m for m in missions)

    years_map = {item["year"]: item["years_elapsed"] for item in network}
    assert years_map[1964] == 62
    assert years_map[1967] == 59
    assert years_map[2007] == 19
    assert years_map[2013] == 13
