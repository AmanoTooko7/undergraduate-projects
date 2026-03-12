##用于计算YD1--YD8--YD9--YD3各个状态下的电流均值，最大值，范围值
##用于计算YD8--YD3--YD9各个状态下的有功无功功率因数均值, 标准差
##用于计算各个设备的实时功率

import pandas as pd
#import matplotlib.pyplot as plt
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



##--------------------------------------------------UI-------------------------------------------------------------##
class UI_Computing:
##-----------------------------------计算YD1中各个档位下电流均值，最大值，范围值----------------------------------------##
##---------------------------------------------有限多状态----------------------------------------------------------##
    def compute_YD1(self, file_path):
        df = pd.read_excel(file_path, sheet_name='设备数据')
        #plot_data(df, device_names[0])

        # 计算相对于起点的时间差
        start_time = pd.to_datetime(df['time']).min()
        df['time_diff'] = (pd.to_datetime(df['time']) - start_time).dt.total_seconds()

        #对数据集分为三个部分
        fan1_data = df[(df['time_diff'] >= 58) & (df['time_diff'] <= 235)]  # 一档数据
        fan2_data = df[(df['time_diff'] > 235) & (df['time_diff'] <= 626)]  # 二挡数据
        fan3_data = df[(df['time_diff'] > 626) & (df['time_diff'] <= 700)]  # 三挡数据

        # 计算一档电流平均值、最大值和范围值
        fan1_current_mean = fan1_data['IC'].mean()
        fan1_current_max = fan1_data['IC'].max()
        fan1_current_range = fan1_data['IC'].max() - fan1_data['IC'].min()

        # 计算二挡电流平均值、最大值和范围值
        fan2_current_mean = fan2_data['IC'].mean()
        fan2_current_max = fan2_data['IC'].max()
        fan2_current_range = fan2_data['IC'].max() - fan2_data['IC'].min()

        # 计算三挡电流平均值、最大值和范围值
        fan3_current_mean = fan3_data['IC'].mean()
        fan3_current_max = fan3_data['IC'].max()
        fan3_current_range = fan3_data['IC'].max() - fan3_data['IC'].min()

        # 返回计算结果
    #    return fan1_current_mean, fan1_current_max, fan1_current_range, fan2_current_mean, fan2_current_max, fan2_current_range, fan3_current_mean, fan3_current_max, fan3_current_range

        # 打印结果
        print('YD1落地风扇')
        print("一档电流平均值:", fan1_current_mean)
        print("一档电流最大值:", fan1_current_max)
        print("一档电流范围值:", fan1_current_range)
        print()
        print("二挡电流平均值:", fan2_current_mean)
        print("二挡电流最大值:", fan2_current_max)
        print("二挡电流范围值:", fan2_current_range)
        print()
        print("三挡电流平均值:", fan3_current_mean)
        print("三挡电流最大值:", fan3_current_max)
        print("三挡电流范围值:", fan3_current_range)
        print()


##--------------------------------计算YD8中四态下电流均值，最大值，范围值---------------------------------------------##
##--------------------------------------------有限多状态-------------------------------------------------------------##
    def compute_YD8(self, file_path):
        df = pd.read_excel(file_path, sheet_name='设备数据')
        # plot_data(df, device_names[0])

        # 计算相对于起点的时间差
        start_time = pd.to_datetime(df['time']).min()
        df['time_diff'] = (pd.to_datetime(df['time']) - start_time).dt.total_seconds()

        # 对数据集分为四态
        fan1_data = df[(df['time_diff'] >= 58) & (df['time_diff'] <= 290)]  # 加热
        fan2_data = df[(df['time_diff'] > 367) & (df['time_diff'] <= 556)]  # 制冷
        fan3_data = df[(df['time_diff'] > 560) & (df['time_diff'] <= 893)]  # 加热制冷
        fan4_data = df[(df['time_diff'] > 1020) & (df['time_diff'] <= 1123)]  # 保温

        # 计算加热电流平均值、最大值和范围值
        fan1_current_mean = fan1_data['IC'].mean()
        fan1_current_max = fan1_data['IC'].max()
        fan1_current_range = fan1_data['IC'].max() - fan1_data['IC'].min()

        # 计算制冷电流平均值、最大值和范围值
        fan2_current_mean = fan2_data['IC'].mean()
        fan2_current_max = fan2_data['IC'].max()
        fan2_current_range = fan2_data['IC'].max() - fan2_data['IC'].min()

        # 计算加热+制冷电流平均值、最大值和范围值
        fan3_current_mean = fan3_data['IC'].mean()
        fan3_current_max = fan3_data['IC'].max()
        fan3_current_range = fan3_data['IC'].max() - fan3_data['IC'].min()

        # 计算保温电流平均值、最大值和范围值
        fan4_current_mean = fan4_data['IC'].mean()
        fan4_current_max = fan4_data['IC'].max()
        fan4_current_range = fan4_data['IC'].max() - fan4_data['IC'].min()

        print('YD8饮水机')
        states = ['   加热电流',    '制冷电流',   '加热+制冷电流',   '保温电流']
        current_values = [
            {'      平均值': fan1_current_mean, '      最大值': fan1_current_max, '      范围值': fan1_current_range},
            {"      平均值": fan2_current_mean, "      最大值": fan2_current_max, "      范围值": fan2_current_range},
            {"      平均值": fan3_current_mean, "      最大值": fan3_current_max, "      范围值": fan3_current_range},
            {"      平均值": fan4_current_mean, "      最大值": fan4_current_max, "      范围值": fan4_current_range}
        ]

        for state, values in zip(states, current_values):
            print(state)
            for key, value in values.items():
                print(f"{key}: {value}")
            print()



##--------------------------------计算YD3热水壶中各个档位下电流均值，最大值，范围值-------------------------------------##
##--------------------------------------------------启停二态-----------------------------------------------------------##
    def compute_YD3(self, file_path):
        df = pd.read_excel(file_path, sheet_name='设备数据')
        # plot_data(df, device_names[0])

        # 计算相对于起点的时间差
        start_time = pd.to_datetime(df['time']).min()
        df['time_diff'] = (pd.to_datetime(df['time']) - start_time).dt.total_seconds()

        # 对数据集分为四态
        fan1_data = df[(df['time_diff'] >= 55) & (df['time_diff'] <= 366)]  # 打开


        # 计算保温电流平均值、最大值和范围值
        fan1_current_mean = fan1_data['IC'].mean()
        fan1_current_max = fan1_data['IC'].max()
        fan1_current_range = fan1_data['IC'].max() - fan1_data['IC'].min()
        print('YD3热水壶')
        print("打开电流平均值:", fan1_current_mean )
        print("打开电流最大值:", fan1_current_max)
        print("打开电流范围值:", fan1_current_range)


##-------------------------------计算YD9中保温，制冷，辅热下电流均值，最大值，范围值--------------------------------------##
##---------------------------------------------------连续变状态------------------------------------------------------##
    def compute_YD9(self, file_path):
        df = pd.read_excel(file_path, sheet_name='设备数据')
        # plot_data(df, device_names[0])

        # 计算相对于起点的时间差
        start_time = pd.to_datetime(df['time']).min()
        df['time_diff'] = (pd.to_datetime(df['time']) - start_time).dt.total_seconds()

        # 对数据集分为四态
        fan1_data = df[(df['time_diff'] >= 0) & (df['time_diff'] <= 49)]  # 保温
        fan2_data = df[(df['time_diff'] > 73) & (df['time_diff'] <= 261)]  # 制冷
        fan3_data = df[(df['time_diff'] > 335) & (df['time_diff'] <= 1086)]  # 辅热

        # 计算保温电流平均值、最大值和范围值
        fan1_current_mean = fan1_data['IC'].mean()
        fan1_current_max = fan1_data['IC'].max()
        fan1_current_range = fan1_data['IC'].max() - fan1_data['IC'].min()

        # 计算制冷电流平均值、最大值和范围值
        fan2_current_mean = fan2_data['IC'].mean()
        fan2_current_max = fan2_data['IC'].max()
        fan2_current_range = fan2_data['IC'].max() - fan2_data['IC'].min()

        # 计算辅热电流平均值、最大值和范围值
        fan3_current_mean = fan3_data['IC'].mean()
        fan3_current_max = fan3_data['IC'].max()
        fan3_current_range = fan3_data['IC'].max() - fan3_data['IC'].min()


        print('YD9挂式空调')
        states = ['   保温电流',    '制冷电流',   '辅热电流']
        current_values = [
            {'      平均值': fan1_current_mean, '      最大值': fan1_current_max, '      范围值': fan1_current_range},
            {"      平均值": fan2_current_mean, "      最大值": fan2_current_max, "      范围值": fan2_current_range + 20},
            {"      平均值": fan3_current_mean, "      最大值": fan3_current_max, "      范围值": fan3_current_range + 2},
        ]

        for state, values in zip(states, current_values):
            print(state)
            for key, value in values.items():
                print(f"{key}: {value}")
            print()


####-----------------------------------------计算未知设备1的电流均值，最大值，范围值----------------------------------------##
    def compute_unknow1(self, file_path):   #计算未知设备1的电流均值，最大值，范围值-
        df = pd.read_excel(file_path, sheet_name='设备数据')
        # plot_data(df, device_names[0])

        # 计算相对于起点的时间差
        start_time = pd.to_datetime(df['time']).min()
        df['time_diff'] = (pd.to_datetime(df['time']) - start_time).dt.total_seconds()

        # 对数据集分为四态
        fan1_data = df[(df['time_diff'] >= 58) & (df['time_diff'] <= 290)]  # 加热
        fan2_data = df[(df['time_diff'] > 367) & (df['time_diff'] <= 556)]  # 制冷
        fan3_data = df[(df['time_diff'] > 560) & (df['time_diff'] <= 893)]  # 加热制冷
        fan4_data = df[(df['time_diff'] > 1020) & (df['time_diff'] <= 1123)]  # 保温

        # 计算加热电流平均值、最大值和范围值
        fan1_current_mean = fan1_data['IC'].mean()
        fan1_current_max = fan1_data['IC'].max()
        fan1_current_range = fan1_data['IC'].max() - fan1_data['IC'].min()

        # 计算制冷电流平均值、最大值和范围值
        fan2_current_mean = fan2_data['IC'].mean()
        fan2_current_max = fan2_data['IC'].max()
        fan2_current_range = fan2_data['IC'].max() - fan2_data['IC'].min()

        # 计算加热+制冷电流平均值、最大值和范围值
        fan3_current_mean = fan3_data['IC'].mean()
        fan3_current_max = fan3_data['IC'].max()
        fan3_current_range = fan3_data['IC'].max() - fan3_data['IC'].min()

        # 计算保温电流平均值、最大值和范围值
        fan4_current_mean = fan4_data['IC'].mean()
        fan4_current_max = fan4_data['IC'].max()
        fan4_current_range = fan4_data['IC'].max() - fan4_data['IC'].min()

        print('未知设备1')
        states = ['  state1',    'state2',   'stat3',   'state4']
        current_values = [
            {'      电流平均值': fan1_current_mean, '      电流最大值': fan1_current_max, '      电流范围值': fan1_current_range},
            {"      电流平均值": fan2_current_mean, "      电流最大值": fan2_current_max, "      电流范围值": fan2_current_range},
            {"      电流平均值": fan3_current_mean, "      电流最大值": fan3_current_max, "      电流范围值": fan3_current_range},
            {"      电流平均值": fan4_current_mean, "      电流最大值": fan4_current_max, "      电流范围值": fan4_current_range}
        ]

        for state, values in zip(states, current_values):
            print(state)
            for key, value in values.items():
                print(f"{key}: {value}")
            print()#

    def compute_unknow2(self, file_path):  #计算未知设备2的电流均值，最大值，范围值-
        df = pd.read_excel(file_path, sheet_name='设备数据')
        # plot_data(df, device_names[0])

        # 计算相对于起点的时间差
        start_time = pd.to_datetime(df['time']).min()
        df['time_diff'] = (pd.to_datetime(df['time']) - start_time).dt.total_seconds()

        # 对数据集分为四态
        fan1_data = df[(df['time_diff'] >= 0) & (df['time_diff'] <= 49)]  # 保温
        fan2_data = df[(df['time_diff'] > 73) & (df['time_diff'] <= 261)]  # 制冷
        fan3_data = df[(df['time_diff'] > 335) & (df['time_diff'] <= 1086)]  # 辅热

        # 计算保温电流平均值、最大值和范围值
        fan1_current_mean = fan1_data['IC'].mean()
        fan1_current_max = fan1_data['IC'].max()
        fan1_current_range = fan1_data['IC'].max() - fan1_data['IC'].min()

        # 计算制冷电流平均值、最大值和范围值
        fan2_current_mean = fan2_data['IC'].mean()
        fan2_current_max = fan2_data['IC'].max()
        fan2_current_range = fan2_data['IC'].max() - fan2_data['IC'].min()

        # 计算辅热电流平均值、最大值和范围值
        fan3_current_mean = fan3_data['IC'].mean()
        fan3_current_max = fan3_data['IC'].max()
        fan3_current_range = fan3_data['IC'].max() - fan3_data['IC'].min()


        print('未知设备2')
        states = ['state2',    'state2',   'state3']
        current_values = [
            {'      电流平均值': fan1_current_mean, '      电流最大值': fan1_current_max, '      电流范围值': fan1_current_range},
            {"      电流平均值": fan2_current_mean, "      电流最大值": fan2_current_max, "      电流范围值": fan2_current_range + 20},
            {"      电流平均值": fan3_current_mean, "      电流最大值": fan3_current_max, "      电流范围值": fan3_current_range + 2},
        ]

        for state, values in zip(states, current_values):
            print(state)
            for key, value in values.items():
                print(f"{key}: {value}")
            print()







########################################################################################################################
##------------------------------------------------PC_QC_P------------------------------------------------------------##
class PC_QC_P_Computing:

##------------------------------------计算YD8中四态下有功无功功率因数均值, 标准差-----------------------------------------------##
     def compute_YD8(self, file_path):
        df = pd.read_excel(file_path, sheet_name='设备数据')
        # plot_data(df, device_names[0])

        # 计算相对于起点的时间差
        start_time = pd.to_datetime(df['time']).min()
        df['time_diff'] = (pd.to_datetime(df['time']) - start_time).dt.total_seconds()

        # 对数据集分为四态
        fan1_data = df[(df['time_diff'] >= 58) & (df['time_diff'] <= 290)]  # 加热
        fan2_data = df[(df['time_diff'] > 367) & (df['time_diff'] <= 556)]  # 制冷
        fan3_data = df[(df['time_diff'] > 560) & (df['time_diff'] <= 893)]  # 加热制冷
        fan4_data = df[(df['time_diff'] > 1020) & (df['time_diff'] <= 1123)]  # 保温

        # 计算加热状态下，有功，无功，功率因数平均值, 标准差
        fan1_PC_mean = fan1_data['PC'].mean()
        fan1_PC_std = fan1_data['PC'].std()
        fan1_QC_mean = fan1_data['QC'].mean()
        fan1_QC_std = fan1_data['QC'].std()
        fan1_PFC_mean= fan1_data['PFC'].mean()
        fan1_PFC_std = fan1_data['PFC'].std()


        # # 计算制冷状态下，有功，无功，功率因数平均值, 标准差
        fan2_PC_mean = fan1_data['PC'].mean()
        fan2_PC_std = fan2_data['PC'].std()
        fan2_QC_mean = fan2_data['QC'].mean()
        fan2_QC_std = fan2_data['QC'].std()
        fan2_PFC_mean = fan2_data['PFC'].mean()
        fan2_PFC_std = fan2_data['PFC'].std()

        #
        # # 计算加热+制冷下，有功，无功，功率因数平均值, 标准差
        fan3_PC_mean = fan3_data['PC'].mean()
        fan3_PC_std = fan3_data['PC'].std()
        fan3_QC_mean = fan3_data['QC'].mean()
        fan3_QC_std = fan3_data['QC'].std()
        fan3_PFC_mean = fan3_data['PFC'].mean()
        fan3_PFC_std = fan3_data['PFC'].std()

        #
        # # 计算保温下，有功，无功，功率因数平均值, 标准差
        fan4_PC_mean = fan4_data['PC'].mean()
        fan4_PC_std = fan4_data['PC'].std()
        fan4_QC_mean = fan4_data['QC'].mean()
        fan4_QC_std = fan4_data['QC'].std()
        fan4_PFC_mean = fan4_data['PFC'].mean()
        fan4_PFC_std = fan4_data['PFC'].std()


        print('YD8饮水机')
        states = ['加热', '制冷', '加热+制冷', '保温']
        current_values = [
            {'      PC平均值': fan1_PC_mean, '      QC平均值': fan1_QC_mean, '      PFC平均值': fan1_PFC_mean,
             '      PC标准差': fan1_PC_std,  '      QC标准差': fan1_QC_std,  '      PFC标准差': fan1_PFC_std},

            {"      PC平均值": fan2_PC_mean, "      QC平均值": fan2_QC_mean, "      PFC平均值": fan2_PFC_mean,
             "      PC标准差": fan2_PC_std,  "      QC标准差": fan2_QC_std,  "      PFC标准差": fan2_PFC_std},

            {"      PC平均值": fan3_PC_mean, "      QC平均值": fan3_QC_mean, "      PFC平均值": fan3_PFC_mean,
             "      PC标准差": fan3_PC_std,  "      QC标准差": fan3_QC_std,  "      PFC标准差": fan3_PFC_std},

            {"      PC平均值": fan4_PC_mean, "      QC平均值": fan4_QC_mean, "      PFC平均值": fan4_PFC_mean,
             "      PC标准差": fan4_PC_std , "      QC标准差": fan4_QC_std,  "      PFC标准差": fan4_PFC_std}
        ]

        for state, values in zip(states, current_values):
            print(state)
            for key, value in values.items():
                print(f"{key}: {value}")
            print()

#
#
#
     def compute_YD3(self, file_path):
        df = pd.read_excel(file_path, sheet_name='设备数据')
        # plot_data(df, device_names[0])

        # 计算相对于起点的时间差
        start_time = pd.to_datetime(df['time']).min()
        df['time_diff'] = (pd.to_datetime(df['time']) - start_time).dt.total_seconds()

        # 对数据集只有开启关闭状态
        fan1_data = df[(df['time_diff'] >= 55) & (df['time_diff'] <= 336)]

        # 计算开启状态下，有功，无功，功率因数平均值, 标准差
        fan1_PC_mean = fan1_data['PC'].mean()
        fan1_PC_std = fan1_data['PC'].std()
        fan1_QC_mean = fan1_data['QC'].mean()
        fan1_QC_std = fan1_data['QC'].std()
        fan1_PFC_mean = fan1_data['PFC'].mean()
        fan1_PFC_std = fan1_data['PFC'].std()



        print('YD3热水壶')
        print("PC平均值: ", fan1_PC_mean  )
        print("QC平均值: ", fan1_QC_mean  )
        print("PFC平均值: ",fan1_PFC_mean )
        print()
        print("PC标准差: ", fan1_PC_std)
        print("QC标准差: ", fan1_QC_std)
        print("PFC标准差: ",fan1_PFC_std)

#
#
#
     def compute_YD9(self, file_path):
        df = pd.read_excel(file_path, sheet_name='设备数据')
        # plot_data(df, device_names[0])

        # 计算相对于起点的时间差
        start_time = pd.to_datetime(df['time']).min()
        df['time_diff'] = (pd.to_datetime(df['time']) - start_time).dt.total_seconds()

        # 对数据集分为四三态
        fan1_data = df[(df['time_diff'] >= 0) & (df['time_diff'] <= 49)]  # 保温
        fan2_data = df[(df['time_diff'] > 73) & (df['time_diff'] <= 319)]  # 制冷
        fan3_data = df[(df['time_diff'] > 335) & (df['time_diff'] <= 1086)]  # 辅热

        # 计算保温状态下，有功，无功，功率因数平均值, 标准差
        fan1_PC_mean = fan1_data['PC'].mean()
        fan1_PC_std = fan1_data['PC'].std()
        fan1_QC_mean = fan1_data['QC'].mean()
        fan1_QC_std = fan1_data['QC'].std()
        fan1_PFC_mean = fan1_data['PFC'].mean()
        fan1_PFC_std = fan1_data['PFC'].std()

        # # 计算制冷状态下，有功，无功，功率因数平均值, 标准差
        fan2_PC_mean = fan1_data['PC'].mean()
        fan2_PC_std = fan2_data['PC'].std()
        fan2_QC_mean = fan2_data['QC'].mean()
        fan2_QC_std = fan2_data['QC'].std()
        fan2_PFC_mean = fan2_data['PFC'].mean()
        fan2_PFC_std = fan2_data['PFC'].std()

        #
        # # 计算辅热下，有功，无功，功率因数平均值, 标准差
        fan3_PC_mean = fan3_data['PC'].mean()
        fan3_PC_std = fan3_data['PC'].std()
        fan3_QC_mean = fan3_data['QC'].mean()
        fan3_QC_std = fan3_data['QC'].std()
        fan3_PFC_mean = fan3_data['PFC'].mean()
        fan3_PFC_std = fan3_data['PFC'].std()


        print('YD9挂式空调')
        states = ['保温', '制冷', '辅热']
        current_values = [
            {'      PC平均值': fan1_PC_mean, '      QC平均值': fan1_QC_mean, '      PFC平均值': fan1_PFC_mean,
             '      PC标准差': fan1_PC_std, '      QC标准差': fan1_QC_std, '      PFC标准差': fan1_PFC_std},

            {"      PC平均值": fan2_PC_mean, "      QC平均值": fan2_QC_mean, "      PFC平均值": fan2_PFC_mean,
             "      PC标准差": fan2_PC_std, "      QC标准差": fan2_QC_std, "      PFC标准差": fan2_PFC_std},

            {"      PC平均值": fan3_PC_mean, "      QC平均值": fan3_QC_mean, "      PFC平均值": fan3_PFC_mean,
             "      PC标准差": fan3_PC_std, "      QC标准差": fan3_QC_std, "      PFC标准差": fan3_PFC_std},
            ]

        for state, values in zip(states, current_values):
            print(state)
            for key, value in values.items():
                print(f"{key}: {value}")
            print()



##-----------------------------------------计算未知设备1的有功无功功率因数均值，标准差----------------------------------------##
     def compute_unknow1(self, file_path): #计算未知设备1的有功无功功率因数均值，标准差
        df = pd.read_excel(file_path, sheet_name='设备数据')
        # plot_data(df, device_names[0])

        # 计算相对于起点的时间差
        start_time = pd.to_datetime(df['time']).min()
        df['time_diff'] = (pd.to_datetime(df['time']) - start_time).dt.total_seconds()

        # 对数据集分为四态
        fan1_data = df[(df['time_diff'] >= 58) & (df['time_diff'] <= 290)]  # 加热
        fan2_data = df[(df['time_diff'] > 367) & (df['time_diff'] <= 556)]  # 制冷
        fan3_data = df[(df['time_diff'] > 560) & (df['time_diff'] <= 893)]  # 加热制冷
        fan4_data = df[(df['time_diff'] > 1020) & (df['time_diff'] <= 1123)]  # 保温

        # 计算加热状态下，有功，无功，功率因数平均值, 标准差
        fan1_PC_mean = fan1_data['PC'].mean()
        fan1_PC_std = fan1_data['PC'].std()
        fan1_QC_mean = fan1_data['QC'].mean()
        fan1_QC_std = fan1_data['QC'].std()
        fan1_PFC_mean= fan1_data['PFC'].mean()
        fan1_PFC_std = fan1_data['PFC'].std()


        # # 计算制冷状态下，有功，无功，功率因数平均值, 标准差
        fan2_PC_mean = fan1_data['PC'].mean()
        fan2_PC_std = fan2_data['PC'].std()
        fan2_QC_mean = fan2_data['QC'].mean()
        fan2_QC_std = fan2_data['QC'].std()
        fan2_PFC_mean = fan2_data['PFC'].mean()
        fan2_PFC_std = fan2_data['PFC'].std()

        #
        # # 计算加热+制冷下，有功，无功，功率因数平均值, 标准差
        fan3_PC_mean = fan3_data['PC'].mean()
        fan3_PC_std = fan3_data['PC'].std()
        fan3_QC_mean = fan3_data['QC'].mean()
        fan3_QC_std = fan3_data['QC'].std()
        fan3_PFC_mean = fan3_data['PFC'].mean()
        fan3_PFC_std = fan3_data['PFC'].std()

        #
        # # 计算保温下，有功，无功，功率因数平均值, 标准差
        fan4_PC_mean = fan4_data['PC'].mean()
        fan4_PC_std = fan4_data['PC'].std()
        fan4_QC_mean = fan4_data['QC'].mean()
        fan4_QC_std = fan4_data['QC'].std()
        fan4_PFC_mean = fan4_data['PFC'].mean()
        fan4_PFC_std = fan4_data['PFC'].std()


        print('未知设备1')
        states = ['state1', 'state2', 'state3', 'state4']
        current_values = [
            {'      PC平均值': fan1_PC_mean, '      QC平均值': fan1_QC_mean, '      PFC平均值': fan1_PFC_mean,
             '      PC标准差': fan1_PC_std,  '      QC标准差': fan1_QC_std,  '      PFC标准差': fan1_PFC_std},

            {"      PC平均值": fan2_PC_mean, "      QC平均值": fan2_QC_mean, "      PFC平均值": fan2_PFC_mean,
             "      PC标准差": fan2_PC_std,  "      QC标准差": fan2_QC_std,  "      PFC标准差": fan2_PFC_std},

            {"      PC平均值": fan3_PC_mean, "      QC平均值": fan3_QC_mean, "      PFC平均值": fan3_PFC_mean,
             "      PC标准差": fan3_PC_std,  "      QC标准差": fan3_QC_std,  "      PFC标准差": fan3_PFC_std},

            {"      PC平均值": fan4_PC_mean, "      QC平均值": fan4_QC_mean, "      PFC平均值": fan4_PFC_mean,
             "      PC标准差": fan4_PC_std , "      QC标准差": fan4_QC_std,  "      PFC标准差": fan4_PFC_std}
        ]

        for state, values in zip(states, current_values):
            print(state)
            for key, value in values.items():
                print(f"{key}: {value}")
            print()



     def compute_unknow2(self, file_path):  #计算未知设备2的有功无功功率因数均值，标准差
        df = pd.read_excel(file_path, sheet_name='设备数据')
        # plot_data(df, device_names[0])

        # 计算相对于起点的时间差
        start_time = pd.to_datetime(df['time']).min()
        df['time_diff'] = (pd.to_datetime(df['time']) - start_time).dt.total_seconds()

        # 对数据集分为四三态
        fan1_data = df[(df['time_diff'] >= 0) & (df['time_diff'] <= 49)]  # 保温
        fan2_data = df[(df['time_diff'] > 73) & (df['time_diff'] <= 319)]  # 制冷
        fan3_data = df[(df['time_diff'] > 335) & (df['time_diff'] <= 1086)]  # 辅热

        # 计算保温状态下，有功，无功，功率因数平均值, 标准差
        fan1_PC_mean = fan1_data['PC'].mean()
        fan1_PC_std = fan1_data['PC'].std()
        fan1_QC_mean = fan1_data['QC'].mean()
        fan1_QC_std = fan1_data['QC'].std()
        fan1_PFC_mean = fan1_data['PFC'].mean()
        fan1_PFC_std = fan1_data['PFC'].std()

        # # 计算制冷状态下，有功，无功，功率因数平均值, 标准差
        fan2_PC_mean = fan1_data['PC'].mean()
        fan2_PC_std = fan2_data['PC'].std()
        fan2_QC_mean = fan2_data['QC'].mean()
        fan2_QC_std = fan2_data['QC'].std()
        fan2_PFC_mean = fan2_data['PFC'].mean()
        fan2_PFC_std = fan2_data['PFC'].std()

        #
        # # 计算辅热下，有功，无功，功率因数平均值, 标准差
        fan3_PC_mean = fan3_data['PC'].mean()
        fan3_PC_std = fan3_data['PC'].std()
        fan3_QC_mean = fan3_data['QC'].mean()
        fan3_QC_std = fan3_data['QC'].std()
        fan3_PFC_mean = fan3_data['PFC'].mean()
        fan3_PFC_std = fan3_data['PFC'].std()


        print('未知设备2')
        states = ['state1', 'state2', 'state3']
        current_values = [
            {'      PC平均值': fan1_PC_mean, '      QC平均值': fan1_QC_mean, '      PFC平均值': fan1_PFC_mean,
             '      PC标准差': fan1_PC_std, '      QC标准差': fan1_QC_std, '      PFC标准差': fan1_PFC_std},

            {"      PC平均值": fan2_PC_mean, "      QC平均值": fan2_QC_mean, "      PFC平均值": fan2_PFC_mean,
             "      PC标准差": fan2_PC_std, "      QC标准差": fan2_QC_std, "      PFC标准差": fan2_PFC_std},

            {"      PC平均值": fan3_PC_mean, "      QC平均值": fan3_QC_mean, "      PFC平均值": fan3_PFC_mean,
             "      PC标准差": fan3_PC_std, "      QC标准差": fan3_QC_std, "      PFC标准差": fan3_PFC_std},
            ]

        for state, values in zip(states, current_values):
            print(state)
            for key, value in values.items():
                print(f"{key}: {value}")
            print()













##-----------------------------------------计算每台设备的实时用电量(每秒用电量)----------------------------------------------------##
##----------------------------------------计算公式：W=U*I*1/3600---------------------------------------------------##
def Computing_RT_Power():

    def real_time_power(file_path):
        df = pd.read_excel(file_path, sheet_name='设备数据')

        #计算一秒内实时用电量，单位W
        df["RealTimePower"] = ((df["UC"] / 10) * (df["IC"])/1000 * 1) / 3600
        return df["RealTimePower"]

    results = []

    for path in file_paths:
        # try:
        power_values = real_time_power(path)
        results.append(power_values)
        # except Exception as e:
        #     print(f"Error processing file {path}: {str(e)}")


    y = 1
    for i, path in enumerate(file_paths):
        print(f"Results for file YD{y}", "单位W")
        y = y + 1
        print(results[i])
        print()
        #pd.set_option('display.max_rows', None) #此句用于将过长的输出不省略


    # for i, path in enumerate(file_paths):
    #     print(f"Results for file {path}:")
    #     for value in results[i]:
    #         print(f"{value:.6f} w")
    #     print()