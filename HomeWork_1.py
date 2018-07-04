# coding=utf-8

'''
该文件实现一个决策树，基于树形结构而非队列
运行后可得到Testing数据集的accuracy
需要改变数据集读取路径
'''

from tools import *
import numpy as np

np.seterr(divide='ignore', invalid='ignore')

maxdepth = 10000
e = 0.01
m = 3


# 叶子节点
class Node:
    '''
    树的叶子节点
    '''
    def __init__(self, L, R, c, w=None, b=None):
        self.L = L
        self.R = R
        self.c = c
        self.w = w
        self.b = b

    def Test_Tree(self, x):
        if self.L is None:
            return self.c
        elif np.vdot(self.w, x) + self.b >= 0:
            return self.L.Test_Tree(x)
        else:
            return self.R.Test_Tree(x)


def Build_Tree(data, m, e, depth, maxdepth):
    root = Build_Tree_Recursion(data, m, e, depth, maxdepth)
    return root


def Build_Tree_Recursion(data, m, e, depth, maxdepth):
    c = get_distribution_list(data)
    print("Building the", depth, "layer......  data.shape", data.shape, "data.distribution:",c)
    f_out.write("Buliding the" + str(depth) + "layer......  data.shape:" + str(data.shape) + "data distribution:"
                + str(c) + '\n')
    if len(data) <= m or is_distinct(data) or depth >= maxdepth:
        f_out.write("Leave Node in layer" + str(depth) + '\n')
        return Node(None, None, c)
    w, b = Linear(data, c, e)

    DL = np.zeros((1, 785))
    DR = np.zeros((1, 785))
    count_pos = 0
    count_neg = 0
    for i in range(len(data)):
        xt = data[i]
        xt = xt[np.newaxis, :]
        # print(xt.shape)
        x = data[i, :-1]
        value = np.vdot(w, x) + b
        if value >= 0:
            count_pos += 1
            DL = np.concatenate((DL, xt), axis=0)
        else:
            count_neg += 1
            DR = np.concatenate((DR, xt), axis=0)
        if (i + 1) % 1000 == 0 or i == (len(data) - 1):
            print("Finish processing the", i + 1, "th sample, positive values: ", count_pos,
                  " negative values: ", count_neg)
            f_out.write("Finish processing the" + str(i + 1) + "th sample, positive values: " + str(count_pos)
                        + " negative values: " + str(count_neg) + '\n')
            count_pos = 0
            count_neg = 0
    DL = np.delete(DL, 0, 0)
    DR = np.delete(DR, 0, 0)
    print(DL.shape, DR.shape)
    if DL.shape[0] == 0 or DR.shape[0] == 0:
        f_out.write("Leave Node in layer" + str(depth) + '\n')
        return Node(None, None, c)
    return Node(Build_Tree_Recursion(DL, m, e, depth + 1, maxdepth), Build_Tree_Recursion(DR, m, e, depth + 1, maxdepth), c, w, b)


def Linear(data, c, e):
    f_out.write("Linear Classification" + '\n')
    # 随机过程
    x_positive, x_negative, positive_label = random_sample_from_data(data, c)

    w = []
    b = []
    w0 = (x_positive - x_negative) / np.linalg.norm(x_positive - x_negative)
    b0 = (np.vdot(w0, x_positive) + np.vdot(w0, x_negative)) / 2
    w.append(w0)
    b.append(b0)
    # print(w0)
    # print("b0:", b0, end="    ")
    T = int(1 / np.square(e))
    for t in range(1, T):
        temp_random = np.random.randint(0, len(data) - 1)
        xt = data[temp_random]
        x = xt[:-1]
        x_label = xt[-1]
        if x_label == positive_label:
            x_label_value = 1
        else:
            x_label_value = -1
        if (np.vdot(w[t - 1], x) + b[t - 1]) * x_label_value < 0:
            w_temp = w[t - 1] + 0.1/(0.1 + t * np.square(e)) * x * x_label_value
            b_temp = b[t - 1] + 0.1/(0.1 + t * np.square(e)) * x_label_value
        else:
            w_temp = w[-1]
            b_temp = b[-1]
        w.append(w_temp)
        b.append(b_temp)
        if (t % len(data) == 0) and np.vdot((w[t] - w[t - len(data)]), (w[t] - w[t - len(data)])) < 0.001:
            break
    # print("w calculated, b[T]:", b[-1])
    # print("End of the loop of the linear classification, Return! ")
    return w[-1], b[-1]


if __name__ == '__main__':
    # Training Process
    with open('D:/git/data/mnistTrain_scale.txt', 'r') as f_in:
        lines = f_in.readlines()
    with open('D:/git/ML-algos/log/log.txt', 'w') as f_out:
        data = np.zeros((6000, 785))
        for i in range(len(lines)):
            if (i + 1) % 10 == 0:
                temp = eval(lines[i])
                p = int(i / 10)
                data[p] = temp
                if (i + 1) % 10000 == 0:
                    f_out.write("Finish processing the " + str(i + 1) + "th line" + '\n')
        # 建立决策树
        tree = Build_Tree(data, m, e, 1, maxdepth)
        f_out.write("Tree built! the shape of data for training:" + str(data.shape) + '\n')

        # Testing Process
        with open('D:/git/data/mnistTest_scale.txt', 'r') as f_in:
            lines = f_in.readlines()
        count_correct = 0
        for i in range(len(lines)):
            test_data = np.array(eval(lines[i]))[:-1]
            label = np.array(eval(lines[i]))[-1]
            value_list = tree.Test_Tree(test_data)
            value = 0
            pos = 0
            for j in range(len(value_list)):
                if value_list[j] > value:
                    value = value_list[j]
                    pos = j
            if label == pos:
                count_correct += 1
        accuracy = count_correct / len(lines)
        f_out.write("Testing Finished!  Accuracy =" + str(accuracy))



