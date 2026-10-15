"""
Unit tests for Solar Orbiter out-of-ecliptic polar dynamo, SolarBlack bone charcoal thermal shield,
coronal heating "campfires", and the 2026 Grand Tridecet (人类深空十三极黄金舰队) engine.
"""

import sys
import unittest
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.solar_orbiter_polar_dynamo_coronal_heating_engine import (
    calculate_solar_orbiter_orbit_and_vga_resonance,
    calculate_solarblack_bone_charcoal_thermal_barrier,
    calculate_remote_sensing_apertures_and_coronal_heating,
    calculate_polar_dynamo_and_stereoscopic_geometry,
    calculate_2026_grand_tridecet_fleet_matrix,
)


class TestSolarOrbiterPolarDynamoCoronalHeating(unittest.TestCase):
    def setUp(self):
        self.orbit = calculate_solar_orbiter_orbit_and_vga_resonance()
        self.thermal = calculate_solarblack_bone_charcoal_thermal_barrier()
        self.science = calculate_remote_sensing_apertures_and_coronal_heating()
        self.dynamo = calculate_polar_dynamo_and_stereoscopic_geometry()
        self.fleet = calculate_2026_grand_tridecet_fleet_matrix()

    def test_solar_orbiter_orbital_elements_and_vis_viva(self):
        """Verifies orbital geometry, 0.28 AU perihelion, and vis-viva velocity range."""
        self.assertEqual(self.orbit["perihelion_au"], 0.280)
        self.assertEqual(self.orbit["aphelion_au"], 0.880)
        self.assertAlmostEqual(self.orbit["semi_major_axis_au"], 0.580, places=2)
        self.assertAlmostEqual(self.orbit["eccentricity"], 0.5172, places=3)
        self.assertAlmostEqual(self.orbit["period_days"], 161.3, delta=1.0)

        # Perihelion speed ~ 69.3 km/s, aphelion speed ~ 22.1 km/s
        self.assertGreater(self.orbit["perihelion_speed_km_s"], 69.0)
        self.assertLess(self.orbit["perihelion_speed_km_s"], 70.0)
        self.assertGreater(self.orbit["aphelion_speed_km_s"], 21.5)
        self.assertLess(self.orbit["aphelion_speed_km_s"], 22.5)

    def test_venus_gravity_assist_resonance_and_vga5_countdown(self):
        """Verifies VGA resonance sequence and exact 69-day countdown to 2026-12-24 VGA5."""
        vga_list = self.orbit["vga_sequence"]
        self.assertEqual(len(vga_list), 8)
        self.assertEqual(self.orbit["current_inclination_deg"], 17.0)
        self.assertEqual(self.orbit["post_vga5_inclination_deg"], 24.0)
        self.assertEqual(self.orbit["max_extended_inclination_deg"], 33.5)

        # 69 days from 2026-10-16 to 2026-12-24
        self.assertEqual(self.orbit["days_to_vga5"], 69)
        self.assertEqual(self.orbit["vga5_date"], "2026-12-24")

    def test_solarblack_bone_charcoal_thermo_optical_equilibrium(self):
        """Verifies 17.36 kW/m² solar flux, SolarBlack properties, and 520°C thermal barrier."""
        self.assertAlmostEqual(self.thermal["perihelion_solar_flux_w_m2"], 17359.7, delta=5.0)
        self.assertAlmostEqual(self.thermal["flux_ratio_to_earth"], 12.76, delta=0.1)
        self.assertEqual(self.thermal["heat_shield_area_m2"], 7.44)
        self.assertAlmostEqual(self.thermal["total_incident_thermal_power_kw"], 129.2, delta=0.5)

        # SolarBlack alpha=0.93, epsilon=0.85
        self.assertEqual(self.thermal["solarblack_alpha"], 0.93)
        self.assertEqual(self.thermal["solarblack_epsilon"], 0.85)

        # Stefan-Boltzmann equilibrium ~ 760.8 K (+487.6°C) and design peak 520°C
        self.assertAlmostEqual(self.thermal["theoretical_equilibrium_temp_k"], 760.8, delta=2.0)
        self.assertAlmostEqual(self.thermal["theoretical_equilibrium_temp_c"], 487.6, delta=2.0)
        self.assertEqual(self.thermal["design_peak_temp_c"], 520.0)

    def test_vacuum_gap_and_bus_thermal_attenuation(self):
        """Verifies 40 cm vacuum gap and bus leakage heat suppressed to < 250 W."""
        self.assertEqual(self.thermal["shield_gap_cm"], 40)
        self.assertLess(self.thermal["heat_leakage_to_bus_w"], 250.0)
        self.assertGreater(self.thermal["thermal_attenuation_ratio"], 500.0)
        self.assertEqual(self.thermal["bus_operating_temp_range_c"], [-20.0, 50.0])

    def test_remote_sensing_suite_and_detector_cryogenic_cooling(self):
        """Verifies 6 remote-sensing telescopes, EUI 200 km/px resolution, and <= -60°C cryo-cooling."""
        self.assertEqual(self.science["telescope_count"], 6)
        telescope_names = [t["name"] for t in self.science["telescopes"]]
        self.assertIn("EUI", telescope_names)
        self.assertIn("PHI", telescope_names)
        self.assertIn("SPICE", telescope_names)
        self.assertIn("STIX", telescope_names)
        self.assertIn("Metis", telescope_names)
        self.assertIn("SoloHI", telescope_names)

        # EUI HRIEUV spatial resolution ~ 203 km/px
        self.assertAlmostEqual(self.science["eui_hrieuv_spatial_res_km_per_px"], 203.1, delta=2.0)
        self.assertEqual(self.science["detector_max_temp_c"], -60.0)

    def test_coronal_heating_campfire_micro_reconnection_mechanics(self):
        """Verifies campfire micro-flare energetics and coronal heating resolution."""
        self.assertEqual(self.science["campfire_min_energy_j"], 1.0e21)
        self.assertEqual(self.science["campfire_max_energy_j"], 1.0e24)
        self.assertGreaterEqual(self.science["campfire_power_law_index"], 2.0)
        self.assertGreaterEqual(self.science["campfires_supplied_flux_w_m2"], self.science["quiet_corona_heating_demand_w_m2"])
        self.assertTrue(self.science["coronal_heating_paradox_resolved"])

    def test_polar_dynamo_geometric_foreshortening_enhancement(self):
        """Verifies polar projection factor enhancement from 0.124 up to 0.401 and 0.544."""
        self.assertAlmostEqual(self.dynamo["foreshortening_ecliptic"], 0.1243, delta=0.005)
        self.assertAlmostEqual(self.dynamo["foreshortening_vga4_current"], 0.2879, delta=0.005)
        self.assertAlmostEqual(self.dynamo["foreshortening_vga5_dec2026"], 0.4006, delta=0.005)
        self.assertAlmostEqual(self.dynamo["foreshortening_extended"], 0.5436, delta=0.005)

        # > 3.2x enhancement for VGA5, > 4.3x for extended
        self.assertGreater(self.dynamo["improvement_vga5_ratio"], 3.20)
        self.assertGreater(self.dynamo["improvement_extended_ratio"], 4.30)
        self.assertEqual(self.dynamo["solar_cycle_period_years"], 11.0)
        self.assertEqual(self.dynamo["hale_magnetic_cycle_years"], 22.0)

    def test_2026_grand_tridecet_fleet_duality_and_extrema(self):
        """Verifies 13 flagships in the 2026 Grand Tridecet and extreme cross-domain physical bounds."""
        self.assertEqual(self.fleet["fleet_size"], 13)
        self.assertGreater(self.fleet["distance_span_ratio"], 3700.0)
        self.assertGreater(self.fleet["flux_drop_ratio_millions"], 14.0)
        self.assertGreater(self.fleet["speed_span_ratio"], 900000.0)
        self.assertGreater(self.fleet["temp_span_k"], 1670.0)

        # Heliophysics duality
        duality = self.fleet["solar_physics_duality"]
        self.assertIn("Parker Solar Probe", duality["in_situ_probe"])
        self.assertIn("Solar Orbiter", duality["remote_sensing_probe"])


if __name__ == "__main__":
    unittest.main()
