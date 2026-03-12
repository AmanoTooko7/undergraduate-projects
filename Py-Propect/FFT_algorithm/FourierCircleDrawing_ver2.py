#此程序来源于GPT，目的用于实现用傅里叶画人物图，为版本二

import urllib.request
from PIL import Image
from io import BytesIO
import numpy as np
from scipy.fftpack import fft,ifft
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 1. 读取图片
url = "C:\\Users\\hp\\Desktop\\project\Py-Propect\\FFT_algorithm\\materials\\ele.png"
with urllib.request.urlopen(url) as url:
    img_data = url.read()
img = Image.open(BytesIO(img_data)).convert('L')
img_arr = np.array(img)

# 2. 获取图像上的点
coords = np.column_stack(np.where(img_arr < 255))

# 3. 将点按照距离远近排序，并只取其中一部分
center = np.mean(coords, axis=0)
dists = np.sqrt(((coords - center)**2).sum(axis=1))
inds = dists.argsort()
coords = coords[inds]
coords = coords[::5]

# 4. 将坐标系原点移到中心位置
coords = coords - center

# 5. 进行傅里叶变换，得到复数序列
def compute(z, m):
    n = len(z)
    cn = np.zeros(2 * m + 1, dtype=np.complex128)
    for j in range(-m, m + 1):
        cn[j + m] = np.sum(z * np.exp(-2j * np.pi * j / n * np.arange(n)))
    return cn

def toPt(z):
    return np.array([np.real(z), np.imag(z)])

z = coords[:, 0] + 1j * coords[:, 1]
m = 300
cn = compute(z, m)
r = np.abs(cn)
theta = np.angle(cn)
index = np.concatenate(([m + 1], np.arange(m + 2, 2 * m + 2)[::-1], np.arange(1, m + 1)))
tab = np.array([toPt(cn[j] * np.exp(1j * (j - m - 1) * np.linspace(0, 2 * np.pi, 500))) for j in index])
p = np.cumsum(tab, axis=0)

# 6. 绘制动画
circles = [plt.Circle((p[0, j, 0], p[0, j, 1]), r[index[j]]) for j in range(2 * m + 1)]

fig, ax = plt.subplots(figsize=(5, 5))
for circle in circles:
    ax.add_patch(circle)
line, = ax.plot([], [], lw=2)
ax.set_xlim([-200, 100])
ax.set_ylim([-200, 200])
ax.set_aspect('equal')

def init():
    line.set_data([], [])
    return line,

def update(frame):
    line.set_data(p[frame, :, 0], p[frame, :, 1])
    for j in range(2 * m + 1):
        circles[j].center = (p[frame, j, 0], p[frame, j, 1])
    return line, circles

anim = FuncAnimation(fig, update, frames=len(p), init_func=init, blit=True)
anim.save('bart.gif', writer='imagemagick')
plt.show()


