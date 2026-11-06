"""
火星全球勘测者号 (Mars Global Surveyor, MGS) 发射 30 周年珍珠禧 (Pearl Jubilee, 1996-2026)、
行星级大气制动气动力学、太阳同步两点钟极轨、MOLA 全球激光测高二分性、
古地壳剩余磁场与发电机熄灭、TES 赤铁矿与机遇号着陆点寻路推演引擎
"""

import math
import datetime

# 基础物理与天体常数
SPEED_OF_LIGHT = 299792458.0      # m/s
AU_METERS = 149597870700.0       # 1 AU in meters
STANDARD_GRAVITY = 9.80665       # g0, m/s^2

# 火星物理常数
GM_MARS = 4.282837e13            # m^3/s^2 (G * M_mars)
R_MARS = 3389.5e3                # m (火星平均体积半径, 3389.5 km)
MASS_MARS = 6.4171e23            # kg
MARS_SOL_SECONDS = 88775.244     # 1 火星日 (Sol) = 24h 39m 35.244s
MARS_YEAR_DAYS = 686.98          # 火星公转恒星年 (地球日)
MARS_J2 = 1.96045e-3             # 火星引力二阶纬向带谐系数 J2


class MarsGlobalSurveyorEngine:
    """
    火星全球勘测者号 (MGS) 发射 30 周年珍珠禧动力学与火星科学拓荒推演引擎
    """

    def __init__(self, current_dt=None):
        if current_dt is None:
            # 默认基准时间：2026-11-06 23:15:00 UTC (北京时间 11-07 07:15)
            self.current_dt = datetime.datetime(2026, 11, 6, 23, 15, tzinfo=datetime.timezone.utc)
        else:
            self.current_dt = current_dt

        # 核心任务时间节点
        self.launch_dt = datetime.datetime(1996, 11, 7, 17, 0, 50, tzinfo=datetime.timezone.utc)
        self.moi_dt = datetime.datetime(1997, 9, 12, 1, 17, 0, tzinfo=datetime.timezone.utc)
        self.mapping_start_dt = datetime.datetime(1999, 3, 9, 0, 0, 0, tzinfo=datetime.timezone.utc)
        self.loss_of_signal_dt = datetime.datetime(2006, 11, 2, 23, 0, 0, tzinfo=datetime.timezone.utc)
        self.pearl_jubilee_30y_dt = datetime.datetime(2026, 11, 7, 17, 0, 50, tzinfo=datetime.timezone.utc)

        # 航天器质量与推进参数
        self.m_wet = 1060.0              # kg 发射湿重 (Delta II 7925A 限额)
        self.m_dry = 677.0               # kg 干重 (结构+载荷)
        self.m_prop_initial = 383.0      # kg 初始推进剂质量 (MMH + N2O4)
        self.engine_isp = 317.0          # s 主发动机比冲 (双组元推进剂)

        # 捕获初轨与标称制图轨道参数
        self.r_peri_initial = R_MARS + 262.0e3    # 近火点半径 (高度 262 km)
        self.r_apo_initial = R_MARS + 54026.0e3   # 远火点半径 (高度 54,026 km)
        self.h_mapping = 378.0e3                  # 标称制图轨道平均高度 378 km
        self.r_mapping = R_MARS + self.h_mapping  # 3,767.5 km
        self.flown_inclination_deg = 92.86        # 实际飞行逆行极轨倾角 (度)

    def compute_mission_timeline(self):
        """
        计算任务时间线、服役跨度与 30 周年珍珠禧倒计时
        """
        flight_sec = (self.current_dt - self.launch_dt).total_seconds()
        countdown_sec = (self.pearl_jubilee_30y_dt - self.current_dt).total_seconds()
        active_lifetime_sec = (self.loss_of_signal_dt - self.launch_dt).total_seconds()

        total_flight_years = flight_sec / (86400.0 * 365.25)
        active_lifetime_days = active_lifetime_sec / 86400.0
        active_lifetime_years = active_lifetime_days / 365.25
        active_lifetime_mars_years = active_lifetime_days / MARS_YEAR_DAYS

        countdown_hours = countdown_sec / 3600.0
        countdown_days = countdown_sec / 86400.0

        return {
            "total_flight_years": total_flight_years,
            "active_lifetime_days": active_lifetime_days,
            "active_lifetime_years": active_lifetime_years,
            "active_lifetime_mars_years": active_lifetime_mars_years,
            "countdown_hours": countdown_hours,
            "countdown_days": countdown_days,
            "is_pearl_jubilee_near": 0.0 <= countdown_hours <= 48.0 or abs(countdown_hours) < 24.0,
        }

    def compute_aerobraking_energetics(self):
        """
        行星级大气制动气动力学与齐奥尔科夫斯基推进剂节省核算
        """
        # 捕获初轨半长轴与近火点切向速度
        a_init = (self.r_peri_initial + self.r_apo_initial) / 2.0
        v_peri_init = math.sqrt(GM_MARS * (2.0 / self.r_peri_initial - 1.0 / a_init))

        # 若纯靠化学推进将远火点拉降至 378 km:
        # 转移椭圆：近点为 r_peri_initial，远点为 r_mapping
        a_trans = (self.r_peri_initial + self.r_mapping) / 2.0
        v_peri_trans = math.sqrt(GM_MARS * (2.0 / self.r_peri_initial - 1.0 / a_trans))
        delta_v_peri_burn = abs(v_peri_init - v_peri_trans)

        # 在 378 km 处圆化轨道所需速度增量
        v_apo_trans = math.sqrt(GM_MARS * (2.0 / self.r_mapping - 1.0 / a_trans))
        v_circ_mapping = math.sqrt(GM_MARS / self.r_mapping)
        delta_v_circ_burn = abs(v_circ_mapping - v_apo_trans)

        total_delta_v_saved = delta_v_peri_burn + delta_v_circ_burn

        # 齐奥尔科夫斯基火箭方程推算节省的推进剂质量:
        # m_0 = m_dry * exp(Delta_V / (Isp * g0))
        # m_saved = m_0 - m_dry
        c_exhaust = self.engine_isp * STANDARD_GRAVITY
        mass_ratio = math.exp(total_delta_v_saved / c_exhaust)
        extra_propellant_needed = self.m_dry * (mass_ratio - 1.0)

        # 大气制动实施参数 (891 次掠空减速)
        aerobraking_passes = 891
        avg_dv_per_pass = total_delta_v_saved / aerobraking_passes

        return {
            "v_peri_initial_mps": v_peri_init,
            "v_circ_mapping_mps": v_circ_mapping,
            "total_delta_v_saved_mps": total_delta_v_saved,
            "extra_propellant_needed_kg": extra_propellant_needed,
            "mass_ratio": mass_ratio,
            "aerobraking_passes": aerobraking_passes,
            "avg_dv_per_pass_mps": avg_dv_per_pass,
            "delta_ii_mass_budget_saved": extra_propellant_needed > 300.0,
        }

    def compute_sun_synchronous_orbit_dynamics(self):
        """
        开普勒轨道动力学、火星 J2 引力摄动与太阳同步进动角速度闭合
        """
        r = self.r_mapping
        v_circ = math.sqrt(GM_MARS / r)
        period_s = 2.0 * math.pi * math.sqrt(r**3 / GM_MARS)
        period_min = period_s / 60.0

        orbits_per_earth_day = 86400.0 / period_s
        orbits_per_sol = MARS_SOL_SECONDS / period_s

        # 火星绕日平均公转角速度 (太阳同步所需节点进动率)
        mars_mean_motion_rad_s = (2.0 * math.pi) / (MARS_YEAR_DAYS * 86400.0)
        mars_mean_motion_deg_day = math.degrees(mars_mean_motion_rad_s) * 86400.0

        # 一阶 J2 引起的升交点赤经进动公式:
        # dOmega/dt = -1.5 * J2 * (R_mars / r)^2 * n * cos(i)
        n_orbit = math.sqrt(GM_MARS / r**3)
        factor = -1.5 * MARS_J2 * ((R_MARS / r)**2) * n_orbit
        cos_i_theoretical = mars_mean_motion_rad_s / factor
        theoretical_inclination_deg = math.degrees(math.acos(cos_i_theoretical))

        # 实际飞行轨道进动率
        actual_precession_rad_s = factor * math.cos(math.radians(self.flown_inclination_deg))
        actual_precession_deg_day = math.degrees(actual_precession_rad_s) * 86400.0
        inclination_error_deg = abs(theoretical_inclination_deg - self.flown_inclination_deg)

        return {
            "orbital_radius_km": r / 1000.0,
            "circular_velocity_mps": v_circ,
            "orbital_period_seconds": period_s,
            "orbital_period_minutes": period_min,
            "orbits_per_earth_day": orbits_per_earth_day,
            "orbits_per_sol": orbits_per_sol,
            "desired_precession_deg_day": mars_mean_motion_deg_day,
            "theoretical_inclination_deg": theoretical_inclination_deg,
            "actual_flown_inclination_deg": self.flown_inclination_deg,
            "inclination_error_deg": inclination_error_deg,
            "is_sun_synchronous_closed": inclination_error_deg < 0.1,
            "repeat_ground_track_sols": 7,
            "repeat_ground_track_orbits": 88,
        }

    def compute_mola_topography_dichotomy(self):
        """
        MOLA (火星激光测高仪) 全球高程基准、南北二分性与极端地貌落差
        """
        # MOLA 核心观测数据与物理参数
        laser_wavelength_nm = 1064.0       # Nd:YAG 近红外
        laser_repetition_rate_hz = 10.0    # 10 Hz
        laser_pulse_energy_mj = 40.0       # 40 mJ
        total_shots_fired_millions = 671.0 # > 6.71 亿次真实测高点

        # 全球拓扑二分性 (Topographic Dichotomy)
        northern_lowlands_avg_elevation_km = -4.5   # 北部低地 (平坦水蚀平原)
        southern_highlands_avg_elevation_km = +1.5  # 南部高地 (古老重度陨击坑)
        dichotomy_elevation_gap_km = southern_highlands_avg_elevation_km - northern_lowlands_avg_elevation_km

        # 太阳系极端高程极值
        hellas_basin_floor_km = -8.2       # 希腊平原最低点 (低于基准面 8.2 km)
        olympus_mons_caldera_km = +21.2    # 奥林匹斯火山之巅 (高于基准面 21.2 km)
        total_relief_dynamic_range_km = olympus_mons_caldera_km - hellas_basin_floor_km

        # 地球对比：珠峰 (+8.848 km) 到马里亚纳海沟 (-10.994 km) 极差 19.84 km
        earth_dynamic_range_km = 19.84
        relief_ratio_vs_earth = total_relief_dynamic_range_km / earth_dynamic_range_km

        return {
            "total_shots_fired_millions": total_shots_fired_millions,
            "laser_wavelength_nm": laser_wavelength_nm,
            "dichotomy_elevation_gap_km": dichotomy_elevation_gap_km,
            "hellas_basin_floor_km": hellas_basin_floor_km,
            "olympus_mons_caldera_km": olympus_mons_caldera_km,
            "total_relief_dynamic_range_km": total_relief_dynamic_range_km,
            "relief_ratio_vs_earth": relief_ratio_vs_earth,
            "martian_relief_exceeds_earth": total_relief_dynamic_range_km > earth_dynamic_range_km,
        }

    def compute_crustal_magnetism_and_dynamo_extinction(self):
        """
        MAG/ER 磁强计地壳剩余磁带与火星核心古发电机熄灭机制
        """
        # 现代火星整体偶极磁场与地壳局域强磁异常
        modern_global_dipole_field_nt = 5.0    # 几乎为零 (< 5 nT)
        earth_dipole_field_nt = 50000.0        # 地球偶极场 ~50,000 nT
        max_crustal_magnetic_anomaly_nt = 1500.0 # 南部塞壬高地 (Terra Sirenum) 100km 高度实测

        # 古发电机熄灭与大型撞击盆地年代学约束
        dynamo_shutdown_ga = 4.10              # 约 41 亿年前发电机停滞
        hellas_impact_age_ga = 3.90            # 希腊撞击盆地形成于 39 亿年前
        argyre_impact_age_ga = 3.85            # 阿尔及尔盆地形成于 38.5 亿年前

        # 磁异常条带宽度与地壳增生模式
        stripe_width_km = 120.0                # 正负交替磁条带典型半宽

        return {
            "modern_dipole_field_nt": modern_global_dipole_field_nt,
            "max_crustal_anomaly_nt": max_crustal_magnetic_anomaly_nt,
            "dynamo_shutdown_ga": dynamo_shutdown_ga,
            "hellas_impact_age_ga": hellas_impact_age_ga,
            "is_hellas_demagnetized": hellas_impact_age_ga < dynamo_shutdown_ga,
            "stripe_width_km": stripe_width_km,
            "crustal_remnant_proves_ancient_plate_or_convection": True,
        }

    def compute_tes_opportunity_heritage(self):
        """
        TES 热辐射光谱仪发现子午线高原晶体赤铁矿与机遇号火星车选址实证
        """
        # TES 发现粗晶灰色赤铁矿 (Coarse-grained gray crystalline hematite, alpha-Fe2O3)
        spectral_band_wavenumber_cm_inv = (200.0, 500.0)
        target_region = "Sinus Meridiani / Meridiani Planum"
        mineral_formula = "alpha-Fe2O3"
        aqueous_origin = "Hydrothermal precipitation or standing open water evaporation"

        # 机遇号 (Opportunity, MER-B) 验证
        landing_date = "2004-01-25"
        discovered_blueberry_composition = "Hematite spherules (blueberries)"
        discovered_jarosite = True # 黄钾铁矾证明强酸性水体存在

        return {
            "target_region": target_region,
            "mineral_formula": mineral_formula,
            "spectral_band": spectral_band_wavenumber_cm_inv,
            "aqueous_origin": aqueous_origin,
            "opportunity_landing_date": landing_date,
            "opportunity_verified_blueberries": discovered_blueberry_composition,
            "opportunity_verified_jarosite": discovered_jarosite,
            "mgs_to_opportunity_closed_loop": True,
        }
