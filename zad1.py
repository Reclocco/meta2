import math
import random
import sys
from time import perf_counter

vec_len = lambda x: math.sqrt(x[0] ** 2 + x[1] ** 2 + x[2] ** 2 + x[3] ** 2)


def randomize(x):
    idx = random.randint(0, 3)
    value = random.randint(-1, 1)
    if value <= 0:
        x[idx] += 10
    else:
        x[idx] -= 10

    return x


def happy_cat(x=None):
    if x is None:
        x = [0, 0, 0, 0]
    return ((vec_len(x) ** 2 - 4) ** 2) ** (1 / 8) + (1 / 4) * ((vec_len(x) ** 2) / 2 + sum(x)) + 1 / 2


def griewank(x=None):
    if x is None:
        x = [0, 0, 0, 0]
    return 1 + (x[0] ** 2 + x[1] ** 2 + x[2] ** 2 + x[3] ** 2) / 4000 - \
           (math.cos(x[0]) * math.cos(x[1] / math.sqrt(2)) * math.cos(x[2] / math.sqrt(3)) * math.cos(x[3] / 2))


def search_cat(act_sol, delta, hood):
    local_opt = []
    t_start = perf_counter()
    counter = 0

    while int(sys.argv[1]) - (perf_counter() - t_start) > 0:
        prev_best = act_sol
        for element in get_hood(act_sol, delta, hood):
            if happy_cat(element) < happy_cat(act_sol):
                act_sol = element

        if prev_best == act_sol:
            local_opt.append(act_sol)
            counter += 1

            if counter == 4:
                act_sol = restart()
                counter = 0

            else:
                act_sol = randomize(act_sol)

    best = act_sol
    for opt in local_opt:
        if happy_cat(opt) < happy_cat(best):
            best = opt

    print(best[0], best[1], best[2], best[3], happy_cat(best))


def search_wank(act_sol, delta, hood):
    local_opt = []
    t_start = perf_counter()
    counter = 0

    while int(sys.argv[1]) - (perf_counter() - t_start) > 0:
        prev_best = act_sol
        for element in get_hood(act_sol, delta, hood):
            if griewank(element) < griewank(act_sol):
                act_sol = element

        if prev_best == act_sol:
            local_opt.append(act_sol)
            counter += 1

            if counter == 4:
                act_sol = restart()
                counter = 0

            else:
                act_sol = randomize(act_sol)

    best = act_sol
    for opt in local_opt:
        if griewank(opt) < griewank(best):
            best = opt

    print(best[0], best[1], best[2], best[3], griewank(best))


def get_hood(x=None, delta_fun=0.2, hood_fun=0.6):
    if x is None:
        x = [0, 0, 0, 0]

    my_hood = []

    reach = int((10 * hood_fun) / (10 * delta_fun))

    for idx in range(4):
        x[idx] -= hood_fun

    for _ in range(reach * 2):
        for _ in range(reach * 2):
            for _ in range(reach * 2):
                for _ in range(reach * 2):
                    my_hood.append(x[::])
                    x[3] += delta_fun

                x[3] -= reach * 2 * delta_fun
                x[2] += delta_fun

            x[2] -= reach * 2 * delta_fun
            x[1] += delta_fun

        x[1] -= reach * 2 * delta_fun
        x[0] += delta_fun

    return my_hood


def restart():
    return [random.randint(-1000, 1000), random.randint(-1000, 1000),
            random.randint(-1000, 1000), random.randint(-1000, 1000)]


start = restart()

da_hood = 0.6
da_delta = 0.2

if sys.argv[2] == 0:
    search_cat(start, da_delta, da_hood)
else:
    search_wank(start, da_delta, da_hood)
