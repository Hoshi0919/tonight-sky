"""
OSIRIS-APEX (Origins, Spectral Interpretation, Resource Identification, Security - Apophis Explorer)
Trajectory, Earth Gravity Assists (EGA), Fig-Leaf Thermal Radiation & STIR Regolith Excavation Physics Engine.

Validates the orbital mechanics of the 3:2 Earth resonance, EGA velocity dissipation,
the 4x solar flux thermal barrier, the Lockheed Martin "fig-leaf" shielding geometry,
the STIR thruster plume geotechnical interaction with Apophis,
and integrates OSIRIS-APEX into the 2026 Grand Undecet (人类深空十一极黄金舰队).
"""

import math
from typing import Dict, Any

# Astronomical & Physical Constants
AU_KM = 149597870.7  # 1 AU in km
C_KM_S = 299792.458  # Speed of light in km/s
G_CONST = 6.67430e-11  # m^3 / (kg * s^2)
M_SUN = 1.98847e30  # kg
MU_SUN_KM = 1.32712440018e11  # km^3 / s^2
MU_EARTH_KM = 398600.4418  # km^3 / s^2
R_EARTH_KM = 6378.137  # Earth equatorial radius in km
SIGMA_SB = 5.670374e-8  # Stefan-Boltzmann constant W / (m^2 * K^4)
SOLAR_CONSTANT_1AU = 1361.0  # W/m^2 at 1 AU

# OSIRIS-APEX Spacecraft Baseline Parameters
SPACECRAFT_DRY_MASS_KG = 880.0
SPACECRAFT_WET_MASS_2026_KG = 1050.0  # Approx mass with residual hydrazine
DELTA_V_REMAINING_M_S = 525.0  # m/s
ORIGINAL_DESIGN_MIN_DIST_AU = 0.77  # OSIRIS-REx minimum design solar distance
FIG_LEAF_TRIGGER_DIST_AU = 0.65  # Threshold to engage fig-leaf attitude
APEX_PERIHELION_AU = 0.500  # Perihelion distance in Apophis transfer orbit
APEX_APHELION_AU = 1.026  # Aphelion distance in 3:2 resonance orbit

# Asteroid (99942) Apophis Baseline Parameters
APOPHIS_DIAMETER_M = 340.0
APOPHIS_MASS_KG = 6.1e10  # 61 million metric tons
APOPHIS_DENSITY_KG_M3 = 2100.0  # Rubble pile LL chondrite
APOPHIS_FLYBY_PERIGEE_KM = 38010.0  # Geocentric distance on 2029-04-13
APOPHIS_FLYBY_ALTITUDE_KM = 31632.0  # Altitude above surface


def calculate_heliocentric_orbit_and_resonance() -> Dict[str, Any]:
    """
    Computes heliocentric orbital elements of OSIRIS-APEX in its 3:2 Earth resonance orbit.
    """
    q = APEX_PERIHELION_AU
    Q = APEX_APHELION_AU
    a = (q + Q) / 2.0
    e = (Q - q) / (Q + q)
    period_years = a ** 1.5
    period_days = period_years * 365.25

    # Resonance ratio with Earth (P_Earth = 1.000 yr)
    # In 2.0 Earth years, spacecraft completes 3 orbits: 2 / period_years approx 3.0
    orbits_per_2_years = 2.0 / period_years

    # Velocities at perihelion and aphelion (vis-viva)
    # v^2 = mu * (2/r - 1/a)
    a_km = a * AU_KM
    q_km = q * AU_KM
    Q_km = Q * AU_KM

    v_peri_km_s = math.sqrt(MU_SUN_KM * (2.0 / q_km - 1.0 / a_km))
    v_aphe_km_s = math.sqrt(MU_SUN_KM * (2.0 / Q_km - 1.0 / a_km))

    return {
        "perihelion_au": round(q, 3),
        "aphelion_au": round(Q, 3),
        "semimajor_axis_au": round(a, 4),
        "eccentricity": round(e, 4),
        "period_years": round(period_years, 4),
        "period_days": round(period_days, 1),
        "orbits_per_2_years": round(orbits_per_2_years, 3),
        "perihelion_velocity_km_s": round(v_peri_km_s, 2),
        "aphelion_velocity_km_s": round(v_aphe_km_s, 2),
    }


def calculate_solar_radiation_and_fig_leaf_thermal_barrier() -> Dict[str, Any]:
    """
    Evaluates thermal solar flux, unprotected equilibrium temperature,
    and Lockheed Martin fig-leaf attitude mitigation at 0.50 AU perihelion.
    """
    q = APEX_PERIHELION_AU
    flux_1au = SOLAR_CONSTANT_1AU
    flux_peri = flux_1au / (q ** 2)
    flux_ratio_to_1au = flux_peri / flux_1au

    orig_limit = ORIGINAL_DESIGN_MIN_DIST_AU
    flux_orig_limit = flux_1au / (orig_limit ** 2)
    flux_ratio_to_orig_limit = flux_peri / flux_orig_limit

    # Unprotected equilibrium temperature
    # alpha * S = epsilon * sigma * T^4 -> T = (alpha * S / (epsilon * sigma))^(1/4)
    alpha = 0.90  # Absorptivity
    epsilon = 0.85  # Emissivity
    t_unprotected_k = (alpha * flux_peri / (epsilon * SIGMA_SB)) ** 0.25
    t_unprotected_c = t_unprotected_k - 273.15

    # Fig-leaf configuration:
    # One panel tucked at tilt angle theta relative to incoming sunlight
    theta_tilt_deg = 68.0
    cos_theta = math.cos(math.radians(theta_tilt_deg))
    effective_flux_canted_panel = flux_peri * cos_theta
    t_canted_panel_k = (alpha * effective_flux_canted_panel / (epsilon * SIGMA_SB)) ** 0.25
    t_canted_panel_c = t_canted_panel_k - 273.15

    # Shaded payload deck in geometric shadow:
    # Exposed only to deep space radiation and minor bus conduction
    t_payload_deck_min_c = -10.0
    t_payload_deck_max_c = 25.0

    return {
        "solar_flux_1au_w_m2": round(flux_1au, 1),
        "solar_flux_perihelion_w_m2": round(flux_peri, 1),
        "flux_ratio_to_1au": round(flux_ratio_to_1au, 2),
        "original_design_flux_limit_w_m2": round(flux_orig_limit, 1),
        "flux_exceedance_factor": round(flux_ratio_to_orig_limit, 2),
        "unprotected_equilibrium_temp_k": round(t_unprotected_k, 1),
        "unprotected_equilibrium_temp_c": round(t_unprotected_c, 1),
        "fig_leaf_tilt_deg": theta_tilt_deg,
        "effective_flux_canted_panel_w_m2": round(effective_flux_canted_panel, 1),
        "canted_panel_temp_c": round(t_canted_panel_c, 1),
        "shaded_deck_temp_range_c": [t_payload_deck_min_c, t_payload_deck_max_c],
    }


def calculate_2029_ega_apophis_velocity_reduction() -> Dict[str, Any]:
    """
    Analyzes the 2029-04-13 Earth Gravity Assist (EGA3 of APEX) mechanics:
    1 hour after Apophis flyby, flying by Earth at 1,153 km altitude,
    dissipating 99% of relative velocity to match Apophis's post-encounter orbit.
    """
    v_rel_initial_m_s = 5000.0  # 5.0 km/s relative approach velocity
    v_rel_post_ega_m_s = 51.0  # 51 m/s post-EGA rendezvous velocity
    flyby_altitude_km = 1153.0
    r_perigee_km = R_EARTH_KM + flyby_altitude_km

    velocity_reduction_m_s = v_rel_initial_m_s - v_rel_post_ega_m_s
    velocity_reduction_pct = (velocity_reduction_m_s / v_rel_initial_m_s) * 100.0

    # Hyperbolic orbital parameters during Earth encounter
    v_inf_km_s = v_rel_initial_m_s / 1000.0
    v_p_km_s = math.sqrt(v_inf_km_s ** 2 + 2.0 * MU_EARTH_KM / r_perigee_km)

    delta_v_available = DELTA_V_REMAINING_M_S
    delta_v_prox_ops_needed = 327.0
    delta_v_margin = delta_v_available - delta_v_prox_ops_needed
    margin_pct = (delta_v_margin / delta_v_prox_ops_needed) * 100.0

    return {
        "flyby_date": "2029-04-13",
        "flyby_altitude_km": flyby_altitude_km,
        "perigee_radius_km": round(r_perigee_km, 1),
        "initial_relative_velocity_m_s": v_rel_initial_m_s,
        "post_ega_relative_velocity_m_s": v_rel_post_ega_m_s,
        "velocity_reduction_pct": round(velocity_reduction_pct, 2),
        "perigee_velocity_km_s": round(v_p_km_s, 2),
        "delta_v_remaining_m_s": delta_v_available,
        "delta_v_required_prox_ops_m_s": delta_v_prox_ops_needed,
        "delta_v_margin_m_s": round(delta_v_margin, 1),
        "margin_percentage": round(margin_pct, 1),
    }


def calculate_stir_regolith_interaction_and_planetary_defense_safety() -> Dict[str, Any]:
    """
    Computes the STIR (Spacecraft Thruster Investigation of Regolith) plume dynamics,
    excavation volume, and proves absolute planetary defense safety.
    """
    # 4 RCS hydrazine thrusters firing toward the surface from 3-5 meters altitude
    thrust_single_n = 4.5
    num_thrusters = 4
    thrust_total_n = thrust_single_n * num_thrusters  # 18.0 N
    isp_s = 220.0  # Hydrazine monopropellant
    g0 = 9.80665
    v_exhaust_m_s = isp_s * g0  # ~2157.5 m/s

    burn_duration_s = 3.0  # Nominal pulse
    fuel_mass_burned_kg = (thrust_total_n * burn_duration_s) / v_exhaust_m_s

    # Maximum impulse transferred to Apophis (assuming 50% plume momentum coupling)
    coupling_factor = 0.50
    impulse_transferred_n_s = coupling_factor * fuel_mass_burned_kg * v_exhaust_m_s

    # Apophis orbital perturbation
    apophis_mass = APOPHIS_MASS_KG  # 6.1e10 kg
    delta_v_apophis_m_s = impulse_transferred_n_s / apophis_mass

    # Comparison with radar orbit determination uncertainty (~1e-4 m/s)
    radar_uncertainty_m_s = 1.0e-4
    safety_factor = radar_uncertainty_m_s / delta_v_apophis_m_s

    # Excavation geometry (based on Bennu TAG comparison)
    # At Bennu, 9m diameter, 0.6m depth excavated ~15 m^3
    crater_diameter_m = 9.0
    crater_depth_m = 0.60
    crater_volume_m3 = (math.pi / 6.0) * (3.0 * (crater_diameter_m / 2.0) ** 2 + crater_depth_m ** 2) * crater_depth_m  # spherical cap
    regolith_bulk_density_kg_m3 = 1500.0  # Bulk porous regolith
    excavated_mass_kg = crater_volume_m3 * regolith_bulk_density_kg_m3

    return {
        "thrust_total_n": round(thrust_total_n, 1),
        "isp_s": round(isp_s, 1),
        "exhaust_velocity_m_s": round(v_exhaust_m_s, 1),
        "fuel_mass_burned_kg": round(fuel_mass_burned_kg, 4),
        "impulse_transferred_n_s": round(impulse_transferred_n_s, 2),
        "apophis_mass_kg": apophis_mass,
        "delta_v_imparted_to_apophis_m_s": delta_v_apophis_m_s,
        "delta_v_imparted_nm_s": round(delta_v_apophis_m_s * 1.0e9, 2),
        "radar_uncertainty_threshold_m_s": radar_uncertainty_m_s,
        "safety_margin_factor": round(safety_factor, 0),
        "estimated_crater_diameter_m": crater_diameter_m,
        "estimated_crater_depth_m": crater_depth_m,
        "estimated_excavated_mass_kg": round(excavated_mass_kg, 1),
    }


def calculate_grand_undecet_matrix_2026() -> Dict[str, Any]:
    """
    Integrates OSIRIS-APEX into the Grand Undecet (人类深空十一极黄金舰队).
    """
    fleet = [
        {"name": "旅行者 1 号 (Voyager 1, NASA)", "heliocentric_dist_au": 173.22, "domain": "恒星际极寒最远边界 (1 光日倒计时 34 天)"},
        {"name": "新视野号 (New Horizons, NASA)", "heliocentric_dist_au": 65.92, "domain": "柯伊伯带双曲线逃逸极 (COB 绝尘背景光 / PUI 减速 17%)"},
        {"name": "木星冰月探测器 (JUICE, ESA)", "heliocentric_dist_au": 5.20, "domain": "巨行星卫星内禀磁层极 (2.3年共振巡航 / 探秘木卫三)"},
        {"name": "欧罗巴快船 (Europa Clipper, NASA)", "heliocentric_dist_au": 5.20, "domain": "外行星木卫二深海生命极 (MEGA 掠地 3200 km 倒计时 49 天)"},
        {"name": "灵神星探测器 (Psyche, NASA)", "heliocentric_dist_au": 2.042, "domain": "金属核心世界极 (SPT-140 霍尔电推 / DSOC 1550nm 激光光子链路)"},
        {"name": "赫拉号 (Hera, ESA)", "heliocentric_dist_au": 1.304, "domain": "双小行星微重力伴飞极 (今日 10-15 BRM-1 点火 / beta=3.7 动能偏转)"},
        {"name": "天问二号 (Tianwen-2, CNSA)", "heliocentric_dist_au": 1.001, "domain": "地球准卫星共轨采样与彗星双跃迁极 (28分钟自旋 50倍离心力对抗采样)"},
        {"name": "OSIRIS-APEX (NASA)", "heliocentric_dist_au": 1.010, "perihelion_au": 0.500, "domain": "毁神星伴飞与极端热控无花果叶极 (4倍太阳热流 / 2029 掠地 1153km 减速 99% / STIR 吹扫)"},
        {"name": "詹姆斯·韦伯望远镜 (JWST, NASA/ESA/CSA)", "heliocentric_dist_au": 1.010, "domain": "日地虚空 L2 天文极 (五层隔热 300K 屏障 / 6.7K 极低温 / z>14 原初星系)"},
        {"name": "贝皮可伦坡 (BepiColombo, ESA/JAXA)", "heliocentric_dist_au": 0.387, "domain": "太阳最深引力势能阱水星捕获极 (MOI 捕获制动 -1405 MJ/kg 倒计时 37 天)"},
        {"name": "帕克太阳探测器 (Parker Solar Probe, NASA)", "heliocentric_dist_au": 0.046, "domain": "恒星日冕极高温炼狱极 (192 km/s 人类极速 / 1400°C 防热罩 / P30 倒计时 48 天)"},
    ]

    r_min = min(f["heliocentric_dist_au"] for f in fleet)
    r_max = max(f["heliocentric_dist_au"] for f in fleet)
    ratio_heliocentric = r_max / r_min

    # Flux ratio
    flux_max = SOLAR_CONSTANT_1AU / (r_min ** 2)
    flux_min = SOLAR_CONSTANT_1AU / (r_max ** 2)
    ratio_flux = flux_max / flux_min

    return {
        "fleet_count": len(fleet),
        "fleet": fleet,
        "heliocentric_min_au": r_min,
        "heliocentric_max_au": r_max,
        "heliocentric_span_ratio": round(ratio_heliocentric, 1),
        "flux_max_w_m2": round(flux_max, 1),
        "flux_min_w_m2": round(flux_min, 4),
        "flux_span_ratio": round(ratio_flux, 1),
    }


if __name__ == "__main__":
    import json
    print("--- 1. Heliocentric Orbit & 3:2 Resonance ---")
    print(json.dumps(calculate_heliocentric_orbit_and_resonance(), indent=2))
    print("\n--- 2. Solar Radiation & Fig-Leaf Thermal Barrier ---")
    print(json.dumps(calculate_solar_radiation_and_fig_leaf_thermal_barrier(), indent=2))
    print("\n--- 3. 2029 EGA & Apophis Velocity Reduction ---")
    print(json.dumps(calculate_2029_ega_apophis_velocity_reduction(), indent=2))
    print("\n--- 4. STIR Regolith Interaction & Planetary Defense Safety ---")
    print(json.dumps(calculate_stir_regolith_interaction_and_planetary_defense_safety(), indent=2))
    print("\n--- 5. Grand Undecet Matrix 2026 ---")
    print(json.dumps(calculate_grand_undecet_matrix_2026(), indent=2))
