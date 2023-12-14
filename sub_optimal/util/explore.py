from itertools import permutations
import numpy as np


def explore(explored, current_position, positions):
    for pos in permutations(current_position):
        explored[*pos] = False
    for pos in positions:
        explored[*pos] = False


def color_exploration(explored, explored_color, unexplored_color):
    return np.where(explored, explored_color, unexplored_color)
