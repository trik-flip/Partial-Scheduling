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
from graphing.functions.bound import analytical, calc4jobs, numerical
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
}


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
    vec3 = JOBS[3]
    FIGURE.clf()
    plt.scatter(vec1.p, vec1.w, c="red", label="job 1")
    plt.scatter(vec2.p, vec2.w, c="blue", label="job 2")
    plt.scatter(vec3.p, vec3.w, c="green", label="job 3")
    if any(functions.values()):
        step_size = extra_options["step_size"]
        x_data = np.arange(0.1, window_zoom["x"][1], step_size)
        for func_name, func_is_set in functions.items():
            if func_is_set:
                comp = func_name.split("_")
                comp2 = "_".join(comp[1:])
                if changed[comp[0]][comp2]:
                    y_data[comp[0]][comp2] = name_to_func[comp[0]][comp2](
                        vec1, vec2, vec3
                    )(x_data)
                    changed[comp[0]][comp2] = False
                plt.plot(
                    x_data,
                    y_data[comp[0]][comp2],
                    "--",
                    label=title2(comp[0], comp2),
                    alpha=0.5,
                )
        for k, v in name_to_func.items():
            if (
                "lb" in v
                and "ub" in v
                and all(functions[f"{k}_{k2}"] for k2 in ("lb", "ub"))
            ):
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
        # t_name, bound = name.split("_")
        # changed[t_name][bound] = True
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


def range_slider_config(name: str, value=None, min_val=0, max_val=MAX_VALUES, step=1):
    if value is None:
        value = (min_val, max_val)
    return widgets.IntRangeSlider(
        min=min_val, max=max_val, step=step, value=value, description=name
    )


def int_slider_config(
    text=None, min_val=1, max_val=MAX_VALUES, step=extra_options["step_size"], val=0
):
    if text is not None:
        return widgets.IntSlider(
            min=min_val, max=max_val, step=step, value=val, description=text
        )
    return widgets.IntSlider(min=min_val, max=max_val, step=step, value=val)


def button_config(name: str, value=False):
    return widgets.ToggleButton(value, description=name, tooltip=name)


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
                handle_slider_event(i + 1),
                p=int_slider_config(f"p{i+1}"),
                w=int_slider_config(f"w{i+1}"),
            )
            for i in range(3)
        ]
    )


controls["starting_jobs"] = create_starting_jobs_controls()
controls["bound"] = widgets.VBox(
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
# controls["bound"] = widgets.VBox(
#     [
#         widgets.HBox(
#             [
#                 interactive(
#                     handle_button_event("a_lb"),
#                     use=button_config("A lower bound"),
#                 ),
#                 interactive(
#                     handle_button_event("a_ub"),
#                     use=button_config("A upper bound"),
#                 ),
#             ],
#         ),
#         widgets.HBox(
#             [
#                 interactive(
#                     handle_button_event("n_lb"),
#                     use=button_config("N lower bound"),
#                 ),
#                 interactive(
#                     handle_button_event("n_ub"),
#                     use=button_config("N upper bound"),
#                 ),
#             ],
#         ),
#         widgets.HBox(
#             [
#                 interactive(
#                     handle_button_event("o_b"),
#                     use=button_config("Switch bound"),
#                 ),
#                 interactive(
#                     handle_button_event("o_sb"),
#                     use=button_config("Super bound"),
#                 ),
#             ]
#         ),
#     ]
# )
controls["precision"] = interactive(
    handle_extra_event("step_size"),
    val=log_slider_config("Precision"),
)
controls["window"] = widgets.VBox(
    [
        interactive(handle_range_event("x"), val=range_slider_config("x zoom")),
        interactive(handle_range_event("y"), val=range_slider_config("y zoom")),
    ]
)

logging.basicConfig(level=logging.CRITICAL)

for key, val in controls.items():
    print(key.title())
    HANDLE.display(val)

# %%
