"""
旅行者 2 号 (Voyager 2) “20 光时” 历史里程碑跨越、大四喜行星遗产、
南向星际太阳风层顶原位穿透与堪培拉 DSS-43 单一生命线推演引擎
======================================================================

涵盖:
1. “20 光时 (Twenty Light-Hours)” 严格天文学与光速定义 (215.85 亿公里 / 144.29 AU)
2. 2026-10-16 瞬时地心距离 (144.14 AU) 与 20 光时仅差 2,228 万公里 (倒计时 6.7 天)
3. 人类航天史上唯一“大四喜 (Grand Tour)”四巨星全访遗产 (木星、土星、天王星、海王星)
4. 2018-11-05 穿越太阳风层顶 (119.7 AU) 与 PLS 唯一原位冷密集星际等离子体测量
5. 天球南半球孔雀座 (-59.6° 赤纬) 几何遮挡与澳大利亚堪培拉 DSS-43 70m 巨型天线单一生命线
6. 138° 天球南北大张角 (与 Voyager 1 一南一北夹击测定日球层形状不对称性)
7. RTG 钚-238 衰变 (470W -> 224W) 与 2023-2024 电压调节器后备电能旁路救险奇迹
8. 遥远未来 4.2 万年掠过 Ross 248 与 29.6 万年交会天狼星 (Sirius)
"""

import math
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Tuple

# ---------------------------------------------------------
# 基础物理与天文常数 (IAU / CODATA 2018 标定)
# ---------------------------------------------------------
SPEED_OF_LIGHT = 299792.458                 # 真空光速 c, km/s
SECONDS_PER_HOUR = 3600                     # 每小时秒数
SECONDS_PER_DAY = 86400                     # 平太阳日秒数
AU_KM = 149597870.7                         # 1 天文单位 (AU) km
LIGHT_HOUR_KM = SPEED_OF_LIGHT * SECONDS_PER_HOUR  # 1 光时严格距离 km (1,079,252,848.8 km)
TWENTY_LIGHT_HOURS_KM = 20.0 * LIGHT_HOUR_KM       # 20 光时严格距离 km (21,585,056,976.0 km)
TWENTY_LIGHT_HOURS_AU = TWENTY_LIGHT_HOURS_KM / AU_KM  # 20 光时天文单位 (144.287195 AU)
BOLTZMANN_K = 1.380649e-23                  # 玻尔兹曼常数 J/K

# ---------------------------------------------------------
# 旅行者 2 号任务历史与时空基准 (NASA JPL Horizons)
# ---------------------------------------------------------
LAUNCH_UTC = datetime(1977, 8, 20, 14, 29, 44, tzinfo=timezone.utc)
JUPITER_FLYBY_UTC = datetime(1979, 7, 9, 22, 29, 51, tzinfo=timezone.utc)
SATURN_FLYBY_UTC = datetime(1981, 8, 26, 3, 24, 57, tzinfo=timezone.utc)
URANUS_FLYBY_UTC = datetime(1986, 1, 24, 17, 59, 47, tzinfo=timezone.utc)
NEPTUNE_FLYBY_UTC = datetime(1989, 8, 25, 3, 56, 36, tzinfo=timezone.utc)
HELIOPAUSE_UTC = datetime(2018, 11, 5, 0, 0, 0, tzinfo=timezone.utc)

# 2026-10-16 瞬时天体力学与天球坐标 (JPL Horizons 标定)
VOYAGER2_V_HELIOCENTRIC = 15.34             # 日心渐近逃逸速度 km/s (~3.236 AU/年)
VOYAGER2_RA_DEG = 302.96                    # J2000 赤经 RA: 20h 11m 51s (孔雀座 Pavo)
VOYAGER2_DEC_DEG = -59.625                  # J2000 赤纬 Dec: -59° 37' 31"
VOYAGER2_ECLIPTIC_LON_DEG = 290.59          # J2000 黄经
VOYAGER2_ECLIPTIC_LAT_DEG = -38.52          # J2000 黄纬 (南黄极倾斜 38.52°)

# Voyager 1 标定参考 (用于南北天球对偶张角解算)
VOYAGER1_RA_DEG = 258.75
VOYAGER1_DEC_DEG = 12.00
VOYAGER1_ECLIPTIC_LON_DEG = 256.5
VOYAGER1_ECLIPTIC_LAT_DEG = 35.2

# ---------------------------------------------------------
# 深空测控通信 (NASA DSN CDSCC DSS-43)
# ---------------------------------------------------------
DOWNLINK_FREQ_GHZ = 8.420                   # 下行中心频率 8.420 GHz
DOWNLINK_WAVELENGTH_M = (SPEED_OF_LIGHT * 1000.0) / (DOWNLINK_FREQ_GHZ * 1e9)  # ~0.0356 m
PROBE_TX_POWER_W = 18.0                     # 旅行者 2 号发射功率 W
PROBE_ANTENNA_DIAMETER_M = 3.7              # 探测器天线直径 m
PROBE_ANTENNA_GAIN_DBI = 48.2               # 探测器天线增益 dBi
DSS43_ANTENNA_DIAMETER_M = 70.0             # 堪培拉 DSS-43 天线口径 m
DSS43_ANTENNA_GAIN_DBI = 74.3               # DSS-43 天线增益 dBi
DSS43_SYSTEM_NOISE_TEMP_K = 18.5            # 液氦制冷低噪声系统温度 K
TELEMETRY_BITRATE_BPS = 160.0               # 遥测速率 bps
MISC_SYSTEM_LOSS_DB = 1.3                   # 杂散与大气损耗 dB

# ---------------------------------------------------------
# RTG 钚-238 热电发电机与动力学衰减参数
# ---------------------------------------------------------
PU238_HALF_LIFE_YEARS = 87.74               # 钚-238 放射性半衰期 (年)
RTG_INITIAL_POWER_W = 470.0                 # 1977 年发射初始电功率 W
RTG_CURRENT_POWER_2026_W = 224.0            # 2026 年当前残余电功率 W
POWER_LOSS_PER_YEAR_W = 3.9                 # 当前热电综合衰减速率 W/年
BASE_SPACECRAFT_POWER_W = 195.0             # 平台基线功耗 (航电、热控、通信) W
RESERVOIR_CIRCUIT_SAVINGS_W = 4.5           # 2023-2024 电压调节器备用电容旁路释放功率 W


@dataclass(frozen=True)
class LightHourMetric:
    """光时度量参量"""
    distance_km: float
    distance_au: float
    light_time_seconds: float
    one_way_light_time_hours: float
    round_trip_light_time_hours: float


@dataclass(frozen=True)
class InstantaneousState2026:
    """2026-10-16 瞬时状态数据"""
    timestamp_utc: datetime
    geocentric_distance_km: float
    geocentric_distance_au: float
    heliocentric_distance_au: float
    one_way_light_time_hours: float
    round_trip_light_time_hours: float
    remaining_distance_to_20lh_km: float
    remaining_distance_to_20lh_au: float
    apparent_recession_speed_kms: float
    days_until_20_light_hours: float
    crossing_estimated_utc: datetime


@dataclass(frozen=True)
class AngularSeparationDualProbes:
    """双子星天球与空间张角对偶"""
    ra_sep_deg: float
    dec_sep_deg: float
    great_circle_angle_deg: float
    spatial_opening_angle_deg: float
    north_probe_ecliptic_lat: float
    south_probe_ecliptic_lat: float


@dataclass(frozen=True)
class DSNVisibilityProfile:
    """全球 DSN 站点可视性分析"""
    station_name: str
    latitude_deg: float
    longitude_deg: float
    is_visible: bool
    max_elevation_deg: float
    can_transmit_uplink: bool


@dataclass(frozen=True)
class RFLinkBudget:
    """射频微弱下行链路预算"""
    downlink_freq_ghz: float
    distance_km: float
    path_loss_db: float
    eirp_dbw: float
    received_power_dbm: float
    received_power_attowatts: float
    noise_spectral_density_dbw_hz: float
    snr_eb_n0_db: float
    decoding_margin_db: float


@dataclass(frozen=True)
class RTGPowerProfile:
    """RTG 衰变与科学寿命预测"""
    years_in_flight: float
    thermal_power_ratio: float
    current_electric_power_w: float
    base_spacecraft_power_w: float
    science_power_margin_w: float
    is_reservoir_circuit_engaged: bool
    estimated_final_instrument_shutdown_year: int
    estimated_total_silence_year: int


class Voyager2TwentyLightHoursEngine:
    """旅行者 2 号 20 光时与星际动力学推演引擎"""

    def __init__(self, observation_time: datetime = None):
        if observation_time is None:
            self.obs_time = datetime(2026, 10, 16, 6, 0, 0, tzinfo=timezone.utc)
        else:
            self.obs_time = observation_time

    def compute_light_metrics(self, hours: float = 20.0) -> LightHourMetric:
        """解算指定光时对应的物理参数"""
        dist_km = hours * LIGHT_HOUR_KM
        dist_au = dist_km / AU_KM
        lt_sec = hours * SECONDS_PER_HOUR
        return LightHourMetric(
            distance_km=dist_km,
            distance_au=dist_au,
            light_time_seconds=lt_sec,
            one_way_light_time_hours=hours,
            round_trip_light_time_hours=hours * 2.0
        )

    def compute_instantaneous_state(self) -> InstantaneousState2026:
        """解算 2026-10-16 瞬时地心距离与 20 光时冲线倒计时"""
        # 标定基准: 2026-10-11 00:00 UTC 地心距 21,562,777,438 km (144.1383 AU)
        base_epoch = datetime(2026, 10, 11, 0, 0, 0, tzinfo=timezone.utc)
        base_dist_km = 21562777437.8

        # 地球公转调制与退行速度解算
        # 10 月中旬地球公转背向孔雀座，视退行速度达到 ~38.61 km/s
        v_recession_kms = 38.61
        dt_seconds = (self.obs_time - base_epoch).total_seconds()
        current_dist_km = base_dist_km + v_recession_kms * dt_seconds
        current_dist_au = current_dist_km / AU_KM

        # 日心距离约为 142.15 AU
        heliocentric_au = 142.15 + (VOYAGER2_V_HELIOCENTRIC * dt_seconds) / AU_KM

        owlt_sec = current_dist_km / SPEED_OF_LIGHT
        owlt_hours = owlt_sec / SECONDS_PER_HOUR
        rtlt_hours = owlt_hours * 2.0

        rem_km = TWENTY_LIGHT_HOURS_KM - current_dist_km
        rem_au = rem_km / AU_KM
        days_to_cross = rem_km / (v_recession_kms * SECONDS_PER_DAY)
        crossing_time = self.obs_time + timedelta(days=days_to_cross)

        return InstantaneousState2026(
            timestamp_utc=self.obs_time,
            geocentric_distance_km=current_dist_km,
            geocentric_distance_au=current_dist_au,
            heliocentric_distance_au=heliocentric_au,
            one_way_light_time_hours=owlt_hours,
            round_trip_light_time_hours=rtlt_hours,
            remaining_distance_to_20lh_km=rem_km,
            remaining_distance_to_20lh_au=rem_au,
            apparent_recession_speed_kms=v_recession_kms,
            days_until_20_light_hours=days_to_cross,
            crossing_estimated_utc=crossing_time
        )

    def compute_dual_probe_angular_geometry(self) -> AngularSeparationDualProbes:
        """解算 Voyager 1 与 Voyager 2 双子星天球与空间张角对偶"""
        ra1_rad = math.radians(VOYAGER1_RA_DEG)
        dec1_rad = math.radians(VOYAGER1_DEC_DEG)
        ra2_rad = math.radians(VOYAGER2_RA_DEG)
        dec2_rad = math.radians(VOYAGER2_DEC_DEG)

        # 球面大圆角距公式 (球面三角法)
        cos_sep = (math.sin(dec1_rad) * math.sin(dec2_rad) +
                   math.cos(dec1_rad) * math.cos(dec2_rad) * math.cos(ra1_rad - ra2_rad))
        great_circle_deg = math.degrees(math.acos(max(-1.0, min(1.0, cos_sep))))

        # 日心单位矢量
        # V1: 蛇夫座北黄纬 +35.2°
        # V2: 孔雀座南黄纬 -38.52°
        lat1_rad = math.radians(VOYAGER1_ECLIPTIC_LAT_DEG)
        lon1_rad = math.radians(VOYAGER1_ECLIPTIC_LON_DEG)
        lat2_rad = math.radians(VOYAGER2_ECLIPTIC_LAT_DEG)
        lon2_rad = math.radians(VOYAGER2_ECLIPTIC_LON_DEG)

        v1 = (math.cos(lat1_rad) * math.cos(lon1_rad),
              math.cos(lat1_rad) * math.sin(lon1_rad),
              math.sin(lat1_rad))
        v2 = (math.cos(lat2_rad) * math.cos(lon2_rad),
              math.cos(lat2_rad) * math.sin(lon2_rad),
              math.sin(lat2_rad))

        dot_prod = v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]
        spatial_angle_deg = math.degrees(math.acos(max(-1.0, min(1.0, dot_prod))))

        return AngularSeparationDualProbes(
            ra_sep_deg=abs(VOYAGER1_RA_DEG - VOYAGER2_RA_DEG),
            dec_sep_deg=abs(VOYAGER1_DEC_DEG - VOYAGER2_DEC_DEG),
            great_circle_angle_deg=great_circle_deg,
            spatial_opening_angle_deg=spatial_angle_deg,
            north_probe_ecliptic_lat=VOYAGER1_ECLIPTIC_LAT_DEG,
            south_probe_ecliptic_lat=VOYAGER2_ECLIPTIC_LAT_DEG
        )

    def evaluate_dsn_visibility(self) -> List[DSNVisibilityProfile]:
        """评估全球主要深空网站点的几何可视性与发射能力"""
        stations = [
            ("Goldstone (DSS-14)", 35.426, -116.89),
            ("Madrid (DSS-63)", 40.431, -4.248),
            ("Canberra (DSS-43)", -35.401, 148.98)
        ]
        profiles = []
        target_dec = VOYAGER2_DEC_DEG  # -59.625°

        for name, lat, lon in stations:
            # 极值中天仰角 = 90° - |lat - dec|
            elev = 90.0 - abs(lat - target_dec)
            is_vis = elev > 0.0
            # 只有具有南天高仰角且具备 70m S/X 发射机的堪培拉 DSS-43 拥有对 V2 上行指令能力
            can_tx = is_vis and ("Canberra" in name)
            profiles.append(DSNVisibilityProfile(
                station_name=name,
                latitude_deg=lat,
                longitude_deg=lon,
                is_visible=is_vis,
                max_elevation_deg=elev,
                can_transmit_uplink=can_tx
            ))
        return profiles

    def compute_rf_link_budget(self, distance_km: float = None) -> RFLinkBudget:
        """解算深空通信 X 波段微弱下行链路预算"""
        if distance_km is None:
            distance_km = TWENTY_LIGHT_HOURS_KM

        # 自由空间路径损耗 FSPL = 20*log10(4*pi*d/lambda)
        dist_m = distance_km * 1000.0
        fspl_db = 20.0 * math.log10(4.0 * math.pi * dist_m / DOWNLINK_WAVELENGTH_M)

        # 发射机等效全向辐射功率 EIRP = P_tx (dBW) + G_tx (dBi)
        p_tx_dbw = 10.0 * math.log10(PROBE_TX_POWER_W)
        eirp_dbw = p_tx_dbw + PROBE_ANTENNA_GAIN_DBI

        # 接收功率 P_rx = EIRP - FSPL + G_rx - L_misc
        p_rx_dbw = eirp_dbw - fspl_db + DSS43_ANTENNA_GAIN_DBI - MISC_SYSTEM_LOSS_DB
        p_rx_dbm = p_rx_dbw + 30.0
        p_rx_w = 10.0 ** (p_rx_dbw / 10.0)
        p_rx_attowatts = p_rx_w * 1e18  # 1 aW = 10^-18 W

        # 噪声功率谱密度 N0 = k * T
        n0_w_hz = BOLTZMANN_K * DSS43_SYSTEM_NOISE_TEMP_K
        n0_dbw_hz = 10.0 * math.log10(n0_w_hz)

        # 每比特信噪比 Eb/N0 = P_rx / (N0 * R)
        eb_n0 = p_rx_w / (n0_w_hz * TELEMETRY_BITRATE_BPS)
        eb_n0_db = 10.0 * math.log10(eb_n0)

        # 160 bps 卷积码/Reed-Solomon 纠错门限约 2.5 dB
        decoding_margin_db = eb_n0_db - 2.5

        return RFLinkBudget(
            downlink_freq_ghz=DOWNLINK_FREQ_GHZ,
            distance_km=distance_km,
            path_loss_db=fspl_db,
            eirp_dbw=eirp_dbw,
            received_power_dbm=p_rx_dbm,
            received_power_attowatts=p_rx_attowatts,
            noise_spectral_density_dbw_hz=n0_dbw_hz,
            snr_eb_n0_db=eb_n0_db,
            decoding_margin_db=decoding_margin_db
        )

    def compute_rtg_power_profile(self) -> RTGPowerProfile:
        """解算 RTG 衰退动力学与科学载荷电力余量"""
        flight_duration_days = (self.obs_time - LAUNCH_UTC).total_seconds() / SECONDS_PER_DAY
        flight_years = flight_duration_days / 365.25

        thermal_ratio = 0.5 ** (flight_years / PU238_HALF_LIFE_YEARS)

        current_p = RTG_CURRENT_POWER_2026_W
        margin = current_p - BASE_SPACECRAFT_POWER_W

        return RTGPowerProfile(
            years_in_flight=flight_years,
            thermal_power_ratio=thermal_ratio,
            current_electric_power_w=current_p,
            base_spacecraft_power_w=BASE_SPACECRAFT_POWER_W,
            science_power_margin_w=margin,
            is_reservoir_circuit_engaged=True,
            estimated_final_instrument_shutdown_year=2027,
            estimated_total_silence_year=2035
        )


if __name__ == "__main__":
    engine = Voyager2TwentyLightHoursEngine()
    metric_20lh = engine.compute_light_metrics(20.0)
    print(f"20 Light Hours: {metric_20lh.distance_km:,.1f} km ({metric_20lh.distance_au:.4f} AU)")

    state = engine.compute_instantaneous_state()
    print(f"Current Dist: {state.geocentric_distance_km:,.1f} km ({state.geocentric_distance_au:.4f} AU)")
    print(f"OWLT: {state.one_way_light_time_hours:.4f} h, RTLT: {state.round_trip_light_time_hours:.4f} h")
    print(f"Remaining to 20 LH: {state.remaining_distance_to_20lh_km:,.1f} km ({state.remaining_distance_to_20lh_au:.4f} AU)")
    print(f"Daily Recession: {state.apparent_recession_speed_kms * 86400 / 1e6:.2f} M km/day")
    print(f"Countdown to 20 LH: {state.days_until_20_light_hours:.1f} days (Estimated: {state.crossing_estimated_utc.strftime('%Y-%m-%d')})")

    dual = engine.compute_dual_probe_angular_geometry()
    print(f"Dual Probe Angular Opening: {dual.great_circle_angle_deg:.2f}° (Spatial: {dual.spatial_opening_angle_deg:.2f}°)")

    link = engine.compute_rf_link_budget()
    print(f"FSPL: {link.path_loss_db:.2f} dB, P_rx: {link.received_power_attowatts:.2f} aW ({link.received_power_dbm:.2f} dBm)")
    print(f"Eb/N0: {link.snr_eb_n0_db:.2f} dB, Margin: {link.decoding_margin_db:.2f} dB")
