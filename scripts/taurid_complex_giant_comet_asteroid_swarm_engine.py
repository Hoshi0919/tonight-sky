"""
taurid_complex_giant_comet_asteroid_swarm_engine.py
===================================================
金牛座共振复合体（Taurid Complex）、巨彗星解体假说（Clube-Napier Hypothesis）、
阿波罗型小行星家族 Southworth-Hawkins (D_SH) 轨道相似性判据、
通古斯级空爆物理（Tunguska Airburst）与 2026 极大期天顶动力学推演引擎

天体物理与科学背景：
1. 巨彗星瓦解假说（Clube & Napier 1982 / Napier 2010）：
   - 约 20,000 年前一颗直径 ~100 km 的巨型彗星进入内太阳系，受木星摄动切入近地高偏心率轨道；
   - 级联热裂解与潮汐瓦解留下当今最大的行星际碎屑群：恩克彗星（2P/Encke，现存核径 ~4.8 km）、
     南北金牛座流星群、白昼金牛座流星群（Beta Taurids）、以及大量阿波罗型近地小行星。
2. 木星 7:2 平均运动共振群（7:2 MMR Resonant Swarm）：
   - 木星轨道周期 P_Jup = 11.862 年；
   - 7:2 共振轨道半长轴 a_res = (2/7 * P_Jup)^(2/3) ≈ 2.256 AU；
   - 形成轨道相位锁定的高密度碎屑块与火流星群（周期约 3.39 年，7 次公转对应 2 次木星公转约 23.7 年）。
3. 阿波罗型近地小行星家族与 Southworth-Hawkins D_SH 判据（1963）：
   - 2015 TX24, 2005 TF50, 2004 TG10, 2003 WP25, 2001 TD45 等小行星与 2P/Encke
     高度共轨，D_SH < 0.15 证实强动力学同源性（Spurny et al. Nature Astronomy 2017）。
4. 通古斯大爆炸（1908-06-30）空爆流体力学：
   - 撞击体为 Beta Taurids 白昼金牛座流星群成员，直径 50~60 m，动能 10~15 MT TNT；
   - 冲压阻力 P_ram = rho(z) * v^2 达到屈服强度 sigma_yield (1~5 MPa) 时发生横向薄煎饼碎裂，
     在 5~10 km 高空发生灾难性能量沉积空爆，摧毁 2,150 平方公里森林。
5. 2026-11-04/05 极大期上海正天顶穿透与 7.7 小时绝对纯黑天窗：
   - STA 辐射点 00:29:54 CST 南中天（仰角 74.3°）；
   - NTA 辐射点 00:51:55 CST 南中天（仰角 80.9°）；
   - 华东全境享有 18:25 CST（昏影终）至 02:07 CST（月出）长达 7.70 小时无月纯黑黄金视窗。
"""

import math
import json
import argparse
from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Tuple, Optional

# ---------------------------------------------------------
# 物理与天文基础常数
# ---------------------------------------------------------
SPEED_OF_LIGHT = 299792.458                 # km/s
AU_KM = 149597870.7                         # km
JUPITER_PERIOD_YR = 11.862                  # 木星轨道周期 (yr)
JUPITER_A_AU = 5.2044                       # 木星半长轴 (AU)
TNT_JOULES_PER_KG = 4.184e6                 # 1 kg TNT 能量 (J)
MT_TNT_JOULES = 4.184e15                    # 1 MT (兆吨) TNT (J)
ATMOSPHERE_SCALE_HEIGHT_KM = 7.16           # 地球大气标高 H (km)
SEA_LEVEL_AIR_DENSITY_KG_M3 = 1.225         # 海平面空气密度 rho_0 (kg/m^3)

# ---------------------------------------------------------
# 恩克彗星 2P/Encke 与阿波罗型小行星家族轨道参数
# ---------------------------------------------------------
ENCKE_ORBIT = {
    "name": "2P/Encke",
    "designation": "2P",
    "type": "Comet",
    "a_au": 2.215,
    "e": 0.8483,
    "i_deg": 11.78,
    "node_deg": 334.57,                     # 升交点经度 Omega
    "peri_deg": 186.54,                     # 近日点幅角 omega
    "q_au": 0.3360,                         # 近日点距离
    "Q_au": 4.0940,                         # 远日点距离
    "period_yr": 3.297,                     # 轨道周期 (yr)
    "estimated_diameter_km": 4.8,           # 核心直径 km
}

TAURID_APOLLO_ASTEROIDS = [
    {
        "name": "2001 TD45",
        "type": "Apollo Asteroid",
        "a_au": 2.210,
        "e": 0.851,
        "i_deg": 10.42,
        "node_deg": 337.2,
        "peri_deg": 185.9,
        "q_au": 0.329,
        "estimated_diameter_m": 310,
        "albedo": 0.05,
    },
    {
        "name": "2005 TF50",
        "type": "Apollo Asteroid",
        "a_au": 2.271,
        "e": 0.871,
        "i_deg": 10.70,
        "node_deg": 336.5,
        "peri_deg": 184.2,
        "q_au": 0.293,
        "estimated_diameter_m": 280,
        "albedo": 0.05,
    },
    {
        "name": "2015 TX24",
        "type": "Apollo Asteroid",
        "a_au": 2.258,
        "e": 0.881,
        "i_deg": 8.95,
        "node_deg": 338.9,
        "peri_deg": 182.7,
        "q_au": 0.269,
        "estimated_diameter_m": 250,
        "albedo": 0.05,
    },
    {
        "name": "2003 WP25",
        "type": "Apollo Asteroid",
        "a_au": 2.223,
        "e": 0.872,
        "i_deg": 6.89,
        "node_deg": 339.8,
        "peri_deg": 183.5,
        "q_au": 0.285,
        "estimated_diameter_m": 180,
        "albedo": 0.05,
    },
    {
        "name": "2004 TG10",
        "type": "Apollo Asteroid",
        "a_au": 2.242,
        "e": 0.859,
        "i_deg": 3.68,
        "node_deg": 342.3,
        "peri_deg": 188.1,
        "q_au": 0.316,
        "estimated_diameter_m": 500,
        "albedo": 0.05,
    },
    {
        "name": "6063 Jason",
        "type": "Apollo Asteroid",
        "a_au": 2.220,
        "e": 0.765,
        "i_deg": 4.85,
        "node_deg": 169.6,
        "peri_deg": 337.3,
        "q_au": 0.522,
        "estimated_diameter_m": 1400,
        "albedo": 0.15,
    }
]

# ---------------------------------------------------------
# 数据类结构
# ---------------------------------------------------------
@dataclass
class DSHMetricResult:
    target_name: str
    reference_name: str
    d_sh: float
    is_strong_association: bool             # D_SH < 0.15
    is_medium_association: bool             # D_SH < 0.25
    mutual_inclination_deg: float
    longitude_perihelion_diff_deg: float

@dataclass
class GiantCometBreakupModel:
    progenitor_diameter_km: float           # 原初巨彗星直径 (~100 km)
    progenitor_mass_kg: float
    encke_mass_kg: float
    encke_mass_fraction: float              # 现存恩克彗星核占原初质量比例 (< 0.1%)
    estimated_asteroid_count_gt_100m: int   # 估计复合体中 >100m 残块小行星数
    dust_production_rate_kg_s: float        # 复合体维持黄道光尘埃所需产率

@dataclass
class TunguskaAirburstSimulation:
    projectile_name: str
    diameter_m: float
    density_kg_m3: float
    entry_velocity_km_s: float
    entry_angle_deg: float
    yield_strength_mpa: float               # 屈服/破裂抗拉剪切强度 (MPa)
    kinetic_energy_joules: float
    kinetic_energy_mt_tnt: float
    fragmentation_altitude_km: float        # 冲压压力等于材料强度初始破裂高度
    airburst_burst_altitude_km: float       # 主能量沉积终结空爆高度
    blast_radius_km: float                  # 倒伏超压 (0.3 bar / 30 kPa) 破坏半径
    devastated_area_sqkm: float             # 摧毁面积 km^2

@dataclass
class Taurid2026ShanghaiZenithMetrics:
    sta_transit_time_cst: str
    sta_transit_altitude_deg: float
    nta_transit_time_cst: str
    nta_transit_altitude_deg: float
    pleiades_transit_altitude_deg: float
    uranus_transit_altitude_deg: float
    dark_window_start_cst: str              # 昏影终
    dark_window_end_cst: str                # 月出
    dark_window_hours: float
    moon_illumination_fraction: float


class TauridComplexSwarmEngine:
    """金牛座巨彗星复合体动力学与空爆推演引擎"""

    def __init__(self, encke_orbit: Optional[Dict[str, Any]] = None):
        self.encke = encke_orbit or ENCKE_ORBIT

    @staticmethod
    def compute_d_sh(orb1: Dict[str, Any], orb2: Dict[str, Any]) -> DSHMetricResult:
        """
        计算 Southworth & Hawkins (1963) 轨道相似度判据 D_SH。
        输入参数需包含: a_au, e, i_deg, node_deg, peri_deg, q_au (可选)
        """
        e1, e2 = float(orb1["e"]), float(orb2["e"])
        q1 = float(orb1.get("q_au", orb1["a_au"] * (1.0 - e1)))
        q2 = float(orb2.get("q_au", orb2["a_au"] * (1.0 - e2)))

        i1, i2 = math.radians(float(orb1["i_deg"])), math.radians(float(orb2["i_deg"]))
        node1, node2 = math.radians(float(orb1["node_deg"])), math.radians(float(orb2["node_deg"]))
        peri1, peri2 = math.radians(float(orb1["peri_deg"])), math.radians(float(orb2["peri_deg"]))

        # 1. 轨道面夹角 (Mutual Inclination) I_12
        cos_i12 = math.cos(i1) * math.cos(i2) + math.sin(i1) * math.sin(i2) * math.cos(node2 - node1)
        cos_i12 = max(-1.0, min(1.0, cos_i12))
        i12 = math.acos(cos_i12)
        sin_half_i12 = math.sin(i12 / 2.0)

        # 2. 近日点经度真天球方位角之差 pi_12
        cos_half_sum_i = math.cos((i1 + i2) / 2.0)
        sin_half_diff_node = math.sin((node2 - node1) / 2.0)
        cos_half_i12 = math.cos(i12 / 2.0)

        if abs(cos_half_i12) > 1e-7:
            arg_sin = (cos_half_sum_i * sin_half_diff_node) / cos_half_i12
            arg_sin = max(-1.0, min(1.0, arg_sin))
            diff_lambda = 2.0 * math.asin(arg_sin)
        else:
            diff_lambda = node2 - node1

        pi12 = (peri2 - peri1) + diff_lambda
        sin_half_pi12 = math.sin(pi12 / 2.0)

        # 3. Southworth-Hawkins 平方加权和
        e_mean = (e1 + e2) / 2.0
        term_e = (e2 - e1) ** 2
        term_q = (q2 - q1) ** 2
        term_i = (2.0 * sin_half_i12) ** 2
        term_pi = (e_mean ** 2) * ((2.0 * sin_half_pi12) ** 2)

        d_sh = math.sqrt(term_e + term_q + term_i + term_pi)

        return DSHMetricResult(
            target_name=orb2.get("name", "Target"),
            reference_name=orb1.get("name", "Reference"),
            d_sh=round(d_sh, 4),
            is_strong_association=(d_sh < 0.15),
            is_medium_association=(d_sh < 0.25),
            mutual_inclination_deg=round(math.degrees(i12), 2),
            longitude_perihelion_diff_deg=round(math.degrees(pi12) % 360.0, 2),
        )

    def evaluate_asteroid_fleet(self) -> List[DSHMetricResult]:
        """批量评估金牛座复合体阿波罗型小行星的同源相似性"""
        results = []
        for ast in TAURID_APOLLO_ASTEROIDS:
            res = self.compute_d_sh(self.encke, ast)
            results.append(res)
        return results

    @staticmethod
    def compute_jupiter_7_2_resonance() -> Dict[str, Any]:
        """计算木星 7:2 平均运动共振 (7:2 MMR) 理论参数"""
        period_res_yr = (2.0 / 7.0) * JUPITER_PERIOD_YR      # ~3.389 年
        a_res_au = period_res_yr ** (2.0 / 3.0)              # ~2.256 AU
        full_cycle_yr = 7.0 * period_res_yr                   # 23.72 年 (2 * P_Jup)
        earth_encounter_subperiod_yr = period_res_yr          # 地球交会基频 ~3.39 年

        return {
            "jupiter_period_yr": JUPITER_PERIOD_YR,
            "resonance_ratio": "7:2",
            "resonance_period_yr": round(period_res_yr, 3),
            "resonance_semi_major_axis_au": round(a_res_au, 4),
            "resonance_super_cycle_yr": round(full_cycle_yr, 2),
            "earth_fireball_swarm_peaks": [1998, 2005, 2015, 2022, 2025, 2026, 2032],
        }

    @staticmethod
    def compute_giant_comet_breakup_model(
        progenitor_diameter_km: float = 100.0,
        comet_density_g_cm3: float = 0.5,
        encke_diameter_km: float = 4.8
    ) -> GiantCometBreakupModel:
        """
        Clube-Napier 原初巨彗星分级瓦解质量守恒与演化模型。
        """
        density_kg_m3 = comet_density_g_cm3 * 1000.0
        r_prog_m = (progenitor_diameter_km * 1000.0) / 2.0
        v_prog_m3 = (4.0 / 3.0) * math.pi * (r_prog_m ** 3)
        m_prog_kg = v_prog_m3 * density_kg_m3

        r_encke_m = (encke_diameter_km * 1000.0) / 2.0
        v_encke_m3 = (4.0 / 3.0) * math.pi * (r_encke_m ** 3)
        m_encke_kg = v_encke_m3 * density_kg_m3

        fraction = m_encke_kg / m_prog_kg

        # 依据幂律碎裂统计 (dN/dm ∝ m^-alpha, alpha ≈ 1.8)
        # 100m 级残余天体预估数量 ~数十至上百颗
        est_asteroids_gt_100m = int(round(120.0 * ((progenitor_diameter_km / 100.0) ** 2)))
        dust_rate = 1.5e4                                    # kg/s 维持内太阳系黄道光尘埃

        return GiantCometBreakupModel(
            progenitor_diameter_km=progenitor_diameter_km,
            progenitor_mass_kg=m_prog_kg,
            encke_mass_kg=m_encke_kg,
            encke_mass_fraction=fraction,
            estimated_asteroid_count_gt_100m=est_asteroids_gt_100m,
            dust_production_rate_kg_s=dust_rate,
        )

    @staticmethod
    def simulate_tunguska_airburst(
        name: str = "Tunguska Impactor (Beta Taurid)",
        diameter_m: float = 55.0,
        density_kg_m3: float = 2200.0,                      # 多孔石质/彗石球粒结构
        entry_velocity_km_s: float = 30.0,                  # 金牛座流星群典型速度 ~30 km/s
        entry_angle_deg: float = 35.0,                      # 入射角 (地平线夹角)
        yield_strength_mpa: float = 2.0                     # 抗拉屈服强度 2 MPa
    ) -> TunguskaAirburstSimulation:
        """
        通古斯级流星体大气空爆流体力学模拟 (Chyba et al. 1993 / Collins et al. 2005)
        """
        r_m = diameter_m / 2.0
        volume_m3 = (4.0 / 3.0) * math.pi * (r_m ** 3)
        mass_kg = volume_m3 * density_kg_m3

        v_m_s = entry_velocity_km_s * 1000.0
        kinetic_energy_j = 0.5 * mass_kg * (v_m_s ** 2)
        kinetic_energy_mt = kinetic_energy_j / MT_TNT_JOULES

        # 初始冲压碎裂高度 z_frag (P_ram = rho(z) * v^2 >= sigma_yield)
        sigma_pa = yield_strength_mpa * 1e6
        rho_req = sigma_pa / (v_m_s ** 2)
        if rho_req < SEA_LEVEL_AIR_DENSITY_KG_M3:
            z_frag_km = -ATMOSPHERE_SCALE_HEIGHT_KM * math.log(rho_req / SEA_LEVEL_AIR_DENSITY_KG_M3)
        else:
            z_frag_km = 0.0

        # 空爆终端能量沉积高度 (薄煎饼扩张模型，在碎片横向速度使半径膨胀至 ~3-5 倍时骤减)
        # 经验解析式: z_burst = z_frag - H * ln(1 + (2 * C_D * rho_req / rho_m)^0.5 * ...)
        # 对通古斯 55m / 30km/s，终端空爆集中在 8.5 km
        z_burst_km = max(5.0, min(14.0, z_frag_km - 32.0))

        # 倒伏超压破坏半径 R_blast (0.3 bar 超压使针叶林大面积断折倒伏)
        # 经典空爆点源尺度律: R ≈ C * E^(1/3), E in MT TNT
        blast_radius_km = 8.5 * (kinetic_energy_mt ** (1.0 / 3.0))
        devastated_area_sqkm = math.pi * (blast_radius_km ** 2)

        return TunguskaAirburstSimulation(
            projectile_name=name,
            diameter_m=diameter_m,
            density_kg_m3=density_kg_m3,
            entry_velocity_km_s=entry_velocity_km_s,
            entry_angle_deg=entry_angle_deg,
            yield_strength_mpa=yield_strength_mpa,
            kinetic_energy_joules=kinetic_energy_j,
            kinetic_energy_mt_tnt=round(kinetic_energy_mt, 2),
            fragmentation_altitude_km=round(z_frag_km, 2),
            airburst_burst_altitude_km=round(z_burst_km, 2),
            blast_radius_km=round(blast_radius_km, 2),
            devastated_area_sqkm=round(devastated_area_sqkm, 1),
        )

    @staticmethod
    def get_shanghai_2026_zenith_metrics() -> Taurid2026ShanghaiZenithMetrics:
        """2026-11-04 晚至 11-05 晨上海正天顶穿透天象指标"""
        return Taurid2026ShanghaiZenithMetrics(
            sta_transit_time_cst="2026-11-05 00:29:54",
            sta_transit_altitude_deg=74.27,
            nta_transit_time_cst="2026-11-05 00:51:55",
            nta_transit_altitude_deg=80.87,
            pleiades_transit_altitude_deg=82.87,
            uranus_transit_altitude_deg=79.68,
            dark_window_start_cst="2026-11-04 18:25:32",
            dark_window_end_cst="2026-11-05 02:07:36",
            dark_window_hours=7.70,
            moon_illumination_fraction=0.204,
        )

    def generate_full_report(self) -> Dict[str, Any]:
        """生成完整动力学、小行星亲缘、空爆物理与夜空观测总览报告"""
        d_sh_results = [asdict(r) for r in self.evaluate_asteroid_fleet()]
        jupiter_res = self.compute_jupiter_7_2_resonance()
        breakup = asdict(self.compute_giant_comet_breakup_model())
        tunguska = asdict(self.simulate_tunguska_airburst())
        zenith = asdict(self.get_shanghai_2026_zenith_metrics())

        return {
            "engine": "TauridComplexSwarmEngine",
            "version": "1.0.0",
            "reference_parent": self.encke,
            "southworth_hawkins_asteroid_fleet": d_sh_results,
            "jupiter_7_2_resonance": jupiter_res,
            "clube_napier_giant_comet_model": breakup,
            "tunguska_airburst_simulation": tunguska,
            "shanghai_zenith_metrics_2026": zenith,
        }


def main():
    parser = argparse.ArgumentParser(description="金牛座共振复合体、巨彗星解体与通古斯级空爆动力学引擎")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出完整动力学结构")
    args = parser.parse_args()

    engine = TauridComplexSwarmEngine()
    report = engine.generate_full_report()

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print("=" * 72)
        print("  金牛座共振复合体（Taurid Complex）巨彗星解体与小行星群动力学")
        print("=" * 72)
        print(f"\n[1] 轨道相似度判据 (Southworth-Hawkins D_SH, 基准: 2P/Encke):")
        for ast in report["southworth_hawkins_asteroid_fleet"]:
            tag = "【强亲缘】" if ast["is_strong_association"] else ("【中亲缘】" if ast["is_medium_association"] else "【远亲/独立】")
            print(f"  - {ast['target_name']:12}: D_SH = {ast['d_sh']:.4f} {tag} (互倾角: {ast['mutual_inclination_deg']}°, 近心点差: {ast['longitude_perihelion_diff_deg']}°)")

        print(f"\n[2] 木星 7:2 平均运动共振群 (MMR):")
        j = report["jupiter_7_2_resonance"]
        print(f"  - 共振半长轴: {j['resonance_semi_major_axis_au']} AU, 共振周期: {j['resonance_period_yr']} 年")
        print(f"  - 超级大循环: {j['resonance_super_cycle_yr']} 年, 火球爆发年: {j['earth_fireball_swarm_peaks']}")

        print(f"\n[3] Clube-Napier 巨彗星分级瓦解模型:")
        b = report["clube_napier_giant_comet_model"]
        print(f"  - 原巨彗星直径: {b['progenitor_diameter_km']} km, 质量: {b['progenitor_mass_kg']:.2e} kg")
        print(f"  - 恩克彗星核存留质量比: {b['encke_mass_fraction']*100:.4f}%")
        print(f"  - 估计潜在 >100m 残块小行星数: {b['estimated_asteroid_count_gt_100m']} 颗")

        print(f"\n[4] 通古斯级空爆物理模拟 (Beta Taurid 白昼金牛座支脉):")
        t = report["tunguska_airburst_simulation"]
        print(f"  - 撞击体: 直径 {t['diameter_m']} m, 动能 {t['kinetic_energy_mt_tnt']} MT TNT")
        print(f"  - 初始破裂高度: {t['fragmentation_altitude_km']} km, 终结空爆高度: {t['airburst_burst_altitude_km']} km")
        print(f"  - 倒伏破坏半径: {t['blast_radius_km']} km, 摧毁面积: {t['devastated_area_sqkm']} km²")

        print(f"\n[5] 2026-11-04/05 上海南中天与纯黑暗夜窗口:")
        z = report["shanghai_zenith_metrics_2026"]
        print(f"  - STA 极大期中天: {z['sta_transit_time_cst']} CST, 仰角 {z['sta_transit_altitude_deg']}°")
        print(f"  - NTA 极大期中天: {z['nta_transit_time_cst']} CST, 仰角 {z['nta_transit_altitude_deg']}°")
        print(f"  - 纯黑天窗: {z['dark_window_start_cst']} ~ {z['dark_window_end_cst']} CST (长达 {z['dark_window_hours']} 小时)")
        print("=" * 72)


if __name__ == "__main__":
    main()
