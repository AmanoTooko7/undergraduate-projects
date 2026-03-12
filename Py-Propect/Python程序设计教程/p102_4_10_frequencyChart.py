#创建一个频率直方图
import turtle
def frequencyChart(aList):

    #以下六排为创建countDict{数据：此数据出现次数}
    countDict = {}
    for item in aList:
        if item in countDict:
            countDict[item] = countDict[item] + 1
        else:
            countDict[item] = 1

    itemList = list(countDict.keys())#获取键的列表，也就是数据
    minItem = 0#?
    maxItem = len(itemList) - 1#返回键的长度-1，也就是返回数据的长度-1,此变量用于控制
    itemList.sort()

    countList = list(countDict.values())#获取对的列表
    maxCount = max(countList)#返回此列表中最大的出现此数据的次数

    wn = turtle.Screen()
    chartT  =  turtle.Turtle()
    wn.setworldcoordinates(-1,-1,maxItem + 1,maxCount + 1)#？
    chartT.hideturtle()#此句把那个箭头隐藏了

    #以下四句目的是画出x轴,此时不会画出数据
    chartT.up()
    chartT.goto(0,0)
    chartT.down()
    chartT.goto(maxItem, 0)
    chartT.up()

    #以下四排函数目的是在y轴上绘制数据出现的次数(最小值和最大值)
    #write函数第一个次数必须为字符也就是想写的内容
    #第二个参数为字体的(名称，大小，类型)
    chartT.goto(-1, 0.65)                          #规定0的作图位置
    chartT.write("1", font=("Helvetica",16,"bold"))
    chartT.goto(-1, maxCount)                   #规定最大次数的的作图位置
    chartT.write(str(maxCount),font=("Helvetica",16,"bold"))

    for index in range(len(itemList)):#在数据的长度中循环

        #下两排用于写X的数据
        chartT.goto(index, -1)
        chartT.write(str(itemList[index]),font=("Helvetica",16,"bold"))

        #以下四排目的是绘制坐标的图像内容，也就是可视化每个数据对应的出现次数
        chartT.goto(index, 0)
        chartT.down()
        chartT.goto(index, countDict[itemList[index]])
        chartT.up()
    wn.exitonclick()


frequencyChart([7,8,23,56,34,2,3,5,34,1,1,1,2,2,4,5,6,7,7,8,6,5,6,7,7,7,7,7,7,0])

        
