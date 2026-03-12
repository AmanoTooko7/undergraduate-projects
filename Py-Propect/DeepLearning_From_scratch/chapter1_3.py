"""以下来自斋藤康毅DLFromScratch的书中练习题"""
import numpy as np

#P43激活函数(阶跃函数)的实现,返回0或1的数组
def step_function(x):
    y = x > 0  #这里x可以是一个数组，x中大于0的元素返回True，否则返回False，所以y是一个布尔数组
    return y.astype(np.int)
# 以下为sigmoid函数
def sigmoid(x):
    return 1/(1+np.exp(-x))
# 以下为ReLU函数P50
def relu(x):
    return np.maximum(0,x)
# 以下为恒等函数
def identity_function(x):
    return x

#-------------------------P59以下为三层神经网络的实现，A=XW+B的实现,其余两层见p60,61------------------------------
# X, W1, B1 = np.array([1.0, 0.5]), np.array([[0.1, 0.3, 0.5], [0.2, 0.4, 0.6]]), np.array([0.1, 0.2, 0.3])
# print(W1.shape, X.shape, B1.shape) # (2, 3)  # (2,) # (3,)
# A1 = np.dot(X, W1) + B1
# Z1 = sigmoid(A1)  # 第一层的输出,其余两层的实现与此类似，输出为[0.5744, 0.6681, 0.7503]

#以下为实现初始化权重和偏置的代码
# def init_network():
#     network = {}
#     network['W1'] = np.array([ [0.1, 0.3, 0.5],[0.2, 0.4, 0.6] ]) #第一层的权重2行3列，行表示此神经元的权重，列表示此神经元对后层的输出个数
#     network['b1'] = np.array([0.1, 0.2, 0.3])
#     network['W2'] = np.array([ [0.1,0.4], [0.2,0.5], [0.3,0.6] ])
#     network['b2'] = np.array([0.1,0.2])
#     network['W3'] = np.array([ [0.1,0.3], [0.2,0.4] ])
#     network['b3'] = np.array([0.1,0.2])
#     return network

# def forward(network, x):
#     W1, W2, W3 = network['W1'], network['W2'], network['W3']
#     b1, b2, b3 = network['b1'], network['b2'], network['b3']

#     a1 = np.dot(x, W1) + b1
#     z1 = sigmoid(a1)
#     a2 = np.dot(z1, W2) + b2
#     z2 = sigmoid(a2)
#     a3 = np.dot(z2, W3) + b3
#     y = identity_function(a3)
#     return y

# network = init_network() 
# x = np.array([1.0, 0.5])
# y = forward(network, x)
# print(y) #输出[0.31682708 0.69627909]

#下面这个softmax函数有问题，输出值有负数
# def softmax(a): #见数p91,此函数会返回每个神经元的输出，为0~1之间
#     c = np.max(a)
#     exp_a = np.exp(a-c)
#     sum_exp_a = np.sum(a)
#     y = exp_a/sum_exp_a
#     return y

def softmax(x):#返回概率值
    exp_x = np.exp(x - np.max(x))  # 防止数值溢出
    return exp_x / np.sum(exp_x)


#----------------------------------以下为MNIST数据集手写数字识别的实现--------------------------------
# 显示下载的数据形状p71
# import sys, os      
# sys.path.append(os.pardir)
# from dataset.mnist import load_mnist
# (x_train, t_train), (x_test, t_test) = load_mnist(flatten=True, normalize=False)
# print(x_train.shape, t_train.shape, x_test.shape, t_test.shape)#(60000, 784) (60000,) (10000, 784) (10000,)
# print(x_test[0], '========', t_test[0], '========', x_test, '========', t_test)

#显示mnist图像p72,源代码在ch03/mnist_show.py

# def img_show(img):
#     pil_img = Image.fromarray(np.uint8(img))
#     pil_img.show()

# (x_train, t_train), (x_test, t_test) = load_mnist(flatten=True, normalize=False)
# img = x_train[0]
# label = t_train[0]
# print(label, img.shape) # (784,)
# img = img.reshape(28,28)
# img_show(img)

#---------------------------------神经网络的推理处理p73,73,源代码在ch03/neuralnet_mnist.py-----------------------------------
import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
import pickle
from dataset.mnist import load_mnist

def get_data():  # \表示下一行也是这一行的内容
    (x_train, t_train), (x_test, t_test) = \
        load_mnist(normalize=True, flatten=True, one_hot_label=False)
    return x_test, t_test

#读入保存在pickle文件sample_weight.pkl中的学习到的权重参数
def init_network(): 
    with open("C:\\Users\\hp\\Desktop\\project\\Py-Propect\\DeepLearning_From_scratch\\sample_weight.pkl", 'rb') as f:
        network = pickle.load(f)
    return network

def predict(network, x):
    W1, W2, W3 = network['W1'], network['W2'], network['W3']
    b1, b2, b3 = network['b1'], network['b2'], network['b3']
    a1 = np.dot(x, W1) + b1 #第一层的输出
    z1 = sigmoid(a1)
    a2 = np.dot(z1, W2) + b2
    z2 = sigmoid(a2)
    a3 = np.dot(z2, W3) + b3 #此值有负数，为什么？
    # print(a3, '===', '/n')
    y = softmax(a3) #
    # print(y, '===', '/n')
    return y #返回的是一个长度为10的一维数组，表示0~9的概率

x, t = get_data() #这里的x,t分别是(10000,784)的二维数组，和长度为10000的一维数组
network = init_network()
accuarcy_cnt = 0
for i in range(len(x)):
    y = predict(network, x[i]) #x[i]表示一个长度为784的一维数组，为一张图片
                               #这里的y全为负数值，所以下句将argmax改为argmin
    p = np.argmax(y) #获取概率最高的元素的索引
    if p == t[i]: #如果预测的数字和实际的数字相同
        accuarcy_cnt += 1

print("Accuarcy:" + str(float(accuarcy_cnt) / len(x)))

#------------------------------------------以下为批处理的实现p77----------------------------------------------
x, t = get_data()
network = init_network()
batch_size = 100 #批数量
accuarcy_cnt = 0
#每循环一次，i=0,100,200,300,...,10000，取出100张图片进行
for i in range(0, len(x), batch_size):
    x_batch = x[i:i+batch_size] #x_batch是100*784的二维数组
    y_batch = predict(network, x_batch) #y_batch是100*10的二维数组，表示100张图片，每张图片有10个概率结果
    p = np.argmax(y_batch, axis=1) #axis=1表示按行取最大值的索引，返回长度为100的一维数组，表示100张图片的最高预测值索引，，这也表示预测的数字
    accuarcy_cnt += np.sum(p == t[i:i+batch_size]) #p==t[i:i+batch_size]判断预测的数字和实际的数字是否相同，
                                                   # 返回一个布尔数组，True为1，False为0

print(    "Accuracy:" + str(float(accuarcy_cnt) / len(x) )   ) 







