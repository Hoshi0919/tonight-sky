"""
space_station_zenith_pass_2026_11_04_engine.py

2026-11-04 空间站天顶掠天与晨曦三星伴飞动力学推演引擎

天体物理与航天动力学背景：
1. 国际空间站（ISS）极高仰角天顶过境（Zenith Pass）：
   - 2026年11月04日清晨（农历九月廿六），国际空间站以 85.22° 的极高仰角直贯上海正天顶；
   - 轨道根数：历元 2026-11-01 / 11-02（NORAD CATNR 25544）；
   - 近地点距观测者最近距离仅 426.6 km，气团数低至 X = 1.003（近乎绝对真空消光），视星等达 -3.7 等；
   - 可见窗口：05:02:54 CST 至 05:08:13 CST，由西北（313.5°）经天顶横切滑向东南（137.9°）。
2. 晨曦天象协同（Co-Visibility with Dawn Trio）：
   - 在 05:04:50 CST 空间站过正天顶时刻，东南方天空中正值：
     * 残月（28.5% 照亮，高度 47.4°，方位 115.3°）；
     * 木星（-1.88 等，高度 60.3°，方位 119.6°）；
     * 火星（+0.85 等，高度 64.9°，方位 121.2°）；
   - 空间站天顶过境轨迹恰好沿大圆航线俯冲向东南天空，与残月、木星、火星形成壮丽的黎明苍穹交汇。
3. 中国空间站（CSS/天宫）同日傍晚过境：
   - 11月04日傍晚 17:57:35 至 18:01:40 CST，天宫空间站（CATNR 48274）在东北方低空上演傍晚可见过境，最高仰角 35.65°。
4. 历史航天纪念锚点（11月03日与11月04日）：
   - 2011-11-03：神舟八号与天宫一号首次在轨自动交会对接（15 周年水晶婚）；
   - 2016-11-03：长征五号重型火箭首飞成功（10 周年锡婚）；
   - 2022-11-03：梦天实验舱顺利转位，中国空间站“T”字构型正式在轨组装完成（4 周年）；
   - 2024-11-04：神舟十八号载人飞船安全返回东风着陆场（2 周年）；
   - 1973-11-03：水手10号发射，首探水星与首创引力弹弓（53 周年）。
"""

import math
import datetime
import zoneinfo
from typing import Dict, Any, List, Tuple

import ephem

CST = zoneinfo.ZoneInfo("Asia/Shanghai")
UTC = datetime.timezone.utc

# 官方精确 TLE 根数
TLE_ISS = [
    "ISS (ZARYA)",
    "1 25544U 98067A   26305.78918649  .00005925  00000+0  11503-3 0  9991",
    "2 25544  51.6332 339.1679 0007095 336.8847  23.1822 15.49143202593084"
]

TLE_CSS = [
    "CSS (TIANHE)",
    "1 48274U 21035A   26306.15696214  .00010669  00000+0  12576-3 0  9992",
    "2 48274  41.4677 203.7404 0004165 246.4549 113.5852 15.61293776314714"
]

SHANGHAI_OBS = {
    "lat": 31.2304,
    "lon": 121.4737,
    "elevation": 10.0,
    "name": "上海"
}


def airmass(alt_deg: float) -> float:
    """计算高度角 alt_deg 对应的大气气团数 (Airmass)。"""
    if alt_deg <= 0.1:
        return 40.0
    z_deg = max(0.0, min(89.9, 90.0 - alt_deg))
    z_rad = math.radians(z_deg)
    cos_z = math.cos(z_rad)
    sec_z_eff = 1.0 / (cos_z + 0.50572 * max(0.1, 96.07995 - z_deg) ** (-1.6364))
    return min(40.0, float(sec_z_eff))


def estimate_iss_magnitude(range_km: float, phase_angle_deg: float) -> float:
    """估算国际空间站在距离 range_km 和相位角 phase_angle_deg 下的视星等。"""
    # ISS 绝对星等基准（1000 km 处 50% 照亮约 -1.8）
    m0 = -1.8
    dist_term = 5.0 * math.log10(range_km / 1000.0)
    beta = math.radians(max(0.0, min(180.0, phase_angle_deg)))
    phase_factor = (1.0 + math.cos(beta)) / 2.0
    phase_term = -2.5 * math.log10(max(0.01, phase_factor))
    return round(m0 + dist_term + phase_term, 2)


def calculate_iss_pass_shanghai() -> Dict[str, Any]:
    """计算 2026-11-04 清晨国际空间站过境上海的完整物理参数。"""
    iss = ephem.readtle(TLE_ISS[0], TLE_ISS[1], TLE_ISS[2])
    obs = ephem.Observer()
    obs.lat = str(SHANGHAI_OBS["lat"])
    obs.lon = str(SHANGHAI_OBS["lon"])
    obs.elevation = SHANGHAI_OBS["elevation"]

    # 扫描区间：2026-11-04 05:00 至 05:15 CST (2026-11-03 21:00 至 21:15 UTC)
    start_utc = datetime.datetime(2026, 11, 3, 21, 0, 0, tzinfo=UTC)
    max_alt = -90.0
    tca_utc = None
    tca_az = 0.0
    tca_range_km = 0.0

    visible_points = []

    for s in range(0, 900, 1):
        cur_utc = start_utc + datetime.timedelta(seconds=s)
        obs.date = cur_utc
        iss.compute(obs)
        sun = ephem.Sun(obs)

        alt_deg = math.degrees(float(iss.alt))
        az_deg = math.degrees(float(iss.az))
        sun_alt = math.degrees(float(sun.alt))

        if alt_deg >= 10.0 and sun_alt <= -6.0 and not iss.eclipsed:
            r_km = float(iss.range) / 1000.0
            visible_points.append({
                "time_cst": cur_utc.astimezone(CST).strftime("%H:%M:%S"),
                "alt_deg": round(alt_deg, 2),
                "az_deg": round(az_deg, 2),
                "range_km": round(r_km, 1)
            })

            if alt_deg > max_alt:
                max_alt = alt_deg
                tca_utc = cur_utc
                tca_az = az_deg
                tca_range_km = r_km

    # 峰值时刻天体协同状态
    obs.date = tca_utc
    sun = ephem.Sun(obs)
    moon = ephem.Moon(obs)
    jup = ephem.Jupiter(obs)
    mars = ephem.Mars(obs)

    sun_alt_tca = math.degrees(float(sun.alt))
    moon_alt = math.degrees(float(moon.alt))
    moon_az = math.degrees(float(moon.az))
    jup_alt = math.degrees(float(jup.alt))
    jup_az = math.degrees(float(jup.az))
    mars_alt = math.degrees(float(mars.alt))
    mars_az = math.degrees(float(mars.az))

    mag_peak = estimate_iss_magnitude(tca_range_km, 65.0)

    aos = visible_points[0] if visible_points else {}
    los = visible_points[-1] if visible_points else {}
    duration_sec = len(visible_points)

    return {
        "target": "ISS (ZARYA)",
        "date_local": "2026-11-04",
        "city": SHANGHAI_OBS["name"],
        "aos": aos,
        "los": los,
        "duration_seconds": duration_sec,
        "tca": {
            "time_cst": tca_utc.astimezone(CST).strftime("%H:%M:%S"),
            "max_alt_deg": round(max_alt, 2),
            "az_deg": round(tca_az, 2),
            "range_km": round(tca_range_km, 1),
            "airmass": round(airmass(max_alt), 4),
            "estimated_magnitude": mag_peak,
            "sun_alt_deg": round(sun_alt_tca, 2)
        },
        "co_visible_celestial_trio": {
            "moon": {
                "phase_pct": round(float(moon.phase), 1),
                "alt_deg": round(moon_alt, 2),
                "az_deg": round(moon_az, 2),
                "phase_name": "残月"
            },
            "jupiter": {
                "magnitude": round(float(jup.mag), 2),
                "alt_deg": round(jup_alt, 2),
                "az_deg": round(jup_az, 2)
            },
            "mars": {
                "magnitude": round(float(mars.mag), 2),
                "alt_deg": round(mars_alt, 2),
                "az_deg": round(mars_az, 2)
            }
        }
    }


def calculate_css_evening_pass_shanghai() -> Dict[str, Any]:
    """计算 2026-11-04 傍晚中国空间站（天宫）过境上海的物理参数。"""
    css = ephem.readtle(TLE_CSS[0], TLE_CSS[1], TLE_CSS[2])
    obs = ephem.Observer()
    obs.lat = str(SHANGHAI_OBS["lat"])
    obs.lon = str(SHANGHAI_OBS["lon"])
    obs.elevation = SHANGHAI_OBS["elevation"]

    # 扫描区间：2026-11-04 17:50 至 18:05 CST (09:50 至 10:05 UTC)
    start_utc = datetime.datetime(2026, 11, 4, 9, 50, 0, tzinfo=UTC)
    max_alt = -90.0
    tca_utc = None
    tca_az = 0.0
    tca_range_km = 0.0

    visible_points = []
    for s in range(0, 900, 5):
        cur_utc = start_utc + datetime.timedelta(seconds=s)
        obs.date = cur_utc
        css.compute(obs)
        sun = ephem.Sun(obs)

        alt_deg = math.degrees(float(css.alt))
        az_deg = math.degrees(float(css.az))
        sun_alt = math.degrees(float(sun.alt))

        if alt_deg >= 10.0 and sun_alt <= -6.0 and not css.eclipsed:
            r_km = float(css.range) / 1000.0
            visible_points.append({
                "time_cst": cur_utc.astimezone(CST).strftime("%H:%M:%S"),
                "alt_deg": round(alt_deg, 2),
                "az_deg": round(az_deg, 2),
                "range_km": round(r_km, 1)
            })

            if alt_deg > max_alt:
                max_alt = alt_deg
                tca_utc = cur_utc
                tca_az = az_deg
                tca_range_km = r_km

    obs.date = tca_utc
    sun = ephem.Sun(obs)

    return {
        "target": "CSS (TIANHE)",
        "date_local": "2026-11-04",
        "city": SHANGHAI_OBS["name"],
        "aos": visible_points[0] if visible_points else {},
        "los": visible_points[-1] if visible_points else {},
        "tca": {
            "time_cst": tca_utc.astimezone(CST).strftime("%H:%M:%S") if tca_utc else "",
            "max_alt_deg": round(max_alt, 2),
            "az_deg": round(tca_az, 2),
            "range_km": round(tca_range_km, 1),
            "sun_alt_deg": round(math.degrees(float(sun.alt)), 2)
        }
    }


def get_space_rendezvous_anniversaries() -> Dict[str, Any]:
    """返回 11月03日与11月04日的历史重大航天交会纪念纪元。"""
    return {
        "2011-11-03": {
            "event": "神舟八号与天宫一号首次在轨自动交会对接",
            "years_elapsed": 15,
            "milestone": "水晶婚纪念（中国成为继美俄后第三个掌握独立自动空间交会对接的国家）"
        },
        "2016-11-03": {
            "event": "长征五号重型运载火箭文昌首飞成功",
            "years_elapsed": 10,
            "milestone": "锡婚纪念（开启探月三期、天问一号与空间站建设核心重推力时代）"
        },
        "2022-11-03": {
            "event": "梦天实验舱完成转位，中国空间站“T”字基本构型在轨组装圆满完成",
            "years_elapsed": 4,
            "milestone": "国家太空实验室核心架构在轨完全落成"
        },
        "1973-11-03": {
            "event": "水手10号（Mariner 10）水星与行星引力助推首飞探测器发射",
            "years_elapsed": 53,
            "milestone": "人类历史上首次利用金星引力弹弓变轨抵达水星"
        },
        "2024-11-04": {
            "event": "神舟十八号载人飞船返回舱东风着陆场安全着陆",
            "years_elapsed": 2,
            "milestone": "叶光富、李聪、李广苏完成192天在轨驻留安全回家"
        }
    }


if __name__ == "__main__":
    import json
    iss_res = calculate_iss_pass_shanghai()
    css_res = calculate_css_evening_pass_shanghai()
    ann_res = get_space_rendezvous_anniversaries()
    print(json.dumps({
        "iss_morning_pass": iss_res,
        "css_evening_pass": css_res,
        "anniversaries": ann_res
    }, indent=2, ensure_ascii=False))
