# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 11:01:21 2020
这是一个抓取气象数据的程序
@author: 何旸
"""
import numpy as np
from ladybug.epw import EPW #读取energyplus文件
epw_data=EPW(r'Singapore.epw')
dry_bulb_temp=epw_data.dry_bulb_temperature
rela_humi=epw_data.relative_humidity
dire_norm_radia=epw_data.direct_normal_radiation
diff_hori_radia=epw_data.diffuse_horizontal_radiation
sky_temp=epw_data.sky_temperature
ground_temp=dry_bulb_temp
wind_velocity=epw_data.wind_speed
Weather=[dry_bulb_temp.values,rela_humi.values,dire_norm_radia.values,
    diff_hori_radia.values,sky_temp.values,ground_temp.values,wind_velocity.values]
Weather=np.array(Weather)
Weather=np.transpose(Weather)
Weather[:,4]=Weather[:,4]+273.15
A=np.insert(Weather,-1,values=Weather[8759],axis=0)
