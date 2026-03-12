import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# 读取图像，转化为灰度图像并二值化
img1 = Image.open('C:\\Users\\hp\\Desktop\\project\Py-Propect\\FFT_algorithm\\materials\\ele.png')
img2 = img1.convert('L')#img2为转化后的灰度图像
img3 = np.array(img2.resize((500, 500))) / 255
img = np.where(img3 > 0.5, 1, 0)

# 绘制等高线并找到等高线上的点
contours = plt.contour(np.flipud(img), levels=[0.5])
pts = np.concatenate([contours.collections[0].get_paths()[0].vertices])

# 找到图像中心点
center = np.mean(pts, axis=0)

# 平移点集，使中心点处于原点
pts -= center

# 绘制点集图形
plt.plot(pts[:,0], pts[:,1], 'o')

# 显示图像
plt.show()
