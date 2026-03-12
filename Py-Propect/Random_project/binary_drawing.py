##import struct
##import matplotlib.pyplot as plt
##
##with open("C:\\Users\\hp\\Desktop\\data.bin","rb") as f:
##    # 读取二进制数据
##    data = f.read()
##
### 解析格式为AA55 + 2个字节采样数据
##values = []
##for i in range(0, len(data), 4):
##    header = data[i:i+2]
##    sample = data[i+2:i+4]
##    if header == b'\xAA\x55':
##        value = struct.unpack('h', sample)[0]
##        values.append(value)
##
### 绘制图形
##sample_rate = 2e3 # 采样频率为1.59K
##time = [i/sample_rate for i in range(len(values))]
##plt.plot(time, values)
##plt.xlabel('Time (s)')
##plt.ylabel('Amplitude')
##plt.title('Signal Plot')
##plt.show()


import numpy as np
import matplotlib.pyplot as plt

# 读取二进制数据
data = np.fromfile("C:\\Users\\hp\\Desktop\\Py-Propect\\binary-data.bin", dtype=np.uint8)
#dtype=np.uint8为读取文件时使用的数据类型为无符号8位整数0-255。

# 解析格式为AA55 + 2个字节采样数据？？？
header = np.where(data == 0xAA)[0]
values = []
for i in header:
    if data[i+1] == 0x55:
        value = (data[i+2] << 8) + data[i+3]
        values.append(value)
values = np.array(values, dtype=np.int16)

# 绘制图形
sample_rate = 1.59e3 # 采样频率为1.59K
time = np.arange(len(values)) / sample_rate
plt.plot(time, values)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Signal Plot')
plt.show()
