import math


def energy_black_1_over_r(black, block, neighbors):
    if block not in black:
        return 0
    energy = 0
    for neighbor in black.intersection(neighbors):
        energy += -1 / (math.sqrt((block[0] - neighbor[0])**2 +
                                  (block[1] - neighbor[1])**2))
    return energy


def energy_black_neg_1_over_r(black, block, neighbors):
    return -energy_black_1_over_r(black, block, neighbors)


def energy_black_in_column(black, block, neighbors):
    energy = 0
    if block not in black:
        return 0
    for neighbor in black.intersection(neighbors):
        if neighbor[1] == block[1]:
            energy += -1 / abs(block[0] - neighbor[0])
    return energy


def energy_black_only_2_neighbors(black, block, neighbors):
    energy = 0
    if block not in black:
        return 0
    for neighbor in black.intersection(neighbors):
        if abs(block[0] - neighbor[0]) + abs(block[1] - neighbor[1]) == 1:
            energy += -1
        else:
            energy += 10
    return energy
