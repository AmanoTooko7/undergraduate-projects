#此程序来源于ChatGPT
#此程序用于将一个信号(bin文件)，经过fft变换后
#解析为不同频率的正弦信号，并分出奇次谐波和偶次谐波

#经过下面已经被注释的程序来看，此bin文件为int8类型，并且不为周期信号

import numpy as np
import matplotlib.pyplot as plt

##-------以下程序判断出来binary-data.bin数据类型为int8----------##
### 打开二进制文件
##with open('C:\\Users\\hp\\Desktop\\Py-Propect\\binary-data.bin', 'rb') as file:
##    # 读取前 10000 个字节
##    data = file.read(10000)
##
### 尝试将数据类型指定为不同类型，查看转换后的数组是否有意义
##for dtype in [np.int8, np.uint8, np.int16, np.uint16, np.int32, np.uint32, np.float32, np.float64]:
##    try:
##        arr = np.frombuffer(data, dtype=dtype)
##        print(f"Data type {dtype} works!")
##        break
##    except:
##        print(f"Data type {dtype} doesn't work!")
### 打印数据前 10 个元素
##print("Data:", arr[:10])
##-------------------------------------------------------------##

# 打开二进制文件
with open('C:\\Users\hp\\Desktop\\project\\Py-Propect\\FFT_algorithm\\materials\\binary-data.bin', 'rb') as file:
    # 读取二进制数据并转换为 NumPy 数组
    signal = np.fromfile(file, dtype=np.int8)


### 计算数据的差分
##diffs = np.diff(signal)
##
### 计算数据差分的均值和标准差
##mean_diff = np.mean(diffs)
##std_diff = np.std(diffs)
##
### 判断数据是否具有稳定的周期性
##if std_diff < 0.01 * mean_diff:
##    print('Data is periodic')
##else:
##    print('Data is not periodic')
##---------------通过以上程序判定出此数据不是周期的--------------##



fft_signal = np.fft.fft(signal)
freqs = np.fft.fftfreq(len(signal))
#上行提取signal的频率值

#b=np.where(a),当满足条件a时，也就是为非0时,返回一个元组，有两个元素
#b的第一个元素为满足条件a的a的元素的下标，b的第二个元素为a的元素类型

even_mask = np.where(freqs % 2 == 0)
#找到freqs中为偶数的元素的索引返回给even_mask
even_harmonics = fft_signal[even_mask]
#返回偶数频率下fft_signal中的幅值

odd_mask = np.where(freqs % 2 == 1)
odd_harmonics = fft_signal[odd_mask]
