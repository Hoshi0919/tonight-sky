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

    def test_phase_strip_all_days_consistency(self):
        for day in range(19, 28):
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

if __name__ == "__main__":
    unittest.main()
