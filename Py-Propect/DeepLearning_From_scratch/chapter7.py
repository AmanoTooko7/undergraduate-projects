""""此章为第七章卷积神经网络p201 2024.7.28-7.31"""
# import  sys, os
# sys.path.append(os.pardir)
# from common.util import im2col, col2im
# import numpy as np

#-----------------p220 im2col4函数的实现，解释见notebook的"零碎编程知识点"部分------------------------------
# x1 = np.random.rand(1,3,7,7)
# col1 = im2col(x1, 5, 5, stride=1, pad=0)
# print(col1.shape) #(9, 75)
# print(col1)

# x2 = np.random.rand(10, 3, 7, 7)
# col2 = im2col(x2, 5, 5, stride=1, pad=0)
# print(col2.shape) #(90, 75)

#---------------------------p220实现Convolution类的正向与反向传播--------------------------
class Convolution:
    def __init__(self, W, b, stride=1, pad=0):
        self.W = W
        self.b = b
        self.stride = stride
        self.pad = pad
    
    def forward(self, x):
        FN, C, FH, FW = self.W.shape #kernal shape
        N, C, H, W = x.shape         #input data
        out_h = int(1 + (H + 2*self.pad - FH) / self.stride)
        out_w = int(1 + (W + 2*self.pad - FW) / self.stride)

        col = im2col(x, FH, FW, self.stride, self.pad) # use im2col to expend input data for fast calculation
        col_W = self.W.reshape(FN, -1).T               # expend kernal for fast calculation
        out = np.dot(col, col_W) + self.b

        # Change output to standard type: (N, FN, OH, OW)
        out = out.reshape(N, out_h, out_w, C).transpose(0, 3, 1, 2)
        return out
    
    def backward(self, dout): #？？？？？？？
        FN, C, FH, FW = self.W.shape
        dout = dout.transpose(0,2,3,1).reshape(-1, FN)

        self.db = np.sum(dout, axis=0)
        self.dW = np.dot(self.col.T, dout)
        self.dW = self.dW.transpose(1, 0).reshape(FN, C, FH, FW)

        dcol = np.dot(dout, self.col_W.T)
        dx = col2im(dcol, self.x.shape, FH, FW, self.stride, self.pad)

        return dx
    

# ----------------------------------p223池化层的实现--------------------------------------
class Pooling:
    def __init__(self, pool_h, pool_w, stride=1, pad=0):
        self.pool_h = pool_h
        self.pool_w = pool_w
        self.stride = stride
        self.pad = pad

    def forward(self, x): #"x" from  the input of activation function
        N, C, H, W = x.shape
        out_h = int(1 + (H - self.pool_h) / self.stride) # Pooling no pad,
        out_w = int(1 + (W - self.pool_w) / self.stride)
        
        #expand
        col = im2col(x, self.pool_h, self.pool_w, self.stride, self.pad)
        col = col.reshape(-1, self.pool_h * self.pool_w)
        #max value
        out = np.max(col, axis=1)
        out = out.reshape(N, out_h, out_w, C).transpose(0, 3, 1, 2)
 
        return out

    def backward(self, dout): #？？？？？？？？？？？
        dout = dout.transpose(0, 2, 3, 1)
        
        pool_size = self.pool_h * self.pool_w
        dmax = np.zeros((dout.size, pool_size))
        dmax[np.arange(self.arg_max.size), self.arg_max.flatten()] = dout.flatten()
        dmax = dmax.reshape(dout.shape + (pool_size,)) 
        
        dcol = dmax.reshape(dmax.shape[0] * dmax.shape[1] * dmax.shape[2], -1)
        dx = col2im(dcol, self.x.shape, self.pool_h, self.pool_w, self.stride, self.pad)
        
        return dx


#--------------------------------------p225 简单CNN的实现与测试------------------------------------------
import sys, os
sys.path.append(os.pardir)  # 
import pickle
import numpy as np
from collections import OrderedDict
from common.layers import *
from common.gradient import numerical_gradient

from dataset.mnist import load_mnist
from common.trainer import Trainer

class SimpleConvNet:
    ''' input_dim=(channel, height,weight),is input data
        "conv_param" correspond Convolution layer
        "hidden_size" correspond two Affine layers both have 100 nodes
        "output_size" indicate last Affine layer have 10 input nodes

        "input_size" is original imput data size =28
        "conv_output_size" is height and width after convolution =23
        "pool_output_size" is total size of the output after the pooling layer
    '''
    def __init__(self, input_dim=(1,28,28), conv_param=
                 {'filter_num':30, 'filter_size':5, 
                'pad':0, 'stride':1}, 
                hidden_size=100, output_size=10, weight_init_std=0.01):
        filter_num = conv_param['filter_num']
        filter_size = conv_param['filter_size']
        filter_pad = conv_param['pad']
        filter_stride = conv_param['stride']
        input_size = input_dim[1] #28
        conv_output_size = (input_size - filter_size + 2*filter_pad) / filter_stride + 1 #23
        pool_output_size = int(filter_num * (conv_output_size/2) * (conv_output_size/2))

        #kernal,weight,bias setting
        self.params = {}
        # 'W1' is the kernal value in the frist layer's convolution part
        self.params['W1'] = weight_init_std * np.random.randn(filter_num,filter_size, filter_size)
        self.params['b1'] = np.zeros(filter_num)
        self.params['W2'] = weight_init_std * np.random.randn(pool_output_size, hidden_size)
        self.params['b2'] = np.zeros(hidden_size)
        self.params['W3'] = weight_init_std * np.random.randn(hidden_size, output_size)
        self.params['b3'] = np.zeros(output_size)
        
        #layers structure setting,"class instantiation"
        self.layers = OrderedDict()
        self.layers['Convl'] = Convolution(self.params['W1'],
                                           self.params['b1'],
                                           conv_param['stride'], 
                                           conv_param['pad'])
        self.layers['ReLu1'] = Relu()
        self.layers['Pool1'] = Pooling(pool_h=2, pool_w=2, stride=2) #pooling Window size
        self.layers['Affine1'] = Affine(self.params['W2'], self.params['b2'])
        self.layers['Relu2'] = Relu()
        self.layers['Affine2'] = Affine(self.params['W3'], self.params['b3'])
        self.lastLayer = SoftmaxWithLoss()

    def predict(self, x):
        for layer in self.layers.values():
            x = layer.forward(x)
        return x
    
    def loss(self, x, t):
        y = self.predict(x)
        return self.lastLayer.forward(y, t)
    
    def gradient(self, x, t):
        #forward
        self.loss(x, t)
        #backward
        dout = 1
        dout = self.lastLayer.backward(dout)
        
        #Extrsct esch layer istance(vslues of self.layers) and combine them into a list
        layers = list(self.layers.values()) 
        layers.reverse()
        for layer in layers:
            dout = layer.backward(dout)
        
        grads = {}
        grads['W1'] = self.layers['Conv1'].dW
        grads['b1'] = self.layers['Conv1'].db
        grads['W2'] = self.layers['Affine1'].dW
        grads['b2'] = self.layers['Affine1'].db
        grads['W3'] = self.layers['Affine2'].dW
        grads['b3'] = self.layers['Affine2'].db
        return grads

#testing code see：C:\Users\hp\Desktop\せいたい\OnlineBooks\斋藤康毅_深度学习_电子书及其代码\deep-learning-from-scratch-master\ch07\train_convnet.py



        
         

