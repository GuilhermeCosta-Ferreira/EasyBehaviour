# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np
from matplotlib import pyplot as plt

from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.colors import to_rgba
from matplotlib.lines import Line2D

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
    multiplier = 0
    for attribute, measurement in data_dict.items():
        offset = (width + gap) * multiplier

        rects = ax.bar(x + offset, measurement, width, label=attribute, color="none")

        for rect, h in zip(rects, measurement):
                    if np.isnan(h) or h <= 0:
                        continue

                    add_vertical_gradient_to_bar(
                        ax=ax,
                        rect=rect,
                        color=colors[multiplier],
                        alpha_bottom=0.0,
                        alpha_top=1.0
                    )

        if show_rects:
            ax.bar_label(rects, padding=3, label_type="center")
        multiplier += 1

    # 6. Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(x + (width + gap)/2, sub_groups)
    ax.set_aspect("auto")
    ax.set_xlim(-width, len(sub_groups) - 1 + width * 2 + gap)
    ax.tick_params(axis='x', length=0)
    if show_legend:
        ax.legend(loc='upper right', ncols=1)
    ax.spines["bottom"].set_visible(False)

    if vertical_offset == 0 and ylim is not None:
        ax.set_ylim(ylim)
        ax.set_yticks([0, int(ylim[1])])
    else:
        max_value = max(np.nanmax(arr) for arr in data_dict.values())
        ymax = max_value + vertical_offset
        ax.set_ylim((0, int(ymax)))
        ax.set_yticks([0, int(ymax)])

    if vertical_offset == 0:
        ax.set_ylim(ylim)
    else:
        max_value = max(np.max(arr) for arr in data_dict.values())
        ax.set_ylim((0, max_value + vertical_offset))

    legend_handles = [
        Line2D([0], [0], marker='o', linestyle='None',
               markerfacecolor=colors[0], markeredgecolor=colors[0],
               markersize=14, label='Control'),

        Line2D([0], [0], marker='o', linestyle='None',
               markerfacecolor=colors[1], markeredgecolor=colors[1],
               markersize=14, label=group_names[1]),
    ]

    ax.legend(
        handles=legend_handles,
        loc='upper center',
        bbox_to_anchor=(0.5, -0.10),
        ncol=2,
        frameon=False,
        handlelength=0.8,
        handletextpad=0.5,
        columnspacing=1.5,
        fontsize=16
    )

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

def add_vertical_gradient_to_bar(
    ax: Axes,
    rect,
    color: str,
    alpha_bottom: float = 0.0,
    alpha_top: float = 1.0
) -> None:
    x = rect.get_x()
    y = rect.get_y()
    w = rect.get_width()
    h = rect.get_height()

    rgba = np.array(to_rgba(color))
    gradient = np.ones((256, 1, 4))
    gradient[..., :3] = rgba[:3]

    t = np.linspace(0, 1, 256).reshape(256, 1)
    gradient[..., 3] = alpha_bottom + (alpha_top - alpha_bottom) * (t ** 0.5)

    im = ax.imshow(
        gradient,
        extent=[x, x + w, y, y + h],
        origin="lower",
        aspect="auto",
        interpolation="bicubic",
        zorder=2
    )

    im.set_clip_path(rect)
