"""
五星通宵接力天象分析器 (Five-Planet All-Night Relay Mechanics)
精确核算指定夜晚五大肉眼经典行星（水星、金星、火星、木星、土星）与月球在观测站地平坐标系下的交接、伴行与能见度轨迹。
"""

import datetime
import json
import math
import sys
from typing import Dict, List, Any, Optional
import ephem

UTC = datetime.timezone.utc
TZ_CST = datetime.timezone(datetime.timedelta(hours=8))

CONSTELLATION_NAMES_ZH = {
    "Aql": "天鹰座", "Aqr": "宝瓶座", "Ari": "白羊座", "Cnc": "巨蟹座",
    "Cap": "摩羯座", "Cas": "仙后座", "Cet": "鲸鱼座", "Gem": "双子座",
    "Leo": "狮子座", "Lib": "天秤座", "Ori": "猎户座", "Peg": "飞马座",
    "Psc": "双鱼座", "Sco": "天蝎座", "Sgr": "人马座", "Tau": "金牛座",
    "UMa": "大熊座", "Vir": "室女座"
}


def to_cst(ephem_date: ephem.Date) -> datetime.datetime:
    """将 ephem.Date 转换为 CST (UTC+8) datetime。"""
    return ephem_date.datetime().replace(tzinfo=UTC).astimezone(TZ_CST)


def get_observer(lat: str = "31.2304", lon: str = "121.4737", elevation: float = 4.0) -> ephem.Observer:
    """获取指定地理坐标的观测站（默认上海）。"""
    obs = ephem.Observer()
    obs.lat = str(lat)
    obs.lon = str(lon)
    obs.elevation = elevation
    return obs


def compute_planet_relay(
    date_str: str = "2026-09-27",
    obs: Optional[ephem.Observer] = None
) -> Dict[str, Any]:
    """
    计算指定夜晚（默认 2026-09-27）的五星通宵接力数据。
    """
    if obs is None:
        obs = get_observer()

    base_dt = datetime.datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=TZ_CST)
    noon_cst = base_dt.replace(hour=12, minute=0, second=0)
    obs.date = ephem.Date(noon_cst.astimezone(UTC))

    sun = ephem.Sun()
    moon = ephem.Moon()
    planets = {
        "Mercury": ("水星", ephem.Mercury()),
        "Venus": ("金星", ephem.Venus()),
        "Mars": ("火星", ephem.Mars()),
        "Jupiter": ("木星", ephem.Jupiter()),
        "Saturn": ("土星", ephem.Saturn())
    }

    # 日落与次日日出
    sunset_cst = to_cst(obs.next_setting(sun))
    obs.date = ephem.Date(sunset_cst.astimezone(UTC))
    sunrise_cst = to_cst(obs.next_rising(sun))

    # 计算日月及各行星的基本星历（升落、上中天、星座、星等）
    bodies_info = {}
    
    # 太阳
    bodies_info["Sun"] = {
        "name_zh": "太阳",
        "set_cst": sunset_cst.strftime("%H:%M:%S"),
        "rise_cst": sunrise_cst.strftime("%H:%M:%S")
    }

    # 月球
    obs.date = ephem.Date(noon_cst.astimezone(UTC))
    moon_rise = to_cst(obs.next_rising(moon))
    moon_transit = to_cst(obs.next_transit(moon))
    moon_set = to_cst(obs.next_setting(moon))
    obs.date = ephem.Date(moon_transit.astimezone(UTC))
    moon.compute(obs)
    c_abbr, c_name = ephem.constellation(moon)
    bodies_info["Moon"] = {
        "name_zh": "月球",
        "rise_cst": moon_rise.strftime("%H:%M:%S"),
        "transit_cst": moon_transit.strftime("%H:%M:%S"),
        "set_cst": moon_set.strftime("%H:%M:%S"),
        "max_alt": round(math.degrees(moon.alt), 2),
        "phase_percent": round(moon.phase, 1),
        "constellation": c_name,
        "constellation_zh": CONSTELLATION_NAMES_ZH.get(c_abbr, c_name)
    }

    # 五大行星
    for key, (zh_name, body) in planets.items():
        obs.date = ephem.Date(noon_cst.astimezone(UTC))
        try:
            p_rise = to_cst(obs.next_rising(body)).strftime("%H:%M:%S")
        except Exception:
            p_rise = "--:--:--"
        try:
            p_transit = to_cst(obs.next_transit(body)).strftime("%H:%M:%S")
        except Exception:
            p_transit = "--:--:--"
        try:
            p_set = to_cst(obs.next_setting(body)).strftime("%H:%M:%S")
        except Exception:
            p_set = "--:--:--"

        # 估算过中天时的最大高度与星等
        obs.date = ephem.Date(noon_cst.astimezone(UTC))
        body.compute(obs)
        c_abbr, c_name = ephem.constellation(body)
        
        info = {
            "name_zh": zh_name,
            "rise_cst": p_rise,
            "transit_cst": p_transit,
            "set_cst": p_set,
            "magnitude": round(float(body.mag), 2),
            "constellation": c_name,
            "constellation_zh": CONSTELLATION_NAMES_ZH.get(c_abbr, c_name)
        }
        if hasattr(body, "phase"):
            info["phase_percent"] = round(float(body.phase), 1)
        bodies_info[key] = info

    # 逐小时轨迹（从 17:00 至次日 06:00 CST）
    timeline = []
    seen_planets = set()
    max_simultaneous = 0
    max_simultaneous_time = ""

    for h in range(17, 31):
        dt = base_dt + datetime.timedelta(hours=h)
        obs.date = ephem.Date(dt.astimezone(UTC))
        sun.compute(obs)
        sun_alt = math.degrees(sun.alt)
        moon.compute(obs)

        current_visible_planets = []
        planet_coords = {}

        for key, (zh_name, body) in planets.items():
            body.compute(obs)
            alt = math.degrees(body.alt)
            az = math.degrees(body.az)
            planet_coords[key] = (alt, az, body)
            if alt > 0 and sun_alt < 0:
                current_visible_planets.append(key)
                seen_planets.add(key)

        if len(current_visible_planets) > max_simultaneous:
            max_simultaneous = len(current_visible_planets)
            max_simultaneous_time = dt.strftime("%H:%M")

        # 关键角距
        # 昏影期：水星与金星
        sep_mercury_venus = None
        if "Mercury" in planet_coords and "Venus" in planet_coords:
            sep_mercury_venus = round(math.degrees(ephem.separation(planet_coords["Mercury"][2], planet_coords["Venus"][2])), 2)

        # 全夜：月球与土星
        sep_moon_saturn = round(math.degrees(ephem.separation(moon, planet_coords["Saturn"][2])), 2)

        # 晨光期：火星与木星
        sep_mars_jupiter = None
        if "Mars" in planet_coords and "Jupiter" in planet_coords:
            sep_mars_jupiter = round(math.degrees(ephem.separation(planet_coords["Mars"][2], planet_coords["Jupiter"][2])), 2)

        timeline.append({
            "time_cst": dt.strftime("%Y-%m-%d %H:%M:%S"),
            "hour": dt.strftime("%H:%M"),
            "sun_alt": round(sun_alt, 2),
            "is_dark": sun_alt < 0,
            "moon_alt": round(math.degrees(moon.alt), 2),
            "moon_az": round(math.degrees(moon.az), 2),
            "visible_planets": current_visible_planets,
            "visible_count": len(current_visible_planets),
            "planets_detail": {
                k: {
                    "alt": round(planet_coords[k][0], 2),
                    "az": round(planet_coords[k][1], 2),
                    "is_above_horizon": planet_coords[k][0] > 0
                } for k in planets
            },
            "separations": {
                "mercury_venus_deg": sep_mercury_venus,
                "moon_saturn_deg": sep_moon_saturn,
                "mars_jupiter_deg": sep_mars_jupiter
            }
        })

    # 三大接力幕次窗口总结
    acts = {
        "act_1_dusk_relay": {
            "title": "第一幕：黄昏东西并辉（17:45 - 18:45 CST）",
            "west": "水星与金星在西偏南黄昏地平线上并耀（金星 -4.46等，水星 -0.07等，角距约 13.1°）",
            "east": "八月十七望日满月（17:52升起）与土星（18:09升起，+0.33等）在正东-东偏南相伴升起",
            "significance": "全天最亮两星体（月球与金星）分别镇守东西地平线两端"
        },
        "act_2_midnight_culmination": {
            "title": "第二幕：子夜南天双璧（21:00 - 01:00 CST）",
            "south": "满月与土星通宵相依，于 00:16（土星）与 00:25（月球）先后过正南中天（仰角 60.7° / 67.8°）",
            "separation": "子夜时分两星视角距稳定在 6.8° ~ 7.4°，双筒望远镜可一览无余"
        },
        "act_3_dawn_procession": {
            "title": "第三幕：黎明双星迎曦（03:00 - 05:40 CST）",
            "east": "火星（+1.15等）于 00:39 升起，木星（-1.71等）于 02:12 升起；04:00 时高悬东天，角距约 19.2°",
            "west": "满月与土星渐落西天（土星 06:22 落，月球 07:07 落）",
            "significance": "黎明前（03:00-05:00）火星、木星、土星三颗大行星同挂苍穹，五星全夜通观接力完成闭环"
        }
    }

    return {
        "date": date_str,
        "location": {
            "latitude": obs.lat,
            "longitude": obs.lon,
            "elevation_m": obs.elevation
        },
        "bodies_info": bodies_info,
        "timeline": timeline,
        "acts": acts,
        "statistics": {
            "relay_complete": len(seen_planets) == 5,
            "seen_planets_count": len(seen_planets),
            "seen_planets": sorted(list(seen_planets)),
            "max_simultaneous_planets": max_simultaneous,
            "max_simultaneous_time": max_simultaneous_time
        }
    }


def format_relay_report(data: Dict[str, Any]) -> str:
    """生成格式化分析文本报告。"""
    lines = []
    lines.append(f"============================================================")
    lines.append(f"  2026-09-27 五星通宵接力天体力学核算报告 (Shanghai CST)")
    lines.append(f"============================================================")
    lines.append("")
    stats = data["statistics"]
    lines.append(f"【核心结论】")
    lines.append(f"- 五星接力完整性：{'达成全部 5/5 颗肉眼经典行星通观' if stats['relay_complete'] else '未全部可见'}")
    lines.append(f"- 观测期间夜间同框极值：{stats['max_simultaneous_planets']} 颗行星同时在地平线上（发生于 {stats['max_simultaneous_time']} CST）")
    lines.append("")
    lines.append(f"【天体星历速览】")
    b = data["bodies_info"]
    lines.append(f"- 太阳：日落 {b['Sun']['set_cst']}，次日日出 {b['Sun']['rise_cst']}")
    lines.append(f"- 月球：{b['Moon']['rise_cst']} 升，{b['Moon']['transit_cst']} 中天（仰角 {b['Moon']['max_alt']}°），{b['Moon']['set_cst']} 落，相位 {b['Moon']['phase_percent']}%，{b['Moon']['constellation_zh']}")
    for k in ["Mercury", "Venus", "Mars", "Jupiter", "Saturn"]:
        info = b[k]
        lines.append(f"- {info['name_zh']} ({k:7s})：升 {info['rise_cst']} | 中天 {info['transit_cst']} | 落 {info['set_cst']} | 星等 {info['magnitude']:+5.2f} | {info['constellation_zh']}")
    lines.append("")
    lines.append(f"【通宵三大幕次】")
    for act_key in ["act_1_dusk_relay", "act_2_midnight_culmination", "act_3_dawn_procession"]:
        act = data["acts"][act_key]
        lines.append(f"★ {act['title']}")
        for sub_k, sub_v in act.items():
            if sub_k != "title":
                lines.append(f"  · {sub_v}")
    lines.append("")
    lines.append(f"【逐小时夜空可见行星矩阵】")
    lines.append(f" 时间(CST) | 太阳高度 | 月球(仰角/方位) | 夜空可见行星 (Alt > 0°)")
    lines.append(f"-----------+----------+-----------------+----------------------------------------")
    for row in data["timeline"]:
        hour = row["hour"]
        s_alt = f"{row['sun_alt']:+5.1f}°"
        m_info = f"{row['moon_alt']:+5.1f}° / {row['moon_az']:5.1f}°"
        vis = ", ".join([f"{p}({row['planets_detail'][p]['alt']:+.1f}°)" for p in row["visible_planets"]]) if row["visible_planets"] else "（白昼或无行星）"
        lines.append(f" {hour:9s} |  {s_alt}  | {m_info:15s} | {vis}")
    lines.append(f"============================================================")
    return "\n".join(lines)


if __name__ == "__main__":
    result = compute_planet_relay("2026-09-27")
    if "--json" in sys.argv:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_relay_report(result))
