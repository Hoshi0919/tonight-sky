"""
99942 Apophis (毁神星) 2029 年 4 月 13 日极限掠地天体力学推演引擎
========================================================================

涵盖:
1. 双曲线相遇开普勒轨道、地球引力弹弓 (Gravity Assist) 与渐近线偏转角 (Deflection Angle)
2. 轨道分类历史性跃迁: Aten 型 (阿登型) -> Apollo 型 (阿波罗型) 轨道根数突变
3. 洛希极限 (Roche Limit) 边界与碎石堆小行星 (Rubble Pile) 潮汐应力/星震 (Asteroid Quakes)
4. 地球同步静止卫星轨道 (GEO Belt) 穿越几何与轨道安全分析
5. 肉眼可见峰值视星等 (+3.1 等) 与极限超高速视运动 (42°~48°/h)
6. 华夏各大城市时空观测视窗与全球探测舰队 (OSIRIS-APEX / ESA RAMSES)
"""

import math
from dataclasses import dataclass
from typing import Dict, Any, Tuple, List

# 天文与物理常数
G = 6.67430e-11                  # 引力常数 m^3 / (kg s^2)
M_EARTH = 5.9722e24             # 地球质量 kg
R_EARTH = 6378.137e3            # 地球赤道半径 m
MU_EARTH = 3.986004418e14       # 地心引力常数 m^3 / s^2
AU_METERS = 149597870700.0      # 1 天文单位 (AU) 米
GEO_RADIUS = 42164.14e3         # 地球静止轨道地心距 m (高度 35,786 km)

# 99942 Apophis 物理常数 (JPL / ESA 官方综合参量)
APOPHIS_MEAN_RADIUS = 170.0     # 等效平均半径 m (等效球体直径约 340~370 m)
APOPHIS_MASS = 6.1e10           # 质量 kg (约 6100 万吨)
APOPHIS_DENSITY = 2300.0        # 平均密度 kg/m^3 (典型 S 型硅酸盐/普通球粒陨石碎石堆)
APOPHIS_H_MAG = 19.09           # 绝对星等 H
APOPHIS_SLOPE_G = 0.24          # 斜率参数 G (S-type 小行星典型值)

# 2029-04-13 掠地几何参量 (JPL Horizons 标定解)
# 最接近时刻: 2029-04-13 21:46 UTC (北京时间 2029-04-14 05:46 CST)
R_PERIGEE = 38010.0e3           # 最接近地心距 m (38,010 km, ~5.96 R_Earth)
V_INFINITY = 5850.0             # 双曲线无穷远相对速度 m/s (5.85 km/s)

@dataclass(frozen=True)
class HyperbolicFlybyResult:
    """双曲线掠地轨道参数"""
    v_inf: float                # 无穷远相对速度 km/s
    v_perigee: float            # 近地点速度 km/s
    r_perigee_km: float         # 近地点地心距 km
    altitude_km: float          # 近地点地表高度 km
    inside_geo_km: float        # 深入 GEO 轨道内部距离 km
    a_hyperbolic_km: float      # 双曲线半长轴 km (负值)
    e_hyperbolic: float         # 双曲线偏心率
    deflection_deg: float       # 速度矢量渐近线偏转角 (度)

@dataclass(frozen=True)
class OrbitalTransitionResult:
    """轨道分类跃迁前后对比 (Aten -> Apollo)"""
    pre_semi_major_au: float    # 掠地前半长轴 AU
    pre_eccentricity: float     # 掠地前偏心率
    pre_period_days: float      # 掠地前绕日周期 (天)
    pre_perihelion_au: float    # 掠地前近日点 AU
    pre_aphelion_au: float      # 掠地前远日点 AU
    pre_class: str              # 掠地前类别 (Aten)
    
    post_semi_major_au: float   # 掠地后半长轴 AU
    post_eccentricity: float    # 掠地后偏心率
    post_period_days: float     # 掠地后绕日周期 (天)
    post_perihelion_au: float   # 掠地后近日点 AU
    post_aphelion_au: float     # 掠地后远日点 AU
    post_class: str             # 掠地后类别 (Apollo)
    period_increase_days: float # 周期增加天数

@dataclass(frozen=True)
class TidalPhysicsResult:
    """潮汐力、洛希极限与星震参数"""
    g_asteroid_surface: float   # 小行星表面自引力加速度 mm/s^2
    a_tidal_gradient: float     # 地球潮汐引力加速度差 mm/s^2
    tidal_to_gravity_ratio: float # 潮汐力占自身引力百分比 (%)
    rigid_roche_limit_km: float # 刚体洛希极限 km
    fluid_roche_limit_km: float # 流体洛希极限 km
    is_tidally_disrupted: bool  # 是否发生灾难性整体潮汐瓦解
    seismic_shaking_risk: str   # 表面星震/滑坡重塑等级

@dataclass(frozen=True)
class VisibilityDynamicsResult:
    """视星等、角速度与地表可见性"""
    peak_v_mag: float           # 峰值视星等
    naked_eye_visible: bool     # 是否肉眼可见
    peak_ang_speed_deg_hr: float# 峰值角速度 (度/小时)
    peak_ang_speed_deg_min: float # 峰值角速度 (度/分钟)
    moon_diameter_traversal_sec: float # 跨越一个满月视直径 (0.5°) 所需秒数

class Apophis2029FlybyEngine:
    """99942 Apophis 2029 极限掠地天体力学计算引擎"""

    def __init__(self,
                 r_perigee: float = R_PERIGEE,
                 v_inf: float = V_INFINITY,
                 mean_radius: float = APOPHIS_MEAN_RADIUS,
                 mass: float = APOPHIS_MASS,
                 density: float = APOPHIS_DENSITY):
        self.r_p = r_perigee
        self.v_inf = v_inf
        self.r_ast = mean_radius
        self.m_ast = mass
        self.rho_ast = density

    def compute_hyperbolic_flyby(self) -> HyperbolicFlybyResult:
        """解算地心双曲线相遇轨道与引力偏转角"""
        # 活力公式: v_p^2 = v_inf^2 + 2*mu/r_p
        v_p_sq = self.v_inf**2 + 2.0 * MU_EARTH / self.r_p
        v_p = math.sqrt(v_p_sq)
        
        # 双曲线半长轴: a = -mu / v_inf^2
        a_hyp = -MU_EARTH / (self.v_inf**2)
        
        # 偏心率: r_p = |a|*(e - 1) => e = 1 + r_p / |a|
        e_hyp = 1.0 + self.r_p / abs(a_hyp)
        
        # 渐近线偏转角: sin(delta / 2) = 1 / e => delta = 2 * arcsin(1 / e)
        delta_rad = 2.0 * math.asin(1.0 / e_hyp)
        delta_deg = math.degrees(delta_rad)
        
        alt_km = (self.r_p - R_EARTH) / 1000.0
        inside_geo = (GEO_RADIUS - self.r_p) / 1000.0
        
        return HyperbolicFlybyResult(
            v_inf=self.v_inf / 1000.0,
            v_perigee=v_p / 1000.0,
            r_perigee_km=self.r_p / 1000.0,
            altitude_km=alt_km,
            inside_geo_km=inside_geo,
            a_hyperbolic_km=a_hyp / 1000.0,
            e_hyperbolic=e_hyp,
            deflection_deg=delta_deg
        )

    def compute_orbital_transition(self) -> OrbitalTransitionResult:
        """
        解算小行星轨道根数突变: Aten 类向 Apollo 类跃迁
        掠地前: a=0.9224 AU, e=0.1912, P=323.6 天 (Aten 类: a < 1.0 AU, Q > 0.983 AU)
        掠地后 (受引力加速甩出): a ≈ 1.100 AU, e ≈ 0.191, P ≈ 423.8 天 (Apollo 类: a > 1.0 AU, q < 1.017 AU)
        """
        # 掠地前公称值
        pre_a = 0.9224
        pre_e = 0.1912
        pre_p = 365.2568983 * (pre_a ** 1.5) # 开普勒第三定律
        pre_q = pre_a * (1.0 - pre_e)
        pre_q_aph = pre_a * (1.0 + pre_e)
        
        # 掠地后公称值 (JPL 标定轨道跃迁)
        post_a = 1.1002
        post_e = 0.1914
        post_p = 365.2568983 * (post_a ** 1.5)
        post_q = post_a * (1.0 - post_e)
        post_q_aph = post_a * (1.0 + post_e)
        
        return OrbitalTransitionResult(
            pre_semi_major_au=pre_a,
            pre_eccentricity=pre_e,
            pre_period_days=pre_p,
            pre_perihelion_au=pre_q,
            pre_aphelion_au=pre_q_aph,
            pre_class="Aten (阿登型, a < 1.0 AU)",
            post_semi_major_au=post_a,
            post_eccentricity=post_e,
            post_period_days=post_p,
            post_perihelion_au=post_q,
            post_aphelion_au=post_q_aph,
            post_class="Apollo (阿波罗型, a > 1.0 AU)",
            period_increase_days=post_p - pre_p
        )

    def compute_tidal_physics(self) -> TidalPhysicsResult:
        """
        解算地球潮汐力、洛希极限与碎石堆星震形变条件
        """
        # 表面自身重力: g = G * M / R^2 (mm/s^2)
        g_ast = (G * self.m_ast / (self.r_ast ** 2)) * 1000.0
        
        # 地球潮汐梯度差分加速度: a_tidal = 2 * mu_earth * R_ast / r_p^3 (mm/s^2)
        a_tidal = (2.0 * MU_EARTH * self.r_ast / (self.r_p ** 3)) * 1000.0
        
        ratio = (a_tidal / g_ast) * 100.0
        
        # 地球平均密度
        rho_earth = M_EARTH / (4.0 / 3.0 * math.pi * (R_EARTH ** 3)) # ~5514 kg/m^3
        
        # 刚体洛希极限: d_rigid = R_earth * (2 * rho_earth / rho_ast)^(1/3)
        d_rigid = R_EARTH * ((2.0 * rho_earth / self.rho_ast) ** (1.0 / 3.0)) / 1000.0
        
        # 流体洛希极限: d_fluid = 2.44 * R_earth * (rho_earth / rho_ast)^(1/3)
        d_fluid = 2.44 * R_EARTH * ((rho_earth / self.rho_ast) ** (1.0 / 3.0)) / 1000.0
        
        # 是否整体潮汐瓦解 (近地点距 38,010 km > 刚体与流体极限)
        is_disrupted = (self.r_p / 1000.0) < d_rigid
        
        # 星震风险评估: 虽然整体不瓦解，但潮汐比 > 1% 足以打破松散碎石堆休止角
        if ratio > 1.0:
            seismic_grade = "高风险强星震 (Global Seismic Shaking & Surface Landslides)"
        else:
            seismic_grade = "微弱扰动"
            
        return TidalPhysicsResult(
            g_asteroid_surface=g_ast,
            a_tidal_gradient=a_tidal,
            tidal_to_gravity_ratio=ratio,
            rigid_roche_limit_km=d_rigid,
            fluid_roche_limit_km=d_fluid,
            is_tidally_disrupted=is_disrupted,
            seismic_shaking_risk=seismic_grade
        )

    def compute_visibility_and_dynamics(self) -> VisibilityDynamicsResult:
        """
        解算最接近时刻的视星等与天球角速度
        """
        # 最接近时地表站心距 delta ≈ 31,632 km
        delta_km = (self.r_p - R_EARTH) / 1000.0
        delta_au = (delta_km * 1000.0) / AU_METERS
        r_helio_au = 1.000 # 掠地时日距约 1.00 AU
        
        # 相角 alpha 约 70° (0.3888 rad)
        # H-G 简化相函数: Phi(alpha) ≈ 0.25 (相角 70° 衰减约 1.5 等)
        # V = H + 5 log10(r * delta) + phase_loss
        dist_factor = 5.0 * math.log10(r_helio_au * delta_au)
        phase_loss = 2.38 # 典型相角散射损失
        v_mag = APOPHIS_H_MAG + dist_factor + phase_loss
        
        # 活力公式求近地点速度
        v_p = math.sqrt(self.v_inf**2 + 2.0 * MU_EARTH / self.r_p)
        
        # 站心天球角速度 omega = v_p / delta (rad/s)
        omega_rad_s = v_p / (delta_km * 1000.0)
        deg_per_sec = math.degrees(omega_rad_s)
        deg_per_min = deg_per_sec * 60.0
        deg_per_hr = deg_per_sec * 3600.0
        
        # 满月视直径约 0.5° (30')
        moon_traverse_sec = 0.5 / deg_per_sec
        
        return VisibilityDynamicsResult(
            peak_v_mag=round(v_mag, 2),
            naked_eye_visible=v_mag < 6.0,
            peak_ang_speed_deg_hr=round(deg_per_hr, 1),
            peak_ang_speed_deg_min=round(deg_per_min, 2),
            moon_diameter_traversal_sec=round(moon_traverse_sec, 1)
        )

    def get_chinese_cities_windows(self) -> List[Dict[str, Any]]:
        """
        华夏代表性城市时空视窗 (2029-04-13 夜至 04-14 晨)
        最接近时刻: 2029-04-14 05:46 CST
        此时华夏东部已临近晨光始，西部 (乌鲁木齐、喀什) 则处黑夜绝佳观测窗；
        而在 04-13 晚间 20:00~02:00 CST，小行星正以超高加速度逼近，全境皆可在暗夜追踪!
        """
        cities = [
            {
                "city": "乌鲁木齐",
                "lat": 43.83,
                "lon": 87.62,
                "window": "04-14 03:30 ~ 05:46 CST",
                "dark_sky_status": "极佳纯黑暗空 (晨光终在 06:15 之后)",
                "event": "极近掠地巅峰 (距地 3.8 万 km，肉眼高速飞越)"
            },
            {
                "city": "北京",
                "lat": 39.90,
                "lon": 116.40,
                "window": "04-13 22:00 ~ 04-14 04:30 CST",
                "dark_sky_status": "通宵暗夜逼近 (晨光始约 04:45 CST)",
                "event": "逼近弧线高速贯穿星空 (视星等自 +7 等骤升至 +3.5 等)"
            },
            {
                "city": "上海",
                "lat": 31.23,
                "lon": 121.47,
                "window": "04-13 21:30 ~ 04-14 04:20 CST",
                "dark_sky_status": "通宵暗夜追踪 (晨光始约 04:35 CST)",
                "event": "巨蟹-长蛇座天区高速划过"
            },
            {
                "city": "广州",
                "lat": 23.13,
                "lon": 113.26,
                "window": "04-13 21:00 ~ 04-14 04:50 CST",
                "dark_sky_status": "高空深黑无月窗口 (晨光始约 05:05 CST)",
                "event": "南方高仰角绝景，跨越满月尺度仅需半分钟"
            },
            {
                "city": "成都",
                "lat": 30.67,
                "lon": 104.06,
                "window": "04-13 22:00 ~ 04-14 05:15 CST",
                "dark_sky_status": "极佳后半夜暗夜 (晨光始约 05:30 CST)",
                "event": "掠地前夕肉眼极盛冲刺"
            }
        ]
        return cities

    def generate_full_report(self) -> Dict[str, Any]:
        """汇总完整推演数据报告"""
        flyby = self.compute_hyperbolic_flyby()
        trans = self.compute_orbital_transition()
        tidal = self.compute_tidal_physics()
        vis = self.compute_visibility_and_dynamics()
        cities = self.get_chinese_cities_windows()
        
        return {
            "target": "99942 Apophis (毁神星 / 2004 MN4)",
            "encounter_epoch_utc": "2029-04-13 21:46 UTC",
            "encounter_epoch_cst": "2029-04-14 05:46 CST",
            "flyby_dynamics": {
                "v_inf_km_s": flyby.v_inf,
                "v_perigee_km_s": round(flyby.v_perigee, 3),
                "r_perigee_km": flyby.r_perigee_km,
                "altitude_km": round(flyby.altitude_km, 1),
                "geo_penetration_depth_km": round(flyby.inside_geo_km, 1),
                "hyperbolic_eccentricity": round(flyby.e_hyperbolic, 4),
                "deflection_angle_deg": round(flyby.deflection_deg, 2)
            },
            "orbital_transition": {
                "pre_class": trans.pre_class,
                "pre_semi_major_au": trans.pre_semi_major_au,
                "pre_period_days": round(trans.pre_period_days, 1),
                "post_class": trans.post_class,
                "post_semi_major_au": trans.post_semi_major_au,
                "post_period_days": round(trans.post_period_days, 1),
                "period_increase_days": round(trans.period_increase_days, 1)
            },
            "tidal_and_seismology": {
                "g_surface_mm_s2": round(tidal.g_asteroid_surface, 4),
                "a_tidal_mm_s2": round(tidal.a_tidal_gradient, 6),
                "tidal_to_gravity_percent": round(tidal.tidal_to_gravity_ratio, 2),
                "fluid_roche_limit_km": round(tidal.fluid_roche_limit_km, 1),
                "is_catastrophically_disrupted": tidal.is_tidally_disrupted,
                "seismic_shaking_assessment": tidal.seismic_shaking_risk
            },
            "observational_geometry": {
                "peak_magnitude": vis.peak_v_mag,
                "naked_eye": vis.naked_eye_visible,
                "peak_angular_speed_deg_hr": vis.peak_ang_speed_deg_hr,
                "moon_crossing_time_sec": vis.moon_diameter_traversal_sec
            },
            "cities_coverage": cities,
            "missions": [
                {
                    "name": "NASA OSIRIS-APEX (原 OSIRIS-REx)",
                    "role": "掠地后会合探测器",
                    "objective": "掠地后数月进入环绕轨道，勘测表面形变，并点火吹拂风化层裸露新鲜岩石"
                },
                {
                    "name": "ESA RAMSES (Rapid Apophis Mission for Space Safety)",
                    "role": "掠地前全时程伴飞探测器",
                    "objective": "掠地前 2 个月抵达，全程近距离见证地球引力潮汐对小行星的物理重塑过程"
                }
            ]
        }

if __name__ == "__main__":
    engine = Apophis2029FlybyEngine()
    import json
    report = engine.generate_full_report()
    print(json.dumps(report, indent=2, ensure_ascii=False))
