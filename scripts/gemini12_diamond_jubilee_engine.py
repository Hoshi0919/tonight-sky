"""
双子座12号 (Gemini 12) 发射 60 周年甲子钻禧纪念 (1966-11-11 至 2026-11-11)
天体动力学、雷达失效视线手控交会对接、水下中性浮力训练与出舱力学突破、
30米系绳重力梯度稳定及双子座计划大结局解算引擎
"""

import math
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List

class Gemini12DiamondJubileeEngine:
    """
    双子座 12 号 60 周年钻禧天体力学与航天先驱机理推演引擎
    """

    # 基础天体物理与常数 (CODATA / IAU 标定)
    G_CONSTANT = 6.67430e-11                  # m^3 / (kg * s^2)
    MU_EARTH = 3.986004418e14                 # m^3 / s^2 (地球引力常数 GM)
    R_EARTH = 6378137.0                       # m (地球 WGS84 赤道半径)
    STANDARD_GRAVITY = 9.80665                # m/s^2 (g0)
    SPEED_OF_LIGHT = 299792458.0              # m/s

    def __init__(self, current_dt: datetime = None):
        if current_dt is None:
            # 默认基准时间：2026-11-11 20:46:33 UTC (整 60 周年时刻)
            self.current_dt = datetime(2026, 11, 11, 20, 46, 33, tzinfo=timezone.utc)
        else:
            self.current_dt = current_dt

        # 核心任务时间戳
        self.launch_utc = datetime(1966, 11, 11, 20, 46, 33, tzinfo=timezone.utc)
        self.agena_launch_utc = datetime(1966, 11, 11, 19, 7, 59, tzinfo=timezone.utc)
        self.docking_utc = datetime(1966, 11, 12, 1, 0, 0, tzinfo=timezone.utc) # MET 04:14
        self.eva1_start_utc = datetime(1966, 11, 12, 16, 15, 0, tzinfo=timezone.utc)
        self.eva2_start_utc = datetime(1966, 11, 13, 15, 34, 0, tzinfo=timezone.utc)
        self.eva3_start_utc = datetime(1966, 11, 14, 14, 52, 0, tzinfo=timezone.utc)
        self.splashdown_utc = datetime(1966, 11, 15, 19, 21, 4, tzinfo=timezone.utc)

        # 乘组与载荷
        self.command_pilot = "James A. Lovell Jr."
        self.pilot = "Edwin E. 'Buzz' Aldrin Jr."
        self.gemini_mass_kg = 3763.0             # kg (双子座12号在轨质量)
        self.agena_mass_kg = 3200.0              # kg (阿金纳目标飞行器 5001 质量)
        self.tether_length_m = 30.0              # m (达克龙 Dacron 聚酯系绳长度)

    def compute_launch_and_phasing_dynamics(self) -> Dict[str, Any]:
        """
        解算泰坦二号火箭入轨参数、阿金纳目标轨道与共椭圆相位追赶动力学
        """
        # 1. 双子座 12 号初始入轨 (160.8 km x 270.6 km)
        hp_gemini = 160.8e3
        ha_gemini = 270.6e3
        rp_gemini = self.R_EARTH + hp_gemini
        ra_gemini = self.R_EARTH + ha_gemini
        a_gemini = (rp_gemini + ra_gemini) / 2.0
        e_gemini = (ra_gemini - rp_gemini) / (ra_gemini + rp_gemini)
        t_gemini_s = 2.0 * math.pi * math.sqrt(a_gemini**3 / self.MU_EARTH)
        t_gemini_min = t_gemini_s / 60.0
        vp_gemini = math.sqrt(self.MU_EARTH * (2.0 / rp_gemini - 1.0 / a_gemini))
        va_gemini = math.sqrt(self.MU_EARTH * (2.0 / ra_gemini - 1.0 / a_gemini))

        # 2. 阿金纳目标飞行器 5001 (ATV-12) 标称圆轨道 (298.3 km x 302.2 km)
        hp_agena = 298.3e3
        ha_agena = 302.2e3
        rp_agena = self.R_EARTH + hp_agena
        ra_agena = self.R_EARTH + ha_agena
        a_agena = (rp_agena + ra_agena) / 2.0
        e_agena = (ra_agena - rp_agena) / (ra_agena + rp_agena)
        t_agena_s = 2.0 * math.pi * math.sqrt(a_agena**3 / self.MU_EARTH)
        t_agena_min = t_agena_s / 60.0
        v_agena_mean = math.sqrt(self.MU_EARTH / a_agena)

        # 3. 相位角追赶速率 (Differential Mean Motion)
        omega_gemini = 2.0 * math.pi / t_gemini_s      # rad/s
        omega_agena = 2.0 * math.pi / t_agena_s        # rad/s
        delta_omega_rad_s = omega_gemini - omega_agena # 双子座角速度优势
        delta_deg_per_min = math.degrees(delta_omega_rad_s) * 60.0
        delta_deg_per_orbit = math.degrees(delta_omega_rad_s) * t_gemini_s

        # 4. 霍曼共面追赶至共椭圆高度 (Co-elliptic orbit, 约 270 km 圆轨)
        # 抬高近地点至 270 km 所需 Delta_v
        r_coelliptic = ra_gemini
        v_circ_coelliptic = math.sqrt(self.MU_EARTH / r_coelliptic)
        delta_v_circ_apogee = abs(v_circ_coelliptic - va_gemini)

        return {
            "gemini_orbit": {
                "perigee_km": hp_gemini / 1e3,
                "apogee_km": ha_gemini / 1e3,
                "semi_major_axis_km": a_gemini / 1e3,
                "eccentricity": e_gemini,
                "period_minutes": t_gemini_min,
                "perigee_velocity_ms": vp_gemini,
                "apogee_velocity_ms": va_gemini,
            },
            "agena_target_orbit": {
                "perigee_km": hp_agena / 1e3,
                "apogee_km": ha_agena / 1e3,
                "semi_major_axis_km": a_agena / 1e3,
                "eccentricity": e_agena,
                "period_minutes": t_agena_min,
                "mean_orbital_speed_ms": v_agena_mean,
            },
            "phasing_kinematics": {
                "orbital_period_difference_sec": t_agena_s - t_gemini_s,
                "catchup_angular_rate_deg_min": delta_deg_per_min,
                "catchup_angular_rate_deg_orbit": delta_deg_per_orbit,
                "apogee_circularization_delta_v_ms": delta_v_circ_apogee,
            }
        }

    def compute_aldrin_manual_rendezvous_and_hcw(self) -> Dict[str, Any]:
        """
        解算雷达失效工况下 Buzz Aldrin 博士论文视线制导 (Line-of-Sight) 与
        希尔-克洛赫西-威尔特郡 (Hill-Clohessy-Wiltshire, HCW) 相对运动方程与六分仪手控对接
        """
        # 1. 雷达失效边界参量
        radar_failure_range_nm = 5.9                   # 海里
        radar_failure_range_km = radar_failure_range_nm * 1.852 # 10.927 km

        # 2. HCW 相对坐标系动力学参量
        # 目标阿金纳轨道高度 ~300 km
        r_orbit = self.R_EARTH + 300.0e3
        n_mean_motion = math.sqrt(self.MU_EARTH / (r_orbit**3)) # 约 0.001155 rad/s

        # 3. 终端变轨点火 (TPI, Terminal Phase Initiation)
        # 典型视线交会转移角 phi = 130 deg
        phi_tpi_deg = 130.0
        phi_tpi_rad = math.radians(phi_tpi_deg)

        # 沿视线方向 (Line of Sight, LOS) 标称点火速度增量 Delta_v_tpi:
        # 基于 HCW 转移脉冲，相对高度差 delta_h ~ 15 km (共椭圆高度差 8 海里 ~ 14.8 km)
        delta_h_coelliptic_km = 14.816
        # 经验解析 TPI 冲量公式: Delta_V_TPI ~= 0.56 * n * delta_h / sin(phi/2)
        v_tpi_nominal_ms = 0.56 * n_mean_motion * (delta_h_coelliptic_km * 1e3) / math.sin(phi_tpi_rad / 2.0)

        # 4. 六分仪星空夹角测距与手算相对角速率
        # 视线角速率 d(sigma)/dt 控制裕度: 漂移率需通过 OAMS 姿态脉冲维持在 0.1 deg/min 之内
        max_los_drift_rate_deg_min = 0.10

        return {
            "aldrin_academic_background": {
                "institution": "MIT (Massachusetts Institute of Technology)",
                "degree": "Doctor of Science (Sc.D.) in Astronautics (1963)",
                "dissertation_title": "Line-of-Sight Guidance Techniques for Manned Orbital Rendezvous",
                "nickname": "Dr. Rendezvous",
            },
            "radar_failure_event": {
                "subsystem": "Westinghouse Rendezvous Radar",
                "failure_mode": "Transmitter power decay / intermittent lock",
                "failure_range_km": radar_failure_range_km,
                "failure_range_nm": radar_failure_range_nm,
            },
            "manual_navigation_methodology": {
                "optical_sensor": "Manual Space Sextant (六分仪视距测量)",
                "computational_tool": "Handheld Circular Slide Rule & Pre-computed Nomograms (手持计算尺与列线图)",
                "orbital_equations": "Hill-Clohessy-Wiltshire (HCW) Relative Motion Dynamics",
                "mean_orbital_motion_rad_s": n_mean_motion,
                "tpi_transfer_angle_deg": phi_tpi_deg,
                "tpi_nominal_delta_v_ms": round(v_tpi_nominal_ms, 2),
                "max_los_drift_threshold_deg_min": max_los_drift_rate_deg_min,
                "docking_met": "04:14 (Orbit 3)",
                "docking_result": "100% Successful Hard Docking with Agena 5001",
            }
        }

    def compute_aldrin_eva_biomechanics_and_neutral_buoyancy(self) -> Dict[str, Any]:
        """
        解算 Buzz Aldrin 三次出舱活动 (EVA)、水下中性浮力训练机理、
        约束支架力学 (“金色拖鞋”与腰部系绳) 及生理代谢对比
        """
        # 1. 三次出舱持续时间明细 (分钟)
        eva1_standup_min = 149.0   # 2小时29分 (SEVA-1: 44张紫外天文照片)
        eva2_umbilical_min = 126.0 # 2小时06分 (UEVA-2: 阿金纳工作台17项工作负载与30米系绳系紧)
        eva3_standup_min = 55.0    # 55分 (SEVA-3: 紫外摄影与废弃物抛弃)
        total_eva_min = eva1_standup_min + eva2_umbilical_min + eva3_standup_min
        total_eva_hours = total_eva_min / 60.0

        # 2. 约束支架与反作用力矩平衡力学
        # 在失重微重力下，无下肢锚定时人体对目标施加力矩 tau 会导致身体逆向自旋:
        # 扭力扳手拧紧螺栓 (25 N*m) 时，若无脚部锁定，人体躯干将产生角加速度 alpha = tau / I_body
        i_body_roll_pitch = 12.0 # kg*m^2 (宇航服与人体转动惯量)
        unrestrained_alpha_rad_s2 = 25.0 / i_body_roll_pitch # ~2.08 rad/s^2 剧烈自旋失控
        # “金色拖鞋” (Golden Slippers) 刚性脚部约束槽承受该 25 N*m 反扭矩，角加速度降为 0

        # 3. 生理代谢与体温对比 (Gemini 12 Aldrin vs Gemini 9A Cernan)
        cernan_g9a_heart_rate_max_bpm = 180.0
        cernan_g9a_metabolic_rate_btu_hr = 3200.0 # ~938 W (极端过热竭力、头盔面罩100%结雾失明)
        aldrin_g12_heart_rate_mean_bpm = 115.0
        aldrin_g12_heart_rate_max_bpm = 135.0
        aldrin_g12_metabolic_rate_btu_hr = 1050.0 # ~308 W (平稳可控、面罩结雾率 0%)

        return {
            "eva_breakdown": {
                "eva1_standup_minutes": eva1_standup_min,
                "eva2_umbilical_minutes": eva2_umbilical_min,
                "eva3_standup_minutes": eva3_standup_min,
                "total_eva_minutes": total_eva_min,
                "total_eva_hours": total_eva_hours,
            },
            "training_innovation": {
                "facility": "School of Aviation Medicine / Environmental Research Associates (ERA) Pool",
                "training_concept": "Neutral Buoyancy Water Immersion Simulation (水下中性浮力模拟失重)",
                "first_astronaut_trained": "Buzz Aldrin (人类首位系统性水下浮力训练宇航员)",
                "foot_restraints": "Golden Slippers (便携式双足固定锁定槽)",
                "handholds_count": 9,
                "waist_tethers": True,
            },
            "biomechanical_dynamics": {
                "torque_wrench_load_nm": 25.0,
                "unrestrained_angular_acceleration_rad_s2": round(unrestrained_alpha_rad_s2, 2),
                "restrained_angular_acceleration_rad_s2": 0.0,
            },
            "physiological_comparison": {
                "gemini_9a_cernan": {
                    "heart_rate_max_bpm": cernan_g9a_heart_rate_max_bpm,
                    "metabolic_rate_watts": round(cernan_g9a_metabolic_rate_btu_hr * 0.293071, 1),
                    "visor_fogging_percent": 100.0,
                    "task_abort": True,
                },
                "gemini_12_aldrin": {
                    "heart_rate_mean_bpm": aldrin_g12_heart_rate_mean_bpm,
                    "heart_rate_max_bpm": aldrin_g12_heart_rate_max_bpm,
                    "metabolic_rate_watts": round(aldrin_g12_metabolic_rate_btu_hr * 0.293071, 1),
                    "visor_fogging_percent": 0.0,
                    "task_abort": False,
                }
            }
        }

    def compute_gravity_gradient_tether_dynamics(self) -> Dict[str, Any]:
        """
        解算 30 米达克龙系绳重力梯度无工质姿态稳定动力学 (Tether Gravity-Gradient Dynamics)
        """
        m1 = self.gemini_mass_kg     # 3763 kg
        m2 = self.agena_mass_kg      # 3200 kg
        l_tether = self.tether_length_m # 30 m

        # 约化质量 mu_sys
        mu_reduced_kg = (m1 * m2) / (m1 + m2) # ~1728.7 kg

        # 在 300 km 近圆轨道上
        r_orbit = self.R_EARTH + 300.0e3
        omega_0 = math.sqrt(self.MU_EARTH / (r_orbit**3)) # ~0.001155 rad/s

        # 重力梯度张力 (沿地心矢径垂直对齐时理论稳态张力):
        # T_grav = 3 * omega_0^2 * mu_reduced * L
        tension_newtons = 3.0 * (omega_0**2) * mu_reduced_kg * l_tether

        # 面内天平动微幅振荡固有频率 (In-plane Pitch Libration Frequency):
        # omega_pitch = sqrt(3) * omega_0
        omega_pitch = math.sqrt(3.0) * omega_0
        period_pitch_s = 2.0 * math.pi / omega_pitch
        period_pitch_min = period_pitch_s / 60.0

        # 系绳保持稳定时间
        tether_stabilization_hours = 4.7667 # 4小时46分 (286分钟, 跨越第33至36轨道圈次)
        propellant_expended_kg = 0.0        # 无动力无工质全被动稳定

        return {
            "system_mass_kg": {
                "gemini12_kg": m1,
                "agena_target_kg": m2,
                "reduced_mass_kg": round(mu_reduced_kg, 1),
            },
            "tether_parameters": {
                "material": "Dacron (聚酯高强编织带)",
                "length_m": l_tether,
            },
            "gravity_gradient_physics": {
                "orbital_radius_km": r_orbit / 1e3,
                "orbital_angular_velocity_rad_s": omega_0,
                "theoretical_tension_newtons": round(tension_newtons, 4),
                "pitch_libration_frequency_rad_s": omega_pitch,
                "pitch_libration_period_minutes": round(period_pitch_min, 1),
                "passive_stabilization_duration_minutes": 286.0,
                "passive_stabilization_duration_hours": round(tether_stabilization_hours, 2),
                "propellant_consumed_kg": propellant_expended_kg,
            }
        }

    def compute_program_gemini_milestone_and_jubilee(self) -> Dict[str, Any]:
        """
        解算双子座计划大结局历史成就与 60 周年甲子钻禧时间轴精准对齐
        """
        # 任务总持续时间
        duration = self.splashdown_utc - self.launch_utc
        duration_hours = duration.total_seconds() / 3600.0
        duration_days = duration.total_seconds() / 86400.0

        # 钻禧时间差计算
        time_elapsed = self.current_dt - self.launch_utc
        years_elapsed = time_elapsed.total_seconds() / (365.25 * 86400.0)
        days_elapsed = time_elapsed.days

        return {
            "program_milestone": {
                "program_name": "Project Gemini (双子座载人航天计划)",
                "mission_number": "Gemini XII (双子座12号，第10次亦即最后一次载人任务)",
                "total_orbits": 59,
                "mission_duration_hours": round(duration_hours, 2),
                "mission_duration_text": "3 days, 22 hours, 34 minutes, 31 seconds",
                "recovery_ship": "USS Wasp (CVS-18)",
                "distance_from_target_km": 4.8,
            },
            "gemini_program_grand_totals": {
                "total_crewed_flights": 10,
                "total_astronaut_flight_hours": 1938.8,
                "total_dockings_achieved": 7,
                "total_evas_conducted": 16,
                "path_to_apollo_unlocked": [
                    "Spacecraft Rendezvous & Docking (空间交会对接)",
                    "Long-duration Manned Flight (8天与14天超长耐力测试)",
                    "Controlled Lifting Atmospheric Reentry (受控升力半弹道升力再入)",
                    "Practical Non-exhausting Extravehicular Activity (实用无衰竭出舱活动)",
                ]
            },
            "diamond_jubilee": {
                "anniversary_years": 60,
                "jubilee_name": "Diamond Jubilee (六十甲子钻禧)",
                "launch_date_utc": "1966-11-11 20:46:33 UTC",
                "exact_60yr_date_utc": "2026-11-11 20:46:33 UTC",
                "days_since_launch": days_elapsed,
                "years_since_launch": round(years_elapsed, 4),
            }
        }

    def generate_summary_report(self) -> str:
        """
        生成完整的双子座12号 60 周年甲子钻禧综合学术与工程推演报告
        """
        launch = self.compute_launch_and_phasing_dynamics()
        rendezvous = self.compute_aldrin_manual_rendezvous_and_hcw()
        eva = self.compute_aldrin_eva_biomechanics_and_neutral_buoyancy()
        tether = self.compute_gravity_gradient_tether_dynamics()
        jubilee = self.compute_program_gemini_milestone_and_jubilee()

        report = f"""# 双子座12号 (Gemini 12) 发射 60 周年甲子钻禧综合天体力学与航天先驱推演报告

**任务代号**：Project Gemini · Gemini XII (NASA Spacecraft No. 12)
**航天员**：指令长 James A. Lovell Jr. / 驾驶员 Edwin E. 'Buzz' Aldrin Jr.
**发射时刻**：1966 年 11 月 11 日 20:46:33 UTC (肯尼迪航天中心 LC-19)
**钻禧节点**：2026 年 11 月 11 日 20:46:33 UTC (整 60 周年，21,915 地球日)
**历史地位**：双子座载人航天计划壮丽大结局，阿波罗登月工程的奠基之桥。

---

## 1. 轨道交会动力学与雷达失效手控对接突破
- **发射与追赶轨道**：
  - 双子座 12 号入轨于 {launch['gemini_orbit']['perigee_km']} × {launch['gemini_orbit']['apogee_km']} km 椭圆轨道（周期 {launch['gemini_orbit']['period_minutes']:.2f} 分钟）；
  - 阿金纳目标飞行器 5001 位于 {launch['agena_target_orbit']['perigee_km']} × {launch['agena_target_orbit']['apogee_km']} km 近圆轨道（周期 {launch['agena_target_orbit']['period_minutes']:.2f} 分钟）；
  - 双子座角速度优势带来每圈次 {launch['phasing_kinematics']['catchup_angular_rate_deg_orbit']:.2f}° 的超强相位追赶速率。
- **雷达失效与“交会博士”现场奇迹**：
  - 飞船在距目标 {rendezvous['radar_failure_event']['failure_range_km']:.1f} km ({rendezvous['radar_failure_event']['failure_range_nm']} 海里) 处西屋机载雷达发生发射功率骤降与跟踪断锁故障；
  - 驾驶员 Buzz Aldrin 凭借其在麻省理工学院 (MIT) 的航空航天理学博士论文《载人轨道交会的视线制导技术》，使用手动六分仪测量视线角、手持圆形计算尺配合列线图进行手工解算；
  - 精准解算希尔-克洛赫西-威尔特郡 (HCW) 相对运动方程，计算出 TPI 点火速度增量 ({rendezvous['manual_navigation_methodology']['tpi_nominal_delta_v_ms']} m/s)；Lovell 点火，飞船于任务第 4 小时 14 分成功与阿金纳完成刚性对接！

---

## 2. 出舱力学革命：水下中性浮力训练与“金色拖鞋”约束系统
- **三次出舱总计 5 小时 30 分钟 (330 分钟)**：
  - 站立出舱 SEVA-1：149 分钟（拍摄 44 张天体紫外照片）；
  - 脐带式出舱 UEVA-2：126 分钟（在阿金纳工作台完成 17 项精细装配任务并连接系绳）；
  - 站立出舱 SEVA-3：55 分钟。
- **力矩平衡与中性浮力训练**：
  - 彻底终结了此前双子座 9A (Cernan) 因失重缺乏支点导致的极端竭力过热（心率 180 bpm、面罩 100% 结雾）；
  - Aldrin 率先引入水下中性浮力模拟训练，并在飞船表面铺设便携式双足固定槽（“金色拖鞋”）、9 处扶手与腰部系绳；
  - 在输出 25 N·m 扭矩时，角加速度由自由漂浮状态下的 {eva['biomechanical_dynamics']['unrestrained_angular_acceleration_rad_s2']} rad/s² 彻底降为零；
  - 出舱全程平均心率仅 {eva['physiological_comparison']['gemini_12_aldrin']['heart_rate_mean_bpm']} bpm，代谢率仅 {eva['physiological_comparison']['gemini_12_aldrin']['metabolic_rate_watts']} W，面罩结雾率 0%，彻底证明了人类在太空中具备长时间精细工作的能力。

---

## 3. 30 米达克龙系绳重力梯度无工质姿态稳定实验
- **系统物理构型**：
  - 双子座 12 号 (3,763 kg) 与阿金纳目标飞行器 (3,200 kg) 之间连接 30 米 Dacron 聚酯系绳；
  - 系统约化质量 {tether['system_mass_kg']['reduced_mass_kg']} kg；
- **重力梯度力矩与微小张力**：
  - 沿地心矢径对齐后，地球重力梯度产生 {tether['gravity_gradient_physics']['theoretical_tension_newtons']} N 的微小持续拉紧张力；
  - 面内天平动振荡周期约为 {tether['gravity_gradient_physics']['pitch_libration_period_minutes']} 分钟；
  - 飞船在长达 {tether['gravity_gradient_physics']['passive_stabilization_duration_hours']} 小时内，未消耗任何姿控推进剂 ({tether['gravity_gradient_physics']['propellant_consumed_kg']} kg)，完全依靠自然物理场维持了双星刚体定向稳定！

---

## 4. 双子座计划大结局历史成就与 60 周年钻禧
- 双子座计划累计 10 次载人飞行，完成了人类走向深空月球的四大关键技术闭环：
  1. 空间轨道交会与刚性对接；
  2. 8 天至 14 天长程载人太空耐力验证；
  3. 受控半弹道升力大气层再入；
  4. 实用、低代谢消耗的宇航员舱外出舱作业。
- 1966 年 11 月 15 日飞船溅落大西洋，距离搜救航母 USS Wasp 仅 4.8 km，双子座计划完美落幕，为阿波罗 8 号绕月与阿波罗 11 号登月铺平了全部道路！
"""
        return report
