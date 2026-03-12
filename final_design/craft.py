import sensor, image, time
# import lcd
from pyb import UART
import struct

EXPOSURE_TIME_SCALE = 0.6
uart = UART(3, 115200)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(True)
sensor.set_hmirror(True)
sensor.skip_frames(time=2000)
red_thresholds = [(78, 100, -10, 43, -18, 21)]
clock = time.clock()

roi1 = [156, 114, 10, 11]  # 此感兴趣的区域用于识别激光点

# 由于舵机精度不高，所以以下角度并没有太大用处，仅用于确定当舵机在中央，P1P2P3P4时，检测矩形时感兴趣区域，第二个为第二个舵机
rois = {"RoiRect_Center": [28, 25, 274, 199], # 舵机的初始角度都为(99,93),(90,90)
        "RoiRect_LowRight": [148, 100, 158, 125],  # 上下舵机给定角度为(96,103)()
        "RoiRect_LowLeft": [16, 101, 167, 133],  # 上下舵机给定角度为(96,89.5)()
        "RoiRect_UpLeft": [7, 5, 173, 134],  # 上下舵机给定角度为(105,89.5)()
        "RoiRect_UpRight": [144, 6, 165, 128]}  # 上下舵机给定角度为(105.5,103)()

roi_rect = [36, 27, 267, 195]  # 此感兴趣的区域用于识别矩形
#这里为通过laser_dot()这个函数得到的激光点的坐标，所以基本不太变化了，仅使用laser_dot()函数一次即可
x_laser = 169
y_laser = 118


def find_max(blobs):
    max_size = 0
    max_blob = None
    for blob in blobs:
        if blob[2] * blob[3] > max_size:
            max_blob = blob
            max_size = blob[2] * blob[3]
    return max_blob

def laser_dot():
    img = sensor.snapshot().lens_corr(strength=1.0)
#    img.draw_rectangle(roi1[0], roi1[1], roi1[2], roi1[3], color=[0, 0, 0])  # 画激光笔的感兴趣区域
    img.binary([(0, 35)], invert=True)  # 将图像转换为二值图像，黑色为矩形
    red_blobs = img.find_blobs(red_thresholds, roi=roi1, area_threshold=1, pixels_threshold=1)  # 返回检测红色激光点
    if red_blobs:  # 返回检测红色激光点
        max_red_blob = find_max(red_blobs)
        x = struct.pack('i', max_red_blob.cx())
        y = struct.pack('i', max_red_blob.cy())
        z = x + y + '*#'
        img.draw_cross(max_red_blob.cx(), max_red_blob.cy(), color=[0, 255, 0])  # 对检测到的红色激光点标记
        x_coord, y_coord = struct.unpack('ii', z[:8])  # 解包前8个字节为x坐标和y坐标
        uart.write(z)  # 回传红色激光点的坐标
        print('激光点坐标：', x_coord, y_coord)
        return x_coord, y_coord
    img.draw_cross(max_red_blob.cx(), max_red_blob.cy(), color=[0, 255, 0])  # 对检测到的红色激光点标记

def find_rect():
    a = 1
    while a:
        img = sensor.snapshot().lens_corr(strength=1.0)
#        img.histeq() # 增加对比度
        img.binary([(0, 35)], invert=True) # 将图像转换为二值图像，黑色为矩形
        # 尝试减少腐蚀和膨胀的强度
        img.erode(0) # 腐蚀操作
        img.dilate(1) # 膨胀操作
        # 使用gamma函数调整图像的亮度
#        img.gamma(1) # 增加亮度，可以间接地增加对比度

        img.draw_rectangle(rois["RoiRect_Center"], color=[0, 0, 255])#当摄像头运动时，画出兴趣区域，=====================
        img.draw_rectangle(rois["RoiRect_Center"], color=[0, 0, 255]) # 画框==================================
        for r in img.find_rects(rois["RoiRect_Center"], threshold=10000):#找矩形感兴趣====================================
            z = bytes()  # 用于厨房要回传的数据
            img.draw_rectangle(r.rect(), color=(255, 77, 100))  # 在图片中画出识别到的矩形
            for i, p in enumerate(r.corners()):  # 遍历矩形的每个角点
                img.draw_circle(p[0], p[1], 5, color=(0, 255, 0))  # 对于每个角画圆
                x = struct.pack('i', p[0])
                y = struct.pack('i', p[1])
                print('矩形', i + 1, '的角点坐标：', p[0], p[1])  # 输出角点坐标
                z += x + y  # 将角点坐标添加到输出中
            z += b'*#'  # 添加结束标记
            uart.write(z)
            print('回传数据包：', z)
        a = 0  # 结束循环
        img.draw_rectangle(rois["RoiRect_Center"], color=[0, 0, 255]) # 画框===================================
        print('------------------------------')
        #以下用于在二值化图像中画激光点十字
        red_blobs = img.find_blobs(red_thresholds, roi=roi1 ,area_threshold = 1, pixels_threshold = 1)#返回检测红色激光点
        if red_blobs:#返回检测红色激光点
            max_red_blob = find_max(red_blobs)
            img.draw_cross(max_red_blob.cx(), max_red_blob.cy(), color=[0,255,0])#对检测到的红色激光点标记
            img.draw_cross(max_red_blob.cx(), max_red_blob.cy(), color=[0,255,0])#对检测到的红色激光点标记

time.sleep(2)  # 延迟,用于固定场景
while (True):
    clock.tick()
    # openMV与激光笔相对固定，绿色激光点在固定位置
    laser_dot()
    find_rect()
#    time.sleep(0.1)
