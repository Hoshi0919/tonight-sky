"""
test_neptune_opposition.py
==========================
单元测试套件：2026 年海王星冲日天体力学推演与海卫一逆行捕获动力学引擎
(Unit tests for Neptune Opposition 2026 & Triton Dynamics Engine)
"""

import sys
from pathlib import Path
import pytest

scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from neptune_opposition_engine import (
    compute_opposition_point,
    compute_retrograde_cycle,
    compute_triton_dynamics,
    compute_guide_star_separations,
    compute_city_geometry,
    generate_full_report,
    NEPTUNE_SYSTEM,
    TRITON_SYSTEM
)


def test_opposition_physics():
    """验证海王星冲日天体测量与物理参数极值"""
    opp = compute_opposition_point()
    # 冲日时刻落在 2026-09-24 ~ 2026-09-25
    assert "2026-09" in opp["opposition_time_cst"]
    # 地心距离 ~28.875 AU
    assert 28.87 <= opp["earth_distance_au"] <= 28.88
    # 单向光行时 ~240 分钟 (4 小时)
    assert 239.0 <= opp["light_travel_time_minutes"] <= 241.0
    # 视星等 V 约 7.8 等
    assert 7.7 <= opp["v_magnitude"] <= 7.9
    # 视直径约 2.37 角秒
    assert 2.30 <= opp["angular_diameter_arcsec"] <= 2.45


def test_equinox_proximity():
    """验证海王星冲日点与春分点及天赤道极近交会"""
    opp = compute_opposition_point()
    # 距离春分点在 3.3° ~ 3.5° 之间
    assert 3.2 <= opp["equinox_separation_deg"] <= 3.5
    # 赤纬几乎位于天赤道 (-0.2° ~ 0.0°)
    assert -0.2 <= opp["dec_deg"] <= 0.0


def test_retrograde_cycle():
    """验证 2026 年海王星逆行周期、留点与角跨度"""
    retro = compute_retrograde_cycle()
    # 留一点在 2026 年 7 月
    assert "2026-07" in retro["stationary_1_cst"]
    # 留二点在 2026 年 12 月
    assert "2026-12" in retro["stationary_2_cst"]
    # 逆行总天数 155 ~ 162 天
    assert 155.0 <= retro["retrograde_duration_days"] <= 162.0
    # 天球逆行角跨度 2.7° ~ 2.9°
    assert 2.70 <= retro["retrograde_arc_deg"] <= 2.90


def test_triton_retrograde_geometry():
    """验证海卫一逆行轨道物理与冲日视投影几何"""
    opp = compute_opposition_point()
    triton = compute_triton_dynamics(opp["earth_distance_au"])
    # 逆行轨道倾角 156.8°
    assert 156.0 <= triton["orbital_inclination_deg"] <= 157.5
    # 逆行周期为负数
    assert triton["orbital_period_days"] < 0
    # 极大视投影角距在 16.5" ~ 17.5"
    assert 16.5 <= triton["max_angular_separation_arcsec"] <= 17.5
    # 相当于海王星行星半径的 14 倍
    assert 13.5 <= triton["separation_in_planet_radii"] <= 15.0
    # 占系统质量 99% 以上
    assert triton["mass_ratio_system_percent"] >= 99.0


def test_triton_roche_limit_and_decay():
    """验证海卫一洛希极限与潮汐衰减寿命模型"""
    opp = compute_opposition_point()
    triton = compute_triton_dynamics(opp["earth_distance_au"])
    # 流体洛希极限 ~55,600 km (~2.26 R_N)
    assert 55000.0 <= triton["fluid_roche_limit_km"] <= 56500.0
    assert 2.20 <= triton["fluid_roche_in_planet_radii"] <= 2.35
    # 刚体洛希极限 ~32,800 km
    assert 32000.0 <= triton["rigid_roche_limit_km"] <= 33500.0
    # 当前轨道距离为流体洛希极限的 6.3 ~ 6.5 倍
    assert 6.2 <= triton["current_distance_to_fluid_roche_ratio"] <= 6.6
    # 衰减瓦解预期寿命 1.4 ~ 3.6 Gyr
    assert triton["decay_lifetime_min_gyr"] == 1.4
    assert triton["decay_lifetime_max_gyr"] == 3.6


def test_guide_stars():
    """验证双鱼座周边导星角距排序与视星等"""
    stars = compute_guide_star_separations()
    assert len(stars) >= 5
    # 最近的导星为 29 Psc，角距小于 3.0°
    assert stars[0]["name"] == "29 Psc"
    assert stars[0]["separation_deg"] < 3.0
    # 次近的导星角距小于 3.5°
    assert stars[1]["separation_deg"] < 3.5


def test_city_observational_geometry():
    """验证华夏五大城市通宵观测几何 (赤道平分 12 小时)"""
    cities = compute_city_geometry()
    for name, c in cities.items():
        # 可见时间极度接近 12.0 小时 (11.8 ~ 12.2)
        assert 11.8 <= c["visibility_hours"] <= 12.2
    # 广州仰角最高 (66° ~ 68°)
    assert 66.0 <= cities["Guangzhou"]["transit_altitude_deg"] <= 68.0
    # 上海仰角 58° ~ 60°
    assert 58.0 <= cities["Shanghai"]["transit_altitude_deg"] <= 60.0
    # 北京仰角 49° ~ 51°
    assert 49.0 <= cities["Beijing"]["transit_altitude_deg"] <= 51.0


def test_full_report_structure():
    """验证综合报告结构与必要字段"""
    data = generate_full_report()
    assert "neptune_opposition" in data
    assert "retrograde_cycle" in data
    assert "triton_dynamics" in data
    assert "guide_stars" in data
    assert "city_observational_geometry" in data
