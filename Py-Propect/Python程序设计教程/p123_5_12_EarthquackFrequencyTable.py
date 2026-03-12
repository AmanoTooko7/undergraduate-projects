#这里传进来的aList是地震级数第一行题目下(用mag表示)的数据列表，
#输出地震的不同级数的次数，但因为我没找到数据所以并没有书上效果
def EarthquackFrequencyTable(aList):
    countDict = {}

    for item in aList:
        if item in countDict:
            countDict[item] = countDict[item] + 1#增加数据次数
        else:
            countDict[item] = 1

    itemList = list(countDict.keys())
    itemList.sort()

    print("ITEM","FREQUENCY")
    #item为键的列表(这里键指的是数据mag)
    for item in itemList:
        print("{0:4.2f}{1:6d}".format(item, countDict[item]))

EarthquackFrequencyTable(["1.3","3.3"])
