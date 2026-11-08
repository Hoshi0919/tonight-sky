"""
阿波罗 4 号 (Apollo 4 / AS-501) 59 周年土星 5 号全状态试飞与第二宇宙速度再入、
卡尔·萨根 (Carl Sagan) 诞辰 92 周年暗淡蓝点几何与金星失控温室效应辐射传输、
及 2026-11-09 农历十月初一朔日纯黑暗空天象推演引擎
"""

import math
import datetime

# 基础物理与天体常数
SPEED_OF_LIGHT = 299792458.0           # m/s
AU_METERS = 149597870700.0            # 1 AU in meters (149,597,870.7 km)
SOLAR_CONSTANT_1AU = 1361.0           # W/m^2 (地球 1 AU 太阳辐射常数)
R_SUN_METERS = 696340000.0            # 太阳半径 R_sun (米)
R_EARTH_METERS = 6371000.0            # 地球平均半径 (米)
D_EARTH_KM = 12742.0                  # 地球直径 (km)
GM_SUN = 1.32712440018e20             # m^3/s^2 (G * M_sun)
GM_EARTH = 3.986004418e14             # m^3/s^2 (G * M_earth)
STEFAN_BOLTZMANN = 5.670374419e-8     # W/(m^2 K^4)
STANDARD_GRAVITY = 9.80665            # m/s^2 (g0)


class Apollo4CarlSaganEngine:
    """
    阿波罗 4 号 59 周年、卡尔·萨根 92 周年与 2026-11-09 朔日暗空天体物理推演引擎
    """

    def __init__(self, current_dt=None):
        if current_dt is None:
            # 默认基准时间：2026-11-09 22:30:00 CST (14:30:00 UTC)
            self.current_dt = datetime.datetime(2026, 11, 9, 14, 30, tzinfo=datetime.timezone.utc)
        else:
            self.current_dt = current_dt

        # 核心任务与历史节点
        self.apollo4_launch_dt = datetime.datetime(1967, 11, 9, 12, 0, 1, tzinfo=datetime.timezone.utc)
        self.apollo4_splashdown_dt = datetime.datetime(1967, 11, 9, 20, 37, 0, tzinfo=datetime.timezone.utc)
        self.carl_sagan_birth_dt = datetime.datetime(1934, 11, 9, 0, 0, 0, tzinfo=datetime.timezone.utc)
        self.carl_sagan_death_dt = datetime.datetime(1996, 12, 20, 0, 0, 0, tzinfo=datetime.timezone.utc)
        self.pale_blue_dot_photo_dt = datetime.datetime(1990, 2, 14, 4, 48, 0, tzinfo=datetime.timezone.utc)

        # 土星 5 号 (Saturn V / SA-501) 物理与动力学参数
        self.saturn_v_liftoff_mass_kg = 2824000.0   # kg (约 2,824 吨总起飞质量)
        self.saturn_v_height_m = 110.6              # m
        self.f1_engine_count = 5
        self.f1_thrust_single_sea_n = 6.77e6        # N (单台 6.77 MN)
        self.s_ic_total_thrust_sea_n = 33.85e6      # N (海平面 33.85 MN / 7.61M lbf)
        self.s_ic_burn_time_s = 150.8               # s
        self.s_ic_staging_altitude_km = 61.6        # km
        self.s_ic_staging_speed_kms = 2.75          # km/s (马赫 8.1)

        # 阿波罗 4 号轨道抬升与第二宇宙速度再入
        self.apollo4_apogee_km = 18079.0            # km (S-IVB 二重点火大椭圆轨远地点)
        self.apollo4_perigee_km = 185.0             # km
        self.apollo4_reentry_speed_kms = 11.14      # km/s (40,104 km/h，第二宇宙速度再入)
        self.apollo4_cm_mass_kg = 5425.0            # kg (指令舱质量)
        self.apollo4_heat_shield_temp_c = 2760.0    # °C (防热盾最高温度)
        self.apollo4_mission_duration_hours = 8.616 # 8 小时 37 分钟

        # 卡尔·萨根暗淡蓝点几何参数 (Voyager 1, 1990-02-14)
        self.pbd_distance_sun_au = 40.47            # AU
        self.pbd_distance_earth_au = 40.11          # AU (约 60 亿公里)
        self.voyager_nac_focal_length_m = 1.500     # 1500 mm
        self.voyager_nac_pixel_size_m = 15.24e-6    # 15.24 um
        self.voyager_nac_pixel_scale_arcsec = (self.voyager_nac_pixel_size_m / self.voyager_nac_focal_length_m) * (180.0 / math.pi) * 3600.0  # 2.096"

        # 金星温室效应物理参数
        self.venus_distance_au = 0.7233
        self.venus_bond_albedo = 0.77
        self.venus_surface_temp_k = 737.0           # 463.85 °C
        self.venus_surface_pressure_bar = 92.0      # 92 个标准大气压

    def compute_apollo4_launch_and_reentry(self):
        """
        计算阿波罗 4 号 59 周年、土星 5 号动力学参数与极端再入热动能
        """
        elapsed_sec = (self.current_dt - self.apollo4_launch_dt).total_seconds()
        total_years = elapsed_sec / (86400.0 * 365.25)
        total_days = elapsed_sec / 86400.0

        # 再入动能 Ek = 0.5 * m * v^2
        v_reentry_ms = self.apollo4_reentry_speed_kms * 1000.0
        reentry_ke_joules = 0.5 * self.apollo4_cm_mass_kg * (v_reentry_ms ** 2)
        reentry_ke_gj = reentry_ke_joules / 1e9

        # 起飞推重比 TWR = F / (m * g0)
        twr_liftoff = self.s_ic_total_thrust_sea_n / (self.saturn_v_liftoff_mass_kg * STANDARD_GRAVITY)

        # S-IVB 抬升后的大椭圆轨道能量与周期 (Kepler)
        r_earth_m = R_EARTH_METERS
        r_p_m = r_earth_m + self.apollo4_perigee_km * 1000.0
        r_a_m = r_earth_m + self.apollo4_apogee_km * 1000.0
        semi_major_m = (r_p_m + r_a_m) / 2.0
        eccentricity = (r_a_m - r_p_m) / (r_a_m + r_p_m)

        # 轨道周期 T = 2 * pi * sqrt(a^3 / mu)
        orbit_period_s = 2.0 * math.pi * math.sqrt(math.pow(semi_major_m, 3) / GM_EARTH)
        orbit_period_hours = orbit_period_s / 3600.0

        # 远地点速度与近地点速度 (Vis-viva)
        v_perigee_ms = math.sqrt(GM_EARTH * (2.0 / r_p_m - 1.0 / semi_major_m))
        v_apogee_ms = math.sqrt(GM_EARTH * (2.0 / r_a_m - 1.0 / semi_major_m))

        return {
            "elapsed_years": round(total_years, 2),
            "elapsed_days": round(total_days, 1),
            "liftoff_thrust_mn": round(self.s_ic_total_thrust_sea_n / 1e6, 2),
            "liftoff_thrust_pounds": round(self.s_ic_total_thrust_sea_n * 0.224809, 0),
            "liftoff_twr": round(twr_liftoff, 2),
            "apogee_km": self.apollo4_apogee_km,
            "perigee_km": self.apollo4_perigee_km,
            "orbit_eccentricity": round(eccentricity, 4),
            "orbit_period_hours": round(orbit_period_hours, 2),
            "v_perigee_kms": round(v_perigee_ms / 1000.0, 2),
            "v_apogee_kms": round(v_apogee_ms / 1000.0, 2),
            "reentry_speed_kms": self.apollo4_reentry_speed_kms,
            "reentry_speed_kmh": round(self.apollo4_reentry_speed_kms * 3600.0, 0),
            "reentry_kinetic_energy_gj": round(reentry_ke_gj, 2),
            "heat_shield_temp_celsius": self.apollo4_heat_shield_temp_c,
            "mission_duration_hours": self.apollo4_mission_duration_hours,
        }

    def compute_carl_sagan_pale_blue_dot_and_greenhouse(self):
        """
        计算卡尔·萨根诞辰 92 周年、“暗淡蓝点”成像几何与金星失控温室效应光学厚度
        """
        elapsed_sec = (self.current_dt - self.carl_sagan_birth_dt).total_seconds()
        birth_years = elapsed_sec / (86400.0 * 365.25)

        # 1. 暗淡蓝点成像几何
        dist_earth_km = self.pbd_distance_earth_au * (AU_METERS / 1000.0)
        dist_sun_km = self.pbd_distance_sun_au * (AU_METERS / 1000.0)
        light_travel_time_hours = (self.pbd_distance_earth_au * AU_METERS) / SPEED_OF_LIGHT / 3600.0

        # 地球视张角 (弧度 -> 角秒)
        ang_rad = (D_EARTH_KM * 1000.0) / (dist_earth_km * 1000.0)
        ang_arcsec = math.degrees(ang_rad) * 3600.0

        # 地球在旅行者 1 号相机感光芯片上占有的物理跨度 (像素比例)
        pixel_fraction = ang_arcsec / self.voyager_nac_pixel_scale_arcsec

        # 地球在 40.11 AU 处的视星等 (绝对星等 H = -3.99)
        # m = H + 5 * log10(r_sun * r_earth)
        mag_earth = -3.99 + 5.0 * math.log10(self.pbd_distance_sun_au * self.pbd_distance_earth_au)

        # 2. 金星失控温室效应辐射平衡
        # 太阳常数通量 S_v = S0 / r^2
        flux_venus_w_m2 = SOLAR_CONSTANT_1AU / math.pow(self.venus_distance_au, 2)
        # 吸收净通量 F_abs = S_v * (1 - albedo) / 4
        flux_abs_w_m2 = (flux_venus_w_m2 * (1.0 - self.venus_bond_albedo)) / 4.0
        # 裸星/黑体平衡温度 T_eq = (F_abs / sigma)^0.25
        t_eq_k = math.pow(flux_abs_w_m2 / STEFAN_BOLTZMANN, 0.25)
        t_eq_c = t_eq_k - 273.15

        # 萨根 Eddington 灰体两流逼近: T_surf^4 = T_eq^4 * (1 + 0.75 * tau)
        # tau = (4/3) * ((T_surf / T_eq)^4 - 1)
        tau_greenhouse = (4.0 / 3.0) * (math.pow(self.venus_surface_temp_k / t_eq_k, 4) - 1.0)
        temp_boost_c = self.venus_surface_temp_k - t_eq_k

        return {
            "sagan_birth_anniversary_years": round(birth_years, 2),
            "pbd_distance_billion_km": round(dist_earth_km / 1e9, 3),
            "pbd_light_hours": round(light_travel_time_hours, 2),
            "pbd_earth_angular_diam_arcsec": round(ang_arcsec, 4),
            "pbd_pixel_scale_arcsec": round(self.voyager_nac_pixel_scale_arcsec, 3),
            "pbd_earth_pixel_fraction": round(pixel_fraction, 3),
            "pbd_apparent_magnitude": round(mag_earth, 2),
            "venus_solar_flux_w_m2": round(flux_venus_w_m2, 1),
            "venus_equilibrium_temp_k": round(t_eq_k, 1),
            "venus_equilibrium_temp_celsius": round(t_eq_c, 1),
            "venus_actual_surface_temp_k": self.venus_surface_temp_k,
            "venus_actual_surface_temp_celsius": round(self.venus_surface_temp_k - 273.15, 1),
            "venus_greenhouse_temp_boost_c": round(temp_boost_c, 1),
            "venus_required_optical_depth_tau": round(tau_greenhouse, 1),
            "venus_surface_pressure_atm": self.venus_surface_pressure_bar,
        }

    def compute_night_darksky_status(self):
        """
        2026-11-09 农历十月初一朔日纯黑暗空天象与月球参数
        """
        # 精确新月时间：2026-11-09 07:02:03 UTC (15:02:03 CST)
        exact_new_moon_dt = datetime.datetime(2026, 11, 9, 7, 2, 3, tzinfo=datetime.timezone.utc)
        elapsed_from_new_moon_hours = (self.current_dt - exact_new_moon_dt).total_seconds() / 3600.0

        return {
            "lunar_phase_percent": 0.28,
            "moon_age_days": 0.31,
            "distance_km": 404704.0,
            "hours_since_exact_new_moon": round(elapsed_from_new_moon_hours, 2),
            "darksky_window_percent": 100.0,
            "night_sky_condition": "朔日极黑暗空天窗 (100% 零月光，月沉地平下 71°)",
        }


def format_summary_report():
    engine = Apollo4CarlSaganEngine()
    ap4 = engine.compute_apollo4_launch_and_reentry()
    cs = engine.compute_carl_sagan_pale_blue_dot_and_greenhouse()
    sky = engine.compute_night_darksky_status()

    return f"""
================================================================================
阿波罗 4 号 59 周年、卡尔·萨根诞辰 92 周年与 2026-11-09 朔日暗空天体力学推演报告
================================================================================
【一、阿波罗 4 号 (Apollo 4 / AS-501) 土星 5 号首飞 59 周年】
- 发射时刻：1967-11-09 12:00:01 UTC (LC-39A，今日整整 {ap4['elapsed_years']} 周年 / {ap4['elapsed_days']} 天)
- 起飞全重：2,824 吨（全高 110.6 米）
- 一级动力：5 台 F-1 发动机，总推力 {ap4['liftoff_thrust_mn']} MN（{int(ap4['liftoff_thrust_pounds']):,} lbf），起飞推重比 {ap4['liftoff_twr']}
- 空间二次点火：S-IVB 三级首次在轨重启，推入 {ap4['perigee_km']} × {ap4['apogee_km']} km 大椭圆轨道（偏心率 {ap4['orbit_eccentricity']}，周期 {ap4['orbit_period_hours']} 小时）
- 第二宇宙速度再入：SPS 发动机主动加速，指令舱以 {ap4['reentry_speed_kms']} km/s（时速 {int(ap4['reentry_speed_kmh']):,} km/h）高速砸入大气层
- 极端热动能释放：5,425 kg 指令舱携带 {ap4['reentry_kinetic_energy_gj']} GJ 动能，Avcoat 防热盾承受 {ap4['heat_shield_temp_celsius']} °C 极温考验
- 历史意义：首次“全状态”（All-up）发射圆满成功，为阿波罗 8 号绕月与 11 号登月铺平道路

【二、卡尔·萨根 (Carl Sagan) 诞辰 92 周年 (1934-11-09 ~ 1996-12-20)】
- 诞辰纪念：1934-11-09 诞生于纽约布鲁克林，今日整整 {cs['sagan_birth_anniversary_years']} 周年
- “暗淡蓝点” (Pale Blue Dot, 1990-02-14)：
  * 回望距离：{cs['pbd_distance_billion_km']} 亿公里 (40.11 AU)，光行时 {cs['pbd_light_hours']} 小时
  * 视张角：地球在 40 AU 外仅 {cs['pbd_earth_angular_diam_arcsec']}"（不足半个角秒）
  * 相机成像：旅行者 1 号窄角相机单像素为 {cs['pbd_pixel_scale_arcsec']}"，地球仅占 {cs['pbd_earth_pixel_fraction']} 像素！
  * 视星等：+{cs['pbd_apparent_magnitude']} 等（孤独悬浮在太阳散射光芒的光柱之中）
- 金星失控温室效应模型：
  * 太阳常数：{cs['venus_solar_flux_w_m2']} W/m² (硫酸云层反照率 0.77)
  * 无温室裸星平衡温度：仅 {cs['venus_equilibrium_temp_k']} K ({cs['venus_equilibrium_temp_celsius']} °C)
  * 92 大气压实测表面温度：{cs['venus_actual_surface_temp_k']} K ({cs['venus_actual_surface_temp_celsius']} °C)，温室效应抬升 {cs['venus_greenhouse_temp_boost_c']} °C
  * 萨根灰体辐射传输解：要求大气有效红外光学厚度 τ 达 {cs['venus_required_optical_depth_tau']}

【三、今夜天象 (2026-11-09 农历十月初一 · 朔日)】
- 月相特征：亮面仅 {sky['lunar_phase_percent']}%，月龄 {sky['moon_age_days']} 天，地月距 {sky['distance_km']} km
- 朔日时序：今日 15:02 CST 精确朔月，今夜过朔仅 {sky['hours_since_exact_new_moon']} 小时
- 观测天窗：{sky['night_sky_condition']}，华夏全境整夜 100% 零月光污染，深空天体最高信噪比天窗
================================================================================
"""

if __name__ == "__main__":
    print(format_summary_report())
