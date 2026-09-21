#!/usr/bin/env python3
"""
tonight-sky: Generates sky-data.json and injects it into sketch.html.
Requires: ephem (uv run --with ephem python3 skygen.py)
"""

import argparse
import datetime
import json
import math
import random
import sys
from pathlib import Path

try:
    import ephem
except ImportError:
    ephem = None

DIR = Path(__file__).resolve().parent

STAR_NAMES = [
    'Sirius','Canopus','Arcturus','Vega','Capella','Rigel','Procyon','Betelgeuse',
    'Achernar','Altair','Aldebaran','Antares','Spica','Pollux','Fomalhaut','Deneb',
    'Regulus','Castor','Shaula','Gacrux','Bellatrix','Elnath','Miaplacidus','Alnilam',
    'Alnair','Alnitak','Alioth','Dubhe','Mirfak','Wezen','Kaus Australis','Alkaid',
    'Sargas','Menkalinan','Atria','Alhena','Peacock','Alphecca','Rasalhague','Hamal',
    'Diphda','Mizar','Nunki','Mirach','Almach','Denebola','Markab','Enif','Scheat',
    'Sabik','Alcyone','Polaris','Sadr','Caph','Izar','Algol','Sadalsuud','Alcor',
    'Albireo','Gienah','Zosma','Kochab','Thuban','Unukalhai','Markeb','Aspidiske'
]

def radec(body):
    return (math.degrees(float(body.ra)), math.degrees(float(body.dec)))

def azimuth_to_zh(az_deg):
    dirs = ['正北', '东北', '正东', '东南', '正南', '西南', '正西', '西北']
    idx = round((az_deg % 360) / 45) % 8
    return dirs[idx]

def get_phase_short(lunar_day, illum=None):
    if lunar_day == 1:
        return '新月'
    elif lunar_day < 8:
        return '蛾眉'
    elif lunar_day == 8:
        return '上弦'
    elif lunar_day < 15:
        return '盈凸'
    elif lunar_day in (15, 16):
        return '望月'
    elif lunar_day == 17:
        return '满月'
    elif lunar_day < 23:
        return '亏凸'
    elif lunar_day == 23:
        return '下弦'
    else:
        return '残月' 

def compute_sky_data(date_str='2026-09-20', time_str='22:30', lat='31.23', lon='121.47', elevation=10, tz=8):
    if ephem is None:
        raise RuntimeError("ephem module is required to compute astronomical sky data")

    year, month, day = map(int, date_str.split('-'))
    hour, minute = map(int, time_str.split(':'))

    local_dt = datetime.datetime(year, month, day, hour, minute, 0)
    utc_dt = local_dt - datetime.timedelta(hours=tz)

    obs = ephem.Observer()
    obs.lat, obs.lon, obs.elevation = str(lat), str(lon), elevation
    obs.date = utc_dt

    out = {
        't0_utc': utc_dt.isoformat(),
        'date_local': date_str,
        'time_local': time_str,
        'lat': float(lat),
        'lon': float(lon),
        'tz': tz,
        'seed': int(date_str.replace('-', ''))
    }

    # 1. Named stars
    stars = []
    for n in STAR_NAMES:
        try:
            b = ephem.star(n)
            b.compute(obs)
            ra, dec = radec(b)
            alt = math.degrees(float(b.alt))
            stars.append({
                'n': n,
                'ra': round(ra, 3),
                'dec': round(dec, 3),
                'mag': round(float(b.mag), 2),
                'alt0': round(alt, 1)
            })
        except Exception:
            pass
    out['stars'] = stars
    out['tri'] = ['Vega', 'Altair', 'Deneb']

    # 2. Moon
    moon = ephem.Moon()
    t_start = utc_dt - datetime.timedelta(minutes=30)
    t_end = utc_dt + datetime.timedelta(minutes=90)

    track_radec = []
    track_alt = []
    t = t_start
    while t <= t_end:
        obs.date = t
        moon.compute(obs)
        ra, dec = radec(moon)
        m = int((t - t_start).total_seconds() // 60)
        track_radec.append({
            'm': m,
            'ra': round(ra, 3),
            'dec': round(dec, 3),
            'illum': round(moon.phase, 1)
        })
        track_alt.append({
            'm': m,
            'alt': round(math.degrees(float(moon.alt)), 2),
            'az': round(math.degrees(float(moon.az)), 2),
            'illum': round(moon.phase, 1)
        })
        t += datetime.timedelta(minutes=5)

    obs.date = utc_dt
    moon.compute(obs)
    prev_new = ephem.previous_new_moon(obs.date)
    next_full = ephem.next_full_moon(obs.date)
    age_d = obs.date - prev_new
    moon_alt = math.degrees(float(moon.alt))
    moon_az = math.degrees(float(moon.az))
    moon_ra = math.degrees(float(moon.ra))
    moon_dec = math.degrees(float(moon.dec))
    moon_illum = moon.phase
    moon_dist_km = moon.earth_distance * 149597870.7
    moon_az_zh = azimuth_to_zh(moon_az)

    # 3. Chinese lunar date calculation
    local_new_dt = ephem.localtime(prev_new)
    lunar_day = (local_dt.date() - local_new_dt.date()).days + 1
    chinese_nums = ['初一','初二','初三','初四','初五','初六','初七','初八','初九','初十',
                    '十一','十二','十三','十四','十五','十六','十七','十八','十九','二十',
                    '廿一','廿二','廿三','廿四','廿五','廿六','廿七','廿八','廿九','三十']
    lunar_day_str = chinese_nums[lunar_day - 1] if 1 <= lunar_day <= 30 else f'{lunar_day}日'
    phase_short = get_phase_short(lunar_day, moon_illum)

    out['moon_t0'] = {
        'alt': round(moon_alt, 2),
        'az': round(moon_az, 2),
        'az_zh': moon_az_zh,
        'ra': round(moon_ra, 3),
        'dec': round(moon_dec, 3),
        'illum': round(moon_illum, 1),
        'phase_short': phase_short,
        'age_d': round(age_d, 2),
        'distance_km': round(moon_dist_km)
    }
    out['moon_track'] = track_radec
    out['moon_track_alt'] = track_alt

    # Moon setting
    next_setting_dt = ephem.localtime(obs.next_setting(moon))
    out['moonset_local'] = str(next_setting_dt)[:16]
    out['next_full_local'] = str(ephem.localtime(next_full))[:16]

    if next_setting_dt.date() == local_dt.date():
        moonset_str = f"{next_setting_dt.strftime('%H:%M')} 落山"
    else:
        moonset_str = f"次日 {next_setting_dt.strftime('%H:%M')} 落山"
    out['moonset_text'] = moonset_str

    if lunar_day == 9:
        phase_term = '上弦后第一夜'
    elif lunar_day == 10:
        phase_term = '宵月（盈凸）'
    elif lunar_day == 13 and date_str == '2026-09-23':
        phase_term = '秋分 · 盈凸月'
    elif lunar_day == 15:
        phase_term = '中秋节 · 望月'
    elif lunar_day == 16:
        phase_term = '十六夜 · 既望'
    elif lunar_day == 17:
        phase_term = '十七夜 · 望日满月'
    elif lunar_day < 8:
        phase_term = '蛾眉月'
    elif lunar_day == 8:
        phase_term = '上弦月'
    elif lunar_day < 15:
        phase_term = f'盈凸月（{round(moon_illum)}%）'
    else:
        phase_term = f'盈凸月（月龄 {age_d:.1f} 天）'

    out['title_main'] = '今晚的月亮'
    out['title_sub'] = f"{date_str} · 农历八月{lunar_day_str} · {phase_term}"
    out['moon_label'] = f"月亮 · {round(moon_illum)}% {phase_short}"
    if moon_alt < 0:
        out['moon_alt_az_text'] = f"地平线下（高度 {moon_alt:.1f}° · {moon_az_zh}方向）"
    else:
        out['moon_alt_az_text'] = f"高度 {moon_alt:.1f}° · {moon_az_zh}天空"

    # 4. Saturn track
    sat = ephem.Saturn()
    strack = []
    t = t_start
    while t <= t_end:
        obs.date = t
        sat.compute(obs)
        ra, dec = radec(sat)
        strack.append({
            'm': int((t - t_start).total_seconds() // 60),
            'ra': round(ra, 4),
            'dec': round(dec, 4)
        })
        t += datetime.timedelta(minutes=10)
    out['saturn_track'] = strack

    obs.date = utc_dt
    sat.compute(obs)
    moon.compute(obs)
    moon_sat_sep = math.degrees(float(ephem.separation(moon, sat)))
    out['moon_sat_sep'] = round(moon_sat_sep, 1)
    sat_alt = math.degrees(float(sat.alt))
    sat_az = math.degrees(float(sat.az))
    sat_az_zh = azimuth_to_zh(sat_az)

    # 5. Milky Way: band + seeded grain
    rng = random.Random(out['seed'])
    band = []
    for l_deg in range(0, 360, 3):
        for b_deg in range(-12, 13, 3):
            g = ephem.Galactic(math.radians(l_deg), math.radians(b_deg))
            eq = ephem.Equatorial(g)
            band.append({
                'ra': round(math.degrees(float(eq.ra)), 2),
                'dec': round(math.degrees(float(eq.dec)), 2)
            })
    grain = []
    for _ in range(900):
        l = rng.uniform(0, 360)
        b = rng.gauss(0, 5.5)
        if abs(b) > 14:
            continue
        g = ephem.Galactic(math.radians(l), math.radians(b))
        eq = ephem.Equatorial(g)
        grain.append({
            'ra': round(math.degrees(float(eq.ra)), 2),
            'dec': round(math.degrees(float(eq.dec)), 2),
            'a': round(rng.uniform(0.25, 0.85), 2)
        })
    out['mw_band'] = band
    out['mw_grain'] = grain

    # 6. Phase strip (progression across key dates)
    if date_str == '2026-09-19':
        strip_days = [19, 21, 23, 25, 27]
    elif date_str == '2026-09-20':
        strip_days = [20, 22, 24, 25, 27]
    elif day == 21:
        strip_days = [21, 23, 25, 27, 29]
    elif day == 22:
        strip_days = [22, 23, 25, 27, 29]
    elif day == 23:
        strip_days = [23, 24, 25, 27, 29]
    elif day == 24:
        strip_days = [24, 25, 26, 27, 29]
    elif day == 25:
        strip_days = [25, 26, 27, 28, 29]
    elif day == 26:
        strip_days = [26, 27, 28, 29, 30]
    else:
        strip_days = [day + i for i in range(5)]

    strip = []
    for sday in strip_days:
        s_date = local_dt.date() + datetime.timedelta(days=(sday - day))
        obs.date = datetime.datetime(s_date.year, s_date.month, s_date.day, 14, 30, 0)
        moon.compute(obs)
        item = {
            'date': f'{s_date.month:02d}-{s_date.day:02d}',
            'illum': round(moon.phase, 1)
        }
        if sday == day:
            if sday == 23:
                item['label'] = f"今晚(秋分) · {round(moon.phase)}%"
            elif sday == 25:
                item['label'] = f"今晚(中秋) · {round(moon.phase)}%"
            elif sday == 27:
                item['label'] = f"今晚(满月) · {round(moon.phase)}%"
            else:
                item['label'] = f"今晚 · {round(moon.phase)}%"
        elif sday == 23:
            item['label'] = f"秋分 · {round(moon.phase, 1)}%"
        elif sday == 25:
            item['label'] = f"中秋 · {round(moon.phase, 1)}%"
        elif sday == 27:
            item['label'] = f"满月 · {round(moon.phase, 1)}%"
        strip.append(item)
    obs.date = utc_dt
    moon.compute(obs)
    out['phase_strip'] = strip
    out['station_pass'] = []

    # 7. Panel lines
    l1 = f"今晚 {time_str} · 东部沿海（{lat}°N {lon}°E）· 全天拱极投影 · 星历：pyephem 本地计算"
    l2 = f"月亮：{round(moon_illum)}% {phase_short} · 月龄 {age_d:.1f} 天 · 距离 {moon_dist_km:,.0f} km · 高度 {moon_alt:.1f}°（{moon_az_zh}天空） · {moonset_str}"
    if moon_sat_sep <= 12.0:
        sat_event = f"土星伴月（相距 {moon_sat_sep:.1f}°）"
    else:
        sat_event = "全夜可见"
    l3 = f"土星：{sat_az_zh} {round(sat_alt)}° · {sat.mag:.1f} 等 · {sat_event} · 夏季大三角西斜 · 飞马四边形高悬 · 银河斜贯天顶"
    days_to_midautumn = (datetime.date(2026, 9, 25) - local_dt.date()).days
    days_to_equinox = (datetime.date(2026, 9, 23) - local_dt.date()).days

    if date_str == '2026-09-19':
        l4 = "上弦精确时刻：今日 04:43 · 农历八月初九 · 中秋 09-25，满月时刻却在 09-27 凌晨 00:48（八月十七）"
    elif date_str == '2026-09-23':
        l4 = "今日 08:05 秋分（太阳黄经 180° · 昼夜平分）· 距中秋（09-25 望夕）还有 2 天 · 满月 09-27 凌晨 00:48"
    elif date_str == '2026-09-25':
        l4 = "农历八月十五 · 今夕中秋望夕（月出东南）· 满月精确时刻在 09-27 凌晨 00:48（十五的月亮十七圆）"
    elif days_to_midautumn > 0:
        if days_to_equinox > 0:
            l4 = f"农历八月{lunar_day_str} · 距中秋（09-25 望夕）还有 {days_to_midautumn} 天 · 距秋分（09-23 08:05）还有 {days_to_equinox} 天 · 满月 09-27 凌晨 00:48"
        else:
            l4 = f"农历八月{lunar_day_str} · 距中秋（09-25 望夕）还有 {days_to_midautumn} 天 · 满月精确时刻 09-27 凌晨 00:48（八月十七）"
    else:
        l4 = f"农历八月{lunar_day_str} · 满月时刻 09-27 凌晨 00:48（八月十七）· 月相渐过极值"

    out['panel_lines'] = [
        [l1, 20, 'ink'],
        [l2, 17, 'dim'],
        [l3, 17, 'dim'],
        [l4, 17, 'gold']
    ]

    # 8. ISS pass (graceful fallback)
    out['iss'] = []
    return out

def render_template(data, template_path, output_path=None):
    template_text = Path(template_path).read_text(encoding='utf-8')
    data_json_str = json.dumps(data, ensure_ascii=False)
    rendered = template_text.replace('__DATA__', data_json_str)
    if output_path:
        Path(output_path).write_text(rendered, encoding='utf-8')
    return rendered

def main():
    parser = argparse.ArgumentParser(description="Generate tonight-sky astronomical poster data and HTML.")
    parser.add_argument("--date", default="2026-09-20", help="Target date YYYY-MM-DD (default: 2026-09-20)")
    parser.add_argument("--time", default="22:30", help="Target time HH:MM (default: 22:30)")
    parser.add_argument("--lat", default="31.23", help="Observer latitude (default: 31.23)")
    parser.add_argument("--lon", default="121.47", help="Observer longitude (default: 121.47)")
    parser.add_argument("--out", default=str(DIR / "sky-data.json"), help="Output JSON path")
    parser.add_argument("--sketch-out", default=str(DIR / "sketch.html"), help="Output rendered HTML path")
    parser.add_argument("--template", default=str(DIR / "sketch_template.html"), help="Template HTML path")

    args = parser.parse_args()
    data = compute_sky_data(date_str=args.date, time_str=args.time, lat=args.lat, lon=args.lon)

    out_json_path = Path(args.out)
    with open(out_json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Wrote {out_json_path} (stars={len(data['stars'])}, mw={len(data['mw_band'])+len(data['mw_grain'])})")

    tpl_path = Path(args.template)
    if tpl_path.exists():
        rendered = render_template(data, tpl_path, args.sketch_out)
        print(f"Rendered {args.sketch_out} ({len(rendered)} chars)")

if __name__ == "__main__":
    main()
