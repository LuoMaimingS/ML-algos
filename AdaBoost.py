# coding=utf-8

from tools import *
from HomeWork_1 import *
import numpy as np
import math

T = 5

if __name__ == '__main__':
    with open('D:/git/data/mnistTrain_scale.txt', 'r') as f_in:
        lines = f_in.readlines()
    data = np.zeros((6000, 785))
    for i in range(len(lines)):
        if (i + 1) % 10 == 0:
            temp = eval(lines[i])
            p = int(i / 10)
            data[p] = temp
    c = get_distribution_list(data)
    '''
    temp_list = c.copy()
    temp_list.sort()
    max1 = temp_list[0]
    max2 = temp_list[1]
    '''
    # 分割data集并初始化权重
    # lower_bound = 0
    # temp = 0
    ave_weight = 1 / len(c)
    weight_list = []
    for i in range(len(c)):
        '''
        upper_bound = lower_bound + c[i]
        用来细分数据集，未使用
        if c[i] == max1 or c[i] == max2:
            exec("dataset_%s = data[lower_bound:upper_bound, :]" % temp)
            temp += 1
        print(dataset_0.shape, dataset_1.shape)
        lower_bound = upper_bound
        '''
        weight_list.append(ave_weight)

    # 调用分类器, 以选取在一定样本权值下的最优分类器， S为弱分类器个数
    tree_list = []
    error_rate_list = []
    accumulative_weighted_error_list = []
    alpha_list = []
    for t in range(T):
        # choose classifier and computing its error rate
        for i in range(S):
            print(".........................................Start building the",
                  i, "th tree.........................................")
            exec("tree%s = Build_Tree(data, m, e, 1, maxdepth=15)" % i)
            accumulative_weighted_error = 0
            error = 0
            for j in range(len(data)):
                back_test_data = data[j, :-1]
                back_test_label = int(data[j, -1])
                value_list = []
                exec("value_list = tree%s.Test_Tree(back_test_data)" % i)
                value = 0
                pos = 0
                for j in range(len(value_list)):
                    if value_list[j] > value:
                        value = value_list[j]
                        pos = j
                # pos即为对该向量的预测值y, back_test_label即为其真实值
                if pos != back_test_label:
                    accumulative_weighted_error += weight_list[back_test_label]
                    error += 1
            accumulative_weighted_error_list.append(accumulative_weighted_error)
            error_rate_list.append((error / len(data)))
            exec("tree_list.append(tree%s)" % i)
        print(error_rate_list)
        print(accumulative_weighted_error_list)
        min = np.inf
        chosen_tree_pos = 0
        for i in range(len(accumulative_weighted_error_list)):
            if accumulative_weighted_error_list[i] < min:
                chosen_tree_pos = i
        chosen_tree = tree_list[chosen_tree_pos]
        error = error_rate_list[chosen_tree_pos]

        # if the classifier is too bad, skip it
        if error > 0.3:
            continue

        # calculate weight of the classifier
        alpha = 0.5 * (math.log((1 / error) - 1))
        alpha_list.append(alpha)

        # z = math.exp(-alpha * )









