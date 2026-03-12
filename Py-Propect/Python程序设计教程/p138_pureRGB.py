#以下用于实现RGB分别为255时所显示颜色的窗口
from cImage import *
import time #用于延时
pixelR = Pixel(255, 0, 0)
pixelG = Pixel(0, 255, 0)
PixelB = Pixel(0, 0, 255)
myWindow = ImageWin("Empty", 900, 300)

for row in 300:
    for col in 300:
        myWindow.setPixel(col, row, PixelR)
        time.sleep(0.001)
        myWindow.setPixel(col, row + 300, PixelG)
        time.sleep(0.001)
        myWindow.setPixel(col, row + 600, PixelB)





    
