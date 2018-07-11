# coding=utf-8

import numpy as np

k = 2


def k_means_clustering(data, k):
    # Initialization
    update_flag = True
    means_vector = []
    random_list = []
    temp_random = np.random.randint(0, data.shape[0])
    random_list.append(temp_random)
    means_vector.append(data[temp_random])
    for i in range(k - 1):
        distinct_flag = False
        while not distinct_flag:
            temp_random = np.random.randint(0, data.shape[0])
            for j in range(len(random_list)):
                if temp_random == random_list[j]:
                    distinct_flag = False
                    break
                distinct_flag = True
        random_list.append(temp_random)
        means_vector.append(data[temp_random])
    print(random_list)

    while update_flag:
        # clear division of clusters
        c = []
        for i in range(k):
            c.append([])
        # new division of clusters
        for j in range(data.shape[0]):
            tag = None
            min_dis = np.inf
            for i in range(k):
                dis = np.linalg.norm(data[j] - means_vector[i])
                if dis < min_dis:
                    min_dis = dis
                    tag = i
                    # print(dis)
            c[tag].append(data[j])
        # calculate new mean_vectors
        # update_flag = True
        for i in range(k):
            sum_vector = np.zeros((1, data.shape[1]))
            for j in range(len(c[i])):
                sum_vector += c[i][j]
            new_mean_vector = sum_vector / len(c[i])
            print(np.linalg.norm(new_mean_vector - means_vector[i]), end=' ')
            if np.linalg.norm(new_mean_vector - means_vector[i]) < 0.001:
                update_flag = False
            means_vector[i] = new_mean_vector
        print('')
    print("clustering finished!")
    for i in range(len(c)):
        print("scale of cluster", i + 1, ":", len(c[i]))
        print("mean_vector:", means_vector[i])


if  __name__ == '__main__':
    with open('D:/git/data/HomeWork_3_Kmeans.txt', 'r') as f_in:
        lines = f_in.readlines()

    data = np.zeros((1000, 24))
    for i in range(len(lines)):
        temp = eval(lines[i])
        data[i] = temp[:-1]
    k_means_clustering(data, k)
