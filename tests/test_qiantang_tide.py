import datetime
import sys
from pathlib import Path
import pytest

scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from qiantang_tide_mechanics import (
    vec_sub, vec_add, vec_scale, vec_dot, vec_mag,
    compute_tide_at_time, compute_diurnal_curve,
    compute_multiday_peaks, analyze_qiantang_bore_2026,
    compute_estuary_propagation, ESTUARY_STATIONS,
    TZ_CST
)


def test_vector_math():
    v1 = (1.0, 2.0, 3.0)
    v2 = (4.0, -1.0, 0.0)
    assert vec_add(v1, v2) == (5.0, 1.0, 3.0)
    assert vec_sub(v1, v2) == (-3.0, 3.0, 3.0)
    assert vec_scale(v1, 2.0) == (2.0, 4.0, 6.0)
    assert vec_dot(v1, v2) == 1.0 * 4.0 + 2.0 * (-1.0) + 3.0 * 0.0
    assert abs(vec_mag((3.0, 4.0, 0.0)) - 5.0) < 1e-9


def test_tide_acceleration_order_of_magnitude():
    dt = datetime.datetime(2026, 9, 28, 12, 0, tzinfo=TZ_CST)
    data = compute_tide_at_time(dt, lat_deg=30.534, lon_deg=120.563)
    
    # 物理量级自洽性检验 (μm/s²)
    # 月球引潮力加速度应在 0.5 ~ 1.5 μm/s² 之间
    moon_acc = data["moon"]["acc_total_um_s2"]
    assert 0.5 <= moon_acc <= 1.5
    
    # 太阳引潮力加速度应在 0.2 ~ 0.8 μm/s² 之间
    sun_acc = data["sun"]["acc_total_um_s2"]
    assert 0.2 <= sun_acc <= 0.8
    
    # 合成引潮力应在合理界限内
    comb_acc = data["combined"]["acc_total_um_s2"]
    assert 0.5 <= comb_acc <= 2.5
    
    # 几何分解守恒性: a_tot^2 ≈ a_vert^2 + a_horiz^2
    az = data["combined"]["acc_vert_um_s2"]
    ah = data["combined"]["acc_horiz_um_s2"]
    recon = (az**2 + ah**2)**0.5
    assert abs(recon - comb_acc) < 0.05


def test_aug18_is_global_peak():
    analysis = analyze_qiantang_bore_2026()
    assert analysis["global_peak_day"] == "2026-09-28"
    assert analysis["is_aug18_peak"] is True
    assert analysis["global_peak_force_um_s2"] > 1.63


def test_diurnal_curve_steps():
    curve = compute_diurnal_curve("2026-09-28", step_minutes=60)
    assert len(curve) == 24
    for pt in curve:
        assert "timestamp_cst" in pt
        assert "combined" in pt
        assert pt["combined"]["acc_total_um_s2"] > 0.0


def test_yanguan_bore_windows():
    analysis = analyze_qiantang_bore_2026()
    windows = analysis["yanguan_windows"]
    assert len(windows) == 2
    types = [w["bore_type"] for w in windows]
    assert any("夜潮" in t for t in types)
    assert any("日潮" in t for t in types)


def test_estuary_propagation_structure():
    prop = compute_estuary_propagation("2026-09-28 13:25")
    assert len(prop) == 7
    # 距离单调递增
    kms = [s["river_km"] for s in prop]
    assert kms == sorted(kms)
    assert kms[0] == 0.0
    assert kms[-1] == 82.0
    
    # 抵达时间单调递增
    times = [s["estimated_arrival_cst"] for s in prop]
    assert times == sorted(times)
    assert "13:25" in prop[2]["estimated_arrival_cst"]  # 盐官精准落在 13:25


def test_estuary_hydrodynamics_physics():
    prop = compute_estuary_propagation("2026-09-28 13:25")
    
    # 波速在合理物理范围 (25 ~ 35 km/h)
    for s in prop:
        assert 25.0 <= s["bore_speed_kmh"] <= 35.0
        assert s["dissipation_mw"] > 0.0
    
    # 盐官站应为全流域弗劳德数与能量耗散巅峰 (激波强度最大)
    yanguan = prop[2]
    assert yanguan["id"] == "yanguan"
    assert yanguan["froude_number"] > 1.5
    assert "破碎涌潮" in yanguan["shock_type"]
    assert yanguan["dissipation_mw"] > 100.0  # 超过 100 兆瓦耗散
    
    # 杭州市区站水深增加，弗劳德数应回落转为波状涌潮 (Undular Bore)
    hangzhou = prop[-1]
    assert hangzhou["id"] == "qiantang_bridge"
    assert hangzhou["froude_number"] < 1.25
    assert "波状涌潮" in hangzhou["shock_type"]
