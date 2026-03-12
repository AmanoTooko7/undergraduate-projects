##用于做出YD1-YD11以时间为纵坐标以I,U横坐标得到所有T-(U,I)图像

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import MinMaxScaler

# 文件路径列表
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
device_names = ['YD1', 'YD2', 'YD3', 'YD4', 'YD5', 'YD6', 'YD7', 'YD8', 'YD9', 'YD10', 'YD11']

class drawing:

##------------------------------------------画出YD1-YD11所有U,I-t图-----------------------------------------------------##

    def draw_UI(self):
        device_names = ['YD1', 'YD2', 'YD3', 'YD4', 'YD5', 'YD6', 'YD7', 'Y8', 'YD9', 'YD10', 'YD11']
        def plot_data(file_path, device_name):
            # 读取数据
            df = pd.read_excel(file_path, sheet_name='设备数据')

            # 计算相对于起点的时间差
            start_time = pd.to_datetime(df['time']).min()
            df['time_diff'] = (pd.to_datetime(df['time']) - start_time).dt.total_seconds()

            # 缩放IC和UC的值
            df['IC'] = df['IC'] / 1000
            df['UC'] = df['UC'] / 10

            # 创建图形对象和坐标轴对象
            fig, ax1 = plt.subplots()
            ax2 = ax1.twinx()

            # 绘制IC数据
            ax1.plot(df['time_diff'], df['IC'], label='IC', color='blue')

            # 绘制UC数据
            ax2.plot(df['time_diff'], df['UC'], label='UC', color='red')

            # 设置坐标轴标签和图例
            ax1.set_xlabel('Time (seconds)')
            ax1.set_ylabel('Current (A)')
            ax2.set_ylabel('Voltage (V)')

            ax1.legend(loc='upper left')
            ax2.legend(loc='upper right')
            # 添加设备名称标签
            ax1.text(0.01, 0.915, device_name, transform=ax1.transAxes, fontsize=12, fontweight='bold', va='top')

        # 循环处理每个文件
        for file_path, device_names in zip(file_paths, device_names):
             plot_data(file_path, device_names)
        #plt.show()



    ##-------------------------------------画出YD1-YD11所有PC-T,QC-T,P-T图------------------------------------------------##
    def draw_PC_QC_P(self):
        def plot_data(file_path, device_name):
            # 读取数据
            df = pd.read_excel(file_path, sheet_name='设备数据')

            # 计算相对于起点的时间差
            start_time = pd.to_datetime(df['time']).min()
            df['time_diff'] = (pd.to_datetime(df['time']) - start_time).dt.total_seconds()

            # 创建图形对象和坐标轴对象
            fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True)

            # 绘制PC和QC数据
            ax1.plot(df['time_diff'], df['PC'], label='PC', color='blue')
            ax1.plot(df['time_diff'], df['QC'], label='QC', color='red')

            # 绘制P数据
            ax2.plot(df['time_diff'], df['PFC'], label='P', color='green')

            # 设置坐标轴标签和图例
            ax1.set_xlabel('Time (seconds)')
            ax1.set_ylabel('Power 0.0001KW')
            ax2.set_ylabel('PFC % ')

            ax1.legend(loc='upper left')
            ax2.legend(loc='upper left')

            # 添加设备名称标签
            ax1.text(0.01, 0.72, device_name, transform=ax1.transAxes, fontsize=12, fontweight='bold', va='top')

        # 循环处理每个文件
        for file_path, device_name in zip(file_paths, device_names):
            plot_data(file_path, device_name)


##-------------------------------------------画出YD1-YD11所有U-I图像----------------------------------------------------##
    def draw_U_I(self):
        device_names = ['YD1', 'YD2', 'YD3', 'YD4', 'YD5', 'YD6', 'YD7', 'Y8', 'YD9', 'YD10', 'YD11']

        def plot_data(file_path, device_name):

            df = pd.read_excel(file_path, sheet_name='周波数据')

            IC_data = df.iloc[:, 1:129].values  # 读取所有行的电流数据，从第2列到第129列
            UC_data = df.iloc[:, 129:257].values  # 读取所有行的电压数据，从第130列到第257列

            # IC_data = df.iloc[1, 1:129].values #读取一行数据
            # UC_data = df.iloc[1, 129:257].values #读取一行电压数据

            # print(IC_data)
            # print()

            # 将二维数组转置，以便按列提取数据
            IC_data = IC_data.T
            UC_data = UC_data.T

            # # 归一化处理
            # scaler = MinMaxScaler(feature_range=(-1, 1))
            # IC_data = scaler.fit_transform(IC_data)
            # UC_data = scaler.fit_transform(UC_data)

            # 创建图形对象和坐标轴对象
            fig, ax = plt.subplots()

            len(IC_data)
            # 绘制曲线图
            for i in range(len(IC_data)):
                #ax.plot(IC_data[i], UC_data[i])

                ax.scatter(UC_data[i]/10, IC_data[i]/10000, s=1)

            # 设置坐标轴标签和图例
            ax.set_xlabel('IC')
            ax.set_ylabel('UC')
            ax.set_title(f'{device_name} - V-I Curve')
            ax.legend()

            

        for file_path, device_name in zip(file_paths, device_names):
            plot_data(file_path, device_name)



##-------------------------------------------画出YD1-YD11所有瞬时功率图像----------------------------------------------------##


    def draw_ins_p(self):

        def plot_data(file_path, device_name):
            # 读取数据
            df = pd.read_excel(file_path)

            # 计算相对于起点的时间差
            start_time = pd.to_datetime(df['time']).min()
            df['time_diff'] = (pd.to_datetime(df['time']) - start_time).dt.total_seconds()

            # 缩放IC和UC的值
            df['IC'] = df['IC'] / 1000
            df['UC'] = df['UC'] / 10

            # 创建图形对象和坐标轴对象
            fig, ax1 = plt.subplots()
            ax2 = ax1.twinx()

            # 绘制UC*IC数据
            ax1.plot(df['time_diff'], df['IC'] * df['UC'], label='Ins-P', color='blue')

            # 设置坐标轴标签和图例
            ax1.set_xlabel('Time (seconds)')
            ax1.set_ylabel('ins-P (W)')

            ax1.legend(loc='upper left')
            ax2.legend(loc='upper right')
            # 添加设备名称标签
            ax1.text(0.01, 0.915, device_name, transform=ax1.transAxes, fontsize=12, fontweight='bold', va='top')

        # 循环处理每个文件
        for file_path, device_name in zip(file_paths, device_names):
            plot_data(file_path, device_name)




