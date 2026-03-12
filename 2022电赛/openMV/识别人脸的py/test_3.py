# Untitled - By: 29595 - 周日 7月 3 2022

import sensor, image, time, os, lcd, pyb, struct, tf
from pyb import LED
from pyb import UART

FILE_NAME = "/keypoints"

def find_mask():
    global face_cascade

    sensor.reset()                         # Reset and initialize the sensor.
    sensor.set_pixformat(sensor.RGB565)    # Set pixel format to RGB565 (or GRAYSCALE)
    sensor.set_framesize(sensor.QVGA)      # Set frame size to QVGA (320x240)
    sensor.set_windowing((240, 240))       # Set 240x240 window.
    sensor.skip_frames(time=2000)          # Let the camera adjust.

    net = "trained.tflite"
    labels = [line.rstrip('\n') for line in open("labels.txt")]
    red.off()
    #clock = time.clock()
    num = 1

    mask_value = 0.0
    while(num):
        # 拍摄图片并返回img
        img = sensor.snapshot()

        #img.draw_string(0, 0, "Looking for a face...")

        objects = img.find_features(face_cascade, threshold=0.5, scale_factor=1.25)
        if objects:

        #clock.tick()

        #img = sensor.snapshot()

        # default settings just do one detection... change them to search the image...
            for obj in tf.classify(net, img, min_scale=1.0, scale_mul=0.8, x_overlap=0.5, y_overlap=0.5):
                #print("**********\nPredictions at [x=%d,y=%d,w=%d,h=%d]" % obj.rect())
                img.draw_rectangle(obj.rect())
                # This combines the labels and confidence values into a list of tuples
                predictions_list = list(zip(labels, obj.output()))

                #for i in range(len(predictions_list)):
                    #uart.write(str("%s = %f" % (predictions_list[i][0], predictions_list[i][1])))
                mask_value += predictions_list[1][1]
            num -= 1

        else :
            pass
        #print(clock.fps(), "fps")
    if mask_value > 0.93 :
        uart.write(str(("%f\n") % (mask_value)))
        uart.write(str("mask\n"))
        green.on()
    else :
        uart.write(str(("%f\n") % (1-mask_value)))
        uart.write(str("face\r\n"))
        blue.on()

    # 初始化摄像头
    sensor.reset()

    # 设置相机图像的对比度为1
    sensor.set_contrast(1)

    # 设置相机的增益上限为16
    sensor.set_gainceiling(16)

    # 设置采集到照片的大小
    #sensor.set_framesize(sensor.QVGA)

    # 在VGA(640*480)下开个小窗口，相当于数码缩放
    sensor.set_windowing((320, 240))

    # 设置采集到照片的格式：灰色图像
    sensor.set_pixformat(sensor.GRAYSCALE)
    green.off()
    blue.off()

#****************************************************************************

def find_face():
    red.on()
    global face_cascade
    global FILE_NAME
    # 初始化摄像头
    #sensor.reset()

    # 设置相机图像的对比度为3
    #sensor.set_contrast(3)

    # 设置相机的增益上限为16
    #sensor.set_gainceiling(16)

    # 设置采集到照片的大小
    #sensor.set_framesize(sensor.QVGA)

    # 在VGA(640*480)下开个小窗口，相当于数码缩放
    #sensor.set_windowing((320, 240))

    # 设置采集到照片的格式：灰色图像
    #sensor.set_pixformat(sensor.GRAYSCALE)

    #sensor.skip_frames(time = 10000)     # Wait for settings take effect.


    loop_flag=1#循环检测标志位，检测到人脸身边识别后退出
    #type_flag=0#kpts1类别正确标志位，正确为1，错误为0
    dir_lists = os.listdir(FILE_NAME)  # 路径下文件夹
    dir_num = len(dir_lists)
    match_num = 0

    while(loop_flag):
        max_match = [] #保存检测点和样本点的匹配程度，越大越接近，初始化为最小
        img = sensor.snapshot()
        objects = img.find_features(face_cascade, threshold=0.7, scale_factor=1.25)
        if objects:
            face = (objects[0][0]-15,
                    objects[0][1]-15,
                    objects[0][2]+15*2,
                    objects[0][3]+15*2)
            kpts1 = img.find_keypoints(roi = face,
                                    threshold = 12,
                                    scale_factor = 1.4,
                                    max_keypoints = 100,
                                    normalized = True)

            if kpts1 != None:
                for i in range(0,dir_num):
                    match_value = 0
                    item_lists = os.listdir(FILE_NAME+"/"+dir_lists[i])
                    item_num = len(item_lists)
                    for j in range(0,item_num):
                        kpts2=image.load_descriptor("/keypoints/%s/%s"%(dir_lists[i],item_lists[j]))
                        c = image.match_descriptor(kpts1, kpts2, threshold = 85)
                        if c[6] > match_value :
                            match_value = c[6]

                        #match_value += c[6]
                    max_match.append(match_value)
                    #uart.write(str(match_value))
                    #uart.write(str("\r\n"))

                    #if match_value > max_match:
                        #max_match = match_value
                        #match_num = i

                match_max = 0
                for i in range(len(max_match)):

                    if match_max < max_match[i]:
                        match_max = max_match[i]
                        match_num = i

                uart.write(str("\r\n"))
                uart.write(str(match_max))
                uart.write(str("\r\n"))
                #if(max_match > 55):
                loop_flag = 0

                uart.write(str(match_num+1))
                uart.write(str("find face"))

                red.off()

            else :
                uart.write(str("no kpts"))

        else :
            uart.write(str("no face"))
			
			
#****************************************************************************


def register():  #此函数用于现场录入新的人脸

    photo_num = 10
    global face_cascade
    global FILE_NAME
    # 初始化摄像头
    #sensor.reset()

    # 设置相机图像的对比度为3
    #sensor.set_contrast(3)

    # 设置相机的增益上限为16
    #sensor.set_gainceiling(16)

    # 设置采集到照片的大小
    #sensor.set_framesize(sensor.QVGA)

    # 在VGA(640*480)下开个小窗口，相当于数码缩放
    #sensor.set_windowing((320, 240))

    # 设置采集到照片的格式：灰色图像
    #sensor.set_pixformat(sensor.GRAYSCALE)

    #sensor.skip_frames(time = 3000)     # Wait for settings take effect.

    dir_lists = os.listdir(FILE_NAME)  # 路径下文件夹
    dir_num = len(dir_lists)

    new_dir = ("%s/s%d") % (FILE_NAME,int(dir_num)+1)
    os.mkdir(new_dir)
    # 初始化特征kpts1
    kpts1 = None
    red.on()
    while(photo_num):

        # 拍摄图片并返回img
        img = sensor.snapshot()

        #img.draw_string(0, 0, "Looking for a face...")

        objects = img.find_features(face_cascade, threshold=0.7, scale_factor=1.25)  #找到人脸特征find_features返回列表
        if objects:
            #img.draw_rectangle(object[0])
            # 将 ROI（x, y, w, h）往各个方向扩展31像素
            face = (objects[0][0]-15,
                    objects[0][1]-15,
                    objects[0][2]+15*2,
                    objects[0][3]+15*2)
            # 使用扩展后的ROI区域(人脸)学习关键点
            kpts1 = img.find_keypoints(roi = face,  #find_keypoints返回
                                    threshold = 12,
                                    scale_factor = 1.4,
                                    max_keypoints = 100)

            #img.draw_keypoints(kpts1, size=15)

            #img = sensor.snapshot()
            #将人脸保存到本地文件
            if kpts1 :
                image.save_descriptor(kpts1, "%s/%d.orb"%(new_dir,photo_num))
                photo_num -= 1
                print(photo_num)
                red.off()
                blue.on()
                time.sleep_ms(200)
                blue.off()
                red.on()
            else :
                pass
        else:
            print("no find face")
    pyb.LED(2).on()
    sensor.skip_frames(time = 100)
    pyb.LED(2).off()
    sensor.skip_frames(time = 100)
    pyb.LED(2).on()
    sensor.skip_frames(time = 100)
    pyb.LED(2).off()
    lcd.clear()
    red.off()
    uart.write(str("f"))#发送f代表学习完成






#****************************************************************************
uart = UART(3,115200)   #串口

red   = pyb.LED(1)
green = pyb.LED(2)
blue  = pyb.LED(3)


# 初始化摄像头
sensor.reset()

# 设置相机图像的对比度为1
sensor.set_contrast(1)

# 设置相机的增益上限为16
sensor.set_gainceiling(16)

# 设置采集到照片的大小
sensor.set_framesize(sensor.LCD)

# 在VGA(640*480)下开个小窗口，相当于数码缩放
#sensor.set_windowing((320, 240))

# 设置采集到照片的格式：灰色图像
sensor.set_pixformat(sensor.GRAYSCALE)

# 加载Haar Cascade 模型
# 默认使用25个步骤，减少步骤会加快速度但会影响识别成功率
face_cascade = image.HaarCascade("frontalface", stage = 25)

# 创建一个时钟来计算摄像头每秒采集的帧数FPS
clock = time.clock()

#lcd.init()

while(True):   #主函数

    img = sensor.snapshot()

    clock.tick()
    # 拍摄图片并返回img
    #img = sensor.snapshot()

    # 寻找人脸对象
    # threshold和scale_factor两个参数控制着识别的速度和准确性
    objects = img.find_features(face_cascade, threshold=0.75, scale_factor=1.25)

    # 用矩形将人脸画出来
    for r in objects:
        img.draw_rectangle(r)
    #lcd.display(img)
    # 串口打印FPS参数
    print(clock.fps())

    if uart.any():
        data = uart.readline().decode()
        print(data)
        #data = uart.readchar()
        if data == 'R':
            green.on()
            time.sleep_ms(100)
            green.off()
            register()

        elif data == 'F':
            red.on()
            time.sleep_ms(100)
            red.off()
            find_face()
        elif data == 'M':
            red.on()
            #time.sleep_ms(100)
            #blue.off()
            find_mask()




