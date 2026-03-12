# 以下来自pytorch官网自带教程https://pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html
import os
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

# 用于判断使用的设备，这里是的device="cuda"
device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)
# print(f"Using {device} device") 

# input = torch.randn(32, 1, 5, 5)
# 从左到右四个参数分别是batch_size, channel, height, width，实际意义是：
# (样本个数，样本特征数，样本高度，样本宽度)，
# 用图片来解释就是(图片数量，rbg三个通道，图片高度，图片宽度)。

class NeuralNetwork(nn.Module):
    #本函数定义了NN的输入层，隐藏层，输出层
    #输入层：28*28=784个神经元，隐藏层：512个神经元，输出层：10个神经元
    #
    def __init__(self):  
        super(NeuralNetwork, self).__init__()       #
        self.flatten = nn.Flatten()#将数据展平，即将数据从28*28的二维张量转换为784的一维张量
        self.linear_relu_stack = nn.Sequential(   #此函数定义了一个神经网络的结构
            nn.Linear(28*28, 512), #输入层
            nn.ReLU(),
            nn.Linear(512, 512), #隐藏层
            nn.ReLU(),
            nn.Linear(512, 10), #输出层
        )

    def forward(self, x):  #定义前向传播函数
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits  #返回的是logits，即神经网络的输出有10个神经元
    
model = NeuralNetwork().to(device) #对神经网络这类的模型进行实例化，device表示
# print(model)

X = torch.rand(1, 28, 28, device=device) #表示创建一个1*28*28的张量，存储在device上
logits = model(X)
pred_probab = nn.Softmax(dim=1)(logits) #Softmax(dim=1)中的dim=1表示在每个类别的预测值转换为概率值
y_pred = pred_probab.argmax(1) #argmax(1)表示取概率最大的那个类别

# print(f"logits:", logits) #输出的是一个10维的张量，一个表示只有一个样本1
#                           # 0维表示10个神经元的输出,输出的device='cuda:0'表示这个张量存储在第一个GPU上
#                           #输出的这10个值有正有负，无实际解释意义，没看懂？？？

# # "10个类别"是指你的模型试图从10个不同的选项中进行预测。具体的类别取决于你的数据集和你试图解决的问题。
# # 例如，如果你正在训练一个手写数字识别的模型，那么你可能有10个类别，每个类别对应一个数字0-9。在这种情况下，
# # 模型的任务是看一个图像，并预测它是哪个数字。又或者，如果你正在训练一个图像分类器来识别10种不同的动物，
# # 那么你的10个类别可能是"猫"，"狗"，"鸟"，"鱼"等等。
# # 在你的代码中，模型的输出层有10个神经元，这意味着它被设计为从10个不同的类别中进行预测。
# # 每个神经元的输出是模型对相应类别的预测分数。然后，这些分数通过softmax函数转换为概率最高概率的类别被选择为预测的类别
# print(f"logits shape:", logits.shape) #输出为torch.Size([1,10]),表示1个样本的输出有10个神经元
#                                       #10表示样本的类别，这10个神经元表示10个类别的输出
#                                       # print(logits[0, 2]) #输出第三个神经元的输出
# print(f"pred_probab:", pred_probab)
# print(f"Predicted class: {y_pred}")

# ----------------------------------------------------------------------------------------
#3个images，每个image的大小为28*28,将这个图像输入给模型观察隐藏层的输出
input_image = torch.rand(3,28,28) 
flatten = nn.Flatten()  #实例化一个展平层
flat_image = flatten(input_image) #将输入的图像展平
# print(flat_image.size()) #输出为torch.Size([3, 784]),表示3个样本，每个样本有784个特征

#nn.Linear()是一个module，使用权重weights和偏置bias进行线性变换
#也就是y = x*W^T + b，其中x是输入，W是权重，b是偏置
layer1 =nn.Linear(in_features=28*28, out_features=20) #定义一个线性层，输入特征数为28*28，输出特征数为20)
hidden1 = layer1(flat_image) #将输入的图像输入到这个线性层中
# print(hidden1.size()) #输出为torch.Size([3, 20]),表示3个样本，每个样本有20个特征
# print(f"Before RuLu:{hidden1}\n\n") #输出的是三个样本的输出，每个样本有20个特征
hidden2 = nn.ReLU()(hidden1) #将hidden1的输出输入到ReLU激活函数中，
                             #此处的用法是直接调用nn.ReLU()，表示实例化一个ReLU激活函数
# print(f"After ReLU:{hidden2}") #表示经过ReLU激活函数后的输出hidden2

#-----------------------------------------------------------------
#以下内容是将上述的步骤整合到一个Sequential模块中
seq_modules = nn.Sequential(   #此模块是一个有序的容器
    flatten,
    layer1,
    nn.ReLU(),
    nn.Linear(20,10)
)
input_image = torch.rand(3,28,28)
logits = seq_modules(input_image) #将输入的图像输入到这个Sequential模块中
softmax = nn.Softmax(dim=1) #实例化一个softmax函数
pred_probab = softmax(logits)
print(f"Model structure:{model}\n\n")
for name, param in seq_modules.named_parameters(): #没看懂输出的内容？？？
    print(f"Layer:{name} --- Size:{param.size()} --- Values:{param[:2]}\n")




        
