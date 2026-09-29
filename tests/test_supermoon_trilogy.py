"""
test_supermoon_trilogy.py - Unit test suite for 2026 Supermoon Trilogy Engine
Tests anomalistic-synodic beat resonance, geocentric distances, topocentric parallax,
physical ratios against micromoon, and deep-sky conjunctions.
"""

import math
import sys
from pathlib import Path
import pytest

# Add project root and scripts dir to path
DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = DIR / 'scripts'
sys.path.insert(0, str(SCRIPTS_DIR))

import supermoon_trilogy_engine as engine


def test_constants_and_fmc_resonance():
    """Validates astronomical periods and anomalistic-synodic resonance mathematics."""
    assert 29.530 < engine.SYNODIC_MONTH_DAYS < 29.531
    assert 27.554 < engine.ANOMALISTIC_MONTH_DAYS < 27.555
    
    # FMC beat period: 411.78 days
    assert 411.5 < engine.FMC_BEAT_PERIOD_DAYS < 412.0
    # Equivalent to ~13.944 synodic months
    assert 13.90 < engine.FMC_BEAT_SYNODIC_RATIO < 14.00
    
    # Resonance drift: 14 synodic vs 15 anomalistic months
    drift_days = abs(14 * engine.SYNODIC_MONTH_DAYS - 15 * engine.ANOMALISTIC_MONTH_DAYS)
    drift_hours = drift_days * 24.0
    assert drift_hours < 3.0, f"Resonance drift too large: {drift_hours} hours"


def test_supermoon_trilogy_monotonicity():
    """Tests that full moon distances and time deltas tighten monotonically towards December."""
    events = [engine.compute_supermoon_event(w) for w in engine.TRILOGY_WINDOWS]
    assert len(events) == 3
    
    # Distance should decrease monotonically
    d1 = events[0]['fm_distance_km']
    d2 = events[1]['fm_distance_km']
    d3 = events[2]['fm_distance_km']
    assert d1 > d2 > d3, f"Distances not strictly decreasing: {d1}, {d2}, {d3}"
    assert d1 < 370000.0
    assert d2 < 362000.0
    assert d3 < 357000.0
    
    # Time delta between Syzygy and Perigee should decrease monotonically
    dt1 = events[0]['time_delta_hours']
    dt2 = events[1]['time_delta_hours']
    dt3 = events[2]['time_delta_hours']
    assert dt1 > dt2 > dt3, f"Time deltas not decreasing: {dt1}, {dt2}, {dt3}"
    assert dt3 < 8.0, f"December supermoon time delta should be < 8h: {dt3}h"
    
    # Apparent size should increase monotonically
    s1 = events[0]['apparent_size_arcmin']
    s2 = events[1]['apparent_size_arcmin']
    s3 = events[2]['apparent_size_arcmin']
    assert s1 < s2 < s3, f"Apparent sizes not increasing: {s1}, {s2}, {s3}"


def test_supermoon_3_extreme_and_ratios():
    """Tests Supermoon III extreme parameters and physical ratios vs 2026 micromoon."""
    sm3 = engine.compute_supermoon_event(engine.TRILOGY_WINDOWS[2])
    assert sm3['id'] == 'supermoon_3'
    assert '2026-12-24' in sm3['date_str']
    assert sm3['dec_deg'] > 27.0, f"Declination should be > +27°: {sm3['dec_deg']}"
    assert sm3['perigee_distance_km'] < 356700.0
    
    ratios = sm3['ratios_vs_micromoon']
    # Diameter increase > 13%
    assert ratios['diameter_percent'] > 13.0
    # Area illuminance increase > 28%
    assert ratios['area_illuminance_percent'] > 28.0
    # Tidal force ratio > 45%
    assert ratios['tidal_force_percent'] > 45.0


def test_topocentric_parallax_enhancement():
    """Tests topocentric parallax and apparent size enhancement for Chinese cities."""
    # Test for Shanghai
    topo_sh = engine.compute_topocentric_culmination('shanghai', '2026/12/23 20:00:00')
    assert topo_sh['altitude_deg'] > 85.0, f"Shanghai altitude should be > 85°: {topo_sh['altitude_deg']}"
    assert topo_sh['topocentric_distance_km'] < 351000.0
    assert topo_sh['topocentric_size_arcmin'] > 34.05
    
    # Test for Chengdu
    topo_cd = engine.compute_topocentric_culmination('chengdu', '2026/12/23 20:00:00')
    assert topo_cd['altitude_deg'] > 86.0
    assert topo_cd['topocentric_size_arcmin'] > 34.05
    
    # Test for Beijing
    topo_bj = engine.compute_topocentric_culmination('beijing', '2026/12/23 20:00:00')
    assert topo_bj['altitude_deg'] > 76.0
    assert topo_bj['topocentric_distance_km'] < 351000.0
    
    # All 6 cities
    for city_key in engine.CITIES:
        res = engine.compute_topocentric_culmination(city_key, '2026/12/23 20:00:00')
        assert res['altitude_deg'] > 60.0
        assert res['topocentric_size_arcmin'] > 34.00


def test_dec24_sky_conjunctions():
    """Tests celestial background and deep-sky conjunctions around Supermoon III."""
    conjunctions = engine.compute_deepsky_conjunctions_dec24()
    assert len(conjunctions) == 8
    
    # Check M35 open cluster
    m35 = next((c for c in conjunctions if 'M35' in c['name']), None)
    assert m35 is not None
    assert m35['separation_deg'] < 3.5, f"M35 separation should be < 3.5°: {m35['separation_deg']}"
    
    # Check surrounding winter hexagon stars
    star_names = ['北河二', '北河三', '参宿四', '五车二', '毕宿五', '南河三', '天狼星']
    for sn in star_names:
        s = next((c for c in conjunctions if sn in c['name']), None)
        assert s is not None
        assert 10.0 < s['separation_deg'] < 50.0


def test_full_report_structure():
    """Validates complete data structure generation."""
    data = engine.build_full_report_data()
    assert 'title' in data
    assert 'constants' in data
    assert len(data['trilogy_events']) == 3
    assert 'night_dec23_24' in data['supermoon_3_transits']
    assert len(data['supermoon_3_transits']['night_dec23_24']) == 6
    assert len(data['dec24_sky_conjunctions']) == 8
