#以下为计算标准差，越小表示数据紧密的帖在平均值的周围
import math
import statistics
def standarDev(aList):
    theMean = statistics.stdev(aList)
    b = 0
    #这个for循环只用做列表中的每个数据减去平均值，平方后加和这个工作
    for i in aList:
        a = (i-theMean) ** 2
        b = b + a

    value = math.sqrt(b/(len(aList) - 1))

    return value

print(standarDev([12,34,5,6,32,4,0,100]))

    
        
