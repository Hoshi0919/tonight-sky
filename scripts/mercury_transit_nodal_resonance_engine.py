"""
水星凌日 (Mercury Transit)、轨道交点共振 (Nodal Resonance) 与丢番图周期逼近动力学解算引擎
纪念 2019-11-11 极罕见水星凌日 7 周年轨道交点共振 (2019-11-11 至 2026-11-11)
推演水星高偏心率轨道、升降交点几何、7/13/46 年凌日周期律及 2032-11-13 下一次凌日预报
"""

import math
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List


class MercuryTransitNodalResonanceEngine:
    """
    水星凌日天体力学与交点谐波共振推演引擎
    """

    # 基础天体物理常数 (IAU / CODATA 标定)
    AU_KM = 149597870.7                  # 1 天文单位 (km)
    R_SUN_KM = 696340.0                  # 太阳物理半径 (km)
    R_MERCURY_KM = 2439.7                # 水星物理半径 (km)
    R_EARTH_KM = 6378.137                # 地球赤道半径 (km)
    SPEED_OF_LIGHT_KMS = 299792.458      # 光速 (km/s)

    # 地球与水星名义轨道参数 (J2000)
    P_EARTH_DAYS = 365.256363            # 地球恒星年 (日)
    P_MERCURY_DAYS = 87.9691             # 水星恒星公转周期 (日)
    A_MERCURY_AU = 0.387098              # 水星半长轴 (AU)
    E_MERCURY = 0.205630                 # 水星轨道偏心率
    I_MERCURY_DEG = 7.0049               # 水星轨道倾角 (度)
    OMEGA_NODE_ASC_DEG = 48.331          # 升交点黄经 (度)
    OMEGA_NODE_DESC_DEG = 228.331        # 降交点黄经 (度)
    OMEGA_PERIHELION_DEG = 29.124        # 近日点幅角 (度)
    VARPI_PERIHELION_DEG = 77.455        # 近日点黄经 (度)

    def __init__(self, current_dt: datetime = None):
        if current_dt is None:
            self.current_dt = datetime(2026, 11, 11, 12, 0, 0, tzinfo=timezone.utc)
        else:
            self.current_dt = current_dt

        # 2019-11-11 水星凌日实测基准时间戳
        self.transit_2019_t1_utc = datetime(2019, 11, 11, 12, 35, 27, tzinfo=timezone.utc) # 第一外切
        self.transit_2019_mid_utc = datetime(2019, 11, 11, 15, 19, 48, tzinfo=timezone.utc) # 最小角距极大
        self.transit_2019_t4_utc = datetime(2019, 11, 11, 18, 4, 14, tzinfo=timezone.utc)  # 第四外切

    def compute_orbital_resonance_diophantine(self) -> Dict[str, Any]:
        """
        解算地球-水星会合周期、连分数展开与丢番图周期逼近谐波 (Diophantine Approximation)
        """
        # 会合周期 S = 1 / (1/P_M - 1/P_E)
        synodic_period_days = 1.0 / (1.0 / self.P_MERCURY_DAYS - 1.0 / self.P_EARTH_DAYS)
        ratio_years = self.P_EARTH_DAYS / self.P_MERCURY_DAYS

        # 连分数与周期收敛项
        # 1. 7 年周期 (29 个水星公转年, 22 个会合周期)
        earth_7y_days = 7.0 * self.P_EARTH_DAYS
        merc_29y_days = 29.0 * self.P_MERCURY_DAYS
        syn_22_days = 22.0 * synodic_period_days
        err_7y_days = earth_7y_days - merc_29y_days

        # 2. 13 年周期 (54 个水星公转年, 41 个会合周期)
        earth_13y_days = 13.0 * self.P_EARTH_DAYS
        merc_54y_days = 54.0 * self.P_MERCURY_DAYS
        syn_41_days = 41.0 * synodic_period_days
        err_13y_days = earth_13y_days - merc_54y_days

        # 3. 46 年大周期 (191 个水星公转年, 145 个会合周期)
        earth_46y_days = 46.0 * self.P_EARTH_DAYS
        merc_191y_days = 191.0 * self.P_MERCURY_DAYS
        syn_145_days = 145.0 * synodic_period_days
        err_46y_days = earth_46y_days - merc_191y_days

        return {
            "synodic_period_days": synodic_period_days,
            "period_ratio_PE_over_PM": ratio_years,
            "cycle_7yr": {
                "earth_years": 7,
                "mercury_revolutions": 29,
                "synodic_cycles": 22,
                "delta_days_vs_orbit": err_7y_days,
                "delta_days_vs_synodic": earth_7y_days - syn_22_days,
                "relative_error": abs(29.0 / 7.0 - ratio_years) / ratio_years,
            },
            "cycle_13yr": {
                "earth_years": 13,
                "mercury_revolutions": 54,
                "synodic_cycles": 41,
                "delta_days_vs_orbit": err_13y_days,
                "delta_days_vs_synodic": earth_13y_days - syn_41_days,
                "relative_error": abs(54.0 / 13.0 - ratio_years) / ratio_years,
            },
            "cycle_46yr": {
                "earth_years": 46,
                "mercury_revolutions": 191,
                "synodic_cycles": 145,
                "delta_days_vs_orbit": err_46y_days,
                "delta_days_vs_synodic": earth_46y_days - syn_145_days,
                "relative_error": abs(191.0 / 46.0 - ratio_years) / ratio_years,
            }
        }

    def compute_nodal_transit_geometry(self) -> Dict[str, Any]:
        """
        解算五月升交点与十一月降交点水星凌日的偏心率几何差异与发生频率不对称机理
        """
        # 水星近日点距离与远日点距离
        r_perihelion_au = self.A_MERCURY_AU * (1.0 - self.E_MERCURY)
        r_aphelion_au = self.A_MERCURY_AU * (1.0 + self.E_MERCURY)

        # 1. 降交点 (11 月 10-11 日): 靠近水星近日点 (幅角 ~29°)
        # r_desc 约 0.31 AU
        # 地心距 Delta_desc = 1.0 - r_desc ~ 0.69 AU
        r_desc_au = 0.3129
        delta_desc_au = 1.0 - r_desc_au
        # 视直径 (角秒): 2 * R_merc / (Delta * AU) * 206265
        ang_diam_desc_arcsec = (2.0 * self.R_MERCURY_KM) / (delta_desc_au * self.AU_KM) * 206264.806
        # 太阳视直径 (降交点时日地距约 0.989 AU):
        r_sun_desc_au = 0.989
        sun_diam_desc_arcsec = (2.0 * self.R_SUN_KM) / (r_sun_desc_au * self.AU_KM) * 206264.806

        # 2. 升交点 (5 月 7-8 日): 靠近水星远日点
        # r_asc 约 0.45 AU
        # 地心距 Delta_asc = 1.0 - r_asc ~ 0.55 AU
        r_asc_au = 0.4533
        delta_asc_au = 1.0 - r_asc_au
        ang_diam_asc_arcsec = (2.0 * self.R_MERCURY_KM) / (delta_asc_au * self.AU_KM) * 206264.806
        r_sun_asc_au = 1.008
        sun_diam_asc_arcsec = (2.0 * self.R_SUN_KM) / (r_sun_asc_au * self.AU_KM) * 206264.806

        # 轨道速率 (开普勒活力公式 v = sqrt(GM * (2/r - 1/a)))
        mu_sun = 1.32712440018e11 # km^3 / s^2
        a_km = self.A_MERCURY_AU * self.AU_KM
        v_desc = math.sqrt(mu_sun * (2.0 / (r_desc_au * self.AU_KM) - 1.0 / a_km))
        v_asc = math.sqrt(mu_sun * (2.0 / (r_asc_au * self.AU_KM) - 1.0 / a_km))

        # 凌日历时极限 (弦长穿越最大历时)
        # 降交点穿越速度较快，典型历时 5.5 小时；升交点速度慢，典型历时可达 8.0~8.5 小时
        max_duration_desc_hours = 5.5
        max_duration_asc_hours = 8.5

        # 降交点 (11月) 与升交点 (5月) 发生几率比约为 2 : 1
        november_to_may_ratio = 2.05

        return {
            "november_descending_node": {
                "crossing_date_window": "November 10 - 11",
                "mercury_sun_distance_au": r_desc_au,
                "mercury_earth_distance_au": delta_desc_au,
                "orbital_speed_kms": v_desc,
                "mercury_apparent_diameter_arcsec": ang_diam_desc_arcsec,
                "sun_apparent_diameter_arcsec": sun_diam_desc_arcsec,
                "solar_area_obscuration_ratio": (ang_diam_desc_arcsec / sun_diam_desc_arcsec)**2,
                "solar_flux_drop_percent": (ang_diam_desc_arcsec / sun_diam_desc_arcsec)**2 * 100.0,
                "typical_max_duration_hours": max_duration_desc_hours,
            },
            "may_ascending_node": {
                "crossing_date_window": "May 7 - 8",
                "mercury_sun_distance_au": r_asc_au,
                "mercury_earth_distance_au": delta_asc_au,
                "orbital_speed_kms": v_asc,
                "mercury_apparent_diameter_arcsec": ang_diam_asc_arcsec,
                "sun_apparent_diameter_arcsec": sun_diam_asc_arcsec,
                "solar_area_obscuration_ratio": (ang_diam_asc_arcsec / sun_diam_asc_arcsec)**2,
                "solar_flux_drop_percent": (ang_diam_asc_arcsec / sun_diam_asc_arcsec)**2 * 100.0,
                "typical_max_duration_hours": max_duration_asc_hours,
            },
            "frequency_ratio_november_vs_may": november_to_may_ratio
        }

    def compute_2019_transit_baseline_and_7yr_echo(self) -> Dict[str, Any]:
        """
        解算 2019-11-11 水星凌日实测基准数据及今日 2026-11-11 7 周年轨道几何回响
        """
        duration_s = (self.transit_2019_t4_utc - self.transit_2019_t1_utc).total_seconds()
        duration_h = duration_s / 3600.0

        # 从 2019-11-11 极大时刻到 2026-11-11 12:00:00 UTC 的经历时间
        elapsed_days = (self.current_dt - self.transit_2019_mid_utc).total_seconds() / 86400.0
        elapsed_years = elapsed_days / 365.256363
        mercury_orbits_completed = elapsed_days / self.P_MERCURY_DAYS

        # 今日水星几何状态 (2026-11-11)
        # 水星刚刚在 2026-11-05 经历下合日 (距离太阳仅 0°57')
        # 今日与太阳角距 ~13°，正处于晨曦向西大距快速展开期
        days_since_inferior_conjunction = 6.0
        mercury_elongation_deg = -13.72
        next_greatest_elongation_west_date = "2026-11-20"
        next_greatest_elongation_west_deg = 19.5

        return {
            "transit_2019_11_11_observed": {
                "ingress_t1_utc": "12:35:27",
                "greatest_transit_mid_utc": "15:19:48",
                "egress_t4_utc": "18:04:14",
                "duration_hours": duration_h,
                "minimum_separation_arcsec": 75.9,
                "mercury_diameter_arcsec": 9.93,
                "solar_diameter_arcsec": 1937.8,
            },
            "seven_year_anniversary_2026": {
                "exact_elapsed_days": elapsed_days,
                "exact_elapsed_earth_years": elapsed_years,
                "exact_mercury_orbits_completed": mercury_orbits_completed,
                "resonance_deviation_days": elapsed_days - 29.0 * self.P_MERCURY_DAYS,
                "inferior_conjunction_recent_utc": "2026-11-05",
                "days_since_inferior_conjunction": days_since_inferior_conjunction,
                "current_mercury_elongation_deg": mercury_elongation_deg,
                "upcoming_western_greatest_elongation": {
                    "date": next_greatest_elongation_west_date,
                    "elongation_deg": next_greatest_elongation_west_deg
                }
            }
        }

    def compute_century_21_transits_catalog(self) -> List[Dict[str, Any]]:
        """
        21 世纪全部水星凌日编目与 7/13/46 周期跃迁网络
        """
        transits = [
            {"date": "2003-05-07", "node": "Ascending (May)", "duration_h": 5.3, "interval_previous": None},
            {"date": "2006-11-08", "node": "Descending (Nov)", "duration_h": 4.9, "interval_previous": "3.5 years"},
            {"date": "2016-05-09", "node": "Ascending (May)", "duration_h": 7.5, "interval_previous": "13 years (from 2003)"},
            {"date": "2019-11-11", "node": "Descending (Nov)", "duration_h": 5.5, "interval_previous": "13 years (from 2006)"},
            {"date": "2032-11-13", "node": "Descending (Nov)", "duration_h": 4.5, "interval_previous": "13 years (from 2019)"},
            {"date": "2039-11-07", "node": "Descending (Nov)", "duration_h": 3.7, "interval_previous": "7 years (from 2032)"},
            {"date": "2049-05-07", "node": "Ascending (May)", "duration_h": 6.8, "interval_previous": "46 years (from 2003)"},
            {"date": "2052-11-09", "node": "Descending (Nov)", "duration_h": 4.0, "interval_previous": "46 years (from 2006)"},
            {"date": "2062-05-10", "node": "Ascending (May)", "duration_h": 7.6, "interval_previous": "46 years (from 2016)"},
            {"date": "2065-11-11", "node": "Descending (Nov)", "duration_h": 5.4, "interval_previous": "46 years (from 2019)"},
            {"date": "2078-11-14", "node": "Descending (Nov)", "duration_h": 4.2, "interval_previous": "46 years (from 2032)"},
            {"date": "2085-11-07", "node": "Descending (Nov)", "duration_h": 3.5, "interval_previous": "46 years (from 2039)"},
            {"date": "2095-05-08", "node": "Ascending (May)", "duration_h": 6.9, "interval_previous": "46 years (from 2049)"},
            {"date": "2098-11-10", "node": "Descending (Nov)", "duration_h": 4.1, "interval_previous": "46 years (from 2052)"},
        ]
        return transits
