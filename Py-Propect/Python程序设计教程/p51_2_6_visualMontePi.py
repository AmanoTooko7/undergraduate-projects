import math
import turtle
import random

def showMontePi(numDarts):
    #设置窗口和对象
    wn = turtle.Screen()
    t = turtle.Turtle()

    wn.setworldcoordinates(-20, -20, 20, 20)

    #绘制十字坐标
    t.up()
    t.goto(-50, 0)
    t.down()
    t.goto(50, 0)

    t.up()
    t.goto(0, 50)
    t.down()
    t.goto(0,-50)

    inCircle = 0#此参数用于记录有多少点落在圆内
    t.up()
    t.goto(0, 0)
    t.down()

    #
    for i in range(numDarts):
        
        x = 10 * random.random()
        y = 10 * random.random()

        distance = math.sqrt(x**2 + y**2)

        if distance <= 1:
            inCircle = inCircle + 1
            t.color("pink")
        else: t.color("orange")

        t.goto(x, y)
        t.dot()

    pi = inCircle / numDarts*4
    wn.exitonclick()

    return pi
