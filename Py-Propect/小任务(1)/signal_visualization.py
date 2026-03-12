import os
# import random
import torch
# from sklearn.metrics import confusion_matrix
# import torch.nn as nn
import torch.nn.parallel
import numpy as np
# import torch.backends.cudnn as cudnn
# import torch.optim as optim
import torch.utils.data
# import torchvision.datasets as datasets
# import torchvision.transforms as transforms
# import torchvision.utils as utils
# import torch.nn.functional as F
# from torch.autograd import Variable
# from torch.utils.data import DataLoader
# from torchvision.utils import save_image
import matplotlib.pyplot as plt
# from torchvision.transforms import Compose, CenterCrop, Normalize, ToTensor
# from pytorch_wavelets import DWT1DForward, DWT1DInverse  # or simply DWT1D, IDWT1D
# from glob import glob
# import seaborn as sns
# import pywt
# import matplotlib.animation as animation
# import time
# from sklearn.manifold import TSNE
# For the UCI ML handwritten digits dataset
# from sklearn.datasets import load_digits
# Import matplotlib for plotting graphs ans seabofor attractive graphics.
# import matplotlib.patheffects as pe
# from former.dct_attv14 import Dwctformer


T_acc=[]#训练集准确率
E_acc=[]#测试集准确率
T_loss=[]#训练集损失
E_loss=[]


class CWRU(object):
    def __init__(self, root, batch_size=64, shuffle=True, h_condition: int = 0):

        self.base_dir = root
        self.batch_size =64
        self.shuffle = True
    def load(self):
        x_test_path = os.path.join(self.base_dir, 'test')
        # print("x_test_path: ", x_test_path)

        x_test = torch.load(x_test_path)  # tensor:(300,1,4096)
        # print("x-test: ", x_test)  #datasets.SequenceDatasets.dataset object at 0x000001305A5B5960>
        # print('type: ', type(x_test), '\n'
        #       'len:  ',  len(x_test), '\n'  #len(x_test)==261,261 samples
        #       'dir:  ', dir(x_test), '\n')
        # print('label:', x_test.labels)  #have 261 labels

        print(len(x_test[0]), '\n', '==',   # len(x_test[0]) == 2
               x_test[0], '\n', '==',       #so x_test[0] is a turtle have 2 elements:"array([[ 0.09727357,..., 0.137939 ]]", dtype=float32) and "5"
               len( x_test[0][0][0]))       #length is 1024       

        
        # print(x_test[9][0].shape)
        for i in range(len(x_test)):
            if x_test[i][1]==7:          #choose fault type"7"
                 print(i)
        # print(x_test[40]) # 9正常类型0  14故障类型1  4故障类型2
                            # 10故障类型3(明显)  40故障类型4(明显)   12故障类型5(明显）
                            # 23故障类型6   2故障类型7(明显）  54故障类型8
                            # 17故障类型9(明显)
        x_test = x_test[54][0]
        return x_test



root='C:\\Users\\hp\\Desktop\\小任务(1)\\CWRU_dataset1HP'
cwru = CWRU(root)
test_loader = cwru.load()
#device = torch.device("cuda:0" if (torch.cuda.is_available()) else "cpu")
device = torch.device("cuda:0" if (torch.cuda.is_available()) else "cpu")
# print(torch.cuda.is_available())

input_tensor = test_loader
input_tensor=torch.tensor(input_tensor)


## 绘制相关的波形图
plt.figure(figsize=(6, 2))
plt.margins(x=0)#去除生成图像两边空白
plt.plot(np.reshape(input_tensor, (1, 1024))[0])

plt.savefig('故障类型8ball0db.svg', dpi=600)
plt.savefig('故障类型8ball0db.png', dpi=600)  # 在保存图形时指定dpi值
# plt.show()