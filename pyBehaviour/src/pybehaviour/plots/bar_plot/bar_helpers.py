# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

from matplotlib.axes import Axes

from ..PlotSettings import PlotSettings
from ..features import convert_rect_to_grad
from ...logger import logger
from ...styling import change_lighness



# ================================================================
# 1. Section: Generate Bars
# ================================================================
def add_bars(
    data_dict: dict,
    ax: Axes,
    x: np.ndarray,
    plt_settings: PlotSettings
) -> Axes:
    multiplier = 0
    for attribute, measurement in data_dict.items():
        print(attribute, measurement)
        # 1. Computes the offset for bar placing on the x axis
        offset = (plt_settings.width + plt_settings.gap) * multiplier

        # 2. Computes the rects as fading gradients
        rects = ax.bar(x + offset, measurement, plt_settings.width, label=attribute, color="none")
        rects = convert_rect_to_grad(rects, ax, measurement, plt_settings.colors[multiplier])

        # 3. To show or not the measurement value at the top
        if plt_settings.show_rects:
            ax.bar_label(rects, padding=3, label_type="center")
        multiplier += 1

    return ax

def add_points(
    data_dict: dict,
    ax: Axes,
    x: np.ndarray,
    plt_settings: PlotSettings
) -> Axes:
    multiplier = 0
    for attribute, measurement in data_dict.items():

        # 1. Computes the offset for bar placing on the x axis
        offset = (plt_settings.width + plt_settings.gap) * multiplier

        # 2. Computes the rects as fading gradients
        for idx, msr in enumerate(measurement):
            color = plt_settings.colors[multiplier]
            soft_color = change_lighness(color, factor=0.10)

            jitter = np.random.uniform(-0.015, 0.015, size=len(msr))

            ax.scatter(
                np.array([int(x[idx])] * len(msr)) + offset + jitter,
                msr,
                s=75,
                label=attribute,
                color=soft_color,
                zorder=5,
                alpha=0.8,
                edgecolor="none"
            )

        multiplier += 1

    return ax



# ================================================================
# 2. Section: Axis Management
# ================================================================
def get_y_axis(
    ax: Axes,
    data_dict: dict,
    plt_settings: PlotSettings
) -> Axes:
    ax.set_ylabel(plt_settings.ylabel)
    if plt_settings.vertical_offset == 0 and plt_settings.ylim is not None:
        ax.set_ylim(plt_settings.ylim)
        ax.set_yticks([0,
            int(plt_settings.ylim[1])])
    else:
        max_value = max(np.nanmax(arr) for arr in data_dict.values())
        ymax = max_value + plt_settings.vertical_offset
        ax.set_ylim((0, int(ymax)))
        ax.set_yticks([0, int(ymax)])

    return ax



# ================================================================
# 3. Section: Assertions
# ================================================================
def assert_same_keys(dict_1: dict, dict_2: dict) -> None:
    if(dict_1.keys != dict_2.keys):
        logger.warning("Both groups have different sub-group labels, some bars migh be empty\n"
            f"Group 1 Keys: {dict_1.keys()}"
            f"Group 2 Keys: {dict_2.keys()}"
        )
