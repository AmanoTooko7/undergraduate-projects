#没看懂这个，感觉有问题
def FrequencyTableAlt(aList):
    print("ITEM", "FREQUENCY")

    sortedList = aList[:]#将传进来的列表复制
    sortedList.sort()

    countList = []

    previous = sortedList[0]#将排序后的第一位赋值
    groupCount = 0
    for current in sortedList:
        if current == previous:
            groupCpunt = groupCount + 1
            previous = current
        else:#当前一位数和后一位数不相同时
            print(previous, " ", groupCount)
            previuos = current
            groupCount = 1

    printt(previous, " ", groupCount)
    
