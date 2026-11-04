#!/usr/bin/env python3
"""
verify_sun_twilight.py — 对比 ephem 计算值与外部权威数据 (sunrise-sunset.org)
覆盖 2026 年 11 月整月（30天），统计日出、日落与暮光各阶段的秒级误差分布。
"""

import json
import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import ephem

DIR = Path(__file__).resolve().parent.parent
DATA_FILE = DIR / "tests" / "data" / "sun_twilight_2026_11_shanghai.json"

CST = ZoneInfo("Asia/Shanghai")
UTC = datetime.timezone.utc


def parse_iso(iso_str):
    return datetime.datetime.fromisoformat(iso_str).astimezone(UTC)


def evaluate_accuracy(use_correct_horizon=True):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    lat = str(data["latitude"])
    lon = str(data["longitude"])
    obs = ephem.Observer()
    obs.lat = lat
    obs.lon = lon
    obs.elevation = 4.0

    errors = {
        "sunset": [],
        "sunrise": [],
        "civil_dusk": [],
        "nautical_dusk": [],
        "astro_dusk": [],
        "astro_dawn": [],
    }

    sun = ephem.Sun()

    for rec in data["records"]:
        date_str = rec["date"]
        d = datetime.date.fromisoformat(date_str)
        noon_utc = datetime.datetime(d.year, d.month, d.day, 4, 0, tzinfo=UTC)

        # 外部真实值
        ext_sunset = parse_iso(rec["sunset"])
        ext_sunrise = parse_iso(rec["sunrise"])
        ext_civil_dusk = parse_iso(rec["civil_twilight_end"])
        ext_naut_dusk = parse_iso(rec["nautical_twilight_end"])
        ext_astro_dusk = parse_iso(rec["astronomical_twilight_end"])
        ext_astro_dawn = parse_iso(rec["astronomical_twilight_begin"])

        # 1. Sunset
        obs.horizon = "0" if use_correct_horizon else "-0:34"
        obs.date = ephem.Date(noon_utc)
        calc_sunset = obs.next_setting(sun).datetime().replace(tzinfo=UTC)
        err_sunset = abs((calc_sunset - ext_sunset).total_seconds())
        errors["sunset"].append(err_sunset)

        # 2. Sunrise
        # 前一个午夜开始寻日出
        midnight_utc = datetime.datetime(d.year, d.month, d.day, 0, 0, tzinfo=UTC) - datetime.timedelta(hours=8)
        obs.horizon = "0" if use_correct_horizon else "-0:34"
        obs.date = ephem.Date(midnight_utc)
        calc_sunrise = obs.next_rising(sun).datetime().replace(tzinfo=UTC)
        err_sunrise = abs((calc_sunrise - ext_sunrise).total_seconds())
        errors["sunrise"].append(err_sunrise)

        # 3. Civil Dusk (-6°)
        obs.horizon = "-6"
        obs.date = ephem.Date(noon_utc)
        calc_civil = obs.next_setting(sun, use_center=True).datetime().replace(tzinfo=UTC)
        errors["civil_dusk"].append(abs((calc_civil - ext_civil_dusk).total_seconds()))

        # 4. Nautical Dusk (-12°)
        obs.horizon = "-12"
        obs.date = ephem.Date(noon_utc)
        calc_naut = obs.next_setting(sun, use_center=True).datetime().replace(tzinfo=UTC)
        errors["nautical_dusk"].append(abs((calc_naut - ext_naut_dusk).total_seconds()))

        # 5. Astro Dusk (-18°)
        obs.horizon = "-18"
        obs.date = ephem.Date(noon_utc)
        calc_astro = obs.next_setting(sun, use_center=True).datetime().replace(tzinfo=UTC)
        errors["astro_dusk"].append(abs((calc_astro - ext_astro_dusk).total_seconds()))

        # 6. Astro Dawn (-18°)
        obs.horizon = "-18"
        obs.date = ephem.Date(midnight_utc)
        calc_astro_dawn = obs.next_rising(sun, use_center=True).datetime().replace(tzinfo=UTC)
        errors["astro_dawn"].append(abs((calc_astro_dawn - ext_astro_dawn).total_seconds()))

    stats = {}
    for k, v in errors.items():
        stats[k] = {
            "max_s": round(max(v), 1),
            "mean_s": round(sum(v) / len(v), 1),
            "median_s": round(sorted(v)[len(v) // 2], 1),
        }
    return stats


def main():
    print("=== 对比 1: 旧配置 (含 -0:34 冗余大气折射) ===")
    old_stats = evaluate_accuracy(use_correct_horizon=False)
    for k, v in old_stats.items():
        print(f"  {k:15s}: max={v['max_s']:6.1f}s, mean={v['mean_s']:5.1f}s, median={v['median_s']:5.1f}s")

    print("\n=== 对比 2: 新配置 (标准物理地平线 horizon='0') ===")
    new_stats = evaluate_accuracy(use_correct_horizon=True)
    for k, v in new_stats.items():
        print(f"  {k:15s}: max={v['max_s']:6.1f}s, mean={v['mean_s']:5.1f}s, median={v['median_s']:5.1f}s")


if __name__ == "__main__":
    main()
