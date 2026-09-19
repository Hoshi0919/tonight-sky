#!/usr/bin/env python3
"""
tonight-sky: Generates sky-data.json and injects it into sketch.html.
Requires: ephem (uv run --with ephem python3 skygen.py)
"""

import datetime
import json
import math
import random
import sys
from pathlib import Path
import ephem

DIR = Path(__file__).resolve().parent

obs = ephem.Observer()
obs.lat, obs.lon, obs.elevation = '31.23', '121.47', 10
T0 = datetime.datetime(2026, 9, 19, 14, 30, 0)  # UTC == 22:30 CST
obs.date = T0

out = {
    't0_utc': '2026-09-19T14:30:00',
    'lat': 31.23,
    'lon': 121.47,
    'tz': 8
}

def radec(body):
    return (math.degrees(float(body.ra)), math.degrees(float(body.dec)))

# --- stars: curated named catalog, keep RA/Dec
names = [
    'Sirius','Canopus','Arcturus','Vega','Capella','Rigel','Procyon','Betelgeuse',
    'Achernar','Altair','Aldebaran','Antares','Spica','Pollux','Fomalhaut','Deneb',
    'Regulus','Castor','Shaula','Gacrux','Bellatrix','Elnath','Miaplacidus','Alnilam',
    'Alnair','Alnitak','Alioth','Dubhe','Mirfak','Wezen','Kaus Australis','Alkaid',
    'Sargas','Menkalinan','Atria','Alhena','Peacock','Alphecca','Rasalhague','Hamal',
    'Diphda','Mizar','Nunki','Mirach','Almach','Denebola','Markab','Enif','Scheat',
    'Sabik','Alcyone','Polaris','Sadr','Caph','Izar','Algol','Sadalsuud','Alcor',
    'Albireo','Gienah','Zosma','Kochab','Thuban','Unukalhai','Markeb','Aspidiske'
]
stars = []
for n in names:
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

# --- summer triangle
out['tri'] = ['Vega', 'Altair', 'Deneb']

# --- moon: RA/Dec and alt/az every 5 min (22:00 -> 24:00 CST)
moon = ephem.Moon()
track_radec = []
track_alt = []
t_start = datetime.datetime(2026, 9, 19, 14, 0, 0)
t_end = datetime.datetime(2026, 9, 19, 16, 0, 0)

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

obs.date = T0
moon.compute(obs)
out['moon_t0'] = {
    'alt': round(math.degrees(float(moon.alt)), 2),
    'az': round(math.degrees(float(moon.az)), 2),
    'illum': round(moon.phase, 1),
    'age_d': round(obs.date - ephem.previous_new_moon(obs.date), 2)
}
out['moon_track'] = track_radec
out['moon_track_alt'] = track_alt
out['moonset_local'] = str(ephem.localtime(obs.next_setting(moon)))[:16]
out['next_full_local'] = str(ephem.localtime(ephem.next_full_moon(obs.date)))[:16]

# --- saturn track
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

# --- milky way: galactic plane band + seeded grain
rng = random.Random(20260919)
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

# --- phase strip: upcoming days at 22:30 CST
strip = []
for day in [19, 21, 23, 25, 27]:
    obs.date = datetime.datetime(2026, 9, day, 14, 30, 0)
    moon.compute(obs)
    strip.append({'date': f'09-{day}', 'illum': round(moon.phase, 1)})
out['phase_strip'] = strip
out['station_pass'] = []

# --- ISS pass within window
try:
    import urllib.request
    tle = urllib.request.urlopen(
        'https://celestrak.org/NORAD/elements/gp.php?CATNR=25544&FORMAT=TLE',
        timeout=10
    ).read().decode().strip().splitlines()
    iss = ephem.readtle(tle[0], tle[1], tle[2])
    found = []
    t = T0
    for i in range(120):
        iss.compute(t)
        alt = math.degrees(float(iss.alt))
        s = ephem.Sun()
        s.compute(t)
        if alt > 10 and math.degrees(float(s.alt)) < -6:
            found.append({
                'local': str(ephem.localtime(t))[11:16],
                'alt': round(alt, 1),
                'az': round(math.degrees(float(iss.az)), 1),
                'mag': round(float(iss.mag), 1)
            })
        t = ephem.Date(t + 30.0 / 1440)
    out['iss'] = found[:12]
except Exception as e:
    out['iss'] = []

data_path = DIR / 'sky-data.json'
with open(data_path, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print(f"Wrote {data_path} (stars={len(stars)}, mw={len(band)+len(grain)})")

template_path = DIR / 'sketch_template.html'
if template_path.exists():
    sketch_path = DIR / 'sketch.html'
    template_text = template_path.read_text(encoding='utf-8')
    data_json_str = json.dumps(out, ensure_ascii=False)
    rendered = template_text.replace('__DATA__', data_json_str)
    sketch_path.write_text(rendered, encoding='utf-8')
    print(f"Rendered {sketch_path} ({len(rendered)} chars)")
