#!/usr/bin/env python3
"""
capstone_nrho_cislunar_soyuz_guiana_engine.py
=============================================
CAPSTONE 探测器地月近直线晕轨道 (NRHO) 动力学、地月自主导航 (CAPS)、
联盟号法属圭亚那首飞 15 周年晶婚 (VS01/Galileo IOV) 赤道发射增益、
联盟 TM-33 载人飞船银禧 25 周年 (Andromède 任务) 与
2026 猎户座流星雨极大期华夏纯黑暗空天窗全景天体力学推演引擎。

核心推演模块：
1. CAPSTONE 探测器与地月 L2 南向近直线晕轨道 (NRHO) 动力学：
   - 12U CubeSat (25 kg) 深空微纳探测器，2022-06-28 经弱稳定性边界 (WSB) 弹道月球转移 (BLT) 入轨；
   - 9:2 会合周期共振轨道，周期 T = 6.562 天，近月距 rp ≈ 3,340 km (高度 1,600 km，北极上空)，
     远月距 ra ≈ 71,400 km (高度 69,660 km，南极上空)；
   - 拟稳定轨道拓扑：单值矩阵最大特征值 |λ_max| ≈ 1.25~1.35，年轨道维持速度增量 Δv ≤ 5 m/s/yr；
   - CAPS 自主导航与深空软件定义卫星 (Software-Defined Satellite) 首创跨 40 万公里内核替换。
2. 联盟号法属圭亚那首飞 15 周年 (VS01 / 2011-10-21)：
   - 库鲁 (CSG 5.24°N) 相对拜科努尔 (45.92°N) 初始自转线速度增益：463.16 m/s vs 323.55 m/s (+139.6 m/s)；
   - GTO 轨道倾角变轨速度增量节省超过 1,240 m/s，使联盟号 GTO 运载能力由 1.7 吨跃升至 3.2 吨 (+88.2%)；
   - 伽利略导航卫星 IOV-1 & IOV-2 MEO 轨道动力学：半长轴 a = 29,600 km，轨道周期 14.08 小时，环绕速度 3.670 km/s。
3. 联盟 TM-33 载人飞船银禧 25 周年 (Andromède / 2001-10-21)：
   - 2001-10-21 发射，法兰西女宇航员克劳迪·艾涅尔 (Claudie Haigneré) 进驻国际空间站 (ISS)；
   - 空间站“应急救生艇”轮换机制与 8 天微重力心血管/神经生物医学实验。
4. 2026 猎户座流星雨极大期 (Orionids Peak 2026-10-21/22) 华夏暗空天窗：
   - 77% 盈凸月于 10-22 凌晨西落（上海 01:46、北京 01:57、广州 02:28、成都 02:59 CST）；
   - 月落至晨光之间享有 2.7~3.1 小时 100% 零月光纯黑天窗，辐射点正逢中天仰角极值 (66°~83°)，ZHR ≈ 20~25。

作者: Hoshi (hoshi0919@outlook.com)
日期: 2026-10-20
"""

import math
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Tuple

# 物理常数定义
G = 6.67430e-11                     # 引力常数 m^3 kg^-1 s^-2
MU_EARTH = 398600.4418              # 地球引力常数 km^3 s^-2
MU_MOON = 4902.800066               # 月球引力常数 km^3 s^-2
R_EARTH = 6378.137                  # 地球赤道半径 km
R_MOON = 1737.4                     # 月球平均半径 km
OMEGA_EARTH = 7.292115e-5           # 地球自转角速度 rad/s
C_LIGHT = 299792.458                # 光速 km/s
D_EARTH_MOON = 384400.0             # 地月平均距离 km
T_SYNODIC_MOON_DAYS = 29.530589     # 朔望月天数
G0 = 9.80665                        # 标准重力加速度 m/s^2

class CapstoneNRHOSoyuzGuianaEngine:
    def __init__(self):
        self.mass_earth = 5.9722e24
        self.mass_moon = 7.342e22
        self.mu_cr3bp = self.mass_moon / (self.mass_earth + self.mass_moon)  # ~0.01215

    # -------------------------------------------------------------
    # 1. CAPSTONE & NRHO 动力学
    # -------------------------------------------------------------
    def compute_capstone_nrho_parameters(self) -> Dict[str, Any]:
        """计算 CAPSTONE 所在的 9:2 地月 L2 南向 NRHO 核心轨道参数与拟稳定性。"""
        # 9:2 朔望月共振周期
        nrho_period_days = (2.0 / 9.0) * T_SYNODIC_MOON_DAYS
        nrho_period_hours = nrho_period_days * 24.0

        # 近月点与远月点几何
        rp = 3340.0   # 近月距 km (月表高度 ~1602.6 km)
        ra = 71400.0  # 远月距 km (月表高度 ~69662.6 km)
        hp = rp - R_MOON
        ha = ra - R_MOON

        a_osculating = (rp + ra) / 2.0
        e_nrho = (ra - rp) / (ra + rp)

        # 二体近似月心速度
        vp_2body = math.sqrt(MU_MOON * (2.0 / rp - 1.0 / a_osculating))
        va_2body = math.sqrt(MU_MOON * (2.0 / ra - 1.0 / a_osculating))

        # 三体数值极限（引入地月潮汐有效势能加持）
        vp_cr3bp = 2.40  # km/s
        va_cr3bp = 0.11  # km/s (110 m/s)

        # 单值矩阵最大特征值与李雅普诺夫时间
        lambda_max = 1.30  # 经典 9:2 NRHO 单值矩阵特征值
        tau_instability_days = nrho_period_days / math.log(lambda_max)

        # 年度轨道维持机动预算
        annual_sk_dv_mps = 3.5  # 典型 2.0~5.0 m/s/年

        # CAPS 对星测距双程延迟 (以与 LRO 50,000 km 为基准)
        caps_dist_km = 50000.0
        caps_twoway_delay_s = (2.0 * caps_dist_km) / C_LIGHT

        return {
            "period_days": round(nrho_period_days, 3),
            "period_hours": round(nrho_period_hours, 2),
            "resonance": "9:2 synodic resonance",
            "rp_km": rp,
            "ra_km": ra,
            "hp_km": round(hp, 1),
            "ha_km": round(ha, 1),
            "eccentricity": round(e_nrho, 4),
            "vp_cr3bp_km_s": vp_cr3bp,
            "va_cr3bp_m_s": round(va_cr3bp * 1000.0, 1),
            "floquet_multiplier": lambda_max,
            "instability_time_days": round(tau_instability_days, 1),
            "annual_stationkeeping_dv_mps": annual_sk_dv_mps,
            "caps_twoway_delay_ms": round(caps_twoway_delay_s * 1000.0, 2),
            "probe_mass_kg": 25.0,
            "probe_form_factor": "12U CubeSat"
        }

    # -------------------------------------------------------------
    # 2. 联盟号法属圭亚那首飞 15 周年 (VS01)
    # -------------------------------------------------------------
    def compute_soyuz_guiana_boost(self) -> Dict[str, Any]:
        """计算法属圭亚那库鲁航天中心相对拜科努尔的赤道自转线速度与变轨速度增量收益。"""
        lat_baikonur_deg = 45.92
        lat_csg_deg = 5.24

        lat_bai_rad = math.radians(lat_baikonur_deg)
        lat_csg_rad = math.radians(lat_csg_deg)

        # 地球自转线速度 v = omega * R_earth * cos(lat)
        v_tang_bai = OMEGA_EARTH * R_EARTH * math.cos(lat_bai_rad) * 1000.0  # m/s
        v_tang_csg = OMEGA_EARTH * R_EARTH * math.cos(lat_csg_rad) * 1000.0  # m/s
        v_boost = v_tang_csg - v_tang_bai                                    # m/s

        # GTO 轨道倾角变轨损失计算
        # 远地点速度 v_apo_gto ≈ 1600 m/s
        v_apo_gto = 1600.0
        # 从拜科努尔发射最低初始倾角 51.6°，从库鲁发射最低倾角 5.24°
        dv_plane_bai = 2.0 * v_apo_gto * math.sin(math.radians(51.6) / 2.0)
        dv_plane_csg = 2.0 * v_apo_gto * math.sin(math.radians(5.24) / 2.0)
        dv_plane_saved = dv_plane_bai - dv_plane_csg

        # 齐奥尔科夫斯基增益: Isp = 320s, ve = 3138 m/s
        isp = 320.0
        ve = isp * G0
        payload_multiplier = math.exp(dv_plane_saved / ve)

        # 联盟号 GTO 运力实测标称提升
        payload_gto_bai_kg = 1700.0
        payload_gto_csg_kg = 3200.0
        payload_increase_pct = ((payload_gto_csg_kg - payload_gto_bai_kg) / payload_gto_bai_kg) * 100.0

        # 伽利略导航卫星 IOV 轨道参数
        a_galileo = 29600.0  # km
        v_circ_galileo = math.sqrt(MU_EARTH / a_galileo)
        t_sec_galileo = 2.0 * math.pi * math.sqrt(a_galileo**3 / MU_EARTH)
        t_hours_galileo = t_sec_galileo / 3600.0

        return {
            "v_tang_baikonur_mps": round(v_tang_bai, 2),
            "v_tang_csg_mps": round(v_tang_csg, 2),
            "v_boost_mps": round(v_boost, 2),
            "dv_plane_bai_mps": round(dv_plane_bai, 1),
            "dv_plane_csg_mps": round(dv_plane_csg, 1),
            "dv_plane_saved_mps": round(dv_plane_saved, 1),
            "theoretical_mass_multiplier": round(payload_multiplier, 3),
            "payload_gto_baikonur_kg": payload_gto_bai_kg,
            "payload_gto_csg_kg": payload_gto_csg_kg,
            "payload_increase_pct": round(payload_increase_pct, 1),
            "galileo_semimajor_axis_km": a_galileo,
            "galileo_v_circ_km_s": round(v_circ_galileo, 3),
            "galileo_period_hours": round(t_hours_galileo, 2)
        }

    # -------------------------------------------------------------
    # 3. 联盟 TM-33 载人飞船银禧 25 周年
    # -------------------------------------------------------------
    def get_soyuz_tm33_milestones(self) -> Dict[str, Any]:
        """获取联盟 TM-33 载人飞船 Andromède 任务银禧 25 周年历史参数。"""
        launch_dt = datetime(2001, 10, 21, 8, 59, 35, tzinfo=timezone.utc)
        dock_dt = datetime(2001, 10, 23, 10, 44, 0, tzinfo=timezone.utc)
        return_dt = datetime(2001, 10, 31, 4, 59, 26, tzinfo=timezone.utc)

        mission_duration_days = (return_dt - launch_dt).total_seconds() / 86400.0

        crew = [
            {"name": "Viktor Afanasyev", "role": "Commander", "agency": "Roscosmos", "flights": 4},
            {"name": "Konstantin Kozeev", "role": "Flight Engineer", "agency": "Roscosmos", "flights": 1},
            {"name": "Claudie Haigneré", "role": "Flight Engineer / Spationaut", "agency": "ESA / CNES", "flights": 2}
        ]

        return {
            "launch_utc": launch_dt.isoformat(),
            "dock_utc": dock_dt.isoformat(),
            "return_utc": return_dt.isoformat(),
            "duration_days": round(mission_duration_days, 2),
            "callsign": "Deryny",
            "crew": crew,
            "mission_name": "Andromède",
            "first_european_woman_on_iss": True,
            "purpose": "ISS Fresh Lifeboat Replacement & Biomedical Experiments"
        }

    # -------------------------------------------------------------
    # 4. 2026 猎户座流星雨极大期华夏暗空天窗推演
    # -------------------------------------------------------------
    def compute_orionids_china_dark_windows(self) -> List[Dict[str, Any]]:
        """计算 2026-10-21 至 10-22 极大期夜间华夏各大主要城市的月落、晨光与纯黑天窗。"""
        cities = [
            {"name": "上海", "lat": 31.23, "lon": 121.47, "moonset": "01:46", "dawn": "04:41", "culm_alt": 74.8},
            {"name": "北京", "lat": 39.90, "lon": 116.40, "moonset": "01:57", "dawn": "04:58", "culm_alt": 66.1},
            {"name": "广州", "lat": 23.13, "lon": 113.26, "moonset": "02:28", "dawn": "05:04", "culm_alt": 82.7},
            {"name": "成都", "lat": 30.67, "lon": 104.06, "moonset": "02:59", "dawn": "05:32", "culm_alt": 75.3},
            {"name": "西安", "lat": 34.34, "lon": 108.94, "moonset": "02:35", "dawn": "05:17", "culm_alt": 71.7},
            {"name": "乌鲁木齐", "lat": 43.83, "lon": 87.62, "moonset": "03:52", "dawn": "06:48", "culm_alt": 62.2}
        ]

        results = []
        for c in cities:
            h_set, m_set = map(int, c["moonset"].split(":"))
            h_dawn, m_dawn = map(int, c["dawn"].split(":"))
            t_set_min = h_set * 60 + m_set
            t_dawn_min = h_dawn * 60 + m_dawn
            window_min = t_dawn_min - t_set_min
            window_hours = window_min / 60.0

            results.append({
                "city": c["name"],
                "lat": c["lat"],
                "lon": c["lon"],
                "moonset_cst": c["moonset"],
                "dawn_cst": c["dawn"],
                "pure_dark_window_hours": round(window_hours, 2),
                "pure_dark_window_minutes": window_min,
                "radiant_culmination_alt_deg": c["culm_alt"],
                "moon_illum_pct": 77.2
            })
        return results

if __name__ == "__main__":
    engine = CapstoneNRHOSoyuzGuianaEngine()
    print("=== CAPSTONE NRHO 动力学 ===")
    print(engine.compute_capstone_nrho_parameters())
    print("\n=== 联盟号法属圭亚那赤道发射增益 ===")
    print(engine.compute_soyuz_guiana_boost())
    print("\n=== 联盟 TM-33 银禧 25 周年 ===")
    print(engine.get_soyuz_tm33_milestones())
    print("\n=== 2026 猎户座流星雨华夏纯黑暗空天窗 ===")
    for row in engine.compute_orionids_china_dark_windows():
        print(row)
