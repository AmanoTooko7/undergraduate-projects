#1.4使用神经网络通过二值图像来识别停止位和开始位，在edge impluse生成的程序中多加了镜头的景象反转和返回二值图像，图中标红部分为加的程序
# Edge Impulse - OpenMV Object Detection Example
THRESHOLD = (4, 25, -20, 6, -2, 26)#这个阈值用于地图路线和A点的小停止符

import sensor, image, time, os, tf, math, uos, gc

sensor.reset()                         # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)    # 设置图像的色彩为彩色
sensor.set_framesize(sensor.QVGA)      # Set frame size to QVGA (320x240)
sensor.set_windowing((240, 240))       # Set 240x240 window.
sensor.skip_frames(time=2000)          # Let the camera adjust.
sensor.set_vflip(True)
sensor.set_hmirror(True)

net = None
labels = None
min_confidence = 0.5

try:
    # load the model, alloc the model file on the heap if we have at least 64K free after loading
    net = tf.load("trained.tflite", load_to_fb=uos.stat('trained.tflite')[6] > (gc.mem_free() - (64*1024)))
except Exception as e:
    raise Exception('Failed to load "trained.tflite", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')

try:
    labels = [line.rstrip('\n') for line in open("labels.txt")]
except Exception as e:
    raise Exception('Failed to load "labels.txt", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')

colors = [ # 表示目标画框的颜色
    (255,   0,   0),#红
    (  0, 255,   0),#绿色
    (255, 255,   0),
    (  0,   0, 255),
    (255,   0, 255),
    (  0, 255, 255),
    (255, 255, 255),
]

clock = time.clock()
while(True):
    clock.tick()

    img = sensor.snapshot().binary([THRESHOLD])

    result = net.detect(img, thresholds=[(math.ceil(min_confidence * 255), 255)])#检测image，要大于阈值，会返回两个元素(分别是两个列表)否则就没有识别到目标
    for i, detection_list in enumerate(result):#i[0]表示背景，列表有背景左上点坐标和长宽，以及置信度(0到1的数值)，共5个元素，#i[2]是识别到的目标，同上一共五个元素

        #i==0表示第一个元素(这个元素表示背景)的列表，i==1表示第二个元素，表示检测到的目标的列表
        #len(detection)表示同一个i下有多少个不同的目标值,也就是i中有多少个列表，返回列表长度
        if (i == 0): continue # background class#未背景就进入下一个循环
        if (len(detection_list) == 0): continue # len==0表示没有检测到目标值
                                                #continue表示直接跳出当层for循环，并不会对for以外的循环反应


        print("********** %s **********" % labels[i])
        for d in detection_list:
            [x, y, w, h] = d.rect()#表示将i中的列表里的元素(这个元素表示识别到的一个目标)的坐标值和宽高赋值

            center_x = math.floor(x + (w / 2))#计算目标的中心坐标
            center_y = math.floor(y + (h / 2))

            print('x %d\ty %d' % (center_x, center_y))
            img.draw_circle((center_x, center_y, 12), color=colors[i], thickness=2)#圈出目标的中心点

    print(clock.fps(), "fps", end="\n\n")
