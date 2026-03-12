#此程序用于在一个实际在图书馆录音文件使用fft，作出时域和频域图像
#并尝试分离奇次谐波和偶次谐波
import wave
import numpy as np
import matplotlib.pyplot as plt

sample1 = "C:\\Users\\hp\\Desktop\\project\\Py-Propect\\FFT_algorithm\\materials\\Sample_1_ForFft.wav"
sample2 = "C:\\Users\\hp\\Desktop\\project\\Py-Propect\\FFT_algorithm\\materials\\Sample_2_ForFft.wav"

#sample2:mp3格式转为wav格式，在网站中所选的采样率为48000
with wave.open(sample2, 'rb') as wavfile:
    framerate = wavfile.getframerate()
    #上行获得wav的采样率,储存在framerate中，也就是样本点数每秒
    #print(framerate)#采样率为44100

    frames = wavfile.readframes(-1)
    #此行读取WAV文件的所有帧并将其存储在名为frames的变量中。-1表示读取所有帧
    #帧表示一个很小的时间段一般是10到20毫秒

    signal = np.frombuffer(frames, dtype='int16')
    #此行将帧转换为NumPy数组。'int16'是数据类型，它表示采样的值以16位有符号整数的形式存储。
    #存储格式为立体声，即每个采样点占用两个字节。
    #print(len(signal))#长度为1221888

    fft = np.fft.fft(signal)
    #frequencies = np.fft.fftfreq(len(signal)) * framerate#计算频率值，为复数
    frequencies = np.arange(len(signal)) * framerate / len(signal)#计算频率值，为实数
    #不管是提取复数的频率值还是提取实数的频率值长度都为1221888
    #这里不同的计算频率的方法不同所画出的频率——幅值不同，
    #实际问题中一般是用第二种方式计算
    
    #print(len(frequencies))##长度为1221888，为一个数组
    spectrum = np.abs(fft)#为不同频率下的幅值

    time = np.linspace(0, len(signal) / framerate, num=len(signal))
    #起始点0，终止值len(signal)，生成样本数为len(signal)个的等差数列
    plt.figure(1)
    plt.plot(time, signal)#时域图
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.plot(time, signal)
    plt.title('Time domain')

    plt.figure(2)                 
    plt.plot(frequencies, spectrum)#频域图
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.title('Fequency domain')
    plt.xlim(0, 1800)

    max_index = np.argmax(spectrum)
    #返回fft后结果中幅值最大的那个频率索引值，保存在max_index,一般情况下基本比谐波大
    fundamental_frequency = frequencies[max_index]
    #返回保存为幅值最大对应下的频率值，也就是返回基波
    #输出基波频率与幅值
    
    plt.axvline(fundamental_frequency, color='r', linestyle='--')
    #上一行在图中标注基波所在位子
    plt.show()

##----------------以下为分离基波,奇次谐波和偶次谐波---------------------##

    print("Fundamental frequency: {} Hz, Amplitude: {}".format(fundamental_frequency, spectrum[max_index]))
    #结果为Fundamental frequency: 123.10874646448774 Hz, Amplitude: 16637463.664885579

    #奇次谐波是基波频率的奇数倍，偶次谐波同理，这里提取奇偶次谐波为整数
    mulpiple_frequency = frequencies/fundamental_frequency#基波的倍数，为numpy数组

    even_mask = np.where(mulpiple_frequency  % 2 == 0)
    #找到mulpiple_frequency中(基频倍数)为偶数的元素的索引返回给even_mask
    even_harmonics = np.trunc( frequencies[even_mask] )#trunc为对数组向下取整

    odd_mask = np.where(mulpiple_frequency % 2 == 1)
    odd_harmonics = np.trunc( frequencies[odd_mask] )

    print("even har：\n", even_harmonics,"\n", "odd har:\n", odd_harmonics)










    
