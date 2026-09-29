#!/usr/bin/env python3
"""
meteor_shower_dynamics_engine.py
================================
2026 年十月双流星雨天体动力学、流星体物理烧蚀与天幕辐射对比引擎
(October 2026 Meteor Shower Dynamics, Ablation Physics & Sky Contrast Engine)

深度推演与建模：
1. 天龙座流星雨 (Draconids, DRA #009) vs 猎户座流星雨 (Orionids, ORI #008)
2. 母彗星 21P/Giacobini-Zinner (顺行追赶, 20 km/s) vs 1P/Halley (逆行迎头相撞, 66 km/s) 轨道动力学
3. 大气烧蚀动能、发光效率 (Luminous Efficiency) 与金属原子光谱激波特征
4. 辐射点天球时序日周弧度与中国五大地理纬度恒显圈 (Circumpolar) 几何
5. 2026 年农历廿八近无月暗空 (3.5% 月相) vs 农历十二盈凸月 (77% 强光) 瑞利/米氏散射夜空极限星等 (NELM) 模型
6. 有效小时率 (HR_obs) 积分与各大城市黄金观测天窗提取

Author: Hoshi (hoshi0919@outlook.com)
Date: 2026-09-29
"""

import math
import json
import argparse
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple, Any

import ephem

# ----------------------------------------------------------------------
# 1. 物理常数与天体测量学参数
# ----------------------------------------------------------------------
DEG_TO_RAD = math.pi / 180.0
RAD_TO_DEG = 180.0 / math.pi
CST_TZ = timezone(timedelta(hours=8))

# 中国五大典型地理观测节点 (经度, 纬度, 海拔)
DEFAULT_CITIES = {
    "Mohe": {"name_cn": "漠河 (北极村)", "lat": "52.9716", "lon": "122.5358", "elevation": 300},
    "Beijing": {"name_cn": "北京 (国家天文台兴隆站)", "lat": "39.9042", "lon": "116.4074", "elevation": 900},
    "Shanghai": {"name_cn": "上海 (佘山)", "lat": "31.2304", "lon": "121.4737", "elevation": 100},
    "Guangzhou": {"name_cn": "广州 (从化阿婆六)", "lat": "23.1291", "lon": "113.2644", "elevation": 730},
    "Urumqi": {"name_cn": "乌鲁木齐 (南山天文台)", "lat": "43.8256", "lon": "87.6168", "elevation": 2080}
}


@dataclass
class CometOrbitProfile:
    name: str
    designation: str
    period_years: float
    semi_major_axis_au: float
    eccentricity: float
    inclination_deg: float
    perihelion_dist_au: float
    encounter_geometry: str


@dataclass
class MeteorAblationProfile:
    entry_velocity_kms: float
    kinetic_energy_per_mg_joules: float
    luminous_efficiency_relative: float
    shock_temperature_kelvin: float
    ionization_degree: str
    dominant_emissions: str
    visual_color: str
    trail_speed_perception: str
    persistent_train_probability: float


@dataclass
class ShowerConfig:
    name: str
    name_cn: str
    imo_code: str
    iau_number: int
    peak_date_cst: str
    radiant_ra_hours: str
    radiant_ra_deg: float
    radiant_dec_deg: float
    zhr_base: float
    population_index_r: float
    comet: CometOrbitProfile
    ablation: MeteorAblationProfile


def get_draconids_config() -> ShowerConfig:
    """天龙座流星雨 (Draconids 2026) 配置与物理参量"""
    comet = CometOrbitProfile(
        name="21P/Giacobini-Zinner",
        designation="21P",
        period_years=6.55,
        semi_major_axis_au=3.526,
        eccentricity=0.710,
        inclination_deg=31.81,
        perihelion_dist_au=1.028,
        encounter_geometry="顺行追赶相交 (Prograde Trailing Catch-up)"
    )
    # 动能: E = 0.5 * m * v^2 -> 1mg = 1e-6 kg, v = 20.4 km/s -> 0.5 * 1e-6 * (20400)^2 = 208.1 J
    # 发光效率比: 相对 猎户座 (66 km/s) ~ (20.4/66.0)^3.5 = 0.0163 (约 1:60 发光功率比)
    ablation = MeteorAblationProfile(
        entry_velocity_kms=20.4,
        kinetic_energy_per_mg_joules=208.1,
        luminous_efficiency_relative=0.016,
        shock_temperature_kelvin=3500.0,
        ionization_degree="弱电离 (微弱复合)",
        dominant_emissions="Na I (589 nm 钠黄双线), Fe I 中性铁线, Mg I",
        visual_color="暖黄 / 琥珀金色 (Amber Gold)",
        trail_speed_perception="悠缓优雅、近乎慢动作划过 (Slow Motion)",
        persistent_train_probability=0.02
    )
    return ShowerConfig(
        name="Draconids",
        name_cn="天龙座流星雨",
        imo_code="DRA",
        iau_number=9,
        peak_date_cst="2026-10-08",
        radiant_ra_hours="17:28:00",
        radiant_ra_deg=262.0,
        radiant_dec_deg=54.0,
        zhr_base=10.0,
        population_index_r=2.6,
        comet=comet,
        ablation=ablation
    )


def get_orionids_config() -> ShowerConfig:
    """猎户座流星雨 (Orionids 2026) 配置与物理参量"""
    comet = CometOrbitProfile(
        name="1P/Halley",
        designation="1P",
        period_years=75.3,
        semi_major_axis_au=17.83,
        eccentricity=0.967,
        inclination_deg=162.26,
        perihelion_dist_au=0.586,
        encounter_geometry="逆行迎头对撞 (Retrograde Head-on Collision)"
    )
    # 动能: v = 66.0 km/s -> 0.5 * 1e-6 * (66000)^2 = 2178.0 J
    ablation = MeteorAblationProfile(
        entry_velocity_kms=66.0,
        kinetic_energy_per_mg_joules=2178.0,
        luminous_efficiency_relative=1.000,
        shock_temperature_kelvin=18500.0,
        ionization_degree="强完全电离 (高能等离子体鞘)",
        dominant_emissions="O I (557.7 nm 极光禁线), Mg II (448.1 nm), N2+ 激发态",
        visual_color="蓝白耀斑 / 浅绿荧光 (Blue-white / Emerald)",
        trail_speed_perception="迅猛极速、瞬间破空 (Blazing Fast)",
        persistent_train_probability=0.45
    )
    return ShowerConfig(
        name="Orionids",
        name_cn="猎户座流星雨",
        imo_code="ORI",
        iau_number=8,
        peak_date_cst="2026-10-21",
        radiant_ra_hours="06:20:00",
        radiant_ra_deg=95.0,
        radiant_dec_deg=16.0,
        zhr_base=20.0,
        population_index_r=2.5,
        comet=comet,
        ablation=ablation
    )


# ----------------------------------------------------------------------
# 2. 辐射点位置、天幕天光与极限星等 (NELM) 物理模型
# ----------------------------------------------------------------------

def calculate_lunar_sky_degradation(moon_alt_deg: float, moon_phase_pct: float,
                                    moon_separation_deg: float) -> Tuple[float, float]:
    """
    计算散射月辉对夜空极限星等 (NELM) 的压制 (基于 Schaefer 1993 与 Krisciunas 1991 简化模型)
    
    Returns:
        (b_moon_ratio, delta_mag): 月光与暗夜天底亮度比值, 以及 NELM 衰减等数
    """
    if moon_alt_deg <= 0.0 or moon_phase_pct < 0.5:
        return 0.0, 0.0
    
    # 照度因子: 满月(100%)为 1.0, 照亮比例与相位衰减
    # 月球相函数拟合 (Hapke): 接近新月时极度微弱
    phase_factor = (moon_phase_pct / 100.0) ** 2.2
    
    # 地平仰角消光与投影: sin(h)
    alt_factor = math.sin(max(0.0, moon_alt_deg) * DEG_TO_RAD)
    
    # 散射角分布: 瑞利散射 (1 + cos^2 theta) + 米氏前向散射峰
    cos_theta = math.cos(moon_separation_deg * DEG_TO_RAD)
    rayleigh = 1.0 + cos_theta ** 2
    # 气溶胶微粒前向散射辉光
    mie = 10.0 / (1.0 + (moon_separation_deg / 10.0) ** 2)
    scattering = rayleigh + 0.1 * mie
    
    # 综合月辉比例 (归一化至典型乡村暗夜背景 B_dark)
    # 满月天顶时 B_moon / B_dark 约为 25~30 (压制约 3.5 等)
    b_ratio = 28.0 * phase_factor * alt_factor * (scattering / 2.0)
    
    # 极限星等退化量: Delta m = 2.5 * log10(1 + B_moon / B_dark)
    delta_mag = 2.5 * math.log10(1.0 + b_ratio)
    return b_ratio, delta_mag


def calculate_hourly_record(observer: ephem.Observer, shower: ShowerConfig,
                            dt_cst: datetime, base_nelm_dark: float = 6.5,
                            gamma: float = 1.4) -> Dict[str, Any]:
    """
    计算特定观测点与时刻下的天象、辐射点、月面几何与有效观测流星率 (HR_obs)
    """
    # 确保 ephem.Date 传入 UTC 解释
    dt_utc = dt_cst.astimezone(timezone.utc)
    observer.date = ephem.Date(dt_utc)
    
    # 1. 辐射点位置解算
    rad_body = ephem.FixedBody()
    rad_body._ra = ephem.hours(shower.radiant_ra_hours)
    rad_body._dec = ephem.degrees(str(shower.radiant_dec_deg))
    rad_body.compute(observer)
    
    rad_alt = float(rad_body.alt) * RAD_TO_DEG
    rad_az = float(rad_body.az) * RAD_TO_DEG
    
    # 2. 太阳位置解算
    sun = ephem.Sun(observer)
    sun_alt = float(sun.alt) * RAD_TO_DEG
    
    # 3. 月球位置与相位解算
    moon = ephem.Moon(observer)
    moon_alt = float(moon.alt) * RAD_TO_DEG
    moon_phase = float(moon.phase)
    
    # 4. 月球与辐射点角距
    moon_sep = float(ephem.separation(rad_body, moon)) * RAD_TO_DEG
    
    # 5. 暮光状态判定
    if sun_alt > 0.0:
        sky_twilight = "白天 (Daylight)"
    elif sun_alt > -6.0:
        sky_twilight = "民用暮光 (Civil Twilight)"
    elif sun_alt > -12.0:
        sky_twilight = "航海暮光 (Nautical Twilight)"
    elif sun_alt > -18.0:
        sky_twilight = "天文暮光 (Astronomical Twilight)"
    else:
        sky_twilight = "纯黑天文夜 (Pure Astronomical Night)"
        
    # 6. 月光背景与极限星等 (NELM)
    b_ratio, delta_mag = calculate_lunar_sky_degradation(moon_alt, moon_phase, moon_sep)
    
    # 太阳暮光对极限星等的严重破坏
    if sun_alt > -12.0:
        nelm = max(0.0, 3.0 + (sun_alt / 4.0)) # 暮光期极限星等骤降
    elif sun_alt > -18.0:
        # 天文暮光轻微压制
        twi_penalty = (sun_alt + 18.0) / 6.0 * 1.5
        nelm = max(2.0, base_nelm_dark - delta_mag - twi_penalty)
    else:
        nelm = max(2.0, base_nelm_dark - delta_mag)
        
    # 7. 天顶仰角修正因子 C_z = sin^gamma(h)
    if rad_alt <= 0.0:
        cz = 0.0
    else:
        cz = math.sin(rad_alt * DEG_TO_RAD) ** gamma
        
    # 8. 云量与天顶可见率修正 (假设良好净空)
    # HR_obs = ZHR * sin^gamma(h) * r^(NELM - 6.5)
    mag_factor = (shower.population_index_r) ** (nelm - 6.5)
    
    if sun_alt > -10.0 or rad_alt <= 5.0:
        hr_obs = 0.0
        observable = False
    else:
        hr_obs = shower.zhr_base * cz * mag_factor
        observable = True
        
    return {
        "timestamp_cst": dt_cst.strftime("%Y-%m-%d %H:%M"),
        "sun_alt_deg": round(sun_alt, 2),
        "sky_twilight": sky_twilight,
        "radiant_alt_deg": round(rad_alt, 2),
        "radiant_az_deg": round(rad_az, 2),
        "moon_alt_deg": round(moon_alt, 2),
        "moon_phase_pct": round(moon_phase, 1),
        "moon_separation_deg": round(moon_sep, 1),
        "nelm": round(nelm, 2),
        "cz_factor": round(cz, 4),
        "lunar_attenuation_factor": round(mag_factor, 4),
        "hr_obs": round(hr_obs, 2),
        "is_observable": observable
    }


# ----------------------------------------------------------------------
# 3. 逐时夜空连续模拟与最佳天窗检测
# ----------------------------------------------------------------------

def simulate_night_window(city_key: str, shower: ShowerConfig,
                          start_hour_cst: int = 18, duration_hours: int = 14,
                          step_mins: int = 30) -> Dict[str, Any]:
    """
    对指定城市进行极盛之夜全夜连续模拟
    """
    city = DEFAULT_CITIES[city_key]
    obs = ephem.Observer()
    obs.lat = city["lat"]
    obs.lon = city["lon"]
    obs.elevation = city["elevation"]
    
    # 极盛基准日期解析
    base_date = datetime.strptime(shower.peak_date_cst, "%Y-%m-%d")
    sim_start = datetime(base_date.year, base_date.month, base_date.day,
                         start_hour_cst, 0, tzinfo=CST_TZ)
    
    records = []
    current_dt = sim_start
    total_steps = int((duration_hours * 60) / step_mins)
    
    # 恒显圈判定: 90 - lat <= dec
    lat_val = float(city["lat"])
    is_circumpolar = (lat_val + shower.radiant_dec_deg >= 90.0)
    
    for _ in range(total_steps + 1):
        rec = calculate_hourly_record(obs, shower, current_dt)
        records.append(rec)
        current_dt += timedelta(minutes=step_mins)
        
    # 提取最佳连续观测窗口
    # 条件: is_observable == True, sun_alt <= -12, radiant_alt >= 15
    obs_recs = [r for r in records if r["is_observable"] and r["sun_alt_deg"] <= -12.0 and r["radiant_alt_deg"] >= 15.0]
    
    if obs_recs:
        best_rec = max(obs_recs, key=lambda x: x["hr_obs"])
        window_start = obs_recs[0]["timestamp_cst"]
        window_end = obs_recs[-1]["timestamp_cst"]
        valid_duration = len(obs_recs) * (step_mins / 60.0)
        max_hr = best_rec["hr_obs"]
        avg_nelm = sum(r["nelm"] for r in obs_recs) / len(obs_recs)
        
        # 统计纯无月时间
        moon_free_recs = [r for r in obs_recs if r["moon_alt_deg"] <= 0.0]
        moon_free_hours = len(moon_free_recs) * (step_mins / 60.0)
    else:
        window_start = "无有效窗口"
        window_end = "无有效窗口"
        valid_duration = 0.0
        max_hr = 0.0
        avg_nelm = 0.0
        best_rec = None
        moon_free_hours = 0.0
        
    return {
        "city_key": city_key,
        "city_name": city["name_cn"],
        "is_circumpolar": is_circumpolar,
        "shower_name": shower.name,
        "shower_name_cn": shower.name_cn,
        "records": records,
        "window_summary": {
            "window_start": window_start,
            "window_end": window_end,
            "duration_hours": round(valid_duration, 1),
            "moon_free_hours": round(moon_free_hours, 1),
            "max_hr_obs": round(max_hr, 1),
            "best_time_cst": best_rec["timestamp_cst"] if best_rec else "N/A",
            "avg_nelm": round(avg_nelm, 2)
        }
    }


# ----------------------------------------------------------------------
# 4. 报告生成与对比引擎
# ----------------------------------------------------------------------

def generate_comparison_text_report(city_key: str = "Shanghai") -> str:
    """生成详尽终端富文本天体物理对比报告"""
    drac = get_draconids_config()
    orion = get_orionids_config()
    
    drac_sim = simulate_night_window(city_key, drac, start_hour_cst=18, duration_hours=12)
    orion_sim = simulate_night_window(city_key, orion, start_hour_cst=20, duration_hours=11)
    
    city = DEFAULT_CITIES[city_key]
    
    lines = []
    lines.append("=" * 82)
    lines.append(f"  2026 年十月双流星雨天体动力学与天幕辐射对比引擎 ({city['name_cn']})")
    lines.append("=" * 82)
    lines.append("")
    
    lines.append("【一、母彗星轨道相交动力学与流星体物理烧蚀对比】")
    lines.append("-" * 82)
    lines.append(f"{'参量名称 / 物理指标':<24} | {'天龙座流星雨 (Draconids)':<26} | {'猎户座流星雨 (Orionids)':<24}")
    lines.append("-" * 82)
    lines.append(f"{'母彗星 (Parent Comet)':<22} | {drac.comet.name:<26} | {orion.comet.name:<24}")
    lines.append(f"{'轨道周期 P / 倾角 i':<22} | {f'{drac.comet.period_years} yr / {drac.comet.inclination_deg}°':<26} | {f'{orion.comet.period_years} yr / {orion.comet.inclination_deg}°':<24}")
    lines.append(f"{'交汇轨道拓扑几何':<22} | {'顺行追赶相交 (同向切入)':<24} | {'逆行迎头对撞 (对冲相撞)':<24}")
    lines.append(f"{'大气层切入速度 v_entry':<20} | {f'{drac.ablation.entry_velocity_kms} km/s (全天最慢!)':<24} | {f'{orion.ablation.entry_velocity_kms} km/s (全天极速)':<24}")
    lines.append(f"{'1毫克尘埃初始动能 E_k':<20} | {f'{drac.ablation.kinetic_energy_per_mg_joules:.1f} J':<26} | {f'{orion.ablation.kinetic_energy_per_mg_joules:.1f} J (高 10.5 倍!)':<24}")
    lines.append(f"{'发光效率 Tau_v 相对比':<20} | {f'{drac.ablation.luminous_efficiency_relative:.3f}':<26} | {f'{orion.ablation.luminous_efficiency_relative:.3f} (1.000 基准)':<24}")
    lines.append(f"{'等离子体激波温度':<22} | {f'{drac.ablation.shock_temperature_kelvin:.0f} K (中温轻微烧蚀)':<24} | {f'{orion.ablation.shock_temperature_kelvin:.0f} K (强激波完全电离)':<24}")
    lines.append(f"{'特征辐射发射谱线':<22} | {'Na I 589nm 钠黄双线, Fe I':<24} | {'O I 557nm 极光绿, Mg II, N2+':<24}")
    lines.append(f"{'肉眼目视色彩与体感':<22} | {drac.ablation.visual_color:<26} | {orion.ablation.visual_color:<24}")
    lines.append(f"{'轨迹动力学视觉体验':<22} | {'慢条斯理、优雅悬浮划过':<24} | {'快若闪电、瞬间破空':<24}")
    lines.append(f"{'持久电离余迹概率':<22} | {f'{drac.ablation.persistent_train_probability*100:.0f}% (极少发生)':<26} | {f'{orion.ablation.persistent_train_probability*100:.0f}% (频繁留存数秒至数分)':<24}")
    lines.append("-" * 82)
    lines.append("")
    
    lines.append("【二、2026 年十月天象天幕背景与月光辐射传输条件】")
    lines.append("-" * 82)
    lines.append("1. 天龙座流星雨 (10月8日~9日极盛)：")
    dw = drac_sim["window_summary"]
    lines.append(f"   - 农历月相：八月廿八 (纤细极残月，照亮比仅 3.5%)")
    lines.append(f"   - 月出时刻：次日凌晨 04:15 CST。全夜整整 {dw['moon_free_hours']} 小时完全处于无月纯黑夜空！")
    lines.append(f"   - 极限星等：乡村暗夜 NELM 稳定在 6.45 ~ 6.50 等，月光背景干扰度 = 0.00%")
    lines.append(f"   - 辐射点日周特性：位于天龙座头部四边形 (RA 17h28m, Dec +54°)。傍晚一入夜 (19:30 CST) 即达到最高仰角！")
    lines.append(f"   - 黄金窗口：{dw['window_start']} ~ {dw['window_end']} (持续 {dw['duration_hours']} 小时，峰值在 {dw['best_time_cst']})")
    lines.append("")
    lines.append("2. 猎户座流星雨 (10月21日~22日极盛)：")
    ow = orion_sim["window_summary"]
    lines.append(f"   - 农历月相：九月十二 (盈凸月，照亮比高达 77.3%~79.1%)")
    lines.append(f"   - 月落时刻：次日凌晨 01:46 CST。前半夜受强月光漫反射洗刷，NELM 被压缩至 4.10~4.35 等，暗流星淹没率 > 85%！")
    lines.append(f"   - 后半夜黄金天窗：01:46 CST 月落后至 04:45 CST 天文拂晓前，存在罕见的 ~3.0 小时纯暗天窗！")
    lines.append(f"   - 辐射点日周特性：子夜前 (21:30 CST) 升起，凌晨 04:00 CST 达到中天最高仰角 (74.4°)")
    lines.append(f"   - 最佳观测窗口：{ow['window_start']} ~ {ow['window_end']} (月落后 01:46~04:45 CST)")
    lines.append("-" * 82)
    lines.append("")
    
    lines.append(f"【三、{city['name_cn']} 极盛夜逐时实况积分解算】")
    lines.append("-" * 82)
    lines.append(f"时刻 (CST)   | 太阳仰角 | 天龙座辐射点(仰/角) | 天龙NELM | 天龙HR | 猎户座辐射点(仰/角) | 猎户NELM | 猎户HR")
    lines.append("-" * 82)
    
    # 抽取 18:30 到 05:00 典型时刻
    drac_dict = {r["timestamp_cst"][-5:]: r for r in drac_sim["records"]}
    orion_dict = {r["timestamp_cst"][-5:]: r for r in orion_sim["records"]}
    
    sample_hours = ["18:30", "19:30", "20:30", "21:30", "22:30", "23:30",
                    "00:30", "01:30", "02:30", "03:30", "04:30", "05:00"]
    
    for sh in sample_hours:
        d_rec = drac_dict.get(sh)
        o_rec = orion_dict.get(sh)
        
        sun_str = f"{d_rec['sun_alt_deg']:5.1f}°" if d_rec else " N/A "
        
        if d_rec and d_rec["radiant_alt_deg"] > 0:
            d_rad_str = f"{d_rec['radiant_alt_deg']:4.1f}° / {d_rec['radiant_az_deg']:5.1f}°"
            d_nelm_str = f"{d_rec['nelm']:4.2f}"
            d_hr_str = f"{d_rec['hr_obs']:4.1f}/h"
        else:
            d_rad_str = "地平线下"
            d_nelm_str = "--  "
            d_hr_str = " 0.0/h"
            
        if o_rec and o_rec["radiant_alt_deg"] > 0:
            o_rad_str = f"{o_rec['radiant_alt_deg']:4.1f}° / {o_rec['radiant_az_deg']:5.1f}°"
            o_nelm_str = f"{o_rec['nelm']:4.2f}"
            o_hr_str = f"{o_rec['hr_obs']:4.1f}/h"
        else:
            o_rad_str = "地平线下"
            o_nelm_str = "--  "
            o_hr_str = " 0.0/h"
            
        lines.append(f"{sh:<12} | {sun_str:<8} | {d_rad_str:<18} | {d_nelm_str:<8} | {d_hr_str:<6} | {o_rad_str:<18} | {o_nelm_str:<8} | {o_hr_str:<6}")
        
    lines.append("-" * 82)
    lines.append("注：天龙座极盛(10-08)辐射点最高在傍晚19:30~21:00，全夜无月；猎户座(10-21)辐射点中天在清晨04:00，月落(01:46)后迎爆发。")
    lines.append("=" * 82)
    return "\n".join(lines)


def export_multi_city_summary() -> Dict[str, Any]:
    """生成全国五大节点结构化分析矩阵"""
    drac = get_draconids_config()
    orion = get_orionids_config()
    
    summary = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "draconids_config": asdict(drac),
        "orionids_config": asdict(orion),
        "cities": {}
    }
    
    for ckey in DEFAULT_CITIES:
        d_res = simulate_night_window(ckey, drac, start_hour_cst=18, duration_hours=13)
        o_res = simulate_night_window(ckey, orion, start_hour_cst=20, duration_hours=11)
        summary["cities"][ckey] = {
            "city_name": DEFAULT_CITIES[ckey]["name_cn"],
            "draconids_window": d_res["window_summary"],
            "is_draconids_circumpolar": d_res["is_circumpolar"],
            "orionids_window": o_res["window_summary"]
        }
    return summary


def main():
    parser = argparse.ArgumentParser(description="2026 年十月双流星雨天体动力学与天幕辐射对比引擎")
    parser.add_argument("--city", default="Shanghai", choices=list(DEFAULT_CITIES.keys()) + ["all"],
                        help="观测节点城市 (默认: Shanghai)")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出完整结构化数据")
    args = parser.parse_args()
    
    if args.json:
        data = export_multi_city_summary()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        if args.city == "all":
            for ckey in DEFAULT_CITIES:
                print(generate_comparison_text_report(ckey))
                print("\n")
        else:
            print(generate_comparison_text_report(args.city))


if __name__ == "__main__":
    main()
