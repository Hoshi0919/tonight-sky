#!/usr/bin/env python3
"""
chandrayaan1_venera9_orionids_peak_engine.py
============================================
月船一号 (Chandrayaan-1) 发射 18 周年成年礼与月表水分子开创性探测、
金星九号 (Venera 9) 历史性首张外星地表全景图与极端地狱温压工程 51 周年、
以及 2026 猎户座流星雨 (Orionids 2026) 极大期主峰夜华夏全景天体力学推演引擎。

核心推演模块：
1. 月船一号 (Chandrayaan-1) 18 周年 (2008-10-22)：
   - PSLV-XL (C11) 五级地球变轨升高远地点 (22,860 km -> 380,000 km) 与地月中继注入 (TLI)；
   - 近月制动 (LOI, Delta-V ≈ 367 m/s) 切入 100 km 极月圆形环绕轨道 (T = 118.4 min, v = 1.633 km/s)；
   - NASA M3 光谱仪在 2.8~3.0 um 谱段首次确证月表羟基 (OH) 与水分子 (H2O) 吸收特征；
   - MIP 撞击探测器 1.69 km/s 撞击南极沙克尔顿坑与原位外逸层质谱探测；
   - 2017 年 NASA JPL 地基雷达 (Goldstone/GBT) 跨越 7.5 年成功找回在轨失联月船一号。
2. 金星九号 (Venera 9) 历史性外星首图与极端耐压耐温工程 51 周年 (1975-10-22)：
   - 10.7 km/s 高速双曲再入金星 96.5% 超浓密 CO2 大气，承受 150~180 g 峰值过载；
   - 50 km 高度抛弃降落伞，利用 2.1 米圆盘形空气动力学减速板自由落体，地表终端撞击速度仅 7~8 m/s；
   - 环形金属吸能皱褶环 (Crash Ring) 吸收 ~25 kJ 动能平稳触地；
   - 9.0 MPa (90 大气压) 极端压强与 485°C (758 K) 极端高温下的相变储热蓄冷控温 (LiNO3·3H2O 潜热 280 kJ/kg)；
   - 人类历史上首次回传外星地表 180° 全景图（坚硬多角玄武岩碎屑与地平线，打破无光海洋假说），极限运行 53 分钟。
3. 2026 猎户座流星雨极大期主峰夜 (Orionids Peak Night 2026-10-21/22)：
   - 哈雷彗星逆行冰尘以 66.0 km/s 超高速对冲地球，单位动能密度 2.18 GJ/kg (520x TNT 当量)；
   - 48% 高空等离子体电离持久余迹率；
   - 华夏全域 2.5~3.0 小时 100% 纯黑暗空天窗（月落至晨光），辐射点高达 65°~83° 中天极值，ZHR ≈ 20~25；
   - 木星 (-1.8等) 与火星 (+1.0等) 伴月镶嵌冬季大六角星空天幕。

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
MU_VENUS = 324859.0                  # 金星引力常数 km^3 s^-2
R_EARTH = 6378.137                   # 地球赤道半径 km
R_MOON = 1737.4                      # 月球半径 km
R_VENUS = 6051.8                     # 金星半径 km
C_LIGHT = 299792.458                 # 光速 km/s
G0 = 9.80665                         # 标准重力加速度 m/s^2


class Chandrayaan1Venera9OrionidsPeakEngine:
    """Chandrayaan-1、Venera 9 与 Orionids 极大夜综合物理天体力学引擎。"""

    def __init__(self):
        pass

    # -------------------------------------------------------------
    # 1. 月船一号 (Chandrayaan-1) 18 周年动力学与水分子光谱
    # -------------------------------------------------------------
    def compute_chandrayaan1_dynamics(self) -> Dict[str, Any]:
        """计算月船一号轨道提升、近月制动、100km 环月轨道及 M3 水冰光谱参数。"""
        # 初始停泊轨道与 5 次地球轨道机动 (EBN-1 ~ EBN-5)
        r_perigee = R_EARTH + 255.0     # 6,633.1 km
        r_apogee_init = R_EARTH + 22860.0  # 29,238.1 km
        r_apogee_tli = R_EARTH + 380000.0  # 386,378.1 km

        # TLI 转移椭圆近地点速度
        a_tli = (r_perigee + r_apogee_tli) / 2.0
        v_perigee_tli = math.sqrt(MU_EARTH * (2.0 / r_perigee - 1.0 / a_tli))  # km/s

        # 月球 100 km 圆轨道动力学
        r_lunar_100km = R_MOON + 100.0  # 1837.4 km
        v_circ_100km = math.sqrt(MU_MOON / r_lunar_100km)  # km/s
        t_orbit_sec = 2.0 * math.pi * math.sqrt(r_lunar_100km**3 / MU_MOON)
        t_orbit_min = t_orbit_sec / 60.0

        # 月球 200 km 轨道动力学 (2009 年及 2017 年雷达复测状态)
        r_lunar_200km = R_MOON + 200.0  # 1937.4 km
        v_circ_200km = math.sqrt(MU_MOON / r_lunar_200km)
        t_orbit_200km_min = (2.0 * math.pi * math.sqrt(r_lunar_200km**3 / MU_MOON)) / 60.0

        # LOI 制动速度增量 (双曲过剩速度 v_inf ≈ 0.82 km/s 进入 504 x 7502 km 捕获轨)
        v_inf_lunar = 0.82  # km/s
        rp_loi = R_MOON + 504.0
        ra_loi = R_MOON + 7502.0
        a_loi = (rp_loi + ra_loi) / 2.0
        v_hyp_peri = math.sqrt(v_inf_lunar**2 + 2.0 * MU_MOON / rp_loi)
        v_cap_peri = math.sqrt(MU_MOON * (2.0 / rp_loi - 1.0 / a_loi))
        dv_loi = (v_hyp_peri - v_cap_peri) * 1000.0  # m/s

        # MIP 撞击探测器动力学
        mip_impact_speed_km_s = 1.69  # km/s
        mip_descent_time_min = 25.0   # min

        # M3 光谱关键水特征波段
        m3_spectral_range_um = (0.43, 3.0)
        water_absorption_band_um = (2.8, 3.0)

        # 2017 年 JPL 地基雷达探测时延 (Goldstone 70m 雷达，地月距 ~384,400 km)
        radar_roundtrip_delay_s = (2.0 * 384400.0) / C_LIGHT

        return {
            "launch_date_utc": "2008-10-22T00:52:11Z",
            "anniversary_years": 18,
            "launcher": "PSLV-XL (C11)",
            "launch_site": "SDSC SHAR, Sriharikota, India",
            "v_perigee_tli_km_s": round(v_perigee_tli, 3),
            "loi_braking_dv_mps": round(dv_loi, 1),
            "orbit_100km_v_circ_km_s": round(v_circ_100km, 3),
            "orbit_100km_period_min": round(t_orbit_min, 2),
            "orbit_200km_period_min": round(t_orbit_200km_min, 2),
            "mip_impact_speed_km_s": mip_impact_speed_km_s,
            "mip_impact_target": "Shackleton Crater, South Pole (89.9°S)",
            "m3_spectral_range_um": m3_spectral_range_um,
            "m3_water_hydroxyl_band_um": water_absorption_band_um,
            "radar_roundtrip_delay_s": round(radar_roundtrip_delay_s, 3),
            "jpl_radar_rediscovery_year": 2017
        }

    # -------------------------------------------------------------
    # 2. 金星九号 (Venera 9) 极端地表环境与气动减速动力学
    # -------------------------------------------------------------
    def compute_venera9_landing_dynamics(self) -> Dict[str, Any]:
        """计算金星九号双曲再入、气动圆盘减速、相变热控与地表极端温压参数。"""
        # 再入与气动制动
        v_entry_km_s = 10.7           # 入轨双曲速度 km/s
        peak_deceleration_g = 168.0    # 150~180 g
        chute_jettison_alt_km = 50.0  # 50 km 高度切伞
        aero_disk_diameter_m = 2.1    # 2.1 米气动减速环

        # 金星地表大气与终端撞击速度
        rho_venus_surface = 65.0      # kg/m^3 (地表二氧化碳密度，地球海平面的 ~54 倍)
        lander_impact_mass_kg = 660.0 # 落地时仪器舱核心质量
        cd_disk = 1.2                 # 气动圆盘阻力系数
        s_disk = math.pi * (aero_disk_diameter_m / 2.0)**2  # 3.4636 m^2

        # 终端沉降速度 v_term = sqrt(2 * m * g / (rho * Cd * S))
        g_venus = 8.87                # m/s^2 (金星表面重力)
        v_terminal = math.sqrt((2.0 * lander_impact_mass_kg * g_venus) / (rho_venus_surface * cd_disk * s_disk))
        kinetic_energy_impact_kj = 0.5 * lander_impact_mass_kg * (v_terminal**2) / 1000.0

        # 地表极端热压环境
        surface_pressure_mpa = 9.0    # 90 个地球标准大气压
        surface_pressure_bar = 90.0
        equivalent_ocean_depth_m = 900.0
        surface_temp_c = 485.0
        surface_temp_k = surface_temp_c + 273.15

        # 相变储热蓄冷材料性能 (LiNO3·3H2O)
        phase_change_material = "LiNO3·3H2O (Lithium Nitrate Trihydrate)"
        latent_heat_kj_per_kg = 280.0
        pcm_mass_kg = 35.0
        heat_absorption_capacity_mj = (pcm_mass_kg * latent_heat_kj_per_kg) / 1000.0

        # 表面科学运行时间
        operational_duration_min = 53.0
        designed_duration_min = 30.0

        return {
            "landing_date_utc": "1975-10-22T05:13:00Z",
            "anniversary_years": 51,
            "landing_site": "Beta Regio (31.01°N, 291.64°E)",
            "v_entry_km_s": v_entry_km_s,
            "peak_deceleration_g": peak_deceleration_g,
            "chute_cut_altitude_km": chute_jettison_alt_km,
            "aero_disk_diameter_m": aero_disk_diameter_m,
            "venus_surface_density_kg_m3": rho_venus_surface,
            "terminal_impact_velocity_m_s": round(v_terminal, 2),
            "terminal_impact_velocity_km_h": round(v_terminal * 3.6, 1),
            "impact_kinetic_energy_kj": round(kinetic_energy_impact_kj, 1),
            "surface_pressure_mpa": surface_pressure_mpa,
            "surface_pressure_bar": surface_pressure_bar,
            "equivalent_ocean_depth_m": equivalent_ocean_depth_m,
            "surface_temp_c": surface_temp_c,
            "surface_temp_k": round(surface_temp_k, 2),
            "pcm_material": phase_change_material,
            "heat_absorption_capacity_mj": round(heat_absorption_capacity_mj, 1),
            "operational_duration_min": operational_duration_min,
            "first_extraterrestrial_surface_photo": True,
            "panorama_field_of_view_deg": 180.0
        }

    # -------------------------------------------------------------
    # 3. 2026 猎户座流星雨极大期主峰夜华夏全域暗空推演
    # -------------------------------------------------------------
    def compute_orionids_peak_night_dynamics(self) -> Dict[str, Any]:
        """计算 2026-10-21 至 10-22 极大期主峰物理碰撞与华夏暗空观测天窗。"""
        # 哈雷彗星逆行流星尘埃碰撞动力学
        v_meteor_km_s = 66.0
        v_meteor_m_s = v_meteor_km_s * 1000.0
        kinetic_energy_density_gj_per_kg = 0.5 * (v_meteor_m_s**2) / 1e9  # GJ/kg
        tnt_equivalent_kg_per_kg = (kinetic_energy_density_gj_per_kg * 1e9) / 4.184e6  # 1 kg TNT = 4.184 MJ
        persistent_train_fraction = 0.48  # 48% 电离持久余迹率
        zhr_peak_nominal = 23             # 标称 ZHR 20~25

        # 辐射点中天仰角与极大夜天窗 (2026-10-21 23:00 至 10-22 05:00 CST)
        cities_observation = [
            {"city": "上海", "lat": 31.23, "lon": 121.47, "moonset": "01:46", "dawn": "04:41", "window_hr": 2.92, "culm_alt": 74.8},
            {"city": "北京", "lat": 39.90, "lon": 116.40, "moonset": "01:57", "dawn": "04:58", "window_hr": 3.02, "culm_alt": 66.1},
            {"city": "广州", "lat": 23.13, "lon": 113.26, "moonset": "02:28", "dawn": "05:04", "window_hr": 2.60, "culm_alt": 82.7},
            {"city": "成都", "lat": 30.67, "lon": 104.06, "moonset": "02:59", "dawn": "05:32", "window_hr": 2.55, "culm_alt": 75.3},
            {"city": "西安", "lat": 34.34, "lon": 108.94, "moonset": "02:35", "dawn": "05:17", "window_hr": 2.70, "culm_alt": 71.7},
            {"city": "拉萨", "lat": 29.65, "lon": 91.13, "moonset": "03:48", "dawn": "06:21", "window_hr": 2.55, "culm_alt": 76.4}
        ]

        # 辐射点仰角几何增益 factor = sin^1.4(alt)
        for c in cities_observation:
            alt_rad = math.radians(c["culm_alt"])
            c["elevation_efficiency_factor"] = round(math.sin(alt_rad)**1.4, 3)

        return {
            "parent_comet": "1P/Halley",
            "comet_orbital_period_years": 76.0,
            "entry_velocity_km_s": v_meteor_km_s,
            "kinetic_energy_density_gj_per_kg": round(kinetic_energy_density_gj_per_kg, 2),
            "tnt_equivalent_kg_per_kg": round(tnt_equivalent_kg_per_kg, 1),
            "persistent_train_fraction": persistent_train_fraction,
            "zhr_peak": zhr_peak_nominal,
            "radiant_ra": "06h 20m (95.0°)",
            "radiant_dec": "+16.0°",
            "moon_phase_pct": 77.2,
            "peak_window_cst": "2026-10-21 23:00 ~ 2026-10-22 04:00 CST",
            "city_dark_windows": cities_observation
        }


if __name__ == "__main__":
    engine = Chandrayaan1Venera9OrionidsPeakEngine()
    print("=== 1. 月船一号 18 周年成年礼动力学 ===")
    print(engine.compute_chandrayaan1_dynamics())
    print("\n=== 2. 金星九号 51 周年极端地表环境与着陆动力学 ===")
    print(engine.compute_venera9_landing_dynamics())
    print("\n=== 3. 2026 猎户座流星雨极大期主峰夜华夏推演 ===")
    print(engine.compute_orionids_peak_night_dynamics())
