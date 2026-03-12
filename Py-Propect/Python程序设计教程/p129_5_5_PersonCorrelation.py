#皮尔逊相关系数程序实现
#这里的xList,yList两个列表的长度必修为一样的
def correlation(xList, yList):#传进来的两个参数为两个列表
    import statistics
    xBar = statistics.mean(xList)
    yBar = statistics.mean(yList)
    xStd = statistics.stdev(xList)
    yStd = statistics.stdev(yList)

    num = 0
    for i in range(len(xList)):
        num = num + (xList[i]-xBar) * ((yList[i]-yBar))
    corr = num / ((len(xList)-1)*xStd*yStd)
    return corr
    
