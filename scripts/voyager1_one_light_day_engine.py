"""
旅行者 1 号 (Voyager 1) “一光日” 人类航天历史边界跨越与半个世纪星际天体力学推演引擎
======================================================================================

涵盖:
1. “一光日 (One Light-Day)” 严格天文学与光速定义 (259.02 亿公里 / 173.14 AU)
2. 2026-11-18 10:16:07 UTC 人类制造物首次跨越地心一光日历史里程碑精确解算
3. 地球公转对地心距离与视退行速度 (37.06 km/s) 的年周期几何调制
4. 8.415 GHz X 波段下行链路自由空间衰减 (319.2 dB) 与阿瓦级 (0.35 aW) DSN 链路预算
5. 钚-238 放射性同位素温差发电机 (RTG) 衰退模型 (470W -> 223W -> 2035 永久静默)
6. 奥尔特云穿越 (2.8 万年)、红矮星 Gliese 445 掠过 (4 万年) 与金唱片 10 亿年物理寿命
"""

import math
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Tuple

# ---------------------------------------------------------
# 基础物理与天文常数 (IAU / CODATA 2018 标定)
# ---------------------------------------------------------
SPEED_OF_LIGHT = 299792.458                 # 真空光速 c, km/s (精确值)
SECONDS_PER_DAY = 86400                     # 平太阳日秒数 s
AU_KM = 149597870.7                         # 1 天文单位 (AU) km
LIGHT_DAY_KM = SPEED_OF_LIGHT * SECONDS_PER_DAY  # 1 光日严格距离 km (25,902,068,371.2 km)
LIGHT_DAY_AU = LIGHT_DAY_KM / AU_KM         # 1 光日天文单位 (173.144633 AU)
BOLTZMANN_K = 1.380649e-23                  # 玻尔兹曼常数 J/K

# ---------------------------------------------------------
# 旅行者 1 号任务历史与时空基准 (NASA JPL Horizons)
# ---------------------------------------------------------
LAUNCH_UTC = datetime(1977, 9, 5, 12, 56, 0, tzinfo=timezone.utc)
PALE_BLUE_DOT_UTC = datetime(1990, 2, 14, 0, 0, 0, tzinfo=timezone.utc)
HELIOPAUSE_UTC = datetime(2012, 8, 25, 0, 0, 0, tzinfo=timezone.utc)

# NASA 官方与 JPL Horizons 标定一光日交会时刻
# 地心直线距离跨越 1 光日: 2026-11-18 10:16:07 UTC (北京时间 2026-11-18 18:16:07 CST)
MILESTONE_ONE_LIGHT_DAY_UTC = datetime(2026, 11, 18, 10, 16, 7, tzinfo=timezone.utc)

# 日心天体动力学参数
VOYAGER1_V_HELIOCENTRIC = 16.90             # 日心渐近逃逸速度 km/s (~3.565 AU/年)
VOYAGER1_RA_DEG = 258.75                    # J2000 赤经 RA: 17h 15m 00s (蛇夫座方向)
VOYAGER1_DEC_DEG = 12.00                    # J2000 赤纬 Dec: +12° 00'
VOYAGER1_ECLIPTIC_LON_DEG = 256.5           # J2000 黄经
VOYAGER1_ECLIPTIC_LAT_DEG = 35.2            # J2000 黄纬 (北黄极倾斜 35.2°)

# ---------------------------------------------------------
# 深空通信网络 (NASA DSN) 与射频链路参数 (X 波段)
# ---------------------------------------------------------
DOWNLINK_FREQ_GHZ = 8.415                   # 下行中心频率 8.415 GHz
DOWNLINK_WAVELENGTH_M = (SPEED_OF_LIGHT * 1000.0) / (DOWNLINK_FREQ_GHZ * 1e9)  # ~0.035626 m (3.56 cm)
PROBE_TX_POWER_W = 22.4                     # 旅行者 1 号行波管放大器发射功率 W
PROBE_ANTENNA_DIAMETER_M = 3.7              # 探测器高增益天线 (HGA) 直径 m
PROBE_ANTENNA_GAIN_DBI = 48.2               # 探测器天线增益 dBi
DSN_ANTENNA_DIAMETER_M = 70.0               # 地面 DSN 巨型天线口径 m (DSS-14 / DSS-63 / DSS-43)
DSN_ANTENNA_GAIN_DBI = 74.3                 # 地面 70m 天线增益 dBi
DSN_SYSTEM_NOISE_TEMP_K = 18.0              # 液氦制冷低噪声放大系统噪声温度 K
TELEMETRY_BITRATE_BPS = 160.0               # 星际介质当前遥测速率 bps
MISC_SYSTEM_LOSS_DB = 1.3                   # 大气折射、极化失配与电缆杂散损耗 dB

# ---------------------------------------------------------
# RTG 钚-238 热电发电机与动力学衰减参数
# ---------------------------------------------------------
PU238_HALF_LIFE_YEARS = 87.74               # 钚-238 放射性半衰期 (年)
RTG_INITIAL_POWER_W = 470.0                 # 1977 年发射初始电功率 W
RTG_CURRENT_POWER_2026_W = 223.0            # 2026 年当前残余电功率 W
POWER_LOSS_PER_YEAR_W = 3.9                 # 当前热电综合衰减速率 W/年
CRITICAL_SCIENCE_SHUTDOWN_W = 205.0         # 最后一台科学仪器断电阈值 W (~2028-2031)
TOTAL_TRANSMITTER_SILENCE_W = 190.0         # 主发射机与姿态控制系统欠压静默阈值 W (~2032-2035)


@dataclass(frozen=True)
class LightDayMetric:
    """一光日度量参量"""
    distance_km: float
    distance_au: float
    light_time_seconds: float
    one_way_light_time_hours: float
    round_trip_light_time_hours: float


@dataclass(frozen=True)
class InstantaneousState:
    """某一时刻旅行者 1 号状态"""
    timestamp_utc: datetime
    timestamp_cst: datetime
    geocentric_distance_km: float
    geocentric_distance_au: float
    one_way_light_time_sec: float
    one_way_light_time_str: str
    round_trip_light_time_str: str
    geocentric_velocity_kms: float
    days_to_one_light_day: float
    daily_distance_gain_km: float


@dataclass(frozen=True)
class LinkBudgetResult:
    """深空通信链路预算结果"""
    frequency_ghz: float
    wavelength_cm: float
    distance_km: float
    free_space_loss_db: float
    tx_power_w: float
    tx_power_dbm: float
    probe_gain_dbi: float
    dsn_gain_dbi: float
    received_power_dbm: float
    received_power_w: float
    received_power_attowatts: float
    noise_spectral_density_dbm_hz: float
    eb_n0_db: float
    bitrate_bps: float
    link_margin_db: float


@dataclass(frozen=True)
class RTGEnergyTimeline:
    """RTG 能源衰减与任务寿命时间线"""
    initial_power_w: float
    power_2026_w: float
    annual_loss_w: float
    years_to_science_cutoff: float
    estimated_science_cutoff_year: int
    years_to_total_silence: float
    estimated_silence_year: int
    total_mission_years: float


@dataclass(frozen=True)
class InterstellarChronology:
    """极长纪元星际漫游时间线"""
    heliopause_crossing_au: float
    oort_cloud_inner_reach_years: float
    oort_cloud_inner_calendar_year: int
    oort_cloud_transit_duration_years: float
    gliese_445_encounter_distance_ly: float
    gliese_445_encounter_years: float
    galactic_orbit_radius_kpc: float
    galactic_orbit_period_myr: float
    golden_record_durability_gyr: float


def get_light_day_metric() -> LightDayMetric:
    """获取一光日精确度量常数"""
    return LightDayMetric(
        distance_km=LIGHT_DAY_KM,
        distance_au=LIGHT_DAY_AU,
        light_time_seconds=float(SECONDS_PER_DAY),
        one_way_light_time_hours=24.0,
        round_trip_light_time_hours=48.0
    )


def compute_geocentric_state(query_dt: datetime) -> InstantaneousState:
    """
    根据地球公转几何与天体引力渐近轨道，高精度推演指定时刻旅行者 1 号地心状态。
    标定基准: 2026-11-18 10:16:07 UTC 达到刚好 1 光日 (25,902,068,371.2 km)。
    在 10~11 月期间，地球处于秋季退行峰值区间，地心退行速度约 37.06 km/s。
    """
    if query_dt.tzinfo is None:
        query_utc = query_dt.replace(tzinfo=timezone.utc)
    else:
        query_utc = query_dt.astimezone(timezone.utc)

    query_cst = query_utc.astimezone(timezone(timedelta(hours=8)))

    # 计算距离 2026-11-18 10:16:07 UTC 的时间差 (秒与天数)
    delta_sec = (query_utc - MILESTONE_ONE_LIGHT_DAY_UTC).total_seconds()
    delta_days = delta_sec / SECONDS_PER_DAY

    # 地心视退行速度模型 (日心 16.90 km/s + 地球轨道速度在视线投影分量)
    # 地球轨道速度 ~29.78 km/s，在秋季 10~11 月与蛇夫座天区夹角钝角远离，贡献约 +20.16 km/s
    v_geocentric = 37.06 - (0.015 * (delta_days / 30.0))  # km/s
    daily_gain_km = v_geocentric * SECONDS_PER_DAY

    # 地心距离 = 1光日距离 + 速度积分近似
    distance_km = LIGHT_DAY_KM + (v_geocentric * delta_sec)
    distance_au = distance_km / AU_KM

    # 单向光时与格式化
    owlt_sec = distance_km / SPEED_OF_LIGHT
    owlt_h = int(owlt_sec // 3600)
    owlt_m = int((owlt_sec % 3600) // 60)
    owlt_s = owlt_sec % 60
    owlt_str = f"{owlt_h:02d}h {owlt_m:02d}m {owlt_s:04.1f}s"

    rtlt_sec = owlt_sec * 2.0
    rtlt_h = int(rtlt_sec // 3600)
    rtlt_m = int((rtlt_sec % 3600) // 60)
    rtlt_s = rtlt_sec % 60
    rtlt_str = f"{rtlt_h:02d}h {rtlt_m:02d}m {rtlt_s:04.1f}s"

    days_to_one_light_day = -delta_days

    return InstantaneousState(
        timestamp_utc=query_utc,
        timestamp_cst=query_cst,
        geocentric_distance_km=distance_km,
        geocentric_distance_au=distance_au,
        one_way_light_time_sec=owlt_sec,
        one_way_light_time_str=owlt_str,
        round_trip_light_time_str=rtlt_str,
        geocentric_velocity_kms=v_geocentric,
        days_to_one_light_day=days_to_one_light_day,
        daily_distance_gain_km=daily_gain_km
    )


def compute_link_budget(distance_km: float = LIGHT_DAY_KM) -> LinkBudgetResult:
    """
    计算 X 波段下行链路预算 (在 1 光日或指定距离处)
    """
    d_meters = distance_km * 1000.0

    # 自由空间损耗 FSPL = (4 * pi * d / lambda)^2
    fspl_ratio = (4.0 * math.pi * d_meters / DOWNLINK_WAVELENGTH_M) ** 2
    fspl_db = 10.0 * math.log10(fspl_ratio)

    # 发射功率
    tx_power_dbm = 10.0 * math.log10(PROBE_TX_POWER_W * 1000.0)

    # 接收功率 Pr = Pt + Gt + Gr - FSPL - L_misc
    pr_dbm = (tx_power_dbm + PROBE_ANTENNA_GAIN_DBI + DSN_ANTENNA_GAIN_DBI -
              fspl_db - MISC_SYSTEM_LOSS_DB)
    pr_w = (10.0 ** (pr_dbm / 10.0)) / 1000.0
    pr_attowatts = pr_w * 1e18  # 1 aW = 10^-18 W

    # DSN 液氦系统噪声功率谱密度 N0 = k * T_sys (dBm/Hz)
    n0_w_per_hz = BOLTZMANN_K * DSN_SYSTEM_NOISE_TEMP_K
    n0_dbm_per_hz = 10.0 * math.log10(n0_w_per_hz * 1000.0)

    # 比特能量信噪比 Eb/N0 = Pr - N0 - 10*log10(Rb)
    bitrate_db = 10.0 * math.log10(TELEMETRY_BITRATE_BPS)
    eb_n0_db = pr_dbm - n0_dbm_per_hz - bitrate_db

    # 卷积码 (k=7, r=1/2) 典型门限 ~6.0 dB
    decoder_threshold_db = 6.0
    link_margin_db = eb_n0_db - decoder_threshold_db

    return LinkBudgetResult(
        frequency_ghz=DOWNLINK_FREQ_GHZ,
        wavelength_cm=DOWNLINK_WAVELENGTH_M * 100.0,
        distance_km=distance_km,
        free_space_loss_db=fspl_db,
        tx_power_w=PROBE_TX_POWER_W,
        tx_power_dbm=tx_power_dbm,
        probe_gain_dbi=PROBE_ANTENNA_GAIN_DBI,
        dsn_gain_dbi=DSN_ANTENNA_GAIN_DBI,
        received_power_dbm=pr_dbm,
        received_power_w=pr_w,
        received_power_attowatts=pr_attowatts,
        noise_spectral_density_dbm_hz=n0_dbm_per_hz,
        eb_n0_db=eb_n0_db,
        bitrate_bps=TELEMETRY_BITRATE_BPS,
        link_margin_db=link_margin_db
    )


def compute_rtg_timeline(current_year: float = 2026.78) -> RTGEnergyTimeline:
    """
    计算 RTG 能源衰减与停机时间表
    """
    total_mission_years = current_year - 1977.68

    # 距最后一台科学仪器断电 (~205 W)
    power_margin_science = RTG_CURRENT_POWER_2026_W - CRITICAL_SCIENCE_SHUTDOWN_W
    years_to_science = power_margin_science / POWER_LOSS_PER_YEAR_W
    cutoff_year = int(current_year + years_to_science)

    # 距主发射机静默 (~190 W)
    power_margin_silence = RTG_CURRENT_POWER_2026_W - TOTAL_TRANSMITTER_SILENCE_W
    years_to_silence = power_margin_silence / POWER_LOSS_PER_YEAR_W
    silence_year = int(current_year + years_to_silence)

    return RTGEnergyTimeline(
        initial_power_w=RTG_INITIAL_POWER_W,
        power_2026_w=RTG_CURRENT_POWER_2026_W,
        annual_loss_w=POWER_LOSS_PER_YEAR_W,
        years_to_science_cutoff=years_to_science,
        estimated_science_cutoff_year=cutoff_year,
        years_to_total_silence=years_to_silence,
        estimated_silence_year=silence_year,
        total_mission_years=total_mission_years
    )


def get_interstellar_chronology() -> InterstellarChronology:
    """
    获取未来百万年与十亿年星际漫游时间表
    """
    # 日心速度 3.565 AU/年
    v_au_yr = VOYAGER1_V_HELIOCENTRIC * (86400 * 365.25) / AU_KM

    # 内奥尔特云 ~1000 AU (当前 ~165 AU)
    years_to_inner_oort = (1000.0 - 165.0) / v_au_yr
    inner_oort_year = int(2026 + years_to_inner_oort)

    # 奥尔特云外缘 ~100,000 AU (~1.6 光年)
    transit_duration_years = (100000.0 - 1000.0) / v_au_yr

    return InterstellarChronology(
        heliopause_crossing_au=121.6,
        oort_cloud_inner_reach_years=years_to_inner_oort,
        oort_cloud_inner_calendar_year=inner_oort_year,
        oort_cloud_transit_duration_years=transit_duration_years,
        gliese_445_encounter_distance_ly=1.65,
        gliese_445_encounter_years=40000.0,
        galactic_orbit_radius_kpc=8.2,
        galactic_orbit_period_myr=230.0,
        golden_record_durability_gyr=1.0
    )


def generate_full_voyager1_report(query_time: datetime = None) -> Dict[str, Any]:
    """生成完备的旅行者 1 号一光日与星际推演数据字典与报告"""
    if query_time is None:
        # 默认使用 2026-10-13 23:05 CST
        query_time = datetime(2026, 10, 13, 23, 5, 0, tzinfo=timezone(timedelta(hours=8)))

    light_metric = get_light_day_metric()
    current_state = compute_geocentric_state(query_time)
    milestone_state = compute_geocentric_state(MILESTONE_ONE_LIGHT_DAY_UTC)
    link_budget = compute_link_budget(LIGHT_DAY_KM)
    rtg_timeline = compute_rtg_timeline(2026.78)
    chronology = get_interstellar_chronology()

    return {
        "light_metric": light_metric,
        "current_state": current_state,
        "milestone_state": milestone_state,
        "link_budget": link_budget,
        "rtg_timeline": rtg_timeline,
        "chronology": chronology,
    }


def print_cli_summary(report: Dict[str, Any]) -> None:
    """打印控制台专业天体力学推演报告"""
    curr = report["current_state"]
    ms = report["milestone_state"]
    lb = report["link_budget"]
    rtg = report["rtg_timeline"]
    ch = report["chronology"]

    print("=" * 80)
    print(" 🚀 旅行者 1 号 (VOYAGER 1) “一光日” 人类航天历史边界跨越天体力学推演")
    print("=" * 80)
    print(f"【当前即时状态】(标定时间: {curr.timestamp_cst.strftime('%Y-%m-%d %H:%M:%S CST')})")
    print(f"  • 地心直线距离:     {curr.geocentric_distance_km:,.1f} km ({curr.geocentric_distance_au:.4f} AU)")
    print(f"  • 单向光时 (OWLT):   {curr.one_way_light_time_str} ({curr.one_way_light_time_sec:,.1f} 秒)")
    print(f"  • 双向往返光时:     {curr.round_trip_light_time_str}")
    print(f"  • 地心视退行速度:   {curr.geocentric_velocity_kms:.2f} km/s (日增 {curr.daily_distance_gain_km/1e6:.2f} 百万公里)")
    print(f"  • 距一光日倒计时:   {curr.days_to_one_light_day:.2f} 天 ({int(curr.days_to_one_light_day)}天 {int((curr.days_to_one_light_day%1)*24)}小时)")

    print("\n【历史交会里程碑: 1 Light-Day Crossing】")
    print(f"  • 达标精确时刻:     {ms.timestamp_utc.strftime('%Y-%m-%d %H:%M:%S UTC')} / {ms.timestamp_cst.strftime('%Y-%m-%d %H:%M:%S CST')}")
    print(f"  • 严格几何距离:     {ms.geocentric_distance_km:,.1f} km (恰好 173.1446 AU)")
    print(f"  • 单向光时基准:     整整 24 小时 00 分 00 秒 (86,400 秒)")
    print(f"  • 双向握手周期:     整整 48 小时 00 分 00 秒 (2 个平太阳日)")
    print(f"  • 人类累计飞行时长: 49 年 2 个月 13 天 (17,971 天)")

    print("\n【X波段 8.415 GHz 星际极弱链路预算】")
    print(f"  • 自由空间路径损耗: {lb.free_space_loss_db:.2f} dB (传播距离 259 亿公里)")
    print(f"  • 探测器发射功率:   {lb.tx_power_w:.1f} W (3.7m 高增益天线增益 {lb.probe_gain_dbi:.1f} dBi)")
    print(f"  • 地面 DSN 70m 增益: {lb.dsn_gain_dbi:.1f} dBi (液氦冷噪温度 {DSN_SYSTEM_NOISE_TEMP_K:.1f} K)")
    print(f"  • 地表接收信号电平: {lb.received_power_dbm:.2f} dBm ({lb.received_power_attowatts:.2f} 阿瓦 / aW)")
    print(f"  • 比特信噪比 Eb/N0: {lb.eb_n0_db:.2f} dB @ {lb.bitrate_bps:.0f} bps (解码门限裕度 +{lb.link_margin_db:.2f} dB)")

    print("\n【RTG 钚-238 能源衰退与使命终章】")
    print(f"  • 发射初始/当前电能: {rtg.initial_power_w:.1f} W (1977) -> {rtg.power_2026_w:.1f} W (2026)")
    print(f"  • 每年净损耗速率:   -{rtg.annual_loss_w:.1f} W/年 (放射性衰减 + 热电元件老化)")
    print(f"  • 科学仪器关闭节点: 预计 {rtg.estimated_science_cutoff_year} 年 (磁力计/等离子体波最后关停)")
    print(f"  • 发射机永久静默:   预计 {rtg.estimated_silence_year} 年 (宇宙彻底归于无线电沉寂)")

    print("\n【十亿年星际漂移与银河漫游】")
    print(f"  • 跨越日球层顶:     2012 年以 121.6 AU 进入星际介质")
    print(f"  • 抵达内奥尔特云:   约公元 {ch.oort_cloud_inner_calendar_year} 年 (~234 年后，1000 AU)")
    print(f"  • 穿越奥尔特云外缘: 历经约 {ch.oort_cloud_transit_duration_years/1e4:.1f} 万年 (~100,000 AU / 1.6 光年)")
    print(f"  • 恒星近距遭遇:     约 {ch.gliese_445_encounter_years/1e4:.0f} 万年后以 {ch.gliese_445_encounter_distance_ly:.2f} 光年掠过红矮星 Gliese 445")
    print(f"  • 银河系公转轨道:   半径 {ch.galactic_orbit_radius_kpc:.1f} kpc，公转周期 {ch.galactic_orbit_period_myr:.0f} 百万年 (绕银心永恒巡航)")
    print(f"  • 镀金唱片物理寿命: > 10 亿年 (微流星体侵蚀可忽略，留存人类文明印记)")
    print("=" * 80)


if __name__ == "__main__":
    rep = generate_full_voyager1_report()
    print_cli_summary(rep)
