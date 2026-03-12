#此方法使用计算权重算法一
import numpy as np
import matplotlib.pyplot as plt

# #以下读取训练集文件，缺失值？用0代替，返回特征值和标签
# def load_data(file_path):
#     # 定义两个空列表，用来存储特征数据和标签数据
#     data = []
#     labels = []
#     # 使用with语句打开文件，这样可以确保文件在使用完毕后会被正确关闭
#     with open(file_path, 'r') as file:
#         # 遍历文件中的每一行
#         for line in file:
#             # 去除每一行两端的空白字符（如空格、制表符和换行符）
#             line = line.strip()
#             # 使用split函数将每一行分隔成若干个字符串，这里假设数据文件每行以空格分隔
#             line_data = line.split(' ')
#             # 对于每一行中除了最后一个字符串之外的所有字符串，将其转换为浮点数并添加到data列表中
#             # 如果遇到问号'?'，则用0.0来代替缺失值
#             data.append([float(x) if x != '?' else 0.0 for x in line_data[:-1]])
#             # 对于每一行中的最后一个字符串，将其转换为整数并添加到labels列表中
#             labels.append(int(float(line_data[-1])))
#
#     # 将data和labels列表转换为NumPy数组并返回
#     return np.array(data), np.array(labels)

def load_data(file_path):
    f = open(file_path)
    data = []
    labels = []
    for line in f.readlines():
        currLine = line.strip().split('	')
        lineArr = []
        for i in range(21):
            lineArr.append(float(currLine[i]))
        data.append(lineArr)
        labels.append(float(currLine[21]))
    return np.array(data), np.array(labels)

##------------------training----------------------##
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def logistic(data, labels, num_iterations, learning_rate):#？？？？？？？？？？？？？？？？？？？？？
    num_samples, num_features = data.shape
    # 初始化权重向量
    weights = np.zeros(num_features)
    for i in range(num_iterations):
        # 计算预测值
        predictions = sigmoid(np.dot(data, weights))
        # 计算误差
        error = labels - predictions
        # 根据误差和学习率更新权重
        weights += learning_rate * np.dot(data.T, error)
    return weights

##-------------------test-----------------------##
def predict(data, weights):
    predictions = sigmoid(np.dot(data, weights))
    # 根据预测值确定类别
    return [1 if p >= 0.5 else 0 for p in predictions]

##-------------------vis-------------------------##

def visualize_predictions(predictions, labels):
    fig, ax = plt.subplots()

    # 统计每个类别的数量
    unique_labels = sorted(set(labels))
    pred_counts = [sum(predictions == label) for label in unique_labels]
    true_counts = [sum(labels == label) for label in unique_labels]

    # 设置柱状图位置和宽度
    bar_width = 0.35
    index = np.arange(len(unique_labels))

    # 绘制预测值柱状图
    rects1 = ax.bar(index, pred_counts, bar_width, label='Predictions')
    # 绘制实际值柱状图
    rects2 = ax.bar(index + bar_width, true_counts, bar_width, label='Actual Labels')

    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(unique_labels)
    ax.legend()
    ax.set_xlabel('1,2')
    ax.set_ylabel('Counts')

    # 在每个柱子上标出数值
    for rect1, rect2 in zip(rects1, rects2):
        height1 = rect1.get_height()
        height2 = rect2.get_height()
        ax.annotate(f'{height1}', xy=(rect1.get_x() + rect1.get_width() / 2, height1),
                    xytext=(0, 3), textcoords='offset points', ha='center', va='bottom')
        ax.annotate(f'{height2}', xy=(rect2.get_x() + rect2.get_width() / 2, height2),
                    xytext=(0, 3), textcoords='offset points', ha='center', va='bottom')

    print('预测值： ', pred_counts, '实际值： ', true_counts)
    plt.show()
##    return pred_counts, true_counts
##------------------------------------------------------------------------------------------##
# 主函数
def main():
    # 1. 收集及准备数据
    data, labels = load_data('C:\\Users\\hp\\Desktop\\exp1\\horseColicTraining.txt')
    # 4. 训练算法
    num_iterations = 20000
    learning_rate =0.1
    weights = logistic(data, labels, num_iterations, learning_rate)
    # 5. 测试算法
    data_test, labels_test = load_data('C:\\Users\\hp\\Desktop\\exp1\\horseColicTest.txt')
    predictions = predict(data_test, weights)
    accuracy = np.mean(predictions == labels_test)
    print('权重:', weights)
    print('Accuracy:\t', accuracy)
    print('Prediction:', predictions)
    print('labels_test:', labels_test)
    visualize_predictions(predictions, labels_test)


if __name__ == '__main__':
   main()

