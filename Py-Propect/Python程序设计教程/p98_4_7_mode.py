#此函数用于计算众数
def mode(aList):#aList为传进来的数据列表
    
    countDict = {}#里面保存的是{aList的各个数据：此数据出现的次数}

    #以下这个for目的是生成countDict字典
    for item in aList:#item为数据中的各个项,下面作为couuntDict的键
        
        if item in countDict:
            countDict[item] = countDict[item] + 1
        else:
            countDict[item] = 1#此句为新添加的键对在countDict末尾

    countList = countDict.values()#返回次数的列表
    maxCount = max(countList)#找到aList中的元素次数出现最多的，并返回这个次数

    modeList = []
    for item in countDict:                  #item并不是表示一个键对，而是仅仅表示一个键
        if countDict[item] == maxCount:   #countDict[item]表示“对”，也就是数据出现的次数
            modeList.append(item)

    return modeList
            
     #当这个数据列表有多个众数时也可起作用，因为max返回的是数据出现的最多的次数,
     #当有两个或以上的的数据出现相同的次数且都为最大时，再把item加进去

a=mode([12,45,2,2,2,6,7,1,1,1,2,1])
print(a)
