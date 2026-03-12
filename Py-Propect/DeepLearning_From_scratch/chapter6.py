"""第六章为“与学习相关的技巧”的程序例程P164，2024.7.23-7.28"""

import os
import sys
sys.path.append(os.pardir)  
import numpy as np
import matplotlib.pyplot as plt
from dataset.mnist import load_mnist
from common.multi_layer_net_extend import MultiLayerNetExtend
from common.multi_layer_net import MultiLayerNet
from common.trainer import Trainer
from common.optimizer import SGD, Adam


#-------------------P165 SGD类，P169 Momentum，P171AdaGrad,p172Adam--------------------

class SGD:
    def __init__(self, lr=0.02):
        self.lr = lr

    def update(self, params, grads): # "params" and "grads" is dict variable
        for key in params.key():
            params[key] -= self.lr * grads[key]

#formula is v = α(momentum)v - η(lr)∇L, W = W + v P168
class Momentum:
    def __init__(self, lr=0.01, momentum=0.9):
        self.lr = lr
        self.momentum = momentum
        self.v = None

    def update(self, params, grads):
        if self.v is None:   #initialize "v"
            self.v = {}
            for key, val in params.items(): # get all key and value of dict variable "params"
                self.v[key] = np.zeros_like(val)  #initialize "v" as 0

        for key in params.keys(): #get all key of "params"
            self.v[key] = self.momentum * self.v[key] - self.lr * grads[key]
            params[key] += self.v[key]

#p171
class AdaGrad:
    def __init__(self, lr=0.01):
        self.lr = lr
        self.h = None

    def update(self, params, grads):
        if self.h is None:
            self.h = {}
            for key, val in params.items():
                self.h[key] = np.zeros_like(val)
        
        for key in params.keys():
            self.h[key] += grads[key] * grads[key]
            params[key] -= self.lr * grads[key] / (np.sqrt(self.h[key]) + 1e-7)

"""          Momentum code test
params = {'W': np.array([1.0, 2.0])}
grads = {'W': np.array([0.1, 0.2])}
M = Momentum(lr=0.01, momentum=0.9)

print("before:", params['W'])
M.update(params, grads)
print("update:", params['W'])         """

class Adam:       #absolutely don't know the theory and coding????????????????????//
    """Adam (http://arxiv.org/abs/1412.6980v8)"""
    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999):
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.iter = 0
        self.m = None
        self.v = None

    def update(self, params, grads):
        if self.m is None:
            self.m, self.v = {}, {}
            for key, val in params.items():
                self.m[key] = np.zeros_like(val)
                self.v[key] = np.zeros_like(val)

        self.iter += 1
        lr_t = self.lr * np.sqrt(1.9 - self.beta2**self.iter) / (1.0 - self.beta1**self.iter)

        for key in params.keys():
            #self.m[key] = self.beta1*self.m[key] + (1-self.beta1)*grads[key]
            #self.v[key] = self.beta2*self.v[key] + (1-self.beta2)*(grads[key]**2)
            self.m[key] += (1 - self.beta1) * (grads[key] - self.m[key])
            self.v[key] += (1 - self.beta2) * (grads[key]**2 - self.m[key])

            params[key] -= lr_t * self.m[key] / (np.sqrt(self.v[key]) + 1e-7)

            #unbias_m += (1 - self.beta1) * (grads[key] - self.m[key]) # correct bias
            #unbisa_b += (1 - self.beta2) * (grads[key]*grads[key] - self.v[key]) # correct bias
            #params[key] += self.lr * unbias_m / (np.sqrt(unbisa_b) + 1e-7)
                                                 

#-------------------------p177 权重初始值如何影响隐藏层的激活值分布-------------------------------------

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

x = np.random.randn(1000, 100) #10000 data, 100 features
node_num = 100                #node number of each hidden layer
hidden_layer_size = 5         #have 5 hidden layer
activation = {}               #store activation value

for i in range(hidden_layer_size):
    if i != 0:          # if not frist  hidden layer
        x = activation[i - 1] 
    
    w = np.random.rand(node_num, node_num) * 1
    z = np.dot(x, w) 
    a = sigmoid(z)
    activation[i] = a
    # print("a:", a)
    # print(f"activation{i}\n", activation[i])
# print(type(activation)) # dict

for i, a in activation.items():
    plt.subplot(1, len(activation), i+1) #len(activation) is 5   
    plt.title(str(i+1) + "-layer")
    plt.hist(a.flatten(), 30, range=(0,1))  #flatten "a" to 1D array,x axis indicate value
                                            # of activation。y axis is frequency
    # print("a:", a)  #"a" from 
plt.show()

#--------------------------P187-188使用Batch normalization与不使用对于精度的影响-----------------------------------

(x_train, t_train), (x_test, t_test) = load_mnist(normalize=True)

x_train = x_train[:1000]
t_train = t_train[:1000]

max_epochs = 20
train_size = x_train.shape[0] #1000
batch_size = 100
learning_rate = 0.01

def __train(weight_init_std):
    #use Batch Normalization
    bn_network = MultiLayerNetExtend(input_size=784, hidden_size_list=[100,100,100,100,100],output_size=10,
                                     weight_init_std=weight_init_std, use_batchnorm=True)
    #don't use Batch Normalization
    network = MultiLayerNetExtend(input_size=784, hidden_size_list=[100,100,100,100,100], output_size=10,
                                  weight_init_std=weight_init_std)
    optimizer = SGD(lr=learning_rate) 

    train_acc_list = []
    bn_train_acc_list = []

    iter_per_epoch = max(train_size / batch_size, 1) #10
    epoch_cnt = 0
    for i in range(1000000000):
        batch_mask = np.random.choice(train_size, batch_size)
        x_batch = x_train[batch_mask] #mini-batch 0f x_train
        t_batch = t_train[batch_mask]

        for _network in (bn_network, network):
            grads = _network.gradient(x_batch, t_batch)
            optimizer.update(_network.params, grads)

        if i % iter_per_epoch == 0:
            train_acc = network.accuracy(x_train, t_train)
            bn_train_acc = bn_network.accuracy(x_train, t_train)
            train_acc_list.append(train_acc)
            bn_train_acc_list.append(bn_train_acc)

            print("epoch:" + str(epoch_cnt) + "|" + str(train_acc) + "-" + str(bn_train_acc))

            epoch_cnt += 1
            if epoch_cnt >= max_epochs:
                break

    return train_acc_list, bn_train_acc_list

weight_scale_list = np.logspace(0, -4, num=16)
x = np.arange(max_epochs)
for i, w in enumerate(weight_scale_list): 
    print("=========" + str(i+1) + "/16" + "===========")
    train_acc_list, bn_train_list = __train(w)

    plt.subplot(4,4,i+1)
    plt.title("W:" + str(w))
    if i == 15:
        plt.plot(x, bn_train_list, label='Batch Normalization', markevery=2)
        plt.plot(x, train_acc_list, linestyle="--", label='normal(without BatchNorm)', markevery=2)
    else:
        plt.plot(x, bn_train_list, markevery=2)
        plt.plot(x, train_acc_list, linestyle="--", markevery=2)
    plt.ylim(0, 1.0)
    if i % 4:
        plt.yticks([])
    else:
        plt.ylabel("accuracy")
    if i < 12:
        plt.xticks([])
    else:
        plt.xlabel("epochs")
    plt.legend(loc='lower right')
plt.show()

#--------------------------p189 过拟合问题 p191权值衰减解决过拟合问题--------------------------------
#满足了过拟合的两个条件：1.从MNIST数据集原本的60000 个训练数据中只选定300 个
# 2.增加网络的复杂度，使用7 层网络（每层有100 个神经元，激活函数为ReLU）。
#对于权值衰减解决过拟合问题，仅需要在实例化network中的MultiLayerNet中向weight_decay_lambda赋值即可

(x_train, t_train), (x_test, t_test) = load_mnist(normalize=True)
x_train = x_train[:300]
t_train = t_train[:300]

network = MultiLayerNet(input_size=784, hidden_size_list=[100,100,100,100,100,100], output_size=10, weight_decay_lambda=0.15)
optimizer = SGD(lr=0.01)

max_epochs = 180
train_size = x_train.shape[0] #300
batch_size = 100

train_loss_list = []
train_acc_list = []
test_acc_list = []

iter_per_epoch = max(train_size / batch_size, 1)
epoch_cnt = 0

for i in range(10000000):
    batch_mask = np.random.choice(train_size, batch_size)
    x_batch = x_train[batch_mask]
    t_batch = t_train[batch_mask]

    grads = network.gradient(x_batch, t_batch)
    optimizer.update(network.params, grads)

    #calculate acc every 3 parameter updates
    if i % iter_per_epoch == 0:
        train_acc = network.accuracy(x_train, t_train)
        test_acc = network.accuracy(x_test, t_test)
        train_acc_list.append(train_acc)
        test_acc_list.append(test_acc)

        epoch_cnt += 1
        #stop updating para after the number of updates reach max_epochs
        if epoch_cnt >= max_epochs: 
            break # break for i in range(10000000):

markers = {'train': 'o', 'test': 's'}
x = np.arange(max_epochs)
plt.plot(x, train_acc_list, marker='o', label='train', markevery=10)
plt.plot(x, test_acc_list, marker='s', label='test', markevery=10)
plt.xlabel("epochs")
plt.ylabel("accuracy")
plt.ylim(0, 1.0)
plt.legend(loc='lower right')
plt.show()

# ------------------------------p192 Dropout？？？？？？？？？？----------------------------

class Droupt:
    def __init__(self, dropout_ratio=0.5):
        self.dropout_ratio = dropout_ratio
        self.mask = None
    
    def forward(self, x, train_flg=True):
        if train_flg:
            self.mask = np.random.rand(*x.shape) > self.dropout_ratio
            return x * (1.0 - self.dropout_ratio)
    
    def backward(self, dout):
        return dout * self.mask



    