import random
import numpy as np
import matplotlib.pyplot as plt


def main():
    low = 0
    high = 1000
    points = generate_points_groups(20, 3, 0.3, 10, 10)
    plot(points, 'red')
    result = simulanneal(points, arbitrary_swap, value, high, low,
                linear_probability, temp_change, 10000)
    plot(result, 'blue')


def plot(points, color='b', plot_last=True):
    x, y = zip(*points)
    plt.plot(x, y, 'ro')
    for i in range(0, len(points) - 1):
        plt.plot([points[i][0], points[(i+1)][0]], [points[i][1], points[(i+1)][1]], lw=1, c=color)
    if plot_last:
        i = len(points) - 1
        plt.plot([points[i][0], points[0][0]], [points[i][1], points[0][1]], lw=1, c=color)
    plt.show()


def generate_points_groups(n, m, r, x_max, y_max):
    def generate_group(n, r):
        x, y = [np.random.random() * (_max - 2 * r) + r for _max in (x_max, y_max)]
        return list(zip(*[[a + (np.random.random() - 0.5) * 2 * r for _ in range(0, n)] for a in (x, y)]))

    if r > x_max / 2 or r > y_max / 2 or m > n:
        return []

    groups_sizes = [n // m for _ in range(0, m)]
    for i in range(0, n % m):
        groups_sizes[i] += 1

    points = []
    for group_size in groups_sizes:
        points.extend(generate_group(group_size, r))
    np.random.shuffle(points)
    return points


def generate_points_with_gaussian_dist(n, loc, scale, x_max, y_max):
    def gen(n, loc, scale, _max):
        l = []
        while len(l) < n:
            l.extend([x for x in np.random.normal(loc, scale, n - len(l))
                      if 0 < x < _max])
        return l[:n]

    return list(zip(*[gen(n, loc, scale, _max) for _max in (x_max, y_max)]))


def generate_points_with_uniform_dist(n, x_max, y_max):
    return list(zip(*[np.random.uniform(0, _max, n)
                      for _max in (x_max, y_max)]))


def consecutive_swap(state):
    a = np.random.randint(1, len(state) - 2)
    new_state = state[:]
    new_state[a], new_state[a + 1] = new_state[a + 1], new_state[a]
    return new_state


def arbitrary_swap(state):
    a = random.randint(1, len(state) - 1)
    b = random.randint(1, len(state) - 2)
    if b >= a:
        b += 1
    new_state = state[:]
    new_state[a], new_state[b] = new_state[b], new_state[a]
    return new_state


def value(state):
    val = 0
    for i in range(0, len(state)):
        val += np.sqrt(sum((x - y)**2 for x, y in zip(state[i], state[(i+1)%len(state)])))
    return val


def linear_probability(t, temp_max, temp_min):
    return .5 * np.sqrt((t - temp_min) / (temp_max - temp_min))


def temp_change(t):
    return t * 0.998


def simulanneal(start_state, next_state_func, value_func, temp_max, temp_min,
                probability_func, temp_change_func, iterations):
    actual_state = start_state
    best_state = actual_state
    temp = temp_max
    points = [(0, value(actual_state))]
    for i in range(0, iterations):
        next_state = next_state_func(actual_state)
        probability = probability_func(temp, temp_max, temp_min)
        val = value_func(next_state)
        # probability = np.exp(-(val - value_func(actual_state))/temp)
        if value_func(actual_state) > val \
                or random.random() < probability:
            actual_state = next_state
            points.append((i, val))
            if value_func(best_state) > val:
                best_state = actual_state
        temp = temp_change_func(temp)
    points.append((iterations, value(best_state)))
    plot(points, plot_last=False)
    return best_state


if __name__ == "__main__":
    main()