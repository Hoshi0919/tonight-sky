import ephem, datetime
obs = ephem.Observer()
moon, sun = ephem.Moon(), ephem.Sun()
UTC = datetime.timezone.utc
TZ = datetime.timezone(datetime.timedelta(hours=8))

def diff_at(dt_utc):
    obs.date = ephem.Date(dt_utc)  # naive datetime 按 UTC 解释
    moon.compute(obs); sun.compute(obs)
    lon1 = float(ephem.Ecliptic(moon).lon)
    lon2 = float(ephem.Ecliptic(sun).lon)
    return ((lon1 - lon2) % 6.283185307179586) * 57.29577951308232

a = datetime.datetime(2026, 9, 26, 16, 0)  # UTC
b = datetime.datetime(2026, 9, 26, 18, 0)
for _ in range(50):
    m = a + (b - a)/2
    if diff_at(m) < 180.0:
        a = m
    else:
        b = m
t = a + (b - a)/2
print('天文望:', t.replace(tzinfo=UTC).astimezone(TZ).strftime('%m-%d %H:%M:%S.%f')[:-3], 'CST  diff =', round(diff_at(t), 5))
