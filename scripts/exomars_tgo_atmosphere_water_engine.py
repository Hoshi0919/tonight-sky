"""
ExoMars 痕量气体轨道器 (ExoMars Trace Gas Orbiter, TGO) 在轨环绕 10 周年整（十年锡婚 / Decennial）、
NOMAD 与 ACS 太阳掩星 50 pptv 甲烷检测极限与火星甲烷对立佯谬、
人类首次发现火星氯化氢 (HCl) 气体与卤素光化学循环、
FREND 准直超热中子望远镜与水手号大峡谷 40% 水冰绿洲、
火星现役七大功勋金刚 (The Martian Septet) 与 2026 人类深空二十八极黄金舰队 (The Grand Octovigintet / 深空二十八宿) 推演引擎
"""

import math
import datetime

# 基础物理与天体常数
SPEED_OF_LIGHT = 299792458.0  # m/s
AU_METERS = 149597870700.0   # 1 AU in meters
SOLAR_CONSTANT_1AU = 1361.0  # W/m^2 at 1 AU
G_CONST = 6.67430e-11        # m^3 / (kg s^2)

# 火星物理常数
GM_MARS = 4.282837e13         # m^3/s^2 (G * M_mars)
R_MARS = 3389.5e3             # m (Mars mean volumetric radius, 3389.5 km)
MASS_MARS = 6.4171e23         # kg
MARS_SOL_SECONDS = 88775.244  # 1 sol = 24h 39m 35.244s
MARS_SCALE_HEIGHT = 11.1e3    # m (火星大气标高 ~11.1 km)

class ExoMarsTGOEngine:
    """
    ExoMars TGO 在轨 10 周年动力学、大气化学、水冰反演、火星七金刚与深空二十八宿矩阵
    """
    def __init__(self, current_dt=None):
        if current_dt is None:
            # 默认评估历元：2026-10-18 08:45:00 CST (00:45:00 UTC)
            self.current_dt = datetime.datetime(2026, 10, 18, 0, 45, tzinfo=datetime.timezone.utc)
        else:
            self.current_dt = current_dt

        # 关键历史与科学历元
        self.launch_dt = datetime.datetime(2016, 3, 14, 9, 31, 0, tzinfo=datetime.timezone.utc)
        self.schiaparelli_sep_dt = datetime.datetime(2016, 10, 16, 14, 42, 0, tzinfo=datetime.timezone.utc)
        self.moi_dt = datetime.datetime(2016, 10, 19, 15, 24, 0, tzinfo=datetime.timezone.utc) # Mars Orbit Insertion
        self.anniversary_10y_dt = datetime.datetime(2026, 10, 19, 15, 24, 0, tzinfo=datetime.timezone.utc)

        # 标称科学制图轨道参数 (Circular Sun-synchronous-like High-inclination Orbit)
        self.h_orbit = 400.0e3        # 标称工作轨道平均高度 400 km
        self.r_orbit = R_MARS + self.h_orbit # 3789.5 km
        self.inclination_deg = 74.0   # 74度高倾角（覆盖全纬度与局部时掩星）
        self.eccentricity = 0.005     # 近圆轨道

    def compute_mission_timeline(self):
        """
        计算任务时间线与 10 周年倒计时
        """
        flight_sec = (self.current_dt - self.launch_dt).total_seconds()
        orbit_sec = (self.current_dt - self.moi_dt).total_seconds()
        countdown_sec = (self.anniversary_10y_dt - self.current_dt).total_seconds()

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
            "countdown_to_10y_days": countdown_days,
            "countdown_to_10y_hours": countdown_hours,
            "is_decennial_eve": 0 <= countdown_hours <= 48.0
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
            "cumulative_orbits": total_orbits,
            "inclination_deg": self.inclination_deg
        }

    def compute_aerobraking_physics(self):
        """
        气动减速 (Aerobraking) 物理与推进剂节省模型
        TGO 历时近一年通过 950 余次大气掠飞将 4 日椭圆轨压制为 400km 圆轨
        """
        # 初始捕获大椭圆轨道: 346 km x 98,000 km (周期 ~4 天)
        rp_init = R_MARS + 346.0e3   # 3735.5 km
        ra_init = R_MARS + 98000.0e3 # 101389.5 km
        a_init = (rp_init + ra_init) / 2.0

        # 近火点速度
        vp_init = math.sqrt(GM_MARS * (2.0 / rp_init - 1.0 / a_init))
        # 400km 圆轨道速度
        r_target = R_MARS + 400.0e3
        v_target_circ = math.sqrt(GM_MARS / r_target)

        # 远火点降低至 400km 后的椭圆过渡轨 (346km x 400km)
        a_trans = (rp_init + r_target) / 2.0
        vp_trans = math.sqrt(GM_MARS * (2.0 / rp_init - 1.0 / a_trans))

        # 气动减速所耗散的等效速度增量 (主要靠大气阻力在近火点剥蚀动能)
        delta_v_aerobraking = vp_init - vp_trans # m/s

        # 齐奥尔科夫斯基火箭方程计算节省的推进剂
        isp_sec = 310.0 # 标称单组元/双组元姿控主轨发动机比冲
        g0 = 9.80665
        dry_mass = 1532.0 # TGO 干重 (kg)

        # 若纯靠推进剂变轨所需燃料质量
        mass_fuel_saved = dry_mass * (math.exp(delta_v_aerobraking / (isp_sec * g0)) - 1.0)
        passes_count = 952 # 实际经历约 952 次气动掠飞
        avg_delta_v_per_pass = delta_v_aerobraking / passes_count

        return {
            "initial_apoapsis_km": 98000.0,
            "initial_periapsis_km": 346.0,
            "final_circular_altitude_km": 400.0,
            "vp_initial_kms": vp_init / 1e3,
            "vp_transition_kms": vp_trans / 1e3,
            "v_final_circ_kms": v_target_circ / 1e3,
            "equivalent_delta_v_saved_ms": delta_v_aerobraking,
            "equivalent_delta_v_saved_kms": delta_v_aerobraking / 1e3,
            "propellant_saved_kg": mass_fuel_saved,
            "aerobraking_passes": passes_count,
            "avg_delta_v_per_pass_ms": avg_delta_v_per_pass
        }

    def compute_solar_occultation_and_methane_paradox(self):
        """
        NOMAD 与 ACS 太阳掩星几何放大效应与火星甲烷对立佯谬物理
        """
        # 太阳掩星切向穿透火星大气的有效光程 L = 2 * sqrt(2 * R_mars * H)
        h_scale = MARS_SCALE_HEIGHT
        path_length_meters = 2.0 * math.sqrt(2.0 * R_MARS * h_scale)
        path_length_km = path_length_meters / 1e3

        # 天底观测大气等效垂直厚度约为 1 个标高 H
        optical_path_enhancement = path_length_meters / h_scale

        # 科学仪器灵敏度与探测下限
        tgo_methane_upper_limit_ppbv = 0.05 # 50 pptv (0.05 ppbv)
        curiosity_gale_crater_spike_ppbv = 21.0 # 好奇号在盖尔坑测得的局地脉冲峰值 21 ppbv
        methane_paradox_ratio = curiosity_gale_crater_spike_ppbv / tgo_methane_upper_limit_ppbv

        # 甲烷无局地汇时的光解寿命（通常认为为 300 年）
        nominal_photochemical_lifetime_years = 300.0

        return {
            "tangent_path_length_km": path_length_km,
            "optical_path_enhancement_factor": optical_path_enhancement,
            "tgo_methane_upper_limit_ppbv": tgo_methane_upper_limit_ppbv,
            "tgo_methane_upper_limit_pptv": tgo_methane_upper_limit_ppbv * 1000.0,
            "curiosity_gale_crater_spike_ppbv": curiosity_gale_crater_spike_ppbv,
            "methane_paradox_ratio": methane_paradox_ratio,
            "nominal_lifetime_years": nominal_photochemical_lifetime_years,
            "paradox_implication": "若无超快地表化学销毁汇或夜间行星边界层陷阱，21 ppbv 脉冲将在全球扩散形成 >1 ppbv 背景，与 TGO <0.05 ppbv 严苛观测截然对立"
        }

    def compute_hcl_and_water_escape_chemistry(self):
        """
        人类首次发现火星氯化氢 (HCl) 气体与同位素水汽逃逸模型
        """
        # 氯化氢观测特征
        hcl_abundance_range_ppbv = (0.5, 4.0)
        nominal_hcl_ppbv = 2.5
        dust_season_solar_longitude_deg = (250.0, 310.0) # 南半球夏至近火点沙尘暴活跃期

        # 水汽高空泵升与同位素分馏 (D/H)
        max_h2o_lofting_altitude_km = 80.0 # 大沙尘暴期间水汽突破冷阱上升到 80km 以上
        mars_dh_ratio_relative_to_vsmow = 5.5 # 火星现存水体 D/H 相对地球海水 VSMOW 的富集倍数 (5~6倍)

        # 瑞利蒸馏分馏模型：R / R0 = f^(alpha - 1)
        # alpha 为逃逸分馏因子（轻氢逃逸速率大于重氢氘）
        # 测得富集 5.5 倍意味着古代火星至少失去了 80%~90% 以上的原生全球等效水层 (GEL)
        estimated_water_loss_fraction = 1.0 - (1.0 / mars_dh_ratio_relative_to_vsmow)

        return {
            "hcl_abundance_range_ppbv": hcl_abundance_range_ppbv,
            "nominal_hcl_ppbv": nominal_hcl_ppbv,
            "active_ls_season": dust_season_solar_longitude_deg,
            "water_lofting_altitude_km": max_h2o_lofting_altitude_km,
            "dh_enrichment_vs_vsmow": mars_dh_ratio_relative_to_vsmow,
            "min_ancient_water_loss_fraction": estimated_water_loss_fraction
        }

    def compute_frend_candor_chaos_water_oasis(self):
        """
        FREND 准直超热中子望远镜与水手号大峡谷浅表水冰绿洲测算
        """
        # 准直套筒带来的空间分辨率跃升
        uncollimated_footprint_km = 400.0 # 传统无准直中子仪视场 ~400 km
        frend_collimated_footprint_km = 75.0 # FREND 准直后视场 ~60-100 km (标称 75km)
        spatial_resolution_improvement = uncollimated_footprint_km / frend_collimated_footprint_km

        # 坎多尔混沌区 (Candor Chaos) 水当量氢 (WEH)
        candor_chaos_weh_wt_percent = 40.0 # 质量百分比高达 40%
        equatorial_baseline_weh_wt_percent = 3.5 # 赤道基线含量 ~3%
        enrichment_factor = candor_chaos_weh_wt_percent / equatorial_baseline_weh_wt_percent

        # 绿洲水储量几何估算 (面积相当于荷兰 ~41,500 km^2，探测深度 1 米)
        oasis_area_km2 = 41500.0
        oasis_depth_m = 1.0
        regolith_bulk_density_kg_m3 = 1500.0 # 含冰风化层干容重
        total_regolith_mass_kg = (oasis_area_km2 * 1e6) * oasis_depth_m * regolith_bulk_density_kg_m3
        water_ice_mass_kg = total_regolith_mass_kg * (candor_chaos_weh_wt_percent / 100.0)
        water_ice_mass_tons = water_ice_mass_kg / 1000.0

        return {
            "uncollimated_footprint_km": uncollimated_footprint_km,
            "frend_collimated_footprint_km": frend_collimated_footprint_km,
            "resolution_gain_ratio": spatial_resolution_improvement,
            "candor_chaos_weh_wt_percent": candor_chaos_weh_wt_percent,
            "equatorial_baseline_weh_wt_percent": equatorial_baseline_weh_wt_percent,
            "water_enrichment_factor": enrichment_factor,
            "oasis_area_km2": oasis_area_km2,
            "oasis_depth_m": oasis_depth_m,
            "estimated_water_ice_tons": water_ice_mass_tons,
            "estimated_water_ice_billion_tons": water_ice_mass_tons / 1e9
        }

    def get_martian_septet_matrix(self):
        """
        2026 火星现役七大功勋金刚 (The Martian Septet) 协同体系
        由原六大金刚正式扩编为七大金刚矩阵
        """
        return [
            {
                "rank": 1,
                "name": "2001 火星奥德赛号 (Mars Odyssey, NASA)",
                "year_arrived": 2001,
                "type": "Orbiter",
                "orbit_type": "Sun-synchronous Frozen Polar (400 km)",
                "core_science": "GRS 伽马中子浅表水冰人类首探、THEMIS 全球热惯量、在轨 25 周年银禧世界纪录 (倒计时 6 天)",
                "lifespan_years": 25.0,
                "status": "现役行星在轨连续服役最长世界冠军"
            },
            {
                "rank": 2,
                "name": "火星快车号 (Mars Express, ESA)",
                "year_arrived": 2003,
                "type": "Orbiter",
                "orbit_type": "Near-polar Highly Elliptical (340 x 10,100 km)",
                "core_science": "MARSIS 5km 超深穿地雷达南极冰下湖、火卫一 45km 极近飞掠碎石堆测地学、OMEGA 三大水成纪元",
                "lifespan_years": 22.8,
                "status": "欧洲首个火星探测功勋旗舰，穿透火卫一轨道"
            },
            {
                "rank": 3,
                "name": "火星勘测轨道飞行器 (MRO, NASA)",
                "year_arrived": 2006,
                "type": "Orbiter",
                "orbit_type": "Sun-synchronous Frozen Polar (255 x 320 km)",
                "core_science": "HiRISE 30cm 光学微观极限、SHARAD 1km 浅层探冰、Electra 巡视器 80% 通信中继骨干",
                "lifespan_years": 20.6,
                "status": "在轨 20 周年，回传超 56.8 TB 科学数据"
            },
            {
                "rank": 4,
                "name": "好奇号火星车 (Curiosity / MSL, NASA)",
                "year_arrived": 2012,
                "type": "Rover",
                "orbit_type": "Surface (Gale Crater / Mount Sharp)",
                "core_science": "盖尔撞击坑夏普山麓漫游 33.6km、盖迪兹谷单质硫晶体突破、MMRTG 同位素供电",
                "lifespan_years": 14.2,
                "status": "在轨巡航超 14 年，行驶突破 33.6 km"
            },
            {
                "rank": 5,
                "name": "ExoMars 痕量气体轨道器 (TGO, ESA/Roscosmos)",
                "year_arrived": 2016,
                "type": "Orbiter",
                "orbit_type": "Circular Polar Mapping (400 km, 74° inc)",
                "core_science": "NOMAD/ACS 50 pptv 甲烷检测极限、人类首次确证火星 HCl 气体、FREND 40% 水手峡谷水冰绿洲、CaSSIS 4.6m 四色立体成像",
                "lifespan_years": 10.0,
                "status": "在轨 10 周年整（十年锡婚 / Decennial 冲线倒计时 14.6 小时）"
            },
            {
                "rank": 6,
                "name": "毅力号火星车 (Perseverance, NASA)",
                "year_arrived": 2021,
                "type": "Rover",
                "orbit_type": "Surface (Jezero Crater Rim / Wild West)",
                "core_science": "500m 环壁攀爬进入狂野西部、生成式 AI 导航、33 支古原生岩芯密封、MOXIE 制氧",
                "lifespan_years": 5.7,
                "status": "登顶杰泽罗环壁，原位探索 40 亿年前古地壳"
            },
            {
                "rank": 7,
                "name": "天问一号环绕器 (Tianwen-1, CNSA)",
                "year_arrived": 2021,
                "type": "Orbiter",
                "orbit_type": "Polar Elliptical Remote Sensing (265 x 10,700 km)",
                "core_science": "76m 全球彩色正射影像底图、MOSIR 百米地下雷达探冰、3I/ATLAS 星际彗星极限成像",
                "lifespan_years": 5.7,
                "status": "极轨遥感巡天，3.5 TB 数据全球开放"
            }
        ]

    def get_grand_octovigintet_fleet(self):
        """
        2026 人类深空二十八极黄金舰队 (The Grand Octovigintet / 深空二十八宿) 宏伟时空矩阵
        严格按日心极距降序排列，完美对齐华夏二十八宿天象
        """
        fleet = [
            {"rank": 1, "name": "旅行者 1 号 (Voyager 1, NASA)", "heliocentric_dist_au": 173.22, "mansion": "角宿 (东宫苍龙第一宿)", "role": "最远恒星际边界极 (1 光日冲线倒计时 31 天)"},
            {"rank": 2, "name": "旅行者 2 号 (Voyager 2, NASA)", "heliocentric_dist_au": 144.29, "mansion": "亢宿 (东宫苍龙第二宿)", "role": "恒星际南天天球星际极 (今日凌晨刚破 20 光时大关！)"},
            {"rank": 3, "name": "新视野号 (New Horizons, NASA)", "heliocentric_dist_au": 65.92, "mansion": "氐宿 (东宫苍龙第三宿)", "role": "柯伊伯带双曲线逃逸极 (COB 绝尘暗夜超额光)"},
            {"rank": 4, "name": "朱诺号 (Juno, NASA)", "heliocentric_dist_au": 5.20, "mansion": "房宿 (东宫苍龙第四宿)", "role": "木星极轨高能辐射极 (钛金保险库，PJ89 倒计时 26 天)"},
            {"rank": 5, "name": "木星冰月探测器 (JUICE, ESA)", "heliocentric_dist_au": 5.20, "mansion": "心宿 (东宫苍龙第五宿)", "role": "巨行星卫星内禀磁层极 (奔木共振巡航，探秘木卫三深海)"},
            {"rank": 6, "name": "欧罗巴快船 (Europa Clipper, NASA)", "heliocentric_dist_au": 5.20, "mansion": "尾宿 (东宫苍龙第六宿)", "role": "外行星木卫二深海生命极 (MEGA 地球引力弹弓倒计时 46 天)"},
            {"rank": 7, "name": "露西号 (Lucy, NASA)", "heliocentric_dist_au": 5.04, "mansion": "箕宿 (东宫苍龙第七宿)", "role": "木星特洛伊群原始微行星极 (7.3m UltraFlex 折叠帆板，发射五周年)"},
            {"rank": 8, "name": "灵神星探测器 (Psyche, NASA)", "heliocentric_dist_au": 2.042, "mansion": "斗宿 (北宫玄武第一宿)", "role": "金属核心微行星极 (SPT-140 霍尔电推，DSOC 激光光子链路)"},
            {"rank": 9, "name": "2001 火星奥德赛号 (Mars Odyssey, NASA)", "heliocentric_dist_au": 1.579, "mansion": "牛宿 (北宫玄武第二宿)", "role": "行星在轨服役世界纪录极 (连续在轨 25 周年银禧倒计时 6 天！绕火 11.1 万圈)"},
            {"rank": 10, "name": "火星快车号 (Mars Express, ESA)", "heliocentric_dist_au": 1.579, "mansion": "女宿 (北宫玄武第三宿)", "role": "火星 23 年地下雷达与火卫一穿越极 (MARSIS 5km 探地、火卫一 45km 飞掠碎石堆)"},
            {"rank": 11, "name": "ExoMars 痕量气体轨道器 (TGO, ESA/Roscosmos)", "heliocentric_dist_au": 1.579, "mansion": "虚宿 (北宫玄武第四宿)", "role": "火星大气痕量气体与浅表水冰极 (在轨 10 周年整锡婚冲线！NOMAD/ACS 50 pptv 极限、HCl 首探、水手峡谷 40% 水冰绿洲)"},
            {"rank": 12, "name": "好奇号火星车 (Curiosity, NASA)", "heliocentric_dist_au": 1.524, "mansion": "危宿 (北宫玄武第五宿)", "role": "火星盖尔坑夏普山麓极 (14 年漫游 33.6km，盖迪兹谷纯单质硫突破)"},
            {"rank": 13, "name": "毅力号火星车 (Perseverance, NASA)", "heliocentric_dist_au": 1.524, "mansion": "室宿 (北宫玄武第六宿)", "role": "火星古湖泊与原生古地壳原位探测极 (500m 环壁登顶狂野西部，生成式 AI 导航)"},
            {"rank": 14, "name": "天问一号环绕器 (Tianwen-1, CNSA)", "heliocentric_dist_au": 1.524, "mansion": "壁宿 (北宫玄武第七宿)", "role": "火星极轨全域遥感极 (76m 全球彩色正射图，MOSIR 百米雷达，3I/ATLAS 星际观测)"},
            {"rank": 15, "name": "火星勘测轨道器 (MRO, NASA)", "heliocentric_dist_au": 1.524, "mansion": "奎宿 (西宫白虎第一宿)", "role": "火星超分对焦与深空信息中枢极 (HiRISE 30cm 光学极限、SHARAD 探冰、80% 中继)"},
            {"rank": 16, "name": "赫拉号 (Hera, ESA)", "heliocentric_dist_au": 1.304, "mansion": "娄宿 (西宫白虎第二宿)", "role": "双小行星微重力伴飞极 (BRM-1 93 分钟主减速点火圆满达成)"},
            {"rank": 17, "name": "隼鸟二号 (Hayabusa2# / SHARP, JAXA)", "heliocentric_dist_au": 1.120, "mansion": "胃宿 (西宫白虎第三宿)", "role": "十米级超快自转微小行星极 (744m Torifune 掠飞后巡航，490 倍离心力)"},
            {"rank": 18, "name": "OSIRIS-APEX (NASA)", "heliocentric_dist_au": 1.010, "mansion": "昴宿 (西宫白虎第四宿)", "role": "毁神星伴飞与极限热控无花果叶极 (4 倍太阳热流，2029 掠地 1153km 减速 99%)"},
            {"rank": 19, "name": "詹姆斯·韦伯望远镜 (JWST, NASA/ESA/CSA)", "heliocentric_dist_au": 1.010, "mansion": "毕宿 (西宫白虎第五宿)", "role": "日地虚空 L2 天文极 (6.5m 铍金镜，300 K 隔热 6.7 K 制冷，捕获 z>14 原初星系)"},
            {"rank": 20, "name": "欧几里得空间望远镜 (Euclid, ESA)", "heliocentric_dist_au": 1.010, "mansion": "觜宿 (西宫白虎第六宿)", "role": "日地 L2 暗宇宙与宇宙网宏观极 (1.2m SiC TMA，0.53 deg² 巨视场，6.09 亿像素 VIS)"},
            {"rank": 21, "name": "天问二号 (Tianwen-2, CNSA)", "heliocentric_dist_au": 1.001, "mansion": "参宿 (西宫白虎第七宿)", "role": "地球准卫星共轨采样与彗星双跃迁极 (28 分钟自旋 50 倍离心力对抗采样)"},
            {"rank": 22, "name": "鹊桥二号 (Queqiao-2, CNSA)", "heliocentric_dist_au": 1.000, "mansion": "井宿 (南宫朱雀第一宿)", "role": "地月空间与月球南极/月背冻结中继极 (地心距 38.44 万公里，4.2m 伞天线)"},
            {"rank": 23, "name": "嫦娥四号与玉兔二号 (Chang'e-4 / Yutu-2, CNSA)", "heliocentric_dist_au": 1.000, "mansion": "鬼宿 (南宫朱雀第二宿)", "role": "月球背面原位巡视极 (地心距 38.44 万公里，人类唯一月背软着陆、96 月昼 7.79 年)"},
            {"rank": 24, "name": "太阳和日球层天文台 (SOHO, ESA/NASA)", "heliocentric_dist_au": 0.990, "mansion": "柳宿 (南宫朱雀第三宿)", "role": "日地 L1 向日日冕哨兵极 (地心距 149 万公里，30 年守望三轮太阳周，5200 颗彗星)"},
            {"rank": 25, "name": "日地关系天文台 (STEREO-A, NASA)", "heliocentric_dist_au": 0.962, "mansion": "星宿 (南宫朱雀第四宿)", "role": "日心超前漂移轨道 3D CME 立体极 (20 周年里程碑，太阳远背面 5.2 天超前预警)"},
            {"rank": 26, "name": "贝皮可伦坡 (BepiColombo, ESA/JAXA)", "heliocentric_dist_au": 0.387, "mansion": "张宿 (南宫朱雀第五宿)", "role": "太阳最深引力势能阱水星捕获极 (-1405 MJ/kg MOI 盲操倒计时 34 天)"},
            {"rank": 27, "name": "太阳轨道飞行器 (Solar Orbiter, ESA/NASA)", "heliocentric_dist_au": 0.280, "mansion": "翼宿 (南宫朱雀第六宿)", "role": "黄道外高倾角极区成像极 (520°C 骨黑热障，微耀斑篝火，平安夜 VGA5 倒计时 67 天)"},
            {"rank": 28, "name": "帕克太阳探测器 (Parker Solar Probe, NASA)", "heliocentric_dist_au": 0.046, "mansion": "轸宿 (南宫朱雀第七宿)", "role": "恒星日冕极高温炼狱原位极 (192 km/s 人类极速，1400°C 防热罩，P30 倒计时 45 天)"}
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
    engine = ExoMarsTGOEngine()
    tl = engine.compute_mission_timeline()
    od = engine.compute_orbit_dynamics()
    ab = engine.compute_aerobraking_physics()
    meth = engine.compute_solar_occultation_and_methane_paradox()
    hcl = engine.compute_hcl_and_water_escape_chemistry()
    frend = engine.compute_frend_candor_chaos_water_oasis()
    septet = engine.get_martian_septet_matrix()
    octo = engine.get_grand_octovigintet_fleet()

    print("=== ExoMars 痕量气体轨道器 (TGO) 在轨 10 周年整推演 ===")
    print(f"在轨服役: {tl['days_in_orbit']:.1f} 天 ({tl['years_in_orbit']:.2f} 地球年 / {tl['mars_years_in_orbit']:.2f} 火星年)")
    print(f"10周年倒计时: {tl['countdown_to_10y_hours']:.1f} 小时 (是否处于10周年冲线前夕: {tl['is_decennial_eve']})")
    print(f"工作轨道: 高度 {od['orbital_altitude_km']:.1f} km, 倾角 {od['inclination_deg']}°, 速度 {od['orbital_velocity_kms']:.3f} km/s, 周期 {od['period_minutes']:.2f} min, 累计公转 {od['cumulative_orbits']:.0f} 圈")
    print(f"气动减速: 经历 {ab['aerobraking_passes']} 次掠飞, 节省等效速度增量 {ab['equivalent_delta_v_saved_ms']:.1f} m/s, 节省推进剂 {ab['propellant_saved_kg']:.1f} kg")
    print(f"太阳掩星切向光程: {meth['tangent_path_length_km']:.1f} km (相对天底放大 {meth['optical_path_enhancement_factor']:.1f} 倍)")
    print(f"甲烷检测下限: < {meth['tgo_methane_upper_limit_pptv']:.1f} pptv (与好奇号峰值 21 ppbv 反差达 {meth['methane_paradox_ratio']:.0f} 倍)")
    print(f"氯化氢气体: 首次探测 {hcl['nominal_hcl_ppbv']} ppbv, 伴随沙尘暴与水汽逃逸 (D/H 富集 {hcl['dh_enrichment_vs_vsmow']} 倍)")
    print(f"FREND 水手峡谷水冰绿洲: WEH 高达 {frend['candor_chaos_weh_wt_percent']:.1f} wt%, 浅表表层 1m 水冰储量估计达 {frend['estimated_water_ice_billion_tons']:.1f} 亿吨")
    print(f"火星现役金刚规模: {len(septet)} 艘 (火星七大功勋金刚)")
    print(f"人类深空黄金舰队规模: {octo['fleet_size']} 艘 (深空二十八极 / 二十八宿矩阵, 极距跨度 {octo['extreme_ratios']['distance_ratio']:.2f} 倍)")
