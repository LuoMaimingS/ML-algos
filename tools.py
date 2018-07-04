# coding utf-8

import numpy as np


def get_distribution_list(data):
    c = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(len(data)):
        label = int(data[i, -1])
        c[label] += 1
    return c


def get_class_distribution(data):
    c = []
    for i in range(len(data)):
        c.append(data[i][-1])
    return c


def is_distinct(data):
    c = get_distribution_list(data)
    category = 0
    for i in range(len(c)):
        if c[i] != 0:
            category += 1
    if category == 1:
        return True
    else:
        return False



def random_sample_from_data(data, c):
    temp_random = np.random.randint(0, len(data) - 1)
    xt_positive = data[temp_random]
    positive_label = xt_positive[-1]
    count_negative = 0
    for i in range(len(c)):
        if i != positive_label:
            count_negative += c[i]
    try:
        temp_random = np.random.randint(0, count_negative)
    except ValueError as e:
        print("exception:", e, "    ", count_negative)
    xt_negative = data[temp_random]
    x_positive = xt_positive[:-1]
    x_negative = xt_negative[:-1]
    return x_positive, x_negative, positive_label
