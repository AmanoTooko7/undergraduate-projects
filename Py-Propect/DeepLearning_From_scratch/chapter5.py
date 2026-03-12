"""此章为第五章误差反向传播法的程序例程P121，2024.7.17-2024.7.22"""
import numpy as np
#----------------------P135乘法层的实现,p137加法层的实现---------------------
class MulLayer:
    def __init__(self):
        self.x = None
        self.y = None
    
    def forward(self, input_1, input_2):
        self.x = input_1
        self.y = input_2
        out = input_1 * input_2
        return out
    
    def backward(self, dout): # dout is derivative of output
        dx = dout * self.y
        dy = dout * self.x
        return dx, dy


# 实现购买两个苹果P136-------------------------
# apple = 100
# appleNum = 2
# tax = 1.1 

# #layer 
# mul_apple_layer = MulLayer() #
# mul_tax_layer = MulLayer()

# #forward,through two layers.see P136
# apple_price = mul_apple_layer.forward(apple, appleNum) #200，self.x=100  self.y=2
# price = mul_tax_layer.forward(apple_price, tax) #200*1.1=220   self.x=200  self.y=1.1
# # print(price) #220

# #backward
# dprice = 1
# dapple_price, dtax = mul_tax_layer.backward(dprice) #x=200,y=1.1,dapple_price = 1.1
# dapple, dappleNum = mul_apple_layer.backward(dapple_price) #dapple=2.2,dappleNum=110
# print (dapple, dappleNum, dtax) #2.2 110 200

#加法层的实现
class AddLayer:
    def __init__(self):
        pass

    def forward(self, x, y):
        out = x + y
        return out
    
    def backward(self, dout):
        dx = dout * 1
        dy = dout * 1
        return dx, dy
    

# #实现购买2个苹果和3个橘子P138---------------------
# apple = 100
# apple_num = 2
# orange = 150
# orange_num = 3
# tax = 1.1

# #the number of instances of the add and mul classes depends on  nodes 
# mul_apple_layer = MulLayer()
# mul_orange_layer = MulLayer()
# add_apple_orange_layer = AddLayer()
# mul_tax_layer = MulLayer()

# #forward
# apple_price = mul_apple_layer.forward(apple, apple_num)
# orange_price = mul_orange_layer.forward(orange, orange_num)
# all_price = add_apple_orange_layer.forward(apple_price, orange_price)
# price = mul_tax_layer.forward(all_price, tax)

# #backward
# deprice = 1
# dall_price, dtax = mul_tax_layer.backward(deprice)
# dapple_price, dorange_price = add_apple_orange_layer.backward(dall_price)
# dorage, dorange_num = mul_orange_layer.backward(dorange_price)
# dapple, dapple_num = mul_apple_layer.backward(dapple_price)

# print(price) #715
# print(dapple, dorage, dorange_num, dtax) #2.2  3.3  165  650


#-----------------------P140ReLU层的实现,P144Sigmoid的实现--------------------------------
 #refer to p140 fig.5-18
class ReLU:
    def __init__(self):
        self.mask = None

    def forward(self, x):
        self.mask = (x <= 0) #mask is boolean array
        out = x.copy() # 
        out[self.mask] = 0
        return out
    
    def backward(self, dout):
        dout[self.mask] = 0
        dx = dout
        return dx
    
 #refer to p144 fig.5-22
class Sigmoid:
    def __init__(self):
        self.out = None

    def forward(self, x):
        out = 1 / (1 + np.exp(-x))
        self.out = out
        return out
    
    def backward(self, dout):
        dx = dout*(1 - self.out)*self.out
        return dx
    

#---------------------p150 Affine的实现,p153 Softmax_With_Loss实现----------------------
# implement Y = xW + b. #refer to p148 fig.148
class Affine: 
    def __init__(self, W, b):
        self.W = W
        self.b = b
        self.x = None
        self.dW = None
        self.db = None

    def forward(self, x):
        self.x = x
        out = np.dot(x, self.W) + self.b
        return out
    
    def backward(self, dout): #refer to P147 fig.5-25
        dx = np.dot(dout, self.W.T)
        self.dW = np.dot(self.x.t, dout)
        self.db = np.sum(dout, axis=0)
        return dx

def softmax(x):#return probability
    exp_x = np.exp(x - np.max(x))  # 防止数值溢出
    return exp_x / np.sum(exp_x)

def cross_entropy_error(y, t): #y为神经网络的输出，t为监督数据
    if y.ndim == 1:  #神经网络的输出y的维度为1，也就是求单个数据的交叉熵误差
        y = t.reshape(1, t.size)
        y = y.reshape(1, y.size)
    batch_size = y.shape[0]
    return -np.sum(t*np.log(y+1e-7)) / batch_size  #除batch_size(数据个数)是为了求平均

#refer to fig.5-30 P152
class SoftmaxWithLoss:
    def __init__(self):
        self.loss = None # 
        self.y = None    # output of Softmax
        self.t = None    #supervised data (one-hot)

    def forward(self, x, t):
        self.t = t
        self.y = softmax(x)
        self.loss = cross_entropy_error(self.y, self.t)
        return self.loss
    
    def backward(self, dout=1):
        batch_size = self.t.shape[0] # 
        dx = (self.y - self.t) / batch_size # / batch_size is single data's error
        return dx # return difference between entire network's output and supervised data called "dout"
    

#-----------------------------------P156 TwoLayerNet实现------------------------------------------
import sys, os
sys.path.append(os.pardir)
import numpy as np
from common.layers import *
from common.gradient import numerical_gradient
from collections import OrderedDict

class TwoLayerNet: #refer to P150 fig.5-28
    """the structure of the network is Affine1->ReLU1->Affine2->SoftmaxWithLoss
    for MINIST dataset, input_size=784, hidden_size=50, output_size=10"""
    def __init__(self, input_size, hidden_size, output_size, weight_init_std=0.01):
        self.params = {}
        self.params['W1'] = weight_init_std * np.random.rand(input_size, hidden_size)
        self.params['b1'] = np.zeros(hidden_size)
        self.params['W2'] = weight_init_std * np.random.rand(hidden_size, output_size)
        self.params['b2'] = np.zeros(output_size)

        #building layers
        self.layers = OrderedDict() # it's oredered dictionary
        self.layers['Affine1'] = Affine(self.params['W1'], self.params['b1']) #instance of Affine1
        self.layers['ReLU1'] = ReLU()
        self.layers['Affine2'] = Affine(self.params['W2'], self.params['b2'])

        self.lastLayer = SoftmaxWithLoss() # forward will return loss

    def predict(self, x): # 
        for layer in self.layers.values(): # iterate through each layers(Affine1,ReLU1，Affine2) to cal output
            x = layer.forward(x)
        return x
    
    #x:input data, t:supervised data
    def loss(self, x, t):
        y = self.predict(x) #y is output of Affine2
        return self.lastLayer.forward(y, t) # return output of entire network's loss
    
    def accuracy(self, x, t):
        y = self.predict(x)
        y = np.argmax(y, axis=1)

        #this judgement apply one-dimension array like[1,3,5,9,3...] and one-hot
        #when t is one-hot,implement t=np.argmax(t, axis=1) convert it to one-dimension array
        if t.ndim != 1 : t = np.argmax(t, axis=1) 
        accuracy = np.sum(y == t) / float(x.shape[0])
        return accuracy
    
    #
    def cal_numerical_gradient(self, x, t):
        loss_W = lambda W: self.loss(x, t) # W isn't used there,jsut a placeholder
        grads = {}
        grads['W1'] = numerical_gradient(loss_W, self.params['W1'])
        grads['b1'] = numerical_gradient(loss_W, self.params['b1'])
        grads['W2'] = numerical_gradient(loss_W, self.params['W2'])
        grads['b2'] = numerical_gradient(loss_W, self.params['b2'])
        return grads
    
    def gradient(self, x, t): # Gradients are the results of backpropagation
        #forward
        self.loss(x, t)
        #backward
        dout = 1
        dout = self.lastLayer.backward(dout) #net's output "y" - label data "t"

        layers = list(self.layers.values())  #layers = ['Affine1','ReLU1','Affine2'] 
        layers.reverse()                     #layers = ['Affine2','ReLU1','Affine1']
        # print(layers)
        for layer in layers: # each layer is instance
            dout = layer.backward(dout)
        
        #after the for loop over each layer
        # save the values of dW,db through class Affine backward
        grads = {}
        grads['W1'] = self.layers['Affine1'].dW # @class Affine-backward
        grads['b1'] = self.layers['Affine1'].db
        grads['W2'] = self.layers['Affine2'].dW
        grads['b2'] = self.layers['Affine2'].db
        return grads

#----------------------------------P158梯度确认---------------------------------------
# import sys, os
# sys.path.append(os.pardir)
# import numpy as np
# from dataset.mnist import load_mnist

# (x_train, t_train), (x_test, t_test) =load_mnist(normalize=True, one_hot_label=True)
# network = TwoLayerNet(784, 50, 10)

# x_batch = x_train[:3]
# t_batch = t_train[:3]

# grad_numerical = network.cal_numerical_gradient(x_batch, t_batch)
# grad_backprop = network.gradient(x_batch, t_batch)

# #求各个权重的绝对误差的平均值
# for key in grad_numerical.keys():
#     print("key: ", key) #key is W1,b1,W2,b2
#     diff = np.average( np.abs(grad_backprop[key] - grad_numerical[key]) )
#     print(key + ":" + str(diff))

#-----------------------p160使用误差反向传播法的学习---------------------------
import sys, os
sys.path.append(os.pardir)
import numpy as np
from dataset.mnist import load_mnist

(x_train, t_train), (x_test, t_test) =load_mnist(normalize=True, one_hot_label=True)
network = TwoLayerNet(input_size=784, hidden_size=50, output_size=10)

iters_num = 10000 
train_size = x_train.shape[0] #60000
batch_size = 100
lr = 0.1
train_loss_list = []
train_acc_list = []
test_acc_list = []

before_data = np.copy(network.params['W1'])
print("before_data_id:", id(before_data))
# print("network.params['W1']: \n", network.params['W1'][:5, :5])



iter_per_epoch = max(train_size / batch_size, 1) #return 60000/100=600
for i in range(iters_num):
    # get mini-batch
    batch_mask = np.random.choice(train_size, batch_size) #randomly select 100 samples from 60000
    x_batch = x_train[batch_mask] # a mini-batch of x_-train
    t_batch = t_train[batch_mask]

    grad = network.gradient(x_batch, t_batch)
    # print("grad: ", grad)
    #update
    for key in ('W1', 'b1', 'W2', 'b2'):
        # print('network.params[key] = ', network.params[key])
        network.params[key] -= lr * grad[key]  #the type ofoutput:[-0.71963096 0.89747031 -0.36864599 -0.41066712 0.27672346 0.44393905 -0.14344078  0.38767803 -0.57101702  0.20759102]
    
    loss = network.loss(x_batch, t_batch)
    train_loss_list.append(loss)

    if i % iter_per_epoch == 0:#i == 0,600,1200,1800...
        train_acc = network.accuracy(x_train, t_train)#
        test_acc = network.accuracy(x_test, t_test) #
        train_acc_list.append(train_acc)
        test_acc_list.append(test_acc)

        print("trsin acc, test acc |" + str(train_acc) + ", " + str(test_acc))

# print(network.params['W1'].shape,'-',network.params['b1'].shape,'-',network.params['W2'].shape,'-',network.params['b2'].shape)
# (784, 50) - (50,) - (50, 10) - (10,)
# print(grad['W1'].shape,'-',grad['b1'].shape,'-',grad['W2'].shape,'-',grad['b2'].shape)
# (784, 50)  (50,)  (50, 10)  (10,)

# print("After_network.params['W1']: \n", network.params['W1'][:5, :50])

after_data = network.params['W1']
print("after_data_id:", id(after_data))

# compare
if (before_data == after_data).all(): print("same") 
else: print("deffenent") # diffenent



#两个问题1：查看参数更新前后是否值相同。相同
#2：看network.params[key] -= lr * grad[key]是怎样运算的。










        


