from itertools import permutations

import matplotlib.patches as mpatches
import numpy as np
from matplotlib import pyplot as plt

from .utils import explode


def big_boom(n_voxels, face_colors, edge_colors=None):
    filled = explode(np.ones(n_voxels.shape))
    if edge_colors is None:
        edge_colors = face_colors
    face_colors = explode(face_colors)
    edge_colors = explode(edge_colors)
    return filled, face_colors, edge_colors


def create_voxels(arr):
    x, y, z = np.indices(np.array(arr.shape) + 1).astype(float) // 2
    size = 0.1
    x[0::2, :, :] += size
    y[:, 0::2, :] += size
    z[:, :, 0::2] += size

    size = 1 - size
    x[1::2, :, :] += size
    y[:, 1::2, :] += size
    z[:, :, 1::2] += size
    return x, y, z


def viz(filled, face_colors, edge_colors, **legend):
    # Shrink the gaps
    x, y, z = create_voxels(filled)

    ax = plt.figure().add_subplot(projection="3d")
    ax.voxels(x, y, z, filled, facecolors=face_colors, edgecolors=edge_colors)
    ax.set_aspect("equal")

    prepare_plot(legend, ax)
    plt.show()


def prepare_plot(legend, ax):
    patches = [mpatches.Patch(color=k, label=v) for k, v in legend.items()]
    ax.legend(handles=patches, loc="best")
    plt.tight_layout(pad=0)
    manager = plt.get_current_fig_manager()
    assert manager is not None
    manager.full_screen_toggle()


def partial_viz(filled, face_colors, edge_colors, **legend):
    # Shrink the gaps
    x, y, z = create_voxels(filled)

    n = filled.shape[0] + 1
    conditional = [
        [[x < y and x < z and y < z for x in range(n)] for y in range(n)]
        for z in range(n)
    ]
    x *= conditional

    ax = plt.figure().add_subplot(projection="3d")
    ax.voxels(x, y, z, filled, facecolors=face_colors, edgecolors=edge_colors)
    ax.set_aspect("equal")

    prepare_plot(legend, ax)
    plt.show()


def color_current_position(color, p_colors, position):
    for pos in permutations(position):
        p_colors[*pos] = color


def color_faces(color, p_colors, positions):
    for position in positions:
        p_colors[*position] = color
