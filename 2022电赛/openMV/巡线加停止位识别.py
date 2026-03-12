THRESHOLD = (0, 24, -20, 127, -128, 127) # Grayscale threshold for dark things...
import sensor, image, time
from image import SEARCH_EX, SEARCH_DS
from pyb import LED
import car
from pid import PID
from pyb import UART
rho_pid = PID(p=0.4, i=0)
theta_pid = PID(p=0.001, i=0)

uart = UART(3,115200)
uart.init(115200, bits=8, parity=None, stop=1)

LED(1).on()
LED(2).on()
LED(3).on()

sensor.reset()
sensor.set_vflip(True)
sensor.set_hmirror(True)
sensor.set_contrast(1)  #设置对比度
sensor.set_gainceiling(16)#自动增益


#sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQQVGA) # 80x60 (4,800 pixels) - O(N^2) max = 2,3040,000.
#sensor.set_windowing([0,20,80,40])
#sensor.skip_frames(time = 2000)     # WARNING: If you use QQVGA it may take seconds
sensor.set_pixformat(sensor.GRAYSCALE)  #模板匹配是基于灰度图的


clock = time.clock()                # to process a frame sometimes.
template = image.Image("/1.pgm")

while(True):
    clock.tick()

    img = sensor.snapshot().binary([THRESHOLD]) #生成2值图像
    line = img.get_regression([(100,100)], robust = True)
    if (line):
        rho_err = abs(line.rho())-img.width()/2
        if line.theta()>90:
            theta_err = line.theta()-180
        else:
            theta_err = line.theta()
        img.draw_line(line.line(), color = 127)
        print(rho_err,theta_err)
        pack_1 = ["0xb3","0xb3",rho_err,theta_err,"0x5b"]
        uart.write(str("%s\r\n")%(pack_1))


    r = img.find_template(template, 0.70, step=4, search=SEARCH_EX) #, roi=(10, 0, 60, 60))
    if r:    #这个需要灰度图
        img.draw_rectangle(r)
        pack_2 = ["0x01","0x01",12,"0x00"]
        uart.write(str("%s\r\n")%(pack_2))
