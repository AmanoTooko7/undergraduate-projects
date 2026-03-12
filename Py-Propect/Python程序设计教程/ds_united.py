from drawSpiral import * #使用import *方法导入drawSpiral这个模块可以随意使用此模块里的所有函数，相当于里面的函数是可见的
import turtle            #而使用import turtle时，相当于turtle里的函数是不可见的，不能在当前编译页面上使用里面的函数
t = turtle.Turtle()
drawSpiral(t, 700)
