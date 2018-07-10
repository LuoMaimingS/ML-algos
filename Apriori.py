# coding=utf-8

import numpy as np

minsup = 0.144


def apriori(data):
    k = 1
    f = []
    for i in range(data.shape[1]):
        temp = np.zeros((1, data.shape[1]))
        temp[0, i] = 1
        f.append(temp)

    # Init
    f_new = []
    for i in range(len(f)):
        count = 0
        for t in range(data.shape[0]):
            if match_transaction(f[i], data[t, :]):
                count += 1
        support = count / data.shape[0]
        if support >= minsup:
            print(i, support)
            f_new.append(f[i])

    while len(f_new) != 0:
        f_new = []
        for i in range(len(f) - 1):
            for j in range(i + 1, len(f)):
                pair, flag = pairs(f[i], f[j], k)
                if flag:
                    count = 0
                    for t in range(data.shape[0]):
                        if match_transaction(pair, data[t, :]):
                            count += 1
                    support = count / data.shape[0]
                    # print(support)
                    if support >= minsup:

                        for l in range(pair.shape[1]):
                            if pair[0, l] == 1:
                                print(l + 1, end=' ')
                        print(support)
                        # print("f_new append", pair, support)
                        f_new.append(pair)
        if len(f_new) == 0:
            break
        f = f_new
        k += 1

    # print(f)


def pairs(a1, a2, k):
    pair = np.zeros((1, a1.shape[1]))
    pos = 0
    for i in range(a1.shape[1]):
        c_backwards = k - 1
        pos = 0
        while (c_backwards > 0) and pos < a1.shape[1]:
            if a1[0, pos] == 0 and a2[0, pos] == 0:
                pos += 1
                continue
            elif a1[0, pos] == 1 and a2[0, pos] == 1:
                pair[0, pos] = 1
                pos += 1
                c_backwards -= 1
            else:
                return None, False
    for i in range(pos, a1.shape[1]):
        if a1[0, i] == 1 or a2[0, i] == 1:
            pair[0, i] = 1
    # print("append", pair)

    return pair, True


def match_transaction(v, t):
    for i in range(len(t)):
        # item i not in this transaction
        if (v[0, i] == 1) and (t[i] == 0):
            return False
    return True


# def join(a1, a2):


if __name__ == '__main__':
    with open('d:/git/data/Apriori_data.txt', 'r') as f_in:
        lines = f_in.readlines()
        row = len(lines)
        col = (len(lines[0].split(' ')))

    data = np.zeros((row, col))
    for i in range(row):
        for j in range(col):
            data[i, j] = lines[i].split(' ')[j]
    data = data[1:, :]

    # print(data.shape)
    apriori(data)

