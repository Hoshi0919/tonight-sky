import unittest
import sys
import math
from pathlib import Path

DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR))

try:
    import ephem
    HAS_EPHEM = True
except ImportError:
    HAS_EPHEM = False

from scripts import uranus_opposition_engine as uoe


@unittest.skipUnless(HAS_EPHEM, "ephem is required for uranus opposition tests")
class TestUranusOpposition(unittest.TestCase):
    def test_physical_constants(self):
        phys = uoe.URANUS_PHYSICAL
        self.assertEqual(phys["name"], "Uranus")
        self.assertEqual(phys["chinese_name"], "天王星")
        self.assertEqual(phys["discoverer"], "William Herschel")
        self.assertEqual(phys["discovery_date"], "1781-03-13")
        self.assertAlmostEqual(phys["axial_tilt_deg"], 97.77, delta=0.01)
        self.assertAlmostEqual(phys["orbital_period_years"], 84.02, delta=0.1)
        self.assertIn("CH4", phys["atmosphere"])

    def test_opposition_geometry(self):
        opp = uoe.compute_opposition_instant()
        self.assertIn("2026-11-26", opp["opp_time_cst"])
        self.assertIn("06:25", opp["opp_time_cst"])
        # Ecliptic longitude diff ~ 180 deg
        diff_lon = abs(opp["ecliptic_lon_deg"] - opp["sun_ecliptic_lon_deg"])
        self.assertAlmostEqual(diff_lon, 180.0, delta=0.05)
        # Phase angle near 0
        self.assertLess(opp["phase_angle_deg"], 0.05)
        # Visual magnitude
        self.assertAlmostEqual(opp["visual_mag"], 5.58, delta=0.05)
        # Size
        self.assertAlmostEqual(opp["angular_size_arcsec"], 3.82, delta=0.1)
        # Coordinates in Taurus
        self.assertTrue(opp["ra"].startswith("4:06"))
        self.assertTrue(opp["dec"].startswith("20:44"))

    def test_perigee_instant(self):
        peri = uoe.compute_perigee_instant()
        self.assertIn("2026-11-26", peri["perigee_time_cst"])
        self.assertAlmostEqual(peri["min_dist_au"], 18.444, delta=0.01)
        self.assertAlmostEqual(peri["light_time_minutes"], 153.39, delta=0.5)

    def test_retrograde_cycle(self):
        retro = uoe.compute_retrograde_cycle()
        self.assertIn("2026-09-11", retro["station1_time_cst"])
        self.assertIn("2027-02-08", retro["station2_time_cst"])
        self.assertAlmostEqual(retro["retrograde_duration_days"], 150.8, delta=2.0)
        self.assertAlmostEqual(retro["retrograde_arc_deg"], 3.95, delta=0.5)
        self.assertTrue(retro["station1_ra"].startswith("4:15"))
        self.assertTrue(retro["station2_ra"].startswith("3:58"))

    def test_ring_and_moons_projection(self):
        opp = uoe.compute_opposition_instant()
        opp_date = ephem.Date(opp["opp_time_utc"])
        proj = uoe.compute_ring_and_moons_projection(opp_date)

        self.assertAlmostEqual(proj["ring_opening_angle_deg"], 74.15, delta=1.0)
        self.assertAlmostEqual(proj["apparent_axis_ratio"], 0.962, delta=0.02)

        moons = proj["moons_projection"]
        self.assertEqual(len(moons), 5)
        moon_names = [m["name"] for m in moons]
        self.assertIn("Titania (天卫三)", moon_names)
        self.assertIn("Oberon (天卫四)", moon_names)

        titania = next(m for m in moons if "Titania" in m["name"])
        self.assertAlmostEqual(titania["mag"], 13.5, delta=0.2)
        self.assertAlmostEqual(titania["semi_major_arcsec"], 32.6, delta=1.0)

        oberon = next(m for m in moons if "Oberon" in m["name"])
        self.assertAlmostEqual(oberon["mag"], 13.7, delta=0.2)
        self.assertAlmostEqual(oberon["semi_major_arcsec"], 43.6, delta=1.5)

    def test_star_hopping_taurus_gate(self):
        opp = uoe.compute_opposition_instant()
        opp_date = ephem.Date(opp["opp_time_utc"])
        hops = uoe.compute_star_hopping_geometry(opp_date)

        self.assertGreaterEqual(len(hops), 8)
        # 43 Tau twin reference star
        star_43 = next(s for s in hops if "43 Tau" in s["name"])
        self.assertAlmostEqual(star_43["sep_deg"], 1.30, delta=0.05)
        self.assertAlmostEqual(star_43["mag"], 5.51, delta=0.05)

        # 37 Tau
        star_37 = next(s for s in hops if "37 Tau" in s["name"])
        self.assertAlmostEqual(star_37["sep_deg"], 1.42, delta=0.05)

        # Alcyone (Pleiades)
        alcyone = next(s for s in hops if "Alcyone" in s["name"])
        self.assertAlmostEqual(alcyone["sep_deg"], 5.34, delta=0.1)

        # Aldebaran
        aldebaran = next(s for s in hops if "Aldebaran" in s["name"])
        self.assertAlmostEqual(aldebaran["sep_deg"], 8.39, delta=0.1)

    def test_supermoon_conjunction(self):
        sm = uoe.compute_supermoon_conjunction()
        self.assertIn("2026-11-25 01:13", sm["conjunction_time_cst"])
        self.assertAlmostEqual(sm["min_sep_deg"], 5.09, delta=0.1)
        self.assertGreater(sm["moon_phase_pct"], 99.0)

    def test_cities_observing_window(self):
        cities = uoe.compute_cities_observing_window()
        self.assertEqual(len(cities), 5)
        gz = next(c for c in cities if "广州" in c["city"])
        self.assertAlmostEqual(gz["transit_alt_deg"], 87.6, delta=0.5)
        self.assertAlmostEqual(gz["air_mass_transit"], 1.00, delta=0.02)

        for c in cities:
            self.assertGreater(c["visible_hours"], 13.0)
            self.assertGreater(c["transit_alt_deg"], 65.0)
            self.assertLess(c["air_mass_transit"], 1.10)

    def test_full_pipeline_and_formatting(self):
        data = uoe.run_full_pipeline if hasattr(uoe, "run_full_pipeline") else uoe.run_full_uranus_pipeline()
        self.assertIn("opposition", data)
        self.assertIn("rings_and_moons", data)
        report = uoe.format_cli_report(data)
        self.assertIn("天王星", report)
        self.assertIn("射击靶心", report)
        self.assertIn("金牛座天门", report)


if __name__ == "__main__":
    unittest.main()
