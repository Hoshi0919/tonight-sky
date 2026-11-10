"""
双子座12号 (Gemini 12) 60 周年甲子钻禧纪念天体力学与航天先驱自动化测试集
"""

import sys
from pathlib import Path
import pytest
from datetime import datetime, timezone

DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR / 'scripts'))

from gemini12_diamond_jubilee_engine import Gemini12DiamondJubileeEngine

@pytest.fixture
def engine():
    return Gemini12DiamondJubileeEngine()

def test_gemini12_launch_and_phasing(engine):
    data = engine.compute_launch_and_phasing_dynamics()
    gemini = data['gemini_orbit']
    agena = data['agena_target_orbit']
    phasing = data['phasing_kinematics']

    # 验证双子座 12 号初始轨道参数
    assert abs(gemini['perigee_km'] - 160.8) < 0.5
    assert abs(gemini['apogee_km'] - 270.6) < 0.5
    assert 88.0 < gemini['period_minutes'] < 89.5
    assert 7700.0 < gemini['perigee_velocity_ms'] < 7900.0

    # 验证阿金纳目标飞行器 5001 轨道
    assert abs(agena['perigee_km'] - 298.3) < 0.5
    assert abs(agena['apogee_km'] - 302.2) < 0.5
    assert 90.0 < agena['period_minutes'] < 91.5

    # 验证相位角追赶速率优势
    assert phasing['orbital_period_difference_sec'] > 90.0 # 周期差 ~102.5s
    assert 6.0 < phasing['catchup_angular_rate_deg_orbit'] < 7.5 # 每圈追赶 ~6.8度
    assert 25.0 < phasing['apogee_circularization_delta_v_ms'] < 40.0

def test_aldrin_manual_rendezvous_hcw(engine):
    data = engine.compute_aldrin_manual_rendezvous_and_hcw()
    academic = data['aldrin_academic_background']
    radar = data['radar_failure_event']
    nav = data['manual_navigation_methodology']

    # 验证 Aldrin MIT 博士论文信息
    assert academic['institution'] == 'MIT (Massachusetts Institute of Technology)'
    assert 'Line-of-Sight Guidance Techniques' in academic['dissertation_title']
    assert academic['nickname'] == 'Dr. Rendezvous'

    # 验证雷达失效工况
    assert abs(radar['failure_range_nm'] - 5.9) < 0.1
    assert 10.5 < radar['failure_range_km'] < 11.5

    # 验证 HCW 相对轨道运动与 TPI 点火
    assert 0.00110 < nav['mean_orbital_motion_rad_s'] < 0.00120
    assert nav['tpi_transfer_angle_deg'] == 130.0
    assert 9.5 < nav['tpi_nominal_delta_v_ms'] < 12.0 # 34.7 ft/s ~ 10.58 m/s
    assert nav['docking_met'] == '04:14 (Orbit 3)'

def test_aldrin_eva_biomechanics_neutral_buoyancy(engine):
    data = engine.compute_aldrin_eva_biomechanics_and_neutral_buoyancy()
    eva = data['eva_breakdown']
    training = data['training_innovation']
    bio = data['biomechanical_dynamics']
    phys = data['physiological_comparison']

    # 验证三次出舱时长
    assert eva['eva1_standup_minutes'] == 149.0
    assert eva['eva2_umbilical_minutes'] == 126.0
    assert eva['eva3_standup_minutes'] == 55.0
    assert eva['total_eva_minutes'] == 330.0
    assert abs(eva['total_eva_hours'] - 5.50) < 0.01

    # 验证水下中性浮力与约束支架
    assert 'Neutral Buoyancy' in training['training_concept']
    assert 'Golden Slippers' in training['foot_restraints']
    assert training['handholds_count'] == 9

    # 验证反力矩物理学
    assert bio['unrestrained_angular_acceleration_rad_s2'] > 1.8
    assert bio['restrained_angular_acceleration_rad_s2'] == 0.0

    # 验证生理代谢对比 (Aldrin vs Cernan)
    assert phys['gemini_12_aldrin']['heart_rate_mean_bpm'] < 125.0
    assert phys['gemini_12_aldrin']['metabolic_rate_watts'] < 350.0
    assert phys['gemini_12_aldrin']['visor_fogging_percent'] == 0.0
    assert phys['gemini_9a_cernan']['visor_fogging_percent'] == 100.0
    assert phys['gemini_9a_cernan']['heart_rate_max_bpm'] == 180.0

def test_gravity_gradient_tether_dynamics(engine):
    data = engine.compute_gravity_gradient_tether_dynamics()
    mass = data['system_mass_kg']
    tether = data['tether_parameters']
    grav = data['gravity_gradient_physics']

    # 验证约化质量
    assert mass['gemini12_kg'] == 3763.0
    assert mass['agena_target_kg'] == 3200.0
    assert 1720.0 < mass['reduced_mass_kg'] < 1735.0

    # 验证系绳长度与材质
    assert tether['length_m'] == 30.0
    assert 'Dacron' in tether['material']

    # 验证重力梯度张力与天平动周期
    assert 0.18 < grav['theoretical_tension_newtons'] < 0.23 # ~0.208 N
    assert 50.0 < grav['pitch_libration_period_minutes'] < 55.0 # ~52.3 分钟
    assert grav['passive_stabilization_duration_minutes'] == 286.0
    assert grav['propellant_consumed_kg'] == 0.0

def test_program_gemini_milestone_and_jubilee(engine):
    data = engine.compute_program_gemini_milestone_and_jubilee()
    program = data['program_milestone']
    totals = data['gemini_program_grand_totals']
    jubilee = data['diamond_jubilee']

    # 验证任务持续时间与回收
    assert program['total_orbits'] == 59
    assert 94.0 < program['mission_duration_hours'] < 95.0
    assert program['recovery_ship'] == 'USS Wasp (CVS-18)'
    assert program['distance_from_target_km'] < 5.0

    # 验证双子座计划历史总计
    assert totals['total_crewed_flights'] == 10
    assert totals['total_dockings_achieved'] == 7
    assert totals['total_evas_conducted'] == 16

    # 验证 60 周年甲子钻禧
    assert jubilee['anniversary_years'] == 60
    assert jubilee['jubilee_name'] == 'Diamond Jubilee (六十甲子钻禧)'
    assert jubilee['days_since_launch'] == 21915

def test_gemini12_summary_report(engine):
    report = engine.generate_summary_report()
    assert '双子座12号 (Gemini 12)' in report
    assert 'James A. Lovell Jr.' in report
    assert "Buzz' Aldrin" in report
    assert '六分仪' in report
    assert '金色拖鞋' in report
    assert '30 米达克龙系绳' in report
    assert 'USS Wasp' in report
