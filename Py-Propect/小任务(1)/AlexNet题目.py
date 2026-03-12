import torch.nn as nn
import os
import torch
from sklearn.metrics import confusion_matrix
import torch.nn.parallel
import numpy as np
import torch.utils.data
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
import seaborn as sns
import time 


T_acc=[]#训练集准确率
E_acc=[]#测试集准确率
T_loss=[]#训练集损失
E_loss=[]

#数据集加载类
class CWRU(object):
    def __init__(self, root, batch_size=64, shuffle=True, h_condition: int = 0):

        self.base_dir = root
        self.batch_size =64
        self.shuffle = True
    def load(self):
        x_train_path = os.path.join(self.base_dir,'train')
        x_test_path = os.path.join(self.base_dir,  'test')

        x_train = torch.load(x_train_path)   # tensor:(700,1,4096)
        #print(x_train[1].shape)
        x_test = torch.load(x_test_path)      # tensor:(300,1,4096)
      #  print(x_test[1].shape)

        data_train = DataLoader(x_train,
                                batch_size=self.batch_size,
                                shuffle=self.shuffle,
                                drop_last=True)
        data_test = DataLoader(x_test,
                               batch_size=self.batch_size,
                               shuffle=self.shuffle,
                               drop_last=False)

        return data_train, data_test



root=('C:\\Users\\hp\\Desktop\\project\\Py-Propect\\小任务(1)\\CWRU_dataset1HP')#更换为自己的数据集所在路径
wtg = CWRU(root)
train_loader, test_loader = wtg.load()

#以下为查看数据格式的程序
# print("data attribute：", len(train_loader), '\n',   #len(train_loader) == 16,indicate 16 sets
#                         type(train_loader)         # <class 'torch.utils.data.dataloader.DataLoader'>
#         )

# for i, batch in enumerate(train_loader):   # Output 64 samples of the first set,so "batch" is 64 sampls
#     print(f"batch{i}:", batch)

#     inputs, labels = batch
    
#     print("Inputs:", inputs)  #len(inputs) and len(labels) == 64, len(inputs[0][0])==1024
#     print("Labels:", labels)
#     break



device = torch.device("cuda:0" if (torch.cuda.is_available()) else "cpu")              #选择GPU计算无则选择cpu
# print(torch.cuda.is_available())  # True



class AlexNet(nn.Module):
    """
        "in_channels" is the channel of input data
        "num_classes" is model's classes
        the second param of "nn.Conv1d" defines the number of output channels

    """
    def __init__(self, in_channels=1, num_classes=5):    
        # super(AlexNet, self).__init__()
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv1d(in_channels, 48, kernel_size=11, stride=4, padding=2, bias=False),      #第一层卷积层输入1个数据，输出48个特征
            nn.ReLU(inplace=True),                                                            #ReLU(x) = max(0,x)
            nn.MaxPool1d(kernel_size=3, stride=2),                                            #池化窗口大小为3，步长为2
            nn.Conv1d(48, 128, kernel_size=3, padding=1, bias=False),
            nn.ReLU(inplace=True),
            nn.MaxPool1d(kernel_size=3, stride=2),
            nn.Conv1d(128, 192, kernel_size=3, padding=1, bias=False),
            nn.ReLU(inplace=True),
            nn.Conv1d(192, 192, kernel_size=3, padding=1, bias=False),
            nn.ReLU(inplace=True),
            nn.Conv1d(192, 128, kernel_size=3, padding=1, bias=False),
            nn.ReLU(inplace=True),
            nn.MaxPool1d(kernel_size=3, stride=2),  )
        
        self.avgpool = nn.AdaptiveAvgPool1d(2)          #将输入数据长度池化为指定的长度2，输入为(N,C L_in)输出为(N,C,L_out)，其中L_out为2
        self.flatten = nn.Flatten()                     #展平除了样本数外的所有维度，输入为N,C L_in)输出为(N,C*L_out)
        self.classifier = nn.Sequential(
            nn.Dropout(),                               #通过丢弃一部分展平层后的输出值来抑制过拟合
            nn.Linear(128 * 2, 256),                    #全连接层，输入为128*2个神经元，输出神经元有256个
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(256, 256),
            nn.ReLU(inplace=True),
            nn.Linear(in_features=256 , out_features=10 ),  ) #看这行的in_features和out_features该如何设置
        

    def forward(self, x):           #输入数据为(64*16=1024, 1, 1024)
        out = self.features(x)      #变成(1024, 128, L)
        out = self.avgpool(out)     #变成(1024, 128， 2)
        out = self.flatten(out)     #变成(1024, 128*2)
        out = self.classifier(out)  #变成(1024, 10)
        return out



model = AlexNet().to(device)  #model为AlexNet的实例

loss_func = nn.CrossEntropyLoss()    #自己选择损失函数
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)  #自己选择优化器设置学习率等参数
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='max', factor=0.9, \
            patience=10, threshold=0.0001, threshold_mode='rel', cooldown=0, min_lr=0, eps=1e-08)


losses = []
acces = []
eval_losses = []
eval_acces = []
starttime = time.time()

#训练测试损失绘制函数
def draw_figloss(list1,list2,epoch):
    x1 = range(1, epoch + 1)
    x2 = range(1, epoch + 1)
    y1 = list1
    y2 = list2
    ax = plt.subplot()
    ax.plot(x1, y1, '.-', label='train loss')
    ax.grid()
    ax.plot(x2, y2, '.-', label='test loss')
    plt.grid()
    plt.xlabel('epoch')
    plt.ylabel('loss')
    plt.title("train loss & test loss")
    ax.legend()
    plt.savefig('loss.png')
    plt.show()
accmax=0

#训练测试准确率绘制函数
def draw_figacc(list1,list2,epoch):
    x1 = range(1, epoch + 1)
    x2 = range(1, epoch + 1)
    y1 = list1
    y2 = list2
    ax = plt.subplot()
    ax.plot(x1, y1, '.-', label='train accuracy')
    ax.grid()

    ax.plot(x2, y2, '.-', label='test accuracy')
    ax.grid()
    plt.xlabel('epoch')
    plt.ylabel('accuracy')
    plt.title("train accuracy & test accuracy")
    ax.legend()
    plt.savefig('accuracy.png')
    plt.show()

maxepoch=0
pred1 = []
pred2 = []
pred11=[]
pred22=[]
acc1=0
lables = []
lables2=[]
tmp = []
tmp2 = []

'''
以下代码不用修改仔只需要设置自己认为合理的迭代(epoch)次数即可,如何自己设置了学习策略(scheduler)需要自行在对应位置添加
'''

all_epochs = 200
for epoch in range(all_epochs):    #每循环一次所有数据就训练完一遍，每运行一个epoch前数据会被打乱一次吗？？？
    train_loss = 0          #损失函数值
    train_acc = 0           #训练精度
    i=epoch
    model.train()           #model为AlexNet的实例化，使用.train()会将模型切换到训练模式
    for img, label in train_loader:         
        img = img.float()
        img = img.to(device)
        label = label.to(device)
        label = label.long()
        out = model(img)                     #输入数据到模型，进行前向传播
        out = torch.squeeze(out).float()     #将模型的输出数据(1024,1,10)变成(1024,10)此操作并不会改变
        loss = loss_func(out, label)
        optimizer.zero_grad()                #前一批数据的梯度会累加而不会覆盖，所以要清除前一批数据的梯度
        loss.backward()                      #利用当前损失值通过反向传播计算梯度值
        optimizer.step()                     #利用当前优化器更新参数

        train_loss += loss.item()            #计算得到所有批次损失值叠加
        # 学习率更新
        # scheduler.step(train_acc / 16)
        
        # 计算分类的准确率
        _, pred = out.max(1)                            #pred为每一行最大值索引，也就相当于预测结果

        num_correct = (pred == label).sum().item()      # 
        acc = num_correct / img.shape[0]                #预测正确的样本占这一批次总样本(64个样本)的占比
        train_acc += acc                                #每个批次训练精度的<<累计值>>

    losses.append(train_loss / len(train_loader))       #每个epoch平均损失函数值，是列表
    acces.append(train_acc / len(train_loader))         #每个epoch的平均训练精度，是列表

    eval_loss = 0
    eval_acc = 0                                      
    model.eval()                                        # 将模型改为预测模式
    for img, label in test_loader:
        img = img.type(torch.FloatTensor)               #将img转化为32位浮点数类型
        img = img.to(device)
        label = label.to(device)
        label = label.long()                            #label为tensor长整型

        out = model(img)

        out1 = torch.squeeze(out).float()               #
        loss = loss_func(out1, label)
        # 记录误差
        eval_loss += loss.item()                        #每一批数据的损失值<<累计值>>，标量
        # 记录准确率
        _, pred = out1.max(1)
        num_correct = (pred == label).sum().item()
        acc = num_correct / img.shape[0]
        eval_acc += acc                                 #每一批数据的精度<<累计值>>，标量
        # 降维可视化
        out = out.cpu().detach().numpy()                #out是模型输出量转到cpu处理
        label1 = np.array([int(i) for i in label])      #label1是label中每个元素转化为整型后转化为array数组
        for i in label1:
            # label1=i
            lables.append(i)                            #labels是是有标签数据构成的整数列表，其中一个批次数据
        for i in out:
            tmp.append(i)                               #tmp是由模型输出构成的列表，其中一个批次数据
        out = torch.tensor(out)
        out = out.to(device)

        pred1.extend(pred.cpu().numpy())                #pred1为<<累加>>每一批数据的模型预测结果
        pred2.extend(label.cpu().numpy())               #pred2为<<累加>>每一批数据的真实标签
    
    #出for后，以下所有变量的对象就是当前epoch中的<<所有样本>>--------------------------------------------------------------------------

    lables2.append(lables)                              #lables2<<累加>>每一个epoch中所有批次标签数据的集合
    tmp2.append(tmp)                                    #tmp2保存了每一个epoch中最后一批的模型输出结果
    lables = []
    tmp = []
    pred11.append(pred1)                                #pred11为所有批次预测结果
    pred22.append(pred2)                                #pred22为所有批次标签
    pred1 = []
    pred2 = []

    #eval_loss, eval_acc分别为当前批次的损失值, 精度值
    eval_losses.append(eval_loss / len(test_loader))    #eval_losses为列表，每个元素代表每一个epoch平均损失值
    eval_acces.append(eval_acc / len(test_loader))      #eval_acces为列表，每个元素代表每一个epoch平均损精度

    if (eval_acc / len(test_loader))>accmax:            #如果当前epoch每个样本的平均精度 > 前一个epoch每个样本的平均精度
        maxepoch = epoch                                #所有epoch中的最大测试精度的epoch
        accmax = (eval_acc / len(test_loader))          #前一个epoch每个样本的平均精度


    #输出分别为：最大准确率的epoch(迭代次数)，当前批次的平均损失值，当前批次的训练精度，当前批次测试集损失值，当前批次测试精度
    print('epoch: {}, Train Loss: {:.4f}, Train Acc: {:.4f}, Test Loss: {:.4f}, Test Acc: {:.4f}'  #
          .format(epoch, train_loss / len(train_loader), train_acc / len(train_loader),
                  eval_loss / len(test_loader), eval_acc / len(test_loader)))
    print("\n")

    T_acc.append(train_acc / len(train_loader))         #T_acc  为每个epoch平均训练精度值，是列表，来自模型训练的值(train_loader)
    T_loss.append(train_loss / len(train_loader))       #T_loss 为每个epoch平均损失函数值，是列表，来自模型训练的值(train_loader)
    E_acc.append(eval_acc / len(test_loader))           #E_acc  为每个元素代表每一个epoch平均损精度，列表，来自模型评估的值(test_loader)
    E_loss.append(eval_loss / len(test_loader))         #E_loss 为每个元素代表每一个epoch平均损失值，列表，来自模型评估的值(test_loader)

print("labels2：",lables2[maxepoch])                      #输出最大准确率的标签值
print("max",maxepoch)                                   #输出所有epoch中的最大测试精度的epoch

endtime = time.time()
dtime = endtime - starttime
print("running time：%.8s s" % dtime)
print("accmax:{}" .format( accmax))
torch.save(model.state_dict(), 'formermodel.pt')        #将模型参数保存在formermodel.pt文件中

import pandas as pd
pd.set_option('display.max_columns', None)   #显示完整的列
pd.set_option('display.max_rows', None)  #显示完整的行



#绘制混淆矩阵
conf_matrix = confusion_matrix(pred22[maxepoch], pred11[maxepoch])          #在最优epoch计算模型的真实标签(y)和预测标签的混淆矩阵(x)

plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', cbar=False)     #可视化混淆矩阵，对矩阵着色
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix')
# 计算分类精度和类的数目
class_accuracy = np.diag(conf_matrix) / conf_matrix.sum(axis=1)             #每一类的精度，共10类别
class_counts = conf_matrix.sum(axis=1)                                      #这个变量表示的是每一类的真实标签个数（混淆矩阵行相加）
# 添加分类精度和类的数目到图的右边
ax = plt.gca()                                                              #获取当前的二维Axes对象

for i in range(len(class_accuracy)):    #等同于range(10)
    #ax.text(x, y, text, ha, va)：在坐标 (x, y) 处绘制 text 文本，ha 和 va 分别表示水平对齐和垂直对齐方式
    
    ax.text(len(class_accuracy) + 0.5, i + 0.5, f"{class_accuracy[i] * 100:.2f}%", ha='center', va='center')  #显示百分比
    ax.text(len(class_accuracy) + 0.5, -0.2, 'Accuracy', ha='center', va='center', fontweight='bold')         #显示Accuracy

    # 添加类的数目并将标题放在精度和类别数的上方
    ax.text(len(class_accuracy) + 1.5, i + 0.5, f"{class_counts[i]}", ha='center', va='center')               #显示右侧每个类别标签个数
    ax.text(len(class_accuracy) + 1.5, -0.2, 'Counts', ha='center', va='center', fontweight='bold')           #显示Count

# 调整图的布局
plt.tight_layout()
plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
plt.show()


draw_figloss(T_loss, E_loss, epoch=all_epochs)        #回传每个epoch的训练损失值，每个epoch测试损失值(均为列表)
draw_figacc(T_acc, E_acc, epoch=all_epochs)           #回传每个epoch的训练精度， 每个epoch的测试精度(均为列表)

