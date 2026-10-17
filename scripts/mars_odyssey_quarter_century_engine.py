"""
2001 火星奥德赛号 (2001 Mars Odyssey) 在轨环绕 25 周年银禧纪念、
GRS 伽马射线与中子谱仪浅表水冰发现、THEMIS 全球热惯量与矿物制图、
火星现役六重奏 (The Martian Hexad / Sextet) 与 2026 人类深空二十七极黄金舰队 (The Grand Septemvigintet) 推演引擎
"""

import math
import datetime

# 基础物理与天体常数
SPEED_OF_LIGHT = 299792458.0  # m/s
AU_METERS = 149597870700.0   # 1 AU in meters
SOLAR_CONSTANT_1AU = 1361.0  # W/m^2 at 1 AU

# 火星物理常数
GM_MARS = 4.282837e13         # m^3/s^2 (G * M_mars)
R_MARS = 3389.5e3             # m (Mars mean volumetric radius, 3389.5 km)
MASS_MARS = 6.4171e23         # kg
MARS_SOL_SECONDS = 88775.244  # 1 sol = 24h 39m 35.244s

class MarsOdysseyEngine:
    """
    2001 Mars Odyssey 在轨 25 周年动力学、水冰反演、热惯量与六大金刚矩阵
    """
    def __init__(self, current_dt=None):
        if current_dt is None:
            self.current_dt = datetime.datetime(2026, 10, 18, 4, 30, tzinfo=datetime.timezone.utc)
        else:
            self.current_dt = current_dt

        # 关键历史时间节点
        self.launch_dt = datetime.datetime(2001, 4, 7, 15, 2, tzinfo=datetime.timezone.utc)
        self.moi_dt = datetime.datetime(2001, 10, 24, 2, 26, tzinfo=datetime.timezone.utc) # Mars Orbit Insertion
        self.anniversary_25y_dt = datetime.datetime(2026, 10, 24, 2, 26, tzinfo=datetime.timezone.utc)

        # 标称制图轨道参数 (Circular Sun-synchronous near-polar mapping orbit)
        self.h_orbit = 400.0e3      # 标称轨道平均高度 400 km (390~405 km)
        self.r_orbit = R_MARS + self.h_orbit # 3789.5 km
        self.inclination_deg = 93.1 # 逆行极轨倾角
        self.eccentricity = 0.009   # 近圆轨道偏心率

    def compute_mission_timeline(self):
        """
        计算任务时间线与 25 周年倒计时
        """
        flight_sec = (self.current_dt - self.launch_dt).total_seconds()
        orbit_sec = (self.current_dt - self.moi_dt).total_seconds()
        countdown_sec = (self.anniversary_25y_dt - self.current_dt).total_seconds()

        days_in_orbit = orbit_sec / 86400.0
        years_in_orbit = days_in_orbit / 365.25
        mars_years_in_orbit = days_in_orbit / 686.98

        countdown_days = countdown_sec / 86400.0
        countdown_hours = countdown_sec / 3600.0

        return {
            "days_in_orbit": days_in_orbit,
            "years_in_orbit": years_in_orbit,
            "mars_years_in_orbit": mars_years_in_orbit,
            "total_flight_days": flight_sec / 86400.0,
            "countdown_to_25y_days": countdown_days,
            "countdown_to_25y_hours": countdown_hours,
            "is_silver_jubilee_near": 0 <= countdown_days <= 10.0
        }

    def compute_orbit_dynamics(self):
        """
        开普勒轨道动力学：速度、周期与公转圈数
        """
        r = self.r_orbit
        v_circ = math.sqrt(GM_MARS / r) # m/s
        period_sec = 2.0 * math.pi * math.sqrt(r**3 / GM_MARS) # s
        period_min = period_sec / 60.0
        period_hours = period_sec / 3600.0

        orbits_per_earth_day = 86400.0 / period_sec
        orbits_per_sol = MARS_SOL_SECONDS / period_sec

        timeline = self.compute_mission_timeline()
        total_orbits = timeline["days_in_orbit"] * orbits_per_earth_day

        return {
            "orbital_altitude_km": self.h_orbit / 1e3,
            "orbital_radius_km": r / 1e3,
            "orbital_velocity_kms": v_circ / 1e3,
            "period_minutes": period_min,
            "period_hours": period_hours,
            "orbits_per_earth_day": orbits_per_earth_day,
            "orbits_per_sol": orbits_per_sol,
            "cumulative_orbits": total_orbits
        }

    def compute_aerobraking_physics(self):
        """
        气动减速 (Aerobraking) 物理与推进剂节省模型
        """
        # 初始捕获轨道: 250 km x 27,000 km (周期约 19.9 小时)
        rp_initial = R_MARS + 250.0e3 # 3639.5 km
        ra_initial = R_MARS + 27000.0e3 # 30389.5 km
        a_initial = (rp_initial + ra_initial) / 2.0
        
        # 最终制图轨道: 400 km x 400 km
        a_final = self.r_orbit

        # 若纯靠化学推进机动降轨所需 Delta-V
        # 1. 远火点降低到 400 km (在近火点点火减速)
        v_p_initial = math.sqrt(GM_MARS * (2.0 / rp_initial - 1.0 / a_initial))
        a_trans = (rp_initial + self.r_orbit) / 2.0
        v_p_trans = math.sqrt(GM_MARS * (2.0 / rp_initial - 1.0 / a_trans))
        delta_v1 = abs(v_p_initial - v_p_trans)

        # 2. 近火点抬升至 400 km (在远火点点火)
        v_a_trans = math.sqrt(GM_MARS * (2.0 / self.r_orbit - 1.0 / a_trans))
        v_a_final = math.sqrt(GM_MARS / self.r_orbit)
        delta_v2 = abs(v_a_final - v_a_trans)

        delta_v_propulsive_total = delta_v1 + delta_v2 # m/s

        # 齐奥尔科夫斯基火箭方程节省推进剂反演
        # 探测器干重 376 kg, 肼/四氧化二氮推进剂比冲 Isp ~ 310 s
        m_dry = 376.0 # kg
        isp = 310.0   # s
        g0 = 9.80665  # m/s^2
        # 若需额外提供 delta_v_propulsive_total, 需额外燃料:
        # m_extra = m_dry * (exp(delta_v / (isp * g0)) - 1)
        fuel_saved_kg = m_dry * (math.exp(delta_v_propulsive_total / (isp * g0)) - 1.0)

        return {
            "initial_apoapsis_km": 27000.0,
            "final_apoapsis_km": 400.0,
            "equivalent_delta_v_saved_ms": delta_v_propulsive_total,
            "propellant_saved_kg": fuel_saved_kg,
            "aerobraking_duration_months": 3.0,
            "fuel_mass_ratio_saved_pct": (fuel_saved_kg / m_dry) * 100.0
        }

    def compute_grs_subsurface_ice_physics(self):
        """
        GRS (Gamma Ray Spectrometer) 伽马射线与中子谱仪水冰探测物理
        宇宙射线散裂中子减速与 2.223 MeV 氢捕获伽马特征
        """
        # 弹性碰撞最大动能转移分数: xi = 4 * M * m / (M + m)^2
        # 中子质量 m_n ~ 1 u, 靶核质量 M
        targets = {
            "Hydrogen (H-1)": 1.008,
            "Carbon (C-12)": 12.00,
            "Oxygen (O-16)": 16.00,
            "Silicon (Si-28)": 28.08,
            "Iron (Fe-56)": 55.85
        }
        energy_transfer_ratios = {}
        for elem, mass in targets.items():
            xi = (4.0 * mass * 1.008) / ((mass + 1.008)**2)
            energy_transfer_ratios[elem] = xi

        # 氢捕获伽马射线特征能量
        # n + p -> d + gamma (2.223 MeV)
        h_capture_gamma_mev = 2.2233

        # 极区浅表土壤富冰层参数 (Boynton et al. 2002)
        ice_depth_min_cm = 30.0 # 极区高纬(75°S)埋深仅 30 cm
        ice_depth_max_cm = 60.0 # 60°S 埋深约 60 cm
        ice_mass_fraction_min = 0.20 # 20%
        ice_mass_fraction_max = 0.50 # 50%
        ice_volume_fraction = 0.55   # 体积比 >50% ("冰中带土")

        # 估计地下水冰储量相当于密歇根湖 (Lake Michigan) 的两倍
        lake_michigan_volume_km3 = 4920.0
        equivalent_ice_volume_km3 = lake_michigan_volume_km3 * 2.0

        return {
            "h_capture_gamma_energy_mev": h_capture_gamma_mev,
            "energy_transfer_fraction_hydrogen": energy_transfer_ratios["Hydrogen (H-1)"],
            "energy_transfer_fraction_silicon": energy_transfer_ratios["Silicon (Si-28)"],
            "hydrogen_collision_efficiency_vs_silicon": energy_transfer_ratios["Hydrogen (H-1)"] / energy_transfer_ratios["Silicon (Si-28)"],
            "polar_ice_depth_range_cm": [ice_depth_min_cm, ice_depth_max_cm],
            "polar_ice_mass_fraction_range": [ice_mass_fraction_min, ice_mass_fraction_max],
            "polar_ice_volume_fraction_pct": ice_volume_fraction * 100.0,
            "equivalent_water_ice_volume_km3": equivalent_ice_volume_km3
        }

    def compute_themis_thermal_inertia_physics(self):
        """
        THEMIS 热辐射成像系统热惯量物理与矿物学
        Thermal Inertia I = sqrt(k * rho * c)
        """
        # 热惯量典型值 (J m^-2 K^-1 s^-1/2, 即 tiu)
        # 细尘: ~50, 粗砂: ~250, 固结岩石: ~1200+
        materials = {
            "Fine Dust / Silt": {"k": 0.02, "rho": 1200.0, "c": 700.0},
            "Coarse Sand / Regolith": {"k": 0.15, "rho": 1600.0, "c": 800.0},
            "Duricrust / Indurated Soil": {"k": 0.50, "rho": 1900.0, "c": 850.0},
            "Solid Basalt Bedrock": {"k": 2.20, "rho": 2800.0, "c": 900.0}
        }
        ti_results = {}
        for mat, p in materials.items():
            I = math.sqrt(p["k"] * p["rho"] * p["c"])
            ti_results[mat] = round(I, 1)

        # THEMIS 光学波段
        ir_bands_count = 9    # 6.78 ~ 14.88 um
        vis_bands_count = 5   # 425 ~ 860 nm
        spatial_res_ir_m = 100.0 # 100 m/pixel
        spatial_res_vis_m = 18.0 # 18 m/pixel

        return {
            "thermal_inertia_tiu": ti_results,
            "ir_bands_count": ir_bands_count,
            "vis_bands_count": vis_bands_count,
            "spatial_resolution_ir_m": spatial_res_ir_m,
            "spatial_resolution_vis_m": spatial_res_vis_m,
            "major_mineral_discovery": "Olivine-rich basalts & Chloride salt deposits"
        }

    def get_martian_hexad_matrix(self):
        """
        火星现役六大金刚 (The Martian Hexad / Sextet) 协同体系
        """
        return [
            {
                "name": "2001 火星奥德赛号 (Mars Odyssey, NASA)",
                "year_arrived": 2001,
                "type": "Orbiter",
                "orbit_type": "Sun-synchronous Near-Polar (400 km circular)",
                "core_science": "GRS 伽马中子谱仪浅表水冰发现、THEMIS 全球热惯量与矿物图、首代表面中继基站",
                "lifespan_years": 25.0,
                "status": "连续在轨 25 周年银禧！绕火 103,000+ 圈历史纪录"
            },
            {
                "name": "火星快车号 (Mars Express, ESA)",
                "year_arrived": 2003,
                "type": "Orbiter",
                "orbit_type": "Quasi-polar Eccentric (340 x 10,100 km, 穿透火卫一)",
                "core_science": "MARSIS 5km 穿地雷达、火卫一 45km 飞掠碎石堆测地、OMEGA 三大水成纪元、HRSC 3D 全图",
                "lifespan_years": 22.8,
                "status": "欧洲最长寿深空功勋旗舰，服役超 23 载"
            },
            {
                "name": "火星勘测轨道飞行器 (MRO, NASA)",
                "year_arrived": 2006,
                "type": "Orbiter",
                "orbit_type": "Sun-synchronous Frozen Polar (255 x 320 km)",
                "core_science": "HiRISE 30cm 光学微观极限、SHARAD 1km 浅层探冰、Electra 巡视器 80% 通信中继骨干",
                "lifespan_years": 20.6,
                "status": "在轨 20 周年，回传超 56.8 TB 科学数据"
            },
            {
                "name": "好奇号火星车 (Curiosity / MSL, NASA)",
                "year_arrived": 2012,
                "type": "Rover",
                "orbit_type": "Surface (Gale Crater / Mount Sharp)",
                "core_science": "盖尔撞击坑夏普山麓漫游 33.6km、盖迪兹谷单质硫晶体突破、MMRTG 同位素供电",
                "lifespan_years": 14.2,
                "status": "在轨巡航超 14 年，行驶突破 33.6 km"
            },
            {
                "name": "毅力号火星车 (Perseverance, NASA)",
                "year_arrived": 2021,
                "type": "Rover",
                "orbit_type": "Surface (Jezero Crater Rim / Wild West)",
                "core_science": "500m 环壁攀爬进入狂野西部、生成式 AI 导航、33 支古原生岩芯密封、MOXIE 制氧",
                "lifespan_years": 5.7,
                "status": "登顶杰泽罗环壁，原位探索 40 亿年前古地壳"
            },
            {
                "name": "天问一号环绕器 (Tianwen-1, CNSA)",
                "year_arrived": 2021,
                "type": "Orbiter",
                "orbit_type": "Polar Elliptical Remote Sensing (265 x 10,700 km)",
                "core_science": "76m 全球彩色正射影像底图、MOSIR 百米地下雷达探冰、3I/ATLAS 星际彗星极限成像",
                "lifespan_years": 5.7,
                "status": "极轨遥感巡天，3.5 TB 数据全球开放"
            }
        ]

    def get_grand_septemvigintet_fleet(self):
        """
        2026 人类深空二十七极黄金舰队 (The Grand Septemvigintet) 宏伟时空矩阵
        严格按日心极距降序排列
        """
        fleet = [
            {"rank": 1, "name": "旅行者 1 号 (Voyager 1, NASA)", "heliocentric_dist_au": 173.22, "role": "最远恒星际边界极 (1 光日冲线倒计时 31 天)"},
            {"rank": 2, "name": "旅行者 2 号 (Voyager 2, NASA)", "heliocentric_dist_au": 144.29, "role": "恒星际南天天球星际极 (今日凌晨刚破 20 光时大关！)"},
            {"rank": 3, "name": "新视野号 (New Horizons, NASA)", "heliocentric_dist_au": 65.92, "role": "柯伊伯带双曲线逃逸极 (COB 绝尘暗夜超额光)"},
            {"rank": 4, "name": "朱诺号 (Juno, NASA)", "heliocentric_dist_au": 5.20, "role": "木星极轨高能辐射极 (钛金保险库，PJ89 倒计时 26 天)"},
            {"rank": 5, "name": "木星冰月探测器 (JUICE, ESA)", "heliocentric_dist_au": 5.20, "role": "巨行星卫星内禀磁层极 (奔木共振巡航，探秘木卫三深海)"},
            {"rank": 6, "name": "欧罗巴快船 (Europa Clipper, NASA)", "heliocentric_dist_au": 5.20, "role": "外行星木卫二深海生命极 (MEGA 地球引力弹弓倒计时 46 天)"},
            {"rank": 7, "name": "露西号 (Lucy, NASA)", "heliocentric_dist_au": 5.04, "role": "木星特洛伊群原始微行星极 (7.3m UltraFlex 折叠帆板，发射五周年)"},
            {"rank": 8, "name": "灵神星探测器 (Psyche, NASA)", "heliocentric_dist_au": 2.042, "role": "金属核心微行星极 (SPT-140 霍尔电推，DSOC 激光光子链路)"},
            {"rank": 9, "name": "2001 火星奥德赛号 (Mars Odyssey, NASA)", "heliocentric_dist_au": 1.579, "role": "行星在轨连续服役最长世界纪录极 (连续在轨 25 周年银禧倒计时 6 天！绕火 10.3 万圈)"},
            {"rank": 10, "name": "火星快车号 (Mars Express, ESA)", "heliocentric_dist_au": 1.579, "role": "火星 23 年地下雷达与火卫一穿越极 (MARSIS 5km 探地、火卫一 45km 飞掠碎石堆)"},
            {"rank": 11, "name": "好奇号火星车 (Curiosity, NASA)", "heliocentric_dist_au": 1.524, "role": "火星盖尔坑夏普山麓极 (14 年漫游 33.6km，盖迪兹谷纯单质硫突破)"},
            {"rank": 12, "name": "毅力号火星车 (Perseverance, NASA)", "heliocentric_dist_au": 1.524, "role": "火星古湖泊与原生古地壳原位探测极 (500m 环壁登顶狂野西部，生成式 AI 导航)"},
            {"rank": 13, "name": "天问一号环绕器 (Tianwen-1, CNSA)", "heliocentric_dist_au": 1.524, "role": "火星极轨全域遥感极 (76m 全球彩色正射图，MOSIR 百米雷达，3I/ATLAS 星际观测)"},
            {"rank": 14, "name": "火星勘测轨道器 (MRO, NASA)", "heliocentric_dist_au": 1.524, "role": "火星超分对焦与深空信息中枢极 (HiRISE 30cm 光学极限、SHARAD 探冰、80% 中继)"},
            {"rank": 15, "name": "赫拉号 (Hera, ESA)", "heliocentric_dist_au": 1.304, "role": "双小行星微重力伴飞极 (BRM-1 93 分钟主减速点火圆满达成)"},
            {"rank": 16, "name": "隼鸟二号 (Hayabusa2# / SHARP, JAXA)", "heliocentric_dist_au": 1.120, "role": "十米级超快自转微小行星极 (744m Torifune 掠飞后巡航，490 倍离心力)"},
            {"rank": 17, "name": "OSIRIS-APEX (NASA)", "heliocentric_dist_au": 1.010, "role": "毁神星伴飞与极限热控无花果叶极 (4 倍太阳热流，2029 掠地 1153km 减速 99%)"},
            {"rank": 18, "name": "詹姆斯·韦伯望远镜 (JWST, NASA/ESA/CSA)", "heliocentric_dist_au": 1.010, "role": "日地虚空 L2 天文极 (6.5m 铍金镜，300 K 隔热 6.7 K 制冷，捕获 z>14 原初星系)"},
            {"rank": 19, "name": "欧几里得空间望远镜 (Euclid, ESA)", "heliocentric_dist_au": 1.010, "role": "日地 L2 暗宇宙与宇宙网宏观极 (1.2m SiC TMA，0.53 deg² 巨视场，6.09 亿像素 VIS)"},
            {"rank": 20, "name": "天问二号 (Tianwen-2, CNSA)", "heliocentric_dist_au": 1.001, "role": "地球准卫星共轨采样与彗星双跃迁极 (28 分钟自旋 50 倍离心力对抗采样)"},
            {"rank": 21, "name": "鹊桥二号 (Queqiao-2, CNSA)", "heliocentric_dist_au": 1.000, "role": "地月空间与月球南极/月背冻结中继极 (地心距 38.44 万公里，4.2m 伞天线)"},
            {"rank": 22, "name": "嫦娥四号与玉兔二号 (Chang'e-4 / Yutu-2, CNSA)", "heliocentric_dist_au": 1.000, "role": "月球背面原位巡视极 (地心距 38.44 万公里，人类唯一月背软着陆、96 月昼 7.79 年)"},
            {"rank": 23, "name": "太阳和日球层天文台 (SOHO, ESA/NASA)", "heliocentric_dist_au": 0.990, "role": "日地 L1 向日日冕哨兵极 (地心距 149 万公里，30 年守望三轮太阳周，5200 颗彗星)"},
            {"rank": 24, "name": "日地关系天文台 (STEREO-A, NASA)", "heliocentric_dist_au": 0.962, "role": "日心超前漂移轨道 3D CME 立体极 (20 周年里程碑，太阳远背面 5.2 天超前预警)"},
            {"rank": 25, "name": "贝皮可伦坡 (BepiColombo, ESA/JAXA)", "heliocentric_dist_au": 0.387, "role": "太阳最深引力势能阱水星捕获极 (-1405 MJ/kg MOI 盲操倒计时 34 天)"},
            {"rank": 26, "name": "太阳轨道飞行器 (Solar Orbiter, ESA/NASA)", "heliocentric_dist_au": 0.280, "role": "黄道外高倾角极区成像极 (520°C 骨黑热障，微耀斑篝火，平安夜 VGA5 倒计时 67 天)"},
            {"rank": 27, "name": "帕克太阳探测器 (Parker Solar Probe, NASA)", "heliocentric_dist_au": 0.046, "role": "恒星日冕极高温炼狱原位极 (192 km/s 人类极速，1400°C 防热罩，P30 倒计时 45 天)"}
        ]

        # 极端物理指标
        min_au = fleet[-1]["heliocentric_dist_au"]
        max_au = fleet[0]["heliocentric_dist_au"]
        ratio_dist = max_au / min_au
        ratio_flux = (max_au / min_au)**2

        return {
            "fleet_size": len(fleet),
            "fleet": fleet,
            "extreme_ratios": {
                "max_heliocentric_au": max_au,
                "min_heliocentric_au": min_au,
                "distance_ratio": ratio_dist,
                "solar_flux_ratio": ratio_flux
            }
        }

if __name__ == "__main__":
    engine = MarsOdysseyEngine()
    tl = engine.compute_mission_timeline()
    od = engine.compute_orbit_dynamics()
    ab = engine.compute_aerobraking_physics()
    grs = engine.compute_grs_subsurface_ice_physics()
    th = engine.compute_themis_thermal_inertia_physics()
    hexad = engine.get_martian_hexad_matrix()
    fleet = engine.get_grand_septemvigintet_fleet()

    print("=== 2001 火星奥德赛号 (2001 Mars Odyssey) 在轨 25 周年银禧推演 ===")
    print(f"在轨时间: {tl['days_in_orbit']:.1f} 天 ({tl['years_in_orbit']:.2f} 地球年 / {tl['mars_years_in_orbit']:.2f} 火星年)")
    print(f"25 周年倒计时: {tl['countdown_to_25y_days']:.2f} 天 ({tl['countdown_to_25y_hours']:.1f} 小时)")
    print(f"制图轨道: 高度 {od['orbital_altitude_km']:.1f} km, 速度 {od['orbital_velocity_kms']:.3f} km/s, 周期 {od['period_minutes']:.2f} 分钟")
    print(f"每日绕火: {od['orbits_per_earth_day']:.2f} 圈, 累计绕火公转: {od['cumulative_orbits']:.0f} 圈 (超十万圈历史纪录!)")
    print(f"气动减速节省推进剂: {ab['propellant_saved_kg']:.1f} kg (等效 Delta-V {ab['equivalent_delta_v_saved_ms']:.1f} m/s)")
    print(f"GRS 浅表水冰: 2.223 MeV 氢俘获伽马线, 极区地下 30~60cm 水冰质量比 {grs['polar_ice_mass_fraction_range'][0]*100}%~{grs['polar_ice_mass_fraction_range'][1]*100}%, 体积比 >50%")
    print(f"THEMIS 热惯量制图: 细尘 {th['thermal_inertia_tiu']['Fine Dust / Silt']} tiu vs 基岩 {th['thermal_inertia_tiu']['Solid Basalt Bedrock']} tiu")
    print(f"火星现役六大金刚 (Martian Hexad): 共 {len(hexad)} 大航天器")
    print(f"2026 人类深空黄金舰队: 扩充至二十七极 (The Grand Septemvigintet, {fleet['fleet_size']} 艘深空器)")
    print(f"极距跨度: {fleet['extreme_ratios']['distance_ratio']:.1f} 倍, 辐射落差: {fleet['extreme_ratios']['solar_flux_ratio']:.0f} 倍")
