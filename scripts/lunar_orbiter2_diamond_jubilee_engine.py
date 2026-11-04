import math

class LunarOrbiter2DiamondJubileeEngine:
    """
    Lunar Orbiter 2 (LO-2 / Spacecraft 5) 60 周年甲子钻禧纪念 (1966-11-06 至 2026-11-06)
    天体动力学、柯达 Bimat 干式显影、飞点扫描 (Flying Spot Scanner)、
    图像运动补偿 (IMC)、哥白尼环形山“世纪之照”与月球质量瘤 (Mascon) 重力摄动解算引擎
    """
    # 基础物理常数
    G = 6.67430e-11              # m^3 / (kg * s^2)
    C = 299792458.0              # m / s
    MU_MOON = 4.9028e12          # m^3 / s^2 (4902.8 km^3/s^2)
    R_MOON = 1737400.0           # m (月球平均赤道半径 1737.4 km)
    AU_METERS = 1.495978707e11   # m

    def __init__(self):
        pass

    def compute_orbital_dynamics(self):
        """
        解算 Lunar Orbiter 2 初始捕获椭圆轨与 Orbit 33 摄影工作轨动力学
        """
        # 1. 初始椭圆捕获轨道 (Initial Capture Orbit, 1966-11-10 LOI)
        hp_init = 196.3e3
        ha_init = 1850.0e3
        rp_init = self.R_MOON + hp_init
        ra_init = self.R_MOON + ha_init
        a_init = (rp_init + ra_init) / 2.0
        e_init = (ra_init - rp_init) / (ra_init + rp_init)
        T_init_s = 2.0 * math.pi * math.sqrt(a_init**3 / self.MU_MOON)
        T_init_min = T_init_s / 60.0
        vp_init = math.sqrt(self.MU_MOON * (2.0 / rp_init - 1.0 / a_init))
        va_init = math.sqrt(self.MU_MOON * (2.0 / ra_init - 1.0 / a_init))

        # 2. 摄影工作轨道 (Photo Reconnaissance Orbit, Orbit 33 变轨, 1966-11-15)
        hp_photo = 45.1e3
        ha_photo = 1843.0e3
        rp_photo = self.R_MOON + hp_photo
        ra_photo = self.R_MOON + ha_photo
        a_photo = (rp_photo + ra_photo) / 2.0
        e_photo = (ra_photo - rp_photo) / (ra_photo + rp_photo)
        T_photo_s = 2.0 * math.pi * math.sqrt(a_photo**3 / self.MU_MOON)
        T_photo_min = T_photo_s / 60.0
        vp_photo = math.sqrt(self.MU_MOON * (2.0 / rp_photo - 1.0 / a_photo))
        va_photo = math.sqrt(self.MU_MOON * (2.0 / ra_photo - 1.0 / a_photo))

        # 3. 变轨制动速度增量 (Orbit Transfer Burn Delta-v at Apolune)
        # 在初始轨远月点减速降低近月点至 45.1 km:
        # v_a_transfer = sqrt(MU * (2/ra_init - 1/a_photo))
        va_transfer = math.sqrt(self.MU_MOON * (2.0 / ra_init - 1.0 / a_photo))
        delta_v_transfer = abs(va_transfer - va_init)

        # 4. 近月捕获制动 (LOI Delta-v)
        # 双曲线进场剩余速度 v_inf ~ 820 m/s
        v_inf = 820.0
        v_hyp_arrival = math.sqrt(v_inf**2 + 2.0 * self.MU_MOON / rp_init)
        loi_theoretical_delta_v = v_hyp_arrival - vp_init

        return {
            "mission": "Lunar Orbiter 2 (LO-B / Spacecraft 5)",
            "launch_utc": "1966-11-06 23:21:00.195",
            "anniversary_years": 60,
            "jubilee_name": "Diamond Jubilee (六十甲子钻禧)",
            "launch_vehicle": "Atlas SLV-3 (5802) + Agena D (6631)",
            "launch_site": "Cape Canaveral LC-13",
            "dry_mass_kg": 385.6,
            "initial_capture_orbit": {
                "perilune_alt_km": round(hp_init / 1e3, 1),
                "apolune_alt_km": round(ha_init / 1e3, 1),
                "semi_major_axis_km": round(a_init / 1e3, 1),
                "eccentricity": round(e_init, 4),
                "period_min": round(T_init_min, 2),
                "perilune_velocity_m_s": round(vp_init, 1),
                "apolune_velocity_m_s": round(va_init, 1),
                "inclination_deg": 11.97
            },
            "photo_orbit": {
                "perilune_alt_km": round(hp_photo / 1e3, 1),
                "apolune_alt_km": round(ha_photo / 1e3, 1),
                "semi_major_axis_km": round(a_photo / 1e3, 1),
                "eccentricity": round(e_photo, 4),
                "period_min": round(T_photo_min, 2),
                "perilune_velocity_m_s": round(vp_photo, 1),
                "apolune_velocity_m_s": round(va_photo, 1),
                "inclination_deg": 11.98
            },
            "transfer_maneuver": {
                "orbit_number": 33,
                "burn_date_utc": "1966-11-15 22:58",
                "engine_burn_duration_s": 17.4,
                "theoretical_delta_v_m_s": round(delta_v_transfer, 1),
                "actual_delta_v_m_s": 28.1
            },
            "loi_maneuver": {
                "arrival_utc": "1966-11-10 20:26:37",
                "hyperbolic_arrival_v_inf_m_s": v_inf,
                "hyperbolic_perilune_speed_m_s": round(v_hyp_arrival, 1),
                "theoretical_delta_v_m_s": round(loi_theoretical_delta_v, 1),
                "actual_marquardt_burn_duration_s": 611.6,
                "actual_marquardt_delta_v_m_s": 829.7,
                "engine_thrust_n": 445.0  # 100 lbf Marquardt hypergolic engine
            }
        }

    def compute_photographic_and_imc_physics(self):
        """
        解算双镜头光学系统、图像运动补偿 (IMC) 机械平移与地物空间分辨率
        """
        hp = 45.1e3  # 45.1 km 近月点高度
        vp = 1916.4  # 近月点轨道线速度 m/s
        exposure_time_s = 0.04  # 1/25 秒快门

        # 1. 高分辨率 Paxar 远摄镜头 (High Resolution)
        f_hr = 0.610        # 610 mm 焦距 (24 inch)
        f_number_hr = 5.6
        d_aperture_hr = f_hr / f_number_hr  # 108.9 mm 口径
        lambda_light = 5.5e-7               # 550 nm 绿光波长

        # 瑞利判据角分辨率 (Rayleigh Diffraction Limit)
        theta_diff_hr_rad = 1.22 * lambda_light / d_aperture_hr
        theta_diff_hr_arcsec = theta_diff_hr_rad * (180.0 / math.pi) * 3600.0
        ground_diff_res_hr_m = hp * theta_diff_hr_rad

        # 柯达 SO-243 胶片感光乳剂分辨率 (4 微米极细晶粒，250 线对/mm)
        grain_size_m = 4.0e-6
        ground_film_res_hr_m = (hp / f_hr) * grain_size_m

        # 2. 中分辨率 Xenotar 广角镜头 (Medium Resolution)
        f_mr = 0.080        # 80 mm 焦距
        f_number_mr = 2.8
        d_aperture_mr = f_mr / f_number_mr  # 28.57 mm 口径
        theta_diff_mr_rad = 1.22 * lambda_light / d_aperture_mr
        theta_diff_mr_arcsec = theta_diff_mr_rad * (180.0 / math.pi) * 3600.0
        ground_diff_res_mr_m = hp * theta_diff_mr_rad
        ground_film_res_mr_m = (hp / f_mr) * 15.0e-6

        # 3. 图像运动补偿 (IMC, Image Motion Compensation)
        # 地表角速率 omega = v_p / H (rad/s)
        omega_ground = vp / hp
        omega_deg_s = omega_ground * (180.0 / math.pi)

        # 焦平面胶片台平移线速度 v_film = f * omega
        v_platen_hr_mm_s = (f_hr * omega_ground) * 1e3
        v_platen_mr_mm_s = (f_mr * omega_ground) * 1e3

        # 无补偿时的像移破坏
        ground_smear_uncompensated_m = vp * exposure_time_s
        film_smear_hr_uncompensated_mm = v_platen_hr_mm_s * exposure_time_s
        smear_to_grain_ratio = (film_smear_hr_uncompensated_mm * 1e-3) / grain_size_m

        # V/H 光学伺服补偿后的残余像移 (< 3 微米)
        residual_film_smear_um = 2.5
        residual_ground_smear_m = (hp / f_hr) * (residual_film_smear_um * 1e-6)

        # 视场角 (FOV, 55 mm 曝光幅宽)
        film_width_m = 0.055
        fov_hr_deg = 2.0 * math.atan((film_width_m / 2.0) / f_hr) * (180.0 / math.pi)
        fov_mr_deg = 2.0 * math.atan((film_width_m / 2.0) / f_mr) * (180.0 / math.pi)

        return {
            "perilune_altitude_km": hp / 1e3,
            "orbital_speed_m_s": vp,
            "exposure_time_s": exposure_time_s,
            "high_resolution_paxar": {
                "focal_length_mm": f_hr * 1e3,
                "aperture_f_stop": f_number_hr,
                "clear_aperture_mm": round(d_aperture_hr * 1e3, 1),
                "diffraction_limit_arcsec": round(theta_diff_hr_arcsec, 2),
                "diffraction_ground_resolution_m": round(ground_diff_res_hr_m, 3),
                "film_emulsion_ground_resolution_m": round(ground_film_res_hr_m, 3),
                "practical_readout_resolution_m": 1.0,
                "field_of_view_deg": round(fov_hr_deg, 2)
            },
            "medium_resolution_xenotar": {
                "focal_length_mm": f_mr * 1e3,
                "aperture_f_stop": f_number_mr,
                "clear_aperture_mm": round(d_aperture_mr * 1e3, 1),
                "diffraction_limit_arcsec": round(theta_diff_mr_arcsec, 2),
                "ground_resolution_m": round(ground_film_res_mr_m, 2),
                "field_of_view_deg": round(fov_mr_deg, 2)
            },
            "image_motion_compensation_imc": {
                "ground_angular_rate_deg_s": round(omega_deg_s, 3),
                "platen_speed_hr_mm_s": round(v_platen_hr_mm_s, 2),
                "platen_speed_mr_mm_s": round(v_platen_mr_mm_s, 2),
                "uncompensated_ground_smear_m": round(ground_smear_uncompensated_m, 2),
                "uncompensated_film_smear_mm": round(film_smear_hr_uncompensated_mm, 3),
                "smear_to_grain_blur_factor": round(smear_to_grain_ratio, 1),
                "residual_film_smear_microns": residual_film_smear_um,
                "residual_ground_smear_m": round(residual_ground_smear_m, 3)
            }
        }

    def compute_copernicus_picture_of_century_geometry(self):
        """
        解算 1966-11-23 哥白尼环形山“世纪之照” (Picture of the Century) 斜向三维透视投影几何
        """
        # 探测器位置 (Orbit 52, 1966-11-23 00:05:42 UT)
        probe_lat_deg = -4.5       # 4.5°S
        probe_lon_deg = -20.1      # 20.1°W
        probe_alt_km = 45.7        # 28.4 miles

        # 哥白尼环形山中心与南缘 (Copernicus Crater, 9.62°N, 20.08°W)
        copernicus_lat_deg = 9.62
        copernicus_lon_deg = -20.08
        copernicus_diameter_km = 93.0
        rim_height_km = 3.8        # 坑壁较坑底落差 3.8 km
        central_peak_height_km = 1.2  # 中央峰群高达 1.2 km

        # 经纬度大圆球面角距 (Great circle angular distance along meridian)
        d_lat_deg = copernicus_lat_deg - probe_lat_deg
        d_lat_rad = d_lat_deg * (math.pi / 180.0)
        arc_dist_center_km = (self.R_MOON / 1e3) * d_lat_rad
        arc_dist_south_rim_km = arc_dist_center_km - (copernicus_diameter_km / 2.0)

        # 视线斜距 (Slant range to crater rim)
        slant_range_km = math.sqrt(arc_dist_south_rim_km**2 + probe_alt_km**2)

        # 视线仰俯角 (Grazing elevation angle looking down into the crater)
        grazing_angle_deg = math.atan2(probe_alt_km, arc_dist_south_rim_km) * (180.0 / math.pi)

        # 姿态机动滚转角 (Off-nadir spacecraft roll)
        spacecraft_roll_deg = 17.0

        # 中央峰视张角 (Angular size of central peak 1.2 km from 250~380 km)
        central_peak_angular_size_arcmin = (central_peak_height_km / slant_range_km) * (180.0 / math.pi) * 60.0

        return {
            "photo_title": "Copernicus - Picture of the Century (世纪之照)",
            "capture_utc": "1966-11-23 00:05:42",
            "orbit_number": 52,
            "probe_coordinates": {
                "latitude_deg": probe_lat_deg,
                "longitude_deg": probe_lon_deg,
                "altitude_km": probe_alt_km
            },
            "copernicus_crater": {
                "latitude_deg": copernicus_lat_deg,
                "longitude_deg": copernicus_lon_deg,
                "diameter_km": copernicus_diameter_km,
                "rim_wall_depth_km": rim_height_km,
                "central_peaks_height_km": central_peak_height_km,
                "northern_feature": "Gay-Lussac crater on rim"
            },
            "viewing_geometry": {
                "meridian_arc_distance_center_km": round(arc_dist_center_km, 1),
                "meridian_arc_distance_south_rim_km": round(arc_dist_south_rim_km, 1),
                "slant_range_to_rim_km": round(slant_range_km, 1),
                "grazing_perspective_angle_deg": round(grazing_angle_deg, 2),
                "spacecraft_roll_angle_deg": spacecraft_roll_deg,
                "central_peak_angular_height_arcmin": round(central_peak_angular_size_arcmin, 2)
            },
            "historical_significance": "人类首次在斜向透视中看到月球山脉与环形山的真实三维立体地貌，打破了千百年来将月球地表视为平坦浅盘的传统认知。"
        }

    def compute_bimat_and_telemetry(self):
        """
        解算柯达 Bimat 干式扩散转移显影与飞点阴极射线管 (CRT Flying Spot Scanner) 遥测重构
        """
        # 1. 胶片与药卷
        film_total_length_m = 80.0  # 260 ft 70mm SO-243 胶片
        bimat_web_length_m = 79.0   # 浸润单浴显影定影剂的聚酯带
        development_temp_c = 29.4   # 85°F 恒温水夹套
        development_time_min = 3.4  # 3.4 分钟层压显影

        # 2. 飞点扫描系统 (Flying Spot Scanner)
        spot_size_um = 5.0          # 5 微米电子束斑点
        scan_width_mm = 2.68        # 每个条带 (Framelet) 宽 2.68 mm
        scan_length_mm = 57.0       # 条带长 57 mm
        lines_per_mm = 287.0        # 287 线/毫米超高线密
        lines_per_framelet = int(scan_width_mm * lines_per_mm * 22) # 约 17,000 扫描线
        framelets_per_hr_frame = 117 # 每张远摄大图切分为 117 个条带

        # 3. S 频段通信下传 (S-band TWTA Downlink)
        carrier_freq_mhz = 2295.0   # 2.295 GHz
        transmitter_power_w = 10.0  # 10 W 行波管放大器 (TWTA)
        video_bandwidth_khz = 310.0
        time_per_framelet_s = 42.0  # 每个 framelet 需 42 秒逐行扫描下传
        time_per_dual_photo_min = (framelets_per_hr_frame * time_per_framelet_s) / 60.0

        # 总图像数据量
        total_photos_taken = 211    # 211 对双镜头底片 (422 幅独立图像)
        primary_apollo_sites = 13   # 13 个阿波罗初选候选着陆区

        return {
            "chemical_processing": {
                "process_name": "Eastman Kodak Bimat Diffusion-Transfer Process",
                "film_stock": "Kodak SO-243 (70mm unperforated thin-base aerial)",
                "film_capacity_meters": film_total_length_m,
                "bimat_reagent_web_meters": bimat_web_length_m,
                "process_temperature_c": development_temp_c,
                "lamination_contact_time_min": development_time_min,
                "zero_gravity_advantage": "全固态接触反应，彻底杜绝失重环境下游离液体气泡和化学液滴漂浮造成的灾难性污染。"
            },
            "flying_spot_scanner": {
                "electron_beam_diameter_microns": spot_size_um,
                "framelet_width_mm": scan_width_mm,
                "framelet_length_mm": scan_length_mm,
                "effective_scan_density_lines_per_mm": lines_per_mm,
                "approx_lines_per_framelet": lines_per_framelet,
                "framelets_per_telephoto_frame": framelets_per_hr_frame,
                "photomultiplier_tube": "RCA 931A PMT (光电倍增管光电模拟信号转换)"
            },
            "s_band_downlink": {
                "carrier_frequency_ghz": round(carrier_freq_mhz / 1e3, 3),
                "twta_rf_power_watts": transmitter_power_w,
                "video_bandwidth_khz": video_bandwidth_khz,
                "readout_time_per_framelet_s": time_per_framelet_s,
                "readout_time_per_full_frame_min": round(time_per_dual_photo_min, 1),
                "dsn_stations": ["Goldstone DSS 11/12", "Madrid DSS 61", "Woomera DSS 41"]
            },
            "reconnaissance_output": {
                "dual_frame_exposures": total_photos_taken,
                "total_individual_images": total_photos_taken * 2,
                "primary_apollo_sites_covered": primary_apollo_sites,
                "apollo_11_site_verified": "Primary Site 2 (Mare Tranquillitatis / 静海)"
            }
        }

    def compute_mascon_gravitational_perturbation(self):
        """
        解算多普勒跟踪摄动与月球质量瘤 (Mascon) 重力异常发现机制
        """
        # LO-2 在经过雨海 (Mare Imbrium) 上空时的多普勒残差
        doppler_velocity_residual_mm_s = 12.0  # +12 mm/s 加速残差
        orbital_alt_m = 45.1e3                # 45.1 km

        # 质量瘤过剩引力加速度估算
        # delta_a ~ (delta_v / delta_t) 约 1.2e-3 m/s^2 (120 mGal)
        delta_g_mgal = 125.0
        delta_g_m_s2 = delta_g_mgal * 1.0e-5

        # 估算雨海质量瘤多余质量 (Point-mass / disk excess mass)
        # delta_g = G * delta_M / r^2 -> delta_M = delta_g * r^2 / G
        r_eff = orbital_alt_m + 30.0e3 # 假设质量瘤埋深 30 km
        excess_mass_kg = (delta_g_m_s2 * r_eff**2) / self.G

        return {
            "doppler_tracking_perturbation": {
                "carrier_band": "S-band (2.295 GHz)",
                "doppler_residual_peak_mm_s": doppler_velocity_residual_mm_s,
                "gravity_anomaly_mgal": delta_g_mgal,
                "excess_gravity_acceleration_m_s2": delta_g_m_s2,
                "target_basin": "Mare Imbrium (雨海盆地)",
                "estimated_excess_mass_kg": excess_mass_kg,
                "discovery_by": "Muller & Sjogren (1968, Science)",
                "mascon_nature": "撞击熔融与晚期玄武岩致密深层充填形成的高密度正引力异常体",
                "apollo_criticality": "若不纳入质量瘤非球形引力场摄动，阿波罗登月舱降轨下降阶段的近月点高度将产生数公里的不可控误差，导致登月失败。"
            }
        }

    def compute_exploration_continuum(self):
        """
        横向对照 1964~2026 深空探测多重里程碑：
        1. 1964-11-05 水手3号 (Mariner 3) 罩整流罩故障教训与水手4号快速更迭
        2. 1966-10-22 月球12号 (Luna 12) 苏联 Enisei-3 电视扫描钻禧
        3. 1966-11-06 月球轨道器2号 (Lunar Orbiter 2) 美国干式扫描与世纪之照钻禧
        4. 2007-11-05 嫦娥一号 (Chang'e-1) 近月制动 19 周年与全月三维图
        5. 2013-11-05 曼加里安号 (Mangalyaan MOM) 奥伯斯效应火星发射 13 周年
        6. 2018-11-05 旅行者2号 (Voyager 2) 星际穿越 8 周年
        """
        return {
            "mariner_3_1964": {
                "launch_utc": "1964-11-05 19:22:05",
                "target": "Mars flyby",
                "failure_mode": "玻纤整流罩未分离，阻碍太阳翼展开，8.7 小时电池耗尽",
                "heliocentric_orbit": "0.984 AU x 1.311 AU, period 448.7 days",
                "legacy": "23 天极限更换镁钍合金整流罩，成就 1964-11-28 水手4号首获火星特写"
            },
            "luna_12_1966": {
                "launch_utc": "1966-10-22 08:42:26",
                "arrival_utc": "1966-10-25 20:45",
                "orbit_km": "133 x 1200",
                "technology": "苏联 Enisei-3 湿式药水显影 + 1100 线机械分面电视扫描",
                "diamond_jubilee": 60
            },
            "lunar_orbiter_2_1966": {
                "launch_utc": "1966-11-06 23:21:00",
                "arrival_utc": "1966-11-10 20:26",
                "orbit_km": "45.1 x 1843",
                "technology": "美国柯达 Bimat 干式覆膜显影 + 5微米飞点阴极射线管扫描",
                "diamond_jubilee": 60,
                "highlight": "哥白尼环形山世纪之照 + 发现月球质量瘤 (Mascon) + 查明静海阿波罗11着陆场"
            },
            "change_1_2007": {
                "launch_utc": "2007-10-24 18:05",
                "loi_1_cst": "2007-11-05 11:15",
                "orbit_km": "200 km 极月圆轨道",
                "technology": "三线阵 CCD 推扫立体相机，120米全月三维地图，轨道播发中华名曲",
                "anniversary_years": 19
            },
            "mangalyaan_2013": {
                "launch_utc": "2013-11-05 09:08",
                "orbit_km": "421.7 x 76994 (Mars)",
                "technology": "近地点连续 6 次升轨奥伯斯效应机动，7300万美元极限深空探测",
                "anniversary_years": 13
            },
            "voyager_2_2018": {
                "heliopause_crossing_utc": "2018-11-05",
                "crossing_distance_au": 119.7,
                "current_distance_au": 144.3,
                "one_way_light_time_hours": 20.18,
                "anniversary_years": 8
            }
        }
