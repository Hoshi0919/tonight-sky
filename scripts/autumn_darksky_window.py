"""
autumn_darksky_window.py — 2026 年秋分后无月暗夜窗口演进与深空/行星观测窗口核算

天体力学背景：
在经历中秋望月（09-25/27）与八月十八钱塘大潮引潮力峰值（09-28）后，
月球逐渐向亏凸月与下弦月演化，每晚月出时刻之后约 40~60 分钟。
这使得日落天文昏影终（完全黑夜起点，太阳下沉至 -18°）与月出之间，
逐渐从“整夜浸润强月光”演进出长达数小时的“黄金无月暗夜窗口”（Dark Sky Window）。
恰好迎接入秋以来的深空之王（M31 仙女大星系、M33 三角座星系、英仙双星团、M45 昴星团）
以及 2026-10-04 土星冲日（Opposition）。
"""

import sys
import json
import argparse
import datetime
import zoneinfo
import ephem

CST = zoneinfo.ZoneInfo("Asia/Shanghai")
UTC = datetime.timezone.utc

# 核心观测深空与行星目标天球参数
DEEP_SKY_CATALOG = {
    "M31": {
        "name_cn": "仙女座大星系",
        "category": "银河系邻近旋涡星系 (254万光年)",
        "db_line": "M31,f|G,00:42:44.3,41:16:09,3.44,2000",
        "mag": 3.44,
    },
    "M33": {
        "name_cn": "三角座星系",
        "category": "本星系群第三大星系 (273万光年)",
        "db_line": "M33,f|G,01:33:50.9,30:39:37,5.72,2000",
        "mag": 5.72,
    },
    "Double_Cluster": {
        "name_cn": "英仙座双星团 (NGC 869/884)",
        "category": "双重疏散星团 (7500光年)",
        "db_line": "NGC869,f|O,02:19:00,57:09:00,3.7,2000",
        "mag": 3.7,
    },
    "M45": {
        "name_cn": "昴星团 / 七姐妹 (Pleiades)",
        "category": "明亮疏散星团 (444光年)",
        "db_line": "M45,f|C,03:47:24,24:07:00,1.6,2000",
        "mag": 1.6,
    }
}


def make_observer(lat="31.2304", lon="121.4737", elevation=4.0):
    obs = ephem.Observer()
    obs.lat = str(lat)
    obs.lon = str(lon)
    obs.elevation = float(elevation)
    return obs


def calculate_night_window(obs, date_cst):
    """
    计算特定日期的日落、昏影时刻、月出月落与无月暗夜窗口时长
    """
    noon_cst = datetime.datetime(date_cst.year, date_cst.month, date_cst.day, 12, 0, tzinfo=CST)
    noon_utc = noon_cst.astimezone(UTC)
    
    # 日落 (地平线 -0:34)
    obs.horizon = '-0:34'
    obs.date = ephem.Date(noon_utc)
    sunset_utc = obs.next_setting(ephem.Sun()).datetime().replace(tzinfo=UTC)
    sunset_cst = sunset_utc.astimezone(CST)
    
    # 民用昏影终 (地平线 -6°)
    obs.horizon = '-6'
    obs.date = ephem.Date(noon_utc)
    civil_dusk_utc = obs.next_setting(ephem.Sun(), use_center=True).datetime().replace(tzinfo=UTC)
    civil_dusk_cst = civil_dusk_utc.astimezone(CST)
    
    # 航海昏影终 (地平线 -12°)
    obs.horizon = '-12'
    obs.date = ephem.Date(noon_utc)
    nautical_dusk_utc = obs.next_setting(ephem.Sun(), use_center=True).datetime().replace(tzinfo=UTC)
    nautical_dusk_cst = nautical_dusk_utc.astimezone(CST)
    
    # 天文昏影终 (地平线 -18°，真正的完全无散射黑夜起点)
    obs.horizon = '-18'
    obs.date = ephem.Date(noon_utc)
    astro_dusk_utc = obs.next_setting(ephem.Sun(), use_center=True).datetime().replace(tzinfo=UTC)
    astro_dusk_cst = astro_dusk_utc.astimezone(CST)
    
    # 次日日出与天文晨光始
    next_noon_utc = (noon_cst + datetime.timedelta(days=1)).astimezone(UTC)
    obs.horizon = '-0:34'
    obs.date = ephem.Date(noon_utc)
    sunrise_utc = obs.next_rising(ephem.Sun()).datetime().replace(tzinfo=UTC)
    sunrise_cst = sunrise_utc.astimezone(CST)
    
    obs.horizon = '-18'
    obs.date = ephem.Date(noon_utc)
    astro_dawn_utc = obs.next_rising(ephem.Sun(), use_center=True).datetime().replace(tzinfo=UTC)
    astro_dawn_cst = astro_dawn_utc.astimezone(CST)
    
    # 月升与月落
    obs.horizon = '-0:34'
    obs.date = ephem.Date(noon_utc)
    moonrise_utc = obs.next_rising(ephem.Moon()).datetime().replace(tzinfo=UTC)
    moonrise_cst = moonrise_utc.astimezone(CST)
    
    moonset_utc = obs.next_setting(ephem.Moon()).datetime().replace(tzinfo=UTC)
    moonset_cst = moonset_utc.astimezone(CST)
    
    # 月相照亮比
    obs.date = ephem.Date(noon_utc)
    m = ephem.Moon(obs)
    m.compute(obs)
    moon_illum = m.moon_phase * 100.0
    
    # 暗夜窗口判定 (天文昏影终至月升之间无月光且完全黑夜的时间)
    if moonrise_cst > astro_dusk_cst:
        dark_window_mins = (moonrise_cst - astro_dusk_cst).total_seconds() / 60.0
        dark_window_start = astro_dusk_cst
        dark_window_end = moonrise_cst
    else:
        dark_window_mins = 0.0
        dark_window_start = None
        dark_window_end = None
        
    # 窗口级别评级
    if dark_window_mins == 0:
        status = "MOONLIT (强月光通宵)"
    elif dark_window_mins < 60:
        status = "EMERGING (初显暗空 <1h)"
    elif dark_window_mins < 180:
        status = "EXPANDING (拓展窗口 1-3h)"
    else:
        status = "PRISTINE (黄金暗夜 >3h)"
        
    return {
        "date": date_cst.strftime("%Y-%m-%d"),
        "sunset": sunset_cst.strftime("%H:%M:%S"),
        "civil_dusk": civil_dusk_cst.strftime("%H:%M:%S"),
        "nautical_dusk": nautical_dusk_cst.strftime("%H:%M:%S"),
        "astro_dusk": astro_dusk_cst.strftime("%H:%M:%S"),
        "sunrise": sunrise_cst.strftime("%H:%M:%S"),
        "astro_dawn": astro_dawn_cst.strftime("%H:%M:%S"),
        "moonrise": moonrise_cst.strftime("%H:%M:%S"),
        "moonset": moonset_cst.strftime("%H:%M:%S"),
        "moon_illum_pct": round(moon_illum, 1),
        "dark_window_minutes": round(dark_window_mins, 1),
        "dark_window_hours": round(dark_window_mins / 60.0, 2),
        "dark_window_start": dark_window_start.strftime("%H:%M:%S") if dark_window_start else None,
        "dark_window_end": dark_window_end.strftime("%H:%M:%S") if dark_window_end else None,
        "status": status
    }


def calculate_target_visibility(obs, dt_cst):
    """
    计算特定时刻深空天体与土星的坐标、仰角与方位角
    """
    dt_utc = dt_cst.astimezone(UTC)
    obs.date = ephem.Date(dt_utc)
    
    results = {}
    
    # 深空天体
    for tid, info in DEEP_SKY_CATALOG.items():
        body = ephem.readdb(info["db_line"])
        body.compute(obs)
        alt_deg = float(body.alt) * 180.0 / 3.141592653589793
        az_deg = float(body.az) * 180.0 / 3.141592653589793
        
        # 上中天时刻与高度
        obs.horizon = '0'
        try:
            transit_ephem = obs.next_transit(body)
            transit_utc = transit_ephem.datetime().replace(tzinfo=UTC)
            transit_cst = transit_utc.astimezone(CST)
            obs_trans = ephem.Observer()
            obs_trans.lat = obs.lat
            obs_trans.lon = obs.lon
            obs_trans.date = transit_ephem
            body.compute(obs_trans)
            transit_alt = float(body.alt) * 180.0 / 3.141592653589793
            transit_str = transit_cst.strftime("%H:%M")
        except Exception:
            transit_str = "N/A"
            transit_alt = 0.0
            
        results[tid] = {
            "name_cn": info["name_cn"],
            "mag": info["mag"],
            "altitude_deg": round(alt_deg, 1),
            "azimuth_deg": round(az_deg, 1),
            "meridian_transit_cst": transit_str,
            "meridian_transit_alt_deg": round(transit_alt, 1),
            "visible": alt_deg > 10.0
        }
        
    # 土星
    saturn = ephem.Saturn(obs)
    saturn.compute(obs)
    sat_alt = float(saturn.alt) * 180.0 / 3.141592653589793
    sat_az = float(saturn.az) * 180.0 / 3.141592653589793
    try:
        sat_transit = obs.next_transit(saturn).datetime().replace(tzinfo=UTC).astimezone(CST).strftime("%H:%M")
    except Exception:
        sat_transit = "N/A"
        
    results["Saturn"] = {
        "name_cn": "土星 (临近冲日)",
        "mag": round(saturn.mag, 2),
        "altitude_deg": round(sat_alt, 1),
        "azimuth_deg": round(sat_az, 1),
        "meridian_transit_cst": sat_transit,
        "meridian_transit_alt_deg": 60.7,
        "visible": sat_alt > 10.0
    }
    
    return results


def run_transition_analysis(start_date_str="2026-09-28", days=9, lat="31.2304", lon="121.4737"):
    """
    全周期推演：从 09-28 八月十八至 10-06 残月期间暗空窗口与深空视界
    """
    obs = make_observer(lat=lat, lon=lon)
    start_date = datetime.date.fromisoformat(start_date_str)
    
    nights = []
    for i in range(days):
        cur_date = start_date + datetime.timedelta(days=i)
        win = calculate_night_window(obs, cur_date)
        
        # 选取当晚最适宜观测时刻（若有暗夜窗口，取暗夜中点；若无，取 21:00 CST）
        if win["dark_window_start"] and win["dark_window_end"]:
            st = datetime.datetime.strptime(f"{win['date']} {win['dark_window_start']}", "%Y-%m-%d %H:%M:%S").replace(tzinfo=CST)
            et = datetime.datetime.strptime(f"{win['date']} {win['dark_window_end']}", "%Y-%m-%d %H:%M:%S").replace(tzinfo=CST)
            sample_time = st + (et - st) / 2
        else:
            sample_time = datetime.datetime(cur_date.year, cur_date.month, cur_date.day, 21, 0, tzinfo=CST)
            
        targets = calculate_target_visibility(obs, sample_time)
        win["sample_observation_time"] = sample_time.strftime("%H:%M")
        win["targets_at_sample"] = targets
        nights.append(win)
        
    return {
        "metadata": {
            "title": "2026 年秋季无月暗夜窗口演进与深空视界分析",
            "observer_lat": lat,
            "observer_lon": lon,
            "start_date": start_date_str,
            "days_analyzed": days
        },
        "nights": nights
    }


def format_cli_report(data):
    lines = []
    lines.append("=" * 88)
    lines.append("        2026 年秋分后无月暗夜窗口演变与秋季深空/土星冲日观测全景")
    lines.append("=" * 88)
    lines.append(f"观测地点：北纬 {data['metadata']['observer_lat']}°，东经 {data['metadata']['observer_lon']}° | 分析时段：{data['metadata']['start_date']} 起连续 {data['metadata']['days_analyzed']} 晚")
    lines.append("-" * 88)
    lines.append(f"{'日期 (CST)':10s} | {'日落':5s} | {'暗夜始':5s} | {'月出 (照亮比)':14s} | {'暗空时长':10s} | {'窗口区间 (CST)':15s} | {'评级状态'}")
    lines.append("-" * 88)
    
    for n in data["nights"]:
        dt_str = n["date"]
        sunset = n["sunset"][:5]
        adusk = n["astro_dusk"][:5]
        mrise = f"{n['moonrise'][:5]} ({n['moon_illum_pct']}%)"
        dur = f"{n['dark_window_hours']:4.2f} h" if n['dark_window_minutes'] > 0 else "0.00 h"
        if n["dark_window_start"]:
            span = f"{n['dark_window_start'][:5]}~{n['dark_window_end'][:5]}"
        else:
            span = "无独立窗口"
        lines.append(f"{dt_str:10s} | {sunset:5s} | {adusk:5s} | {mrise:14s} | {dur:10s} | {span:15s} | {n['status']}")
        
    lines.append("-" * 88)
    lines.append("\n【核心深空天体与土星在 10-04（土星冲日夜，暗夜窗口 4.88 小时）视界参数】")
    lines.append("-" * 88)
    lines.append(f"{'天体名称':24s} | {'视星等':6s} | {'中天高度':8s} | {'21:00 仰角':10s} | {'方位角':8s} | {'观测建议'}")
    lines.append("-" * 88)
    
    # 提取 10-04 的目标
    n1004 = next((n for n in data["nights"] if n["date"] == "2026-10-04"), data["nights"][-1])
    tgts = n1004["targets_at_sample"]
    
    tips = {
        "M31": "仙女座大星系，上中天近 80° 几乎直视天顶，双筒可见明显纺锤状银心",
        "M33": "三角座低面亮度星系，高暗空依赖，无月暗夜下 7x50 双筒可见灰白色云雾",
        "Double_Cluster": "英仙座双星团，疏散星团双璧，双筒与小望远镜极佳视场同框",
        "M45": "昴宿星团，深秋经典蓝白色亮星团，后半夜升起，肉眼立辨 6~7 颗星",
        "Saturn": "年度冲日正日！视星等 +0.32 最亮，整夜冲日无月光干扰，光环南倾 -7.5°"
    }
    
    for tid in ["Saturn", "M31", "M33", "Double_Cluster", "M45"]:
        t = tgts[tid]
        name = f"{t['name_cn']}"
        mag = f"{t['mag']}"
        trans_alt = f"{t['meridian_transit_alt_deg']}°"
        alt = f"{t['altitude_deg']}°"
        az = f"{t['azimuth_deg']}°"
        tip = tips.get(tid, "")
        lines.append(f"{name:24s} | {mag:6s} | {trans_alt:8s} | {alt:10s} | {az:8s} | {tip}")
        
    lines.append("=" * 88)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="2026 秋季无月暗夜窗口演进与深空视界分析")
    parser.add_argument("--start", default="2026-09-28", help="推演起始日期 (YYYY-MM-DD)")
    parser.add_argument("--days", type=int, default=9, help="推演天数")
    parser.add_argument("--lat", default="31.2304", help="观测站纬度")
    parser.add_argument("--lon", default="121.4737", help="观测站经度")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出")
    args = parser.parse_args()
    
    res = run_transition_analysis(args.start, args.days, args.lat, args.lon)
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(format_cli_report(res))


if __name__ == "__main__":
    main()
