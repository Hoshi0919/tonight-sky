"""
嫦娥四号与玉兔二号月背巡视、极寒核热源动力学与
2026 人类深空二十一极黄金舰队 (The Grand Unvigintet) 单元测试集
==================================================================

9 项严苛物理与工程断言:
1. 玉兔二号长寿命巡视与月昼数检验 (超 95 月昼，超期服役超 30 倍，人类在轨最长月球车)
2. 钚-238 RHU 放射性同位素热力学衰减守恒检验 (半衰期 87.74 年，衰减 <6.5%，强劲供热 >2.3 W)
3. 月球表面斯忒藩-玻尔兹曼极限温差与舱内热平衡检验 (昼夜温差近 300 K，RHU 维持舱内 >-40°C)
4. 月球背面 100% 几何遮蔽与射电静默区物理检验 (衰减 >100 dB，0.1~30 MHz 宇宙黑暗时代窗口)
5. 地月中继光时延与地月 L2 晕轨道几何检验 (单向光时 ~1.28 秒，鹊桥中继距月 ~65,000 km)
6. 1.6+ km 累计巡视漫游里程检验 (稳健推进超 1600 米)
7. 二十一极深空黄金舰队严格日心距离降序与多极归类检验 (21 大旗舰，从 173.22 AU 到 0.046 AU)
8. 二十一极舰队极限物理跨度检验 (极距跨度 >3700倍，太阳能流落差 >1400万倍，光时跨度 >60000倍)
9. 月球表面原位与环月轨道中继互补对偶检验 (玉兔二号原位巡视与鹊桥二号轨道中继协同)
"""

import sys
import math
from pathlib import Path
from datetime import datetime, timezone
import pytest

scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from change4_yutu2_far_side_lunar_engine import (
    Change4Yutu2FarSideLunarEngine,
    LANDING_UTC,
    VON_KARMAN_LAT_DEG,
    VON_KARMAN_LON_DEG,
    PU238_HALF_LIFE_YEARS,
    DESIGN_LIFETIME_LUNAR_DAYS,
    RHU_INITIAL_POWER_W,
    MOON_MEAN_DISTANCE_KM,
    SPEED_OF_LIGHT
)


def test_yutu2_operational_longevity_and_lunar_days():
    """断言 1: 玉兔二号长寿命巡视与月昼数检验"""
    engine = Change4Yutu2FarSideLunarEngine(datetime(2026, 10, 17, 3, 11, 0, tzinfo=timezone.utc))
    op = engine.compute_operational_metrics()

    # 着陆日期验证
    assert LANDING_UTC.year == 2019
    assert LANDING_UTC.month == 1
    assert LANDING_UTC.day == 3

    # 在轨运行天数超 2800 天，地球年超 7.7 年
    assert op.elapsed_earth_days > 2800.0
    assert 7.7 < op.elapsed_earth_years < 7.9

    # 历经月昼数突破 95 个月昼 (Luns)
    assert op.elapsed_lunar_days > 95.0

    # 超出设计寿命 (3 个月昼) 30 倍以上
    assert op.design_lifetime_multiple > 30.0

    # 确认为人类月面寿命最长月球车
    assert op.is_longest_lunar_rover is True


def test_pu238_rhu_decay_conservation():
    """断言 2: 钚-238 RHU 放射性同位素热力学衰减守恒检验"""
    engine = Change4Yutu2FarSideLunarEngine(datetime(2026, 10, 17, 3, 11, 0, tzinfo=timezone.utc))
    op = engine.compute_operational_metrics()

    # 半衰期 87.74 年
    assert PU238_HALF_LIFE_YEARS == 87.74

    # 7.79 年后放射性衰减应在 5% ~ 6.5% 之间 (衰减因子 0.935 ~ 0.950)
    assert 0.935 < op.pu238_decay_factor < 0.950

    # 初始 2.5W 热功率，当前残余热功率保持在 2.3 W 以上
    assert op.pu238_current_power_w > 2.30
    assert op.pu238_current_power_w < RHU_INITIAL_POWER_W


def test_thermal_equilibrium_and_swing():
    """断言 3: 月球表面极端温差与保温舱热平衡检验"""
    engine = Change4Yutu2FarSideLunarEngine()
    th = engine.compute_thermal_equilibrium()

    # 日下点最高理论平衡温度在 110°C ~ 125°C 之间
    assert 110.0 < th.subsolar_temp_c < 125.0

    # 冯·卡门坑 (45.4°S) 正午地表温度在 75°C ~ 95°C 之间
    assert 75.0 < th.noon_temp_von_karman_c < 95.0

    # 月夜地表极寒温度低于 -170°C
    assert th.night_temp_surface_c < -170.0

    # 昼夜表面极端总温差接近 300 K
    assert 280.0 < th.total_thermal_swing_k < 310.0

    # 依靠核热源与重力热管流体回路，保温舱内核热维持在 -40°C ~ -20°C 安全区间
    assert -40.0 <= th.cabin_temperature_with_rhu_c <= -20.0
    assert th.noon_nap_required is True


def test_far_side_geometry_and_radio_shielding():
    """断言 4: 月背 100% 几何遮蔽与射电静默区物理检验"""
    engine = Change4Yutu2FarSideLunarEngine()
    sh = engine.compute_far_side_shielding_and_radio()

    # 地球永远在地平线以下 (仰角为负且低于 -35°)
    assert sh.earth_visibility_elevation_deg < -35.0
    assert sh.is_earth_invisible is True

    # 月球岩石本体遮蔽衰减超过 100 dB
    assert sh.lunar_body_attenuation_db >= 100.0

    # 地球电离层等离子体截断频率 ~10 MHz
    assert abs(sh.earth_ionosphere_cutoff_mhz - 10.0) < 1.0

    # 月背超低频射电天文窗口涵盖 0.1 ~ 30 MHz
    assert sh.radio_quiet_window_mhz_low <= 0.1
    assert sh.radio_quiet_window_mhz_high >= 30.0


def test_earth_moon_light_time_and_relay():
    """断言 5: 地月中继光时延与地月 L2 晕轨道几何检验"""
    engine = Change4Yutu2FarSideLunarEngine()
    sh = engine.compute_far_side_shielding_and_radio()

    # 地月单向通信光时在 1.25 ~ 1.35 秒之间
    assert 1.25 < sh.earth_moon_one_way_light_time_s < 1.35

    # 鹊桥一号在地月 L2 Halo 轨道距离月球约 6.0 ~ 7.0 万公里
    assert 60000.0 <= sh.queqiao1_relay_distance_km <= 70000.0


def test_cumulative_odometer_progress():
    """断言 6: 1.6+ km 累计巡视漫游里程检验"""
    engine = Change4Yutu2FarSideLunarEngine()
    op = engine.compute_operational_metrics()

    # 累计行驶里程在 1500 米至 1800 米之间
    assert 1500.0 < op.cumulative_odometer_m < 1800.0


def test_grand_unvigintet_fleet_structure_and_order():
    """断言 7: 二十一极深空黄金舰队严格日心距离降序与多极归类检验"""
    engine = Change4Yutu2FarSideLunarEngine()
    fleet = engine.compute_grand_unvigintet_matrix()

    # 舰队规模严格为 21
    assert len(fleet) == 21

    # 严格单调非递增日心距离排序
    distances = [f.heliocentric_dist_au for f in fleet]
    for i in range(len(distances) - 1):
        assert distances[i] >= distances[i+1]

    # 第 1 极为旅行者 1 号 (> 170 AU)
    assert fleet[0].rank == 1
    assert "Voyager 1" in fleet[0].name
    assert fleet[0].heliocentric_dist_au > 170.0

    # 第 2 极为旅行者 2 号 (> 140 AU)
    assert fleet[1].rank == 2
    assert "Voyager 2" in fleet[1].name

    # 第 18 极为嫦娥四号与玉兔二号 (1.000 AU, 地心 38.44 万公里)
    assert fleet[17].rank == 18
    assert "Yutu-2" in fleet[17].name
    assert abs(fleet[17].heliocentric_dist_au - 1.0) < 0.01
    assert abs(fleet[17].geocentric_dist_km - 384400.0) < 1000.0

    # 第 21 极为帕克太阳探测器 (< 0.05 AU)
    assert fleet[20].rank == 21
    assert "Parker" in fleet[20].name
    assert fleet[20].heliocentric_dist_au < 0.05


def test_grand_unvigintet_extreme_contrasts():
    """断言 8: 二十一极舰队极限物理跨度检验"""
    engine = Change4Yutu2FarSideLunarEngine()
    fleet = engine.compute_grand_unvigintet_matrix()
    contrasts = engine.compute_fleet_contrasts(fleet)

    assert contrasts["fleet_size"] == 21
    # 日心极距跨度 > 3700 倍
    assert contrasts["heliocentric_distance_ratio"] > 3700.0
    # 太阳辐射能流落差 > 1400 万倍
    assert contrasts["solar_flux_ratio"] > 1.4e7
    # 地心距离跨度 > 60000 倍
    assert contrasts["geocentric_distance_ratio"] > 60000.0
    # 通信单向光时跨度 > 60000 倍
    assert contrasts["one_way_light_time_ratio"] > 60000.0
    # 极端速度跨度 > 2500 万倍
    assert contrasts["extreme_velocity_ratio"] > 2.5e7
    # 物理极端温差跨度 > 1650 K
    assert contrasts["extreme_temperature_span_k"] > 1650.0


def test_lunar_surface_exploration_complementarity():
    """断言 9: 月球表面原位与环月轨道中继互补对偶检验"""
    engine = Change4Yutu2FarSideLunarEngine()
    fleet = engine.compute_grand_unvigintet_matrix()

    queqiao2 = next(f for f in fleet if "Queqiao-2" in f.name)
    yutu2 = next(f for f in fleet if "Yutu-2" in f.name)

    # 两者均位于日心 1.000 AU 且地心 38.44 万公里
    assert abs(queqiao2.heliocentric_dist_au - 1.000) < 0.01
    assert abs(yutu2.heliocentric_dist_au - 1.000) < 0.01
    assert abs(queqiao2.geocentric_dist_km - yutu2.geocentric_dist_km) < 1000.0

    # 角色互补: 轨道中继 vs 表面原位巡视
    assert "中继" in queqiao2.target or "中继" in queqiao2.operating_regime
    assert "巡视" in yutu2.target or "巡视" in yutu2.operating_regime
