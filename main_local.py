"""
# Sources:
- [IPython](https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html)
- [ipywidgets](https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20Custom.html#domwidget-valuewidget-and-widget)
"""
# %% imports
import logging

import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
from IPython import get_ipython
from IPython.display import DisplayHandle
from ipywidgets import interactive

from graphing.control.elements import Gui
from graphing.functions.local.calc4jobs import job3, job4
from partial_scheduling.models.job import Job

_ = (ipython := get_ipython()) is not None and ipython.run_line_magic(
    "matplotlib", "widget"
)

# %% This is our magic Value
NUMBER_OF_JOBS = 4 + 1
jobs = [(2, 37), (2, 40), (2, 42), (23, 4), (5, 20), (32, 3), (14, 7)]

# %% Constants
MAX_VALUES = 100
HANDLE = DisplayHandle()
FIGURE = plt.figure()
JOBS = {i: Job(1, 1) for i in range(1, NUMBER_OF_JOBS)}
# %% Controls info


extra_options = {"step_size": 1}
window_zoom = {"x": (0, 20), "y": (0, 20)}
NAME_TO_FUNC: dict[str, dict] = {
    "3": {
        "ub": job3.upper_bound,
        "lb": job3.lower_bound,
        "lb_1": job3.lower_bound1,
        "lb_2": job3.lower_bound2,
        "lb_3": job3.lower_bound3,
        "lb_4": job3.lower_bound4,
    },
    "4": {
        "ub": job4.upper_bound,
        "lb": job4.lower_bound,
        "lb_1": job4.lower_bound1,
        "lb_2": job4.lower_bound2,
        "lb_3": job4.lower_bound3,
        "lb_4": job4.lower_bound4,
    },
}
functions = {f"{k}_{k2}": False for k, v in NAME_TO_FUNC.items() for k2 in v}
LETTER_TO_NAME = {
    "n": "Numerical",
    "o": "Other",
    "lb": "Lower",
    "ub": "Upper",
    "3": "3th job",
    "4": "4th job",
}
y_data = {k: {k2: np.array([]) for k2 in v} for k, v in NAME_TO_FUNC.items()}
changed = {k: {k2: False for k2 in v} for k, v in NAME_TO_FUNC.items()}


# %% Controls
def title(k1: str, k2: str):
    return f"{LETTER_TO_NAME[k1]} {LETTER_TO_NAME[k2]}"


def title2(k1: str, k2: str):
    _k2 = k2.split("_")
    return f"{LETTER_TO_NAME[k1]} {LETTER_TO_NAME[_k2[0]]} " + " ".join(_k2[1:])


def update_plot():
    FIGURE.clf()
    for k, v in JOBS.items():
        plt.scatter(v.p, v.w, c=Gui.Colors.ALL[k - 1], label=f"job {k}")
    if any(functions.values()):
        step_size = extra_options["step_size"]
        x_data = np.arange(0.1, window_zoom["x"][1], step_size)
        for func_name, is_used in functions.items():
            if is_used:
                comp = func_name.split("_")
                comp2 = "_".join(comp[1:])
                if changed[comp[0]][comp2]:
                    bound_function = NAME_TO_FUNC[comp[0]][comp2]
                    y_data[comp[0]][comp2] = bound_function(*JOBS.values())(x_data)
                    changed[comp[0]][comp2] = False
                plt.plot(
                    x_data,
                    y_data[comp[0]][comp2],
                    "--",
                    label=title2(comp[0], comp2),
                    alpha=0.5,
                )
        for func_name, is_used in NAME_TO_FUNC.items():
            if (
                "lb" in is_used
                and "ub" in is_used
                and all(functions[f"{func_name}_{k2}"] for k2 in ("lb", "ub"))
            ):
                lower_bound = y_data[func_name]["lb"]
                upper_bound = y_data[func_name]["ub"]
                plt.fill_between(
                    x_data,
                    lower_bound,
                    upper_bound,
                    where=(upper_bound > lower_bound),
                    color="blue",
                    alpha=0.2,
                    interpolate=True,
                )
                plt.fill_between(
                    x_data,
                    lower_bound,
                    upper_bound,
                    where=(upper_bound < lower_bound),
                    color="red",
                    alpha=0.2,
                    interpolate=True,
                )

    # if is_valid(*JOBS.values()):
    plt.title("Valid")
    # else:
    # plt.title(f"Invalid {calc_constraints(*JOBS.values()).index(False) + 1}")
    plt.grid()
    plt.legend()
    plt.xlabel("processing_time")
    plt.ylabel("weight")
    plt.xlim(window_zoom["x"])
    plt.ylim(window_zoom["y"])
    plt.draw()


def is_valid(*vectors: Job):
    return all(calc_constraints(*vectors))


def calc_constraints(*vectors):
    constraints = []
    vec1 = vectors[0]
    vec2 = vectors[1]
    constraints += [vec1.ratio <= vec2.ratio]
    for i, v in enumerate(vectors[2:]):
        x = v.p
        y = v.w
        lb = NAME_TO_FUNC[f"a{i+3}"]["lb"](*vectors)(x)
        ub = NAME_TO_FUNC[f"a{i+3}"]["ub"](*vectors)(x)
        constraints += [lb <= y <= ub]
    return constraints


def handle_slider_event(i):
    def inner_func(p: int, w: int):
        JOBS[i] = Job(p, w)
        for k, v in changed.items():
            for k2 in v:
                changed[k][k2] = True
        update_plot()

    return inner_func


def handle_button_event(name: str):
    def inner_func(use: bool):
        functions[name] = use
        update_plot()

    return inner_func


def handle_range_event(name: str):
    def inner_func(val):
        window_zoom[name] = val
        update_plot()

    return inner_func


def handle_extra_event(name: str):
    def inner_func(val):
        extra_options[name] = val
        recompute_lines()
        update_plot()

    def recompute_lines():
        for k, v in changed.items():
            for k2 in v:
                changed[k][k2] = True

    return inner_func


def range_slider_config(name: str, val=None, min_val=0, max_val=MAX_VALUES, step=1):
    if val is None:
        val = (min_val, max_val)
    return widgets.IntRangeSlider(
        min=min_val, max=max_val, step=step, value=val, description=name
    )


def int_slider_config(
    text=None, min_value=1, max_value=MAX_VALUES, step=extra_options["step_size"], val=0
):
    if text is not None:
        return widgets.IntSlider(
            min=min_value, max=max_value, step=step, value=val, description=text
        )
    return widgets.IntSlider(min=min_value, max=max_value, step=step, value=val)


def button_config(name: str, val=False):
    return widgets.ToggleButton(val, description=name, tooltip=name)


def log_slider_config(text=None, min_value=-2, max_value=0, step=1):
    if text is not None:
        return widgets.FloatLogSlider(
            min=min_value, max=max_value, step=step, description=text
        )
    return widgets.FloatLogSlider(min=min_value, max=max_value, step=step)


UI = {}


def create_starting_jobs_controls():
    return widgets.HBox(
        [
            interactive(
                handle_slider_event(i),
                p=int_slider_config(f"p{i}", val=jobs[i - 1][0]),
                w=int_slider_config(f"w{i}", val=jobs[i - 1][1]),
            )
            for i in range(1, NUMBER_OF_JOBS)
        ]
    )


UI["starting_jobs"] = create_starting_jobs_controls()
UI["bound"] = widgets.VBox(
    [
        widgets.HBox(
            [
                interactive(
                    handle_button_event(f"{k}_{k2}"),
                    use=button_config(title2(k, k2)),
                )
                for k2 in v
            ],
        )
        for k, v in NAME_TO_FUNC.items()
    ]
)
UI["precision"] = interactive(
    handle_extra_event("step_size"),
    val=log_slider_config("Precision"),
)
UI["window"] = widgets.VBox(
    [
        interactive(handle_range_event("x"), val=range_slider_config("x zoom")),
        interactive(handle_range_event("y"), val=range_slider_config("y zoom")),
    ]
)

logging.basicConfig(level=logging.CRITICAL)

for widget_name, widget in UI.items():
    print(widget_name.title())
    HANDLE.display(widget)

# %%
