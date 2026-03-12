import sensor, image, time
#import lcd
from pyb import UART
import struct

EXPOSURE_TIME_SCALE = 0.6
uart = UART(3, 115200)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(True)
sensor.set_hmirror(True)
sensor.skip_frames(time = 2000)
red_thresholds = [(78, 100, -10, 43, -18, 21)]
clock = time.clock()

#def find_min(blobs):
#    min_size = 160*160
#    min_blob = None
#    for blob in blobs:
#        if blob[2]*blob[3] < min_size:
#            min_blob = blob
#            min_size = blob[2]*blob[3]
#    return min_blob

def find_max(blobs):
    max_size = 0
    max_blob = None
    for blob in blobs:
        if blob[2]*blob[3] > max_size:
            max_blob = blob
            max_size = blob[2]*blob[3]
    return max_blob

#def reduce_exposure():
#    print("Initial exposure == %d" % sensor.get_exposure_us())
#    sensor.set_auto_gain(False)
#    sensor.set_auto_whitebal(False)
#    sensor.skip_frames(time=500)
#    current_exposure_time_in_microseconds = sensor.get_exposure_us()
#    sensor.set_auto_exposure(False, exposure_us=int(
#        current_exposure_time_in_microseconds * EXPOSURE_TIME_SCALE))
#    sensor.set_auto_exposure(False)
#    print("New exposure == %d" % sensor.get_exposure_us())

while(True):
    clock.tick()
    img = sensor.snapshot().lens_corr(strength = 1.0)
    if uart.any():#如果接收到了来自串口返回的数据
        char = uart.readchar()#接收来自主控的数据char
        if char == 0x30 + 1 :#如果接收到数据为1，则返回红色激光点中心坐标
            print('11111111')
            red_blobs = img.find_blobs(red_thresholds, area_threshold = 1, pixels_threshold = 1)#返回检测红色激光点
            if red_blobs:#返回检测红色激光点
                max_red_blob = find_max(red_blobs)
                img.draw_cross(min_red_blob.cx(), max_red_blob.cy(), color=[0,255,0])#对检测到的红色激光点标记
                x = struct.pack('i', max_red_blob.cx())
                y = struct.pack('i', max_red_blob.cy())
                z = x + y + '*#'
                uart.write(z)#回传红色激光点的坐标
#---------------------------------以下发送矩形坐标---------------------------------------------------------
        elif char == 0x30 + 2:#如果串口收到数据2
            print('22222222')
            a = 1
            while(a):
                img = sensor.snapshot().lens_corr(strength = 1.0)
                for r in img.find_rects(threshold = 10000):#识别矩形，返回一个矩形对象
                    z = bytes()#用于厨房要回传的数据
                    img.draw_rectangle(r.rect(), color = (255, 0, 0))#在图片中画出识别到的矩形，
                    for p in r.corners():#这里的p表示矩形的一个角的点坐标
                        img.draw_circle(p[0], p[1], 5, color = (0, 255, 0))#对于每个角画圆
                        x = struct.pack('i', p[0])
                        y = struct.pack('i', p[1])
                        print(p[0],p[1])
                        z = z + x + y
                    a = a - 1
                    z = z + '*#'
                    uart.write(z)
