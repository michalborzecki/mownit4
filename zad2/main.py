import random
import matplotlib.pyplot as plt
import numpy as np
from energies import *
from neighbors import *


def main():
    n = 20
    density = 0.2
    image = create_image(n, density)
    show_image(image)

    temp_max = 2000
    iterations = 1000
    neighbors_f = get_12_neighbors
    result = simulanneal(image, lambda i: generate_next_state(i, neighbors_f),
                         lambda i: get_image_energy(i, energy_black_in_column, neighbors_f),
                         temp_max, lambda t: t * 0.95, iterations)
    show_image(result)


def show_image(image):
    n = len(image)
    fig = plt.figure(figsize=[8, 8])
    ax = fig.add_subplot(111)
    ax.set_position([0, 0, 1, 1])
    ax.set_axis_off()
    ax.set_xlim(-1, n)
    ax.set_ylim(-1, n)
    for i in range(n):
        for j in range(n):
            ax.plot(j, i, 's', markersize=570/n, markeredgecolor='k',
                    markerfacecolor=image[i][j], markeredgewidth=1)
    plt.show()


def create_image(size, density):
    return [['w' if density < random.random() else 'k' for _ in range(size)]
            for _ in range(size)]


def simulanneal(start, next_state_f, value_f, temp_max,
                temp_change_f, iterations):
    actual = best = start
    actual_val = best_val = value_f(actual)
    temp = temp_max
    for i in range(1, iterations):
        if i % 100 == 0:
            print(str(i) + ", " + str(best_val))
        block, block2 = next_state_f(actual)
        val = value_f(actual)
        prob = np.exp(-temp_max * (val - actual_val) / temp)
        if actual_val >= val or random.random() <= prob:
            actual_val = val
            if best_val > val:
                best, best_val = [r[:] for r in actual], actual_val
        else:
            undo_next_state(start, block, block2)
        temp = temp_change_f(temp)
    return best


def generate_next_state(image, neighbors_f):
    n = len(image)
    black = [(y, x) for x in range(n) for y in range(n) if image[y][x] == 'k']
    block = random.sample(black, 1)[0]
    block2 = random.sample(neighbors_f(image, block), 1)[0]
    y1, x1 = block
    y2, x2 = block2
    image[y2][x2], image[y1][x1] = image[y1][x1], image[y2][x2]
    return block, block2


def undo_next_state(image, block, block2):
    y1, x1 = block
    y2, x2 = block2
    image[y2][x2], image[y1][x1] = image[y1][x1], image[y2][x2]


if __name__ == "__main__":
    main()
