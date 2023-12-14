# %% imports
from IPython import get_ipython

get_ipython().run_line_magic("matplotlib", "widget")
# %matplotlib widget


from dataclasses import dataclass
from typing import Callable, Iterable

import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import DisplayHandle
from ipywidgets import interactive

vectors = np.array([[3, 4], [1, 3]])


# %% functions
def get_title(vec1, vec2):
    return f"{vec1} {vec2}"


# %% Classes
@dataclass
class Job:
    p: int
    w: int

    @property
    def cost(self):
        return self.p * self.w


Jobs = Iterable[Job]
# %% Graphing

# Displaying the plot and its vectors
figure = plt.figure()
# line_1 = plot_vec(vectors[1 - 1], format_label("Vector 1", vectors[1 - 1]))
# line_2 = plot_vec(vectors[2 - 1], format_label("Vector 2", vectors[2 - 1]))
# plt.legend()
# plt.title(get_title(vectors[1 - 1], vectors[2 - 1]))
plt.grid()
plt.show()

# %% Controls

jobs = {1: Job(1, 2), 2: Job(3, 4)}
functions = {"lower_bound": False}
extra_options = {"step_size": 1}


def calc_lower_bound(*jobs: Job) -> Callable[[float], float]:
    j_max = max([j.cost for j in jobs])
    return lambda i: j_max / i


def calc_upper_bound(*vectors: Job) -> Callable[[float], float]:
    return NotImplemented


def approx_lower_bound(*vectors: Job) -> Callable[[float], float]:
    return NotImplemented


def approx_upper_bound(*vectors: Job) -> Callable[[float], float]:
    return NotImplemented


name_to_func = {
    "analytical_lower_bound": calc_lower_bound,
    "analytical_upper_bound": calc_upper_bound,
    "numerical_lower_bound": approx_lower_bound,
    "numerical_upper_bound": approx_upper_bound,
}


def update_plot():
    vec1: Job = jobs[1]
    vec2: Job = jobs[2]
    figure.clf()
    plt.scatter(vec1.p, vec1.w, c="red", label="job 1")
    plt.scatter(vec2.p, vec2.w, c="blue", label="job 2")

    if functions["lower_bound"]:
        step_size = extra_options["step_size"]
        lower_bound_func = calc_lower_bound(vec1, vec2)
        x_data = np.arange(0.1, 25, step_size)

        y_data = lower_bound_func(x_data)
        plt.plot(x_data, y_data, label="lower_bound")
    plt.title(f"{vec1}, {vec2}")
    plt.grid()
    plt.legend()
    plt.xlim(left=0, right=21)
    plt.ylim(bottom=0, top=21)
    plt.draw()


def handle_slider_event(p1, w1, p2, w2):
    # Here, we are repacking the coordinates into two vectors and processing the change with do_update.
    jobs[1] = Job(p1, w1)
    jobs[2] = Job(p2, w2)
    update_plot()


def handle_button_event(**kwargs):
    functions["lower_bound"] = kwargs["lower_bound"]
    extra_options["step_size"] = kwargs["step_size"]
    update_plot()
    update_control("starting_jobs", create_starting_jobs_controls)


def update_control(name: str, func: Callable):
    if "handle" in extra_options:
        extra_options["handle"].update(func())


def int_slider_config(value):
    print(f"updating {extra_options['step_size']}")
    return widgets.FloatSlider(
        min=1, max=20, step=extra_options["step_size"], value=value
    )


def button_config(value):
    return widgets.ToggleButton(value)


def float_slider_config(value):
    return widgets.FloatLogSlider(min=-2, max=0, step=1)


controls = {}


def create_starting_jobs_controls():
    return interactive(
        handle_slider_event,
        p1=int_slider_config(jobs[1].p),
        w1=int_slider_config(jobs[1].w),
        p2=int_slider_config(jobs[2].p),
        w2=int_slider_config(jobs[2].w),
    )


controls["starting_jobs"] = create_starting_jobs_controls()

controls["bound"] = interactive(
    handle_button_event,
    lower_bound=button_config(functions["lower_bound"]),
    step_size=float_slider_config(1),
)
handle = DisplayHandle()
extra_options["handle"] = handle
for key, val in controls.items():
    handle.display(val)

# print(extra_options)
# %%
