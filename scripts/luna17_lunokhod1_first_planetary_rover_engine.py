"""
月球17号 (Luna 17) 发射 56 周年暨人类首辆地外巡视器月球车1号 (Lunokhod 1) 雨海着陆、
8轮独立电力驱动越野动力学、钋-210 (Po-210) 放射性同位素热控衰变、
及法国 CNES 激光角反射器 (Corner-cube Retroreflector) 毫米级地月中继测距天体物理引擎
"""

import math
import datetime

# 基础物理常数
SPEED_OF_LIGHT = 299792458.0           # m/s
G_CONSTANT = 6.67430e-11                # m^3 / (kg * s^2)
STANDARD_GRAVITY = 9.80665              # m/s^2 (地球标准重力加速度 g0)
G_MOON = 1.622                          # m/s^2 (月球表面重力加速度)
R_MOON = 1737400.0                      # m (月球平均赤道半径 1737.4 km)
M_MOON = 7.342e22                       # kg (月球质量)
MU_MOON = 4.9028e12                     # m^3 / s^2 (GM_moon)
AU_METERS = 149597870700.0              # 1 AU in meters


class Luna17Lunokhod1Engine:
    """
    月球 17 号与月球车 1 号 56 周年巡天天体动力学与机理推演引擎
    """

    def __init__(self, current_dt=None):
        if current_dt is None:
            # 默认基准时间：2026-11-10 22:30:00 CST (14:30:00 UTC)
            self.current_dt = datetime.datetime(2026, 11, 10, 14, 30, tzinfo=datetime.timezone.utc)
        else:
            self.current_dt = current_dt

        # 核心任务历史节点
        self.launch_dt = datetime.datetime(1970, 11, 10, 14, 44, 1, tzinfo=datetime.timezone.utc)
        self.loi_dt = datetime.datetime(1970, 11, 15, 22, 0, 0, tzinfo=datetime.timezone.utc)
        self.landing_dt = datetime.datetime(1970, 11, 17, 3, 47, 0, tzinfo=datetime.timezone.utc)
        self.mission_end_dt = datetime.datetime(1971, 10, 4, 13, 5, 0, tzinfo=datetime.timezone.utc)

        # 质子-K (Proton-K 8K82K / Blok D) 运载火箭参数
        self.proton_liftoff_mass_kg = 705000.0       # kg (705 吨级)
        self.rd253_thrust_sea_n = 1.47e6             # N (单台 RD-253 海平面推力 1.47 MN)
        self.rd253_thrust_vac_n = 1.68e6             # N (单台 RD-253 真空推力 1.68 MN)
        self.first_stage_engine_count = 6            # 6 台 RD-253
        self.first_stage_total_thrust_vac_n = 10.08e6 # N (10.08 MN)
        self.earth_parking_perigee_km = 192.0        # km
        self.earth_parking_apogee_km = 237.0         # km
        self.earth_parking_inclination_deg = 51.5    # deg
        self.tli_delta_v_m_s = 3150.0                # m/s (地月转移注入速度增量)

        # 月球 17 号着陆器与月球车 1 号物理参数
        self.total_landing_mass_kg = 1814.0          # kg (着陆级 + 月球车着陆总质量)
        self.rover_mass_kg = 756.0                   # kg (月球车 1 号自身干重)
        self.descent_stage_dry_mass_kg = 1058.0      # kg
        self.landing_lat_deg = 38.32507              # °N (雨海 Mare Imbrium)
        self.landing_lon_deg = -35.00755             # °W (35.00755°W)
        self.landing_site_name = "Mare Imbrium (雨海盆地南部)"

        # 月球车 1 号机械构型与移动力学
        self.wheel_count = 8                         # 8 轮独立电驱动 (8WD)
        self.wheel_diameter_m = 0.510                # 510 mm
        self.wheel_width_m = 0.200                   # 200 mm
        self.wheel_contact_area_single_m2 = 0.020    # 钛合金网状轮接触面积 ~0.02 m^2
        self.total_contact_area_m2 = self.wheel_contact_area_single_m2 * self.wheel_count # 0.16 m^2
        self.speed_low_kmh = 1.0                     # 低速档 1 km/h (0.278 m/s)
        self.speed_high_kmh = 2.0                    # 高速档 2 km/h (0.556 m/s)
        self.max_climbing_slope_deg = 30.0           # 最大爬坡倾角 30°
        self.total_distance_traversed_m = 10540.0    # 实际总漫游里程 10.54 km
        self.total_operating_days_earth = 322.0      # 运行 322 地球日 (约 11 个月球昼夜)
        self.design_lifetime_days_earth = 90.0       # 原定寿命 3 个月 (~90 天)

        # 钋-210 (Po-210) 放射性同位素热源 (RHU)
        self.po210_half_life_days = 138.376          # Po-210 半衰期 (天)
        self.po210_initial_thermal_power_w = 1000.0  # 初始热功率 1000 W
        self.po210_decay_alpha_energy_mev = 5.304    # 单次 alpha 衰变释放能量 5.304 MeV

        # 法国 CNES 激光角反射器 (Corner-cube Retroreflector) 与测距
        self.retroreflector_prisms_count = 14        # 14 枚高纯度 Homosil 石英角反射棱镜
        self.laser_wavelength_nm = 532.0             # 常用倍频 Nd:YAG 测距波长 532 nm (绿色激光)
        self.retroreflector_optical_cross_section_m2 = 1.2e7 # 有效光学雷达截面积 ~1.2 x 10^7 m^2

    def compute_mission_anniversary(self):
        """
        计算发射与着陆周年里程碑
        """
        delta = self.current_dt - self.launch_dt
        years = delta.days / 365.2425
        exact_years = round(years, 2)
        full_years = self.current_dt.year - self.launch_dt.year
        if (self.current_dt.month, self.current_dt.day) < (self.launch_dt.month, self.launch_dt.day):
            full_years -= 1

        days_since_launch = delta.days
        landing_delta = self.current_dt - self.landing_dt
        days_since_landing = landing_delta.days

        return {
            "mission": "Luna 17 / Lunokhod 1 (月球17号 / 月球车1号)",
            "launch_utc": self.launch_dt.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "landing_utc": self.landing_dt.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "anniversary_full_years": full_years,
            "anniversary_exact_years": exact_years,
            "days_since_launch": days_since_launch,
            "days_since_landing": days_since_landing,
            "milestone_summary": f"月球17号发射 {full_years} 周年 · 人类首辆地外巡视器月球车1号漫游先驱"
        }

    def compute_locomotion_and_soil_mechanics(self):
        """
        计算月球车 1 号 8 轮越野行走力学与月壤承载压强
        """
        # 地球重量 vs 月球重量
        weight_earth_n = self.rover_mass_kg * STANDARD_GRAVITY
        weight_moon_n = self.rover_mass_kg * G_MOON

        # 月壤接地比压 (Ground Contact Pressure P = W_moon / A)
        ground_pressure_pa = weight_moon_n / self.total_contact_area_m2
        ground_pressure_kpa = ground_pressure_pa / 1000.0

        # 如果在地球上测试，接地比压为：
        ground_pressure_earth_kpa = (weight_earth_n / self.total_contact_area_m2) / 1000.0

        # 运行天数扩展倍率 (实际寿命 vs 设计寿命)
        lifetime_extension_ratio = self.total_operating_days_earth / self.design_lifetime_days_earth

        # 平均漫游推进效率 (米/地球日)
        avg_speed_m_per_day = self.total_distance_traversed_m / self.total_operating_days_earth

        # 30° 坡度重力分量与所需摩擦抓地力
        slope_rad = math.radians(self.max_climbing_slope_deg)
        f_parallel_gravity_n = weight_moon_n * math.sin(slope_rad)
        f_normal_gravity_n = weight_moon_n * math.cos(slope_rad)
        min_required_traction_mu = math.tan(slope_rad) # mu >= tan(30°) ~ 0.577

        return {
            "rover_mass_kg": self.rover_mass_kg,
            "weight_earth_n": round(weight_earth_n, 2),
            "weight_moon_n": round(weight_moon_n, 2),
            "weight_reduction_ratio": round(weight_moon_n / weight_earth_n, 4),
            "ground_pressure_kpa": round(ground_pressure_kpa, 2),
            "ground_pressure_earth_kpa": round(ground_pressure_earth_kpa, 2),
            "total_distance_traversed_km": round(self.total_distance_traversed_m / 1000.0, 3),
            "operating_days_earth": self.total_operating_days_earth,
            "design_lifetime_days_earth": self.design_lifetime_days_earth,
            "lifetime_extension_ratio": round(lifetime_extension_ratio, 2),
            "avg_speed_m_per_day": round(avg_speed_m_per_day, 1),
            "max_slope_deg": self.max_climbing_slope_deg,
            "min_required_friction_mu": round(min_required_traction_mu, 3),
            "f_parallel_gravity_n": round(f_parallel_gravity_n, 1),
            "f_normal_gravity_n": round(f_normal_gravity_n, 1)
        }

    def compute_po210_rhu_thermal_decay(self, elapsed_days=None):
        """
        计算钋-210 放射性同位素热源指数衰变历程
        """
        if elapsed_days is None:
            elapsed_days = self.total_operating_days_earth # 322 天任务结束时

        # 指数衰变定律: Q(t) = Q0 * 2^(-t / T_half) = Q0 * exp(-lambda * t)
        decay_constant_per_day = math.log(2.0) / self.po210_half_life_days
        power_at_end_w = self.po210_initial_thermal_power_w * math.exp(-decay_constant_per_day * elapsed_days)
        fraction_remaining = power_at_end_w / self.po210_initial_thermal_power_w

        # 计算任务运行中几个典型时间节点的热功率
        checkpoints_days = [0, 90, 138.376, 200, 322]
        powers_timeline = {}
        for d in checkpoints_days:
            p = self.po210_initial_thermal_power_w * math.exp(-decay_constant_per_day * d)
            powers_timeline[f"day_{int(d)}"] = round(p, 1)

        return {
            "isotope": "Polonium-210 (^210Po)",
            "half_life_days": self.po210_half_life_days,
            "decay_energy_mev": self.po210_decay_alpha_energy_mev,
            "initial_thermal_power_w": self.po210_initial_thermal_power_w,
            "elapsed_days": elapsed_days,
            "final_thermal_power_w": round(power_at_end_w, 2),
            "fraction_remaining": round(fraction_remaining, 4),
            "powers_timeline": powers_timeline,
            "freezeout_threshold_w": 200.0,
            "is_frozen_out": power_at_end_w < 205.0
        }

    def compute_laser_ranging_link_budget(self, moon_distance_km=384400.0):
        """
        计算激光角反射器往返光时与雷达测距链路几何
        """
        d_meters = moon_distance_km * 1000.0

        # 双程光时往返时延 (Round-trip time delay)
        round_trip_delay_s = (2.0 * d_meters) / SPEED_OF_LIGHT

        # 激光单程传播时间
        one_way_time_s = d_meters / SPEED_OF_LIGHT

        # 测距精度与计时分辨率 (如果计时精度为 10 皮秒 10 ps):
        timing_jitter_ps = 10.0 # 10 ps
        range_resolution_mm = (SPEED_OF_LIGHT * (timing_jitter_ps * 1e-12) / 2.0) * 1000.0

        # 地月潮汐减速退行速率：约 3.8 cm/year
        annual_recession_cm = 3.8

        return {
            "target": "Lunokhod 1 French CNES Corner-cube Retroreflector (14 prisms)",
            "lunar_coordinates": {
                "latitude_deg": self.landing_lat_deg,
                "longitude_deg": self.landing_lon_deg,
                "region": self.landing_site_name
            },
            "moon_distance_km": moon_distance_km,
            "round_trip_delay_s": round(round_trip_delay_s, 6),
            "one_way_time_s": round(one_way_time_s, 6),
            "range_resolution_mm": round(range_resolution_mm, 3),
            "annual_recession_cm_per_year": annual_recession_cm,
            "apollo_telescope_recontact_year": 2010,
            "scientific_value": "强等效原理 (SEP) 验证、引力常数 G 变化率约束 (dG/dt / G < 1e-12 / yr)"
        }

    def compute_comprehensive_summary(self, moon_distance_km=384400.0):
        """
        汇总月球 17 号与月球车 1 号全套动力学、热控与测距科学数据
        """
        anniv = self.compute_mission_anniversary()
        locomotion = self.compute_locomotion_and_soil_mechanics()
        thermal = self.compute_po210_rhu_thermal_decay()
        llr = self.compute_laser_ranging_link_budget(moon_distance_km)

        return {
            "mission": "Luna 17 / Lunokhod 1",
            "anniversary": anniv,
            "locomotion": locomotion,
            "thermal": thermal,
            "laser_ranging": llr
        }
