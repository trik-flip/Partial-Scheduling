from itertools import permutations

import numpy as np


def compute_possible_positions(current_position: list[int], N: int):
    possible_positions = []
    for index, val in enumerate(current_position):
        others = current_position[:index] + current_position[index + 1 :]
        new_position = [
            current_position[:index] + [j] + current_position[index + 1 :]
            for j in range(N)
            if j != val and j not in others
        ]
        possible_positions += new_position
    all_possible_positions = []
    for possible_position in possible_positions:
        for perm in permutations(possible_position):
            all_possible_positions += [perm]
    return all_possible_positions


def compute_next_position(current_position: list[int], N: int):
    copy = np.array(current_position)
    if not (current_position[-1] == N - 1 or current_position[-2] == N - 1):
        if current_position[-1] < current_position[-2]:
            copy[-1] += 2
        else:
            copy[-2] += 2
        return list(copy)
    return NotImplemented
