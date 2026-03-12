#此程序来源于ChatGPT,用于理解fft原理
import numpy as np
import matplotlib.pyplot as plt

# 设置采样率和采样点数
sampling_rate = 1000  # 采样率Hz,表示每秒钟的采样点数量
num_samples = 1000    #采样点数，在整个信号持续时间内采样的总次数

# 生成一个正弦波信号
time = np.arange(num_samples) / sampling_rate
frequency = 10  # Hz
signal = np.sin(2 * np.pi * frequency * time)

# 进行FFT变换
freqs = np.arange(num_samples) * (sampling_rate / num_samples)
fft_vals = np.fft.fft(signal)

# 绘制频率谱
plt.plot(freqs, np.abs(fft_vals))
plt.title('Frequency Spectrum')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.show()
