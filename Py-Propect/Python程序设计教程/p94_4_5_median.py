def median(alist):
    copylist = alist[:]
    copylist.sort()

    if len(copylist) % 2 == 0:#当列表有偶数个元素时
        #以下两排表示位置，用于索引
        rightMid = len(copylist) // 2
        leftMid = rightMid - 1
        
        median = (copylist[leftMid] + copylist[rightMid]) / 2
    else:
        mid = len(copylist) // 2
        median = copylist[mid]

    return median

a = [32,42,341,12,34]
print(median(a))
