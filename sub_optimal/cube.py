import numpy as np
from util.explore import color_exploration, explore
from util.positions import compute_next_position, compute_possible_positions
from util.viz import big_boom, color_current_position, color_faces, viz

# Constants
LOW_OPACITY = "A0"
HIGH_OPACITY = "04"
INVISIBLE = "00"
C_NOT_POSSIBLE = "#FF0000" + INVISIBLE
C_CURRENT_POSITION = "#FFD65D" + LOW_OPACITY
C_SEARCH_SPACE = "#7A88CC" + LOW_OPACITY
C_REACHABLE_POSITION = "#4ec9b0" + LOW_OPACITY
N = 6
K = 3
# Constants dependant on constants
LEGEND_1 = {
    C_NOT_POSSIBLE[:-2] + "40": "Not Possible",
    C_CURRENT_POSITION: "Current Position",
    C_SEARCH_SPACE: "Search Space",
    C_REACHABLE_POSITION: "Reachable Position",
}
LEGEND_2 = {
    C_NOT_POSSIBLE[:-2] + "40": "Explored",
    C_SEARCH_SPACE: "Unexplored",
}


def initialize_space(n):
    arr = np.ones((n, n, n), dtype=bool)
    for index in range(n):
        arr[index, index, :] = False
        arr[:, index, index] = False
        arr[index, :, index] = False
    return arr


n_voxels = initialize_space(N)
explored = initialize_space(N)


face_colors = np.where(n_voxels, C_SEARCH_SPACE, C_NOT_POSSIBLE)
edge_colors = np.where(n_voxels, C_SEARCH_SPACE, C_NOT_POSSIBLE)
current_pos = [0, 1, 2]

for i in range(N - 2):
    all_possible_positions = compute_possible_positions(current_pos, N)
    color_faces(C_REACHABLE_POSITION, face_colors, all_possible_positions)
    color_current_position(C_CURRENT_POSITION, face_colors, current_pos)
    args = big_boom(n_voxels, face_colors, edge_colors)
    viz(*args, **LEGEND_1)
    # partial_viz(*args, **LEGEND_1)

    explore(explored, current_pos, all_possible_positions)
    exp_color = color_exploration(explored, C_SEARCH_SPACE, C_NOT_POSSIBLE)
    args = big_boom(explored, exp_color)
    # viz(*args, **LEGEND_2)
    # partial_viz(*args, **LEGEND_2)

    current_pos = compute_next_position(current_pos, N)
