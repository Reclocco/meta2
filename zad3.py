from __future__ import print_function

import copy
import math
import random
import sys
from time import perf_counter


def nums(n):
    num = []
    for i in range(n):
        num.append(i)

    return num


def my_split(line):
    return list(map(int, [digit for digit in line]))


def whole_rand(n):
    return round(random.randint(0, n))


def get_input():
    my_input = []
    line = input().split()
    my_input.append(int(line[0]))
    my_input.append(int(line[1]))
    my_input.append(int(line[2]))

    for i in range(my_input[1]):
        my_input.append(my_split(input()))

    return my_input


def gen_seq():
    my_seq = []
    for i in range(20):
        my_seq.append(whole_rand(3))

    return my_seq


def wheres_waldo(my_map):
    waldo = [0, 0]

    for i in range(len(my_map)):
        for j in range(len(my_map[1])):
            if my_map[i][j] == 5:
                waldo = [i, j]

    return waldo


def search_lab(my_map, temp):
    basic = temp
    time = my_map.pop(0)
    # print("TYPE: ", time, type(time))
    my_map.pop(1)
    my_map.pop(0)
    delta_time = perf_counter()

    x = gen_seq()
    # print('1st path: ', x)

    t_start = perf_counter()
    while time > perf_counter() - t_start and temp > 1:
        if perf_counter() - delta_time >= 0.1:
            temp = temp * 0.999
            delta_time = perf_counter()

        walked = []
        curr_pos = wheres_waldo(my_map)
        # print('successful: ', x)

        next_x = perturb(x, temp/basic)

        for idx in range(len(next_x)):
            if next_x[idx] == 0:  # RIGHT
                try:
                    if my_map[curr_pos[0]][curr_pos[1] + 1] != 1:
                        curr_pos[1] += 1
                        walked.append(next_x[idx])
                except IndexError:
                    pass

            elif next_x[idx] == 1:  # LEFT
                try:
                    if my_map[curr_pos[0]][curr_pos[1] - 1] != 1:
                        curr_pos[1] -= 1
                        walked.append(next_x[idx])
                except IndexError:
                    pass

            elif next_x[idx] == 2:  # DOWN
                try:
                    if my_map[curr_pos[0] + 1][curr_pos[1]] != 1:
                        curr_pos[0] += 1
                        walked.append(next_x[idx])
                except IndexError:
                    pass

            elif next_x[idx] == 3:  # UP
                try:
                    if my_map[curr_pos[0] - 1][curr_pos[1]] != 1:
                        curr_pos[0] -= 1
                        walked.append(next_x[idx])
                except IndexError:
                    pass

            if my_map[curr_pos[0]][curr_pos[1]] == 8:
                # print("FINISHED")

                if len(walked) < len(x):
                    x = copy.deepcopy(walked)

                else:
                    prob = 0.5

                    if random.uniform(0, 1) < prob:
                        x = copy.deepcopy(next_x)

    return x


def perturb(my_path, how_strong):
    copied = copy.deepcopy(my_path)
    for i in range(math.ceil(len(my_path) * how_strong)):
        idx = whole_rand(len(my_path) - 1)
        copied[idx] = whole_rand(3)

    return copied


def to_char(my_path):
    chars = []
    for i in range(len(my_path)):
        if my_path[i] == 0:
            chars.append("P")
        elif my_path[i] == 1:
            chars.append("L")
        elif my_path[i] == 2:
            chars.append("D")
        elif my_path[i] == 3:
            chars.append("U")

    return chars


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


le_inputo = get_input()
my_best = search_lab(le_inputo, 1000)
print(len(my_best))
eprint(to_char(my_best))

