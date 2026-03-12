import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
import matplotlib.pyplot as plt

from Drawing import drawing
from Computing_stable import UI_Computing,  PC_QC_P_Computing, Computing_RT_Power


#文件路径和设备名称
global file_paths

file_paths = [
    'C:\\Users\\hp\\Desktop\\project\\Py-Propect\\AI2023.六月期末大作业\\电力负荷监测与分解\\data\\附件1\\YD1.xlsx',
    'C:\\Users\\hp\\Desktop\\project\\Py-Propect\\AI2023.六月期末大作业\\电力负荷监测与分解\\data\\附件1\\YD2.xlsx',
    'C:\\Users\\hp\\Desktop\\project\\Py-Propect\\AI2023.六月期末大作业\\电力负荷监测与分解\\data\\附件1\\YD3.xlsx',
    'C:\\Users\\hp\\Desktop\\project\\Py-Propect\\AI2023.六月期末大作业\\电力负荷监测与分解\\data\\附件1\\YD4.xlsx',
    'C:\\Users\\hp\\Desktop\\project\\Py-Propect\\AI2023.六月期末大作业\\电力负荷监测与分解\\data\\附件1\\YD5.xlsx',
    'C:\\Users\\hp\\Desktop\\project\\Py-Propect\\AI2023.六月期末大作业\\电力负荷监测与分解\\data\\附件1\\YD6.xlsx',
    'C:\\Users\\hp\\Desktop\\project\\Py-Propect\\AI2023.六月期末大作业\\电力负荷监测与分解\\data\\附件1\\YD7.xlsx',
    'C:\\Users\\hp\\Desktop\\project\\Py-Propect\\AI2023.六月期末大作业\\电力负荷监测与分解\\data\\附件1\\YD8.xlsx',
    'C:\\Users\\hp\\Desktop\\project\\Py-Propect\\AI2023.六月期末大作业\\电力负荷监测与分解\\data\\附件1\\YD9.xlsx',
    'C:\\Users\\hp\\Desktop\\project\\Py-Propect\\AI2023.六月期末大作业\\电力负荷监测与分解\\data\\附件1\\YD10.xlsx',
    'C:\\Users\\hp\\Desktop\\project\\Py-Propect\\AI2023.六月期末大作业\\电力负荷监测与分解\\data\\附件1\\YD11.xlsx'
]

Unknow_devices_paths = [
    'C:\\Users\\hp\\Desktop\\project\\Py-Propect\\AI2023.六月期末大作业\\电力负荷监测与分解\\data\\附件2\\设备1（YD8）.xlsx',
    'C:\\Users\\hp\\Desktop\\project\\Py-Propect\\AI2023.六月期末大作业\\电力负荷监测与分解\\data\\附件2\\设备2（YD9）.xlsx'
]

device_names = ['YD1', 'YD2', 'YD3', 'YD4', 'YD5', 'YD6', 'YD7', 'YD8', 'YD9', 'YD10', 'YD11']
#globals(device_names)







if __name__ == '__main__':
    draw = drawing()
    comUI = UI_Computing()
    comPQP = PC_QC_P_Computing()

#---------------------------------------画IC-t, UC-t,计算稳态下四个设备的UI----------------------------------------##
    draw.draw_UI()
    plt.show()
#
    comUI.compute_YD1(file_paths[0])  #计算落地风扇
    comUI.compute_YD8(file_paths[7])  #计算饮水机
    comUI.compute_YD9(file_paths[8])  #计算挂式空调
    comUI.compute_YD3(file_paths[2])   #计算热水壶
#

#----------------------------------画PC,QC-t, P-t,计算稳态下四个设备的不同状态下的平均值, 标准差-----------------------------##
    draw.draw_PC_QC_P()  #画PC-T, QC-t，P-t
    plt.show()

    comPQP.compute_YD8(file_paths[7])  #计算饮水机
    comPQP.compute_YD3(file_paths[2])  #计算热水壶
    comPQP.compute_YD9(file_paths[8])  #计算挂式空调
    plt.show()


#-----------------------------------------------画出所有识别U-I图---------------------------------------------##
#--------------------------------------------------未成功----------------------------------------------------##
    # draw.draw_U_I()
    # plt.show()

#--- ----------------------------------------------画出所有设备瞬时功率------------------------------------------##
    # draw.draw_ins_p()
    # plt.show()
#
#
# #---------------------------------------------------计算实时用电量---------------------------------------------##
    Computing_RT_Power()
#
#
# ######################################################################################################################
# ######################################################################################################################
# #---------------------------------------------------计算未知设备特征值---------------------------------------------##
#
    comUI.compute_unknow1(Unknow_devices_paths[0])  ##计算未知设备1的电流均值，最大值，范围值
    print('====================================================')
    comPQP.compute_unknow1(Unknow_devices_paths[0])  ##计算未知设备1的有功无功功率因数均值，标准差
#
#     #
    comUI.compute_unknow2(Unknow_devices_paths[1])  ##计算未知设备2的电流均值，最大值，范围值
    print('====================================================')
    comPQP.compute_unknow2(Unknow_devices_paths[1])  ##计算未知设备2的有功无功功率因数均值，标准差





