import numpy as np
import struct
import pickle
from sklearn import svm
###用于做数据预处理
from sklearn import preprocessing


##读取数据集
def load_mnist_train(labels_path, images_path):
    with open(labels_path, 'rb') as lbpath:
        magic, n = struct.unpack('>II', lbpath.read(8))
        labels = np.fromfile(lbpath, dtype=np.uint8)
    with open(images_path, 'rb') as imgpath:
        magic, num, rows, cols = struct.unpack('>IIII', imgpath.read(16))
        images = np.fromfile(imgpath, dtype=np.uint8).reshape(len(labels), 784)
    return images, labels


if __name__ == '__main__':
    ##读取训练数据
    labels_path = "C:\\Users\\hp\\Desktop\\ai\\exp2\\data\\train-labels.idx1-ubyte"
    images_path = "C:\\Users\\hp\\Desktop\\ai\\exp2\\data\\train-images.idx3-ubyte"
    train_images, train_labels = load_mnist_train(labels_path, images_path)

    ##标准化
    X = preprocessing.StandardScaler().fit_transform(train_images)
    X_train = X[0:60000]
    y_train = train_labels[0:60000]

    ##定义并训练模型
    model_svc = svm.SVC()
    model_svc.fit(X_train, y_train)
    file = open("model.pickle", "wb")
    ##保存模型
    pickle.dump(model_svc, file)
    file.close()