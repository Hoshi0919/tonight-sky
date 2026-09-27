"""
土星冲日与满月伴星天体力学分析器 (Saturn Opposition & Moon Conjunction Mechanics)
用于精确核算 2026 年农历八月十七望日满月与土星的通宵伴星天象，以及 2026 年土星冲日（Opposition）与近地点轨道动力学。
"""

import datetime
import math
from typing import Dict, List, Any
import ephem

UTC = datetime.timezone.utc
TZ_CST = datetime.timezone(datetime.timedelta(hours=8))
KM_PER_AU = 149597870.7


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


def compute_tonight_conjunction(
    date_str: str = "2026-09-27",
    obs: ephem.Observer = None
) -> Dict[str, Any]:
    """
    计算指定夜晚（默认 2026-09-27 满月夜）月球与土星的伴星轨迹。
    """
    if obs is None:
        obs = get_observer()

    base_dt = datetime.datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=TZ_CST)
    noon_cst = base_dt.replace(hour=12, minute=0, second=0)
    obs.date = ephem.Date(noon_cst.astimezone(UTC))

    moon = ephem.Moon()
    saturn = ephem.Saturn()
    sun = ephem.Sun()

    # 升落与上中天时刻
    sun_set = to_cst(obs.next_setting(sun))
    moon_rise = to_cst(obs.next_rising(moon))
    saturn_rise = to_cst(obs.next_rising(saturn))
    saturn_transit = to_cst(obs.next_transit(saturn))
    moon_transit = to_cst(obs.next_transit(moon))
    saturn_set = to_cst(obs.next_setting(saturn))
    moon_set = to_cst(obs.next_setting(moon))

    # 逐小时轨迹（从 18:00 到次日 06:00 CST）
    start_track = base_dt.replace(hour=18, minute=0, second=0)
    hourly_records = []
    for h in range(13):
        cur_t = start_track + datetime.timedelta(hours=h)
        obs.date = ephem.Date(cur_t.astimezone(UTC))
        moon.compute(obs)
        saturn.compute(obs)

        sep_deg = math.degrees(ephem.separation(moon, saturn))
        hourly_records.append({
            "time_cst": cur_t.strftime("%Y-%m-%d %H:%M:%S"),
            "hour": cur_t.strftime("%H:%M"),
            "moon_alt": round(math.degrees(moon.alt), 2),
            "moon_az": round(math.degrees(moon.az), 2),
            "moon_phase": round(moon.phase, 1),
            "saturn_alt": round(math.degrees(saturn.alt), 2),
            "saturn_az": round(math.degrees(saturn.az), 2),
            "saturn_mag": round(saturn.mag, 2),
            "separation_deg": round(sep_deg, 2)
        })

    # 当日极值角距（上海地平坐标系与地心坐标系）
    # 搜索范围：从当日 00:00 至次日 12:00
    search_start = base_dt.replace(hour=0, minute=0, second=0)
    min_topo_sep = 999.0
    min_topo_time = None
    min_geo_sep = 999.0
    min_geo_time = None

    for m in range(0, 36 * 60, 2):
        t = search_start + datetime.timedelta(minutes=m)
        d = ephem.Date(t.astimezone(UTC))
        
        # 站心 (Topocentric)
        obs.date = d
        moon.compute(obs)
        saturn.compute(obs)
        topo_sep = math.degrees(ephem.separation(moon, saturn))
        if topo_sep < min_topo_sep:
            min_topo_sep = topo_sep
            min_topo_time = t

        # 地心 (Geocentric)
        m_geo = ephem.Moon(d)
        s_geo = ephem.Saturn(d)
        geo_sep = math.degrees(ephem.separation(m_geo, s_geo))
        if geo_sep < min_geo_sep:
            min_geo_sep = geo_sep
            min_geo_time = t

    return {
        "date": date_str,
        "timing": {
            "sun_set": sun_set.strftime("%H:%M:%S"),
            "moon_rise": moon_rise.strftime("%H:%M:%S"),
            "saturn_rise": saturn_rise.strftime("%H:%M:%S"),
            "saturn_transit": saturn_transit.strftime("%H:%M:%S"),
            "moon_transit": moon_transit.strftime("%H:%M:%S"),
            "saturn_set": saturn_set.strftime("%H:%M:%S"),
            "moon_set": moon_set.strftime("%H:%M:%S"),
        },
        "min_separation": {
            "topocentric_deg": round(min_topo_sep, 4),
            "topocentric_time": min_topo_time.strftime("%Y-%m-%d %H:%M:%S"),
            "geocentric_deg": round(min_geo_sep, 4),
            "geocentric_time": min_geo_time.strftime("%Y-%m-%d %H:%M:%S"),
        },
        "hourly_track": hourly_records
    }


def compute_saturn_opposition(year: int = 2026) -> Dict[str, Any]:
    """
    计算指定年份土星冲日时刻（黄经差 180°）与地土最近距离（近地点时刻）。
    """
    sun = ephem.Sun()
    saturn = ephem.Saturn()

    # 冲日搜索区间：9月20日至10月15日
    start_utc = datetime.datetime(year, 9, 20, 0, 0, 0, tzinfo=UTC)
    min_diff = 999.0
    opp_utc = None

    for m in range(0, 25 * 24 * 60, 2):
        t = start_utc + datetime.timedelta(minutes=m)
        d = ephem.Date(t)
        sun.compute(d)
        saturn.compute(d)

        sun_lon = float(ephem.Ecliptic(sun).lon)
        sat_lon = float(ephem.Ecliptic(saturn).lon)

        diff = abs((sat_lon - sun_lon) % (2 * math.pi) - math.pi)
        if diff < min_diff:
            min_diff = diff
            opp_utc = t

    # 近地点搜索（地土距离极小值）
    min_dist_au = 999.0
    closest_utc = None
    for m in range(0, 25 * 24 * 60, 2):
        t = start_utc + datetime.timedelta(minutes=m)
        d = ephem.Date(t)
        saturn.compute(d)
        if saturn.earth_distance < min_dist_au:
            min_dist_au = saturn.earth_distance
            closest_utc = t

    opp_cst = opp_utc.astimezone(TZ_CST)
    closest_cst = closest_utc.astimezone(TZ_CST)

    d_opp = ephem.Date(opp_utc)
    saturn.compute(d_opp)
    
    return {
        "year": year,
        "opposition_time_cst": opp_cst.strftime("%Y-%m-%d %H:%M:%S"),
        "perigee_time_cst": closest_cst.strftime("%Y-%m-%d %H:%M:%S"),
        "min_distance_au": round(min_dist_au, 6),
        "min_distance_km": int(round(min_dist_au * KM_PER_AU)),
        "magnitude_at_opposition": round(saturn.mag, 2),
        "angular_size_arcsec": round(saturn.size, 2),
        "constellation": ephem.constellation(saturn)
    }


if __name__ == "__main__":
    import json
    conj = compute_tonight_conjunction("2026-09-27")
    opp = compute_saturn_opposition(2026)
    print("=== 土星伴月 (2026-09-27) ===")
    print(json.dumps(conj, indent=2, ensure_ascii=False))
    print("\n=== 土星冲日 (2026) ===")
    print(json.dumps(opp, indent=2, ensure_ascii=False))
