import math

class Luna12Lageos2RelativityEngine:
    """
    1966-10-22 Luna 12 (60 周年甲子钻禧) 与 1992-10-22 LAGEOS-2 (34 周年广义相对论时空拖拽)
    动力学与天体物理测地线解算引擎
    """
    # 基础物理常数
    G = 6.67430e-11              # m^3 / (kg * s^2)
    C = 299792458.0              # m / s
    MU_EARTH = 3.986004418e14    # m^3 / s^2
    R_EARTH = 6378137.0          # m
    J_EARTH = 5.86e33            # kg * m^2 / s (地球自转角动量)
    J2_EARTH = 1.08263e-3        # 地球二阶引力多极矩

    MU_MOON = 4.9028e12          # m^3 / s^2 (4902.8 km^3/s^2)
    R_MOON = 1737400.0           # m

    def __init__(self):
        pass

    def compute_luna12_dynamics(self):
        # 初始椭圆捕获轨
        hp_init = 100.0e3
        ha_init = 1740.0e3
        rp_init = self.R_MOON + hp_init
        ra_init = self.R_MOON + ha_init
        a_init = (rp_init + ra_init) / 2.0
        T_init_s = 2.0 * math.pi * math.sqrt(a_init**3 / self.MU_MOON)
        T_init_min = T_init_s / 60.0

        # 稳定工作轨
        hp = 133.0e3
        ha = 1200.0e3
        rp = self.R_MOON + hp
        ra = self.R_MOON + ha
        a = (rp + ra) / 2.0
        e = (ra - rp) / (ra + rp)
        T_s = 2.0 * math.pi * math.sqrt(a**3 / self.MU_MOON)
        T_min = T_s / 60.0

        vp = math.sqrt(self.MU_MOON * (2.0 / rp - 1.0 / a))
        va = math.sqrt(self.MU_MOON * (2.0 / ra - 1.0 / a))

        return {
            "satellite": "Luna 12 (E-6LF No. 102)",
            "launch_date_utc": "1966-10-22 08:42:26",
            "orbital_insertion_utc": "1966-10-25 20:45",
            "anniversary_years": 60,
            "jubilee_name": "Diamond Jubilee (六十甲子钻禧)",
            "launcher": "Molniya-M 8K78M",
            "launch_site": "Baikonur 31/6",
            "initial_capture_orbit": {
                "perilune_alt_km": 100.0,
                "apolune_alt_km": 1740.0,
                "semi_major_axis_km": round(a_init / 1e3, 1),
                "period_min": round(T_init_min, 1)
            },
            "operational_orbit": {
                "perilune_alt_km": 133.0,
                "apolune_alt_km": 1200.0,
                "semi_major_axis_km": round(a / 1e3, 1),
                "eccentricity": round(e, 4),
                "period_min": round(T_min, 1),
                "inclination_deg": 10.0
            },
            "perilune_velocity_km_s": round(vp / 1e3, 3),
            "apolune_velocity_km_s": round(va / 1e3, 3),
            "imaging_payload": "Enisei-3 automated photographic & scanning unit",
            "scan_lines": 1100,
            "ground_resolution_m": (14.9, 19.8),
            "total_lunar_orbits": 602,
            "radio_sessions": 302,
            "primary_targets": ["Mare Imbrium (Sea of Rains)", "Aristarchus Crater"]
        }

    def compute_lageos2_relativity_dynamics(self):
        a = 12210.0e3
        alt = a - self.R_EARTH
        e = 0.014
        inc_deg = 52.65
        inc = math.radians(inc_deg)
        mass = 405.4
        diam = 0.6
        radius = diam / 2.0
        area = math.pi * (radius**2)
        area_to_mass = area / mass

        # 广义相对论 Lense-Thirring 参考系拖拽 (rad/s)
        # Omega_dot_LT = 2 * G * J_earth / [ c^2 * a^3 * (1 - e^2)^(3/2) ]
        omega_dot_lt_rad_s = (2.0 * self.G * self.J_EARTH) / (
            (self.C**2) * (a**3) * ((1.0 - e**2)**1.5)
        )
        sec_per_yr = 365.25 * 86400.0
        rad_to_mas = (180.0 / math.pi) * 3600.0 * 1000.0
        lt_mas_yr = omega_dot_lt_rad_s * sec_per_yr * rad_to_mas

        # 经典 J2 引力多极矩摄动引起的升交点赤经进动
        # Omega_dot_J2 = -3/2 * J2 * R_earth^2 * sqrt(mu_earth) * a^(-7/2) * (1-e^2)^(-2) * cos(inc)
        omega_dot_j2_rad_s = (
            -1.5 * self.J2_EARTH * (self.R_EARTH**2) * math.sqrt(self.MU_EARTH) *
            (a**(-3.5)) * ((1.0 - e**2)**(-2)) * math.cos(inc)
        )
        j2_deg_day = omega_dot_j2_rad_s * 86400.0 * (180.0 / math.pi)

        # 卫星激光测距双程光行时
        tau_roundtrip_ms = (2.0 * alt / self.C) * 1000.0

        return {
            "satellite": "LAGEOS-2 (Laser Geodynamics Satellite II)",
            "launch_mission": "STS-52 (Space Shuttle Columbia)",
            "launch_date": "1992-10-22",
            "anniversary_years": 34,
            "orbit": {
                "semi_major_axis_km": round(a / 1e3, 1),
                "altitude_km": round(alt / 1e3, 1),
                "eccentricity": e,
                "inclination_deg": inc_deg
            },
            "satellite_specs": {
                "mass_kg": mass,
                "diameter_m": diam,
                "cross_section_area_m2": round(area, 4),
                "area_to_mass_ratio_m2_per_kg": round(area_to_mass, 6),
                "retroreflectors_total": 426,
                "fused_silica_prisms": 422,
                "germanium_prisms": 4
            },
            "relativity_physics": {
                "earth_spin_angular_momentum_kg_m2_s": self.J_EARTH,
                "lense_thirring_precession_mas_per_yr": round(lt_mas_yr, 2),
                "classic_j2_precession_deg_per_day": round(j2_deg_day, 4),
                "slr_ranging_precision_mm": 2.0,
                "laser_roundtrip_time_ms": round(tau_roundtrip_ms, 2),
                "frame_dragging_verified": True
            },
            "complementary_satellite": "LAGEOS-1 (1976, i=109.8 deg, LT=30.67 mas/yr)"
        }

    def compute_quadruple_deepspace_heritage_2026(self):
        return {
            "epoch_date": "2026-10-22",
            "milestones": [
                {
                    "name": "Luna 12",
                    "launch_year": 1966,
                    "anniversary": 60,
                    "domain": "Lunar high-res imaging & photographic facsimile"
                },
                {
                    "name": "Venera 9",
                    "landing_year": 1975,
                    "anniversary": 51,
                    "domain": "First extraterrestrial surface panorama & supercritical landing"
                },
                {
                    "name": "LAGEOS-2",
                    "launch_year": 1992,
                    "anniversary": 34,
                    "domain": "General relativity Lense-Thirring frame-dragging & satellite laser ranging"
                },
                {
                    "name": "Chandrayaan-1",
                    "launch_year": 2008,
                    "anniversary": 18,
                    "domain": "Lunar water ice spectroscopy & South Pole impact confirmation"
                }
            ],
            "total_heritage_count": 4
        }
