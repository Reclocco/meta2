import copy
import math
import random
from time import perf_counter

vec_len = lambda x: math.sqrt(x[0] ** 2 + x[1] ** 2 + x[2] ** 2 + x[3] ** 2)


def get_input():
    line = input().split()
    time = int(line[0])
    start = list(map(int, line[1:]))

    return [time, start]


def perturb(x):
    copied = copy.deepcopy(x)

    idx1 = random.randint(0, 3)
    value = random.randint(-1, 1)

    copied[idx1] += value

    idx2 = random.randint(0, 3)
    value = random.randint(-1, 1)

    copied[idx2] += value

    return copied


def salomon(x=None):
    if x is None:
        x = [0, 0, 0, 0]
    return 1 - math.cos(2 * math.pi * vec_len(x)) + 0.1 * vec_len(x)


def search_salmon(t, c, x, time):
    start_time = perf_counter()
    delta_time = perf_counter()

    while t > 0.1 and time > perf_counter()-start_time:
        next_x = perturb(x)

        if salomon(next_x) < salomon(x):
            x = copy.deepcopy(next_x)
        else:
            prob = 1.0 / (1 + math.pow(math.e, c * (salomon(next_x) - salomon(x)) / t))

            if random.uniform(0, 1) < prob:
                x = copy.deepcopy(next_x)

        if perf_counter() - delta_time >= 0.1:
            t = t*0.999
            delta_time = perf_counter()

    print(x, salomon(x))


my_input = get_input()
my_start = my_input[1]
my_time = my_input[0]

search_salmon(1000, 1, my_start, my_time)

