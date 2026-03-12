#此文件用于莫烦Python基础教程的程序练习
#p15-17------------------------------------------------------------------------------------------------------------------------------------------------
# text = 'this is test file\nfor 莫烦Python'
# my_file = open('my_file.txt', 'w')#打开文件
# my_file.write(text)#写入text文件
# my_file.close()#关闭文件/////////////////////////////
# append_text = '\nthis is append file'
# my_file = open('my_file.txt', 'a')#向my_file文件里加入append_text的内容
# my_file.write(append_text)#追加的append_text文件的内容
# my_file.close()#关闭文件//////////////////////////////////
# file = open('my_file.txt', 'r')
# #content = file.read()#读取file文件存入content,输出结果为
# #content = file.readline()#readline()表示读取第一行，若下一句再次调用readline()则读取第二行，依次
# content = file.readlines()#全部输出结果为一个数组，每一行为一个元素
# print(content)
#p18-19------------------------------------------------------------------------------------------------------------------------------------------------
# class Calculator:
#     def __init__(self,name, price, hight, width, weight):    #此句话为初始化函数的属性，可以直接在上一句括号里固定属性值，或者也可以自定义属性值
#         self.name = name
#         self.price = price
#         self.h = hight
#         self.wi = width
#         self.we = weight
#     def add(self, x, y):
#         print(self.name)#这里的self.name是调用这个类的属性
#         result = x + y
#         print(result)
#     def minus(self, x, y):
#         result = x - y
#         print(result)
#     def times(self, x, y):
#         print(x * y)
#     def divide(self, x, y):
#         print(x / y)
# calcu = Calculator('good calculator',17,21,23,7)#调用其内部函数就用calcu.函数名,自定义属性值
# #print(calcu.name, calcu.price)#调用Calculator这个class这个属性
# #calcu.wi = 7#重新定义属性值
# print(calcu.wi)
# for i in range(3):
#     print(i)
#字典,key对应的value可以是列表，字典，元组使用类似print(d['pear'][1])这种方式调用-------------------------------------------------------------------------------
#d = {'apple':[1,2,3], 'pear':{1:7, 2:3}, 'orange':(4,5)}
#p29zip lambda和map-----------------------------------------------------------------------------------------------------------------------------------
# a = [1,2,3]
# b = [4,5,6]
# zip(a,b)#zip函数将a,b两个列表合并成一个元组的列表,结果为[(1, 4), (2, 5), (3, 6)],zip(a,a,b)#结果为[(1, 1, 4), (2, 2, 5), (3, 3, 6)]
# fun = lambda x,y:x+y#lambda函数，x,y为参数，x+y为返回值,与def函数不同的是lambda函数只能有一个返回值，且不需要return
# list(map(fun,[1,2],[3,4]))#map函数，将fun函数作用于[1,2]和[3,4]两个列表，list为[4, 6]
#p30浅复制和深复制-----------------------------------------------------------------------------------------------------------------------------------
# import copy
# a = [1,2,3,[7,6,5]]
# id(a)#id函数，返回a的内存地址，可以用来判断两个变量是否指向同一个内存地址，如果是同一个地址，则修改其中一个变量的值，另一个变量的值也会改变
# b = copy.copy(a)#浅复制，b的结果为[1, 2, 3, [7, 6, 5]],浅复制只复制第一层，第二层的列表还是指向同一个内存地址，所以修改b[3][0]的值，a[3][0]的值也会改变
# print(id(b) == id(a))#因为只会复制第一层，所以id(b)和id(a)不同,结果为False
# print(id(a[3]) == id(b[3]))#id(a[3])和id(b[3])相同，因为第二层的列表指向同一个内存地址，结果为True
# c = copy.deepcopy(a)#深复制，c的结果为[1, 2, 3, [7, 6, 5]],深复制会复制所有层，所以c和a的内存地址不同，结果为False
# #所以浅复制和深复制的区别在于是否复制所有层，浅复制只复制第一层，所以第二层地址是相同，深复制复制所有层，所以所有层的地址都是不同的
#p34pickle一种文件的存储方式----------------------------------------------------------------------------------------------------------------------------
# import pickle
# a_dict = {'da':111, 2:[23,1,4], '23':{1:2,'d':'sad'}}#定义的字典
# with open('pickle_example.pickle', 'rb') as file:#打开pickle_example.pickle文件，wb表示写入二进制文件,file表示把pickle_example.pickle文件存入file
#     #pickle.dump(a_dict, file)#将a_dict字典写入file文件
#     a_dict1 = pickle.load(file)#将file文件读取出来存入a_dict1
# print(a_dict1)#输出a_dict1
#p35set找不同-----------------------------------------------------------------------------------------------------------------------------------------
char_list = ['a','b','c','c','d','d','d']
sentence = 'Welcome Back to This Tutorial'#
#print(set(char_list))#set函数，将char_list列表转换成集合，集合的特点是无序且不重复，结果为{'a', 'b', 'c', 'd'}
#print(set(sentence))#set(sentence)是一个集，结果为{'a', 'c', 'B', ' ', 'o', 'm', 'e', 'l', 'T', 'i', 'r', 'u', 'W', 'k', 't', 'h', 's', 'a', 'c', 'l'}
unique_char = set(char_list)
unique_char.add('x')#add函数，将'x'加入unique_char集合，而不能unique_char.add('x'，‘y’)
print(unique_char)
set1 = unique_char
set2 = {'a','e','i'}
print(set1.difference(set2))#difference函数，找出set1中不在set2中的元素，结果为{'c', 'd', 'x', 'b'}
print(set1.intersection(set2))#intersection函数，找出set1和set2中相同的元素，结果为{'a'}
#p36RegEx正则表达式-----------------------------------------------------------------------------------------------------------------------------------
#见jupyter notebook




