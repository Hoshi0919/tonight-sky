"""
朱诺号 (Juno) 木星极轨道动力学、纯钛辐射保险库与弱光太阳能测试集
====================================================================

8 项严苛物理断言:
1. 33 天木星极轨道开普勒几何与偏心率检验 (e ≈ 0.975, a ≈ 296 万公里)
2. 近木点 (Perijove) 活力公式掠飞极速检验 (vp > 57 km/s 且超 20 万 km/h)
3. 2026-10-16 瞬时近木点前后时序检验 (PJ88 刚过 3~4 天，距 PJ89 倒计时 28 天)
4. 180 公斤 1 厘米纯钛辐射保险库屏蔽衰减检验 (衰减比 800 倍，内部剂量 <= 25 krad 保护 RAD750)
5. 5.2 AU 处太阳辐射能流逆平方衰减检验 (能流 ~50 W/m² 为地球的 3.7%)
6. 60 m² 弱光低温三叶光伏阵列与老化电能裕度检验 (P_gen ~ 450 W，净科学余量 > 200%)
7. 木星深空科学发现检验 (弥散稀释核 0.5 R_J，大红斑扎根 300~500 km)
8. 木星极区正多边形稳定几何对称气旋群检验 (北极正九边形 1+8，南极 1+5 稳定涡旋)
"""

import sys
import math
from pathlib import Path
from datetime import datetime, timezone
import pytest

# 将 scripts 加入 Python 路径
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from juno_jupiter_radiation_vault_polar_engine import (
    JunoJupiterPolarEngine,
    GM_JUPITER,
    R_JUPITER_EQUATORIAL_KM,
    JUNO_ORBIT_PERIOD_DAYS,
    JUNO_PERIJOVE_ALTITUDE_KM,
    VAULT_MASS_KG,
    VAULT_WALL_THICKNESS_CM,
    PJ88_UTC,
    PJ89_UTC
)


def test_juno_keplerian_polar_orbit_geometry():
    """断言 1: 33 天木星极轨道开普勒几何与偏心率检验"""
    engine = JunoJupiterPolarEngine()
    orbit = engine.compute_polar_orbit_dynamics()

    # 近木点中心距 = 71492 + 3500 = 74992 km
    assert abs(orbit.periapsis_radius_km - 74992.0) < 1.0
    # 半长轴约为 296 万公里 (~41.5 R_J)
    assert 2.90e6 < orbit.semi_major_axis_km < 3.05e6
    # 极高偏心率 (0.970 ~ 0.980)
    assert 0.970 < orbit.eccentricity < 0.980
    # 远木点距离超过 580 万公里 (> 80 R_J)
    assert orbit.apoapsis_radius_km > 5.80e6


def test_juno_periapsis_extreme_velocity():
    """断言 2: 近木点掠飞极速检验"""
    engine = JunoJupiterPolarEngine()
    orbit = engine.compute_polar_orbit_dynamics()

    # 近地点极速 57 ~ 59 km/s
    assert 57.0 < orbit.periapsis_velocity_kms < 59.0
    # 时速超过 205,000 km/h (人类仅次于帕克探测器的极速造物)
    assert orbit.periapsis_velocity_kmh > 205000.0
    # 远木点速度降至不足 1 km/s (< 0.8 km/s)
    assert orbit.apoapsis_velocity_kms < 0.80
    # 近远点速度之比超过 70 倍
    assert orbit.speed_ratio_peri_apo > 70.0


def test_juno_perijove_timeline_2026():
    """断言 3: 2026-10-16 瞬时近木点前后时序检验"""
    engine = JunoJupiterPolarEngine(datetime(2026, 10, 16, 6, 0, 0, tzinfo=timezone.utc))
    cd = engine.compute_perijove_countdown()

    assert cd.last_perijove_number == 88
    # 距 10-12 PJ88 掠飞过去 3.5 ~ 4.5 天
    assert 3.5 < cd.days_since_last_pj < 4.5
    assert cd.next_perijove_number == 89
    # 距 11-13 PJ89 掠飞倒计时 27 ~ 29 天
    assert 27.0 < cd.days_until_next_pj < 29.0
    assert cd.next_perijove_utc.month == 11
    assert cd.next_perijove_utc.day == 13


def test_juno_titanium_vault_radiation_shielding():
    """断言 4: 180 公斤纯钛保险库屏蔽与剂量衰减检验"""
    engine = JunoJupiterPolarEngine()
    vault = engine.evaluate_radiation_vault()

    assert vault.vault_mass_kg == 180.0
    assert vault.vault_thickness_cm == 1.0
    # 衰减倍数达到 800 倍
    assert vault.attenuation_factor == 800.0
    # 内部剂量压低到 25,000 rad 以下
    assert vault.internal_dose_rad <= 25000.0
    assert vault.is_safe_for_rad750


def test_juno_solar_flux_decay_at_5au():
    """断言 5: 5.2 AU 处太阳辐射通量逆平方衰减检验"""
    engine = JunoJupiterPolarEngine()
    pwr = engine.compute_solar_power_budget()

    assert 5.15 < pwr.heliocentric_distance_au < 5.25
    # 太阳常数衰减至约 50 W/m²
    assert 48.0 < pwr.solar_flux_w_m2 < 53.0
    # 占比仅为地球处的 3.5% ~ 3.9%
    assert 0.035 < pwr.flux_ratio_to_earth < 0.039


def test_juno_solar_array_power_and_margin():
    """断言 6: 60 m² 太阳翼与老化后电能裕度检验"""
    engine = JunoJupiterPolarEngine()
    pwr = engine.compute_solar_power_budget()

    assert pwr.array_area_m2 == 60.0
    # 考虑 10 年在轨极端辐射老化后，发电量稳定在 420 ~ 490 W
    assert 420.0 < pwr.generated_power_w < 490.0
    # 平台基线 150 W，净科学余量 > 250 W 且余量百分比 > 150%
    assert pwr.net_science_margin_w > 250.0
    assert pwr.power_margin_percentage > 150.0


def test_juno_interior_atmosphere_discoveries():
    """断言 7: 弥散稀释核与深根大红斑发现检验"""
    engine = JunoJupiterPolarEngine()
    disc = engine.evaluate_interior_atmosphere_discoveries()

    # 弥散稀释核半径达到 0.4 ~ 0.6 R_J
    assert 0.40 <= disc.dilute_core_radius_rj <= 0.60
    # 大红斑向下扎根 300 ~ 500 km
    assert 300.0 <= disc.great_red_spot_depth_km <= 500.0
    assert "Metallic Hydrogen" in disc.magnetic_field_dynamo_origin


def test_juno_polar_cyclones_geometry():
    """断言 8: 极区几何正多边形稳定气旋群检验"""
    engine = JunoJupiterPolarEngine()
    disc = engine.evaluate_interior_atmosphere_discoveries()

    # 北极 1 中心 + 8 外围正九边形气旋群
    assert "Nonagon" in disc.north_polar_cyclone_geometry
    assert "8 Surrounding" in disc.north_polar_cyclone_geometry
    # 南极正五/六边形气旋群
    assert "5 Surrounding" in disc.south_polar_cyclone_geometry
