#图像负片
from cImage import *
def negativePixel(oldPixel):#用于生成一个negative pixel
    newRed = 255 - oldPixel.getRed()
    newBlue = 255 - oldPixel.getBlue()
    newGreen = 255 - oldPixel.getGreen()
    newPixel = Pixel(newRed, newGreen, newBlue)
    return newPixel

#aPixel = Pixel(0,5,255)
#Np=negativePixel(aPixel)
#print(Np)
def makeNegative(imageFile):
    oldImage = FileImage(imageFile)#创建一个图形对象
    width = oldImage.getWidth()
    height = oldImage.getHeight()

    myImageWindow = ImageWin(width*2, height, "Negative Image")
    #先创建一个图像对象,ImageWin()函数对象为一个具体图像和空图像有区别
    oldImage.draw(myImageWindow) #再绘画此对象
    newIm = EmptyImage(width, height)

    #以下for循环作用是设置在新图像(newIm)里创建负片的像素
    for row in range(height):
        for col in range(width):
            oldPixel = oldImage.getPixel(col, row)
            newPixel = negativePixel(oldPixel)
            newIm.setPixel(col, row, newPixel)

    newIm.setPosition(width + 1, 0)
    newIm.draw(myImageWindow)
    myImageWindow.exitOnClick()


#if __name__ == '__main__':

makeNegative(r"C:\Users\hp\Desktop\senpaii.gif")
    #双引号里可写任意地址
print(__name__)
