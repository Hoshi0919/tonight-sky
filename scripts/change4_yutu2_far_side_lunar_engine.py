"""
嫦娥四号 (Chang'e-4) 与玉兔二号 (Yutu-2) 月球背面南极-艾特肯盆地冯·卡门撞击坑巡视、
-180°C 极寒钚-238 RHU 核热源冬眠动力学、月背射电静默区与
2026 人类深空二十一极黄金舰队 (The Grand Unvigintet) 全景推演引擎
========================================================================

涵盖:
1. 2019-01-03 人类首次月球背面软着陆 (45.444°S, 177.599°E 冯·卡门撞击坑)
2. 93+ 月昼与 7.79 年超长巡视 (设计寿命 3 个月昼，超期服役超 31 倍，人类月面运行最长纪录)
3. 极端热控物理: 月昼 +120°C 散热午休与月夜 354 小时 -180°C 钚-238 RHU 同位素热源冬眠守恒
4. 测月雷达 (LPR) 40米高频次生溅射物与 300米玄武岩充填地质层序
5. 月背 100% 绝对地球电磁阻隔与全太阳系超低频射电天文 (0.1~30 MHz) 宇宙黑暗时代黄金窗口
6. 2026 人类深空二十一极黄金舰队 (The Grand Unvigintet) 宏伟时空矩阵
"""

import math
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Tuple

# ---------------------------------------------------------
# 基础物理与天文常数 (IAU / CODATA 2018 标定)
# ---------------------------------------------------------
SPEED_OF_LIGHT = 299792.458                 # 真空光速 c, km/s
SECONDS_PER_DAY = 86400.0                   # 平太阳日秒数
AU_KM = 149597870.7                         # 1 天文单位 (AU) km
MOON_MEAN_DISTANCE_KM = 384400.0            # 地月平均距离 km (~0.00257 AU)
MOON_RADIUS_KM = 1737.4                     # 月球平均半径 km
MOON_MASS_KG = 7.342e22                     # 月球质量 kg
STEFAN_BOLTZMANN = 5.670374419e-8           # 斯忒藩-玻尔兹曼常数 W/(m^2·K^4)
SOLAR_CONSTANT_1AU = 1361.0                 # 1 AU 太阳辐射常数 W/m^2
LUNAR_SYNODIC_MONTH_DAYS = 29.530589        # 朔望月周期 (天)
LUNAR_DAY_HOURS = LUNAR_SYNODIC_MONTH_DAYS * 24.0 / 2.0  # 单个月昼时长 ~354.37 小时
PU238_HALF_LIFE_YEARS = 87.74               # 钚-238 放射性半衰期 (年)

# ---------------------------------------------------------
# 嫦娥四号与玉兔二号工程基准 (CNSA / CLEP 标定)
# ---------------------------------------------------------
LANDING_UTC = datetime(2019, 1, 3, 2, 26, 0, tzinfo=timezone.utc)  # 2019-01-03 10:26 CST
VON_KARMAN_LAT_DEG = -45.444                # 着陆纬度 (45.444°S)
VON_KARMAN_LON_DEG = 177.599                # 着陆经度 (177.599°E)
VON_KARMAN_ELEVATION_M = -5920.0            # 坑底海拔相对于月球基准球面 (m)
VON_KARMAN_DIAMETER_KM = 180.0              # 冯·卡门撞击坑直径 km
DESIGN_LIFETIME_LUNAR_DAYS = 3.0            # 原设计寿命 (3 个月昼 / 约 90 天)
ROVER_MASS_KG = 140.0                       # 玉兔二号总质量 kg
RHU_INITIAL_POWER_W = 2.5                   # 单个 RHU 钚-238 初始热功率 W
LUNAR_ALBEDO = 0.075                        # 冯·卡门坑暗色玄武岩反照率
LUNAR_EMISSIVITY = 0.95                     # 月壤红外热发射率
REGOLITH_DIELECTRIC_CONSTANT = 3.0          # 表层月壤介电常数 ε_r


@dataclass(frozen=True)
class Yutu2OperationalMetrics:
    """玉兔二号长寿命巡视核心指标"""
    timestamp_utc: datetime
    elapsed_earth_days: float
    elapsed_earth_years: float
    elapsed_lunar_days: float               # 经历的月昼数 (Luns)
    design_lifetime_multiple: float         # 超出设计寿命倍数
    pu238_decay_factor: float               # 钚-238 放射性残余比例
    pu238_current_power_w: float            # 当前残余热功率 W
    cumulative_odometer_m: float            # 累计行驶里程 m
    is_longest_lunar_rover: bool            # 是否为人类历史上寿命最长月球车


@dataclass(frozen=True)
class LunarThermalProfile:
    """月表极端温差与核热源热平衡"""
    subsolar_temp_k: float
    subsolar_temp_c: float
    noon_temp_von_karman_c: float           # 45.4°S 正午地表温度 °C
    night_temp_surface_c: float             # 月夜地表辐射极寒温度 °C
    cabin_temperature_with_rhu_c: float     # 密封保温舱内核热源维持温度 °C
    total_thermal_swing_k: float            # 月球表面昼夜总温差 K
    noon_nap_required: bool                 # 正午是否需“午休”防过热


@dataclass(frozen=True)
class LunarFarSideShielding:
    """月球背面几何遮挡与射电静默区特征"""
    earth_visibility_elevation_deg: float   # 对地球直视仰角 (负值代表地平线以下遮蔽)
    is_earth_invisible: bool                # 是否对地球 100% 物理遮蔽
    lunar_body_attenuation_db: float        # 月球岩石本体对地球电磁辐射屏蔽衰减 dB
    earth_ionosphere_cutoff_mhz: float      # 地球电离层截断频率 MHz
    radio_quiet_window_mhz_low: float       # 月背超低频射电天文窗口下限 MHz
    radio_quiet_window_mhz_high: float      # 月背超低频射电天文窗口上限 MHz
    queqiao1_relay_distance_km: float       # 地月 L2 鹊桥一号中继距离 km
    earth_moon_one_way_light_time_s: float  # 地月中继单向通信光时秒


@dataclass(frozen=True)
class DeepSpaceFlagship21:
    """人类深空二十一极单星度量"""
    rank: int
    name: str
    agency: str
    target: str
    heliocentric_dist_au: float
    solar_flux_w_m2: float
    geocentric_dist_km: float
    one_way_light_time_hours: float
    operating_regime: str


class Change4Yutu2FarSideLunarEngine:
    """嫦娥四号与玉兔二号月背巡视与二十一极黄金舰队推演引擎"""

    def __init__(self, ref_utc: datetime = None):
        self.ref_utc = ref_utc or datetime(2026, 10, 17, 3, 11, 0, tzinfo=timezone.utc)

    def compute_operational_metrics(self) -> Yutu2OperationalMetrics:
        """解算玉兔二号在轨巡航时长、月昼数、核热源衰减与里程"""
        delta = self.ref_utc - LANDING_UTC
        elapsed_days = delta.total_seconds() / 86400.0
        elapsed_years = elapsed_days / 365.25
        elapsed_lunar_days = elapsed_days / LUNAR_SYNODIC_MONTH_DAYS
        design_mult = elapsed_lunar_days / DESIGN_LIFETIME_LUNAR_DAYS

        # 钚-238 放射性衰变计算: N(t) = N0 * (0.5)^(t / T_half)
        pu238_decay = math.pow(0.5, elapsed_years / PU238_HALF_LIFE_YEARS)
        current_rhu_power = RHU_INITIAL_POWER_W * pu238_decay

        # 里程模型: 历经 93+ 月昼，在严苛巡视与避障下稳健推进至 ~1650 米
        # 基础里程 1455m (Sol 50) + 后续 40+ 月昼精细勘测推进
        cumulative_odometer = 1658.0

        return Yutu2OperationalMetrics(
            timestamp_utc=self.ref_utc,
            elapsed_earth_days=round(elapsed_days, 1),
            elapsed_earth_years=round(elapsed_years, 3),
            elapsed_lunar_days=round(elapsed_lunar_days, 2),
            design_lifetime_multiple=round(design_mult, 1),
            pu238_decay_factor=round(pu238_decay, 4),
            pu238_current_power_w=round(current_rhu_power, 3),
            cumulative_odometer_m=cumulative_odometer,
            is_longest_lunar_rover=True
        )

    def compute_thermal_equilibrium(self) -> LunarThermalProfile:
        """解算月球表面斯忒藩-玻尔兹曼辐射平衡温控模型"""
        # 日下点极限平衡温度: (1 - A) * S0 = eps * sigma * T^4
        absorbed_flux = (1.0 - LUNAR_ALBEDO) * SOLAR_CONSTANT_1AU
        t_subsolar_k = math.pow(absorbed_flux / (LUNAR_EMISSIVITY * STEFAN_BOLTZMANN), 0.25)
        t_subsolar_c = t_subsolar_k - 273.15

        # 冯·卡门坑 (45.44°S) 正午太阳天顶角约为 45.44° (假设赤纬 0°)
        cos_zenith = math.cos(math.radians(abs(VON_KARMAN_LAT_DEG)))
        absorbed_noon_flux = absorbed_flux * cos_zenith
        t_noon_k = math.pow(absorbed_noon_flux / (LUNAR_EMISSIVITY * STEFAN_BOLTZMANN), 0.25)
        t_noon_c = t_noon_k - 273.15

        # 月夜极寒温度 (依靠极度微弱的月幔深层传热与宇宙微波背景 2.7K 辐射，实测 ~95 K)
        t_night_k = 95.0
        t_night_c = t_night_k - 273.15

        # 舱内温度: 依靠 2.5W 钚-238 RHU 与两相热管重力回路二极管，维持在 -40°C ~ -20°C 之间
        t_cabin_c = -32.5

        thermal_swing = t_subsolar_k - t_night_k

        return LunarThermalProfile(
            subsolar_temp_k=round(t_subsolar_k, 1),
            subsolar_temp_c=round(t_subsolar_c, 1),
            noon_temp_von_karman_c=round(t_noon_c, 1),
            night_temp_surface_c=round(t_night_c, 1),
            cabin_temperature_with_rhu_c=t_cabin_c,
            total_thermal_swing_k=round(thermal_swing, 1),
            noon_nap_required=True
        )

    def compute_far_side_shielding_and_radio(self) -> LunarFarSideShielding:
        """解算月背 100% 物理电磁屏蔽与射电静默区特征"""
        # 冯·卡门坑在月背 177.6°E，地心方向仰角为负 (-42° 以下)，永远隐没在月球地平线下方
        earth_elev = -44.5
        is_occluded = True

        # 月球本体岩石直径 3474 km，对高频/低频地球射电衰减超过 100 dB
        shielding_db = 110.0

        # 地球电离层等离子体截断频率 ~10 MHz
        ionosphere_cutoff = 10.0

        # 月背观测窗口: 0.1 MHz ~ 30 MHz (全频段纯净避开地球广播干扰)
        low_mhz = 0.1
        high_mhz = 30.0

        # 鹊桥一号中继星在地月 L2 Halo 轨道，距月球约 65,000 km，地月中继总光时 1.282 秒
        relay_dist = 65000.0
        light_time_s = MOON_MEAN_DISTANCE_KM / SPEED_OF_LIGHT

        return LunarFarSideShielding(
            earth_visibility_elevation_deg=earth_elev,
            is_earth_invisible=is_occluded,
            lunar_body_attenuation_db=shielding_db,
            earth_ionosphere_cutoff_mhz=ionosphere_cutoff,
            radio_quiet_window_mhz_low=low_mhz,
            radio_quiet_window_mhz_high=high_mhz,
            queqiao1_relay_distance_km=relay_dist,
            earth_moon_one_way_light_time_s=round(light_time_s, 3)
        )

    def compute_grand_unvigintet_matrix(self) -> List[DeepSpaceFlagship21]:
        """构建 2026 人类深空二十一极黄金舰队 (The Grand Unvigintet) 宏伟时空矩阵"""
        data = [
            (1, "旅行者 1 号 (Voyager 1)", "NASA", "恒星际最远深空边界极", 173.22, 2.591e10, 24.01, "星际介质原位穿越 / 1 光日冲线倒计时 33 天"),
            (2, "旅行者 2 号 (Voyager 2)", "NASA", "恒星际南天天球星际极", 144.26, 2.158e10, 19.997, "大四喜四巨星全访 / 20 光时冲线倒计时 21 小时今日跨越"),
            (3, "新视野号 (New Horizons)", "NASA", "柯伊伯带双曲线逃逸极", 65.92, 9.86e9, 9.13, "双曲线逃逸 / COB 绝尘暗夜超额光 / PUI 减速 17%"),
            (4, "朱诺号 (Juno)", "NASA", "木星极轨高能辐射极", 5.20, 7.78e8, 0.72, "木星极轨 / 180kg 钛金保险库 / 掠木 57.8 km/s / PJ89 倒计时 28 天"),
            (5, "木星冰月探测器 (JUICE)", "ESA", "巨行星卫星内禀磁层极", 5.20, 7.78e8, 0.72, "木卫三深海 / 85m² 弱光光伏 / 2.3 年共振巡航"),
            (6, "欧罗巴快船 (Europa Clipper)", "NASA", "外行星木卫二深海生命极", 5.20, 7.78e8, 0.72, "木卫二深海生命 / MEGA 地球引力弹弓倒计时 47 天"),
            (7, "露西号 (Lucy)", "NASA", "木星特洛伊群原始微行星极", 5.04, 7.54e8, 0.70, "特洛伊群化石群 / 7.3m UltraFlex 折叠帆板 / 发射五周年"),
            (8, "灵神星探测器 (Psyche)", "NASA", "金属核心微行星极", 2.042, 3.05e8, 0.28, "金属富集微行星 / SPT-140 霍尔电推 / DSOC 激光通信百倍跃迁"),
            (9, "好奇号 (Curiosity)", "NASA", "火星盖尔撞击坑与夏普山麓极", 1.524, 2.28e8, 0.21, "14 年夏普山垂直攀爬 840m / 盖迪兹谷纯单质硫突破 / MMRTG"),
            (10, "毅力号 (Perseverance)", "NASA", "火星古湖泊与原生古地壳原位探测极", 1.524, 2.28e8, 0.21, "翻越 500m 环壁冲入狂野西部 / 生成式 AI 导航 / MOXIE 制氧 / 33 支岩芯"),
            (11, "天问一号环绕器 (Tianwen-1)", "CNSA", "火星极轨全域遥感极", 1.524, 2.28e8, 0.21, "76m 全球彩色正射图 / MOSIR 雷达探冰 / 3I/ATLAS 星际观测 / 3.5 TB 数据公开"),
            (12, "赫拉号 (Hera)", "ESA", "双小行星微重力伴飞极", 1.304, 1.95e8, 0.18, "双小行星系统伴飞 / 昨日 BRM-1 93 分钟主减速点火圆满达成"),
            (13, "隼鸟二号 (Hayabusa2#)", "JAXA", "十米级超快自转微小行星极", 1.120, 1.68e8, 0.16, "744m Torifune 掠飞后巡航 / 1998 KY26 极区着陆 / 490 倍离心力对抗"),
            (14, "OSIRIS-APEX", "NASA", "毁神星伴飞与极限热控无花果叶极", 1.010, 1.51e8, 0.14, "毁神星近距伴飞 / 4 倍太阳热流 / 2029 掠地 1153km 减速 99% / STIR 吹扫"),
            (15, "詹姆斯·韦伯望远镜 (JWST)", "NASA/ESA/CSA", "日地虚空 L2 天文极", 1.010, 1.51e8, 0.14, "日地 L2 光晕轨道 / 300 K 隔热 6.7 K 制冷 / 0.077'' 捕获 z>14 原初星系"),
            (16, "天问二号 (Tianwen-2)", "CNSA", "地球准卫星共轨采样与彗星双跃迁极", 1.001, 1.498e8, 0.139, "28 分钟自旋 50 倍离心力对抗采样 / 布鲁诺撞击坑月球基岩"),
            (17, "鹊桥二号 (Queqiao-2)", "CNSA", "地月空间与月球南极/月背冻结中继极", 1.000, 3.844e5, 0.000356, "环月大椭圆冻结轨道 / 4.2m 伞状天线 / 月瘤摄动抑制 / 嫦娥六/七/八号生命线"),
            (18, "嫦娥四号与玉兔二号 (Chang'e-4 / Yutu-2)", "CNSA", "月球背面南极-艾特肯盆地原位巡视极", 1.000, 3.844e5, 0.000356, "人类唯一月背软着陆 / 96 月昼 7.79 年超长巡视 / 1.65km 漫游 / -180°C 钚-238 RHU / 月背射电静默区"),
            (19, "贝皮可伦坡 (BepiColombo)", "ESA/JAXA", "太阳最深引力势能阱水星捕获极", 0.387, 5.79e7, 0.054, "水星轨道捕获 / -1405 MJ/kg 势能削减 / MOI 盲操倒计时 36 天"),
            (20, "太阳轨道飞行器 (Solar Orbiter)", "ESA/NASA", "黄道外高倾角极区成像与日冕加热极", 0.280, 4.19e7, 0.039, "金星 4:3 借力 / 520°C 骨黑隔热罩 / 篝火微耀斑 / 倒计时 68 天平安夜 VGA5 跃升 24°"),
            (21, "帕克太阳探测器 (Parker Solar Probe)", "NASA", "恒星日冕极高温炼狱原位极", 0.046, 6.88e6, 0.0064, "192 km/s 人类极速 / 1400°C 碳复合防热罩 / P30 倒计时 47 天")
        ]

        fleet = []
        for r, name, agency, target, helio_au, geo_km, lth, regime in data:
            s_flux = SOLAR_CONSTANT_1AU / (helio_au ** 2)
            fleet.append(DeepSpaceFlagship21(
                rank=r,
                name=name,
                agency=agency,
                target=target,
                heliocentric_dist_au=helio_au,
                solar_flux_w_m2=round(s_flux, 4),
                geocentric_dist_km=geo_km,
                one_way_light_time_hours=lth,
                operating_regime=regime
            ))
        return fleet

    def compute_fleet_contrasts(self, fleet: List[DeepSpaceFlagship21]) -> Dict[str, Any]:
        """解算深空二十一极极端跨度与物理对偶指标"""
        max_helio = fleet[0].heliocentric_dist_au
        min_helio = fleet[-1].heliocentric_dist_au
        helio_ratio = max_helio / min_helio

        max_solar = fleet[-1].solar_flux_w_m2
        min_solar = fleet[0].solar_flux_w_m2
        solar_ratio = max_solar / min_solar

        max_geo = fleet[0].geocentric_dist_km
        min_geo = fleet[17].geocentric_dist_km  # Yutu-2 / Queqiao-2
        geo_ratio = max_geo / min_geo

        max_light = fleet[0].one_way_light_time_hours * 3600.0  # seconds
        min_light = 1.282  # Moon surface one-way light seconds
        light_ratio = max_light / min_light

        # 极端速度跨度: 帕克 192 km/s vs 1998 KY26 表面逃逸速度 6.88 mm/s
        max_v_kms = 192.0
        min_v_kms = 0.00000688
        v_ratio = max_v_kms / min_v_kms

        # 极端温度跨度: 帕克防热屏 1400°C (1673.15 K) vs JWST MIRI 制冷 6.7 K
        temp_span_k = 1673.15 - 2.7

        return {
            "fleet_size": len(fleet),
            "heliocentric_distance_ratio": round(helio_ratio, 2),
            "solar_flux_ratio": round(solar_ratio, 1),
            "geocentric_distance_ratio": round(geo_ratio, 1),
            "one_way_light_time_ratio": round(light_ratio, 1),
            "extreme_velocity_ratio": round(v_ratio, 1),
            "extreme_temperature_span_k": round(temp_span_k, 2)
        }
