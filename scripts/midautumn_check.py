#!/usr/bin/env python3
"""中秋望夕（2026-09-25 晚）月与土星核算 — 北京（39.9042N, 116.4074E）"""
import ephem
import datetime

obs = ephem.Observer()
obs.lat, obs.lon, obs.elevation = '39.9042', '116.4074', 44

TZ = datetime.timezone(datetime.timedelta(hours=8))

def cst(dt_utc):
    return dt_utc.astimezone(TZ)

fmt = '%m-%d %H:%M:%S'

print('== 朔望链条（北京时间）==')
t = datetime.datetime(2026, 9, 1, tzinfo=TZ)
nm_prev = ephem.previous_new_moon(ephem.Date(t - datetime.timedelta(days=1)))
fm = ephem.previous_full_moon(ephem.Date(t + datetime.timedelta(days=27)))
nm_next = ephem.next_new_moon(ephem.Date(t + datetime.timedelta(days=20)))
print('最近朔  :', cst(nm_prev.datetime()))
print('望(满月):', cst(fm.datetime()))
print('下次朔  :', cst(nm_next.datetime()))

print()
print('== 望夕当晚月亮（09-25）==')
obs.pressure = 1010  # 开启大气折射
obs.date = ephem.Date('2026/9/25 4:00:00')   # 北京 12:00
rise = obs.next_rising(ephem.Moon())
set_ = obs.next_setting(ephem.Moon(), start=rise)
print('月出:', cst(rise.datetime()), '  月落:', cst(set_.datetime()))

for h in (19, 20, 21, 22, 23):
    w = datetime.datetime(2026, 9, 25, h, 0, tzinfo=TZ)
    obs.date = w.astimezone(datetime.timezone.utc)
    m = ephem.Moon(obs)
    print(f'{h:02d}:00  高度 {float(m.alt)*57.29578:5.1f}°  方位 {float(m.az)*57.29578:5.1f}°  '
          f'照亮比 {m.phase:5.1f}%  视直径 {m.size}"  距离 {m.earth_distance*384400:.0f} km')

obs.date = ephem.Date('2026/9/25 4:00:00')
m = ephem.Moon(obs)
tr = obs.next_transit(m)
obs.date = tr
m.compute(obs)
print(f'月中天: {cst(tr.datetime())}  高度 {float(m.alt)*57.29578:.1f}°')

print()
print('== 望夕土星与月土角距 ==')
w = datetime.datetime(2026, 9, 25, 22, 0, tzinfo=TZ)
obs.date = w.astimezone(datetime.timezone.utc)
s = ephem.Saturn(obs)
m = ephem.Moon(obs)
sep = ephem.separation((m.ra, m.dec), (s.ra, s.dec))
print(f'土星 22:00  高度 {float(s.alt)*57.29578:5.1f}°  方位 {float(s.az)*57.29578:5.1f}°  星等 {s.mag}')
print(f'月与土星角距 {float(sep)*57.29578:.1f}°')

print()
print('== 照亮比随时间 ==')
for day, hh, mm in [(25, 20, 0), (25, 23, 0), (26, 2, 0), (26, 18, 30), (27, 0, 48)]:
    w = datetime.datetime(2026, 9, day, hh, mm, tzinfo=TZ)
    obs.date = w.astimezone(datetime.timezone.utc)
    m = ephem.Moon(obs)
    print(f'09-{day:02d} {hh:02d}:{mm:02d} 照亮 {m.phase:.2f}%')
