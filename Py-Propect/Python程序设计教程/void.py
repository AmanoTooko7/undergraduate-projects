from cImage import *
def grayPixel(oldPixel):
    intensitySum = oldPixel.getRed()+oldPixel.getGreen()+\
    oldPixel.getBlue()
    aveRGB = intensitySum//3
    newPixel = Pixel(aveRGB, aveRGB, aveRGB)
    return newPixel

grayPixel(Pixel(10, 12, 7))
