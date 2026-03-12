#此FFT算法来自3Blue1Bown
#这里输入的P为多项式系数列表
#与from numpy.fft import fft, ifft自带库中的fft验证，本文件所写程序是不太正确
#这里输入的数组必须是偶数个元素

#import pdb#此行用于导入调试库
#pdb.set_trace()此句相当于断点

import cmath
def FFT(P): 
    n = len(P)
    #print(n)
    if n == 1:
        return P
    omiga = cmath.exp(2 * cmath.pi * 1j / n)
    Pe, Po = P[::2], P[1::2]#Pe为偶数位置元素，Po为奇数位的元素
    ye, yo = FFT(Pe), FFT(Po)
    #print(n)
    y = [0] * n  #y列表中有n个元素且全为0
    for j in range(n // 2):
        y[j] = ye[j] + (omiga ** j) * yo[j]
        y[j + n // 2] = ye[j] - (omiga ** j) * yo[j]
    return y

p=FFT([3,2,2,1])
print(p)
#此程序表示输入的数组m=[3,2,2,1]表示一个多项式3+2x+2x^2+x^3
#在x=1,i,-1,-i时的值，也就是[(8+0j), (1+1j), (2+0j), (0.9999999999999999-1j)]
#取值如： e^2𝜋𝑖𝑘/𝑛 for k = 0, 1, … ,𝑛 − 1，见网站https://medium.com/@aiswaryamathur/understanding-fast-fourier-transform-from-scratch-to-solve-polynomial-multiplication-8018d511162f
#此程序也就将m次多项式表示成m+1个点样式，

