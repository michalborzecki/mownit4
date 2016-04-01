import random
import matplotlib.pyplot as plt
import numpy as np
from energies import *
from neighbors import *


def main():
    n = 100
    density = 0.2
    black = set(create_image(n, density))
    show_image(black, n)

    temp_max = 20000
    iterations = 50000
    neighbors_f = get_8_neighbors
    result = simulanneal(n, black, generate_next_state,
                         energy_black_only_2_neighbors, neighbors_f,
                         temp_max, lambda t: t * 0.999, iterations)
    show_image(result, n)


def show_image(black, size):
    fig = plt.figure(figsize=[8, 8])
    ax = fig.add_subplot(111)
    ax.set_position([0, 0, 1, 1])
    ax.set_axis_off()
    ax.set_xlim(-1, size)
    ax.set_ylim(-1, size)
    black = list(black)
    x = [xy[1] for xy in black]
    y = [xy[0] for xy in black]
    ax.plot(x, y, 's', markersize=640/size, markerfacecolor='k',
            markeredgewidth=0)
    plt.show()


def create_image(size, density):
    return [(j, i) for j in range(size) for i in range(size)
            if density > random.random()]


def simulanneal(size, black, next_state_f, energy_f, neighbor_f, temp_max,
                temp_change_f, iterations):
    actual = best = black
    actual_val = best_val = get_image_energy(size, actual, energy_f, neighbor_f)
    temp = temp_max
    for i in range(1, iterations):
        if i % 1000 == 0:
            print(str(i) + ", " + str(best_val))
        block, block2 = next_state_f(size, neighbor_f, actual)
        val = get_image_energy_next(size, actual, block, block2, actual_val, energy_f, neighbor_f)
        prob = np.exp(-temp_max * (val - actual_val) / temp)
        if actual_val >= val or random.random() <= prob:
            apply_state(block, block2, actual)
            actual_val = val
            if best_val > val:
                best, best_val = actual.copy(), actual_val
        temp = temp_change_f(temp)
    return best


def generate_next_state(size, neighbors_f, black):
    block = random.sample(black, 1)[0]
    block2 = random.sample(neighbors_f(size, block), 1)[0]
    return block, block2


def apply_state(block, block2, black):
    if block not in black:
        black.remove(block2)
        black.add(block)
    elif block2 not in black:
        black.remove(block)
        black.add(block2)


def get_image_energy(size, black, energy_f, neighbors_f):
    return sum([energy_f(black, b, neighbors_f(size, b))
                for b in black])


def get_image_energy_next(size, black, block1, block2, old_energy, energy_f, neighbors_f):
    part = set(neighbors_f(size, block1))
    part.union(set(neighbors_f(size, block2)))
    part.union({block1, block2})
    old_part_energy = sum([energy_f(black, block, neighbors_f(size, block))
                           for block in part])
    apply_state(block1, block2, black)
    new_part_energy = sum([energy_f(black, block, neighbors_f(size, block))
                           for block in part])
    apply_state(block1, block2, black)
    return old_energy - old_part_energy + new_part_energy

if __name__ == "__main__":
    main()
