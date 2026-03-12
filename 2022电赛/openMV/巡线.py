
THRESHOLD = (0, 24, -20, 127, -128, 127) # Grayscale threshold for dark things…
import sensor, image, time
from pyb import LED
import car
from pid import PID
rho_pid = PID(p=0.4, i=0)#控制是直线在视野中左右的距离的偏移
theta_pid = PID(p=0.001, i=0)

LED(1).on()
LED(2).on()
LED(3).on()

sensor.reset()
sensor.set_vflip(True)
sensor.set_hmirror(True)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQQVGA) # 80x60 (4,800 pixels) - O(N^2) max = 2,3040,000.
#sensor.set_windowing([0,20,80,40])
sensor.skip_frames(time = 2000)     # WARNING: If you use QQVGA it may take seconds
clock = time.clock()                # to process a frame sometimes.

while(True):
    clock.tick()
    img = sensor.snapshot().binary([THRESHOLD])  #进行二值画分割，将黑线分成白色，非黑色的线分为黑色
    line = img.get_regression([(100,100)], robust = True)#返回给line一条直线
    if (line):
        rho_err = abs(line.rho())-img.width()/2  #计算的是直线与我们的图像中央偏移的距离
        if line.theta()>90:   #
            theta_err = line.theta()-180
        else:
            theta_err = line.theta()
        img.draw_line(line.line(), color = 127)
        print(rho_err,line.magnitude(),rho_err)
        if line.magnitude()>8:            #magnitude的值越大说明得到的线性回归这一条直线效果越好
            #if -40<b_err<40 and -30<t_err<30:
            rho_output = rho_pid.get_pid(rho_err,1)
            theta_output = theta_pid.get_pid(theta_err,1)
            output = rho_output+theta_output   #将两个pid参数进行相加到output
            car.run(50+output, 50-output)  #50为默认速度
        else:
            car.run(0,0)
    else:
        car.run(50,-50)
        pass
    #print(clock.fps())
