"""
test_meteor_shower_dynamics.py
==============================
单元测试套件：2026 年十月双流星雨天体动力学与天幕辐射对比引擎
(Unit tests for October 2026 Meteor Shower Dynamics Engine)
"""

import math
from datetime import datetime, timezone, timedelta
import pytest
import ephem

import sys
from pathlib import Path
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from meteor_shower_dynamics_engine import (
    get_draconids_config,
    get_orionids_config,
    calculate_lunar_sky_degradation,
    calculate_hourly_record,
    simulate_night_window,
    export_multi_city_summary,
    DEFAULT_CITIES,
    CST_TZ
)


def test_shower_configurations():
    """验证两大流星雨母彗星及轨道基础参数"""
    drac = get_draconids_config()
    orion = get_orionids_config()
    
    # 彗星归属
    assert "21P" in drac.comet.name
    assert "1P" in orion.comet.name or "Halley" in orion.comet.name
    
    # 轨道相交速度：天龙座超慢速 (~20.4 km/s), 猎户座高速对冲 (66 km/s)
    assert 19.5 <= drac.ablation.entry_velocity_kms <= 21.0
    assert 65.0 <= orion.ablation.entry_velocity_kms <= 67.0
    
    # 辐射点赤道坐标校验
    assert drac.radiant_ra_hours == "17:28:00"
    assert drac.radiant_dec_deg == 54.0
    assert orion.radiant_ra_hours == "06:20:00"
    assert orion.radiant_dec_deg == 16.0


def test_kinetic_energy_and_luminous_efficiency():
    """验证流星烧蚀动能密度与发光效率物理定律"""
    drac = get_draconids_config()
    orion = get_orionids_config()
    
    # 动能 E_k = 0.5 * m * v^2
    # 1 mg = 1e-6 kg
    # 猎户座动能应至少是天龙座的 10 倍以上
    ratio_ek = orion.ablation.kinetic_energy_per_mg_joules / drac.ablation.kinetic_energy_per_mg_joules
    assert ratio_ek > 10.0
    
    # 激波温度与电离特征
    assert drac.ablation.shock_temperature_kelvin < 5000.0
    assert orion.ablation.shock_temperature_kelvin > 15000.0
    assert "Na I" in drac.ablation.dominant_emissions
    assert "O I" in orion.ablation.dominant_emissions


def test_circumpolar_geometry():
    """验证华北/东北恒显圈与华南下潜几何"""
    drac = get_draconids_config()
    
    # 漠河 (52.97°N) 与 北京 (39.90°N): 纬度 + 赤纬(54°) >= 90° -> 恒显 (Circumpolar)
    mohe_sim = simulate_night_window("Mohe", drac, start_hour_cst=18, duration_hours=6)
    beijing_sim = simulate_night_window("Beijing", drac, start_hour_cst=18, duration_hours=6)
    assert mohe_sim["is_circumpolar"] is True
    assert beijing_sim["is_circumpolar"] is True
    
    # 上海 (31.23°N) 与 广州 (23.13°N): 纬度 + 赤纬 < 90° -> 会落入地平线下
    shanghai_sim = simulate_night_window("Shanghai", drac, start_hour_cst=18, duration_hours=6)
    guangzhou_sim = simulate_night_window("Guangzhou", drac, start_hour_cst=18, duration_hours=6)
    assert shanghai_sim["is_circumpolar"] is False
    assert guangzhou_sim["is_circumpolar"] is False


def test_draconids_moon_free_pure_dark_window():
    """验证 2026-10-08 天龙座极盛期全夜无月纯暗夜天窗"""
    drac = get_draconids_config()
    sh_sim = simulate_night_window("Shanghai", drac, start_hour_cst=19, duration_hours=6)
    
    # 前半夜 19:00 ~ 23:00 月球在地平线下，月相仅 ~3.5%
    recs = [r for r in sh_sim["records"] if "19:00" <= r["timestamp_cst"][-5:] <= "23:00"]
    for r in recs:
        assert r["moon_alt_deg"] < 0.0  # 月亮全在地平线以下
        assert r["nelm"] >= 6.45        # 暗夜极限星等无月光损失
        assert r["cz_factor"] > 0.15     # 辐射点高于 18°，天顶因子 > 0.15


def test_orionids_moonlight_suppression_and_post_moonset_surge():
    """验证 2026-10-21 猎户座流星雨月光压制与月落后反弹"""
    orion = get_orionids_config()
    sh_sim = simulate_night_window("Shanghai", orion, start_hour_cst=22, duration_hours=8)
    
    # 22:30 CST: 盈凸月高悬 (月相 ~79%)
    rec_moon = next(r for r in sh_sim["records"] if r["timestamp_cst"].endswith("22:30"))
    assert rec_moon["moon_alt_deg"] > 30.0
    assert rec_moon["moon_phase_pct"] > 75.0
    assert rec_moon["nelm"] < 4.8  # NELM 遭受严重打压 (退化至 < 4.8 等)
    assert rec_moon["hr_obs"] < 1.0 # 暗星全被吃掉，有效 HR < 1.0
    
    # 03:30 CST: 月落之后，NELM 恢复至 6.50，辐射点登顶中天，HR 爆发
    rec_dark = next(r for r in sh_sim["records"] if r["timestamp_cst"].endswith("03:30"))
    assert rec_dark["moon_alt_deg"] < 0.0 # 月落
    assert rec_dark["nelm"] >= 6.45
    assert rec_dark["hr_obs"] > 15.0 # 迎来十几倍的有效观测率爆发
    assert rec_dark["hr_obs"] / rec_moon["hr_obs"] > 15.0


def test_lunar_sky_degradation_math():
    """测试月辉退化数学函数边界"""
    # 月亮在地平线下
    b_sub, delta_sub = calculate_lunar_sky_degradation(-10.0, 80.0, 60.0)
    assert b_sub == 0.0
    assert delta_sub == 0.0
    
    # 新月
    b_new, delta_new = calculate_lunar_sky_degradation(45.0, 0.2, 60.0)
    assert b_new == 0.0
    assert delta_new == 0.0
    
    # 满月天顶
    b_full, delta_full = calculate_lunar_sky_degradation(90.0, 100.0, 30.0)
    assert b_full > 10.0
    assert delta_full > 2.5 # 至少损失 2.5 等以上


def test_multi_city_json_export():
    """验证全国多城市 JSON 导出数据完备性"""
    summary = export_multi_city_summary()
    assert "generated_at_utc" in summary
    assert "draconids_config" in summary
    assert "orionids_config" in summary
    assert len(summary["cities"]) == 5
    
    for ckey, cdata in summary["cities"].items():
        assert "draconids_window" in cdata
        assert "orionids_window" in cdata
        assert "max_hr_obs" in cdata["draconids_window"]
        assert "max_hr_obs" in cdata["orionids_window"]
