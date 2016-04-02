import sys
import numpy as np
import random
import matplotlib.pyplot as plt
import math


def main():
    if len(sys.argv) <= 1:
        print("File name is needed.\n")
        return
    path = sys.argv[1]
    sudoku, variables = read_file(path)
    if fill_sudoku(sudoku, variables) == -1:
        exit()
    print_sudoku_with_value(sudoku)

    temp_max = 2000
    iterations = 100000
    result = simulanneal(sudoku, lambda s: fill_sudoku(s, variables),
                         lambda s: generate_state(s, variables), sudoku_value,
                         temp_max, lambda t: t * 0.996, iterations)
    print_sudoku_with_value(result)


def print_sudoku_with_value(sudoku):
    print(sudoku_to_str(sudoku))
    print(sudoku_value(sudoku))


def plot(points, color='b'):
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    plt.plot(x, y, lw=1, c=color)
    plt.show()


def simulanneal(start, reset_state_f, next_state_f, value_f, temp_max,
                temp_change_f, iterations):
    actual = best = [r[:] for r in start]
    actual_val = best_val = value_f(actual)
    temp = temp_max
    points = [(0, actual_val)]
    counter = 0
    for i in range(1, iterations):
        states = [next_state_f(actual) for _ in range(20)]
        next_state = min(states, key=lambda s: sudoku_value_next(actual, actual_val, s[0], s[1]))
        val = sudoku_value_next(actual, actual_val, next_state[0], next_state[1])
        prob = np.exp(-math.sqrt(temp_max)*(val - actual_val)/temp)
        if actual_val >= val or random.random() <= prob:
            apply_next_state(actual, next_state[0], next_state[1])
            actual_val = val
            points.append((i, val))
            if best_val > val:
                best, best_val = [r[:] for r in actual], actual_val
                if val == 0:
                    break

        temp = temp_change_f(temp)
        if temp < 1:
            counter += 1
            print(i, actual_val, best_val)
            temp = temp_max
            if counter == 5:
                print("New permutation")
                reset_state_f(start)
                actual, actual_val = start, value_f(start)
                counter = 0
    points.append((iterations, value_f(best)))
    plot(points)
    return best


def fill_sudoku(sudoku, variables):
    if len(variables) == 0:
        return -1
    for r in variables:
        for c in r:
            for xy in c:
                sudoku[xy[0]][xy[1]] = 0

    for r in range(0, 7, 3):  # 0, 3, 6
        for c in range(0, 7, 3):
            left_numbers = set(range(1, 10)).difference(
                {x for row in sudoku[r:r+3] for x in row[c:c+3]})
            left_indexes = [xy for xy in variables[r//3][c//3] if xy[0] in range(r, r+3) and xy[1] in range(c, c+3)]
            for xy, num in zip(np.random.permutation(left_indexes), left_numbers):
                sudoku[xy[0]][xy[1]] = num
    return 0


def generate_state(sudoku, variables):
    indexes = []
    while len(indexes) < 2:
        indexes = variables[random.choice(range(3))][random.choice(range(3))]

    return random.sample(indexes, 2)


def sudoku_value(sudoku):
    value = 0
    for row in sudoku:
        value += 9 - len(set(row))
    for column in range(9):
        value += 9 - len({sudoku[x][column] for x in range(9)})
    return value


def apply_next_state(sudoku, num1, num2):
    sudoku[num1[0]][num1[1]], sudoku[num2[0]][num2[1]] = \
        sudoku[num2[0]][num2[1]], sudoku[num1[0]][num1[1]]


def sudoku_value_next(sudoku, old_value, num1, num2):
    part_value = 0
    for row in (sudoku[num1[0]], sudoku[num2[0]]):
        part_value -= 9 - len(set(row))
    for column in (num1[1], num2[1]):
        part_value -= 9 - len({sudoku[x][column] for x in range(9)})
    apply_next_state(sudoku, num1, num2)
    for row in (sudoku[num1[0]], sudoku[num2[0]]):
        part_value += 9 - len(set(row))
    for column in (num1[1], num2[1]):
        part_value += 9 - len({sudoku[x][column] for x in range(9)})
    apply_next_state(sudoku, num1, num2)
    return old_value + part_value


def read_file(path):
    def parse_char(c):
        try:
            return int(c)
        except ValueError:
            return 0

    try:
        with open(path, "r") as file:
            sudoku = [[parse_char(x) for x in line[:9]] for line in file
                      if len(line.rstrip("\n")) >= 9]
    except FileNotFoundError:
        print("File " + path + " not found.")
        return [], []
    if len(sudoku) != 9:
        print("Incorrect file format.")
        return [], []

    variables = [[] for _ in range(3)]
    for r in range(3):
        for c in range(3):
            variables[r].append([(r2, c2) for r2 in range(3*r, 3*r+3)
                                 for c2 in range(3*c, 3*c+3) if sudoku[r2][c2] == 0])
    if len(variables) == 0:
        print("Sudoku is solved.")
        return [], []
    return sudoku, variables


def sudoku_to_str(sudoku):
    return "\n".join(
        "".join([str(x) for x in row])
        for row in sudoku)


if __name__ == "__main__":
    main()
