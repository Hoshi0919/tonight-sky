"""
hayabusa2_sharp_micro_asteroid_dynamics_engine.py

隼鸟二号拓展任务 (Hayabusa2 Extended Mission / SHARP) 与 1998 KY26 超微型超快自转小行星动力学推演引擎。
涵盖：
1. 2026-07-05 98943 Torifune (2001 CC21) 744米极限掠飞 (5 km/s) 接触双小行星实测复盘；
2. 1998 KY26 (直径 11m, 自转 5.35min) 极端微重力、赤道 490倍离心力弹射与 8.1 Pa 内聚力物理；
3. 临界纬度 87.41° 与半径仅 24.9 cm 的极区重力庇护所 (Polar Sanctuary) 着陆力学；
4. 4台 μ10 微波离子发动机 30kg 氙推进剂齐奥尔科夫斯基 Δv 盈余 (1759.7 m/s vs 1090 m/s)；
5. 2026 人类深空十六极黄金舰队 (The Grand Sedecet) 全景矩阵与极端物理对偶。
"""

import math
from datetime import datetime, timezone, timedelta

# 天体物理与航天动力学基准常数
C_LIGHT = 299792458.0          # 真空光速 (m/s)
AU_METERS = 149597870700.0     # 1 天文单位 (m)
AU_KM = AU_METERS / 1000.0     # 1 AU (km)
G_CONST = 6.67430e-11          # 万有引力常数 (m^3 kg^-1 s^-2)
G0_ACCEL = 9.80665             # 地球标准重力加速度 (m/s^2)
SOLAR_CONSTANT_1AU = 1361.0    # 1 AU 太阳辐射通量 (W/m^2)


def get_hayabusa2_sharp_status(current_date_str="2026-10-16"):
    """
    计算隼鸟二号拓展任务 (SHARP) 当前巡航状态、里程碑经过天数与关键倒计时。
    """
    dt_current = datetime.strptime(current_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    
    # 历史里程碑
    dt_earth_depart = datetime(2020, 12, 6, tzinfo=timezone.utc)      # 地球返回舱分离并启航拓展任务
    dt_torifune_flyby = datetime(2026, 7, 5, tzinfo=timezone.utc)     # 98943 Torifune 极限飞掠
    
    # 未来关键节点
    dt_ega1 = datetime(2027, 12, 15, tzinfo=timezone.utc)             # 第一次地球重力助推 (EGA-1)
    dt_ega2 = datetime(2028, 6, 15, tzinfo=timezone.utc)              # 第二次地球重力助推 (EGA-2)
    dt_ky26_rendezvous = datetime(2031, 7, 15, tzinfo=timezone.utc)   # 1998 KY26 最终交会与极区着陆
    
    days_since_earth_depart = (dt_current - dt_earth_depart).total_seconds() / 86400.0
    days_since_torifune = (dt_current - dt_torifune_flyby).total_seconds() / 86400.0
    
    days_to_ega1 = (dt_ega1 - dt_current).total_seconds() / 86400.0
    days_to_ega2 = (dt_ega2 - dt_current).total_seconds() / 86400.0
    days_to_ky26 = (dt_ky26_rendezvous - dt_current).total_seconds() / 86400.0
    years_to_ky26 = days_to_ky26 / 365.25
    
    # 当前日心距离与状态估计
    heliocentric_dist_au = 1.120
    solar_flux = SOLAR_CONSTANT_1AU / (heliocentric_dist_au ** 2)
    
    return {
        "current_date": current_date_str,
        "phase": "Post-Torifune Interplanetary Cruise (E(A)EEA Trajectory)",
        "days_since_earth_depart": round(days_since_earth_depart, 1),
        "days_since_torifune_flyby": round(days_since_torifune, 1),
        "days_to_ega1": round(days_to_ega1, 1),
        "days_to_ega2": round(days_to_ega2, 1),
        "days_to_ky26_rendezvous": round(days_to_ky26, 1),
        "years_to_ky26_rendezvous": round(years_to_ky26, 2),
        "heliocentric_distance_au": heliocentric_dist_au,
        "solar_flux_w_m2": round(solar_flux, 2),
    }


def compute_torifune_flyby_metrics():
    """
    计算 2026-07-05 98943 Torifune (2001 CC21) 近距离飞掠实测物理参数。
    """
    closest_approach_m = 744.0
    relative_speed_km_s = 5.0
    dimension_x_m = 840.0
    dimension_y_m = 340.0
    mean_diameter_m = 540.0
    spectral_type = "Sq"
    rotation_period_h = 5.0215
    morphology = "Contact Binary (接触双小行星)"
    
    # 光学自主跟踪角速度峰值 (rad/s 与 deg/s)
    peak_angular_rate_rad_s = (relative_speed_km_s * 1000.0) / closest_approach_m
    peak_angular_rate_deg_s = math.degrees(peak_angular_rate_rad_s)
    
    return {
        "asteroid_name": "98943 Torifune (2001 CC21)",
        "flyby_date": "2026-07-05",
        "closest_approach_distance_m": closest_approach_m,
        "relative_speed_km_s": relative_speed_km_s,
        "morphology": morphology,
        "dimensions_m": f"{dimension_x_m} x {dimension_y_m}",
        "mean_diameter_m": mean_diameter_m,
        "spectral_type": spectral_type,
        "rotation_period_hours": rotation_period_h,
        "peak_tracking_angular_rate_deg_s": round(peak_angular_rate_deg_s, 2),
    }


def compute_1998_ky26_micro_asteroid_physics(radius_m=5.5, density_kg_m3=2800.0, spin_period_min=5.3516):
    """
    严密推演 1998 KY26 超微型超快自转小行星的重力、离心力、内聚力与极区重力庇护所。
    """
    diameter_m = 2.0 * radius_m
    volume_m3 = (4.0 / 3.0) * math.pi * (radius_m ** 3)
    mass_kg = volume_m3 * density_kg_m3
    
    # 表面万有引力 (赤道处纯引力加速度，未扣除离心力)
    surface_gravity_m_s2 = (G_CONST * mass_kg) / (radius_m ** 2)
    surface_gravity_um_s2 = surface_gravity_m_s2 * 1e6
    
    # 逃逸速度
    v_esc_m_s = math.sqrt(2.0 * G_CONST * mass_kg / radius_m)
    v_esc_mm_s = v_esc_m_s * 1000.0
    v_esc_cm_s = v_esc_m_s * 100.0
    
    # 自转角速度 (rad/s)
    spin_period_s = spin_period_min * 60.0
    omega_spin_rad_s = (2.0 * math.pi) / spin_period_s
    
    # 赤道离心加速度 (向外)
    a_centrifugal_equator_m_s2 = (omega_spin_rad_s ** 2) * radius_m
    a_centrifugal_equator_mm_s2 = a_centrifugal_equator_m_s2 * 1000.0
    
    # 赤道处离心加速度与万有引力之比
    centrifugal_to_gravity_ratio = a_centrifugal_equator_m_s2 / surface_gravity_m_s2
    
    # 内部维持不解体所需的临界抗拉内聚强度: Y* ~ 1/4 * rho * omega^2 * R^2
    cohesive_strength_pa = 0.25 * density_kg_m3 * (omega_spin_rad_s ** 2) * (radius_m ** 2)
    
    # 临界纬度计算：径向净重力 g_rad(phi) = g - omega^2 * R * cos^2(phi) >= 0
    cos2_phi_crit = surface_gravity_m_s2 / a_centrifugal_equator_m_s2
    cos_phi_crit = math.sqrt(cos2_phi_crit)
    phi_crit_rad = math.acos(cos_phi_crit)
    phi_crit_deg = math.degrees(phi_crit_rad)
    
    # 极区重力庇护所 (Polar Sanctuary) 空间尺度
    polar_sanctuary_radius_m = radius_m * cos_phi_crit
    polar_sanctuary_radius_cm = polar_sanctuary_radius_m * 100.0
    
    # 全球表面被离心力排斥的面积比例 (纬度区间 [-phi_crit, +phi_crit])
    repulsive_surface_fraction = math.sin(phi_crit_rad)
    repulsive_surface_percentage = repulsive_surface_fraction * 100.0
    
    # 极区稳定重力庇护所面积比例 (南极 + 北极)
    polar_sanctuary_surface_fraction = 1.0 - repulsive_surface_fraction
    polar_sanctuary_surface_percentage = polar_sanctuary_surface_fraction * 100.0
    
    # 各代表性纬度净径向加速度 (正值为指向小行星核心的有效引力，负值为向外弹射)
    def net_radial_accel(phi_deg):
        phi_r = math.radians(phi_deg)
        return surface_gravity_m_s2 - (omega_spin_rad_s ** 2) * radius_m * (math.cos(phi_r) ** 2)

    g_net_equator = net_radial_accel(0.0)      # 赤道 0°
    g_net_45deg = net_radial_accel(45.0)       # 中纬 45°
    g_net_80deg = net_radial_accel(80.0)       # 高纬 80°
    g_net_pole = net_radial_accel(90.0)        # 极点 90°
    
    return {
        "diameter_m": diameter_m,
        "radius_m": radius_m,
        "density_kg_m3": density_kg_m3,
        "mass_kg": mass_kg,
        "spin_period_min": spin_period_min,
        "spin_period_sec": round(spin_period_s, 2),
        "spin_rate_rad_s": omega_spin_rad_s,
        "surface_gravity_m_s2": surface_gravity_m_s2,
        "surface_gravity_um_s2": round(surface_gravity_um_s2, 3),
        "escape_velocity_mm_s": round(v_esc_mm_s, 2),
        "escape_velocity_cm_s": round(v_esc_cm_s, 3),
        "centrifugal_accel_equator_mm_s2": round(a_centrifugal_equator_mm_s2, 3),
        "centrifugal_to_gravity_ratio": round(centrifugal_to_gravity_ratio, 1),
        "required_cohesive_strength_pa": round(cohesive_strength_pa, 2),
        "critical_latitude_deg": round(phi_crit_deg, 2),
        "polar_sanctuary_radius_cm": round(polar_sanctuary_radius_cm, 1),
        "repulsive_surface_percentage": round(repulsive_surface_percentage, 2),
        "polar_sanctuary_surface_percentage": round(polar_sanctuary_surface_percentage, 3),
        "net_radial_accel_equator_mm_s2": round(g_net_equator * 1000.0, 3),
        "net_radial_accel_45deg_mm_s2": round(g_net_45deg * 1000.0, 3),
        "net_radial_accel_80deg_mm_s2": round(g_net_80deg * 1000.0, 3),
        "net_radial_accel_pole_um_s2": round(g_net_pole * 1e6, 3),
    }


def compute_hayabusa2_ion_propulsion_budget(wet_mass_kg=500.0, dry_mass_kg=470.0, isp_s=2900.0, delta_v_req_mps=1090.0):
    """
    推演 4台 μ10 微波 ECR 离子发动机工质消耗与速度增量储备余量。
    """
    propellant_mass_kg = wet_mass_kg - dry_mass_kg
    effective_exhaust_velocity = isp_s * G0_ACCEL
    delta_v_available_mps = effective_exhaust_velocity * math.log(wet_mass_kg / dry_mass_kg)
    delta_v_margin_mps = delta_v_available_mps - delta_v_req_mps
    margin_percentage = (delta_v_margin_mps / delta_v_req_mps) * 100.0
    
    total_thrust_n = 0.040
    max_accel_m_s2 = total_thrust_n / wet_mass_kg
    max_accel_um_s2 = max_accel_m_s2 * 1e6
    
    return {
        "wet_mass_kg": wet_mass_kg,
        "dry_mass_kg": dry_mass_kg,
        "xenon_propellant_kg": propellant_mass_kg,
        "specific_impulse_s": isp_s,
        "delta_v_available_mps": round(delta_v_available_mps, 1),
        "delta_v_available_km_s": round(delta_v_available_mps / 1000.0, 3),
        "delta_v_required_mps": delta_v_req_mps,
        "delta_v_margin_mps": round(delta_v_margin_mps, 1),
        "margin_percentage": round(margin_percentage, 1),
        "total_thrust_mn": total_thrust_n * 1000.0,
        "spacecraft_accel_um_s2": round(max_accel_um_s2, 2),
    }


def get_grand_sedecet_fleet_metrics():
    """
    构建 2026 人类深空十六极黄金舰队 (The Grand Sedecet) 宏伟时空矩阵。
    严格按日心距离降序排列。
    """
    fleet = [
        {
            "rank": 1,
            "name": "旅行者 1 号 (Voyager 1)",
            "agency": "NASA",
            "distance_au": 173.22,
            "region": "恒星际最远深空边界极",
            "focus": "1 光日冲线倒计时 (33天，11-18) · 2.7K 星际介质",
        },
        {
            "rank": 2,
            "name": "旅行者 2 号 (Voyager 2)",
            "agency": "NASA",
            "distance_au": 144.26,
            "region": "恒星际南天天球星际极",
            "focus": "20 光时冲线倒计时 (明日 10-17) · 唯一造访四大巨行星",
        },
        {
            "rank": 3,
            "name": "新视野号 (New Horizons)",
            "agency": "NASA",
            "distance_au": 65.92,
            "region": "柯伊伯带双曲线逃逸极",
            "focus": "宇宙光学背景 (COB) 绝尘暗夜 · PUI 减速 17%",
        },
        {
            "rank": 4,
            "name": "朱诺号 (Juno)",
            "agency": "NASA",
            "distance_au": 5.20,
            "region": "木星极轨高能辐射极",
            "focus": "180kg 钛金保险库 · 33天极轨掠木 57.8 km/s · 弱光光伏",
        },
        {
            "rank": 5,
            "name": "木星冰月探测器 (JUICE)",
            "agency": "ESA",
            "distance_au": 5.20,
            "region": "巨行星卫星内禀磁层极",
            "focus": "木卫三深海 · 85m² 弱光光伏 · 2.3年共振巡航",
        },
        {
            "rank": 6,
            "name": "欧罗巴快船 (Europa Clipper)",
            "agency": "NASA",
            "distance_au": 5.20,
            "region": "外行星木卫二深海生命极",
            "focus": "MEGA 火地借力 · 距 2026-12-04 地球飞掠仅 49 天",
        },
        {
            "rank": 7,
            "name": "露西号 (Lucy)",
            "agency": "NASA",
            "distance_au": 5.04,
            "region": "木星特洛伊群原始微行星极",
            "focus": "7.3m UltraFlex 折叠帆板 · 今日 10-16 发射五周年",
        },
        {
            "rank": 8,
            "name": "灵神星探测器 (Psyche)",
            "agency": "NASA",
            "distance_au": 2.042,
            "region": "金属核心微行星极",
            "focus": "SPT-140 霍尔电推 · DSOC 深空激光通信链路",
        },
        {
            "rank": 9,
            "name": "赫拉号 (Hera)",
            "agency": "ESA",
            "distance_au": 1.304,
            "region": "双小行星微重力伴飞极",
            "focus": "昨日 10-15 BRM-1 减速点火圆满 · 动能偏转实测",
        },
        {
            "rank": 10,
            "name": "隼鸟二号 (Hayabusa2# / SHARP)",
            "agency": "JAXA",
            "distance_au": 1.120,
            "region": "十米级超快自转微小行星极",
            "focus": "Torifune 744m掠飞后巡航 · 1998 KY26 极区着陆 · 490倍离心力对抗",
        },
        {
            "rank": 11,
            "name": "OSIRIS-APEX",
            "agency": "NASA",
            "distance_au": 1.010,
            "region": "毁神星伴飞与极限热控无花果叶极",
            "focus": "0.5 AU 极限耐热无花果叶姿态 · STIR 气体羽流星震吹扫",
        },
        {
            "rank": 12,
            "name": "詹姆斯·韦伯望远镜 (JWST)",
            "agency": "NASA/ESA/CSA",
            "distance_au": 1.010,
            "region": "日地虚空 L2 天文极",
            "focus": "300K 隔热 6.7K 制冷 · 捕获 z > 14 原初星系与深空暗夜",
        },
        {
            "rank": 13,
            "name": "天问二号 (Tianwen-2)",
            "agency": "CNSA",
            "distance_au": 1.001,
            "region": "地球准卫星共轨采样与彗星双跃迁极",
            "focus": "28分钟自旋 50倍离心力对抗采样 · 311P 彗星跃迁",
        },
        {
            "rank": 14,
            "name": "贝皮可伦坡 (BepiColombo)",
            "agency": "ESA/JAXA",
            "distance_au": 0.387,
            "region": "太阳最深引力势能阱水星捕获极",
            "focus": "-1405 MJ/kg MOI 盲操倒计时 37 天 · 倒计时水星交会",
        },
        {
            "rank": 15,
            "name": "太阳轨道飞行器 (Solar Orbiter)",
            "agency": "ESA/NASA",
            "distance_au": 0.280,
            "region": "黄道外高倾角极区成像与日冕加热极",
            "focus": "金星 4:3 借力 24° · 520°C 骨黑屏 · 平安夜 VGA5 倒计时 69 天",
        },
        {
            "rank": 16,
            "name": "帕克太阳探测器 (Parker Solar Probe)",
            "agency": "NASA",
            "distance_au": 0.046,
            "region": "恒星日冕极高温炼狱原位极",
            "focus": "192 km/s 人类极速 · 1400°C 防热屏 · P30 倒计时 48 天",
        },
    ]
    
    max_dist_au = fleet[0]["distance_au"]
    min_dist_au = fleet[-1]["distance_au"]
    dist_ratio = max_dist_au / min_dist_au
    solar_flux_ratio = dist_ratio ** 2
    
    return {
        "fleet_count": len(fleet),
        "fleet_name": "The Grand Sedecet (人类深空十六极黄金舰队)",
        "missions": fleet,
        "max_distance_au": max_dist_au,
        "min_distance_au": min_dist_au,
        "distance_span_ratio": round(dist_ratio, 1),
        "solar_flux_drop_ratio": round(solar_flux_ratio, 1),
    }
