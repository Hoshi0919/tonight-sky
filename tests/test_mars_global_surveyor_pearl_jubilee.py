"""
单元测试：火星全球勘测者号 (Mars Global Surveyor, MGS) 发射 30 周年珍珠禧 (Pearl Jubilee)、
行星级大气制动节油动力学、J2 摄动两点钟太阳同步极轨、MOLA 全球激光测高地形二分性、
古发电机熄灭地壳剩余磁场与 TES 机遇号水成矿物寻路
"""

import math
import datetime
import sys
from pathlib import Path
import pytest

DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR / "scripts"))

from mars_global_surveyor_pearl_jubilee_engine import MarsGlobalSurveyorEngine


@pytest.fixture
def engine():
    # 标称基准测试时间：2026-11-06 23:15:00 UTC (距 11-07 17:00 珍珠禧倒计时约 17.7 小时)
    ref_dt = datetime.datetime(2026, 11, 6, 23, 15, tzinfo=datetime.timezone.utc)
    return MarsGlobalSurveyorEngine(current_dt=ref_dt)


def test_mission_timeline_and_pearl_jubilee_countdown(engine):
    """
    1. 验证任务时间线与 30 周年珍珠禧里程碑：
       - 发射于 1996-11-07，距今跨越整整 30 地球年
       - 实际在轨服役 3,647 天 (近 10 地球年 / 5.3 火星年)
       - 距 30 周年正日倒计时 17.7 小时，处于倒计时 24 小时正日冲刺窗口
    """
    tl = engine.compute_mission_timeline()
    assert 29.98 < tl["total_flight_years"] < 30.01
    assert 3640.0 < tl["active_lifetime_days"] < 3660.0
    assert 9.9 < tl["active_lifetime_years"] < 10.1
    assert 5.2 < tl["active_lifetime_mars_years"] < 5.4
    assert 15.0 < tl["countdown_hours"] < 20.0
    assert 0.6 < tl["countdown_days"] < 0.9
    assert tl["is_pearl_jubilee_near"] is True


def test_aerobraking_energetics_and_mass_budget_saving(engine):
    """
    2. 验证行星级大气制动气动力学与齐奥尔科夫斯基推进剂节省：
       - 从 262 x 54,026 km 椭圆初轨拉降至 378 km 圆形制图轨道
       - 大气粘性阻力累计耗散速度增量 Delta V 超 1,250 m/s (实测 1,271.3 m/s)
       - 若纯靠化学推进需额外消耗 >340 kg 双组元推进剂 (占干重 50.5%)
       - 验证突破 Delta II 7925 运力天花板的工程可行性闭环
    """
    aero = engine.compute_aerobraking_energetics()
    assert 4650.0 < aero["v_peri_initial_mps"] < 4750.0
    assert 3360.0 < aero["v_circ_mapping_mps"] < 3380.0
    assert 1260.0 < aero["total_delta_v_saved_mps"] < 1285.0
    assert 330.0 < aero["extra_propellant_needed_kg"] < 355.0
    assert 1.49 < aero["mass_ratio"] < 1.52
    assert aero["aerobraking_passes"] == 891
    assert 1.40 < aero["avg_dv_per_pass_mps"] < 1.45
    assert aero["delta_ii_mass_budget_saved"] is True


def test_sun_synchronous_orbit_and_j2_perturbation_closure(engine):
    """
    3. 验证火星 J2 摄动与太阳同步极轨升交点进动角速度闭合：
       - 制图高度 378 km，轨道线速度 3.372 km/s
       - 公转周期 117.0 分钟，每火星日公转 12.64 圈
       - 太阳同步进动理论倾角 92.85 度，实际飞行倾角 92.86 度，残差仅 0.011 度
       - 7 火星日 88 圈完整重访回归网格
    """
    sync = engine.compute_sun_synchronous_orbit_dynamics()
    assert 3760.0 < sync["orbital_radius_km"] < 3775.0
    assert 3360.0 < sync["circular_velocity_mps"] < 3380.0
    assert 7000.0 < sync["orbital_period_seconds"] < 7040.0
    assert 116.5 < sync["orbital_period_minutes"] < 117.5
    assert 12.2 < sync["orbits_per_earth_day"] < 12.4
    assert 12.5 < sync["orbits_per_sol"] < 12.7
    assert 0.52 < sync["desired_precession_deg_day"] < 0.53
    assert 92.80 < sync["theoretical_inclination_deg"] < 92.90
    assert sync["actual_flown_inclination_deg"] == 92.86
    assert sync["inclination_error_deg"] < 0.02
    assert sync["is_sun_synchronous_closed"] is True
    assert sync["repeat_ground_track_sols"] == 7
    assert sync["repeat_ground_track_orbits"] == 88


def test_mola_topography_dichotomy_and_extreme_relief(engine):
    """
    4. 验证 MOLA 激光测高仪全球拓扑二分性与太阳系极端高程差：
       - 累计发射超 6.7 亿个激光测高脉冲 (1064 nm Nd:YAG)
       - 北部平原平均 -4.5 km，南部高地平均 +1.5 km，二分性断崖落差 6.0 km
       - 希腊撞击盆地深度 -8.2 km，奥林匹斯山峰顶 +21.2 km，全星极差高达 29.4 km
       - 火星地表动力学落差达地球 (19.84 km) 的 1.48 倍
    """
    mola = engine.compute_mola_topography_dichotomy()
    assert mola["total_shots_fired_millions"] > 670.0
    assert mola["laser_wavelength_nm"] == 1064.0
    assert 5.8 < mola["dichotomy_elevation_gap_km"] < 6.2
    assert mola["hellas_basin_floor_km"] == -8.2
    assert mola["olympus_mons_caldera_km"] == 21.2
    assert 29.0 < mola["total_relief_dynamic_range_km"] < 29.6
    assert 1.45 < mola["relief_ratio_vs_earth"] < 1.50
    assert mola["martian_relief_exceeds_earth"] is True


def test_crustal_paleomagnetism_and_dynamo_extinction(engine):
    """
    5. 验证 MAG/ER 地壳剩余磁带与火星古发电机停滞年代学：
       - 现代火星整体偶极场消失 (< 5 nT)，南部塞壬高地存在高达 1,500 nT 局域磁异常
       - 正负相间 120 km 磁条带记录古板块裂离/热对流印记
       - 约 41 亿年前发电机熄灭，39 亿年前形成的希腊盆地无磁化印记
    """
    mag = engine.compute_crustal_magnetism_and_dynamo_extinction()
    assert mag["modern_dipole_field_nt"] <= 5.0
    assert 1400.0 < mag["max_crustal_anomaly_nt"] < 1600.0
    assert 4.05 < mag["dynamo_shutdown_ga"] < 4.15
    assert 3.85 < mag["hellas_impact_age_ga"] < 3.95
    assert mag["is_hellas_demagnetized"] is True
    assert 100.0 < mag["stripe_width_km"] < 150.0
    assert mag["crustal_remnant_proves_ancient_plate_or_convection"] is True


def test_tes_opportunity_heritage_and_mineralogy_closed_loop(engine):
    """
    6. 验证 TES 热辐射光谱仪发现子午线高原晶体赤铁矿与机遇号实地闭环：
       - 在 200~500 cm^-1 光谱带反演粗晶灰色赤铁矿 (alpha-Fe2O3)
       - 指向古代酸性热液或开放积水蒸发沉淀成因
       - 直接引导 2004 年机遇号在子午线高原着陆并发现富赤铁矿“蓝莓”结核与黄钾铁矾
    """
    tes = engine.compute_tes_opportunity_heritage()
    assert "Meridiani" in tes["target_region"]
    assert tes["mineral_formula"] == "alpha-Fe2O3"
    assert tes["spectral_band"] == (200.0, 500.0)
    assert "hydrothermal" in tes["aqueous_origin"].lower() or "standing" in tes["aqueous_origin"].lower()
    assert tes["opportunity_landing_date"] == "2004-01-25"
    assert "blueberries" in tes["opportunity_verified_blueberries"]
    assert tes["opportunity_verified_jarosite"] is True
    assert tes["mgs_to_opportunity_closed_loop"] is True


def test_mars_global_surveyor_foundational_precursor_fleet_matrix():
    """
    7. 验证火星勘测者作为后继 21 世纪深空舰队的技术母体：
       - 为 2001 Mars Odyssey、2003 Mars Express、2005 MRO 等后续全部任务铺平测绘基准与通信中继通道
       - 验证气动阻力捕获与两点钟太阳同步冻结轨道的设计范式
    """
    engine_custom = MarsGlobalSurveyorEngine()
    tl = engine_custom.compute_mission_timeline()
    sync = engine_custom.compute_sun_synchronous_orbit_dynamics()
    aero = engine_custom.compute_aerobraking_energetics()

    assert tl["active_lifetime_years"] > 9.5
    assert sync["is_sun_synchronous_closed"] is True
    assert aero["total_delta_v_saved_mps"] > 1200.0
