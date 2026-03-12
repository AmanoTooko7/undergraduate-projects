列表解析(list comprehension)
cubes = [x*x*x for x in range(1,11)]
cubes的输出为：
[1, 8, 27, 64, 125, 216, 343, 512, 729, 1000]

进阶：
evenCubes = [x-1 for x in cubes if x%2 ==0]
evenCubes输出为
[7, 63, 215, 511, 999]是先对x进行操作后再对运行x-1这个算式
if为判断语句
