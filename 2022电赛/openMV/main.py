#1.3巡线，分辨单线和岔路口，停止位识别成品，使用右下方带方块检测停止位一共四个小窗口，但用在实际情况并不符合
THRESHOLD = (0, 24, -20, 127, -128, 127)  # 这个颜色阈值用于将地图黑线设置为目标值
import sensor, image, time, ustruct
from pyb import UART, LED
# from pid import PID
# rho_pid = PID(p=0.4, i=0)
# theta_pid = PID(p=0.001, i=0)
import pyb

LED(1).on()
LED(2).on()
LED(3).on()

sensor.reset()
sensor.set_vflip(True)
sensor.set_hmirror(True)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQQVGA)  # 80x60 (4,800 pixels) - O(N^2) max = 2,3040,000.
# sensor.set_windowing([0,20,80,40])
sensor.skip_frames(time=2000)  # WARNING: If you use QQVGA it may take seconds
clock = time.clock()  # to process a frame sometimes.

uart = UART(3, 115200)  # 定义串口3变量
uart.init(115200, bits=8, parity=None, stop=1)  # init with given parameters

# 识别区域
roi1 = [(0, 1, 20, 28),  # 左上  x y w h
        (0, 35,20, 22),  #左下
        (30,0, 22, 15),  # 上
        (54,32,27, 29),  #右下
        (0, 0, 80, 60)]  # 停车


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


p9_flag = 0  # p9需检测从低变高
not_stop = 0
while (True):
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

    #对线性回归的直线做出处理
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
            else: left_up_flag = 0

            if img.find_blobs([(96, 100, -13, 5, -11, 18)], roi=roi1[1]):  # 左下
                 #print('right')
                 left_down_flag = 1
            else: left_down_flag = 0

            if img.find_blobs([(96, 100, -13, 5, -11, 18)], roi=roi1[2]):  # up
                # print('up')
                up_flag = 1
            else: up_flag = 0
            if img.find_blobs([(96, 100, -13, 5, -11, 18)], roi=roi1[3]):  #
                # print('stop sign')
                right_flag = 1
            else: right_flag = 0

            if (left_down_flag and left_up_flag and up_flag and right_flag)==1:  #用于判断停止符
                outuart(0,0,3)
                print('11')
                continue
            if (left_up_flag and up_flag) == 0:  #用于判断只要有一条线
                outuart(0,0,1)
                print('01')
                continue
            if (left_up_flag and left_down_flag and up_flag) == 1:#用于判断是岔路口
                outuart(0, 0, 2)
                print('10')
                continue

        else:
            pass
    else:
        outuart(0, 0, 4)
        print('stop')
