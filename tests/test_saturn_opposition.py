import sys
from pathlib import Path
import json
import pytest

scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from saturn_opposition_engine import (
    find_saturn_opposition_event,
    compute_city_observation_windows,
    compute_seeliger_photometry,
    compute_ring_geometry,
    compute_saturnian_moons,
)
import ephem


def test_opposition_timing_and_geometry():
    """验证 2026 年土星冲日精密动力学参数。"""
    opp = find_saturn_opposition_event(2026)
    
    assert "2026-10-04" in opp["opposition_time_cst"]
    assert "20:14" in opp["opposition_time_cst"]
    
    # 近地点发生在冲日之后 1~2 小时内
    assert "2026-10-04" in opp["perigee_time_cst"]
    assert "21:32" in opp["perigee_time_cst"]
    
    # 最近地距 8.434 AU，约 12.617 亿千米
    assert 8.4340 <= opp["min_distance_au"] <= 8.4345
    assert 1261000000 <= opp["min_distance_km"] <= 1262000000
    
    # 视星等与视直径
    assert 0.30 <= opp["apparent_magnitude"] <= 0.35
    assert 19.5 <= opp["equatorial_size_arcsec"] <= 19.9


def test_phase_angle_and_seeliger_minimum():
    """验证冲日相位角极小值与时刻。"""
    opp = find_saturn_opposition_event(2026)
    
    # 极小相位角仅 0.287° (约 17.25 角分)
    assert 0.285 <= opp["min_phase_angle_deg"] <= 0.290
    assert 17.1 <= opp["min_phase_angle_arcmin"] <= 17.4
    assert "20:18" in opp["min_phase_time_cst"]


def test_ring_tilt_opening_and_direction():
    """验证光环地球视倾角 B 与太阳照角 B'。"""
    opp = find_saturn_opposition_event(2026)
    rg = opp["ring_geometry"]
    
    # 地球视倾角为负数表示南半球光环朝向地球，开度约 -7.6°
    assert -7.7 <= rg["sub_earth_lat_deg"] <= -7.5
    assert 7.5 <= rg["ring_opening_abs_deg"] <= 7.7
    
    # 太阳照射角
    assert 7.7 <= rg["sub_solar_lat_deg"] <= 8.0


def test_ring_angular_dimensions_and_cassini():
    """验证 A/B 环与卡西尼环缝在天空视切平面的角尺寸。"""
    opp = find_saturn_opposition_event(2026)
    rg = opp["ring_geometry"]
    
    # A 环外缘长轴约 44.7 角秒，短轴约 5.9 角秒
    assert 44.0 <= rg["ring_a_major_arcsec"] <= 45.2
    assert 5.7 <= rg["ring_a_minor_arcsec"] <= 6.1
    
    # B 环长轴约 38.4 角秒，短轴约 5.1 角秒
    assert 38.0 <= rg["ring_b_major_arcsec"] <= 39.0
    assert 4.9 <= rg["ring_b_minor_arcsec"] <= 5.3
    
    # 卡西尼缝切向宽度约 1.5 角秒
    assert 1.45 <= rg["cassini_division_width_arcsec"] <= 1.55


def test_ring_major_axis_orientation():
    """验证光环主轴位置角近乎东西走向 (约 93° / 273°)。"""
    opp = find_saturn_opposition_event(2026)
    rg = opp["ring_geometry"]
    
    assert 92.0 <= rg["ring_major_axis_pa_deg"] <= 94.5


def test_photometry_and_seeliger_surge():
    """验证塞利格冲日浪涌效应与星等分解。"""
    ph = compute_seeliger_photometry(
        r_au=9.434,
        delta_au=8.434,
        alpha_deg=0.288,
        B_deg=-7.613
    )
    
    # 裸球本体星等约 +0.64 等
    assert 0.62 <= ph["v_globe_alone"] <= 0.65
    
    # 光环几何增亮约 -0.32 等，通量增量约 34%
    assert 0.31 <= ph["ring_brightness_boost_mag"] <= 0.34
    assert 32.0 <= ph["ring_to_globe_flux_ratio_pct"] <= 37.0
    
    # 塞利格非线性浪涌总增益约 -0.14 ~ -0.16 等
    assert 0.13 <= ph["total_seeliger_surge_mag"] <= 0.17
    assert 0.09 <= ph["surge_shadow_hiding_mag"] <= 0.12
    assert 0.035 <= ph["surge_coherent_backscatter_mag"] <= 0.055


def test_saturnian_moons_distribution():
    """验证五大卫星的几何分布形态：Titan 独居东侧，其余卫星位于西侧。"""
    opp = find_saturn_opposition_event(2026)
    moons = {m["name"]: m for m in opp["saturnian_moons"]}
    
    assert len(moons) == 5
    
    # Titan 位于正东侧大距
    assert moons["Titan"]["side"] == "East"
    assert moons["Titan"]["x_sat_radius"] > 18.0
    assert 85.0 <= moons["Titan"]["position_angle_deg"] <= 90.0
    assert 195.0 <= moons["Titan"]["separation_arcsec"] <= 210.0
    
    # Rhea, Tethys, Dione 位于西侧
    assert moons["Rhea"]["side"] == "West"
    assert moons["Rhea"]["x_sat_radius"] < -6.0
    assert moons["Tethys"]["side"] == "West"
    assert moons["Dione"]["side"] == "West"
    
    # Iapetus 最外侧
    assert moons["Iapetus"]["separation_arcsec"] > 500.0


def test_city_observation_windows():
    """验证五大典型经纬度城市整夜观测窗口与无月夜黑暗条件。"""
    windows = compute_city_observation_windows("2026-10-04")
    assert len(windows) == 5
    
    for w in windows:
        # 整夜可见时长均在 12 小时以上
        assert w["total_visible_hours"] >= 12.0
        # 上中天仰角至少大于 45°
        assert w["saturn_transit_alt_deg"] >= 45.0
        # 前半夜无月光干扰暗空窗口均在 5 小时以上
        assert w["moonless_window_hours"] >= 5.5
