# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np
from matplotlib import pyplot as plt

from matplotlib.axes import Axes
from matplotlib.figure import Figure
from scipy.stats import ttest_ind

from ..features import nice_legend
from ..PlotSettings import PlotSettings
from .bar_helpers import add_bars, add_points, add_errorbar, get_y_axis, assert_same_keys
from ...stats import p_to_stars



# ================================================================
# 1. Section: Functions
# ================================================================
def two_group_stat_bar_plot(
    group_1_dict: dict[str, dict[str, list[float]]],
    group_2_dict: dict[str, dict[str, list[float]]],
    group_names: list[str] | np.ndarray,
    plt_settings: PlotSettings = PlotSettings(),
) -> tuple[Figure, Axes]:
    # 1. Make sure both groups have the same keys, if not just print a warning
    assert_same_keys(group_1_dict, group_2_dict)

    # 2. Builds a dict better suited for this
    sub_groups = sorted(group_1_dict.keys() | group_2_dict.keys())
    data_dict = build_data_dict(group_names, group_1_dict, group_2_dict, sub_groups)
    mean_dict = build_mean_data_dict(data_dict)
    std_dict = build_std_data_dict(data_dict)

    # 3. Define the group positioning
    x = np.arange(len(sub_groups))

    # 4. Initialize and fill the plot
    fig, ax = plt.subplots(layout='constrained', figsize=plt_settings.fig_size)

    # 5. Get sub-group bar positions and parameters
    ax = add_bars(mean_dict, ax, x, plt_settings)
    if plt_settings.show_points:
        ax = add_points(data_dict, ax, x, plt_settings)
    if plt_settings.show_errorbar:
        ax = add_errorbar(mean_dict, std_dict, ax, x, plt_settings)

    # 6. Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_title(plt_settings.title)
    ax.set_aspect("auto")

    # 7. Define the Y lim and its ticks
    ax = get_y_axis(ax, mean_dict, plt_settings)

    # 8. Define the X lim and its ticks
    ax.set_xticks(x + (plt_settings.width + plt_settings.gap)/2, sub_groups)
    ax.set_xlim(-plt_settings.width, len(sub_groups) - 1 + plt_settings.width * 2 + plt_settings.gap)
    ax.tick_params(axis='x', length=0)
    ax.spines["bottom"].set_visible(False)

    # 9. Builds the legend for better visualization
    if plt_settings.show_legend:
        ax = nice_legend(ax, plt_settings.colors, group_names)

    return fig, ax


# ──────────────────────────────────────────────────────
# 1.1 Subsection: Helper Functions
# ──────────────────────────────────────────────────────
def build_data_dict(
    group_names: list[str] | np.ndarray | tuple,
    dict_1: dict,
    dict_2: dict,
    sub_groups: list[str]
) -> dict:
    return {
            group_names[0]: [list(dict_1.get(sub_group, {}).values()) for sub_group in sub_groups],
            group_names[1]: [list(dict_2.get(sub_group, {}).values()) for sub_group in sub_groups],
        }

def build_mean_data_dict(data_dict: dict) -> dict:
    return {
        group_name: [float(np.mean(values)) for values in sub_dict]
        for group_name, sub_dict in data_dict.items()
    }

def build_std_data_dict(data_dict: dict) -> dict:
    return {
        group_name: [float(np.std(values)) for values in sub_dict]
        for group_name, sub_dict in data_dict.items()
    }



def add_significance_lines(
    ax: Axes,
    x: np.ndarray,
    group_1_dict: dict[str, np.ndarray],
    group_2_dict: dict[str, np.ndarray],
    width: float,
    gap: float,
    alpha: float = 0.05,
) -> None:
    sub_groups = sorted(group_1_dict.keys() | group_2_dict.keys())
    y_min, y_max = ax.get_ylim()
    y_range = y_max - y_min

    line_height = 0.03 * y_range
    text_offset = 0.01 * y_range

    for i, sub_group in enumerate(sub_groups):
        data1 = np.asarray(group_1_dict.get(sub_group, []), dtype=float)
        data2 = np.asarray(group_2_dict.get(sub_group, []), dtype=float)

        data1 = data1[~np.isnan(data1)]
        data2 = data2[~np.isnan(data2)]

        #_, p = ttest_ind(data1, data2, equal_var=False)
        p=0.00001

        if p >= alpha:
            continue

        bar1_x = x[i]
        bar2_x = x[i] + width + gap

        top = max(data1, data2)
        print(top)
        y = top + 0.06 * y_range

        ax.plot(
            [bar1_x, bar1_x, bar2_x, bar2_x],
            [y, y + line_height, y + line_height, y],
            color="black",
            linewidth=1.2,
        )
        ax.text(
            (bar1_x + bar2_x) / 2,
            float(y + line_height + text_offset),
            p_to_stars(p),
            ha="center",
            va="bottom",
        )
