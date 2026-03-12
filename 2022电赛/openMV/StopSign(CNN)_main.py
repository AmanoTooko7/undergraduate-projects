#此程序用于结合2022电赛1.小停止位的识别，2.用四个窗口识别巡线，分辨单线和岔路口，大停止位。共两个程序
THRESHOLD = (4, 25, -20, 6, -2, 26)
import sensor, image, time, ustruct, pyb, os, tf, math, uos, gc, pyb
from pyb import UART, LED

LED(1).on()
LED(2).on()
LED(3).on()

sensor.reset()
sensor.set_vflip(True)
sensor.set_hmirror(True)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQQVGA)
sensor.skip_frames(time=2000)

#串口定义
uart = UART(3, 115200)  # 定义串口3变量
uart.init(115200, bits=8, parity=None, stop=1)

#停止位神经网络模型识别的参数定义
net = None
labels = None
min_confidence = 0.5



#下一段不重要，因为我也不晓得用来干啥子
try:
    # load the model, alloc the model file on the heap if we have at least 64K free after loading
    net = tf.load("trained.tflite", load_to_fb=uos.stat('trained.tflite')[6] > (gc.mem_free() - (64*1024)))
except Exception as e:
    raise Exception('Failed to load "trained.tflite", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')

try:
    labels = [line.rstrip('\n') for line in open("labels.txt")]
except Exception as e:
    raise Exception('Failed to load "labels.txt", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')

#串口方块识别区域
roi1 = [(0, 1, 20, 28),  # 左上  x y w h
        (0, 35,20, 22),  #左下
        (30,0, 22, 15),  # 上
        (54,32,27, 29),  #右下
        (0, 0, 80, 60)]  # 停车
#表示目标画框的颜色
colors = [ #
    (255,   0,   0),#红
    (  0, 255,   0),#绿色
    (255, 255,   0),
    (  0,   0, 255),
    (255,   0, 255),
    (  0, 255, 255),
    (255, 255, 255),
]

#定义函数用于串口传输
def outuart(x, a, flag):  # 用于给主控传递参数
    global uart;
    f_x = 0     #这两个值用于判断是单线(01)还是双线(10)
    f_a = 0     #
    if flag == 0:
        pass

    if flag == 1: #拐弯或直线(单线)
        x,a,f_x,f_a=(rho_err,theta_err,0,1)
    if flag == 2:  # 上左#有弯道时
        x, a, f_x, f_a = (rho_err, theta_err, 1, 0)
    if flag==3: #上右#发现停止位时
        x,a,f_x,f_a=(rho_err,theta_err,1,1)
    if flag == 4:  # stop
        x, a, f_x, f_a = (0, 0, 0, 0)


    data = [" 0x2C ",  # 帧头1
            " 0x12 ",  # 帧头2
            int(x),  # up sample by 4   #数据1
            int(a),  # up sample by 4    #数据2
            int(f_x),  # up sample by 4    #数据1
            int(f_a),  # up sample by 4    #数据2
            " 0x5B "]

    uart.write(str("%s\r\n") % (data))  # 必须要传入一个字节数组

#以不用在意
p9_flag = 0  # p9需检测从低变高
not_stop = 0

clock = time.clock()  # 此句与帧率有关

#主程序
while(True):
    clock.tick()
    img = sensor.snapshot().binary([THRESHOLD])
    line = img.get_regression([(100, 100)], robust=True)

    left_up_flag, left_down_flag, up_flag, right_fiag = (0, 0, 0, 0)
    for rec in roi1:
        img.draw_rectangle(rec, color=(255, 0, 0))  # 绘制出roi区域
    p = pyb.Pin("P9", pyb.Pin.IN)
    # print(p.value())
    if p.value() == 0:
        p9_flag = 1
    if p.value() == 1 and p9_flag == 1:
        not_stop = 1
        p9_flag = 0

    # 对线性回归的直线做出处理
    if (line):
        rho_err = abs(line.rho()) - img.width() / 2
        if line.theta() > 90:
            theta_err = line.theta() - 180
        else:
            theta_err = line.theta()
        # 直角坐标调整
        img.draw_line(line.line(), color=127)
        # 画出直线
        if line.magnitude() > 8:
            outdata = [rho_err, theta_err, 0]

            if img.find_blobs([(96, 100, -13, 5, -11, 18)], roi=roi1[0]):  # 左上
                # print('left')
                left_up_flag = 1
            else:
                left_up_flag = 0

            if img.find_blobs([(96, 100, -13, 5, -11, 18)], roi=roi1[1]):  # 左下
                # print('right')
                left_down_flag = 1
            else:
                left_down_flag = 0

            if img.find_blobs([(96, 100, -13, 5, -11, 18)], roi=roi1[2]):  # up
                # print('up')
                up_flag = 1
            else:
                up_flag = 0
            if img.find_blobs([(96, 100, -13, 5, -11, 18)], roi=roi1[3]):  #
                # print('stop sign')
                right_flag = 1
            else:
                right_flag = 0

            if (left_down_flag and left_up_flag and up_flag and right_flag) == 1:  # 用于判断停止符
                outuart(0, 0, 3)
                print('11')
                continue
            if (left_up_flag and up_flag) == 0:  # 用于判断只要有一条线
                outuart(0, 0, 1)
                print('01')
                continue
            if (left_up_flag and left_down_flag and up_flag) == 1:  # 用于判断是岔路口
                outuart(0, 0, 2)
                print('10')
                continue

        else:
            pass

        #此段是CNN检测小停止位的程序
        result = net.detect(img, thresholds=[
            (math.ceil(min_confidence * 255), 255)])  # 检测image，要大于阈值，会返回两个元素(分别是两个列表)否则就没有识别到目标
        for i, detection_list in enumerate(result):  # i[0]表示背景，列表有背景左上点坐标和长宽，以及置信度(0到1的数值)，共5个元素，#i[2]是识别到的目标，同上一共五个元素

            # i==0表示第一个元素(这个元素表示背景)的列表，i==1表示第二个元素，表示检测到的目标的列表
            # len(detection)表示同一个i下有多少个不同的目标值,也就是i中有多少个列表，返回列表长度
            if (i == 0): continue  # background class#未背景就进入下一个循环
            if (len(detection_list) == 0): continue  # len==0表示没有检测到目标值
            # continue表示直接跳出当层for循环，并不会对for以外的循环反应

            print("********** %s **********" % labels[i])
            for d in detection_list:
                [x, y, w, h] = d.rect()  # 表示将i中的列表里的元素(这个元素表示识别到的一个目标)的坐标值和宽高赋值

                center_x = math.floor(x + (w / 2))  # 计算目标的中心坐标
                center_y = math.floor(y + (h / 2))

                print('x %d\ty %d' % (center_x, center_y))
                img.draw_circle((center_x, center_y, 12), color=colors[i], thickness=2)  # 圈出目标的中心点

    else:
        outuart(0, 0, 4)
        print('stop')

