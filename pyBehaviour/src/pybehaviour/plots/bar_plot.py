# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np
from matplotlib import pyplot as plt

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ..logger import logger



# ================================================================
# 1. Section: Functions
# ================================================================
def two_group_bar_plot(
    group_1_dict: dict,
    group_2_dict: dict,
    group_names: list[str] | np.ndarray | tuple,
    ylabel: str = "Metric",
    title: str = "Title of the Plot",
    fig_size: tuple = (8,8),
    ylim: tuple | None = None,
    show_rects: bool = True,
    colors: list[str] = ["NR_GREY", "NR_RED"]
) -> tuple[Figure, Axes]:
    # 1. Make sure both groups have the same keys, if not just print a warning
    assert_same_keys(group_1_dict, group_2_dict)

    # 2. Builds a dict better suited for this
    sub_groups = sorted(group_1_dict.keys() | group_2_dict.keys())
    data_dict = build_data_dict(group_names, group_1_dict, group_2_dict, sub_groups)

    # 3. Define the group positioning
    x = np.arange(len(sub_groups))
    width = 0.25
    multiplier = 0

    # 4. Initialize and fill the plot
    fig, ax = plt.subplots(layout='constrained', figsize=fig_size)

    # 5. Get sub-group bar positions and parameters
    for attribute, measurement in data_dict.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute, color=colors[multiplier])
        if show_rects:
            ax.bar_label(rects, padding=3, label_type="center")
        multiplier += 1

    # 6. Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(x + width/2, sub_groups)
    ax.legend(loc='upper right', ncols=1)
    ax.set_ylim(ylim)

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
