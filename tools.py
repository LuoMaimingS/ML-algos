# coding utf-8


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
    c = get_class_distribution(data)
    distinct_flag = False
    for i in range(len(c) - 1):
        if c[i] != c[i + 1]:
            distinct_flag = True
            break
    return distinct_flag
