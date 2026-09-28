"""
自动化单元测试集：2026 年金星下合与大气光环动力学引擎
测试天体几何、留点解算、下合极值、罗素气溶胶散射光环模型、中国主要城市中天与遮光安全几何。
"""

import sys
from pathlib import Path
import math
import pytest

scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from venus_inferior_conjunction_engine import (
    find_stationary_points,
    find_inferior_conjunction,
    find_minimum_separation,
    compute_cusp_extension,
    compute_topocentric_transits,
    compute_safety_shadow_geometry,
    generate_daily_trajectory,
    build_full_dataset,
)


def test_inferior_conjunction_timing_and_geometry():
    """验证 2026 年金星下合时刻与轨道物理参量。"""
    res = find_inferior_conjunction(2026)
    assert "2026-10-24" in res["exact_cst"]
    st = res["state"]

    # 地心距离在 0.272 ~ 0.274 AU 之间（最近行星极值）
    assert 0.272 <= st["earth_distance_au"] <= 0.274
    # 视直径超过 61.5 角秒
    assert st["angular_size_arcsec"] > 61.5
    # 照亮比例低于 1%
    assert 0.5 <= st["phase_percent"] <= 0.8
    # 太阳金星角距在 6.4° ~ 6.6° 之间
    assert 6.4 <= st["solar_separation_deg"] <= 6.6
    # 相角接近 171°
    assert 170.0 <= st["phase_angle_deg"] <= 172.0


def test_stationary_points_and_retrograde_duration():
    """验证金星顺逆行转折留点及逆行周期。"""
    stats = find_stationary_points(2026)
    assert "stationary_1_direct_to_retrograde" in stats
    assert "stationary_2_retrograde_to_direct" in stats

    p1 = stats["stationary_1_direct_to_retrograde"]["cst_time"]
    p2 = stats["stationary_2_retrograde_to_direct"]["cst_time"]

    # 留一发生在 10 月初（10-02 至 10-03）
    assert "2026-10-02" in p1 or "2026-10-03" in p1
    # 留二发生在 11 月中旬（11-11 至 11-13）
    assert "2026-11-11" in p2 or "2026-11-12" in p2 or "2026-11-13" in p2
    # 逆行持续时间约 39 ~ 41 天
    dur = stats["retrograde_duration_days"]
    assert 39.0 <= dur <= 41.5


def test_minimum_separation():
    """验证极小地心角距时刻与数值。"""
    msep = find_minimum_separation(2026)
    assert "2026-10-24" in msep["exact_cst"]
    assert 6.45 <= msep["min_separation_deg"] <= 6.50
    st = msep["state"]
    # 极小时刻金星视星等在 -3.6 ~ -3.8 之间
    assert -3.9 <= st["visual_magnitude"] <= -3.5


def test_cusp_extension_physics():
    """验证罗素模型与气溶胶米氏散射尖端延伸规律。"""
    # 正常下合角距（sep = 6.5°, phase_angle ~ 171.0°）
    res_normal = compute_cusp_extension(solar_sep_deg=6.5, phase_angle_deg=171.0, s_deg=1.4)
    assert res_normal["total_illuminated_arc_deg"] > 180.0
    assert res_normal["single_cusp_extension_deg"] > 8.0
    assert not res_normal["is_closed_ring"]

    # 较远角距（sep = 20.0°, phase_angle = 150.0°）延伸应明显变小
    res_far = compute_cusp_extension(solar_sep_deg=20.0, phase_angle_deg=150.0, s_deg=1.4)
    assert res_far["total_illuminated_arc_deg"] < res_normal["total_illuminated_arc_deg"]

    # 极端超近角距测试闭合光环（如 phase_angle 达到 179°，sin(alpha) 极小）
    res_closed = compute_cusp_extension(solar_sep_deg=1.0, phase_angle_deg=179.0, s_deg=1.4)
    assert res_closed["is_closed_ring"] is True
    assert res_closed["total_illuminated_arc_deg"] == 360.0
    assert res_closed["single_cusp_extension_deg"] == 90.0


def test_topocentric_transits_chinese_cities():
    """验证中国五大地理节点正午中天解算。"""
    transits = compute_topocentric_transits("2026-10-24")
    assert len(transits) == 5

    for c in transits:
        # 金星与太阳都在地平线以上
        assert c["sun_transit_alt_deg"] > 25.0
        assert c["venus_transit_alt_deg"] > 20.0
        # 金星仰角稳定比太阳低约 6.0° ~ 6.2°
        assert 5.95 <= c["altitude_deficit_deg"] <= 6.20
        # 金星提前约 8.5 ~ 10.5 分钟中天
        assert 8.5 <= c["lead_time_minutes"] <= 10.5
        # 视直径接近 62 角秒
        assert c["apparent_size_arcsec"] > 61.0


def test_shadow_safety_geometry():
    """验证建筑物阴影遮挡安全几何。"""
    shadow = compute_safety_shadow_geometry(sun_alt_deg=47.05, venus_alt_deg=40.95, distance_m=10.0)
    # 6.1° 角距在 10 米外产生大于 1 米的垂直物理间隙
    assert shadow["vertical_shadow_corridor_m"] > 1.0
    assert "100% Direct Solar Blocked" in shadow["solar_safety_margin"]


def test_daily_trajectory_continuity():
    """验证 10 月至 11 月时间序列的物理连续性与极值。"""
    traj = generate_daily_trajectory("2026-10-10", "2026-11-05", step_days=2)
    assert len(traj) > 10

    # 找到视直径最大点和地距最小点
    max_size_row = max(traj, key=lambda x: x["angular_size_arcsec"])
    min_dist_row = min(traj, key=lambda x: x["distance_au"])

    # 极值都应出现在 10-24 或 10-25
    assert max_size_row["date"] in ["2026-10-24", "2026-10-25"]
    assert min_dist_row["date"] in ["2026-10-24", "2026-10-25"]

    # 验证晨昏翻转：前半段包含“昏星”或“下合翻转”，后半段包含“晨星”
    has_evening_or_flip = any("昏星" in r["orientation_desc"] or "翻转" in r["orientation_desc"] for r in traj[:5])
    has_morning = any("晨星" in r["orientation_desc"] for r in traj[-5:])
    assert has_evening_or_flip and has_morning


def test_build_full_dataset():
    """验证数据打包及关键字段完整性。"""
    data = build_full_dataset()
    assert data["mission"] == "Venus Inferior Conjunction & Atmospheric Ring Dynamics 2026"
    assert "inferior_conjunction" in data
    assert "minimum_separation" in data
    assert "meridian_transits_2026_10_24" in data
    assert "daily_trajectory" in data
