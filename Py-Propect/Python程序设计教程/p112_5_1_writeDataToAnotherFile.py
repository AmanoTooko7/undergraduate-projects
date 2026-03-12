#从rainfall这个每个地区对应的降水量(单位inches)的文件，转为每个地区的降水量(单位cm),rainfallInCM这个txt文件
with open("rainfall.txt", "r") as rainFile:
    with open("rainfallInCM.txt", "w") as outFile:

        for aLine in rainFile:
            values = aLine.split()
            inches = float(values[1])
            cm = inches * 2.54
            aChars = outFile.write(values[0] + " " +str(cm) + "\n")
