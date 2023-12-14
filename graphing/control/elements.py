import ipywidgets as widgets


def range_slider_config(name: str, val=None, min=0, max=20, step=1):
    if val is None:
        val = (min, max)
    return widgets.IntRangeSlider(
        min=min, max=max, step=step, value=val, description=name
    )


def int_slider_config(min=1, max=20, step=1, val=0):
    return widgets.IntSlider(min=min, max=max, step=step, value=val)


def button_config(name: str, val=False):
    return widgets.ToggleButton(val, description=name)


def log_slider_config(min=-2, max=0, step=1):
    return widgets.FloatLogSlider(min=min, max=max, step=step)


from enum import Enum


class Gui:
    class Colors(Enum):
        BLUE = "blue"
        ORANGE = "orange"
        GREEN = "green"
        RED = "red"
        PURPLE = "purple"
        BROWN = "brown"
        PINK = "pink"
        GRAY = "gray"
        OLIVE = "olive"
        CYAN = "cyan"
        ALL = [
            "blue",
            "orange",
            "green",
            "red",
            "purple",
            "brown",
            "pink",
            "gray",
            "olive",
            "cyan",
        ]

    class Configuration:
        pass
