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
from graphing.functions.bound import analytical, numerical
from partial_scheduling.models.job import Job

_ = (ipython := get_ipython()) is not None and ipython.run_line_magic(
    "matplotlib", "widget"
)


# %% Constants
HANDLE = DisplayHandle()
FIGURE = plt.figure()
VECTORS = np.array([[3, 4], [1, 3]])
JOBS = {1: Job(1, 2), 2: Job(3, 4)}


# %% Controls info


extra_options = {"step_size": 1}
window_zoom = {"x": (0, 20), "y": (0, 20)}
name_to_func = {
    "n": {"ub": numerical.upper_bound, "lb": numerical.lower_bound},
    "a": {"ub": analytical.upper_bound1, "lb": analytical.lower_bound},
    "o": {"b": analytical.upper_bound3, "sb": ana.viable},
}
functions = {f"{k}_{k2}": False for k, v in name_to_func.items() for k2 in v}
LETTER_TO_NAME = {
    "a": "analytical",
    "n": "numerical",
    "o": "other",
    "lb": "lower bound",
    "ub": "upper bound",
    "b": "switch bound",
    "sb": "super bound",
}
y_data = {k: {k2: np.array([]) for k2 in v} for k, v in name_to_func.items()}
changed = {k: {k2: False for k2 in v} for k, v in name_to_func.items()}
print(changed)


# %% Controls
def title(k1, k2):
    return f"{LETTER_TO_NAME[k1]} {LETTER_TO_NAME[k2]}"


def update_plot():
    vec1 = JOBS[1]
    vec2 = JOBS[2]
    FIGURE.clf()
    plt.scatter(vec1.p, vec1.w, c="red", label="job 1")
    plt.scatter(vec2.p, vec2.w, c="blue", label="job 2")
    if any(functions.values()):
        step_size = extra_options["step_size"]
        x_data = np.arange(0.1, 25, step_size)
        for func_name, func_is_set in functions.items():
            if func_is_set:
                sort_of_type, bound = func_name.split("_")
                if changed[sort_of_type][bound]:
                    y_data[sort_of_type][bound] = name_to_func[sort_of_type][bound](
                        vec1, vec2
                    )(x_data)
                    changed[sort_of_type][bound] = False
                plt.plot(
                    x_data,
                    y_data[sort_of_type][bound],
                    "--",
                    label=title(sort_of_type, bound),
                    alpha=0.5,
                )
        for k, v in name_to_func.items():
            if "lb" in v and "ub" in v and all(functions[f"{k}_{k2}"] for k2 in v):
                lower_bound = y_data[k]["lb"]
                upper_bound = y_data[k]["ub"]
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
    def inner_func(value):
        window_zoom[name] = value
        update_plot()

    return inner_func


def handle_extra_event(name: str):
    def inner_func(value):
        extra_options[name] = value
        recompute_lines()
        update_plot()

    def recompute_lines():
        for k, v in changed.items():
            for k2 in v:
                changed[k][k2] = True

    return inner_func


def range_slider_config(name: str, value=None, min_val=0, max_val=20, step=1):
    if value is None:
        value = (min_val, max_val)
    return widgets.IntRangeSlider(
        min=min_val, max=max_val, step=step, value=value, description=name
    )


def int_slider_config(
    text=None, min_val=1, max_val=20, step=extra_options["step_size"], val=0
):
    if text is not None:
        return widgets.IntSlider(
            min=min_val, max=max_val, step=step, value=val, description=text
        )
    return widgets.IntSlider(min=min_val, max=max_val, step=step, value=val)


def button_config(name: str, value=False):
    return widgets.ToggleButton(value, description=name)


def log_slider_config(text=None, min_val=-2, max_val=0, step=1):
    if text is not None:
        return widgets.FloatLogSlider(
            min=min_val, max=max_val, step=step, description=text
        )
    return widgets.FloatLogSlider(min=min_val, max=max_val, step=step)


controls = {}


def create_starting_jobs_controls():
    return widgets.HBox(
        [
            interactive(
                handle_slider_event(1),
                p=int_slider_config("p1"),
                w=int_slider_config("w1"),
            ),
            interactive(
                handle_slider_event(2),
                p=int_slider_config("p2"),
                w=int_slider_config("w2"),
            ),
        ]
    )


controls["starting_jobs"] = create_starting_jobs_controls()

controls["bound"] = widgets.VBox(
    [
        widgets.HBox(
            [
                interactive(
                    handle_button_event("a_lb"),
                    use=button_config("A lower bound"),
                ),
                interactive(
                    handle_button_event("a_ub"),
                    use=button_config("A upper bound"),
                ),
            ],
        ),
        widgets.HBox(
            [
                interactive(
                    handle_button_event("n_lb"),
                    use=button_config("N lower bound"),
                ),
                interactive(
                    handle_button_event("n_ub"),
                    use=button_config("N upper bound"),
                ),
            ],
        ),
        widgets.HBox(
            [
                interactive(
                    handle_button_event("o_b"),
                    use=button_config("Switch bound"),
                ),
                interactive(
                    handle_button_event("o_sb"),
                    use=button_config("Super bound"),
                ),
            ]
        ),
        interactive(
            handle_extra_event("step_size"),
            val=log_slider_config("Precision"),
        ),
    ]
)
controls["window"] = widgets.VBox(
    [
        interactive(handle_range_event("x"), value=range_slider_config("x zoom")),
        interactive(handle_range_event("y"), value=range_slider_config("y zoom")),
    ]
)

logging.basicConfig(level=logging.CRITICAL)

for key, val in controls.items():
    print(key.title())
    HANDLE.display(val)

# %%
