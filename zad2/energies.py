import math


def get_image_energy(image, energy_f, neighbors_f):
    return sum([energy_f(image, (y, x), neighbors_f(image, (y, x)))
                for y in range(len(image)) for x in range(len(image))])


def energy_black_1_over_r2(image, block, neighbors):
    energy = 0
    if image[block[0]][block[1]] != 'k':
        return 0
    for neighbor in neighbors:
        if image[neighbor[0]][neighbor[1]] == 'k':
            energy += -1 / (math.sqrt((block[0] - neighbor[0])**2) +
                                      (block[1] - neighbor[1])**2)
    return energy


def energy_black_neg_1_over_r2(image, block, neighbors):
    return -energy_black_1_over_r2(image, block, neighbors)


def energy_black_in_column(image, block, neighbors):
    energy = 0
    if image[block[0]][block[1]] != 'k':
        return 0
    for neighbor in neighbors:
        if image[neighbor[0]][neighbor[1]] == 'k' and neighbor[1] == block[1]:
            energy += -1 / abs(block[0] - neighbor[0])
    return energy


def energy_black_only_1_neighbor(image, block, neighbors):
    energy = 0
    if image[block[0]][block[1]] != 'k':
        return 0
    for neighbor in neighbors:
        if image[neighbor[0]][neighbor[1]] == 'k':
            r = (math.sqrt((block[0] - neighbor[0])**2) +
                 (block[1] - neighbor[1])**2)
            if r == 1:
                energy += -1
            else:
                energy += 15
    return energy
