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
