#以下为来自莫烦的pytorch教程
#相关内容在官网https://pytorch.org/tutorials/beginner/blitz/tensor_tutorial.html#bridge-to-np-label
# import torch
# import numpy as np

# # data = [[1, 2], [3, 4]]
# # # tensor = torch.FloatTensor(data)  # 转换成32位浮点 tensor
# # # print(
# # #     '\nnumpy:', np.matmul(data, data),  #矩阵乘法
# # #     '\ntorch:', torch.mm(tensor, tensor)  #矩阵乘法
# # # )

# # x_data = torch.tensor(data) #转换成tensor
# # x_ones = torch.ones_like(x_data) #保持x_data的形状，全1
# # x_rand = torch.rand_like(x_data, dtype=torch.float) #保持x_data的形状，随机数
# # print(f"Ones Tensor: \n{x_ones} \n")
# # print(f"Random Tensor: \n{x_rand} \n")

# shape = (2,3,)
# rand_tensor = torch.rand(shape)
# ones_tensor = torch.ones(shape)
# zeros_tensor = torch.zeros(shape)

# print(f"Random Tensor: \n {rand_tensor} \n")
# print(f"Ones Tensor: \n {ones_tensor} \n")
# print(f"Zeros Tensor: \n {zeros_tensor}")

#--------------下为p8variable变量----------------------------------------------
# import torch
# from torch.autograd import Variable #Variable在pytorch0.4.0版本后被弃用
#----------------下为p9.10什么是激励函数-------------------------------------------
# import torch
# import torch.nn.functional as F
# # from torch.autograd import Variable #
# import matplotlib.pyplot as plt #画图
# #以下目的是画出激励函数的图像
# x = torch.linspace(-5, 5, 200)  # x data (tensor), shape=(100, 1)
# x_np = x.data.numpy()   # numpy array for plotting

# y_relu = torch.relu(x).data.numpy() #relu激励函数
# y_sigmoid = torch.sigmoid(x).data.numpy() #sigmoid激励函数 
# y_tanh = torch.tanh(x).data.numpy() #tanh激励函数
# y_softplus = F.softplus(x).data.numpy() #softplus激励函数
 
# plt.figure(1, figsize=(8, 6))
# plt.subplot(221)
# plt.plot(x_np, y_relu, c='red', label='relu')
# plt.ylim((-1, 5))
# plt.legend(loc='best')

# plt.subplot(222)
# plt.plot(x_np, y_sigmoid, c='red', label='sigmoid')
# plt.ylim((-0.2, 1.2))
# plt.legend(loc='best')

# plt.subplot(223)
# plt.plot(x_np, y_tanh, c='red', label='tanh')
# plt.ylim((-1.2, 1.2))
# plt.legend(loc='best')

# plt.subplot(224)
# plt.plot(x_np, y_softplus, c='red', label='softplus')
# plt.ylim((-0.2, 6))
# plt.legend(loc='best')
# plt.show()

#----------------下为p11Regression回归，构建一个神经网络-------------------------------------------
# import torch
# import torch.nn.functional as F
# # from torch.autograd import Variable #这个内容已经包含在上面的torch中
# import matplotlib.pyplot as plt

# x = torch.unsqueeze(torch.linspace(-1, 1, 200), dim=1)  #unsqueeze是增加维度，dim=1是在第二维增加
# y = x.pow(3) + 0.2*torch.rand(x.size())  #torch.rand(x.size())表示生成10行1列的随机数，用于增加噪点
# # plt.scatter(x.data.numpy(), y.data.numpy())
# # plt.show()

# #定义神经网络
# class Net(torch.nn.Module):
#     def __init__(self, n_feature, n_hidden, n_output): #此函数定义了总的输入，隐藏，输出层的神经元个数
#                                                      #第2,3,4个参数分别是输入，隐藏，输出层的神经元个数
#         super(Net,self).__init__()
#         #self.hidden和self.predict是两个全连接层，
#         #第一个参数表示输入样本有几个特征，第二个参数表示输出有几个特征
#         self.hidden = torch.nn.Linear(n_feature, n_hidden) #此行为隐藏层，n_future是输入，n_hidden是输出
#         self.predict = torch.nn.Linear(n_hidden, n_output)#此行为输出层

#     def forward(self, x): #此函数目的是将输入的x通过隐藏层和输出层，最后输出
#         x = F.relu(self.hidden(x)) #x经过隐藏层后，再经过激励函数relu，此句表示隐藏层的输出
#         x = self.predict(x)  #经过激励函数后再经过预测层，此句表示输出层的输出
#         return x 
    
# net = Net(1, 10, 1) #定义神经网络，输入层有1个特征也就是x,隐藏层有10个神经元，输出层有1个神经元
# # print(net)

# plt.ion()  #此句目的是实时打印图像
# plt.show() 

# #优化神经网络,optimizer是torch.optim.SGD的实例也是对像,可以通过optimizer.来调用SGD的方法
# #loss_func同理，torch.optimizer.SGD和torch.nn.MSELoss()都是类，实例化后可以调用类的方法
# optimizer = torch.optim.SGD(net.parameters(), lr=0.5)#优化器，参数是net的所有参数，学习率是0.5
# loss_func = torch.nn.MSELoss() #损失函数，均方差

# for t in range(300): #训练次数
#     prediction = net(x)
#     # print(prediction)

#     loss = loss_func(prediction, y)  # 
    
#     optimizer.zero_grad() #
#     loss.backward() #
#     optimizer.step() #
    
#     if t % 5 ==0:  #表示t是5的倍数时，执行
#         plt.cla()
#         plt.scatter(x.data.numpy(), y.data.numpy())
#         plt.plot(x.data.numpy(), prediction.data.numpy(),'r-', lw=5)
#         plt.text(0.5, 0, 'Loss=%.4f' % loss.data.numpy(), fontdict={'size':20, 'color':'red'})
#         plt.pause(0.1)
    
# plt.ioff()#
# plt.show()
#----------------------------------p12没看懂？p13快速搭建-----------------------------------
import torch
import torch.nn.functional as F
from torch.autograd import Variable #这个内容已经包含在上面的torch中
import matplotlib.pyplot as plt

#以下是生成数据
n_data = torch.ones(100,2) #生成100行2列的1
x0 = torch.normal(2*n_data, 1) #生成100行2列的正态分布，1是标准差,normal表示正态分布
y0 = torch.zeros(100) #生成100个0
x1 = torch.normal(-2*n_data,1) #生成100行2列的正态分布，1是标准差
y1 = torch.ones(100) #生成100个1
x = torch.cat((x0, x1), 0).type(torch.FloatTensor) #cat表示将y0和y1拼接在一起，0表示拼接的方向，type表示转换成FloatTensor 
y = torch.cat((y0, y1), ).type(torch.FloatTensor) #y是100个0和100个1，用来表示点的颜色
# x大小为200行2列，y大小为200行1列

#[;, 0]表示取所有行的第1列，[;, 1]表示取所有行的第2列，第一列为x坐标，第二列为y坐标
#
# plt.scatter(x.data.numpy()[:, 0], x.data.numpy()[:, 1], c=y.data.numpy(), s=100, lw=0, cmap='RdYlGn') #c表示颜色，s表示大小，lw表示线宽，cmap表示颜色映射
# plt.show()

"""如何在运行终端上运行py文件，以便方便查看过程中的参数：cd "这里写py文件的路径"  下一排python -i De5_运行的文件名.pyHey Cortana Hey Cortana Hello. """
#method 1
class Net(torch.nn.Module):
    def __init__(self, n_feature, n_hidden, n_output):
        super(Net,self).__init__()
        self.hidden = torch.nn.Linear(n_feature,n_hidden)
        self.predict = torch.nn.Linear(n_hidden, n_output)
    def forward(self, x): #x是输入的数据
        X = F.relu(self.hidden(x)) #隐藏层的输出到激励函数relu
        X = self.predict(X)
        return X

net1 = Net(2,10,2) #2个特征一个x坐标特征，一个y坐标特征，10个隐藏层神经元，1个输出神经元,注意目的是分类
# print(net1)
#method 2与method1效果一样
net2 = torch.nn.Sequential(
    torch.nn.Linear(2,10),#第一层
    torch.nn.ReLU(),
    torch.nn.Linear(10,2),
)
# print(net2)

plt.ion() #打开交互模式，此模式下在显示图像时，继续执行后面的代码
plt.show()
optimizer = torch.optim.SGD(net1.parameters(),lr=0.02) #lr是学习率
# print("=====", net1.parameters())

loss_func = torch.nn.CrossEntropyLoss() #分类问题使用的CrossEntropyLoss,返回的是概率

for t in range(100):#训练次数
    out = net1(x) #神经网络的输出
    loss = loss_func(out, y.long()) # 损失函数
    optimizer.zero_grad() 
    loss.backward() #将误差反向传播
    optimizer.step()  
    if  t % 2 == 0: 
        plt.cla()
        prediction = torch.max(F.softmax(out), 1)[1]
        pred_y = prediction.data.numpy().squeeze()
        target_y = y.data.numpy()
        plt.scatter(x.data.numpy()[:,0], x.data.numpy()[:,1], c=pred_y, s=100,lw=0,cmap='RdYlGn')
        accuracy = sum(pred_y == target_y) / 200
        plt.text(1.5, -4, 'Accuracy=%.2f' % accuracy, fontdict={'size':20, 'color':'red'})
        plt.pause(0.1)

plt.ioff()
plt.show()






