#此函数输出文件第一行标题中的(也就是传进去的数据名)对应的数据,
def makeDataList(dataName):
    import csv
    with open("earthquake.csv", "r") as inFile:
        dataList = []#用于存放标题对应的数据

        csvReader = csv.reader(inFile)#获取迭代器
        titles = next(csvReader)#获取文件的第一排内容返回列表到titles

        colNum = 0#

        #下一行：当不等于(!=)时为真，而在下行循环中直到第二个条件为Flase时(dataName不是第一行的最后一个)
        #第一个条件永远为真，此时跳出循环，colNum的值为列表中数据名的index
        while colNum < len(titles) and titles[colNum] != dataName:
            colNum = colNum + 1

        if colNum == len(titles):
            print("Error: ", colNum, "not found.")
        else:
            for line in csvReader:#这个lines是eahquake.csv中的列表(以文件中的每一行为一个列表)
                dataList.append(float(line[colNum]))

        return dataList
    
a = makeDataList("iugofoa")
print(a)

        
