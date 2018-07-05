# ML-algos
some algorithms in Machine Learning


HomeWork_1.py 实现了一个决策树，目前基于树形结构，而非队列，运行后期望可得到Testing数据集的accuracy，该算法使用MINIST数据集（每10行取1行，以减少样本数量，提升运行速度）。
每次运行之后，运行中间信息及最终结果保存在log文件夹中的log.txt中，其中最后一行代表使用一颗决策树的准确率。

K-means.py 基于k-means算法，实现了对1000个数据的聚类，最后打印出所聚的各类规模。由于一开始随机选择的初始均值向量的不同，该算法运行结果具有较大的差异。