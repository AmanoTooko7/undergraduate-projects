# Untitled - By: 29595 - 周一 7月 4 2022

import sensor, image, time, os, lcd, pyb, struct, tf , gc
from pyb import LED
from pyb import UART

rootpath = "/faces"

red   = pyb.LED(1)
green = pyb.LED(2)
blue  = pyb.LED(3)

DIST_THRESHOLD = 9000  # 差异度阈值
lcd.init()

def find():
    global match_flag
    global face_cascade
    img = sensor.snapshot()
    lcd.display(img)

    objects = img.find_features(face_cascade, threshold=0.6, scale_factor=1.45)  # 人脸检测

    if objects:
        #green.on()
        #time.sleep(500)
        #green.off()
        width_old = 0
        height_old = 0
        index = 0
        for r in objects:  # 寻找最大的face
            if r[2] > width_old and r[3] > height_old:
                width_old = r[2]
                height_old = r[3]
                index += 1
        index -= 1
        #print("index:", index)
        img.draw_rectangle(objects[index])
        face = (objects[index][0]-20,
                objects[index][1]-20,
                objects[index][2]+20*2,
                objects[index][3]+20*2)
        lcd.display(img)
        d0 = img.find_lbp((0, 0, img.width(), img.height()))
        if d0:
            if match_flag:

                #blue.off()

                #res = match(d0)
                match(d0)
                #uart.write(str(res))
                    #debug(res)
                    #uart.write(str(res))

#****************************************************************************


def match(d0):  # 人脸识别
    global match_flag
    dir_lists = os.listdir(rootpath)  # 路径下文件夹
    dir_num = len(dir_lists)          # 文件夹数量
    if dir_num == 0:
        return 0
    #debug("*" * 60)
    #debug("Total %d Folders -> %s"%(dir_num, str(dir_lists)))
    lbq_value = []
    for i in range(0, dir_num):
        item_lists = os.listdir(rootpath+'/'+dir_lists[i])  # 路径下文件
        item_num = len(item_lists)                          # 文件数量

        #debug("The %d Folder[%s], Total %d Files -> %s" %(i+1, dir_lists[i], item_num, str(item_lists)))

        #Path_Backup['path'] = rootpath+'/'+dir_lists[i]  # 马上记录当前路径
        #Path_Backup['id'] = item_num                     # 马上记录当前文件数量
        lbq_min = 99999
        for j in range(0, item_num):  # 文件依次对比
            #debug(">> Current File: " + item_lists[j])
            #try:
            img = None
            img = image.Image("/faces/s%d/%d.pgm" % (i+1, j+1))
            #except Exception as e:
                #debug(e)
                #break
            d1 = img.find_lbp((0, 0, img.width(), img.height()))  # 提取特征值
            dist = image.match_descriptor(d0, d1)                 # 计算差异度
            #debug(">> Difference Degree: " + str(dist))
            if dist < lbq_min:
                lbq_min = dist

                #debug(">> ** Find It! **")
                #green.on()
                #time.sleep(1000)
                #green.off()#
        lbq_value.append(lbq_min)
    lbq_min = 99999
    lbq_num = 0
    for i in range(len(lbq_value)):

        if lbq_min > lbq_value[i]:
            lbq_min = lbq_value[i]
            lbq_num = i
    #print((":%d ") % (lbq_value[lbq_num]))
    uart.write(str((":%d ")%(lbq_value[lbq_num])))
    match_flag = 0
    blue.off()
    if lbq_value[lbq_num] < DIST_THRESHOLD:
        #return lbq_num
        #print((" %d       ") % (lbq_num+1))
        uart.write(str((" %d       ") % (lbq_num+1)))
    else:
        #print(0)
        uart.write(str(0))
        #return 0

    #debug(">> ** No Match! **")
    return 0

#****************************************************************************


def register():
    global face_cascade
    photo_num = 10

    dir_lists = os.listdir(rootpath)  # 路径下文件夹
    dir_num = len(dir_lists)          # 文件夹数量
    new_dir = ("%s/s%d") % (rootpath,int(dir_num)+1)
    os.mkdir(new_dir)
    #n = 10
    green.off()
    while(photo_num):
        img = sensor.snapshot()
        objects = img.find_features(face_cascade,threshold=0.75, scale_factor=1.25)
        if objects:

            width_old = 0
            height_old = 0
            index = 0
            for r in objects:  # 寻找最大的face
                if r[2] > width_old and r[3] > height_old:
                    width_old = r[2]
                    height_old = r[3]
                    index += 1
            index -= 1
            img.draw_rectangle(objects[index])
            face = (objects[index][0]-20,
                    objects[index][1]-20,
                    objects[index][2]+20*2,
                    objects[index][3]+20*2)
            lcd.display(img)
            #n -= 1
            #blue.off()
            #photo_num -= 1
            #img.save("%s/%d.pgm" % (new_dir,photo_num) ) # or "example.bmp" (or others)
            if uart.any():
                data = uart.readline().decode()
                if data == 'P' :
                    blue.on()
                    #n = 10
                    #data = uart.readchar()
                    img.crop(face)
                    img.save("%s/%d.pgm" % (new_dir,photo_num) ) # or "example.bmp" (or others)

                    photo_num -= 1
                    print(photo_num)
                    blue.off()
        else:
            pass

    if uart.any():
        data = uart.readline().decode()



#****************************************************************************


uart = UART(3,115200)
# 加载Haar Cascade 模型
# 默认使用25个步骤，减少步骤会加快速度但会影响识别成功率


# 初始化摄像头
sensor.reset()

# 设置相机图像的对比度为1
sensor.set_contrast(1)

# 设置相机的增益上限为16
sensor.set_gainceiling(16)

sensor.set_framesize(sensor.QVGA)

sensor.set_windowing((128, 160))

sensor.set_pixformat(sensor.GRAYSCALE)

sensor.skip_frames(100)

match_flag = 0
face_cascade = image.HaarCascade("frontalface", stage = 25)
while(True):
    find()
    if uart.any():
        data = uart.readline().decode()
        print(data)
        #data = uart.readchar()
        if data == 'R':
            green.on()
            #time.sleep_ms(100)

            register()

        elif data == 'F':
            blue.on()
            #time.sleep_ms(100)
            match_flag = 1
            #red.off()
            #find_face()
        #elif data == 'M':
            #red.on()
            #time.sleep_ms(100)
            #blue.off()
            #find_mask()
    gc.collect()
