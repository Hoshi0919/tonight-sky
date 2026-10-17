"""
火星快车号 (Mars Express, MEX) 23 载在轨传奇、MARSIS 超低频穿地雷达、
火卫一 (Phobos) 轨道相交 45km 超近飞掠与碎石堆内部结构测定、
OMEGA 水成矿物三大地质纪元、HRSC 全球 3D 立体测绘
与 2026 人类深空二十六极黄金舰队 (The Grand Hexavigintet) 推演引擎
======================================================================

涵盖:
1. 23 年在轨服役天文学与轨道动力学 (2003-2026, 8,333 天, 25,600+ 圈)
2. 准极区高偏心椭圆轨道动力学 (近火点 340 km, 远火点 10,100 km, 周期 6.735 小时)
3. 唯一穿透火卫一轨道 (9,376 km) 的现役探测器与 45 km 极近飞掠多普勒引力摄动测地学
4. 火卫一质量 (1.066e16 kg)、体密度 (1,876 kg/m³) 与宏观孔隙度 (~30.5%) 碎石堆确证
5. MARSIS 40m 偶极天线穿透雷达 (1.8~5.0 MHz) 5km 地下剖面动力学与南极冰下反射异常 (>9.5 dB 跃变)
6. 美杜莎槽沟层 (MFF) 3.7km 巨厚冰沉积与全球 2.7m 水当量反演
7. OMEGA 矿物光谱测定火星三大水成演化纪元 (页硅酸盐纪 -> 硫酸盐纪 -> 氧化铁无水纪)
8. HRSC 9 通道推扫立体成像与 98%+ 火星高程 3D 模型
9. 2026 人类深空二十六极黄金舰队 (The Grand Hexavigintet) 宏伟时空矩阵构建
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
SOLAR_CONSTANT_1AU = 1361.0                 # 1 AU 太阳能流 W/m²
GRAVITATIONAL_CONSTANT_G = 6.67430e-11      # 万有引力常数 m³/(kg·s²)

# 火星与火卫一物理天体参数
MARS_MU_KM3_S2 = 42828.37                   # 火星引力常数 GM, km³/s²
MARS_MEAN_RADIUS_KM = 3389.5               # 火星平均半径 km
PHOBOS_SEMI_MAJOR_AXIS_KM = 9376.0         # 火卫一公转半长轴 km
PHOBOS_ORBITAL_PERIOD_H = 7.6538           # 火卫一公转周期 h
PHOBOS_MASS_KG = 1.0659e16                 # 火卫一精确质量 kg
PHOBOS_VOLUME_KM3 = 5689.0                 # 火卫一体积 km³
CARBONACEOUS_GRAIN_DENSITY_KGM3 = 2700.0   # 碳质球粒陨石颗粒母岩密度 kg/m³

# 火星快车发射与在轨历史
MEX_LAUNCH_UTC = datetime(2003, 6, 2, 17, 45, 26, tzinfo=timezone.utc)
MEX_MOI_UTC = datetime(2003, 12, 25, 2, 53, 0, tzinfo=timezone.utc)


@dataclass(frozen=True)
class MEXOrbitState:
    """火星快车在轨动力学状态"""
    semi_major_axis_km: float
    eccentricity: float
    periapsis_alt_km: float
    apoapsis_alt_km: float
    periapsis_radius_km: float
    apoapsis_radius_km: float
    orbital_period_hours: float
    orbits_per_sol: float
    inclination_deg: float
    intersects_phobos_orbit: bool


@dataclass(frozen=True)
class PhobosGeodesyProfile:
    """火卫一近距离飞掠与测地学参量"""
    semi_major_axis_km: float
    phobos_mass_kg: float
    phobos_volume_km3: float
    bulk_density_kgm3: float
    grain_density_kgm3: float
    porosity_percentage: float
    is_rubble_pile: bool
    closest_flyby_distance_km: float
    escape_velocity_ms: float


@dataclass(frozen=True)
class MARSISRadarProfile:
    """MARSIS 穿透雷达与地下介电反射模型"""
    antenna_length_m: float
    freq_min_mhz: float
    freq_max_mhz: float
    max_penetration_depth_km: float
    ice_dielectric_constant: float
    basalt_dielectric_constant: float
    brine_dielectric_constant: float
    ice_radar_velocity_km_s: float
    ice_basalt_reflectivity_db: float
    ice_brine_reflectivity_db: float
    reflectivity_contrast_db: float
    is_liquid_lake_candidate: bool


@dataclass(frozen=True)
class MFFWaterEquivalent:
    """美杜莎槽沟层 (MFF) 水当量估算"""
    max_thickness_km: float
    layer_volume_km3: float
    ice_fraction: float
    water_equivalent_volume_km3: float
    mars_surface_area_km2: float
    equivalent_global_water_layer_m: float


@dataclass(frozen=True)
class DeepSpaceProbePole:
    """深空舰队单极参量"""
    name: str
    agency: str
    target: str
    heliocentric_au: float
    distance_km: float
    solar_flux_w_m2: float
    one_way_light_time_s: float
    key_role: str


class MarsExpressSubsurfacePhobosEngine:
    """火星快车 23 年地下雷达、火卫一穿透与深空二十六极推演引擎"""

    def __init__(self, observation_time: datetime = None):
        if observation_time is None:
            self.obs_time = datetime(2026, 10, 18, 0, 17, 20, tzinfo=timezone.utc)
        else:
            self.obs_time = observation_time

    def compute_mission_longevity(self) -> Dict[str, float]:
        """计算累计在轨与服役天数"""
        flight_sec = (self.obs_time - MEX_LAUNCH_UTC).total_seconds()
        orbit_sec = (self.obs_time - MEX_MOI_UTC).total_seconds()
        return {
            "flight_days": flight_sec / SECONDS_PER_DAY,
            "orbit_days": orbit_sec / SECONDS_PER_DAY,
            "flight_years": flight_sec / (SECONDS_PER_DAY * 365.25),
            "orbit_years": orbit_sec / (SECONDS_PER_DAY * 365.25)
        }

    def compute_orbit_state(self, peri_alt_km: float = 340.0, apo_alt_km: float = 10100.0) -> MEXOrbitState:
        """解算高偏心椭圆极轨动力学"""
        rp = MARS_MEAN_RADIUS_KM + peri_alt_km
        ra = MARS_MEAN_RADIUS_KM + apo_alt_km
        a = (rp + ra) / 2.0
        ecc = (ra - rp) / (ra + rp)

        # 开普勒周期 T = 2 * pi * sqrt(a^3 / mu)
        period_sec = 2.0 * math.pi * math.sqrt((a ** 3) / MARS_MU_KM3_S2)
        period_hours = period_sec / SECONDS_PER_HOUR
        mars_sol_hours = 24.6597
        orbits_per_sol = mars_sol_hours / period_hours

        # 判断是否穿越火卫一轨道
        intersects_phobos = (rp <= PHOBOS_SEMI_MAJOR_AXIS_KM <= ra)

        return MEXOrbitState(
            semi_major_axis_km=a,
            eccentricity=ecc,
            periapsis_alt_km=peri_alt_km,
            apoapsis_alt_km=apo_alt_km,
            periapsis_radius_km=rp,
            apoapsis_radius_km=ra,
            orbital_period_hours=period_hours,
            orbits_per_sol=orbits_per_sol,
            inclination_deg=86.5,
            intersects_phobos_orbit=intersects_phobos
        )

    def compute_phobos_geodesy(self, closest_flyby_km: float = 45.0) -> PhobosGeodesyProfile:
        """解算火卫一内部结构与空隙率"""
        bulk_density = (PHOBOS_MASS_KG / (PHOBOS_VOLUME_KM3 * 1e9))  # kg/m³
        porosity = (1.0 - (bulk_density / CARBONACEOUS_GRAIN_DENSITY_KGM3)) * 100.0
        is_rubble = porosity > 25.0

        # 火卫一表面逃逸速度 v_esc = sqrt(2 * G * M / R)
        r_phobos_m = ((3.0 * PHOBOS_VOLUME_KM3 * 1e9) / (4.0 * math.pi)) ** (1.0 / 3.0)
        v_esc_ms = math.sqrt((2.0 * GRAVITATIONAL_CONSTANT_G * PHOBOS_MASS_KG) / r_phobos_m)

        return PhobosGeodesyProfile(
            semi_major_axis_km=PHOBOS_SEMI_MAJOR_AXIS_KM,
            phobos_mass_kg=PHOBOS_MASS_KG,
            phobos_volume_km3=PHOBOS_VOLUME_KM3,
            bulk_density_kgm3=bulk_density,
            grain_density_kgm3=CARBONACEOUS_GRAIN_DENSITY_KGM3,
            porosity_percentage=porosity,
            is_rubble_pile=is_rubble,
            closest_flyby_distance_km=closest_flyby_km,
            escape_velocity_ms=v_esc_ms
        )

    def compute_marsis_radar(self) -> MARSISRadarProfile:
        """解算 MARSIS 穿透雷达与介质反射对比度"""
        eps_ice = 3.15
        eps_basalt = 7.0
        eps_brine = 70.0

        v_ice = SPEED_OF_LIGHT / math.sqrt(eps_ice)  # 纯冰光速 ~168,913 km/s

        # 菲涅尔正入射功率反射率 R = |(sqrt(e1) - sqrt(e2)) / (sqrt(e1) + sqrt(e2))|^2
        r_ice_basalt = ((math.sqrt(eps_ice) - math.sqrt(eps_basalt)) /
                        (math.sqrt(eps_ice) + math.sqrt(eps_basalt))) ** 2
        r_ice_basalt_db = 10.0 * math.log10(r_ice_basalt)

        r_ice_brine = ((math.sqrt(eps_ice) - math.sqrt(eps_brine)) /
                       (math.sqrt(eps_ice) + math.sqrt(eps_brine))) ** 2
        r_ice_brine_db = 10.0 * math.log10(r_ice_brine)

        contrast_db = r_ice_brine_db - r_ice_basalt_db

        return MARSISRadarProfile(
            antenna_length_m=40.0,
            freq_min_mhz=1.8,
            freq_max_mhz=5.0,
            max_penetration_depth_km=5.0,
            ice_dielectric_constant=eps_ice,
            basalt_dielectric_constant=eps_basalt,
            brine_dielectric_constant=eps_brine,
            ice_radar_velocity_km_s=v_ice,
            ice_basalt_reflectivity_db=r_ice_basalt_db,
            ice_brine_reflectivity_db=r_ice_brine_db,
            reflectivity_contrast_db=contrast_db,
            is_liquid_lake_candidate=(contrast_db > 8.0)
        )

    def compute_mff_water_reservoir(self) -> MFFWaterEquivalent:
        """解算美杜莎槽沟层 (MFF) 全球水层厚度"""
        thick_km = 3.7
        total_vol_km3 = 2.0e6
        ice_ratio = 0.85
        water_vol_km3 = total_vol_km3 * ice_ratio

        area_km2 = 4.0 * math.pi * (MARS_MEAN_RADIUS_KM ** 2)
        # 1 km³ = 1e9 m³, 1 km² = 1e6 m² => 1 km³ / 1 km² = 1000 m
        water_layer_m = (water_vol_km3 / area_km2) * 1000.0

        return MFFWaterEquivalent(
            max_thickness_km=thick_km,
            layer_volume_km3=total_vol_km3,
            ice_fraction=ice_ratio,
            water_equivalent_volume_km3=water_vol_km3,
            mars_surface_area_km2=area_km2,
            equivalent_global_water_layer_m=water_layer_m
        )

    def build_grand_hexavigintet_fleet(self) -> List[DeepSpaceProbePole]:
        """构筑 2026 人类深空二十六极黄金舰队 (The Grand Hexavigintet)"""
        # 26 大深空支柱
        fleet_data = [
            ("旅行者 1 号 (Voyager 1)", "NASA", "恒星际北黄极空间 (173.22 AU)", 173.22,
             "恒星际最远深空边界极，1光日冲线倒计时32天，2.7 K宇宙背景"),
            ("旅行者 2 号 (Voyager 2)", "NASA", "恒星际南天孔雀座 (144.29 AU)", 144.29,
             "恒星际南天天球星际极，今日凌晨正式跨越20光时大关！"),
            ("新视野号 (New Horizons)", "NASA", "柯伊伯带双曲线逃逸 (65.92 AU)", 65.92,
             "柯伊伯带双曲线逃逸极，COB绝尘暗夜超额光，PUI等离子体减速"),
            ("朱诺号 (Juno)", "NASA", "木星极轨高能辐射 (5.20 AU)", 5.20,
             "木星极轨高能辐射极，180kg钛金保险库，掠木57.8 km/s，PJ89倒计时27天"),
            ("木星冰月探测器 (JUICE)", "ESA", "木星卫星深海巡航 (5.20 AU)", 5.20,
             "巨行星卫星内禀磁层极，探秘木卫三深海，85m²弱光光伏，2.3年共振巡航"),
            ("欧罗巴快船 (Europa Clipper)", "NASA", "木卫二深海生命 (5.20 AU)", 5.20,
             "外行星木卫二深海生命极，MEGA地球引力弹弓倒计时47天"),
            ("露西号 (Lucy)", "NASA", "木星特洛伊群原始微行星 (5.04 AU)", 5.04,
             "木星特洛伊群原始微行星极，7.3m UltraFlex折叠帆板，发射五周年"),
            ("灵神星探测器 (Psyche)", "NASA", "主带金属核心小行星 (2.042 AU)", 2.042,
             "金属核心微行星极，SPT-140霍尔电推，DSOC激光光子链路百倍跃迁"),
            ("火星快车号 (Mars Express)", "ESA", "火星极轨地下雷达与火卫一 (1.579 AU)", 1.579,
             "火星23年在轨地下雷达与火卫一穿越极，MARSIS 5km探地、火卫一45km飞掠测地、OMEGA水成纪元、HRSC 3D全图"),
            ("好奇号 (Curiosity)", "NASA", "火星盖尔撞击坑夏普山 (1.524 AU)", 1.524,
             "火星盖尔撞击坑与夏普山麓极，14年漫游33.6km，盖迪兹谷纯单质硫突破，MMRTG"),
            ("毅力号 (Perseverance)", "NASA", "火星耶泽罗陨坑古三角洲 (1.524 AU)", 1.524,
             "火星古湖泊与原生古地壳原位探测极，翻越500m环壁冲入狂野西部、生成式AI导航与33支岩芯密封"),
            ("天问一号环绕器 (Tianwen-1)", "CNSA", "火星极轨全域遥感 (1.524 AU)", 1.524,
             "火星极轨全域遥感极，76m全球彩色正射图，MOSIR雷达探冰，3I/ATLAS星际观测，3.5 TB数据公开"),
            ("火星勘测轨道器 (MRO)", "NASA", "火星在轨超高分辨率对焦 (1.524 AU)", 1.524,
             "火星20年在轨超高分辨率对焦与深空信息中枢极，HiRISE 30cm光学微观极限、SHARAD 1km探冰、Electra 80%中继"),
            ("赫拉号 (Hera)", "ESA", "双小行星微重力伴飞 (1.304 AU)", 1.304,
             "双小行星微重力伴飞极，BRM-1 93分钟主减速点火圆满达成"),
            ("隼鸟二号 (Hayabusa2#)", "JAXA", "十米级超快自转微小行星 (1.120 AU)", 1.120,
             "十米级超快自转微小行星极，744m Torifune掠飞后巡航，1998 KY26极区着陆，490倍离心力对抗，μ10离子电推"),
            ("OSIRIS-APEX", "NASA", "毁神星伴飞与极限热控 (1.010 AU)", 1.010,
             "毁神星伴飞与极限热控无花果叶极，4倍太阳热流，2029掠地1153km减速99%，STIR羽流吹扫"),
            ("詹姆斯·韦伯望远镜 (JWST)", "NASA/ESA/CSA", "日地 L2 红外深空 (1.010 AU)", 1.010,
             "日地虚空L2天文极，6.5m铍金镜，300 K隔热6.7 K制冷，0.077''捕获z>14原初星系"),
            ("欧几里得空间望远镜 (Euclid)", "ESA", "日地 L2 暗宇宙与大尺度网 (1.010 AU)", 1.010,
             "日地L2暗宇宙与大尺度三维宇宙网宏观极，1.2m SiC TMA，0.53 deg²巨视场，6.09亿像素VIS+6500万像素NISP"),
            ("天问二号 (Tianwen-2)", "CNSA", "地球准卫星共轨采样 (1.001 AU)", 1.001,
             "地球准卫星共轨采样与彗星双跃迁极，28分钟自旋50倍离心力对抗采样，布鲁诺撞击坑月球基岩"),
            ("鹊桥二号 (Queqiao-2)", "CNSA", "地月空间与月球极区中继 (1.000 AU)", 1.000,
             "地月空间与月球南极/月背冻结中继极，4.2米伞状天线、月瘤摄动抑制、嫦娥六/七/八号生命线"),
            ("嫦娥四号与玉兔二号", "CNSA", "月球背面南极-艾特肯盆地 (1.000 AU)", 1.000,
             "月球背面南极-艾特肯盆地原位巡视极，人类唯一月背软着陆、96月昼7.79年超长巡视、-180°C钚-238 RHU核热源冬眠"),
            ("太阳和日球层天文台 (SOHO)", "ESA/NASA", "日地 L1 向日日冕哨兵 (0.990 AU)", 0.990,
             "日地L1向日日冕哨兵极，30年守望三轮太阳活动周，LASCO 4450万km视场与CME预警、5200颗彗星世界纪录"),
            ("日地关系天文台 (STEREO-A)", "NASA", "日心超前漂移轨道 (0.962 AU)", 0.962,
             "日心超前漂移轨道3D CME立体极，20周年前夕，21+圈公转，68°超前角侧翼透视消除2D投影简并，太阳远背面5.2天超前预警"),
            ("贝皮可伦坡 (BepiColombo)", "ESA/JAXA", "水星引力势能阱捕获 (0.387 AU)", 0.387,
             "太阳最深引力势能阱水星捕获极，-1405 MJ/kg MOI盲操倒计时35天"),
            ("太阳轨道飞行器 (Solar Orbiter)", "ESA/NASA", "黄道外高倾角极区成像 (0.280 AU)", 0.280,
             "黄道外高倾角极区成像与日冕加热极，金星4:3借力24°，520°C骨黑隔热罩，微耀斑篝火，倒计时68天平安夜VGA5"),
            ("帕克太阳探测器 (Parker Solar Probe)", "NASA", "恒星日冕极高温炼狱原位 (0.046 AU)", 0.046,
             "恒星日冕极高温炼狱原位极，192 km/s人类极速，1400°C防热罩，P30倒计时46天")
        ]

        fleet = []
        for name, agency, target, r_au, role in fleet_data:
            dist_km = r_au * AU_KM
            flux = SOLAR_CONSTANT_1AU / (r_au ** 2)
            lt_s = dist_km / SPEED_OF_LIGHT
            fleet.append(DeepSpaceProbePole(
                name=name,
                agency=agency,
                target=target,
                heliocentric_au=r_au,
                distance_km=dist_km,
                solar_flux_w_m2=flux,
                one_way_light_time_s=lt_s,
                key_role=role
            ))

        # 严格按日心极距降序排列
        fleet.sort(key=lambda p: p.heliocentric_au, reverse=True)
        return fleet

    def compute_fleet_extremes(self) -> Dict[str, float]:
        """解算深空舰队极端动态跨度"""
        fleet = self.build_grand_hexavigintet_fleet()
        max_pole = fleet[0]    # Voyager 1
        min_pole = fleet[-1]   # Parker Solar Probe

        ratio_r = max_pole.heliocentric_au / min_pole.heliocentric_au
        ratio_flux = min_pole.solar_flux_w_m2 / max_pole.solar_flux_w_m2
        ratio_owlt = max_pole.one_way_light_time_s / min_pole.one_way_light_time_s

        return {
            "probe_count": len(fleet),
            "max_heliocentric_au": max_pole.heliocentric_au,
            "min_heliocentric_au": min_pole.heliocentric_au,
            "heliocentric_distance_ratio": ratio_r,
            "solar_flux_ratio": ratio_flux,
            "one_way_light_time_ratio": ratio_owlt
        }


if __name__ == "__main__":
    engine = MarsExpressSubsurfacePhobosEngine()
    longevity = engine.compute_mission_longevity()
    orbit = engine.compute_orbit_state()
    phobos = engine.compute_phobos_geodesy()
    marsis = engine.compute_marsis_radar()
    mff = engine.compute_mff_water_reservoir()
    extremes = engine.compute_fleet_extremes()

    print("=== 火星快车与深空二十六极黄金舰队推演 ===")
    print(f"在轨服役: {longevity['orbit_days']:.1f} 天 ({longevity['orbit_years']:.2f} 年)")
    print(f"椭圆极轨: 半长轴 {orbit.semi_major_axis_km:.1f} km, 偏心率 {orbit.eccentricity:.4f}, 周期 {orbit.orbital_period_hours:.2f} h")
    print(f"火卫一穿透: {orbit.intersects_phobos_orbit}, 体密度 {phobos.bulk_density_kgm3:.1f} kg/m³, 孔隙度 {phobos.porosity_percentage:.1f}% (碎石堆确证)")
    print(f"MARSIS 雷达: 穿透深度 {marsis.max_penetration_depth_km} km, 冰-卤水/冰-玄武岩 反射对比度 {marsis.reflectivity_contrast_db:.1f} dB")
    print(f"MFF 水当量: 全球水层厚度 {mff.equivalent_global_water_layer_m:.1f} 米")
    print(f"深空二十六极: 覆盖 {extremes['probe_count']} 艘深空航天器, 日心极距落差 {extremes['heliocentric_distance_ratio']:.1f} 倍, 能流落差 {extremes['solar_flux_ratio']/1e6:.2f} 百万倍")
