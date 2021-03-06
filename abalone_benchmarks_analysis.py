import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from diff_plt import diff_hist
import os
from tqdm import tqdm
from sklearn.model_selection import train_test_split

import warnings
warnings.filterwarnings("ignore")

path = "./数据挖掘互评作业四数据集/abalone_benchmarks/abalone/benchmarks"

file_list = []

for _ in os.listdir(path):
    file_list.append(path + '/' + _)


"""
#这段代码用来提取所有csv文件中的公共列，结果如下，比较耗时，故将其注释，如需要可解除注释

#公共列为： ['ground.truth', 'V2', 'diff.score', 'original.label', 'motherset', 'V1', 'origin', 'V4', 'V3', 'V7', 'V5', 'V6']

def extra_same_elem(list1, list2):          #这个函数用于提取两个列表的共同元素
    set1 = set(list1)
    set2 = set(list2)
    iset = set1.intersection(set2)
    return list(iset)

list1 = pd.read_csv(file_list[0], index_col=0).columns

print("提取所有csv文件中的公共列：")
for file in tqdm(file_list[1:]):
    list2 = pd.read_csv(file, index_col=0).columns
    list1 = extra_same_elem(list1, list2)

print("公共列为：", list1)

columns = list1
"""

columns = ['V2', 'diff.score', 'original.label', 'V1', 'V4', 'V3', 'V7', 'V5', 'V6']

from pyod.models.knn import KNN   # imprt kNN分类器
from pyod.models.lof import LOF
from pyod.models.pca import PCA
from pyod.models.iforest import IForest


from pyod.utils.data import evaluate_print
from sklearn.metrics import roc_auc_score
from sklearn.utils import column_or_1d
from sklearn.utils import check_consistent_length

from pyod.utils.utility import precision_n_scores

knn_roc = []
knn_prn = []
lof_roc = []
lof_prn = []
pca_roc = []
pca_prn = []
iforest_roc = []
iforest_prn = []

for file in file_list:
    try:
        print(file)
        data = pd.read_csv(file, index_col=0)
        #data = data[data['ground.truth'] == 'nominal']
        #data = data[columns]
        data_len = len(data)
        data.loc[data['ground.truth'] == 'anomaly','ground.truth'] = 1
        data.loc[data['ground.truth'] == 'nominal','ground.truth'] = 0


        x = data[columns]
        y = data['ground.truth']
        #print(x)
        #print(y)


        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=1)

        clf_name = 'KNN'
        clf = KNN()  # 初始化检测器clf
        clf.fit(X_train)  # 使用X_train训练检测器clf

        # 返回训练数据X_train上的异常标签和异常分值
        y_train_pred = clf.labels_  # 返回训练数据上的分类标签 (0: 正常值, 1: 异常值)
        y_train_scores = clf.decision_scores_  # 返回训练数据上的异常值 (分值越大越异常)
        print("On train Data:")
        evaluate_print(clf_name, y_train, y_train_scores)

        # 用训练好的clf来预测未知数据中的异常值
        y_test_pred = clf.predict(X_test)  # 返回未知数据上的分类标签 (0: 正常值, 1: 异常值)
        y_test_scores = clf.decision_function(X_test)  # 返回未知数据上的异常值 (分值越大越异常)
        print("On Test Data:")
        evaluate_print(clf_name, y_test, y_test_scores)

        y_true = column_or_1d(y_test)
        y_pred = column_or_1d(y_test_scores)
        check_consistent_length(y_true, y_pred)

        roc = np.round(roc_auc_score(y_true, y_pred), decimals=4),
        prn = np.round(precision_n_scores(y_true, y_pred), decimals=4)
        knn_roc.append(roc)
        knn_prn.append(prn)


        clf_name = 'LOF'
        clf = LOF()  # 初始化检测器clf
        clf.fit(X_train)  # 使用X_train训练检测器clf

        # 返回训练数据X_train上的异常标签和异常分值
        y_train_pred = clf.labels_  # 返回训练数据上的分类标签 (0: 正常值, 1: 异常值)
        y_train_scores = clf.decision_scores_  # 返回训练数据上的异常值 (分值越大越异常)
        print("On train Data:")
        evaluate_print(clf_name, y_train, y_train_scores)

        # 用训练好的clf来预测未知数据中的异常值
        y_test_pred = clf.predict(X_test)  # 返回未知数据上的分类标签 (0: 正常值, 1: 异常值)
        y_test_scores = clf.decision_function(X_test)  # 返回未知数据上的异常值 (分值越大越异常)
        print("On Test Data:")
        evaluate_print(clf_name, y_test, y_test_scores)

        y_true = column_or_1d(y_test)
        y_pred = column_or_1d(y_test_scores)
        check_consistent_length(y_true, y_pred)

        roc = np.round(roc_auc_score(y_true, y_pred), decimals=4),
        prn = np.round(precision_n_scores(y_true, y_pred), decimals=4)
        lof_roc.append(roc)
        lof_prn.append(prn)

        clf_name = 'PCA'
        clf = PCA()  # 初始化检测器clf
        clf.fit(X_train)  # 使用X_train训练检测器clf

        # 返回训练数据X_train上的异常标签和异常分值
        y_train_pred = clf.labels_  # 返回训练数据上的分类标签 (0: 正常值, 1: 异常值)
        y_train_scores = clf.decision_scores_  # 返回训练数据上的异常值 (分值越大越异常)
        print("On train Data:")
        evaluate_print(clf_name, y_train, y_train_scores)

        # 用训练好的clf来预测未知数据中的异常值
        y_test_pred = clf.predict(X_test)  # 返回未知数据上的分类标签 (0: 正常值, 1: 异常值)
        y_test_scores = clf.decision_function(X_test)  # 返回未知数据上的异常值 (分值越大越异常)
        print("On Test Data:")
        evaluate_print(clf_name, y_test, y_test_scores)

        y_true = column_or_1d(y_test)
        y_pred = column_or_1d(y_test_scores)
        check_consistent_length(y_true, y_pred)

        roc = np.round(roc_auc_score(y_true, y_pred), decimals=4),
        prn = np.round(precision_n_scores(y_true, y_pred), decimals=4)
        pca_roc.append(roc)
        pca_prn.append(prn)

        clf_name = 'IForest'
        clf = IForest()  # 初始化检测器clf
        clf.fit(X_train)  # 使用X_train训练检测器clf

        # 返回训练数据X_train上的异常标签和异常分值
        y_train_pred = clf.labels_  # 返回训练数据上的分类标签 (0: 正常值, 1: 异常值)
        y_train_scores = clf.decision_scores_  # 返回训练数据上的异常值 (分值越大越异常)
        print("On train Data:")
        evaluate_print(clf_name, y_train, y_train_scores)

        # 用训练好的clf来预测未知数据中的异常值
        y_test_pred = clf.predict(X_test)  # 返回未知数据上的分类标签 (0: 正常值, 1: 异常值)
        y_test_scores = clf.decision_function(X_test)  # 返回未知数据上的异常值 (分值越大越异常)
        print("On Test Data:")
        evaluate_print(clf_name, y_test, y_test_scores)

        y_true = column_or_1d(y_test)
        y_pred = column_or_1d(y_test_scores)
        check_consistent_length(y_true, y_pred)

        roc = np.round(roc_auc_score(y_true, y_pred), decimals=4),
        prn = np.round(precision_n_scores(y_true, y_pred), decimals=4)
        iforest_roc.append(roc)
        iforest_prn.append(prn)
    except:
        print("出现预测值全为一种的情况。跳过")
        continue





print('KNN average ROC:', np.average(knn_roc))
print('KNN average PRN:', np.average(knn_prn))
print('LOF average ROC:', np.average(lof_roc))
print('LOF average PRN:', np.average(lof_prn))
print('PCA average ROC:', np.average(pca_roc))
print('PCA average PRN:', np.average(pca_prn))
print('IForest average ROC:', np.average(iforest_roc))
print('IForest average PRN:', np.average(iforest_prn))





roc_all = [np.average(knn_roc), np.average(lof_roc), np.average(pca_roc), np.average(iforest_roc)]
prn_all = [np.average(knn_prn), np.average(lof_prn), np.average(pca_prn), np.average(iforest_prn)]
names = ['KNN', 'LOF', 'PCA', 'IForest']

plt.figure(figsize=(10, 10), dpi=80)
# 再创建一个规格为 1 x 1 的子图
# plt.subplot(1, 1, 1)
# 柱子总数
N = 4
# 包含每个柱子对应值的序列
values = roc_all
# 包含每个柱子下标的序列
index = np.arange(N)
# 柱子的宽度
width = 0.45
# 绘制柱状图, 每根柱子的颜色为紫罗兰色
p2 = plt.bar(index, values, width, label="ROC", color="#87CEFA")
# 设置横轴标签
plt.xlabel('algorithm')
# 设置纵轴标签
plt.ylabel('ROC')
# 添加标题
plt.title('')
# 添加纵横轴的刻度
plt.xticks(index, ('KNN', 'LOF', 'PCA', 'IForest'))
# plt.yticks(np.arange(0, 10000, 10))
# 添加图例
plt.legend(loc="upper right")
plt.show()




plt.figure(figsize=(10, 10), dpi=80)
# 再创建一个规格为 1 x 1 的子图
# plt.subplot(1, 1, 1)
# 柱子总数
N = 4
# 包含每个柱子对应值的序列
values = prn_all
# 包含每个柱子下标的序列
index = np.arange(N)
# 柱子的宽度
width = 0.45
# 绘制柱状图, 每根柱子的颜色为紫罗兰色
p2 = plt.bar(index, values, width, label="ROC", color="#8000FA")
# 设置横轴标签
plt.xlabel('algorithm')
# 设置纵轴标签
plt.ylabel('PRN')
# 添加标题
plt.title('')
# 添加纵横轴的刻度
plt.xticks(index, ('KNN', 'LOF', 'PCA', 'IForest'))
# plt.yticks(np.arange(0, 10000, 10))
# 添加图例
plt.legend(loc="upper right")
plt.show()








