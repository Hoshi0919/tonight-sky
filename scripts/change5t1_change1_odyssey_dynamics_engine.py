#!/usr/bin/env python3
"""
change5t1_change1_odyssey_dynamics_engine.py
============================================
嫦娥五号T1试验器 (小飞) 12 周年与第二宇宙速度半弹道跳跃再入动力学、
嫦娥一号 (Chang'e-1) 19 周年发射华诞与中国探月第一期全月立体测绘工程、
以及 2001 火星奥德赛号 (Mars Odyssey) 火星轨道切入 25 周年气动减速银禧动力学推演引擎。

核心推演模块：
1. 嫦娥五号T1试验器 (Chang'e 5-T1 "Xiaofei") 12 周年 (2014-10-24 02:00 CST / 10-23 18:00 UTC)：
   - 长征三号丙改二型 (CZ-3C/G2) 地月自由返回轨道 (Lunar Free-Return Trajectory)；
   - 飞掠近月点高度 ~11,300 km，无需主推进被动重力弹弓返航；
   - 接近第二宇宙速度 (10.87 km/s) 半弹道跳跃式再入 ("太空打水漂", Skip Reentry)；
   - 初次再入走廊 (γ ≈ -5.8°)，初次下沉至 ~60 km，升阻比 L/D ≈ 0.32 提供升力弹跳出大气层；
   - 弹跳滑行弧段爬升至 ~140 km 高空，耗散 30.2 MJ/kg 初始动能；
   - 二次受控再入并平稳降落四子王旗，将峰值过载从弹道再入的 >16g 骤降至 <4.8g；
   - 服务舱地月 L2 点 Halo 轨道、DRO 逆行远距轨道与极月圆轨道多重轨道拓展。
2. 嫦娥一号 (Chang'e-1) 19 周年发射华诞 (2007-10-24 18:05 CST / 10:05 UTC)：
   - 长征三号甲 (CZ-3A) 阶梯式变轨奔月轨道 (16h -> 24h -> 48h -> TLI)；
   - 3 次近月制动进入 200 km 极月圆轨道 (v = 1.591 km/s, T = 127.5 min)；
   - CCD 立体相机与激光高度计绘制中国首幅 120 米全月 3D 数字地形图；
   - 微波探测仪 (CELMS) 首创微波频段全月壤微波亮温反演与氦-3 资源估算 (~103 万吨)；
   - 2009-03-01 受控撞击月球丰富海圆满谢幕。
3. 2001 火星奥德赛号 (Mars Odyssey) 轨道切入 25 周年银禧 (2001-10-24 02:26 UTC)：
   - 2001-10-24 MOI 轨道切入 (Δv = 1431 m/s)，进入 18.6 小时捕获轨道；
   - 76 天 335 次火星高层大气气动减速 (Aerobraking)，节省 >200 kg 推进剂，切入 400 km 极圆轨道 (v = 3.359 km/s, T = 118.4 min)；
   - 伽马射线谱仪 (GRS) 与中子谱仪首次确证火星高纬度浅表层富含 20%~50% 质量比水冰；
   - 连续在轨服役 25 年，NASA 最长寿火星轨道器，承担漫游车中继主力。
4. 2026-10-23 / 2026-10-24 夜空与超级满月前夕天体力学：
   - 农历九月十四/十五盈凸月 (91.8% -> 97.2%)，距 10-26 年度近地超级满月 3~2 天；
   - 猎户座流星雨极盛后余波与黎明前月落纯黑视窗；
   - 木星 (-1.84 等) 与火星 (+0.98 等) 冬季大六角星空巡礼。

作者: Hoshi (hoshi0919@outlook.com)
日期: 2026-10-21
"""

import math
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Tuple

# 物理与天体常数
G = 6.67430e-11                      # 引力常数 m^3 kg^-1 s^-2
MU_EARTH = 398600.4418               # 地球引力常数 km^3 s^-2
MU_MOON = 4902.800066                # 月球引力常数 km^3 s^-2
MU_MARS = 42828.3752                 # 火星引力常数 km^3 s^-2
R_EARTH = 6378.137                   # 地球赤道半径 km
R_MOON = 1737.4                      # 月球半径 km
R_MARS = 3396.2                      # 火星半径 km
C_LIGHT = 299792.458                 # 光速 km/s
G0 = 9.80665                         # 标准重力加速度 m/s^2


class Change5T1Change1OdysseyDynamicsEngine:
    """嫦娥五号T1、嫦娥一号与火星奥德赛号深空动力学推演引擎。"""

    def __init__(self):
        pass

    # -------------------------------------------------------------
    # 1. 嫦娥五号T1试验器 (小飞) 12 周年与半弹道跳跃再入动力学
    # -------------------------------------------------------------
    def compute_change5t1_dynamics(self) -> Dict[str, Any]:
        """计算嫦娥五号T1地月自由返回轨道、跳跃再入气动力学与服务舱拓展机动。"""
        # 自由返回轨道几何
        h_perigee_tli = 209.0               # TLI 近地点高度 km
        r_perigee_tli = R_EARTH + h_perigee_tli
        v_tli = 10.92                        # km/s
        h_periselenium = 11300.0            # 近月点高度 km
        r_periselenium = R_MOON + h_periselenium
        v_periselenium = math.sqrt(2 * MU_MOON / r_periselenium + 0.82)  # 约 1.18 km/s
        mission_duration_hours = 196.0      # 8.17 天

        # 再入走廊与打水漂动力学
        v_entry = 10.87                     # 大气层入口速度 km/s (~第二宇宙速度)
        v_entry_mps = v_entry * 1000.0      # m/s
        gamma_entry_deg = -5.8              # 再入倾角 度
        h_dip1_min = 60.0                   # 首次再入最低高度 km
        v_skip_exit = 7.60                  # 首次跃出大气层速度 km/s
        v_skip_exit_mps = v_skip_exit * 1000.0
        h_skip_apogee = 140.0               # 跃出最高拱点 km

        # 动能耗散与热流缩放
        # Delta E = 0.5 * (v1^2 - v2^2)
        delta_e_mj_kg = 0.5 * (v_entry_mps**2 - v_skip_exit_mps**2) / 1e6  # MJ/kg
        fraction_e_dissipated = (v_entry_mps**2 - v_skip_exit_mps**2) / (v_entry_mps**2)

        # 升阻比与过载抑制
        lift_to_drag_ratio = 0.32           # L/D
        ballistic_g_load = 16.8             # 纯弹道再入理论峰值过载 g
        skip_peak_g_load = 4.75             # 跳跃再入实测峰值过载 g
        g_load_reduction_pct = (ballistic_g_load - skip_peak_g_load) / ballistic_g_load * 100.0

        # 服务舱扩展任务
        sm_l2_halo_date = "2014-11-28"
        sm_dro_date = "2015-01-11"
        sm_lunar_orbit_date = "2015-03-07"
        sm_lunar_orbit_h = 200.0

        return {
            "mission": "Chang'e 5-T1 (小飞)",
            "launch_cst": "2014-10-24 02:00 CST",
            "launch_utc": "2014-10-23 18:00 UTC",
            "anniversary_years": 12,
            "launcher": "Long March 3C/G2 (长征三号丙改二型)",
            "v_tli_km_s": v_tli,
            "periselenium_altitude_km": h_periselenium,
            "mission_duration_hours": mission_duration_hours,
            "v_entry_km_s": v_entry,
            "entry_flight_path_angle_deg": gamma_entry_deg,
            "first_dip_min_alt_km": h_dip1_min,
            "skip_apogee_alt_km": h_skip_apogee,
            "v_skip_exit_km_s": v_skip_exit,
            "energy_dissipated_first_skip_mj_kg": round(delta_e_mj_kg, 2),
            "energy_dissipated_pct": round(fraction_e_dissipated * 100.0, 1),
            "lift_to_drag_ratio": lift_to_drag_ratio,
            "peak_g_load_skip": skip_peak_g_load,
            "peak_g_load_ballistic": ballistic_g_load,
            "g_load_reduction_pct": round(g_load_reduction_pct, 1),
            "touchdown_site": "四子王旗着陆场 (Siziwang Banner)",
            "touchdown_date_cst": "2014-11-01 06:42 CST",
            "service_module_extensions": {
                "l2_halo": sm_l2_halo_date,
                "dro": sm_dro_date,
                "circular_orbit_200km": sm_lunar_orbit_date
            }
        }

    # -------------------------------------------------------------
    # 2. 嫦娥一号 19 周年发射华诞与探月工程全月立体测绘
    # -------------------------------------------------------------
    def compute_change1_dynamics(self) -> Dict[str, Any]:
        """计算嫦娥一号阶梯升轨、近月制动、200km 极圆工作轨及科学载荷成果。"""
        # 阶梯式地球调相机动
        # 轨道1: 16小时轨道 (200 x 51,000 km)
        a1 = (2 * R_EARTH + 200.0 + 51000.0) / 2.0
        v_p1 = math.sqrt(MU_EARTH * (2.0 / (R_EARTH + 200.0) - 1.0 / a1))
        t1_hours = 2 * math.pi * math.sqrt(a1**3 / MU_EARTH) / 3600.0

        # 轨道2: 24小时轨道 (200 x 73,000 km)
        a2 = (2 * R_EARTH + 200.0 + 73000.0) / 2.0
        v_p2 = math.sqrt(MU_EARTH * (2.0 / (R_EARTH + 200.0) - 1.0 / a2))
        t2_hours = 2 * math.pi * math.sqrt(a2**3 / MU_EARTH) / 3600.0

        # 轨道3: 48小时轨道 (200 x 128,000 km)
        a3 = (2 * R_EARTH + 200.0 + 128000.0) / 2.0
        v_p3 = math.sqrt(MU_EARTH * (2.0 / (R_EARTH + 200.0) - 1.0 / a3))
        t3_hours = 2 * math.pi * math.sqrt(a3**3 / MU_EARTH) / 3600.0

        # 200 km 极月圆轨道
        r_circ_moon = R_MOON + 200.0
        v_circ_moon = math.sqrt(MU_MOON / r_circ_moon)
        t_circ_moon_min = 2 * math.pi * math.sqrt(r_circ_moon**3 / MU_MOON) / 60.0

        # 科学成果与参数
        dem_resolution_m = 120.0            # 全月 3D 数字高程模型分辨率
        laser_altimeter_points = 3200000    # 激光高度计有效激光点数 > 300万
        celms_frequencies_ghz = [3.0, 7.8, 19.35, 37.0]
        he3_reserve_estimate_tons = 1030000.0  # 约 103 万吨全月氦-3 资源
        impact_date_utc = "2009-03-01 08:13:10 UTC"
        impact_site = "丰富海 (Mare Fecunditatis, 1.50°S, 52.36°E)"

        return {
            "mission": "Chang'e-1 (嫦娥一号)",
            "launch_cst": "2007-10-24 18:05 CST",
            "launch_utc": "2007-10-24 10:05 UTC",
            "anniversary_years": 19,
            "launcher": "Long March 3A (长征三号甲)",
            "phasing_orbits": [
                {"period_hours": round(t1_hours, 1), "apogee_km": 51000.0, "v_perigee_km_s": round(v_p1, 3)},
                {"period_hours": round(t2_hours, 1), "apogee_km": 73000.0, "v_perigee_km_s": round(v_p2, 3)},
                {"period_hours": round(t3_hours, 1), "apogee_km": 128000.0, "v_perigee_km_s": round(v_p3, 3)},
            ],
            "polar_orbit_alt_km": 200.0,
            "polar_orbit_v_circ_km_s": round(v_circ_moon, 3),
            "polar_orbit_period_min": round(t_circ_moon_min, 2),
            "dem_resolution_m": dem_resolution_m,
            "laser_altimeter_points": laser_altimeter_points,
            "celms_frequencies_ghz": celms_frequencies_ghz,
            "estimated_he3_reserve_tons": he3_reserve_estimate_tons,
            "controlled_impact_site": impact_site,
            "controlled_impact_utc": impact_date_utc
        }

    # -------------------------------------------------------------
    # 3. 火星奥德赛号 (Mars Odyssey) 轨道切入 25 周年与水冰探测
    # -------------------------------------------------------------
    def compute_mars_odyssey_dynamics(self) -> Dict[str, Any]:
        """计算 2001 火星奥德赛号 MOI 轨道切入、气动减速及水冰探测突破。"""
        # 初始火星轨道切入
        h_peri_initial = 328.0              # km
        h_apo_initial = 27000.0             # km
        r_p_ini = R_MARS + h_peri_initial
        r_a_ini = R_MARS + h_apo_initial
        a_ini = (r_p_ini + r_a_ini) / 2.0
        v_peri_ini = math.sqrt(MU_MARS * (2.0 / r_p_ini - 1.0 / a_ini))
        t_ini_hours = 2 * math.pi * math.sqrt(a_ini**3 / MU_MARS) / 3600.0

        # 400 km 科学工作轨道
        h_sci = 400.0
        r_sci = R_MARS + h_sci
        v_sci_circ = math.sqrt(MU_MARS / r_sci)
        t_sci_min = 2 * math.pi * math.sqrt(r_sci**3 / MU_MARS) / 60.0

        # 气动减速 (Aerobraking) 工程收益
        aerobraking_passes = 335
        aerobraking_duration_days = 76
        propellant_saved_kg = 200.0         # 节省推进剂质量 > 200 kg
        equivalent_delta_v_mps = 1200.0     # 相当于约 1200 m/s 气动速度增量

        # 科学成果与水冰发现
        ice_weight_fraction_min_pct = 20.0
        ice_weight_fraction_max_pct = 50.0
        grs_instruments = ["Gamma Ray Spectrometer (GRS)", "Neutron Spectrometer (NS)", "High Energy Neutron Detector (HEND)"]
        themis_camera = "Thermal Emission Imaging System (THEMIS)"
        continuous_active_years = 25

        return {
            "mission": "2001 Mars Odyssey (火星奥德赛号)",
            "moi_date_utc": "2001-10-24 02:26 UTC",
            "moi_date_pdt": "2001-10-23 19:26 PDT",
            "anniversary_years": 25,
            "initial_orbit": {
                "periapsis_alt_km": h_peri_initial,
                "apoapsis_alt_km": h_apo_initial,
                "period_hours": round(t_ini_hours, 2),
                "v_periapsis_km_s": round(v_peri_ini, 3)
            },
            "aerobraking": {
                "duration_days": aerobraking_duration_days,
                "atmospheric_passes": aerobraking_passes,
                "propellant_saved_kg": propellant_saved_kg,
                "equivalent_delta_v_mps": equivalent_delta_v_mps
            },
            "science_orbit": {
                "altitude_km": h_sci,
                "inclination_deg": 93.1,
                "v_circ_km_s": round(v_sci_circ, 3),
                "period_min": round(t_sci_min, 2)
            },
            "water_ice_discovery": {
                "soil_depth_m": 1.0,
                "ice_mass_fraction_pct": (ice_weight_fraction_min_pct, ice_weight_fraction_max_pct),
                "spectrometers": grs_instruments
            },
            "continuous_operating_years": continuous_active_years
        }

    # -------------------------------------------------------------
    # 4. 2026-10-23 / 2026-10-24 夜空与超级满月前瞻推演
    # -------------------------------------------------------------
    def compute_sky_mechanics_2026_10_23_24(self) -> Dict[str, Any]:
        """计算 2026-10-23 与 2026-10-24 华夏夜空、月落时间与超级满月倒计时。"""
        # 超级满月常数
        supermoon_dt_cst = "2026-10-26 04:12 CST"
        supermoon_perigee_distance_km = 357219.0

        days_to_supermoon_23 = 3
        days_to_supermoon_24 = 2

        # 2026-10-23 (农历九月十四)
        d23_illumination = 91.8
        d23_moonset_cst = "03:46:10 CST"
        d23_darksky_window_min = 56.0       # 03:46 到 04:42 天文晨光

        # 2026-10-24 (农历九月十五)
        d24_illumination = 97.2
        d24_moonset_cst = "04:49:21 CST"

        return {
            "supermoon_target": {
                "peak_cst": supermoon_dt_cst,
                "perigee_distance_km": supermoon_perigee_distance_km
            },
            "2026-10-23": {
                "lunar_calendar": "农历九月十四",
                "phase_name": "盈凸月",
                "illumination_pct": d23_illumination,
                "moonset_cst": d23_moonset_cst,
                "darksky_window_min": d23_darksky_window_min,
                "days_to_supermoon": days_to_supermoon_23
            },
            "2026-10-24": {
                "lunar_calendar": "农历九月十五",
                "phase_name": "望月渐近 (近全月)",
                "illumination_pct": d24_illumination,
                "moonset_cst": d24_moonset_cst,
                "days_to_supermoon": days_to_supermoon_24
            },
            "celestial_highlights": [
                "猎户座流星雨极盛后余波持续 (ZHR ≈ 10~15)",
                "木星 (-1.84 等) 辉映双子座南侧与金牛座毕星团",
                "火星 (+0.98 等) 穿行双子座腰部",
                "后半夜冬季大六角 (参宿七、天狼星、南河三、北河三、五车二、毕宿五) 辉煌升起"
            ]
        }


if __name__ == "__main__":
    engine = Change5T1Change1OdysseyDynamicsEngine()
    ch5 = engine.compute_change5t1_dynamics()
    ch1 = engine.compute_change1_dynamics()
    ody = engine.compute_mars_odyssey_dynamics()
    sky = engine.compute_sky_mechanics_2026_10_23_24()

    print("=== Chang'e 5-T1 Dynamics ===")
    print(f"Mission: {ch5['mission']}, Launch: {ch5['launch_cst']}")
    print(f"Skip Reentry: Entry {ch5['v_entry_km_s']} km/s -> Skip out {ch5['v_skip_exit_km_s']} km/s")
    print(f"Energy Dissipated: {ch5['energy_dissipated_first_skip_mj_kg']} MJ/kg ({ch5['energy_dissipated_pct']}%)")
    print(f"Peak G-Load: {ch5['peak_g_load_skip']}g (vs Ballistic {ch5['peak_g_load_ballistic']}g, reduced {ch5['g_load_reduction_pct']}%)")

    print("\n=== Chang'e-1 Dynamics ===")
    print(f"Mission: {ch1['mission']}, Launch: {ch1['launch_cst']}")
    print(f"Polar Orbit 200km: v = {ch1['polar_orbit_v_circ_km_s']} km/s, T = {ch1['polar_orbit_period_min']} min")
    print(f"CELMS He-3 reserve: {ch1['estimated_he3_reserve_tons']} tons, DEM: {ch1['dem_resolution_m']}m")

    print("\n=== Mars Odyssey Dynamics ===")
    print(f"Mission: {ody['mission']}, MOI: {ody['moi_date_utc']}")
    print(f"Aerobraking: {ody['aerobraking']['atmospheric_passes']} passes, {ody['aerobraking']['propellant_saved_kg']} kg propellant saved")
    print(f"Water ice: {ody['water_ice_discovery']['ice_mass_fraction_pct']}% mass fraction in top 1m soil")

    print("\n=== Sky Mechanics 2026-10-23/24 ===")
    print(f"2026-10-23: {sky['2026-10-23']['lunar_calendar']} Illum {sky['2026-10-23']['illumination_pct']}%, Moonset {sky['2026-10-23']['moonset_cst']}")
    print(f"2026-10-24: {sky['2026-10-24']['lunar_calendar']} Illum {sky['2026-10-24']['illumination_pct']}%, Moonset {sky['2026-10-24']['moonset_cst']}")
