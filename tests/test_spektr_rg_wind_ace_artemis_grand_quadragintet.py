"""
Unit tests for Spektr-RG, Wind, ACE, ARTEMIS P1/P2 & The Grand Unoctoquadragintet Engine.
Asserts mathematical precision, astrodynamic timelines, physical contrasts,
and the comprehensive 41-probe deep space fleet census.
"""

import sys
from pathlib import Path

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from spektr_rg_wind_ace_artemis_grand_quadragintet_engine import (
    compute_spektr_rg_state,
    compute_wind_state,
    compute_ace_state,
    compute_artemis_pair_state,
    compute_plasma_frequency_khz,
    compute_lunar_wake_mach_number,
    the_sun_earth_l1_pentad,
    the_sun_earth_l2_trinity,
    the_lunar_octet,
    the_grand_unoctoquadragintet_fleet_census,
    armada_41_comprehensive_summary,
    EPOCH_2026_10_19
)


def test_spektr_rg_l2_state_and_astrophysics():
    """验证 Spektr-RG 空间高能天文台在轨服役参数与核心物理"""
    state = compute_spektr_rg_state(EPOCH_2026_10_19)
    assert "Spektr-RG" in state.name
    assert "Roscosmos" in state.agency
    assert state.launch_date == "2019-07-13"
    assert state.arrival_or_loi_date == "2019-10-21"
    
    # 在轨服役超 7 年 (2600+ 天)
    assert state.cumulative_years_in_space >= 7.20
    assert state.cumulative_days_in_space >= 2650.0
    assert state.cumulative_days_in_target_orbit >= 2550.0
    
    # 轨道与几何
    assert "L2 Halo" in state.orbit_type
    assert state.distance_from_earth_km == 1500000.0
    assert state.heliocentric_distance_au == 1.010
    
    # 载荷谱段：ART-XC (4-30 keV) 与 eROSITA (0.3-10 keV)
    assert any("ART-XC" in p for p in state.core_payloads)
    assert any("eROSITA" in p for p in state.core_payloads)
    assert any("3 million" in h for h in state.scientific_highlights)


def test_wind_l1_heliospheric_longevity():
    """验证 Wind 风号航天器近 32 年在轨长寿纪录与等离子体物理"""
    state = compute_wind_state(EPOCH_2026_10_19)
    assert state.name == "Wind"
    assert state.agency == "NASA"
    assert state.launch_date == "1994-11-01"
    
    # 在轨服役超 31.9 年 (11,600+ 天)
    assert state.cumulative_years_in_space >= 31.90
    assert state.cumulative_days_in_space >= 11600.0
    
    # 轨道与驻留
    assert "L1 Halo" in state.orbit_type
    assert state.heliocentric_distance_au == 0.990
    
    # 核心载荷与产出
    assert any("WAVES" in p for p in state.core_payloads)
    assert any("Konus" in p for p in state.core_payloads)
    assert any("8,000" in h for h in state.scientific_highlights)
    
    # 等离子体特征频率计算断言
    # f_pe = 8.98 * sqrt(n_e)
    # 对于典型太阳风 n_e = 5 cm^-3, f_pe ~ 20.08 kHz
    f_pe_5 = compute_plasma_frequency_khz(5.0)
    assert 20.0 <= f_pe_5 <= 20.2
    
    # 对于高密度激波前沿 n_e = 100 cm^-3, f_pe ~ 89.8 kHz
    f_pe_100 = compute_plasma_frequency_khz(100.0)
    assert 89.7 <= f_pe_100 <= 89.9


def test_ace_l1_cosmic_ray_space_weather():
    """验证 ACE 探测器超 29 年实时空间天气与宇宙线同位素时钟物理"""
    state = compute_ace_state(EPOCH_2026_10_19)
    assert "ACE" in state.name
    assert state.agency == "NASA"
    assert state.launch_date == "1997-08-25"
    
    # 在轨服役超 29 年 (10,600+ 天)
    assert state.cumulative_years_in_space >= 29.10
    assert state.cumulative_days_in_space >= 10600.0
    
    # 轨道与几何
    assert "L1 Lissajous" in state.orbit_type
    assert state.heliocentric_distance_au == 0.990
    
    # 载荷与时钟断言
    assert any("CRIS" in p for p in state.core_payloads)
    assert any("SWEPAM" in p for p in state.core_payloads)
    assert any("RTSW" in p for p in state.core_payloads)
    assert any("Ni-59" in h for h in state.scientific_highlights)
    assert any("2029" in h for h in state.scientific_highlights)


def test_artemis_p1_p2_lunar_orbit_dynamics():
    """验证 ARTEMIS P1/P2 绕月高偏心双星轨道动力学与 15+ 年运行实绩"""
    pair = compute_artemis_pair_state(EPOCH_2026_10_19)
    p1 = pair["P1"]
    p2 = pair["P2"]
    
    assert "P1" in p1.name and "THEMIS-B" in p1.name
    assert "P2" in p2.name and "THEMIS-C" in p2.name
    assert p1.launch_date == "2007-02-17"
    
    # 总航天器寿命近 20 年 (7,000+ 天)
    assert p1.cumulative_years_in_space >= 19.50
    assert p1.cumulative_days_in_space >= 7100.0
    
    # 绕月运行超 15.2 年 (5,500+ 天)
    assert p1.cumulative_days_in_target_orbit >= 5500.0
    assert p2.cumulative_days_in_target_orbit >= 5500.0
    
    # 对偶轨道几何：P1 逆行，P2 顺行
    assert "Retrograde" in p1.orbit_type
    assert "Prograde" in p2.orbit_type
    
    # 载荷配备与科学焦点
    for probe in (p1, p2):
        assert any("FGM" in p for p in probe.core_payloads)
        assert any("ESA" in p for p in probe.core_payloads)
        assert any("EFI" in p for p in probe.core_payloads)
        assert any("lunar wake" in h for h in probe.scientific_highlights)
        assert any("magnetotail" in h for h in probe.scientific_highlights)


def test_lunar_wake_plasma_physics():
    """验证太阳风月球尾迹超声速马赫数与等离子体物理"""
    # 典型太阳风速度 v_sw = 400 km/s, 离子声速 c_s = 40 km/s
    mach = compute_lunar_wake_mach_number(400.0, 40.0)
    assert mach == 10.0
    assert mach > 5.0  # 远大于 1，形成强超声速吸收尾迹


def test_sun_earth_l1_pentad_census():
    """验证日地 L1 空间天气五大先锋旗舰 (The L1 Heliospheric Pentad)"""
    pentad = the_sun_earth_l1_pentad()
    assert len(pentad) == 5
    names = [p["name"] for p in pentad]
    assert names == ["SOHO", "Wind", "ACE", "DSCOVR", "Aditya-L1"]
    
    # 检查各机构协作
    agencies = {p["agency"] for p in pentad}
    assert "ESA/NASA" in agencies
    assert "NASA" in agencies
    assert "ISRO" in agencies
    assert "NASA/NOAA/USAF" in agencies


def test_sun_earth_l2_trinity_census():
    """验证日地 L2 空间巡天三大天文台对偶矩阵 (The L2 Space Observatory Trinity)"""
    trinity = the_sun_earth_l2_trinity()
    assert len(trinity) == 3
    names = [o["name"] for o in trinity]
    assert names == ["JWST", "Euclid", "Spektr-RG"]
    
    # 覆盖红外、可见/近红外、X射线三大天体物理窗口
    wavelengths = [o["wavelength"] for o in trinity]
    assert any("Infrared" in w for w in wavelengths)
    assert any("Visible" in w for w in wavelengths)
    assert any("X-ray" in w for w in wavelengths)


def test_lunar_octet_census():
    """验证月球现役八大金刚 (The Lunar Octet) 完整编队"""
    octet = the_lunar_octet()
    assert len(octet) == 8
    names = [m["name"] for m in octet]
    assert "LRO" in names
    assert "Chandrayaan-2" in names
    assert "Danuri (KPLO)" in names
    assert "CAPSTONE" in names
    assert "Queqiao-2" in names
    assert "Chang'e-4 / Yutu-2" in names
    assert "ARTEMIS P1" in names
    assert "ARTEMIS P2" in names


def test_the_grand_unoctoquadragintet_fleet_census():
    """验证人类深空四十一极黄金舰队 (The Grand Unoctoquadragintet) 严格排序与极端物理落差"""
    census = the_grand_unoctoquadragintet_fleet_census()
    fleet = census["fleet"]
    
    # 探测器数量严格为 41 艘
    assert census["probe_count"] == 41
    assert len(fleet) == 41
    
    # 严格按日心极距降序排列
    for i in range(len(fleet) - 1):
        assert fleet[i]["dist_au"] >= fleet[i + 1]["dist_au"], (
            f"Fleet ordering broken at rank {fleet[i]['rank']}: {fleet[i]['name']} ({fleet[i]['dist_au']} AU) "
            f"vs {fleet[i+1]['name']} ({fleet[i+1]['dist_au']} AU)"
        )
    
    # 验证关键边界与代表深空器
    assert fleet[0]["name"] == "Voyager 1"
    assert fleet[0]["dist_au"] == 173.22
    assert fleet[1]["name"] == "Voyager 2"
    assert fleet[1]["dist_au"] == 144.29
    assert fleet[-1]["name"] == "Parker Solar Probe"
    assert fleet[-1]["dist_au"] == 0.046
    
    # 验证新晋纳入的 5 大探测器均在名录中
    fleet_names = [f["name"] for f in fleet]
    assert "Spektr-RG" in fleet_names
    assert "Wind" in fleet_names
    assert "ACE" in fleet_names
    assert "ARTEMIS P1" in fleet_names
    assert "ARTEMIS P2" in fleet_names
    
    # 验证物理极端落差
    ext = census["extremes"]
    assert ext["distance_span_ratio"] >= 3700.0
    assert ext["solar_flux_drop_ratio"] >= 1.4e7
    assert ext["temperature_span_k"] >= 1660.0
    assert ext["voyager1_one_way_light_hours"] >= 24.0
    assert ext["communication_latency_ratio"] >= 67000.0
    assert ext["velocity_ratio"] >= 2.7e7


def test_armada_41_comprehensive_summary():
    """验证综合分析汇总数据接口一致性"""
    summary = armada_41_comprehensive_summary()
    assert summary["epoch"] == "2026-10-19 01:30 CST"
    assert summary["fleet_status"]["probe_count"] == 41
    assert len(summary["subsystems"]["l1_pentad"]) == 5
    assert len(summary["subsystems"]["l2_trinity"]) == 3
    assert len(summary["subsystems"]["lunar_octet"]) == 8
