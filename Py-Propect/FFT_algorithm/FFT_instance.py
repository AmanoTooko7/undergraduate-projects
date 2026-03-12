#FFT例程，来源https://pythonnumericalmethods.berkeley.edu/notebooks/chapter24.04-FFT-in-Python.html

#此程序用于生成一个信号利用fft,得到频率曲线，利用ifft由频率曲线还原信号
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn-poster')
#%matplotlib inline
# sampling rate
sr = 20000     #此变量表示采样率(也就是每秒采样次数)
# sampling interval
ts = 1.0/sr   #表示采样间隔时间

#生成时间点序列，由0开始到1(不包括1)结束，步长为采样间隔时间
#t的输出为从0到1，以1/2000的间隔生成一个等差的数组
t = np.arange(0,1,ts)
#一下4个频率分别为1,4,7,10的不同幅值的正弦信号相加得到最终信号
freq = 1.
x = 3*np.sin(2*np.pi*freq*t)
freq = 4
x += np.sin(2*np.pi*freq*t)
freq = 7   
x += 0.5* np.sin(2*np.pi*freq*t)
freq = 20   
x += 5* np.sin(2*np.pi*freq*t)
#这里的x表示不同t值下最终信号的求值，为一个数组

plt.figure(figsize = (8, 7))#此行用于创建一个新图像，宽为8，长为6英寸
plt.plot(t, x, 'b')
plt.ylabel('Amplitude')

##----------------以上程序用于生成一个信号------------##
##----------以下程序用于输出信号x(t)频谱图,并利用ifft复原信号--------##
from numpy.fft import fft, ifft

X = fft(x)#表示给定信号经过fft的结果，为一个数组
N = len(X)#表示频率数据点的个数
n = np.arange(N)#频率数据点的编号，为数组 #T = N/sr#表示频率采样周期，为一个数
freq = n*sr/N#代表频率点的实际频率
print("采样数据长度(N): {}\n对采样数据编号(n): {}\n 每个点对应频率(freq): {}".format(N, n, freq))

plt.figure(figsize = (7, 4))#创建一个图形，并设置大小为12x6英寸
plt.subplot(121)
print(np.abs(X))
plt.stem(freq, np.abs(X), 'b', markerfmt=" ", basefmt="-b")
#这里以freq为横坐标，np.abs(X)，也就是fft后结果的幅值为纵坐标
plt.xlabel('Freq (Hz)')
plt.ylabel('FFT Amplitude |X(freq)|')
plt.xlim(0, 22)
##-------------一二子图程序分界线-------------------##
##-------------二子图为从频域还原信号图--------------##
plt.subplot(122)
plt.plot(t, ifft(X), 'r')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.tight_layout()
plt.show()
##-----------------------##

#要得一组信号signal(长度为N)到经过fft变换后,
#所得到的一个数组values(长度也为N)每个元素的频率计算方法如下
#设values中第K个元素频率为f_k， f_k=(元素索引)*采样频率/N
#这个"元素索引"在Pyhon中一般由numy模块中np.arange(N)生成长度为N的从0到N-1的向量
#经过X = fft(x)变换后，X中每一个元素对应时域中每一个采样的点，X中每个元素为复数，
#------------------这里的每个复数元素不一定是相同的，从多项式下理解fft，因为在单位复数圆中每个取值是不同，
#将各个元素取模则得到频域下不同频率的幅值,这里的幅值由第19-29排程序np.sin前的值决定，




