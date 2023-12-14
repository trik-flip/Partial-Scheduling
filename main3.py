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

from graphing.functions.area import analytical as ana
from graphing.functions.bound import analytical, calc4jobs, calc5jobs, n_jobs, numerical
from partial_scheduling.models.job import Job

_ = (ipython := get_ipython()) is not None and ipython.run_line_magic(
    "matplotlib", "widget"
)


# %% Constants
MAX_VALUES = 100
HANDLE = DisplayHandle()
FIGURE = plt.figure()
JOBS = {
    1: Job(1, 2),
    2: Job(3, 4),
    3: Job(3, 4),
    4: Job(3, 4),
}
COLORS = ["b", "g", "r", "c", "m", "y", "k", "w"]
COLORS = [
    "tab:blue"
    "tab:orange"
    "tab:green"
    "tab:red"
    "tab:purple"
    "tab:brown"
    "tab:pink"
    "tab:gray"
    "tab:olive"
    "tab:cyan"
]
# %% Controls info


extra_options = {"step_size": 1}
window_zoom = {"x": (0, 20), "y": (0, 20)}
name_to_func: dict[str, dict] = {
    "n": {"ub": numerical.upper_bound, "lb": numerical.lower_bound},
    "a": {
        "lb": analytical.lower_bound,
        "lb_1": analytical.lower_bound1,
        "ub": analytical.upper_bound,
        "ub_1": analytical.upper_bound1,
        "ub_2": analytical.upper_bound2,
        "ub_3": analytical.upper_bound3,
    },
    "e": {
        "lb_1": calc4jobs.lower_bound1,
        "lb_2": calc4jobs.lower_bound2,
        "lb_3": calc4jobs.lower_bound3,
        "lb_4": calc4jobs.lower_bound4,
        "lb": calc4jobs.lower_bound,
        "ub": calc4jobs.upper_bound,
    },
    "e2": {
        "lb_1": calc5jobs.lower_bound1,
        "lb_2": calc5jobs.lower_bound2,
        "lb_3": calc5jobs.lower_bound3,
        "lb_4": calc5jobs.lower_bound4,
        "lb_5": calc5jobs.lower_bound5,
        "lb": calc5jobs.lower_bound,
        "ub": calc5jobs.upper_bound,
    },
    "e3": {
        "lb": n_jobs.lower_bound,
        "ub": n_jobs.upper_bound,
    },
    "o": {"sb": ana.viable},
}
functions = {f"{k}_{k2}": False for k, v in name_to_func.items() for k2 in v}
LETTER_TO_NAME = {
    "a": "Analytical",
    "n": "Numerical",
    "o": "Other",
    "lb": "lower bound",
    "ub": "upper bound",
    "b": "switch bound",
    "sb": "super bound",
    "e": "4 jobs",
    "e2": "5 jobs",
    "e3": "N jobs",
}
y_data = {k: {k2: np.array([]) for k2 in v} for k, v in name_to_func.items()}
changed = {k: {k2: False for k2 in v} for k, v in name_to_func.items()}


# %% Controls
def title(k1: str, k2: str):
    return f"{LETTER_TO_NAME[k1]} {LETTER_TO_NAME[k2]}"


def title2(k1: str, k2: str):
    _k2 = k2.split("_")
    return f"{LETTER_TO_NAME[k1]} {LETTER_TO_NAME[_k2[0]]} " + " ".join(_k2[1:])


def update_plot():
    vec1 = JOBS[1]
    vec2 = JOBS[2]
    FIGURE.clf()
    for k, v in JOBS.items():
        plt.scatter(v.p, v.w, c=COLORS[k - 1], label=f"job {k}")
    # plt.scatter(vec2.p, vec2.w, c="blue", label="job 2")
    # plt.scatter(vec3.p, vec3.w, c="green", label="job 3")
    # plt.scatter(vec4.p, vec4.w, c="yellow", label="job 4")
    if any(functions.values()):
        step_size = extra_options["step_size"]
        x_data = np.arange(0.1, window_zoom["x"][1], step_size)
        for func_name, is_used in functions.items():
            if is_used:
                comp = func_name.split("_")
                comp2 = "_".join(comp[1:])
                if changed[comp[0]][comp2]:
                    y_data[comp[0]][comp2] = name_to_func[comp[0]][comp2](
                        JOBS.values()
                    )(x_data)
                    changed[comp[0]][comp2] = False
                plt.plot(
                    x_data,
                    y_data[comp[0]][comp2],
                    "--",
                    label=title2(comp[0], comp2),
                    alpha=0.5,
                )
        for func_name, is_used in name_to_func.items():
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
    if vec1.ratio <= vec2.ratio:
        plt.title(f"Valid, {vec1}, {vec2}")
    else:
        plt.title(f"Invalid, {vec1}, {vec2}")
    plt.grid()
    plt.legend()
    plt.xlabel("processing_time")
    plt.ylabel("weight")
    plt.xlim(window_zoom["x"])
    plt.ylim(window_zoom["y"])
    plt.draw()


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
                handle_slider_event(i + 1),
                p=int_slider_config(f"p{i+1}"),
                w=int_slider_config(f"w{i+1}"),
            )
            for i in range(4)
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
        for k, v in name_to_func.items()
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
