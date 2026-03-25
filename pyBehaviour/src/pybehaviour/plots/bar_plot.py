# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np
from matplotlib import pyplot as plt

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ..logger import logger
from .features import convert_rect_to_grad, nice_legend



# ================================================================
# 1. Section: Functions
# ================================================================
def two_group_bar_plot(
    group_1_dict: dict,
    group_2_dict: dict,
    group_names: list[str] | np.ndarray,
    ylabel: str = "Metric",
    title: str = "Title of the Plot",
    fig_size: tuple = (8,8),
    ylim: tuple | None = None,
    show_rects: bool = True,
    colors: list[str] = ["NR_GREY", "NR_RED"],
    width: float = 0.25,
    gap: float = 0.0,
    vertical_offset: float = 0.0,
    show_legend: bool = True,
) -> tuple[Figure, Axes]:
    # 1. Make sure both groups have the same keys, if not just print a warning
    assert_same_keys(group_1_dict, group_2_dict)

    # 2. Builds a dict better suited for this
    sub_groups = sorted(group_1_dict.keys() | group_2_dict.keys())
    data_dict = build_data_dict(group_names, group_1_dict, group_2_dict, sub_groups)

    # 3. Define the group positioning
    x = np.arange(len(sub_groups))

    # 4. Initialize and fill the plot
    fig, ax = plt.subplots(layout='constrained', figsize=fig_size)

    # 5. Get sub-group bar positions and parameters
    add_bars(data_dict, ax, x, colors, show_rects, width, gap)

    # 6. Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_title(title)
    ax.set_aspect("auto")

    # 7. Define the Y lim and its ticks
    ax = get_y_axis(ax, ylabel, ylim, vertical_offset, data_dict)

    # 8. Define the X lim and its ticks
    ax.set_xticks(x + (width + gap)/2, sub_groups)
    ax.set_xlim(-width, len(sub_groups) - 1 + width * 2 + gap)
    ax.tick_params(axis='x', length=0)
    ax.spines["bottom"].set_visible(False)

    # 9. Builds the legend for better visualization
    if show_legend:
        ax = nice_legend(ax, colors, group_names)

    return fig, ax



# ──────────────────────────────────────────────────────
# 1.1 Subsection: Helper Functions
# ──────────────────────────────────────────────────────
def assert_same_keys(dict_1: dict, dict_2: dict) -> None:
    if(dict_1.keys != dict_2.keys):
        logger.warning("Both groups have different sub-group labels, some bars migh be empty\n"
            f"Group 1 Keys: {dict_1.keys()}"
            f"Group 2 Keys: {dict_2.keys()}"
        )

def build_data_dict(
    group_names: list[str] | np.ndarray | tuple,
    dict_1: dict,
    dict_2: dict,
    sub_groups: list[str]
) -> dict:
    return {
            group_names[0]: [dict_1.get(sub_group, np.nan) for sub_group in sub_groups],
            group_names[1]: [dict_2.get(sub_group, np.nan) for sub_group in sub_groups],
        }

def add_bars(
    data_dict: dict,
    ax: Axes,
    x: np.ndarray,
    colors: list,
    show_rects: bool,
    width: float,
    gap: float
) -> None:
    multiplier = 0
    for attribute, measurement in data_dict.items():
        # 1. Computes the offset for bar placing on the x axis
        offset = (width + gap) * multiplier

        # 2. Computes the rects as fading gradients
        rects = ax.bar(x + offset, measurement, width, label=attribute, color="none")
        rects = convert_rect_to_grad(rects, ax, measurement, colors[multiplier])

        # 3. To show or not the measurement value at the top
        if show_rects:
            ax.bar_label(rects, padding=3, label_type="center")
        multiplier += 1

def get_y_axis(
    ax: Axes,
    ylabel: str,
    ylim: tuple | None,
    vertical_offset: float,
    data_dict: dict
) -> Axes:
    ax.set_ylabel(ylabel)
    if vertical_offset == 0 and ylim is not None:
        ax.set_ylim(ylim)
        ax.set_yticks([0,
            int(ylim[1])])
    else:
        max_value = max(np.nanmax(arr) for arr in data_dict.values())
        ymax = max_value + vertical_offset
        ax.set_ylim((0, int(ymax)))
        ax.set_yticks([0, int(ymax)])

    return ax
