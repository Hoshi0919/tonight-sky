"""
先驱者 9 号 (Pioneer 9) 发射 58 周年纪念、行星际空间天气四角星座预警拓扑、
帕克太阳探测器 (Parker Solar Probe) 首次掠日近日点 8 周年日冕穿越、
WISPR 首张日冕等离子体流全景反演与 2026-11-08 朔日前夕纯黑暗空推演引擎
"""

import math
import datetime

# 基础物理与天体常数
SPEED_OF_LIGHT = 299792458.0          # m/s
AU_METERS = 149597870700.0           # 1 AU in meters
SOLAR_CONSTANT_1AU = 1361.0          # W/m^2 (1 AU 日面辐射能流)
R_SUN_METERS = 696340000.0           # 太阳半径 R_sun (米)
GM_SUN = 1.32712440018e20            # m^3/s^2 (G * M_sun)
STEFAN_BOLTZMANN = 5.670374419e-8    # W/(m^2 K^4)


class Pioneer9ParkerPerihelionEngine:
    """
    先驱者 9 号 58 周年与帕克探测器首次掠日 8 周年天体物理推演引擎
    """

    def __init__(self, current_dt=None):
        if current_dt is None:
            # 默认基准时间：2026-11-08 22:30:00 CST (14:30:00 UTC)
            self.current_dt = datetime.datetime(2026, 11, 8, 14, 30, tzinfo=datetime.timezone.utc)
        else:
            self.current_dt = current_dt

        # 核心任务时间节点
        self.pioneer9_launch_dt = datetime.datetime(1968, 11, 8, 9, 46, tzinfo=datetime.timezone.utc)
        self.pioneer9_last_contact_dt = datetime.datetime(1983, 3, 3, 0, 0, tzinfo=datetime.timezone.utc)
        self.pioneer9_retired_dt = datetime.datetime(1987, 5, 11, 0, 0, tzinfo=datetime.timezone.utc)
        self.pioneer9_anniversary_58y_dt = datetime.datetime(2026, 11, 8, 9, 46, tzinfo=datetime.timezone.utc)

        self.parker_launch_dt = datetime.datetime(2018, 8, 12, 7, 31, tzinfo=datetime.timezone.utc)
        self.parker_first_perihelion_dt = datetime.datetime(2018, 11, 8, 3, 27, tzinfo=datetime.timezone.utc)
        self.parker_first_perihelion_8y_dt = datetime.datetime(2026, 11, 8, 3, 27, tzinfo=datetime.timezone.utc)

        # 先驱者 9 号轨道与物理参数
        self.p9_mass_kg = 63.0               # kg
        self.p9_perihelion_au = 0.754        # AU
        self.p9_aphelion_au = 0.990          # AU
        self.p9_semi_major_axis_au = (self.p9_perihelion_au + self.p9_aphelion_au) / 2.0  # 0.872 AU
        self.p9_eccentricity = (self.p9_aphelion_au - self.p9_perihelion_au) / (self.p9_aphelion_au + self.p9_perihelion_au)

        # 帕克太阳探测器参数
        self.parker_mass_dry_kg = 555.0      # kg
        self.parker_mass_wet_kg = 685.0      # kg
        self.parker_tps_diameter_m = 2.3     # m (热防护罩直径)
        self.parker_tps_thickness_cm = 11.4  # cm (碳碳/碳泡沫复合热盾)

        # 帕克第 1 次近日点 (2018-11-08) vs 最终第 24 次极限近日点 (0.046 AU)
        self.p1_r_peri_au = 0.166            # AU
        self.p1_speed_kms = 95.3             # km/s
        self.p24_r_peri_au = 0.046           # AU
        self.p24_speed_kms = 192.0           # km/s

    def compute_pioneer9_timeline_and_orbit(self):
        """
        计算先驱者 9 号 58 周年时间跨度、开普勒轨道特征与差速超前漂移
        """
        elapsed_sec = (self.current_dt - self.pioneer9_launch_dt).total_seconds()
        total_years = elapsed_sec / (86400.0 * 365.25)
        active_days = (self.pioneer9_last_contact_dt - self.pioneer9_launch_dt).total_seconds() / 86400.0

        # 开普勒周期 T = a^1.5 (年)
        period_years = math.pow(self.p9_semi_major_axis_au, 1.5)
        period_days = period_years * 365.25
        orbital_revs_58y = (total_years * 365.25) / period_days

        # 相对于地球 (365.25 天) 的年均超前漂移角速率 (度/地球年)
        # delta_omega = 360 * (1/T_p9 - 1/T_earth)
        annual_drift_deg = 360.0 * (1.0 / period_years - 1.0)

        # 近日点与远日点速度 (活力公式 v = sqrt(GM * (2/r - 1/a)))
        mu = GM_SUN
        a_m = self.p9_semi_major_axis_au * AU_METERS
        r_p_m = self.p9_perihelion_au * AU_METERS
        r_a_m = self.p9_aphelion_au * AU_METERS

        v_peri_ms = math.sqrt(mu * (2.0 / r_p_m - 1.0 / a_m))
        v_apo_ms = math.sqrt(mu * (2.0 / r_a_m - 1.0 / a_m))

        return {
            "total_elapsed_years": round(total_years, 2),
            "active_service_days": round(active_days, 1),
            "active_service_years": round(active_days / 365.25, 2),
            "design_lifetime_days": 180.0,
            "lifetime_margin_factor": round(active_days / 180.0, 1),
            "semi_major_axis_au": round(self.p9_semi_major_axis_au, 4),
            "eccentricity": round(self.p9_eccentricity, 4),
            "period_days": round(period_days, 2),
            "orbital_revolutions_completed": round(orbital_revs_58y, 2),
            "annual_heliocentric_drift_deg": round(annual_drift_deg, 2),
            "v_perihelion_kms": round(v_peri_ms / 1000.0, 2),
            "v_aphelion_kms": round(v_apo_ms / 1000.0, 2),
        }

    def compute_parker_first_perihelion_physics(self):
        """
        计算 2018-11-08 帕克首次近日点与极限近日点的热力学及动力学对偶
        """
        elapsed_sec = (self.current_dt - self.parker_first_perihelion_dt).total_seconds()
        elapsed_years = elapsed_sec / (86400.0 * 365.25)

        # 太阳辐射通量 S = S0 / r^2
        flux_p1 = SOLAR_CONSTANT_1AU / math.pow(self.p1_r_peri_au, 2)
        flux_p24 = SOLAR_CONSTANT_1AU / math.pow(self.p24_r_peri_au, 2)
        flux_ratio = flux_p24 / flux_p1

        # 距离太阳半径 (R_sun)
        dist_rsun_p1 = (self.p1_r_peri_au * AU_METERS) / R_SUN_METERS
        dist_rsun_p24 = (self.p24_r_peri_au * AU_METERS) / R_SUN_METERS

        # 热盾前向辐射平衡温度估算:
        # 平衡方程: (1 - albedo) * S = emissivity * sigma * T^4
        # 碳碳复合材料: 吸收率 alpha ≈ 0.85, 红外发射率 eps ≈ 0.82
        alpha = 0.85
        eps = 0.82
        sigma = STEFAN_BOLTZMANN

        t_kelvin_p1 = math.pow((alpha * flux_p1) / (eps * sigma), 0.25)
        t_celsius_p1 = t_kelvin_p1 - 273.15

        t_kelvin_p24 = math.pow((alpha * flux_p24) / (eps * sigma), 0.25)
        t_celsius_p24 = t_kelvin_p24 - 273.15

        # 动能密度 Ek = 0.5 * m * v^2
        ek_p1_gj = 0.5 * self.parker_mass_wet_kg * math.pow(self.p1_speed_kms * 1000.0, 2) / 1e9
        ek_p24_gj = 0.5 * self.parker_mass_dry_kg * math.pow(self.p24_speed_kms * 1000.0, 2) / 1e9

        return {
            "first_perihelion_elapsed_years": round(elapsed_years, 2),
            "p1_distance_au": self.p1_r_peri_au,
            "p1_distance_solar_radii": round(dist_rsun_p1, 2),
            "p1_solar_flux_w_m2": round(flux_p1, 1),
            "p1_flux_earth_ratio": round(flux_p1 / SOLAR_CONSTANT_1AU, 1),
            "p1_tps_equilibrium_celsius": round(t_celsius_p1, 1),
            "p1_speed_kms": self.p1_speed_kms,
            "p1_kinetic_energy_gj": round(ek_p1_gj, 2),
            "p24_distance_au": self.p24_r_peri_au,
            "p24_distance_solar_radii": round(dist_rsun_p24, 2),
            "p24_solar_flux_w_m2": round(flux_p24, 1),
            "p24_flux_earth_ratio": round(flux_p24 / SOLAR_CONSTANT_1AU, 1),
            "p24_tps_equilibrium_celsius": round(t_celsius_p24, 1),
            "p24_speed_kms": self.p24_speed_kms,
            "p24_kinetic_energy_gj": round(ek_p24_gj, 2),
            "flux_escalation_ratio": round(flux_ratio, 2),
        }

    def compute_night_darksky_status(self):
        """
        2026-11-08 农历九月三十晦日暗空与朔日倒计时
        """
        # 精确新月时间：2026-11-09 07:02:03 UTC (北京时间 2026-11-09 15:02:03 CST)
        new_moon_dt = datetime.datetime(2026, 11, 9, 7, 2, 3, tzinfo=datetime.timezone.utc)
        countdown_hours = (new_moon_dt - self.current_dt).total_seconds() / 3600.0

        return {
            "lunar_phase_percent": 0.65,
            "moon_age_days": 28.9,
            "distance_km": 401865.0,
            "hours_to_exact_new_moon": round(countdown_hours, 2),
            "darksky_window_percent": 100.0,
            "night_sky_condition": "纯黑暗空天窗 (100% 零月光污染)",
        }


def format_summary_report():
    engine = Pioneer9ParkerPerihelionEngine()
    p9 = engine.compute_pioneer9_timeline_and_orbit()
    psp = engine.compute_parker_first_perihelion_physics()
    sky = engine.compute_night_darksky_status()

    return f"""
================================================================================
先驱者 9 号 58 周年与帕克探测器首次掠日 8 周年天体力学推演报告 (2026-11-08)
================================================================================
【一、先驱者 9 号 (Pioneer 9 / Pioneer D) 58 周年里程碑】
- 发射时刻：1968-11-08 09:46 UTC (Thor-Delta E1，卡纳维拉尔角 LC-17B)
- 在轨跨度：{p9['total_elapsed_years']} 周年整（实测连续服役 {p9['active_service_days']} 天 / {p9['active_service_years']} 年）
- 寿命冗余：设计寿命 {p9['design_lifetime_days']} 天，实测超额生存 {p9['lifetime_margin_factor']} 倍
- 开普勒轨道：半长轴 a = {p9['semi_major_axis_au']} AU，偏心率 e = {p9['eccentricity']}
- 运行周期：{p9['period_days']} 天（58 年间已完成 {p9['orbital_revolutions_completed']} 圈日心公转）
- 差速超前漂移率：{p9['annual_heliocentric_drift_deg']}° / 地球年
- 轨道速度：近日点 {p9['v_perihelion_kms']} km/s，远日点 {p9['v_aphelion_kms']} km/s
- 科学遗产：与 Pioneer 6/7/8 构筑首个太阳系 1 AU 行星际空间天气四角预警天网

【二、帕克太阳探测器 (Parker Solar Probe) 首次掠日近日点 8 周年】
- 首次近日点：2018-11-08 03:27 UTC（距发射仅 88 天，今日整整 {psp['first_perihelion_elapsed_years']} 周年）
- 首次掠日距离：{psp['p1_distance_au']} AU ({psp['p1_distance_solar_radii']} 太阳半径 / 约 2,480 万公里)
- 首次掠日极速：{psp['p1_speed_kms']} km/s (时速 34.3 万公里)
- 首次辐射通量：{psp['p1_solar_flux_w_m2']} W/m² (地球轨道的 {psp['p1_flux_earth_ratio']} 倍)
- 首次热盾平衡温度：{psp['p1_tps_equilibrium_celsius']} °C (碳碳复合热盾前表面)
- 科学突破：WISPR 首次自日冕内部拍摄到日冕流带与背景水星亮星全景
- 极限对偶 (Perihelion #24)：0.046 AU ({psp['p24_distance_solar_radii']} R☉), 能流暴增 {psp['flux_escalation_ratio']} 倍达 {psp['p24_solar_flux_w_m2']} W/m² ({psp['p24_flux_earth_ratio']} 倍地球通量), 热盾温升至 {psp['p24_tps_equilibrium_celsius']} °C

【三、今夜天象 (2026-11-08 农历九月三十 · 晦日)】
- 月相亮面：{sky['lunar_phase_percent']}% 弱微月，月龄 {sky['moon_age_days']} 天
- 距精确朔日新月时刻：仅剩 {sky['hours_to_exact_new_moon']} 小时
- 观测条件：{sky['night_sky_condition']}，华夏全境整夜 100% 零月光干扰，全天暗弱星云与深空星系观测黄金窗口
================================================================================
"""

if __name__ == "__main__":
    print(format_summary_report())
