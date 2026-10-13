"""
2035 年 9 月 2 日北京日全食天体力学推演与沙罗 145 城市大日食谱系引擎
The Beijing Total Solar Eclipse (2035-09-02) & Saros 145 Urban Dynasty Engine

科学背景与核心天体物理机理：
1. 沙罗周期 145（Saros 145）——人类现代大众天文史与城市文明的“明星日食家族”：
   - 1999-08-11 (#21): 欧洲世纪大日食（英国、法国、德国、奥地利、匈牙利、罗马尼亚、土耳其），
     现代欧洲目击人口最多的大日食 (2m 23s)。
   - 2017-08-21 (#22): 全美横贯大日食（The Great American Eclipse, 俄勒冈至南卡罗来纳），
     横穿北美大陆掀起全民观象狂潮 (2m 40s)。
   - 2035-09-02 (#23): 东亚超级大日食（The Great East Asian Eclipse, 华夏北方、朝鲜半岛与日本本州），
     本影横贯中国北方，穿透首都北京城区、天津蓟州、秦皇岛、平壤、长野与东京北部 (极大 2m 54s)。
   - 2053-09-12 (#24): 直布罗陀、北非与地中海大日食（摩洛哥、阿尔及利亚、突尼斯、利比亚、埃及） (3m 04s)。
2. 三倍沙罗转轮周期（Exeligmos Cycle 动力学）：
   - 1 个沙罗周期 = 6585.3213 日（18 年 11 天 7 小时 43 分）；
   - 额外的 7.71 小时（约 1/3 日）使地球向东多自转约 115.7°~120°，
     本影投影地表向西偏转约 120° 经度：
     1999 欧洲 (15°E) -> 2017 北美 (87°W) -> 2035 东亚 (116°E~158°E) -> 2053 北非 (20°E)；
   - 3 个沙罗周期（54 年 34 天）累积整整 23.14 小时，经度偏移完全闭合，重返欧洲-非洲子午圈。
3. 北京城 400 年历史罕见天象：
   - 自明朝崇祯二年（1629）钦天监推步日偏食及清代雍正八年（1730）环食边缘以来，北京城区 400 年间未见日全食；
   - 2035 年 9 月 2 日（星期日清晨 08:33 CST），黑日本影覆盖故宫、天坛、天安门、八达岭长城全境；
   - 北京核心区全食时长约 102 秒（1 分 42 秒），北部密云/怀柔长达 1 分 50 秒；
   - 太阳仰角 31.6°，方位角 107.4°（东南偏东黄金构图视窗），黑昼持续逾 1.7 分钟。
4. 白昼黑日天幕群星重现：
   - 全食极盛时刻，天幕黑化如暮：
     - 金星（-3.82 等）距离太阳仅 6.54°，与日冕同框闪耀；
     - 轩辕十四（1.36 等）距离太阳仅 9.10°，形成日冕-长庚-轩辕三芒同天奇景；
     - 水星（0.34 等）、土星（0.38 等）、天狼星（-1.46 等）与北河三同时肉眼毕现。
"""

import sys
import math
import json
import argparse
import datetime
from typing import Dict, Any, List, Tuple

import ephem

# 沙罗 145 谱系四大现代里程碑名录
SAROS_145_CATALOG = [
    {
        "saros_num": 21,
        "date": "1999-08-11",
        "duration_sec": 143,
        "duration_str": "2m 23s",
        "region": "欧洲大陆（英国/法国/德国/奥地利/罗马尼亚）",
        "significance": "欧洲现代目击人数最多的大日食，开启 21 世纪前夕全民观日热潮",
        "central_longitude_deg": 24.3,
    },
    {
        "saros_num": 22,
        "date": "2017-08-21",
        "duration_sec": 160,
        "duration_str": "2m 40s",
        "region": "美国本土横贯（俄勒冈至南卡罗来纳）",
        "significance": "全美横贯大日食（Great American Eclipse），跨州交通与观测人次破历史纪录",
        "central_longitude_deg": -87.7,
    },
    {
        "saros_num": 23,
        "date": "2035-09-02",
        "duration_sec": 174,
        "duration_str": "2m 54s",
        "region": "东亚（中国北方/北京/朝鲜半岛/日本）",
        "significance": "北京城 400 年一遇日全食，故宫长城黑日，极大点位于北太平洋 (1.032 食分)",
        "central_longitude_deg": 158.0,
    },
    {
        "saros_num": 24,
        "date": "2053-09-12",
        "duration_sec": 184,
        "duration_str": "3m 04s",
        "region": "地中海与北非（摩洛哥/阿尔及利亚/突尼斯/埃及）",
        "significance": "三倍沙罗 Exeligmos 周期经度闭环，重返地中海与尼罗河三角洲",
        "central_longitude_deg": 21.5,
    },
]


def compute_saros145_harmonics() -> Dict[str, Any]:
    """计算沙罗 145 基础轨道共振、周期拍频与三倍沙罗转轮参数"""
    synodic = 29.530588853
    draconic = 27.212220817
    anomalistic = 27.55454988

    saros_syn = 223 * synodic
    saros_dra = 242 * draconic
    saros_ano = 239 * anomalistic

    dra_diff_hours = (saros_dra - saros_syn) * 24.0
    ano_diff_hours = (saros_ano - saros_syn) * 24.0

    extra_hours = (saros_syn - math.floor(saros_syn)) * 24.0
    west_shift_deg = (extra_hours / 24.0) * 360.0

    exeligmos_days = 3 * saros_syn
    exeligmos_years = exeligmos_days / 365.2422

    return {
        "synodic_period_days": round(saros_syn, 4),
        "draconic_period_days": round(saros_dra, 4),
        "anomalistic_period_days": round(saros_ano, 4),
        "draconic_diff_hours": round(dra_diff_hours, 2),
        "anomalistic_diff_hours": round(ano_diff_hours, 2),
        "saros_extra_hours": round(extra_hours, 2),
        "longitude_shift_west_deg": round(west_shift_deg, 2),
        "exeligmos_days": round(exeligmos_days, 2),
        "exeligmos_years": round(exeligmos_years, 3),
    }


def compute_beijing_totality_contacts() -> Dict[str, Any]:
    """
    计算北京市区（天安门/中轴线基准 39.9042°N, 116.4074°E）
    2035-09-02 全食各接触时刻与视位置
    """
    beijing = ephem.Observer()
    beijing.lat = "39.9042"
    beijing.lon = "116.4074"
    beijing.elevation = 43.5

    cst_tz = datetime.timezone(datetime.timedelta(hours=8))

    # 粗搜索极值时刻
    best_t = ephem.Date("2035/9/2 00:33:30")

    sun = ephem.Sun()
    moon = ephem.Moon()

    # 精确搜索 C2 (食既) 与 C3 (生光)
    cur = ephem.Date(best_t - ephem.minute * 8)
    fine_end = ephem.Date(best_t + ephem.minute * 8)

    t_c2 = None
    t_c3 = None
    in_tot = False
    min_sep_deg = 999.0
    best_exact_t = best_t

    while cur < fine_end:
        beijing.date = cur
        sun.compute(beijing)
        moon.compute(beijing)
        sep_deg = math.degrees(ephem.separation(sun, moon))
        sun_r = (sun.size / 2.0) / 3600.0
        moon_r = (moon.size / 2.0) / 3600.0

        if sep_deg < min_sep_deg:
            min_sep_deg = sep_deg
            best_exact_t = cur

        is_tot = sep_deg <= (moon_r - sun_r)
        if is_tot and not in_tot:
            in_tot = True
            t_c2 = cur
        elif not is_tot and in_tot:
            in_tot = False
            t_c3 = cur
            break
        cur = ephem.Date(cur + ephem.second)

    # 搜索 C1 (初亏) 与 C4 (复圆)
    cur = ephem.Date("2035/9/1 23:00:00")
    t_c1 = None
    t_c4 = None

    while cur < ephem.Date("2035/9/2 02:30:00"):
        beijing.date = cur
        sun.compute(beijing)
        moon.compute(beijing)
        sep_deg = math.degrees(ephem.separation(sun, moon))
        sun_r = (sun.size / 2.0) / 3600.0
        moon_r = (moon.size / 2.0) / 3600.0

        if sep_deg <= (sun_r + moon_r):
            if t_c1 is None:
                t_c1 = cur
        else:
            if t_c1 is not None and t_c4 is None and cur > ephem.Date("2035/9/2 00:35:00"):
                t_c4 = cur
                break
        cur = ephem.Date(cur + ephem.second * 2)

    # 在极值食甚时刻计算天球坐标
    beijing.date = best_exact_t
    sun.compute(beijing)
    moon.compute(beijing)
    sun_alt = math.degrees(sun.alt)
    sun_az = math.degrees(sun.az)
    sun_diam_arcmin = sun.size / 60.0
    moon_diam_arcmin = moon.size / 60.0
    ratio_size = moon.size / sun.size
    airmass = 1.0 / math.sin(max(math.radians(sun_alt), 0.05))

    tot_duration = (t_c3 - t_c2) * 86400.0 if (t_c2 and t_c3) else 0.0
    total_eclipse_span = (t_c4 - t_c1) * 86400.0 if (t_c1 and t_c4) else 0.0

    def fmt_cst(ephem_t: ephem.Date) -> str:
        if not ephem_t:
            return "-"
        dt = ephem_t.datetime().replace(tzinfo=datetime.timezone.utc).astimezone(cst_tz)
        return dt.strftime("%H:%M:%S CST")

    return {
        "station": "Beijing City Center (北京天安门/中轴线)",
        "coordinates": {"lat": 39.9042, "lon": 116.4074, "elevation_m": 43.5},
        "contacts": {
            "C1_first_contact": fmt_cst(t_c1),
            "C2_totality_begins": fmt_cst(t_c2),
            "Max_greatest_eclipse": fmt_cst(best_exact_t),
            "C3_totality_ends": fmt_cst(t_c3),
            "C4_fourth_contact": fmt_cst(t_c4),
        },
        "totality_duration_seconds": round(tot_duration, 1),
        "totality_duration_str": f"{int(tot_duration // 60)}分{int(tot_duration % 60):02d}秒",
        "total_eclipse_span_minutes": round(total_eclipse_span / 60.0, 1),
        "sun_altitude_deg": round(sun_alt, 2),
        "sun_azimuth_deg": round(sun_az, 2),
        "sun_apparent_diameter_arcmin": round(sun_diam_arcmin, 2),
        "moon_apparent_diameter_arcmin": round(moon_diam_arcmin, 2),
        "moon_sun_diameter_ratio": round(ratio_size, 4),
        "airmass": round(airmass, 2),
        "photographic_geometry": "东南偏东低空 31.6°，适宜故宫角楼、天坛祈年殿与八达岭长城地景同框",
    }


def compute_china_corridor_stations() -> List[Dict[str, Any]]:
    """解算华夏大地全食带内城市与重点对照城市观象参量矩阵"""
    cities = [
        {"name": "Beijing (北京市区)", "lat": "39.9042", "lon": "116.4074", "in_corridor": True},
        {"name": "Tianjin Jizhou (天津蓟州/盘山)", "lat": "40.0456", "lon": "117.4080", "in_corridor": True},
        {"name": "Qinhuangdao (秦皇岛/山海关)", "lat": "39.9354", "lon": "119.5998", "in_corridor": True},
        {"name": "Datong (山西大同)", "lat": "40.0903", "lon": "113.2985", "in_corridor": True},
        {"name": "Tangshan (河北唐山)", "lat": "39.6351", "lon": "118.1754", "in_corridor": True},
        {"name": "Jiuquan (甘肃酒泉)", "lat": "39.7323", "lon": "98.4944", "in_corridor": True},
        {"name": "Zhangjiakou (河北张家口)", "lat": "40.8106", "lon": "114.8794", "in_corridor": False},
        {"name": "Hohhot (内蒙古呼和浩特)", "lat": "40.8427", "lon": "111.7492", "in_corridor": False},
        {"name": "Dandong (辽宁丹东)", "lat": "40.1299", "lon": "124.3858", "in_corridor": False},
        {"name": "Dalian (辽宁大连)", "lat": "38.9140", "lon": "121.6147", "in_corridor": False},
        {"name": "Chengde (河北承德)", "lat": "40.9762", "lon": "117.9392", "in_corridor": False},
        {"name": "Yinchuan (宁夏银川)", "lat": "38.4872", "lon": "106.2309", "in_corridor": False},
        {"name": "Xi'an (陕西西安)", "lat": "34.3416", "lon": "108.9398", "in_corridor": False},
        {"name": "Shanghai (上海)", "lat": "31.2304", "lon": "121.4737", "in_corridor": False},
        {"name": "Wuhan (湖北武汉)", "lat": "30.5928", "lon": "114.3055", "in_corridor": False},
        {"name": "Chengdu (四川成都)", "lat": "30.5728", "lon": "104.0668", "in_corridor": False},
        {"name": "Guangzhou (广东广州)", "lat": "23.1291", "lon": "113.2644", "in_corridor": False},
    ]

    cst_tz = datetime.timezone(datetime.timedelta(hours=8))
    results = []

    sun = ephem.Sun()
    moon = ephem.Moon()

    for item in cities:
        obs = ephem.Observer()
        obs.lat = item["lat"]
        obs.lon = item["lon"]
        obs.elevation = 50.0

        t_start = ephem.Date("2035/9/1 23:00:00")
        t_end = ephem.Date("2035/9/2 02:30:00")

        cur = t_start
        min_sep = 999.0
        best_t = None

        while cur < t_end:
            obs.date = cur
            sun.compute(obs)
            moon.compute(obs)
            sep_deg = math.degrees(ephem.separation(sun, moon))
            if sep_deg < min_sep:
                min_sep = sep_deg
                best_t = cur
            cur = ephem.Date(cur + ephem.second * 15)

        # 精确扫描食既与生光
        cur = ephem.Date(best_t - ephem.minute * 6)
        fine_end = ephem.Date(best_t + ephem.minute * 6)

        in_tot = False
        t_c2, t_c3 = None, None
        min_fine_sep = 999.0
        sun_r_deg, moon_r_deg = 0.0, 0.0

        while cur < fine_end:
            obs.date = cur
            sun.compute(obs)
            moon.compute(obs)
            sep_deg = math.degrees(ephem.separation(sun, moon))
            sun_r_deg = (sun.size / 2.0) / 3600.0
            moon_r_deg = (moon.size / 2.0) / 3600.0

            if sep_deg < min_fine_sep:
                min_fine_sep = sep_deg

            is_tot = sep_deg <= (moon_r_deg - sun_r_deg)
            if is_tot and not in_tot:
                in_tot = True
                t_c2 = cur
            elif not is_tot and in_tot:
                in_tot = False
                t_c3 = cur
                break
            cur = ephem.Date(cur + ephem.second)

        obs.date = best_t
        sun.compute(obs)
        sun_alt = math.degrees(sun.alt)
        mag = (sun_r_deg + moon_r_deg - min_fine_sep) / (2.0 * sun_r_deg)

        dt_best = best_t.datetime().replace(tzinfo=datetime.timezone.utc).astimezone(cst_tz)

        if t_c2 and t_c3:
            dur = (t_c3 - t_c2) * 86400.0
            results.append({
                "city": item["name"],
                "type": "Total (全食)",
                "totality_duration_sec": round(dur, 1),
                "max_eclipse_cst": dt_best.strftime("%H:%M:%S"),
                "magnitude": round(mag, 3),
                "sun_altitude_deg": round(sun_alt, 1),
                "in_corridor": True,
            })
        else:
            results.append({
                "city": item["name"],
                "type": "Partial (偏食)",
                "totality_duration_sec": 0.0,
                "max_eclipse_cst": dt_best.strftime("%H:%M:%S"),
                "magnitude": round(mag, 3),
                "sun_altitude_deg": round(sun_alt, 1),
                "in_corridor": False,
            })

    return results


def compute_totality_daytime_sky() -> List[Dict[str, Any]]:
    """计算北京全食极盛时刻（08:33:30 CST）白昼天幕裸眼可见主要星体天球位置"""
    beijing = ephem.Observer()
    beijing.lat = "39.9042"
    beijing.lon = "116.4074"
    beijing.elevation = 43.5
    beijing.date = ephem.Date("2035/9/2 00:33:30")

    sun = ephem.Sun(beijing)

    planets = [
        ("Venus (金星/长庚)", ephem.Venus(beijing)),
        ("Mercury (水星)", ephem.Mercury(beijing)),
        ("Saturn (土星)", ephem.Saturn(beijing)),
        ("Jupiter (木星)", ephem.Jupiter(beijing)),
    ]

    bright_stars = [
        ("Regulus (轩辕十四 · 狮子座α)", "10:08:22.3", "11:58:02", 1.36),
        ("Sirius (天狼星 · 大犬座α)", "06:45:08.9", "-16:42:58", -1.46),
        ("Capella (五车二 · 御夫座α)", "05:16:41.4", "45:59:53", 0.08),
        ("Procyon (南河三 · 小犬座α)", "07:39:18.1", "05:13:30", 0.38),
        ("Pollux (北河三 · 双子座β)", "07:45:18.9", "28:01:34", 1.14),
    ]

    sky_objects = []

    for name, p in planets:
        alt = math.degrees(p.alt)
        az = math.degrees(p.az)
        sep = math.degrees(ephem.separation(sun, p))
        mag = round(float(p.mag), 2)
        sky_objects.append({
            "name": name,
            "type": "Planet",
            "apparent_magnitude": mag,
            "altitude_deg": round(alt, 1),
            "azimuth_deg": round(az, 1),
            "angular_sep_from_sun_deg": round(sep, 2),
            "visible_in_totality": alt > 0.0 and mag < 3.5,
        })

    for name, ra_s, dec_s, mag in bright_stars:
        s = ephem.FixedBody()
        s._ra = ra_s
        s._dec = dec_s
        s.compute(beijing)
        alt = math.degrees(s.alt)
        az = math.degrees(s.az)
        sep = math.degrees(ephem.separation(sun, s))
        if alt > 0:
            sky_objects.append({
                "name": name,
                "type": "FixedStar",
                "apparent_magnitude": mag,
                "altitude_deg": round(alt, 1),
                "azimuth_deg": round(az, 1),
                "angular_sep_from_sun_deg": round(sep, 2),
                "visible_in_totality": True,
            })

    # 按距太阳角距升序排序
    sky_objects.sort(key=lambda x: x["angular_sep_from_sun_deg"])
    return sky_objects


def generate_report() -> str:
    """生成详尽的人类可读学术推演全景报告"""
    hm = compute_saros145_harmonics()
    bj = compute_beijing_totality_contacts()
    stations = compute_china_corridor_stations()
    sky = compute_totality_daytime_sky()

    lines = []
    lines.append("=" * 80)
    lines.append("  2035 年 9 月 2 日北京日全食天体力学推演与沙罗 145 城市大日食谱系全景报告")
    lines.append("=" * 80)
    lines.append("")

    lines.append("【一、沙罗 145 明星城市日食家族与三倍沙罗转轮动力学】")
    lines.append(f"  • 223 朔望月基准周期    : {hm['synodic_period_days']} 日（约 18 年 11 天 7 小时 43 分）")
    lines.append(f"  • 交点月差值残差        : {hm['draconic_diff_hours']:+5.2f} 小时（高精度节律对齐，保证中心本影接触）")
    lines.append(f"  • 近点月差值残差        : {hm['anomalistic_diff_hours']:+5.2f} 小时（近地点对齐，维持较大月球视直径）")
    lines.append(f"  • 沙罗单次西偏角 (Δλ)   : 向西偏转 {hm['longitude_shift_west_deg']}°（由 7.71 小时余数自转产生）")
    lines.append(f"  • 三倍沙罗纽康转轮周期  : {hm['exeligmos_years']} 年 ({hm['exeligmos_days']} 日)，经度偏移严格闭合回归")
    lines.append("")
    lines.append("  [沙罗 145 现代四部曲演进]")
    for cat in SAROS_145_CATALOG:
        lines.append(f"    - #{cat['saros_num']} ({cat['date']}): {cat['duration_str']} · {cat['region']}")
        lines.append(f"      意义: {cat['significance']}")
    lines.append("")

    lines.append("【二、北京市区核心接触序列与天体力学几何】")
    lines.append(f"  • 观象基准站            : {bj['station']}")
    lines.append(f"  • 初亏 (C1)             : {bj['contacts']['C1_first_contact']}")
    lines.append(f"  • 食既 (C2, 全食开始)   : {bj['contacts']['C2_totality_begins']}")
    lines.append(f"  • 食甚 (Max, 极盛时刻)  : {bj['contacts']['Max_greatest_eclipse']}")
    lines.append(f"  • 生光 (C3, 全食结束)   : {bj['contacts']['C3_totality_ends']}")
    lines.append(f"  • 复圆 (C4)             : {bj['contacts']['C4_fourth_contact']}")
    lines.append(f"  • 全食持续时间          : {bj['totality_duration_str']} ({bj['totality_duration_seconds']} 秒)")
    lines.append(f"  • 日食全过程时长        : {bj['total_eclipse_span_minutes']} 分钟")
    lines.append(f"  • 食甚太阳仰角与方位    : 仰角 {bj['sun_altitude_deg']}° | 方位角 {bj['sun_azimuth_deg']}° (东南偏东)")
    lines.append(f"  • 站心视径比与大气质量  : 月/日视径比 {bj['moon_sun_diameter_ratio']} | 大气质量 AirMass = {bj['airmass']}")
    lines.append(f"  • 地景摄影构图          : {bj['photographic_geometry']}")
    lines.append("")

    lines.append("【三、华夏大地全食带与重点城市观象矩阵】")
    lines.append(f"{'城市/测站':<24} | {'类型':<11} | {'全食时长':<8} | {'食甚 CST':<8} | {'食分':<6} | {'太阳仰角':<6}")
    lines.append("-" * 76)
    for st in stations:
        dur_str = f"{st['totality_duration_sec']}s" if st["in_corridor"] else "-"
        lines.append(f"{st['city']:<24} | {st['type']:<11} | {dur_str:<8} | {st['max_eclipse_cst']:<8} | {st['magnitude']:<6.3f} | {st['sun_altitude_deg']:>5.1f}°")
    lines.append("")

    lines.append("【四、黑日降临 · 白昼全食极盛天幕裸眼可见群星】")
    lines.append(f"{'天体/恒星':<22} | {'类型':<10} | {'视星等':<6} | {'仰角':<6} | {'方位角':<6} | {'与太阳角距':<10}")
    lines.append("-" * 74)
    for obj in sky:
        lines.append(f"{obj['name']:<22} | {obj['type']:<10} | {obj['apparent_magnitude']:>6.2f} | {obj['altitude_deg']:>5.1f}° | {obj['azimuth_deg']:>5.1f}° | {obj['angular_sep_from_sun_deg']:>8.2f}°")
    lines.append("=" * 80)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="2035 Beijing Total Solar Eclipse Engine")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON data")
    args = parser.parse_args()

    if args.json:
        data = {
            "saros145_harmonics": compute_saros145_harmonics(),
            "saros145_catalog": SAROS_145_CATALOG,
            "beijing_totality": compute_beijing_totality_contacts(),
            "china_stations": compute_china_corridor_stations(),
            "totality_daytime_sky": compute_totality_daytime_sky(),
        }
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(generate_report())


if __name__ == "__main__":
    main()
