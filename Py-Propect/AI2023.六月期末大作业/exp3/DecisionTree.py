#参考来自https://www.cnblogs.com/codeshell/p/13984334.html

from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.tree import export_graphviz
import graphviz


# ##----------DecisionTreeClassifier 类的构造函数------------##
# def __init__(self, *,
# 	criterion="gini",
#     splitter="best",
#     max_depth=None,
#     min_samples_split=2,
# 	min_samples_leaf=1,
#     min_weight_fraction_leaf=0.,
#     max_features=None,
#     random_state=None,
#     max_leaf_nodes=None,
#     min_impurity_decrease=0.,
#     min_impurity_split=None,
# 	class_weight=None,
#     ccp_alpha=0.0):
#
#
# ##----------DecisionTreeRegressor 类的构造函数------------##
# def __init__(self, *,
# 	  criterion="mse",
#     splitter="best",
#     max_depth=None,
#     min_samples_split=2,
#     min_samples_leaf=1,
#     min_weight_fraction_leaf=0.,
#     max_features=None,
#     random_state=None,
#     max_leaf_nodes=None,
#     min_impurity_decrease=0.,
#     min_impurity_split=None,
#     ccp_alpha=0.0):


##-----------------------构造分类树-------------------------##


iris = load_iris()   	# 准备数据集 
features = iris.data	# 获取特征集
labels = iris.target    # 获取目标集

# Split the dataset into training and testing sets
train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.33, random_state=0)

# Create an instance of DecisionTreeClassifier class
clf = DecisionTreeClassifier(criterion='gini')


##-----------------将数据分成训练集和测试集------------------##
train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.33, random_state=0)


##------------------构建决策树-----------------##
	
# 用CART 算法构建分类树
clf = DecisionTreeClassifier(criterion='gini')

# 用训练集拟合构造CART分类树
clf = clf.fit(train_features, train_labels)
test_predict = clf.predict(test_features)#为预测结果

##----------------------预测结果准确率------------------------##
score = accuracy_score(test_labels, test_predict)
score2 = clf.score(test_features, test_labels)
print(score, score2, "余博文")

##----------------------画决策树------------------------##
# clf 为决策树对象
dot_data = export_graphviz(clf)
graph = graphviz.Source(dot_data)

# 显式指定Graphviz的可执行文件路径
# 使用dot引擎生成决策树的图形
dot_data = export_graphviz(clf, out_file=None, filled=True, rounded=True, special_characters=True)
graph = graphviz.Source(dot_data, engine='dot')
graph.view()
# 生成 Source.gv.pdf 文件，并打开






