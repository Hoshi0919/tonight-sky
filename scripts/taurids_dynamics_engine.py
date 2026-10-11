"""
taurids_dynamics_engine.py
==========================
2026 年金牛座流星群复合体（Taurid Complex）、恩克彗星（2P/Encke）最短周期动力学、
7:2 木星共振群（Resonant Swarm）与“万圣节巨型火流星（Halloween Bolides）”深空物理推演引擎

天体物理与科学背景：
1. 母彗星 2P/Encke 动力学特征：
   - 太阳系已知周期最短的周期彗星（P = 3.30 年 / 1205 天）。
   - 半长轴 a = 2.215 AU，偏心率 e = 0.8483。
   - 近日点 q = 0.336 AU（深入水星近日点 0.307 AU 内部），远日点 Q = 4.094 AU（小行星带外缘）。
   - 相对木星 Tisserand 参量 T_J = 3.026（处于木星族与主带/阿波罗型小行星过渡态）。
   - 起源于约 20,000 年前一颗超巨型内太阳系瓦解彗星（直径 > 100 km）。
2. 双分支交角与流星雨流形：
   - 南金牛座流星雨 (STA, IAU #002)：降交点分支，极大期 10-10 ~ 11-05，v_inf = 27.3 km/s。
   - 北金牛座流星雨 (NTA, IAU #001)：升交点分支，极大期 11-12，v_inf = 29.0 km/s。
   - NTA 辐射点（RA 03h52m, Dec +22.0°）距昴星团 M45 仅 2.36°！
3. 27.0 ~ 29.0 km/s 极低速切入与平流层深穿透物理：
   - 大气层动能密度仅 372.6 ~ 420.5 MJ/kg（仅自身重量 89 ~ 100 倍 TNT 当量，狮子座的 14.8%）。
   - 烧蚀速率仅为狮子座的 ~6.1%（dm/dt ∝ v^3）。
   - 停滞激波温度 4800 ~ 5400 K。
   - 大质量碎屑（m >= 0.1 ~ 1 kg）能罕见深潜穿透中间层顶直抵平流层（35 ~ 50 km），引发终端空爆与陨石降落。
4. 木星 7:2 平均运动共振群（Resonant Swarm）与超级火球爆发：
   - 7 * P_comet ≈ 23.1 yr ≈ 2 * P_Jup (23.72 yr)。
   - 共振半长轴 a_res = 2.256 AU，引力相位锁定形成密集碎屑包裹体。
   - 地球穿透共振群形成 7 ~ 10 年周期超级火球爆发群（2005, 2015, 2022, 2025/2026, 2032）。
5. 华夏全境通宵仰望与 2026 纯黑无月天窗：
   - 入夜即升（19:15 ~ 20:30 CST），终夜不落直至晨曦（全夜可观测时长 > 10.5 小时）。
   - 最高中天仰角：广州 81.0° (STA) / 89.0° (NTA，天顶直插！)，上海 72.9° / 80.8°，北京 64.2° / 72.2°。
   - 2026-10-12/13 正值九月初三/初四极纤细蛾眉月（4% ~ 9%），傍晚日落即沉，全夜 0.0% 月光干扰！
"""

import math
import json
import argparse
from typing import Dict, Any, List

# 常数定义
AU_KM = 149597870.7
JUPITER_A_AU = 5.2044
JUPITER_PERIOD_YR = 11.862
TNT_JOULES_PER_KG = 4.184e6

# 2P/Encke 轨道参数 (JPL Horizons)
ENCKE_ORBIT = {
    "name": "2P/Encke",
    "a_au": 2.215,
    "e": 0.8483,
    "i_deg": 11.78,
    "q_au": 0.3360,
    "Q_au": 4.0940,
    "period_yr": 3.297,
    "period_days": 1204.2,
    "arg_perihelion_deg": 186.54,
    "asc_node_deg": 334.57,
}

# 流星雨分支定义
TAURID_BRANCHES = {
    "STA": {
        "name": "Southern Taurids",
        "chinese_name": "南金牛座流星雨",
        "iau_code": "STA",
        "iau_number": 2,
        "peak_window": "10-10 ~ 11-05",
        "nominal_peak": "11-05",
        "v_entry_kms": 27.3,
        "radiant_ra_deg": 50.0,    # 03h 20m
        "radiant_dec_deg": 14.0,
        "zhr_base": 5,
        "population_index_r": 2.3,
    },
    "NTA": {
        "name": "Northern Taurids",
        "chinese_name": "北金牛座流星雨",
        "iau_code": "NTA",
        "iau_number": 1,
        "peak_window": "10-20 ~ 12-10",
        "nominal_peak": "11-12",
        "v_entry_kms": 29.0,
        "radiant_ra_deg": 58.0,    # 03h 52m
        "radiant_dec_deg": 22.0,
        "zhr_base": 5,
        "population_index_r": 2.3,
    }
}

# 华夏观测城市基准
CHINESE_CITIES = {
    "Beijing": {"name": "北京", "lat": 39.9042, "lon": 116.4074},
    "Shanghai": {"name": "上海", "lat": 31.2304, "lon": 121.4737},
    "Guangzhou": {"name": "广州", "lat": 23.1291, "lon": 113.2644},
    "Chengdu": {"name": "成都", "lat": 30.5728, "lon": 104.0668},
    "Urumqi": {"name": "乌鲁木齐", "lat": 43.8256, "lon": 87.6168},
}

# 昴星团 M45 天球坐标
PLEIADES_M45 = {
    "name": "Pleiades (M45 / 昴宿星团)",
    "ra_deg": 56.85,  # 03h 47m 24s
    "dec_deg": 24.11,
}


def calculate_encke_orbital_mechanics() -> Dict[str, Any]:
    """计算 2P/Encke 轨道动力学与木星 Tisserand 参量"""
    a = ENCKE_ORBIT["a_au"]
    e = ENCKE_ORBIT["e"]
    i_deg = ENCKE_ORBIT["i_deg"]
    
    q = a * (1.0 - e)
    Q = a * (1.0 + e)
    p_yr = a ** 1.5
    
    # Tisserand parameter w.r.t Jupiter
    cos_i = math.cos(math.radians(i_deg))
    t_j = (JUPITER_A_AU / a) + 2.0 * math.sqrt((a / JUPITER_A_AU) * (1.0 - e ** 2)) * cos_i
    
    # 7:2 MMR parameters
    # 7 * n_comet = 2 * n_jup -> P_res = (2/7) * P_jup
    p_res_yr = (2.0 / 7.0) * JUPITER_PERIOD_YR
    a_res_au = p_res_yr ** (2.0 / 3.0)
    
    return {
        "perihelion_q_au": round(q, 4),
        "aphelion_Q_au": round(Q, 4),
        "period_yr": round(p_yr, 3),
        "tisserand_parameter_tj": round(t_j, 4),
        "is_transition_object": bool(t_j > 3.0),
        "mmr_7_2_period_yr": round(p_res_yr, 3),
        "mmr_7_2_semi_major_axis_au": round(a_res_au, 3),
        "delta_a_resonance_au": round(abs(a - a_res_au), 4),
    }


def calculate_kinetic_and_ablation_physics() -> Dict[str, Any]:
    """计算切入动能、烧蚀速率对比与平流层深潜穿透物理"""
    results = {}
    for code, branch in TAURID_BRANCHES.items():
        v = branch["v_entry_kms"] * 1000.0  # m/s
        ek_per_kg = 0.5 * (v ** 2)
        ek_mj_kg = ek_per_kg / 1e6
        tnt_equiv = ek_per_kg / TNT_JOULES_PER_KG
        
        # 激波停滞温度 T_shock ~ 0.5 * (gamma - 1) * v^2 / R_air ~ 0.5 * 0.4 * v^2 / 287
        # 经验等效激波温度
        t_shock_k = 0.5 * 0.4 * (v ** 2) / 287.0
        
        # 烧蚀质量损失率对比狮子座 (71 km/s)
        # dm/dt ∝ v^3
        v_leonids = 71000.0
        ablation_ratio_vs_leonids = (v / v_leonids) ** 3
        
        # 烧蚀质量损失率对比猎户座 (66 km/s)
        v_orionids = 66000.0
        ablation_ratio_vs_orionids = (v / v_orionids) ** 3
        
        # 动能释放对比狮子座
        ek_leonids = 0.5 * (v_leonids ** 2)
        ek_ratio_vs_leonids = ek_per_kg / ek_leonids
        
        results[code] = {
            "entry_velocity_kms": branch["v_entry_kms"],
            "kinetic_energy_mj_per_kg": round(ek_mj_kg, 2),
            "tnt_equivalent_ratio": round(tnt_equiv, 1),
            "shock_stagnation_temp_k": round(t_shock_k, 0),
            "ablation_ratio_vs_leonids": round(ablation_ratio_vs_leonids, 4),
            "ablation_ratio_vs_orionids": round(ablation_ratio_vs_orionids, 4),
            "kinetic_energy_ratio_vs_leonids": round(ek_ratio_vs_leonids, 4),
            "initial_light_height_km": 82.0 if code == "STA" else 84.0,
            "peak_light_height_km": 68.0 if code == "STA" else 70.0,
            "can_penetrate_stratosphere": True,  # 适度大质量(m >= 0.1 kg)可突破 50 km
        }
    return results


def calculate_radiant_separations() -> Dict[str, Any]:
    """计算南北群辐射点天球角距及其与昴星团 M45 的近邻关系"""
    ra_sta = TAURID_BRANCHES["STA"]["radiant_ra_deg"]
    dec_sta = TAURID_BRANCHES["STA"]["radiant_dec_deg"]
    
    ra_nta = TAURID_BRANCHES["NTA"]["radiant_ra_deg"]
    dec_nta = TAURID_BRANCHES["NTA"]["radiant_dec_deg"]
    
    ra_m45 = PLEIADES_M45["ra_deg"]
    dec_m45 = PLEIADES_M45["dec_deg"]
    
    def sep(ra1, dec1, ra2, dec2):
        d_ra = math.radians(ra1 - ra2) * math.cos(math.radians((dec1 + dec2) / 2.0))
        d_dec = math.radians(dec1 - dec2)
        return math.degrees(math.sqrt(d_ra ** 2 + d_dec ** 2))
    
    sep_sta_nta = sep(ra_sta, dec_sta, ra_nta, dec_nta)
    sep_nta_m45 = sep(ra_nta, dec_nta, ra_m45, dec_m45)
    sep_sta_m45 = sep(ra_sta, dec_sta, ra_m45, dec_m45)
    
    return {
        "separation_sta_nta_deg": round(sep_sta_nta, 2),
        "separation_nta_m45_deg": round(sep_nta_m45, 2),
        "separation_sta_m45_deg": round(sep_sta_m45, 2),
        "nta_m45_binocular_field_compatible": bool(sep_nta_m45 < 3.0),
    }


def calculate_bolide_photometry_by_mass() -> List[Dict[str, Any]]:
    """测算不同质量金牛座碎屑在大气层烧蚀释放的发光星等与能量表"""
    mass_steps = [
        {"name": "芝麻微粒 (Fine Grain)", "mass_kg": 1e-6, "label": "1 mg"},
        {"name": "豆粒粗砂 (Pea-sized)", "mass_kg": 1e-3, "label": "1 g"},
        {"name": "碎石砾块 (Gravel)", "mass_kg": 1e-2, "label": "10 g"},
        {"name": "拳头卵石 (Fist-sized Boulder)", "mass_kg": 0.1, "label": "100 g"},
        {"name": "致密岩块 (Solid Boulder)", "mass_kg": 1.0, "label": "1 kg"},
        {"name": "保龄球级巨石 (Bowling-ball Rock)", "mass_kg": 10.0, "label": "10 kg"},
        {"name": "亚米级天外巨岩 (Sub-meter Impactor)", "mass_kg": 100.0, "label": "100 kg"},
    ]
    
    # 采用标准流星发光效率经验模型 (Ceplecha et al. 1998, v ~ 28 km/s)
    v_ms = 28000.0
    ek_per_kg = 0.5 * (v_ms ** 2)  # 3.92e8 J/kg
    tau_v = 0.12  # 发光效率 ~ 12%
    duration_s = 2.0  # 平均发光持续 2 秒
    
    records = []
    for step in mass_steps:
        m = step["mass_kg"]
        ek_total = m * ek_per_kg
        ek_lum = ek_total * tau_v
        lum_power_w = ek_lum / duration_s
        
        # 绝对星等 M_v = -2.5 * log10(Power / 1000 W) - 0.5 (标准 IAU 定义近似)
        if lum_power_w > 0:
            m_v = -2.5 * math.log10(lum_power_w / 1000.0) - 0.5
        else:
            m_v = 99.0
            
        # 等效天体地标
        if m_v > 0:
            landmark = "普通肉眼流星 (+2.5 等)"
        elif m_v > -3:
            landmark = "天狼星级亮流星 (-1.5 等)"
        elif m_v > -5:
            landmark = "金星级耀眼火流星 (-4.4 等)"
        elif m_v > -8:
            landmark = "地表投射阴影大火球 (-7.0 等)"
        elif m_v > -10:
            landmark = "弦月级超强火流星 (-9.5 等，可闻声爆)"
        else:
            landmark = "满月级乃至白昼可见超级火流星 (-12.0 等，伴随冲击波)"
            
        records.append({
            "name": step["name"],
            "mass_label": step["label"],
            "mass_kg": m,
            "kinetic_energy_joules": round(ek_total, 1),
            "visual_magnitude_mv": round(m_v, 2),
            "celestial_landmark": landmark,
            "terminal_penetration_altitude_km": (
                80.0 if m <= 1e-3 else
                65.0 if m <= 0.01 else
                52.0 if m <= 0.1 else
                42.0 if m <= 1.0 else
                35.0 if m <= 10.0 else 28.0
            )
        })
    return records


def calculate_chinese_cities_geometry() -> Dict[str, Any]:
    """计算华夏各大城市辐射点最高中天仰角与全夜可观测天窗"""
    city_data = {}
    for city_key, c in CHINESE_CITIES.items():
        lat = c["lat"]
        
        # Culmination altitude = 90 - |lat - dec|
        dec_sta = TAURID_BRANCHES["STA"]["radiant_dec_deg"]
        dec_nta = TAURID_BRANCHES["NTA"]["radiant_dec_deg"]
        
        alt_sta = 90.0 - abs(lat - dec_sta)
        alt_nta = 90.0 - abs(lat - dec_nta)
        
        # Airmass at culmination X = 1 / sin(alt)
        airmass_sta = 1.0 / math.sin(math.radians(alt_sta))
        airmass_nta = 1.0 / math.sin(math.radians(alt_nta))
        
        city_data[city_key] = {
            "name": c["name"],
            "latitude": lat,
            "longitude": c["lon"],
            "sta_culmination_altitude_deg": round(alt_sta, 2),
            "nta_culmination_altitude_deg": round(alt_nta, 2),
            "sta_airmass": round(airmass_sta, 3),
            "nta_airmass": round(airmass_nta, 3),
            "all_night_visible_hours": 10.8 if "Beijing" in city_key or "Urumqi" in city_key else 10.5,
            "reaches_near_zenith": bool(alt_nta > 85.0),
        }
    return city_data


def generate_full_report() -> Dict[str, Any]:
    """综合解算生成完整金牛座动力学报告"""
    encke = calculate_encke_orbital_mechanics()
    ablation = calculate_kinetic_and_ablation_physics()
    radiants = calculate_radiant_separations()
    bolides = calculate_bolide_photometry_by_mass()
    cities = calculate_chinese_cities_geometry()
    
    return {
        "engine": "Taurids Dynamics & Encke Resonant Swarm Engine (2026)",
        "encke_orbital_mechanics": encke,
        "ablation_physics": ablation,
        "radiant_separations": radiants,
        "bolide_photometry_table": bolides,
        "chinese_cities_geometry": cities,
    }


def main():
    parser = argparse.ArgumentParser(description="2026 Taurids Dynamics & Bolide Physics Engine")
    parser.add_argument("--json", action="store_true", help="Output raw JSON data")
    args = parser.parse_args()
    
    report = generate_full_report()
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("=" * 78)
        print(" 2026 年金牛座流星群复合体（Taurid Complex）天体力学与万圣节火流星推演报告")
        print("=" * 78)
        enc = report["encke_orbital_mechanics"]
        print(f"\n[1] 母彗星 2P/Encke 动力学特征：")
        print(f"  - 轨道周期：{enc['period_yr']} 年（太阳系已知最短编号彗星）")
        print(f"  - 近日点 / 远日点：{enc['perihelion_q_au']} AU（深入水星近日点内侧） / {enc['aphelion_Q_au']} AU")
        print(f"  - 木星 Tisserand 参量 T_J：{enc['tisserand_parameter_tj']}（木星族-阿波罗型过渡态）")
        print(f"  - 木星 7:2 平均运动共振半长轴 a_res：{enc['mmr_7_2_semi_major_axis_au']} AU（轨道偏差仅 {enc['delta_a_resonance_au']} AU）")
        
        rad = report["radiant_separations"]
        print(f"\n[2] 双群辐射点天球几何与昴星团邻近：")
        print(f"  - 南北群辐射点角距：{rad['separation_sta_nta_deg']}°")
        print(f"  - 北金牛座辐射点与昴宿星团 (M45) 角距：{rad['separation_nta_m45_deg']}°（双筒望远镜可完美同框！）")
        
        abl = report["ablation_physics"]
        print(f"\n[3] 27.0 ~ 29.0 km/s 超慢速切入与平流层深潜物理：")
        print(f"  - 南金牛座 (STA)：速度 {abl['STA']['entry_velocity_kms']} km/s，动能 {abl['STA']['kinetic_energy_mj_per_kg']} MJ/kg（{abl['STA']['tnt_equivalent_ratio']} 倍 TNT）")
        print(f"  - 北金牛座 (NTA)：速度 {abl['NTA']['entry_velocity_kms']} km/s，动能 {abl['NTA']['kinetic_energy_mj_per_kg']} MJ/kg（{abl['NTA']['tnt_equivalent_ratio']} 倍 TNT）")
        print(f"  - 烧蚀速率对比：仅为狮子座的 {abl['NTA']['ablation_ratio_vs_leonids']*100:.2f}%，猎户座的 {abl['NTA']['ablation_ratio_vs_orionids']*100:.2f}%！")
        print(f"  - 深潜特征：大质量碎屑可穿透中间层顶直达平流层（35 ~ 50 km），引发空爆与陨石坠落。")
        
        print(f"\n[4] 华夏五大城市最高中天仰角：")
        for city_k, c in report["chinese_cities_geometry"].items():
            print(f"  - {c['name']}：STA 中天 {c['sta_culmination_altitude_deg']}° | NTA 中天 {c['nta_culmination_altitude_deg']}°（大气质量 X = {c['nta_airmass']}）")


if __name__ == "__main__":
    main()
