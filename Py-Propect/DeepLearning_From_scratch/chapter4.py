"""此为第四章神经网络的学习的例程程序,2024.7.11-7.17"""
import numpy as np

# #损失函数均方差的实现，mean_squared_error(y,t) y为神经网络的输出，t为监督数据
# #网络的输出与监督数据越接近，均方差越小
# def mean_squared_error(y, t):
#     return 0.5*np.sum( (y-t)**2 )

# #单个数据的交叉熵误差函数的实现,cross_entropy_error(y,t) y为神经网络的输出，t为实际值
# #网络的输出与实际值越接近，交叉熵误差越小
# def cross_entropy_error1(y, t):
#     delta = 1e-7
#     return -np.sum(t*np.log(y + delta))

#-------------------------p89 mini-batch学习，------------------------------
import sys,os
sys.path.append(os.pardir)
from dataset.mnist import load_mnist

(x_train, t_train), (x_test, t_test) = load_mnist(normalize=True, one_hot_label=True)

# print(x_train.shape, x_train.shape)  # (60000, 784)  (60000, 10)
train_size = x_train.shape[0] #训练数据的个数6000
batch_size = 10 #
batch_mask = np.random.choice(train_size, batch_size) #从60000个数据中随机选择10个数据，返回的是一个长度为10的数组，大小在0-59999之间
x_batch = x_train[batch_mask] # 从x_train中选择10个数据

#多个数据的交叉熵函数实现，one—hot形式
def cross_entropy_error2(y, t): #y为神经网络的输出，t为监督数据
    if y.ndim == 1:  #神经网络的输出y的维度为1，也就是求单个数据的交叉熵误差
        y = t.reshape(1, t.size)
        y = y.reshape(1, y.size)
    batch_size = y.shape[0]
    return -np.sum(t*np.log(y+1e-7)) / batch_size  #除batch_size(数据个数)是为了求平均

#多个数据的交叉熵函数实现，非one—hot形式
def cross_entropy_error3(y, t): #y为神经网络的输出，t为监督数据
    if y.ndim == 1:  #神经网络的输出y的维度为1，也就是求单个数据的交叉熵误差
        t = t.reshape(1, t.size) #将t变成一个长度为t.size的一维数组
        y = y.reshape(1, y.size)
    batch_size = y.shape[0]  #y的行数，为数据的个数
    return -np.sum(np.log(y[np.arange(batch_size), t] + 1e-7)) / batch_size  #除batch_size(数据个数)是为了求平均


#---------------------- P96 numerical differentiation ,gradient of function-------------------------
def numerical_diff(f,x):
    h = 1e-5
    return  (f(x+h)-f(x-h)) / (2*h) 

def function_1(x):
    return 0.01*x**2 + 0.1*x   

def function_2(x):
    return x[0]**2 + x[1]**2

# P101 calculate gradient
#don't support arbitrary mrta-functions and arbitrary shapes of x
def numerical_gradient(function,x): #x like [3.0,4.0]
    x = x.astype(float) #change the type of x to float
    delta = 1e-4  
    grad = np.zeros_like(x) 

    for idx in range(x.size):
        tmp_val = x[idx] 
        
        x[idx] = tmp_val + delta
        fxh1 = function(x)
        
        x[idx] = tmp_val - delta
        fxh2 = function(x)

        grad[idx] = (fxh1 - fxh2) / (2*delta)
        x[idx] = tmp_val #

    return grad # return gradient vector，like [6.0,8.0]，the shape of x and grad is the same

# numerical_gradient(function_2,np.array([3.0,4.0]))

# p104 gradient desent method, function represent loss function
def gradient_descent(function, init_x, lr=0.001, step_num=100): #step_num repesent take how many steps to get the minimum value
    x = init_x

    for i in range(step_num):
        grad = numerical_gradient(function, x)
        x -= lr*grad
    return x  #return function's minimum value


#---------------------------------p106神经网络的梯度-----------------------------------------
# import sys, os
# sys.path.append(os.pardir)
# import numpy as np
# from common.functions import softmax, cross_entropy_error
# from common.gradient import numerical_gradient

# class simpleNet:
#     def __init__(self): # property of this class
#         self.W = np.random.randn(2,3) 

#     def predict(self, input):
#         return np.dot(input, self.W)
    
#     def loss(self, input, t): 
#         z = self.predict(input)
#         y = softmax(z)
#         loss = cross_entropy_error(y,t)
#         return loss

# net = simpleNet()
# # print(net.W)
# x0 = np.array([0.6,0.9])
# p = net.predict(x0)
# # print(p)
# t = np.array([0,0,1])
# # print("loss value:", net.loss(x0,t)) # loss value
# def f(W):
#     return net.loss(x0,t)

# dW = numerical_gradient(f, net.W)
# # print("the gradient vector at x0: ",'\n', dW)

#-------------------------p110 Class:TwoLayerNet。p114 mini—batch------------------------------
import sys, os
sys.path.append(os.pardir)
from common.functions import *
from common.gradient import numerical_gradient
from dataset.mnist import load_mnist

class TwoLayerNet:
    def __init__(self, input_size, hidden_size, output_size, weight_init_std=0.01):
        #initialize weights
        self.params = {}
        self.params['W1'] = weight_init_std * np.random.randn(input_size, hidden_size)
        self.params['b1'] = np.zeros(hidden_size)
        self.params['W2'] = weight_init_std * np.random.randn(hidden_size, output_size)
        self.params['b2'] = np.zeros(output_size)

    def predict(self, x):
        W1, W2 = self.params['W1'], self.params['W2']
        b1, b2 = self.params['b1'], self.params['b2']

        a1 = np.dot(x, W1) + b1
        z1 = sigmoid(a1)
        a2 = np.dot(z1, W2) + b2
        y = softmax(a2)
        return y
    
    def loss_function(self, x, t):
        y = self.predict(x)

        return cross_entropy_error(y, t)
    
    def accuracy(self, x, t): #accuracy between predicted value and actual value
        y = self.predict(x)
        y = np.argmax(y, axis=1) 
        t = np.argmax(t, axis=1)
        accuracy = np.sum(y==t) / float(x.shape[0])
        return accuracy
    
    def numerical_gradient(self, x, t):
        loss_W = lambda W: self.loss_function(x, t)

        grads = {}  #storeing gradients of weights and biases
        grads['W1'] = numerical_gradient(loss_W, self.params['W1'])
        grads['b1'] = numerical_gradient(loss_W, self.params['b1'])
        grads['W2'] = numerical_gradient(loss_W, self.params['W2'])
        grads['b2'] = numerical_gradient(loss_W, self.params['b2'])

        return grads
    
    def gradient(self, x, t): #
        W1, W2 = self.params['W1'], self.params['W2']
        b1, b2 = self.params['b1'], self.params['b2']
        grads = {}
        
        batch_num = x.shape[0]
        
        # forward
        a1 = np.dot(x, W1) + b1
        z1 = sigmoid(a1)
        a2 = np.dot(z1, W2) + b2
        y = softmax(a2)
        
        # backward
        dy = (y - t) / batch_num
        grads['W2'] = np.dot(z1.T, dy)
        grads['b2'] = np.sum(dy, axis=0)
        
        dz1 = np.dot(dy, W2.T)
        da1 = sigmoid_grad(a1) * dz1
        grads['W1'] = np.dot(x.T, da1)
        grads['b1'] = np.sum(da1, axis=0)

        return grads
    
# net = TwoLayerNet(input_size=784, hidden_size=100, output_size=10)
# net.params['W1'].shape # (784, 100) indicate 784 input and 100 neurons
# net.params['b1'].shape # (100,)
# net.params['W2'].shape # (100, 10)
# net.params['b2'].shape # (10,)

# (x_train, t_train), (x_test, t_test) = load_mnist(normalize=True, one_hot_label=True)
# train_loss_list = [] #stor loss value

# #hyperparameters
# iter_num = 10000 #updata parameters 10000 times
# train_size = x_train.shape[0] #60000
# batch_size = 100
# learning_rate = 0.1

# network = TwoLayerNet(input_size=784, hidden_size=50, output_size=10)

# for i in range(iter_num):
#     #get mini-batch
#     batch_mask = np.random.choice(train_size, batch_size) #randomly select 100 samples from 60000
#     x_batch = x_train[batch_mask] #
#     t_batch = t_train[batch_mask]

#     #calculate gradient
#     grad = network.gradient(x_batch, t_batch)
#     # grad = network.gradient(x_batch, t_batch) #high-speed version than numerical_gradient
    
#     #update weights and biases
#     for key in ('W1', 'b1', 'W2', 'b2'):
#         network.params[key] -= learning_rate * grad[key]

#     #record learning process
#     loss = network.loss_function(x_batch, t_batch)
#     train_loss_list.append(loss)



#-------------------------p116基于测试数据的评价--------------------------------
import numpy as np
from dataset.mnist import load_mnist
#需要上段的TwoLayerNet类

(x_train, t_train), (x_test, t_test) = load_mnist(normalize=True, one_hot_label=True)

#hyperparameters
iters_num = 10000
train_size = x_train.shape[0] #60000
batch_size = 100
learning_rate = 0.1

train_loss_list = [] #store loss value
train_acc_list = []
test_acc_list = []
#the average number of repeat times of one epoch
iter_per_epoch = max(train_size / batch_size, 1) #return 60000/100=600


network = TwoLayerNet(input_size=784, hidden_size=50, output_size=10)

#optimize network's parameters to minimize loss function and evalute accuracy per epcch(per epoch)
for i in range(iters_num):
    #get mini_batch
    batch_mask = np.random.choice(train_size, batch_size)
    x_batch = x_train[batch_mask]
    t_batch = t_train[batch_mask]
    
    #calculate gradient
    grad = network.gradient(x_batch, t_batch)
    # grad = network.gradient(x_batch, t_batch) #high-speed version than numerical_gradient

    #update weights and biases
    for key in ('W1', 'b1', 'W2', 'b2'):
        network.params[key] -= learning_rate*grad[key]
    
    loss = network.loss_function(x_batch, t_batch)
    train_loss_list.append(loss)

    #calculate accuracy per train_size/batch_size = 600 times
    if i % iter_per_epoch == 0: #0,600,1200,1800...
        train_acc = network.accuracy(x_train, t_train)
        test_acc = network.accuracy(x_test, t_test)
        train_acc_list.append(train_acc)
        test_acc_list.append(test_acc)
        print("trsin acc, test acc |" + str(train_acc) + ", " + str(test_acc))






    



    




