import sys
import numpy as np
import random
import matplotlib.pyplot as plt


def main():
    if len(sys.argv) <= 1:
        print("File name is needed.\n")
        return
    path = sys.argv[1]
    sudoku, variables = read_file(path)
    if fill_sudoku(sudoku, variables) == -1:
        exit()
    print_sudoku_with_value(sudoku)

    temp_max = 5000
    iterations = 100000
    result = simulanneal(sudoku, lambda s: fill_sudoku(s, variables),
                         lambda s: generate_state(s, variables), sudoku_value,
                         temp_max, lambda t: t * 0.995, iterations)
    print_sudoku_with_value(result)


def print_sudoku_with_value(sudoku):
    print(sudoku_to_str(sudoku))
    print(sudoku_value(sudoku))


def plot(points, color='b'):
    for i in range(len(points) - 1):
        plt.plot([points[i][0], points[(i + 1)][0]],
                 [points[i][1], points[(i + 1)][1]], lw=1, c=color)
    plt.show()


def simulanneal(start, reset_state_f, next_state_f, value_f, temp_max,
                temp_change_f, iterations):
    actual = best = start
    actual_val = best_val = value_f(actual)
    temp = temp_max
    # points = [(0, actual_val)]
    counter = 0
    for i in range(1, iterations):
        states = [next_state_f(actual) for _ in range(50)]
        next_state = min(states, key=lambda s: value_f(s))
        val = value_f(next_state)
        prob = np.exp(-temp_max*(val - actual_val)/temp)
        if actual_val >= val or random.random() <= prob:
            actual, actual_val = next_state, val
            if best_val > val:
                # points.append((i, val))
                best, best_val = actual, actual_val
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
    # points.append((iterations, value_f(best)))
    # plot(points)
    return best


def fill_sudoku(sudoku, variables):
    if len(variables) == 0:
        return -1
    for xy in variables:
        sudoku[xy[0]][xy[1]] = 0

    for r in range(0, 7, 3):  # 0, 3, 6
        for c in range(0, 7, 3):
            left_numbers = set(range(1, 10)).difference(
                {x for row in sudoku[r:r+3] for x in row[c:c+3]})
            left_indexes = [xy for xy in variables if xy[0] in range(r, r+3) and xy[1] in range(c, c+3)]
            for xy, num in zip(np.random.permutation(left_indexes), left_numbers):
                sudoku[xy[0]][xy[1]] = num
    return 0


def generate_state(sudoku, variables):
    new_state = [row[:] for row in sudoku]

    indexes = []
    while len(indexes) < 2:
        r = random.choice(range(0, 7, 3))
        c = random.choice(range(0, 7, 3))
        indexes = [xy for xy in variables if xy[0] in range(r, r+3) and xy[1] in range(c, c+3)]

    xy1, xy2 = random.sample(indexes, 2)
    new_state[xy1[0]][xy1[1]], new_state[xy2[0]][xy2[1]] = \
        new_state[xy2[0]][xy2[1]], new_state[xy1[0]][xy1[1]]

    return new_state


def sudoku_value(sudoku):
    value = 0
    for row in sudoku:
        value += 9 - len(set(row))
    for column in range(9):
        value += 9 - len({sudoku[x][column] for x in range(9)})
    return value


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

    variables = [(r, c) for c in range(9) for r in range(9)
                 if sudoku[r][c] == 0]
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
