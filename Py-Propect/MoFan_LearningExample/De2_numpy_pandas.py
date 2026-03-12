#此文件用于莫烦Python的numpy_pandas模块教程程序练习
#import numpy as np
#import pandas as pd
# a = np.array([22,35,67],dtype=np.int64)#定义一个数组，dtype为数组的数据类型还有np.float32,np.float64,np.int32,np.int64等
# print(a.dtype)#输出数组的数据类型
#a = np.arange(10,20,2)#定义一个数组，从10开始，到20结束，步长为2,结果为[10 12 14 16 18]
#a = np.arange(12).reshape((3,4))#定义一个数组，从0开始，到11结束，reshape为3行4列,结果为[[ 0  1  2  3] [ 4  5  6  7] [ 8  9 10 11]]
#a = np.linspace(1,10,20).reshape((2,10))#定义一个数组，从1开始，到10结束，分成20份，reshape为4行5列,结果为[[ 1.          1.47368421  1.94736842  2.42105263  2.89473684] [ 3.36842105  3.84210526  4.31578947  4.78947368  5.26315789] [ 5.73684211  6.21052632  6.68421053  7.15789474  7.63157895] [ 8.10526316  8.57894737  9.05263158  9.52631579 10.        ]]
#.reshape(a,b)的功能就是生成a行b列的数组，但是a*b要等于数组的元素个数，其中linspace(c,d,e)的功能就是生成从c到d的e个数的数组

# A = np.arange(2,14).reshape((3,4))
# print(np.argmin(A))#输出A数组中最小值的索引若要输出A的平均值，最大值，最小值，中位数，累加值，累差值等则使用np.mean(A),np.max(A),np.min(A),np.median(A),np.cumsum(A),np.diff(A)
# print(np.transpose(A))#为矩阵的转置也可print(A.T),如果是转置与原矩阵相乘则使用print((A.T).dot(A))
# print(np.clip(A,5,9))#clip函数，将A数组中小于5的值变成5，大于9的值变成9，结果为[[5 5 5 5] [6 7 8 9] [9 9 9 9]]

# A = np.arange(3,15).reshape((3,4))
# #print(A[2][1])#输出A数组中第2行的所有元素
# #print(A[:,1])#输出A数组中第1列的所有元素,print(A[1,1:3])#输出A数组中第1行的第1到第3个元素
# print(A.flatten())#将A数组变成一行，结果为[ 3  4  5  6  7  8  9 10 11 12 13 14]
# print(A.flat)#输出A数组的迭代器，<numpy.flatiter object at 0x000001F3D3D3D4A0>
# for item in A.flat:#flat是一个迭代器，可以用来迭代A数组中的每一个元素
#     print(item)

# A = np.array([1,1,1])[:,np.newaxis]#np.newaxis函数，列增加一个维度，将A数组变成3行1列的数组，结果为[[1] [1] [1]],这里的:表示所有行
# B = np.array([2,2,2])[:,np.newaxis]
# C = np.vstack((A,B))#vstack函数，将A和B数组垂直合并，结果为[[1 1 1] [2 2 2]]
# D = np.hstack((A,B))#hstack函数，将A和B数组水平合并，结果为[1 1 1 2 2 2]
# E = np.concatenate((A,B,B,A),axis=0)#concatenate函数，将A,B,B,A数组按照axis=0纵向方向合并，结果为[[1] [1] [1] [2] [2] [2] [2] [2] [2] [1] [1] [1]]，axis=1横向方向合并
# print(E)

# A = np.arange(12).reshape((3,4))
# print(A)
# #以下两个都是等量分割
# # print(np.split(A,2,axis=1))#split函数，将A数组按照axis=1竖方向分成2份，结果为[array([[0, 1], [4, 5], [8, 9]]), array([[ 2,  3], [ 6,  7], [10, 11]]]
# # print(np.split(A,3,axis=0))#split函数，将A数组按照axis=0行方向分成3份，结果为[array([[0, 1, 2, 3]]), array([[4, 5, 6, 7]]), array([[ 8,  9, 10, 11]])]
# #以下两个都是不等量分割
# #print(np.array_split(A,3,axis=1))#array_split函数，将A数组按照axis=1竖方向分成3份，结果为[array([[0, 1], [4, 5], [8, 9]]), array([[ 2], [ 6], [10]]), array([[ 3], [ 7], [11]])]
# print(np.vsplit(A,3))#将A数组按照axis=0行方向分成3份，结果为[array([[0, 1, 2, 3]]), array([[4, 5, 6, 7]]), array([[ 8,  9, 10, 11]])]
# print(np.hsplit(A,2))#将A数组按照axis=1竖方向分成2份，结果为[array([[0, 1], [4, 5], [8, 9]]), array([[ 2,  3], [ 6,  7], [10, 11]])]

# a = np.arange(7)
# b = a.copy(a)#深复制，将a数组复制一份给b，a和b的内存地址不同，结果为[0 1 2 3 4 5 6],

#以下为pandas学习内容----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# import numpy as np
# import pandas as pd
# s = pd.Series([1,3,6,np.nan,34,1])#定义一个序列，np.nan表示空值，结果为0    1.0    2.0    3.0    4.0    5.0    6.0    7.0    8.0    9.0
# dates = pd.date_range('2024-4-8',periods=6)#定义一个时间序列，从20130101开始，6个时间点，结果为DatetimeIndex(['2013-01-01', '2013-01-02', '2013-01-03', '2013-01-04', '2013-01-05', '2013-01-06'], dtype='datetime64[ns]', freq='D')
# #print(dates)
# df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=['a','b','c','d'])#定义一个数据框，np.random.randn(6,4) 生成的是一个6行4列符合标准正态分布（均值为0，标准差为1）的随机数，行索引为dates，列索引为a,b,c,d，结果为
# print(df)
# df2 = pd.DataFrame({'A':1.,
#                     'B':pd.Timestamp('2024-4-8'),
#                     'C':pd.Series(1,index=list(range(4)),dtype='float32'),
#                     'D':np.array([3]*4,dtype='int32'),
#                     'E':pd.Categorical(["test","train","test","train"]),
#                     'F':'foo'})
# #print(df2)
# #print(df.sort_index(axis=1,ascending=False))#sort_index函数，axis=1表示列，ascending=False表示降序

#pandas选择数据
# dates = pd.date_range('2024-4-8',periods=6)
# df = pd.DataFrame(np.arange(24).reshape(6,4), index=dates, columns=["A","B","C","D"])
#df = pd.DataFrame(矩阵的值, index=行标题, columns=列标题)#-----------------------------------------------------------------
# print(df)
# print(df["A"], df.A)#输出df数据框中A列的数据，df["A"]和df.A是等价的
# print(df[0:3], df["2024-04-08":"2024-04-10"])#输出df数据框中第0到第2行的数据，df[0:3]和df["2024-04-08":"2024-04-10"]是等价的
#以下为通过纯标签连续的选择数据.loc----------------------------------------------------------------------------
# print(df.loc['2024-4-8'])#输出2024-04-08的内容，结果为A    0 B    1 C    2 D    3 Name: 2024-04-08 00:00:00, dtype: int32
# print(df.loc[:, ['A','B']])#输出df数据框中所有行的A,B列的数据，df.loc[行, 列]
# print( df.loc['2024-04-10',['A','B']] )#输出df数据框中第2024-04-10行的A,B列的数据
#以下为通过纯数字选择数据.iloc--------------------------------------------------------------------------------
# print(df.iloc[3])#输出df数据框中第3行的数据，若是df.iloc[3,1]则输出第3行第1列的数据，若是df.iloc[3:5,1:3]则输出第3到第4行第1到第2列的数据
# print(df.iloc[[1,3,5],1:3])#表示输出第1,3,5行的第1,2列的数据
#以下为混合选择数据，ix已经被弃用，使用loc和iloc代替--------------------------------------------------------------
#print(df.iloc[:3, :].loc[:, ['A','C']])#输出第0到第2行的A,C列的数据
#以下筛选某一列的数据大于某一值的行，返回的是符合条件的行，或者某一行小于某一个值----------------------------------------
# print( df[df.A<17] )#

#pandas设定值
# df.iloc[1,1] = 1111#将第2行第2列的值设定为1111，若是df.loc['2024-04-10','C'] = 1111则是将第2024-04-10行的C列的值设定为1111print(df)
# df[df.A>4] = 0#将df数据框中A列大于4的行的所有列的值设定为0
# print(df)
# df.A[df.A>4] = 0#将df数据框中A列大于4的行的A列的值设定为0
# print(df)
# df['F'] = pd.Series( [1,2,3,4,5,6], index=pd.date_range('2024-4-8',periods=6) ) #增加一列F，值为pd.Series([], index=pd.date_range('2024-4-8',periods=6))
#df['增加的列的名称'] = pd.Series(增加列的值， index=增加列的索引)
# print(df)

# #pandas处理丢失数据
# import numpy as np
# import pandas as pd
# dates = pd.date_range('2024-4-8', periods=6)
# df = pd.DataFrame( np.arange(24).reshape((6,4)), index=dates, columns=['A','B','C','D'] )
# df.iloc[0,1] = np.nan#将第0行第1列的值设定为nan
# df.iloc[1,2] = np.nan
# print( df.dropna(axis=0, how='any') )#axis表示行，how='any'表示只要有nan就删除该行，how='all'表示只有所有的值都为nan才删除该行
# print(df.fillna(value=0))#表示df里的nan值用0来填充
# print(df.isnull())#判断df里是否有缺失的数据，若缺失则返回Ture
# print(np.any(df.isnull()) == True )#输出是否df有缺失的数据。输出True表示有缺失的数据，也就是df中至少有一个是==True的

#pandas导入导出
# import numpy as np
# import pandas as pd
# data = pd.read_csv('文件名1。csv')#注意要在当前程序文件目录下
# print(data)
# data.to_pickle('文件名2')#将data存为pickle文件格式，命名为文件名2

#pandas合并DataFrame,使用concat
import numpy as np
import pandas as pd
#以下为concat的例子
# df1 = pd.DataFrame( np.ones((3,4))*0, columns=['a','b','c','d'] )#以下分别定义全是0,1,2的dataframe
# df2 = pd.DataFrame( np.ones((3,4))*1, columns=['a','b','c','d'] )
# df3 = pd.DataFrame( np.ones((3,4))*2, columns=['a','b','c','d'] )
# res = pd.concat( [df1,df2,df3], axis=0, ignore_index=True )#axis=0为上下合并，axis=1为横向左右合并,ignore_index=True表示对res的索引值从新排列
# print(res)#-------------------------------------------------------------------------------------------------------------------
#以下为join的例子['inner','outer']
# df1 = pd.DataFrame( np.ones((3,4))*0, columns=['a','b','c','d'], index=[1,2,3] )
# df2 = pd.DataFrame( np.ones((3,4))*1, columns=['b','c','d','e'], index=[2,3,4] )
# res = pd.concat( [df1,df2], join='inner', ignore_index=True )#这个inner表示合成df1和df2两组的交集也就是b,c,d，不相同的部分直接裁剪带掉
# print(res)----------------------------------------------------------------------------------------------------------------
#以下为join_ases的例子,此已被废弃使用.reindex
# df1 = pd.DataFrame( np.ones((3,4))*0, columns=['a','b','c','d'], index=[1,2,3] )
# df2 = pd.DataFrame( np.ones((3,4))*1, columns=['b','c','d','e'], index=[2,3,4] )
# res1 = pd.concat( [df1,df2], axis=1 )#这里把df1,df2以axis=1横向合并，输出看效果
# res2 = pd.concat([df1, df2.reindex(df1.index)], axis=1)#df2.reindex(df1.index)表示df2以df1的index，把df1和df2左右合并
# print(df1, '\n', df2)
# print(res1,'\n',res2)#-
#在dataframe原有基础上上增加一行s1------------------------------------------------------------------------------------------
# df1 = pd.DataFrame( np.ones((3,4)), columns=['a','b','c','d'] )
# s1 = pd.Series([1,2,3,4], index=['a','b','c','d'])#pd.Series(增加列的值， index=增加列的索引)
# print(len(df1.index))#输出为3
# df1.loc[len(df1.index)] = s1#传入df1索引长度，在df1中增加一行s1
# print(df1)
#合并merge，只支持左右拼接--------------------------------------------------------------------------------------------------
# left = pd.DataFrame({
#     "key": ["K0", "K1", "K2", "K3"],
#     "A": ["A0", "A1", "A2", "A3"],
#     "B": ["B0", "B1", "B2", "B3"],
# })
# right = pd.DataFrame({
#     "key": ["K0", "K1", "K2", "K3"],
#     "C": ["C0", "C1", "C2", "C3"],
#     "D": ["D0", "D1", "D2", "D3"],
# })
# print(left,'\n',right)
# print( pd.merge(left, right, on="key") )#将left和right左右合并，基于key这一列考虑
#-----------------------------------------------------------------------------------------------------------------------
# left = pd.DataFrame({
#     "A": ["A0", "A1", "A2"],
#     "B": ["B0", "B1", "B2"]
# }, index=["K0", "K1", "K2"])
#
#
# right = pd.DataFrame({
#     "C": ["C0", "C2", "C3"],
#     "D": ["D0", "D2", "D3"]
# }, index=["K0", "K2", "K3"])
# print(left,'\n',right)
# res = pd.merge(left, right, left_index=True, right_index=True, how='outer')#inner相当于取left和right列的交集，outer取列的并集
# print(res)
# boys = pd.DataFrame( {'k':['K0','k1','k2'], 'age':[1,2,3]} )
# girls = pd.DataFrame( {'k':['K0','k0','k3'], 'age':[4,5,6]} )
# print(boys, '\n', girls)
# res1 = pd.merge( boys, girls, on='k',  suffixes=['_1','_2'], how='outer')
# res2 = pd.merge( boys, girls, on='k',  suffixes=['_boys','_girl'], how='inner')
# res3 = pd.merge( boys, girls, on='age',  suffixes=['_boys','_girl'], how='outer')
# res4 = pd.merge( boys, girls, on='age',  suffixes=['_boys','_girl'], how='inner')
# print(res1, '\n', res2, '\n', res3, '\n', res4)
#pandas plot画图功能-------------------------------------------------------------------------------------------------------
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
#
# data = pd.Series(np.random.randn(1000), index=np.arange(1000))
# data = data.cumsum()
# data.plot()
# plt.show()







