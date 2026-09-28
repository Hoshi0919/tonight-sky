"""
test_pleiades_occultation.py — 2026 年国庆子夜月掩昴星团天体力学算法单元测试集
"""

import sys
from pathlib import Path
import datetime
import zoneinfo
import pytest

scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from pleiades_occultation_2026 import (
    PLEIADES_STARS,
    OBSERVERS,
    classify_contact_limb,
    get_position_angle_deg,
    analyze_city_occultation,
    solve_graze_trajectory,
    generate_full_report,
)

CST = zoneinfo.ZoneInfo("Asia/Shanghai")

def test_star_catalog_integrity():
    """测试星表完整性与物理参数有效性"""
    assert len(PLEIADES_STARS) == 10
    for s_id, s_info in PLEIADES_STARS.items():
        assert "hip" in s_info and s_info["hip"] > 0
        assert "name_cn" in s_info and len(s_info["name_cn"]) > 0
        assert 2.0 < s_info["mag"] < 7.0
        assert s_info["spect"].startswith(("B", "A"))
        assert ":" in s_info["ra"]
        assert ":" in s_info["dec"]

def test_position_angle_and_limb_classification():
    """测试方位角与亮暗边判据几何逻辑"""
    # 太阳方位角 75° (亮边中心)
    sun_pa = 75.0
    
    # 恒星在 115°: 偏差 40° < 90° -> 属于亮边
    limb_bright = classify_contact_limb(115.0, sun_pa)
    assert not limb_bright["is_dark"]
    assert "亮边" in limb_bright["limb_type"]
    assert limb_bright["delta_from_sun_pa_deg"] == 40.0
    assert limb_bright["cusp_distance_deg"] == 50.0
    
    # 恒星在 200°: 偏差 125° > 90° -> 属于暗边 (深入暗边 35°)
    limb_dark = classify_contact_limb(200.0, sun_pa)
    assert limb_dark["is_dark"]
    assert "暗边" in limb_dark["limb_type"]
    assert limb_dark["delta_from_sun_pa_deg"] == 125.0
    assert limb_dark["cusp_distance_deg"] == 35.0

def test_beijing_occultation_events():
    """验证北京观测点掩星事件序列与暗边复出特征"""
    t_start = datetime.datetime(2026, 9, 30, 23, 0, tzinfo=CST)
    t_end = datetime.datetime(2026, 10, 1, 3, 30, tzinfo=CST)
    
    bj_res = analyze_city_occultation("beijing", t_start, t_end)
    assert bj_res["classification"] == "FULL_OCCULTATION_ZONE"
    
    occ_star_ids = [occ["star_id"] for occ in bj_res["occultations"]]
    assert "19 Tau (Taygeta)" in occ_star_ids
    assert "21 Tau (Asterope)" in occ_star_ids
    assert "22 Tau" in occ_star_ids
    
    # 验证昂宿二 (Taygeta) 掩始亮边、掩终暗边复出
    taygeta_occ = next(o for o in bj_res["occultations"] if o["star_id"] == "19 Tau (Taygeta)")
    assert not taygeta_occ["ingress_limb"]["is_dark"] # 掩始亮边
    assert taygeta_occ["egress_limb"]["is_dark"]       # 掩终暗边 (核心观测亮点)
    assert 40.0 < taygeta_occ["duration_minutes"] < 50.0
    assert taygeta_occ["peak_altitude_deg"] > 45.0     # 高仰角清晰可见

def test_mohe_high_latitude_penetration():
    """验证极北观测站 (漠河) 月轮深陷星团核心 (掩食 5 颗星)"""
    t_start = datetime.datetime(2026, 9, 30, 23, 0, tzinfo=CST)
    t_end = datetime.datetime(2026, 10, 1, 3, 30, tzinfo=CST)
    
    mohe_res = analyze_city_occultation("mohe", t_start, t_end)
    assert len(mohe_res["occultations"]) >= 4
    occ_ids = [occ["star_id"] for occ in mohe_res["occultations"]]
    assert "20 Tau (Maia)" in occ_ids
    assert "16 Tau (Celaeno)" in occ_ids

def test_shanghai_close_conjunction():
    """验证上海属于极近掠过同框区，未发生全掩但最近距极近"""
    t_start = datetime.datetime(2026, 9, 30, 23, 0, tzinfo=CST)
    t_end = datetime.datetime(2026, 10, 1, 3, 30, tzinfo=CST)
    
    sh_res = analyze_city_occultation("shanghai", t_start, t_end)
    assert sh_res["classification"] == "ULTRA_CLOSE_CONJUNCTION"
    assert len(sh_res["occultations"]) == 0
    assert len(sh_res["grazes_and_approaches"]) > 0
    
    # 昂宿二距月缘外侧小于 5 角分
    taygeta_ap = next(a for a in sh_res["grazes_and_approaches"] if a["star_id"] == "19 Tau (Taygeta)")
    assert 4.0 < taygeta_ap["miss_margin_arcmin"] < 5.5

def test_graze_trajectory_monotonicity():
    """验证掠掩带由于东升视差效应呈现经度东移、临界纬度北抬的单调几何趋势"""
    graze = solve_graze_trajectory("19 Tau (Taygeta)")
    pts = graze["graze_path"]
    assert len(pts) >= 6
    
    lats = [p["graze_latitude"] for p in pts]
    for i in range(len(lats) - 1):
        assert lats[i+1] > lats[i], f"Graze latitude not monotonic: {lats[i]} -> {lats[i+1]}"

def test_full_report_structure():
    """验证全量天象报告数据结构自洽与完备性"""
    report = generate_full_report()
    assert "event_title" in report
    assert "lunar_context" in report
    assert len(report["cities"]) == len(OBSERVERS)
    assert "taygeta" in report["graze_trajectories"]
    assert "asterope" in report["graze_trajectories"]
