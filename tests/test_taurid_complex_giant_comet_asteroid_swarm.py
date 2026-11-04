"""
test_taurid_complex_giant_comet_asteroid_swarm.py
=================================================
金牛座共振复合体、巨彗星解体假说与通古斯级空爆动力学单元测试集

8 项严苛物理与动力学断言:
1. Southworth-Hawkins 严格自相似性检验 (D_SH 自比对恒为 0.0)
2. 恩克彗星阿波罗小行星舰队强同源性检验 (TD45, TF50, TX24, WP25 D_SH < 0.15)
3. 2015 TX24 与 2005 TF50 巨型小行星相互共轨检验 (D_SH < 0.05)
4. 木星 7:2 平均运动共振严格天体力学检验 (a_res ≈ 2.256 AU, P_res ≈ 3.389 yr)
5. Clube-Napier 巨彗星分级瓦解质量守恒检验 (原初质量 > 1e17 kg, 恩克核存留比 < 0.05%)
6. 通古斯级撞击体大气冲压破裂与终结空爆高度检验 (破裂 > 40 km, 空爆 5~15 km)
7. 通古斯针叶林倒伏破坏面积尺度律检验 (1500 ~ 2500 km² 经典观测吻合)
8. 2026 极大期上海天顶穿透与 7.7 小时纯黑暗夜黄金天窗检验
"""

import sys
from pathlib import Path
import pytest

scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from taurid_complex_giant_comet_asteroid_swarm_engine import (
    TauridComplexSwarmEngine,
    ENCKE_ORBIT,
    TAURID_APOLLO_ASTEROIDS,
)


def test_d_sh_self_identity():
    """断言 1: D_SH 自比对恒为 0.0"""
    engine = TauridComplexSwarmEngine()
    res = engine.compute_d_sh(ENCKE_ORBIT, ENCKE_ORBIT)
    assert res.d_sh == 0.0
    assert res.is_strong_association is True
    assert res.mutual_inclination_deg == 0.0


def test_asteroid_fleet_strong_association():
    """断言 2: 四颗核心阿波罗小行星与 2P/Encke 展现强动力学同源性 (D_SH < 0.15)"""
    engine = TauridComplexSwarmEngine()
    results = {r.target_name: r for r in engine.evaluate_asteroid_fleet()}

    # 2001 TD45, 2005 TF50, 2015 TX24, 2003 WP25
    assert results["2001 TD45"].d_sh < 0.06
    assert results["2001 TD45"].is_strong_association is True

    assert results["2005 TF50"].d_sh < 0.08
    assert results["2005 TF50"].is_strong_association is True

    # 2015 TX24 对应 Nature Astronomy 2017 论文报道的 250 米级小行星
    assert results["2015 TX24"].d_sh < 0.10
    assert results["2015 TX24"].is_strong_association is True

    assert results["2003 WP25"].d_sh < 0.12
    assert results["2003 WP25"].is_strong_association is True

    # 2004 TG10 为中等亲缘 (D_SH < 0.25)
    assert results["2004 TG10"].d_sh < 0.25
    assert results["2004 TG10"].is_medium_association is True


def test_inter_asteroid_swarm_co_orbit():
    """断言 3: 2015 TX24 与 2005 TF50 相互间共轨紧密性检验 (D_SH < 0.05)"""
    engine = TauridComplexSwarmEngine()
    ast_map = {a["name"]: a for a in TAURID_APOLLO_ASTEROIDS}
    tx24 = ast_map["2015 TX24"]
    tf50 = ast_map["2005 TF50"]

    res = engine.compute_d_sh(tx24, tf50)
    assert res.d_sh < 0.05
    assert res.is_strong_association is True
    assert res.mutual_inclination_deg < 3.0


def test_jupiter_7_2_resonance_mechanics():
    """断言 4: 木星 7:2 平均运动共振 (7:2 MMR) 物理参数严格性检验"""
    engine = TauridComplexSwarmEngine()
    j = engine.compute_jupiter_7_2_resonance()

    # 共振半长轴与周期检验
    assert 2.25 < j["resonance_semi_major_axis_au"] < 2.265
    assert 3.38 < j["resonance_period_yr"] < 3.40
    assert 23.5 < j["resonance_super_cycle_yr"] < 24.0
    assert 2026 in j["earth_fireball_swarm_peaks"]


def test_clube_napier_giant_comet_conservation():
    """断言 5: Clube-Napier 巨彗星分级瓦解质量守恒与存留比检验"""
    engine = TauridComplexSwarmEngine()
    b = engine.compute_giant_comet_breakup_model()

    # 100km 巨彗星质量在 10^17 kg 量级
    assert 2.0e17 < b.progenitor_mass_kg < 3.5e17
    # 现存恩克核心质量占比极微 (< 0.05%)
    assert b.encke_mass_fraction < 0.0005
    assert b.estimated_asteroid_count_gt_100m >= 100
    assert b.dust_production_rate_kg_s >= 1.0e4


def test_tunguska_ram_fragmentation_and_burst():
    """断言 6: 通古斯级撞击体大气冲压破裂与终结空爆高度物理检验"""
    engine = TauridComplexSwarmEngine()
    t = engine.simulate_tunguska_airburst()

    # 动能处于 10 ~ 25 MT TNT
    assert 10.0 < t.kinetic_energy_mt_tnt < 25.0
    # 初始冲压剪切破裂发生在高空平流层顶/中间层 (> 40 km)
    assert t.fragmentation_altitude_km > 40.0
    # 终结空爆集中在低空对流层/平流层底 (5 ~ 15 km)
    assert 5.0 <= t.airburst_burst_altitude_km <= 15.0


def test_tunguska_blast_devastation_area():
    """断言 7: 通古斯倒伏破坏面积标定尺度律检验 (1500 ~ 2500 km²)"""
    engine = TauridComplexSwarmEngine()
    t = engine.simulate_tunguska_airburst()

    # 破坏半径 20 ~ 26 km
    assert 20.0 < t.blast_radius_km < 26.0
    # 森林倒伏摧毁面积在 1500 ~ 2200 km² 之间
    assert 1500.0 < t.devastated_area_sqkm < 2500.0


def test_shanghai_zenith_and_dark_window_2026():
    """断言 8: 2026 极大期上海天顶穿透与 7.7 小时绝对纯黑暗夜天窗检验"""
    engine = TauridComplexSwarmEngine()
    z = engine.get_shanghai_2026_zenith_metrics()

    # 南北群中天仰角极高 (> 70° 与 > 80°)
    assert z.sta_transit_altitude_deg > 74.0
    assert z.nta_transit_altitude_deg > 80.0
    assert z.pleiades_transit_altitude_deg > 82.0
    assert z.uranus_transit_altitude_deg > 79.0

    # 纯黑无月天窗长达 7.70 小时 (462 分钟)
    assert z.dark_window_hours >= 7.6
    assert z.moon_illumination_fraction < 0.25
