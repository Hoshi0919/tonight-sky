#!/usr/bin/env python3
"""
mangalyaan_taurids_change1_dynamics_engine.py
============================================
2026-11-05 航天动力学与天体力学综合推演引擎：
1. 印度火星轨道探测器 Mangalyaan (Mars Orbiter Mission / MOM) 发射 13 周年：
   - PSLV-C25 (PSLV-XL) 发射与近地点 246.9 km x 远地点 23,566 km 初始轨道；
   - 440 N 液体远地点发动机 (LAM) 6 次近地点变轨抬升与奥伯斯效应 (Oberth Effect) 效率；
   - 地火转移轨道注入 (TMI)、双曲线逃逸剩余速度 (v_inf = 2.97 km/s) 与 6.8 亿 km 霍曼巡航；
   - 火星轨道捕获制动 (MOI)、421.7 km x 76,994 km 大椭圆极轨与五大科学载荷 (13.4 kg)。
2. 中国嫦娥一号 (Chang'e-1) 环月制动 19 周年华诞：
   - 2007-11-05 11:15 CST 第一次近月制动 (LOI-1, delta-v ~ 350 m/s)，切入 12 小时捕获椭圆；
   - 三次近月制动进入 200 km 极月圆轨道 (周期 127.5 分钟)；
   - 环月播放《我的祖国》等 30 首经典乐曲、CCD 120m 全月立体测绘与微波亮温反演；
   - 2009-03-01 受控撞击丰富海。
3. 南金牛座流星雨 (STA) 极大期天体力学与深潜平流层火流星物理：
   - 2P/Encke 母彗星与木星 7:2 平均运动共振 (MMR) 碎屑流；
   - 辐射点 (alpha=53.0°, delta=+15.5°) 00:29:54 CST 上海南中天 (仰角 74.27°)；
   - 北群 NTA (alpha=58.0°, delta=+22.1°) 仰角 80.87° 与昴星团 M45 (82.87°) 协同；
   - 27.3 km/s 超慢速切入气动动力学：动能密度 372.6 MJ/kg (89 倍 TNT 当量)、解离平衡真实激波停滞温度 (~3,700 K)、低烧蚀率；
   - 分米级碎屑深潜至平流层 40~50 km 以下产生万圣节慢速火流星；
   - 华东 7.70 小时 (462 分钟) 绝对纯黑天窗 (18:25 昏影终至 02:07 纤细残月升起)。
4. 历史航天纪念网络 (11月05日)：
   - 1964-11-05 水手3号发射 (火星先驱)；
   - 1967-11-05 ATS-3 静止轨道气象卫星发射 (首传全彩全景地球肖像)。

作者: Hoshi (hoshi0919@outlook.com)
日期: 2026-11-04 CST
"""

import math
from datetime import datetime, timezone
from typing import Dict, Any, List

# 天体常数
G = 6.67430e-11                  # 引力常数 m^3 kg^-1 s^-2
MU_EARTH = 398600.4418           # 地球标准引力常数 km^3 s^-2
MU_MOON = 4902.800066            # 月球引力常数 km^3 s^-2
MU_MARS = 42828.3752             # 火星引力常数 km^3 s^-2
R_EARTH = 6378.137               # 地球赤道半径 km
R_MOON = 1737.4                  # 月球半径 km
R_MARS = 3396.2                  # 火星半径 km
C_LIGHT = 299792.458             # 光速 km/s
G0 = 9.80665                     # 标准重力加速度 m/s^2


class MangalyaanTauridsChange1DynamicsEngine:
    """航天动力学与金牛座流星群极大期综合推演引擎。"""

    def __init__(self):
        pass

    # -------------------------------------------------------------
    # 1. 曼加里安号 (Mangalyaan / MOM) 动力学推演
    # -------------------------------------------------------------
    def compute_mangalyaan_dynamics(self) -> Dict[str, Any]:
        """计算印度火星轨道探测器 (MOM) 轨道提升、地火转移与火星捕获动力学。"""
        # 发射与航天器属性
        launch_date_utc = "2013-11-05 09:08:00 UTC"
        launch_date_cst = "2013-11-05 17:08:00 CST"
        anniversary_years = 13  # 2013 -> 2026
        launcher = "PSLV-C25 (PSLV-XL)"
        launch_site = "Satish Dhawan Space Centre (SDSC SHAR, Sriharikota)"

        mass_wet_kg = 1337.0     # 湿重
        mass_dry_kg = 500.0      # 干重
        propellant_mass_kg = 837.0  # MMH + N2O4
        lam_thrust_n = 440.0     # 液体远地点发动机推力 (N)
        lam_isp_s = 310.0        # 比冲 (s)

        # 初始入轨参数
        hp_initial_km = 246.9
        ha_initial_km = 23566.0
        inc_deg = 19.27
        rp_initial = R_EARTH + hp_initial_km
        ra_initial = R_EARTH + ha_initial_km
        a_initial = (rp_initial + ra_initial) / 2.0
        e_initial = (ra_initial - rp_initial) / (ra_initial + rp_initial)
        period_initial_s = 2.0 * math.pi * math.sqrt(a_initial**3 / MU_EARTH)
        period_initial_hours = period_initial_s / 3600.0

        # 近地点速度与远地点速度 (km/s)
        vp_initial = math.sqrt(MU_EARTH * (2.0 / rp_initial - 1.0 / a_initial))
        va_initial = math.sqrt(MU_EARTH * (2.0 / ra_initial - 1.0 / a_initial))

        # 6次地心近地点升轨序列实测数据
        burn_sequence = [
            {
                "burn_index": 1,
                "date_utc": "2013-11-06 19:47 UTC",
                "date_ist": "2013-11-07 01:17 IST",
                "burn_duration_s": 416.0,
                "achieved_apogee_km": 28825.0,
                "perigee_km": 252.0,
            },
            {
                "burn_index": 2,
                "date_utc": "2013-11-07 20:48 UTC",
                "date_ist": "2013-11-08 02:18 IST",
                "burn_duration_s": 570.6,
                "achieved_apogee_km": 40186.0,
                "perigee_km": 250.0,
            },
            {
                "burn_index": 3,
                "date_utc": "2013-11-08 20:40 UTC",
                "date_ist": "2013-11-09 02:10 IST",
                "burn_duration_s": 707.0,
                "achieved_apogee_km": 71636.0,
                "perigee_km": 250.0,
            },
            {
                "burn_index": 4,
                "date_utc": "2013-11-10 20:36 UTC",
                "date_ist": "2013-11-11 02:06 IST",
                "burn_duration_s": 140.0,  # partial burn (imparted 35 m/s vs planned 130 m/s)
                "achieved_apogee_km": 78276.0,
                "perigee_km": 250.0,
                "note": "Partial burn due to flow anomaly; supplementary burn scheduled"
            },
            {
                "burn_index": 5,
                "date_utc": "2013-11-11 23:33 UTC",
                "date_ist": "2013-11-12 05:03 IST",
                "burn_duration_s": 303.8,
                "achieved_apogee_km": 118642.0,
                "perigee_km": 250.0,
            },
            {
                "burn_index": 6,
                "date_utc": "2013-11-15 19:57 UTC",
                "date_ist": "2013-11-16 01:27 IST",
                "burn_duration_s": 243.5,
                "achieved_apogee_km": 192874.0,
                "perigee_km": 250.0,
            },
        ]

        # 奥伯斯效应 (Oberth Effect) 物理效益分析：
        # 在近地点 (r_p ~ 6628 km) 施加相同 delta_v 产生的机械能增量 Delta E = v * delta_v
        # 对比远地点 (r_a ~ 29944 km) 的速度，机械能增量比约为 v_p / v_a
        energy_gain_ratio_oberth = vp_initial / va_initial

        # 地火转移轨道注入 (TMI - Trans-Mars Injection)
        tmi_date_utc = "2013-11-30 19:19:00 UTC"
        tmi_date_ist = "2013-12-01 00:49:00 IST"
        tmi_burn_duration_s = 1328.89
        tmi_delta_v_m_s = 647.96
        v_hyperbolic_excess_km_s = 2.97
        c3_energy_km2_s2 = v_hyperbolic_excess_km_s**2  # ~ 8.82 km^2/s^2

        # 巡航与火星捕获制动 (MOI - Mars Orbit Insertion)
        cruise_duration_days = 298.0
        cruise_distance_km = 6.8e8
        moi_date_utc = "2014-09-24 01:47:32 UTC"
        moi_date_ist = "2014-09-24 07:17:32 IST"
        moi_burn_duration_s = 1388.67
        moi_delta_v_m_s = 1098.7
        hp_mars_km = 421.7
        ha_mars_km = 76993.6
        inc_mars_deg = 150.0
        rp_mars = R_MARS + hp_mars_km
        ra_mars = R_MARS + ha_mars_km
        a_mars = (rp_mars + ra_mars) / 2.0
        e_mars = (ra_mars - rp_mars) / (ra_mars + rp_mars)
        period_mars_s = 2.0 * math.pi * math.sqrt(a_mars**3 / MU_MARS)
        period_mars_hours = period_mars_s / 3600.0

        # 五大科学仪器载荷 (总重仅 13.4 kg)
        payloads = [
            {"instrument": "MCC", "full_name": "Mars Colour Camera", "mass_kg": 1.4, "purpose": "Surface visual tri-color features & weather dynamics"},
            {"instrument": "TIS", "full_name": "Thermal Infrared Imaging Spectrometer", "mass_kg": 3.2, "purpose": "Mineralogy and surface thermal inertia"},
            {"instrument": "MSM", "full_name": "Methane Sensor for Mars", "mass_kg": 3.0, "purpose": "Methane presence differential radiometer (1.65 um)"},
            {"instrument": "MENCA", "full_name": "Mars Exospheric Neutral Composition Analyser", "mass_kg": 4.0, "purpose": "Quadrupole mass spectrometer for exospheric species"},
            {"instrument": "LAP", "full_name": "Lyman Alpha Photometer", "mass_kg": 1.8, "purpose": "D/H ratio and hydrogen corona escape measurement"},
        ]
        total_payload_mass_kg = sum(p["mass_kg"] for p in payloads)

        # 任务成本与长寿服役
        cost_million_usd = 73.0
        designed_life_months = 6.0
        actual_operating_years = 7.58  # 2014-09 to 2022-04 (loss of signal)

        return {
            "launch_date_utc": launch_date_utc,
            "launch_date_cst": launch_date_cst,
            "anniversary_years": anniversary_years,
            "launcher": launcher,
            "launch_site": launch_site,
            "mass_wet_kg": mass_wet_kg,
            "mass_dry_kg": mass_dry_kg,
            "propellant_mass_kg": propellant_mass_kg,
            "lam_thrust_n": lam_thrust_n,
            "lam_isp_s": lam_isp_s,
            "initial_orbit": {
                "hp_km": hp_initial_km,
                "ha_km": ha_initial_km,
                "inclination_deg": inc_deg,
                "semi_major_axis_km": round(a_initial, 2),
                "eccentricity": round(e_initial, 5),
                "period_hours": round(period_initial_hours, 2),
                "v_perigee_km_s": round(vp_initial, 3),
                "v_apogee_km_s": round(va_initial, 3),
            },
            "burn_sequence": burn_sequence,
            "energy_gain_ratio_oberth": round(energy_gain_ratio_oberth, 2),
            "tmi": {
                "date_utc": tmi_date_utc,
                "date_ist": tmi_date_ist,
                "burn_duration_s": tmi_burn_duration_s,
                "delta_v_m_s": tmi_delta_v_m_s,
                "v_hyperbolic_excess_km_s": v_hyperbolic_excess_km_s,
                "c3_energy_km2_s2": round(c3_energy_km2_s2, 2),
            },
            "cruise": {
                "duration_days": cruise_duration_days,
                "distance_km": cruise_distance_km,
            },
            "moi": {
                "date_utc": moi_date_utc,
                "date_ist": moi_date_ist,
                "burn_duration_s": moi_burn_duration_s,
                "delta_v_m_s": moi_delta_v_m_s,
                "hp_km": hp_mars_km,
                "ha_km": ha_mars_km,
                "inclination_deg": inc_mars_deg,
                "semi_major_axis_km": round(a_mars, 2),
                "eccentricity": round(e_mars, 5),
                "period_hours": round(period_mars_hours, 2),
            },
            "payloads": payloads,
            "total_payload_mass_kg": round(total_payload_mass_kg, 1),
            "cost_million_usd": cost_million_usd,
            "designed_life_months": designed_life_months,
            "actual_operating_years": actual_operating_years,
        }

    # -------------------------------------------------------------
    # 2. 嫦娥一号 (Chang'e-1) 环月制动 19 周年动力学推演
    # -------------------------------------------------------------
    def compute_change1_loi_dynamics(self) -> Dict[str, Any]:
        """计算嫦娥一号 2007-11-05 第一次近月制动 (LOI-1) 与三阶入轨动力学。"""
        anniversary_years = 19
        loi1_time_utc = "2007-11-05 03:15:00 UTC"
        loi1_time_cst = "2007-11-05 11:15:00 CST"

        # 捕获椭圆轨道参数 (LOI-1 之后)
        hp_loi1_km = 210.0
        ha_loi1_km = 8600.0
        rp_loi1 = R_MOON + hp_loi1_km
        ra_loi1 = R_MOON + ha_loi1_km
        a_loi1 = (rp_loi1 + ra_loi1) / 2.0
        period_loi1_hours = 2.0 * math.pi * math.sqrt(a_loi1**3 / MU_MOON) / 3600.0

        # LOI-2 与 LOI-3 演进
        loi_steps = [
            {"step": "LOI-1", "date_cst": "2007-11-05 11:15", "orbit_desc": "210 km x 8,600 km 大椭圆", "period_hours": round(period_loi1_hours, 1), "delta_v_m_s": 350.0},
            {"step": "LOI-2", "date_cst": "2007-11-06 11:21", "orbit_desc": "213 km x 1,700 km 中椭圆", "period_hours": 3.5, "delta_v_m_s": 160.0},
            {"step": "LOI-3", "date_cst": "2007-11-07 08:34", "orbit_desc": "200 km 极月圆轨道", "period_hours": 2.125, "delta_v_m_s": 140.0},
        ]

        # 200 km 极月轨道物理特性
        r_circ_km = R_MOON + 200.0
        v_circ_km_s = math.sqrt(MU_MOON / r_circ_km)
        period_circ_min = 2.0 * math.pi * math.sqrt(r_circ_km**3 / MU_MOON) / 60.0

        # 30首环月搭载播发乐曲经典名录
        broadcast_music_samples = [
            "《我的祖国》",
            "《爱我中华》",
            "《歌唱祖国》",
            "《长江之歌》",
            "《高山流水》",
            "《梁祝》",
            "《二泉映月》",
            "《春江花月夜》",
            "《东方红》",
        ]

        # 科学遗产
        laser_altimeter_points = 9120000  # 912万有效测高点
        dem_resolution_m = 120.0
        celms_frequencies_ghz = [3.0, 7.8, 19.35, 37.0]  # 微波探测仪 4 频段

        # 受控撞击点
        impact_site = "丰富海 (Mare Fecunditatis, 1.50°S, 52.36°E)"
        impact_utc = "2009-03-01 08:13:10 UTC"

        return {
            "anniversary_years": anniversary_years,
            "loi1_time_utc": loi1_time_utc,
            "loi1_time_cst": loi1_time_cst,
            "loi_steps": loi_steps,
            "polar_orbit": {
                "altitude_km": 200.0,
                "velocity_km_s": round(v_circ_km_s, 3),
                "period_min": round(period_circ_min, 2),
                "inclination_deg": 90.0,
            },
            "broadcast_music_total": 30,
            "broadcast_music_samples": broadcast_music_samples,
            "laser_altimeter_points": laser_altimeter_points,
            "dem_resolution_m": dem_resolution_m,
            "celms_frequencies_ghz": celms_frequencies_ghz,
            "impact_site": impact_site,
            "impact_utc": impact_utc,
        }

    # -------------------------------------------------------------
    # 3. 南金牛座流星雨 (STA) 极大期天体力学与深潜火流星物理
    # -------------------------------------------------------------
    def compute_taurids_peak_mechanics(self) -> Dict[str, Any]:
        """计算 2026-11-05 南金牛座流星雨极大期辐射点、大气烧蚀热力学与上海视见几何。"""
        peak_date = "2026-11-05"
        parent_comet = "2P/Encke"
        resonance = "7:2 Jupiter Mean Motion Resonance (MMR)"

        # 辐射点中天几何 (上海 Lat=31.2304°N)
        lat_shanghai_deg = 31.2304
        
        # 南金牛座 STA
        sta_ra_deg = 53.0    # 03h 32m
        sta_dec_deg = 15.5
        sta_transit_alt_deg = 90.0 - lat_shanghai_deg + sta_dec_deg  # 74.27°
        sta_transit_time_cst = "2026-11-05 00:29:54 CST"
        sta_entry_velocity_km_s = 27.3

        # 北金牛座 NTA 协同
        nta_ra_deg = 58.0    # 03h 52m
        nta_dec_deg = 22.1
        nta_transit_alt_deg = 90.0 - lat_shanghai_deg + nta_dec_deg  # 80.87°
        nta_transit_time_cst = "2026-11-05 00:51:55 CST"
        nta_entry_velocity_km_s = 29.0

        # 天体力学近邻：昴星团 M45 与天王星
        m45_transit_alt_deg = 90.0 - lat_shanghai_deg + 24.1  # 82.87°
        m45_transit_time_cst = "2026-11-05 00:46:57 CST"
        uranus_transit_alt_deg = 90.0 - lat_shanghai_deg + 20.9 # 79.67°
        uranus_transit_time_cst = "2026-11-05 01:08:39 CST"

        # 大气切入动力学与烧蚀热力学
        v_entry = sta_entry_velocity_km_s * 1000.0  # m/s
        e_kinetic_j_kg = 0.5 * v_entry**2
        e_kinetic_mj_kg = e_kinetic_j_kg / 1e6      # 372.6 MJ/kg
        tnt_equivalent_ratio = e_kinetic_mj_kg / 4.184 # ~ 89.1 倍 TNT

        # 真实气体热化学平衡解离激波停滞温度 T_stag ~ 3,700 K (非理想气体解离吸热缓冲)
        t_stag_real_gas_k = 3700.0
        t_stag_ideal_unreacted_k = (v_entry**2) / (2.0 * 1005.0)

        # 烧蚀质量损失率对比狮子座 (Leonids, v=71 km/s)
        v_leonids = 71.0
        ablation_ratio_vs_leonids = (sta_entry_velocity_km_s / v_leonids)**3 # ~ 5.68%

        # 平流层深潜穿透深度
        deep_penetration_min_alt_km = 40.0
        deep_penetration_max_alt_km = 50.0

        # 华东绝对纯黑天窗
        sunset_cst = "17:03:30"
        astronomical_twilight_end_cst = "18:25:32"
        moonrise_cst = "2026-11-05 02:07:36"
        moon_phase_pct = 20.4
        dark_window_hours = 7.70
        dark_window_minutes = 462.0

        return {
            "peak_date": peak_date,
            "parent_comet": parent_comet,
            "resonance": resonance,
            "sta": {
                "ra_deg": sta_ra_deg,
                "dec_deg": sta_dec_deg,
                "transit_alt_deg": round(sta_transit_alt_deg, 2),
                "transit_time_cst": sta_transit_time_cst,
                "v_entry_km_s": sta_entry_velocity_km_s,
            },
            "nta": {
                "ra_deg": nta_ra_deg,
                "dec_deg": nta_dec_deg,
                "transit_alt_deg": round(nta_transit_alt_deg, 2),
                "transit_time_cst": nta_transit_time_cst,
                "v_entry_km_s": nta_entry_velocity_km_s,
            },
            "celestial_co_transit": {
                "m45_pleiades": {"transit_alt_deg": round(m45_transit_alt_deg, 2), "transit_time_cst": m45_transit_time_cst},
                "uranus": {"transit_alt_deg": round(uranus_transit_alt_deg, 2), "transit_time_cst": uranus_transit_time_cst},
            },
            "ablation_thermodynamics": {
                "e_kinetic_mj_kg": round(e_kinetic_mj_kg, 1),
                "tnt_equivalent_ratio": round(tnt_equivalent_ratio, 1),
                "stagnation_temp_real_gas_k": t_stag_real_gas_k,
                "stagnation_temp_ideal_unreacted_k": round(t_stag_ideal_unreacted_k, 0),
                "ablation_ratio_vs_leonids_pct": round(ablation_ratio_vs_leonids * 100.0, 2),
                "deep_penetration_alt_range_km": [deep_penetration_min_alt_km, deep_penetration_max_alt_km],
            },
            "dark_window": {
                "sunset_cst": sunset_cst,
                "astronomical_twilight_end_cst": astronomical_twilight_end_cst,
                "moonrise_cst": moonrise_cst,
                "moon_phase_pct": moon_phase_pct,
                "duration_hours": dark_window_hours,
                "duration_minutes": dark_window_minutes,
            }
        }

    # -------------------------------------------------------------
    # 4. 11月05日 航天历史网络联动
    # -------------------------------------------------------------
    def get_november_5_space_network(self) -> List[Dict[str, Any]]:
        """获取 11 月 5 日全历史深空与航天里程碑纪念网络。"""
        return [
            {
                "year": 1964,
                "years_elapsed": 62,
                "mission": "Mariner 3 (水手3号)",
                "agency": "NASA",
                "milestone": "首次火星飞掠任务尝试，整流罩未分离，其工程失效复盘直接保障了23天后水手4号的人类首次火星飞掠成功"
            },
            {
                "year": 1967,
                "years_elapsed": 59,
                "mission": "ATS-3 (应用技术卫星3号)",
                "agency": "NASA",
                "milestone": "地球静止轨道拍摄并传回人类第一幅全彩完整的地球圆盘全景照片"
            },
            {
                "year": 2007,
                "years_elapsed": 19,
                "mission": "Chang'e-1 (嫦娥一号)",
                "agency": "CNSA",
                "milestone": "实施第一次近月制动 (LOI-1)，中国航天器历史上首次进入地外天体环绕轨道，播发《我的祖国》"
            },
            {
                "year": 2013,
                "years_elapsed": 13,
                "mission": "Mangalyaan (Mars Orbiter Mission / MOM)",
                "agency": "ISRO",
                "milestone": "PSLV-C25 火箭发射升空，开创亚洲首次抵达火星与人类首次初战即胜火星探测壮举"
            }
        ]
