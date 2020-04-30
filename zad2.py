from __future__ import print_function

import copy
import math
import random
import sys
from time import perf_counter

values = [0, 32, 64, 128, 160, 192, 223, 255]


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_input():
    line = list(map(int, input().split()))
    time = line[0]
    n_size = line[1]
    m_size = line[2]
    k_size = line[3]
    matrix = []

    for i in range(n_size):
        matrix.append(list(map(int, input().split())))

    return [matrix, time, k_size]


def calc_distance(m1, m2):
    distance = 0

    for i in range(len(m1)):
        for j in range(len(m1[0])):
            distance += (m1[i][j] - m2[i][j]) ** 2

    return distance / (len(m1) * len(m1[0]))


def get_chunk_size(n, m, k):
    n_chunk = random.randint(k, n)
    while n % n_chunk != 0:
        n_chunk = random.randint(k, n)

    m_chunk = random.randint(k, m)
    while m % m_chunk != 0:
        m_chunk = random.randint(k, m)

    return [n_chunk, m_chunk]


def initiate(ideal_matrix, k):
    matrix = copy.deepcopy(ideal_matrix)
    chunk_size = get_chunk_size(len(ideal_matrix), len(ideal_matrix[0]), k)

    # print("INITIATING", len(ideal_matrix), chunk_size, len(ideal_matrix) / chunk_size[0])
    for i in range(int(len(ideal_matrix) / chunk_size[0])):
        for j in range(int(len(ideal_matrix[0]) / chunk_size[1])):
            value = random.choice(values)
            for column in range(chunk_size[0]):
                for row in range(chunk_size[1]):
                    # print(i * chunk_size[0] + column, j * chunk_size[1] + row)
                    matrix[i * chunk_size[0] + column][j * chunk_size[1] + row] = value

    return [matrix, chunk_size]


def perturb(matrix, n_chunk, m_chunk, k):
    copied = copy.deepcopy(matrix)
    chunk_size = [n_chunk, m_chunk]
    if random.randint(0, 30) < 2:
        chunk_size = get_chunk_size(len(copied), len(copied[0]), k)

        for i in range(int(len(copied) / chunk_size[0])):
            for j in range(int(len(copied[0]) / chunk_size[1])):
                value = random.choice(values)
                for column in range(chunk_size[0]):
                    for row in range(chunk_size[1]):
                        copied[i * chunk_size[0] + column][j * chunk_size[1] + row] = value

    else:
        no_chunks = math.ceil((len(copied) * len(copied[0])) / (chunk_size[0] * chunk_size[1]) / 10)
        for perturbation in range(no_chunks):
            chunk_pos = [random.randint(0, len(copied) / chunk_size[0] - 1),
                         random.randint(0, len(copied[0]) / chunk_size[1] - 1)]
            value = random.choice(values)

            # print(chunk_pos, chunk_size, value)
            for i in range(chunk_size[0]):
                for j in range(chunk_size[1]):
                    copied[chunk_pos[0] * chunk_size[0] + i][chunk_pos[1] * chunk_size[1] + j] = value

    return copied


def search_for_closest(ideal, time, t, c, k):
    start_time = perf_counter()
    delta_time = perf_counter()
    tmp = initiate(ideal, k)
    chunk_size = tmp[1]
    x = tmp[0]
    # print("init: ", x)

    while t > 0.1 and time > perf_counter() - start_time:
        next_x = perturb(x[:], chunk_size[0], chunk_size[1], k)
        # print("next: ", next_x, "curr: ", x)

        if calc_distance(next_x, ideal) < calc_distance(x, ideal):
            x = copy.deepcopy(next_x)

        else:
            try:
                prob = 1.0 / (1 + math.pow(math.e, c * (calc_distance(next_x, ideal) - calc_distance(x, ideal)) / t))
            except OverflowError:
                prob = 0

            if random.uniform(0, 1) < prob:
                x = copy.deepcopy(next_x)

        if perf_counter() - delta_time >= 0.1:
            t = t * 0.9
            delta_time = perf_counter()

        # print("DISTANCE", (calc_distance(next_x, ideal) - calc_distance(x, ideal)), "TEMP: ", t, "PROB: ", prob)

    print(calc_distance(x, ideal))

    for i in range(len(x)):
        line = ""
        for j in range(len(x[0])):
            line += str(x[i][j]) + " "
        eprint(line)


# my_matrix = [[1, 1, 0, 0, 5, 52], [1, 1, 0, 0, 8, 3], [5, 5, 3, 3, 8, 40], [5, 5, 3, 3, 54, 77]]
my_input = get_input()
my_matrix = my_input[0]
my_time = my_input[1]
my_k = my_input[2]

search_for_closest(my_matrix, my_time, 5000, 2, my_k)

