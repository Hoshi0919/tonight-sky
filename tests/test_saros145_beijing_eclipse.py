import pytest
import math
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from saros145_beijing_eclipse_2035 import (
    compute_saros145_harmonics,
    compute_beijing_totality_contacts,
    compute_china_corridor_stations,
    compute_totality_daytime_sky,
    generate_report,
    SAROS_145_CATALOG,
)


def test_saros145_harmonics():
    hm = compute_saros145_harmonics()
    # 223 朔望月 ~ 6585.32 日
    assert 6585.0 < hm["synodic_period_days"] < 6586.0
    # 交点月差值 < 1.0 小时
    assert abs(hm["draconic_diff_hours"]) < 1.0
    # 近点月差值 < 6.0 小时
    assert abs(hm["anomalistic_diff_hours"]) < 6.0
    # 沙罗余数时间约 7.7 小时 (7h 43m)
    assert 7.5 < hm["saros_extra_hours"] < 8.0
    # 单次西偏角 ~ 115° 至 120°
    assert 112.0 < hm["longitude_shift_west_deg"] < 120.0
    # 三倍沙罗纽康转轮周期 ~ 54.1 年 (19755.96 日)
    assert 53.8 < hm["exeligmos_years"] < 54.5
    assert 19750.0 < hm["exeligmos_days"] < 19760.0


def test_saros145_catalog_and_progression():
    assert len(SAROS_145_CATALOG) == 4
    nums = [c["saros_num"] for c in SAROS_145_CATALOG]
    assert nums == [21, 22, 23, 24]

    dates = [c["date"] for c in SAROS_145_CATALOG]
    assert dates == ["1999-08-11", "2017-08-21", "2035-09-02", "2053-09-12"]

    # 持续时间随着沙罗家族迈向成熟单调递增
    durations = [c["duration_sec"] for c in SAROS_145_CATALOG]
    assert durations == [143, 160, 174, 184]
    for i in range(len(durations) - 1):
        assert durations[i] < durations[i + 1]


def test_beijing_totality_contacts_chronology():
    bj = compute_beijing_totality_contacts()
    contacts = bj["contacts"]

    assert "07:24" in contacts["C1_first_contact"]
    assert "08:32" in contacts["C2_totality_begins"]
    assert "08:33" in contacts["Max_greatest_eclipse"]
    assert "08:34" in contacts["C3_totality_ends"]
    assert "09:50" in contacts["C4_fourth_contact"]

    # 全食时长约为 102 秒 (1 分 42 秒)
    dur = bj["totality_duration_seconds"]
    assert 95.0 <= dur <= 110.0
    assert "1分42秒" in bj["totality_duration_str"]

    # 全过程时长 ~ 146 分钟 (约 2.43 小时)
    assert 140.0 <= bj["total_eclipse_span_minutes"] <= 150.0

    # 食甚时太阳仰角位于 31.0° ~ 32.5° 黄金地景构图高度
    assert 31.0 <= bj["sun_altitude_deg"] <= 32.5
    # 方位角东南偏东 (105° ~ 110°)
    assert 105.0 <= bj["sun_azimuth_deg"] <= 110.0

    # 站心月/日视径比 > 1.02 (本影完全覆盖太阳光球)
    assert bj["moon_sun_diameter_ratio"] > 1.02
    assert bj["airmass"] < 2.10


def test_china_corridor_stations_partition():
    stations = compute_china_corridor_stations()
    station_map = {s["city"]: s for s in stations}

    # 全食带核心城市
    corridor_cities = [
        "Beijing (北京市区)",
        "Tianjin Jizhou (天津蓟州/盘山)",
        "Qinhuangdao (秦皇岛/山海关)",
        "Datong (山西大同)",
        "Tangshan (河北唐山)",
        "Jiuquan (甘肃酒泉)",
    ]
    for c in corridor_cities:
        assert c in station_map
        st = station_map[c]
        assert st["in_corridor"] is True
        assert st["type"] == "Total (全食)"
        assert st["totality_duration_sec"] >= 50.0

    # 天津蓟州与秦皇岛全食达到或超过 2 分钟 (120 秒)
    assert station_map["Tianjin Jizhou (天津蓟州/盘山)"]["totality_duration_sec"] >= 115.0
    assert station_map["Qinhuangdao (秦皇岛/山海关)"]["totality_duration_sec"] >= 120.0

    # 重点邻近偏食城市食分验证
    assert station_map["Zhangjiakou (河北张家口)"]["magnitude"] > 0.990
    assert station_map["Hohhot (内蒙古呼和浩特)"]["magnitude"] > 0.990
    assert station_map["Dandong (辽宁丹东)"]["magnitude"] > 0.990
    assert station_map["Dalian (辽宁大连)"]["magnitude"] > 0.980
    assert station_map["Chengde (河北承德)"]["magnitude"] > 0.980
    assert station_map["Yinchuan (宁夏银川)"]["magnitude"] > 0.950

    # 南方城市偏食食分
    assert station_map["Shanghai (上海)"]["magnitude"] > 0.700
    assert station_map["Xi'an (陕西西安)"]["magnitude"] > 0.800
    assert station_map["Chengdu (四川成都)"]["magnitude"] > 0.700
    assert 0.400 <= station_map["Guangzhou (广东广州)"]["magnitude"] <= 0.550


def test_totality_daytime_sky_configuration():
    sky = compute_totality_daytime_sky()
    obj_map = {o["name"]: o for o in sky}

    # 金星作为日冕旁最耀眼长庚星 (-3.82 等，角距 < 8.0°)
    venus = obj_map["Venus (金星/长庚)"]
    assert venus["apparent_magnitude"] < -3.5
    assert venus["angular_sep_from_sun_deg"] < 8.0
    assert venus["altitude_deg"] > 20.0

    # 轩辕十四 (Regulus) 在太阳旁 9° 左右
    regulus = obj_map["Regulus (轩辕十四 · 狮子座α)"]
    assert 1.2 <= regulus["apparent_magnitude"] <= 1.5
    assert regulus["angular_sep_from_sun_deg"] < 11.0
    assert regulus["altitude_deg"] > 35.0

    # 检查按与太阳角距严格升序排列
    seps = [o["angular_sep_from_sun_deg"] for o in sky]
    assert seps == sorted(seps)


def test_report_generation():
    rep = generate_report()
    assert "沙罗 145" in rep
    assert "2035 年 9 月 2 日" in rep
    assert "Beijing City Center" in rep
    assert "1分42秒" in rep
    assert "故宫角楼" in rep
    assert "Venus (金星/长庚)" in rep
