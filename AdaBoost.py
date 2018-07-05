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
    # get 2 classes
    temp_list = c.copy()
    temp_list.sort()
    max1 = temp_list[0]
    max2 = temp_list[1]
    # 分割data集并初始化权重
    lower_bound = 0
    temp = 0
    data_set_0 = None
    data_set_1 = None
    for i in range(len(c)):
        upper_bound = lower_bound + c[i]
        # 用来细分数据集
        if c[i] == max1 or c[i] == max2:
            exec("data_set_%s = data[lower_bound:upper_bound, :]" % temp)
            temp += 1
        lower_bound = upper_bound
        # weight_list.append(ave_weight)
    print(data_set_0.shape, data_set_1.shape)
    # set label
    data_set_0[:, -1] = 1
    data_set_1[:, -1] = -1
    data = np.concatenate((data_set_0, data_set_1))
    weight_list = []
    alpha_list = []
    w_list =[]
    b_list = []
    ave_weight = 1 / data.shape[0]
    for i in range(data.shape[0]):
        weight_list.append(ave_weight)
    print(data.shape)

    for t in range(T):
        # 调用线性分类器
        w, b, positive_label = Linear(data, e)
        # 计算错误率
        error = 0
        for i in range(data.shape[0]):
            x = data[i, :-1]
            if (np.vdot(w, x) + b >= 0 and data[i, -1] != positive_label) or \
                    (np.vdot(w, x) + b <= 0 and data[i, -1] == positive_label):
                error += 1
        error_rate = error / data.shape[0]
        print(error_rate)
        # if the classifier is too bad, skip it
        if error_rate > 0.3:
            continue
        else:
            w_list.append(w)
            b_list.append(b)

        # calculate weight of the classifier
        alpha = 0.5 * (math.log((1 / error) - 1))
        alpha_list.append(alpha)

        # 规范化因子
        z = 0
        for i in range(data.shape[0]):
            x = data[i, :-1]
            if np.vdot(w, x) + b >= 0:
                g = positive_label
            else:
                g = -positive_label
            z += weight_list[i] * np.exp(-alpha * data[i, -1] * g)

        # update weight_list
        for i in range(data.shape[0]):
            x = data[i, :-1]
            if np.vdot(w, x) + b >= 0:
                g = positive_label
            else:
                g = -positive_label
            weight_list[i] = weight_list[i] * np.exp(-alpha * data[i, -1] * g) / z

    # output
    test_data = np.zeros((1, 784))  # test_data shape, not real
    gen_value = 0
    for i in range(len(alpha_list)):
        gen_value += alpha_list[i] * (np.vdot(w_list[i], test_data) + b_list[i])
    result = np.sign(gen_value)








