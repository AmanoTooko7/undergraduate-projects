import numpy as np
import struct
import pickle
###用于做数据预处理
from sklearn import preprocessing


def test(images_path, labels_path, modelPath):
    # 读取测试图像
    with open(labels_path, 'rb') as lbpath:
        magic, n = struct.unpack('>II', lbpath.read(8))
        test_labels = np.fromfile(lbpath, dtype=np.uint8)
    with open(images_path, 'rb') as imgpath:
        magic, num, rows, cols = struct.unpack('>IIII', imgpath.read(16))
        test_images = np.fromfile(imgpath, dtype=np.uint8).reshape(len(test_labels), 784)

    ##读取模型
    file = open(modelPath, "rb")
    model_svc = pickle.load(file)
    file.close()

    ##评分并预测
    x = preprocessing.StandardScaler().fit_transform(test_images)
    x_test = x[0:10000]
    y_test = test_labels[0:10000]
    num = model_svc.predict(x_test)
    for i in range(10000):
        print("Real:", y_test[i], "Predict:", num[i])
    print("Accuracy：", model_svc.score(x_test, y_test))
    return num


if __name__ == '__main__':
    images_path = "C:\\Users\\hp\\Desktop\\ai\\exp2\\data\\t10k-images.idx3-ubyte"
    labels_path = "C:\\Users\\hp\\Desktop\\ai\\exp2\\data\\t10k-labels.idx1-ubyte"
    modelPath = "model.pickle"
    num = test(images_path, labels_path, modelPath)