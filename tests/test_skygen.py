import unittest
import sys
import tempfile
import os
from pathlib import Path
import json

DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR))

try:
    import ephem
    HAS_EPHEM = True
except ImportError:
    HAS_EPHEM = False

import skygen

@unittest.skipUnless(HAS_EPHEM, "ephem is required for skygen tests")
class TestSkygen(unittest.TestCase):
    def test_compute_sky_data_2026_10_22(self):
        data = skygen.compute_sky_data(date_str="2026-10-22", time_str="22:30")
        self.assertAlmostEqual(data["moon_t0"]["illum"], 85.2, delta=0.5)
        self.assertAlmostEqual(data["moon_t0"]["alt"], 45.64, delta=0.5)
        self.assertIn("2026-10-23 02:45", data["moonset_local"])
        self.assertIn("九月十三", data.get("title_sub", ""))
        self.assertIn("2026-10-22", data.get("title_sub", ""))
        panel_lines = data.get("panel_lines", [])
        self.assertEqual(len(panel_lines), 4)
        self.assertIn("月船一号发射18周年成年礼", panel_lines[3][0])
        self.assertIn("M3水冰首探", panel_lines[3][0])
        self.assertIn("金星9号首张外星表面全景51周年", panel_lines[3][0])
        self.assertIn("距超级满月4天", panel_lines[3][0])
        self.assertEqual(len(data["phase_strip"]), 5)
        labels = [item.get("label", "") for item in data["phase_strip"]]
        self.assertTrue(any("超级满月" in l for l in labels))

    def test_compute_sky_data_2026_10_21(self):
        data = skygen.compute_sky_data(date_str="2026-10-21", time_str="22:30")
        self.assertAlmostEqual(data["moon_t0"]["illum"], 77.2, delta=0.5)
        self.assertAlmostEqual(data["moon_t0"]["alt"], 34.78, delta=0.5)
        self.assertIn("2026-10-22 01:46", data["moonset_local"])
        self.assertIn("九月十二", data.get("title_sub", ""))
        self.assertIn("2026-10-21", data.get("title_sub", ""))
        panel_lines = data.get("panel_lines", [])
        self.assertEqual(len(panel_lines), 4)
        self.assertIn("猎户座流星雨今夜极盛", panel_lines[3][0])
        self.assertIn("联盟号圭亚那首飞15周年", panel_lines[3][0])
        self.assertIn("联盟TM-33银禧25载", panel_lines[3][0])
        self.assertIn("CAPSTONE地月NRHO四周年", panel_lines[3][0])
        self.assertEqual(len(data["phase_strip"]), 5)
        labels = [item.get("label", "") for item in data["phase_strip"]]
        self.assertTrue(any("今晚(猎户极大)" in l for l in labels))
        self.assertTrue(any("超级满月" in l for l in labels))

    def test_compute_sky_data_2026_10_20(self):
        data = skygen.compute_sky_data(date_str="2026-10-20", time_str="22:30")
        self.assertAlmostEqual(data["moon_t0"]["illum"], 68.3, delta=0.5)
        self.assertAlmostEqual(data["moon_t0"]["alt"], 23.99, delta=0.5)
        self.assertIn("2026-10-21 00:47", data["moonset_local"])
        self.assertIn("九月十一", data.get("title_sub", ""))
        self.assertIn("2026-10-20", data.get("title_sub", ""))
        panel_lines = data.get("panel_lines", [])
        self.assertEqual(len(panel_lines), 4)
        self.assertIn("BepiColombo八载铸剑", panel_lines[3][0])
        self.assertIn("水星倒计时32天", panel_lines[3][0])
        self.assertIn("OSIRIS-REx", panel_lines[3][0])
        self.assertIn("距猎户座流星雨极大1天", panel_lines[3][0])
        self.assertIn("MMX火卫一采样", panel_lines[3][0])
        self.assertEqual(len(data["phase_strip"]), 5)
        labels = [item.get("label", "") for item in data["phase_strip"]]
        self.assertTrue(any("猎户极大" in l for l in labels))
        self.assertTrue(any("超级满月" in l for l in labels))

    def test_compute_sky_data_2026_10_19(self):
        data = skygen.compute_sky_data(date_str="2026-10-19", time_str="22:30")
        self.assertAlmostEqual(data["moon_t0"]["illum"], 59.0, delta=0.5)
        self.assertAlmostEqual(data["moon_t0"]["alt"], 13.41, delta=0.5)
        self.assertIn("2026-10-19 23:49", data["moonset_local"])
        self.assertIn("九月初十", data.get("title_sub", ""))
        self.assertIn("2026-10-19", data.get("title_sub", ""))
        panel_lines = data.get("panel_lines", [])
        self.assertEqual(len(panel_lines), 4)
        self.assertIn("TGO十周年", panel_lines[3][0])
        self.assertIn("IBEX", panel_lines[3][0])
        self.assertIn("ESCAPADE", panel_lines[3][0])
        self.assertIn("半百黄金舰队", panel_lines[3][0])
        self.assertIn("距猎户座流星雨2天", panel_lines[3][0])

    def test_compute_sky_data_2026_09_19(self):
        data = skygen.compute_sky_data(date_str="2026-09-19", time_str="22:30")
        self.assertIn("stars", data)
        self.assertGreater(len(data["stars"]), 50)
        self.assertIn("moon_t0", data)
        self.assertAlmostEqual(data["moon_t0"]["illum"], 57.1, delta=0.5)
        self.assertAlmostEqual(data["moon_t0"]["alt"], 5.76, delta=0.5)
        self.assertIn("23:08", data["moonset_local"])
        self.assertEqual(data["tri"], ["Vega", "Altair", "Deneb"])
        self.assertIn("phase_strip", data)
        self.assertGreaterEqual(len(data["phase_strip"]), 5)
        self.assertIn("上弦精确时刻", data["panel_lines"][3][0])

    def test_compute_sky_data_2026_09_20(self):
        data = skygen.compute_sky_data(date_str="2026-09-20", time_str="22:30")
        self.assertAlmostEqual(data["moon_t0"]["illum"], 66.3, delta=0.5)
        self.assertAlmostEqual(data["moon_t0"]["alt"], 14.73, delta=0.5)
        # Moon sets after midnight on Sep 21
        self.assertIn("2026-09-21 00:0", data["moonset_local"])
        self.assertIn("八月初十", data.get("title_sub", ""))
        self.assertIn("2026-09-20", data.get("title_sub", ""))
        
        # Check panel lines
        panel_lines = data.get("panel_lines", [])
        self.assertEqual(len(panel_lines), 4)
        self.assertIn("66%", panel_lines[1][0])
        self.assertIn("401", panel_lines[1][0])
        self.assertIn("距中秋（09-25 望夕）还有 5 天", panel_lines[3][0])

    def test_compute_sky_data_2026_09_22(self):
        data = skygen.compute_sky_data(date_str="2026-09-22", time_str="22:30")
        self.assertAlmostEqual(data["moon_t0"]["illum"], 83.0, delta=0.5)
        self.assertAlmostEqual(data["moon_t0"]["alt"], 32.73, delta=0.5)
        # Moon sets at 02:02 on Sep 23
        self.assertIn("2026-09-23 02:02", data["moonset_local"])
        self.assertIn("八月十二", data.get("title_sub", ""))
        self.assertIn("2026-09-22", data.get("title_sub", ""))
        
        # Check panel lines
        panel_lines = data.get("panel_lines", [])
        self.assertEqual(len(panel_lines), 4)
        self.assertIn("83%", panel_lines[1][0])
        self.assertIn("393", panel_lines[1][0])
        self.assertIn("距中秋（09-25 望夕）还有 3 天", panel_lines[3][0])
        self.assertIn("距秋分（09-23 08:05）还有 1 天", panel_lines[3][0])

    def test_compute_sky_data_2026_09_21(self):
        data = skygen.compute_sky_data(date_str="2026-09-21", time_str="22:30")
        self.assertAlmostEqual(data["moon_t0"]["illum"], 75.1, delta=0.5)
        self.assertAlmostEqual(data["moon_t0"]["alt"], 23.77, delta=0.5)
        # Moon sets at 01:03 on Sep 22
        self.assertIn("2026-09-22 01:03", data["moonset_local"])
        self.assertIn("八月十一", data.get("title_sub", ""))
        self.assertIn("2026-09-21", data.get("title_sub", ""))
        
        # Check panel lines
        panel_lines = data.get("panel_lines", [])
        self.assertEqual(len(panel_lines), 4)
        self.assertIn("75%", panel_lines[1][0])
        self.assertIn("397", panel_lines[1][0])
        self.assertIn("距中秋（09-25 望夕）还有 4 天", panel_lines[3][0])

    def test_phase_strip_progression(self):
        data = skygen.compute_sky_data(date_str="2026-09-20", time_str="22:30")
        strip = data["phase_strip"]
        self.assertEqual(len(strip), 5)
        dates = [item["date"] for item in strip]
        self.assertEqual(dates, ["09-20", "09-22", "09-24", "09-25", "09-27"])
        # Illumination should be monotonically increasing toward full moon
        illums = [item["illum"] for item in strip]
        self.assertTrue(all(x <= y for x, y in zip(illums, illums[1:])))
        # Check special labels
        self.assertEqual(strip[0]["label"], "今晚 · 66%")
        self.assertEqual(strip[3]["label"], "中秋 · 98.6%")
        self.assertEqual(strip[4]["label"], f"满月 · {strip[4]['illum']}%")

    def test_render_template(self):
        data = skygen.compute_sky_data(date_str="2026-09-20", time_str="22:30")
        template_path = DIR / "sketch_template.html"
        self.assertTrue(template_path.exists())
        rendered = skygen.render_template(data, template_path)
        self.assertNotIn("__DATA__", rendered)
        self.assertIn("const DATA =", rendered)
        self.assertIn("2026-09-20", rendered)

    def test_compute_sky_data_2026_09_23_equinox(self):
        data = skygen.compute_sky_data(date_str="2026-09-23", time_str="22:30")
        self.assertAlmostEqual(data["moon_t0"]["illum"], 89.8, delta=0.5)
        self.assertIn("秋分", data.get("title_sub", ""))
        self.assertIn("八月十三", data.get("title_sub", ""))
        panel_lines = data.get("panel_lines", [])
        self.assertEqual(len(panel_lines), 4)
        self.assertIn("今日 08:05 秋分", panel_lines[3][0])
        self.assertIn("昼夜平分", panel_lines[3][0])
        strip = data["phase_strip"]
        self.assertEqual(len(strip), 5)
        self.assertEqual(strip[0]["date"], "09-23")
        self.assertIn("秋分", strip[0]["label"])
        self.assertEqual(strip[2]["label"], "中秋 · 98.6%")
        self.assertIn("满月", strip[3]["label"])

    def test_compute_sky_data_2026_09_25_midautumn(self):
        data = skygen.compute_sky_data(date_str="2026-09-25", time_str="22:30")
        self.assertAlmostEqual(data["moon_t0"]["illum"], 98.6, delta=0.5)
        self.assertIn("中秋节 · 望月", data.get("title_sub", ""))
        self.assertIn("八月十五", data.get("title_sub", ""))
        panel_lines = data.get("panel_lines", [])
        self.assertEqual(len(panel_lines), 4)
        self.assertIn("今夕中秋望夕", panel_lines[3][0])
        self.assertIn("十五的月亮十七圆", panel_lines[3][0])
        strip = data["phase_strip"]
        self.assertEqual(len(strip), 5)
        self.assertEqual(strip[0]["date"], "09-25")
        self.assertIn("今晚(中秋)", strip[0]["label"])
        self.assertIn("满月", strip[2]["label"])

    def test_compute_sky_data_2026_09_28_qiantang_tide(self):
        data = skygen.compute_sky_data(date_str="2026-09-28", time_str="22:30")
        self.assertAlmostEqual(data["moon_t0"]["illum"], 95.4, delta=0.5)
        self.assertFalse(data["moon_t0"]["is_waxing"])
        self.assertEqual(data["moon_t0"]["phase_short"], "亏凸")
        self.assertIn("八月十八", data.get("title_sub", ""))
        self.assertIn("钱塘大潮", data.get("title_sub", ""))
        self.assertIn("亏凸月", data.get("title_sub", ""))
        panel_lines = data.get("panel_lines", [])
        self.assertEqual(len(panel_lines), 4)
        self.assertIn("钱塘大潮正日", panel_lines[3][0])
        self.assertIn("1.64 μm/s²", panel_lines[3][0])
        strip = data["phase_strip"]
        self.assertEqual(len(strip), 5)
        self.assertEqual(strip[0]["date"], "09-28")
        self.assertEqual(strip[0]["label"], "今晚(大潮) · 95%")
        self.assertFalse(strip[0]["is_waxing"])

    def test_compute_sky_data_2026_09_29(self):
        data = skygen.compute_sky_data(date_str="2026-09-29", time_str="22:30")
        self.assertAlmostEqual(data["moon_t0"]["illum"], 89.5, delta=0.5)
        self.assertFalse(data["moon_t0"]["is_waxing"])
        self.assertEqual(data["moon_t0"]["phase_short"], "亏凸")
        self.assertIn("八月十九", data.get("title_sub", ""))
        self.assertIn("亏凸月", data.get("title_sub", ""))
        strip = data["phase_strip"]
        self.assertEqual(len(strip), 5)
        self.assertEqual(strip[0]["date"], "09-29")
        self.assertIn("今晚 · 90%", strip[0]["label"])
        self.assertFalse(strip[0]["is_waxing"])

    def test_phase_strip_all_days_consistency(self):
        for day in range(19, 30):
            date_str = f"2026-09-{day:02d}"
            data = skygen.compute_sky_data(date_str=date_str, time_str="22:30")
            strip = data["phase_strip"]
            self.assertEqual(len(strip), 5, f"Day {day} phase strip length != 5: {strip}")
            self.assertEqual(strip[0]["date"], f"09-{day:02d}", f"Day {day} first item mismatch")
            dates = [item["date"] for item in strip]
            # Strictly increasing dates
            self.assertEqual(dates, sorted(list(set(dates))), f"Day {day} dates not strictly ascending")

    def test_cli_execution_with_custom_paths(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out_json = Path(tmpdir) / "custom_sky.json"
            out_html = Path(tmpdir) / "custom_sketch.html"
            
            # Save old sys.argv
            old_argv = sys.argv
            try:
                sys.argv = [
                    "skygen.py",
                    "--date", "2026-09-20",
                    "--time", "22:30",
                    "--out", str(out_json),
                    "--sketch-out", str(out_html)
                ]
                skygen.main()
                self.assertTrue(out_json.exists())
                self.assertTrue(out_html.exists())
                
                with open(out_json, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                self.assertEqual(loaded["date_local"], "2026-09-20")
                self.assertIn("moon_t0", loaded)
            finally:
                sys.argv = old_argv


    def test_azimuth_to_zh(self):
        self.assertEqual(skygen.azimuth_to_zh(0), '正北')
        self.assertEqual(skygen.azimuth_to_zh(45), '东北')
        self.assertEqual(skygen.azimuth_to_zh(90), '正东')
        self.assertEqual(skygen.azimuth_to_zh(135), '东南')
        self.assertEqual(skygen.azimuth_to_zh(180), '正南')
        self.assertEqual(skygen.azimuth_to_zh(225), '西南')
        self.assertEqual(skygen.azimuth_to_zh(270), '正西')
        self.assertEqual(skygen.azimuth_to_zh(315), '西北')
        self.assertEqual(skygen.azimuth_to_zh(359), '正北')

    def test_get_phase_short(self):
        self.assertEqual(skygen.get_phase_short(1), '新月')
        self.assertEqual(skygen.get_phase_short(4), '蛾眉')
        self.assertEqual(skygen.get_phase_short(8), '上弦')
        self.assertEqual(skygen.get_phase_short(11), '盈凸')
        self.assertEqual(skygen.get_phase_short(15), '望月')
        self.assertEqual(skygen.get_phase_short(17), '满月')

    def test_dynamic_sky_azimuth_and_naming(self):
        # 09-21: Waxing gibbous in southwest
        d21 = skygen.compute_sky_data(date_str='2026-09-21', time_str='22:30')
        self.assertEqual(d21['moon_t0']['az_zh'], '西南')
        self.assertEqual(d21['moon_t0']['phase_short'], '盈凸')
        self.assertIn('ra', d21['moon_t0'])
        self.assertIn('dec', d21['moon_t0'])
        self.assertIn('西南天空', d21['panel_lines'][1][0])
        self.assertIn('东南', d21['panel_lines'][2][0])

        # 09-25: Mid-Autumn in due south (not southwest!)
        d25 = skygen.compute_sky_data(date_str='2026-09-25', time_str='22:30')
        self.assertEqual(d25['moon_t0']['az_zh'], '正南')
        self.assertEqual(d25['moon_t0']['phase_short'], '望月')
        self.assertEqual(d25['moon_label'], '月亮 · 99% 望月')
        self.assertIn('正南天空', d25['panel_lines'][1][0])
        self.assertIn('望月', d25['panel_lines'][1][0])

        # 09-27: Full moon climbing in southeast
        d27 = skygen.compute_sky_data(date_str='2026-09-27', time_str='22:30')
        self.assertEqual(d27['moon_t0']['az_zh'], '东南')
        self.assertEqual(d27['moon_t0']['phase_short'], '满月')
        self.assertEqual(d27['moon_label'], '月亮 · 99% 满月')
        self.assertIn('东南天空', d27['panel_lines'][1][0])
        self.assertIn('满月', d27['panel_lines'][1][0])

    def test_saturn_conjunction_and_panel_line3(self):
        # 09-21: Normal distance
        d21 = skygen.compute_sky_data(date_str='2026-09-21', time_str='22:30')
        self.assertIn('moon_sat_sep', d21)
        self.assertGreater(d21['moon_sat_sep'], 70)
        self.assertIn('全夜可见', d21['panel_lines'][2][0])
        self.assertIn('夏季大三角西斜', d21['panel_lines'][2][0])
        self.assertIn('飞马四边形高悬', d21['panel_lines'][2][0])

        # 09-27: Saturn-Moon conjunction during full moon (separation < 10 deg)
        d27 = skygen.compute_sky_data(date_str='2026-09-27', time_str='22:30')
        self.assertIn('moon_sat_sep', d27)
        self.assertLess(d27['moon_sat_sep'], 10.0)
        self.assertIn('土星伴月', d27['panel_lines'][2][0])
        self.assertIn(f"{d27['moon_sat_sep']:.1f}°", d27['panel_lines'][2][0])

    def test_rendered_template_astronomy_labels(self):
        d21 = skygen.compute_sky_data(date_str='2026-09-21', time_str='22:30')
        tpl_path = DIR / 'sketch_template.html'
        rendered = skygen.render_template(d21, tpl_path)
        self.assertIn('圆心 = 北天极', rendered)
        self.assertIn('外环 = 天赤道', rendered)
        self.assertIn('未来五日关键月相演进', rendered)
        self.assertNotIn('圆心 = 天顶', rendered)
        self.assertNotIn('map(p.az, 200, 265', rendered)

    def test_moon_waxing_calculation_and_template_shadow(self):
        d19 = skygen.compute_sky_data(date_str='2026-09-19', time_str='22:30')
        self.assertTrue(d19['moon_t0']['is_waxing'])

        d21 = skygen.compute_sky_data(date_str='2026-09-21', time_str='22:30')
        self.assertTrue(d21['moon_t0']['is_waxing'])

        d25 = skygen.compute_sky_data(date_str='2026-09-25', time_str='22:30')
        self.assertTrue(d25['moon_t0']['is_waxing'])

        # 09-27 22:30 is ~22h after exact full moon (00:48), so waning
        d27 = skygen.compute_sky_data(date_str='2026-09-27', time_str='22:30')
        self.assertFalse(d27['moon_t0']['is_waxing'])

        for item in d21['phase_strip']:
            self.assertIn('is_waxing', item)
            self.assertIsInstance(item['is_waxing'], bool)

        tpl_path = DIR / 'sketch_template.html'
        rendered = skygen.render_template(d21, tpl_path)
        self.assertIn('drawMoonPhaseDisc', rendered)
        self.assertNotIn('ellipse(Rm * k, 0, shadowW', rendered)

    def test_waxing_shadow_loop_direction_locked(self):
        """回归锁定：盈月暗影终结线弧必须与外缘弧反向闭合（bottom→top）。

        2026-09-22 曾因终结线循环写成递减（与外缘同向 top→bottom），
        两条弧同向平行导致暗影铺满整个左半盘（等效 k=0.5），且单点
        采样验证无法发现。修复后渲染验证：k=0.83/0.898/0.951/0.986
        的受光起点与理论终结线偏差 ≤1px。
        """
        tpl = (DIR / 'sketch_template.html').read_text(encoding='utf-8')
        # 定位盈月分支（注释「盈月：左半圆为外边缘」之后到亏月分支之前）
        start = tpl.index('盈月：左半圆为外边缘')
        seg = tpl[start:tpl.index('亏月：右半圆为外边缘')]
        # 终结线顶点行
        term_line = "vertex(-Rm * (2 * k - 1) * Math.cos(phi), Rm * Math.sin(phi));"
        self.assertIn(term_line, seg)
        # 终结线循环必须自下而上（i 递增），不得再出现递减循环
        loop_up = "for (let i = 0; i <= steps; i++)"
        self.assertIn(loop_up, seg)
        self.assertNotIn("for (let i = steps; i >= 0; i--)", seg)

    def test_october_23_24_panel_lines_and_strip(self):
        """验证 2026-10-23 与 2026-10-24 嫦娥五号T1/嫦娥一号/火星奥德赛号纪念与相带数据。"""
        d23 = skygen.compute_sky_data(date_str="2026-10-23", time_str="22:30")
        self.assertIn("嫦娥五号T1", d23["panel_lines"][3][0])
        self.assertIn("距超级满月3天", d23["panel_lines"][3][0])
        strip_dates_23 = [item["date"] for item in d23["phase_strip"]]
        self.assertEqual(strip_dates_23, ["10-23", "10-24", "10-25", "10-26", "10-28"])

        d24 = skygen.compute_sky_data(date_str="2026-10-24", time_str="22:30")
        self.assertIn("嫦娥一号", d24["panel_lines"][3][0])
        self.assertIn("火星奥德赛号", d24["panel_lines"][3][0])
        self.assertIn("距超级满月2天", d24["panel_lines"][3][0])
        strip_dates_24 = [item["date"] for item in d24["phase_strip"]]
        self.assertEqual(strip_dates_24, ["10-24", "10-25", "10-26", "10-27", "10-29"])

    def test_october_25_panel_lines_and_strip(self):
        """验证 2026-10-25 STEREO双星20周年/金星10号51周年与相带数据。"""
        d25 = skygen.compute_sky_data(date_str="2026-10-25", time_str="22:30")
        self.assertIn("STEREO双星发射20周年瓷婚", d25["panel_lines"][3][0])
        self.assertIn("金星10号着陆51周年", d25["panel_lines"][3][0])
        self.assertIn("望月前夕", d25["panel_lines"][3][0])
        strip_dates_25 = [item["date"] for item in d25["phase_strip"]]
        self.assertEqual(strip_dates_25, ["10-25", "10-26", "10-27", "10-28", "10-29"])

    def test_october_26_panel_lines_and_strip(self):
        """验证 2026-10-26 猎人满月正日/神舟十七号3周年/卡西尼泰坦Ta首探22周年与相带数据。"""
        d26 = skygen.compute_sky_data(date_str="2026-10-26", time_str="22:30")
        self.assertIn("猎人超级满月正日", d26["panel_lines"][3][0])
        self.assertIn("神舟十七号发射3周年", d26["panel_lines"][3][0])
        self.assertIn("卡西尼泰坦Ta首探22周年", d26["panel_lines"][3][0])
        self.assertIn("STEREO双星20周年正日", d26["panel_lines"][3][0])
        strip_dates_26 = [item["date"] for item in d26["phase_strip"]]
        self.assertEqual(strip_dates_26, ["10-26", "10-27", "10-28", "10-29", "10-30"])
        self.assertEqual(d26["phase_strip"][0]["label"], "今晚(超级满月) · 100%")

if __name__ == "__main__":
    unittest.main()
