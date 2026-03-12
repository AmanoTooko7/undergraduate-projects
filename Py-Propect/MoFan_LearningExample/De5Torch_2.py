# #接上De5Torch_1.py，此文件p14保存提取这一节开始
#---------------------------------p14保存提取，看不懂？？？-------------------------------------#
# import torch
# from torch.autograd import Variable
# import matplotlib.pyplot as plt

# torch.manual_seed(1) #

# #fake data
# x = torch.unsqueeze( torch.linspace(-1,1,100), dim=1 ) #生成-1到1的100个点列向量
# y = x.pow(2) + 0.2*torch.rand(x.size()) #y=x^2+0.2*随机数

# #将数据保存为pkl文件
# def save():
#     net1 = torch.nn.Sequential(
#         torch.nn.Linear(1,10),
#         torch.nn.ReLU(),
#         torch.nn.Linear(10,1)
#     )
#     optimizer = torch.optim.SGD(net1.parameters(), lr=0.5)
#     loss_func = torch.nn.MSELoss()
#     for t in range(100):
#         prediction = net1(x)
#         loss = loss_func(prediction, y)
#         optimizer.zero_grad()
#         loss.backward()
#         optimizer.step()
    
#     torch.save(net1, 'net_ForDe5Torch_2.pkl')                   #保存整个网络
#     torch.save(net1.state_dict(), 'netParams_ForDe5_pytorch_2.pkl') #只保存网络中的参数

#     plt.figure(1, figsize=(10,3))
#     plt.subplot(131)
#     plt.title('Net1')
#     plt.scatter(x.data.numpy(), y.data.numpy())
#     plt.plot(x.data.numpy(), prediction.data.numpy(), 'r-', lw=5)

# def restore_net(): #提取整个网络
#     net2 = torch.load('net_ForDe5Torch_2.pkl')
#     #画图
#     plt.subplot(132)
#     plt.title('Net2')
#     plt.scatter(x.data.numpy(), y.data.numpy())
#     plt.plot(x.data.numpy(), net2(x).data.numpy(), 'r-', lw=5)

# def restore_params(): #提取网络中的参数,需要先定义一个相同的网络
#     net3 = torch.nn.Sequential(
#         torch.nn.Linear(1,10),
#         torch.nn.ReLU(),
#         torch.nn.Linear(10,1)
#     )
#     net3.load_state_dict(torch.load('netParams_ForDe5_pytorch_2.pkl'))

#     #画图
#     plt.subplot(133)
#     plt.title('Net3')
#     plt.scatter(x.data.numpy(), y.data.numpy())
#     plt.plot(x.data.numpy(), net3(x).data.numpy(), 'r-', lw=5)
#     plt.show()

# save()#保存net1
# restore_net()#提取整个网络
# restore_params()#提取网络中的参数

#---------------------------------p15批数据训练,不懂？？？-------------------------------------#
import torch
import torch.utils.data as Data

BATCH_SIZE = 8 #批训练的数据个数
x = torch.linspace(1,10,10) #输入的10个数据
y = torch.linspace(10,1,10) #输出的10个数据

torch_dataset = Data.TensorDataset(x, y) #
loader = Data.DataLoader(
    dataset=torch_dataset,  
    batch_size=BATCH_SIZE,
    shuffle=False,           #打乱数据进行训练
    num_workers=2           #使用两个线程进行数据读取
)
def show_batch():
    for epoch in range(3):
        for step, (batch_x, batch_y) in enumerate(loader):
            #训练数据
            print('epoch:', epoch, '|Step:', step, '|batch x:', 
                    batch_x.numpy(), '|batch y:', batch_y.numpy())

if __name__ == '__main__':
    show_batch()






