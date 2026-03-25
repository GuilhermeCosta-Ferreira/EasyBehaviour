# ================================================================
# 0. Section: IMPORTS
# ================================================================
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ...plots import two_group_bar_plot
from ..io import GroupScrap



# ================================================================
# 1. Section: Plots for Paper
# ================================================================
def multigroup_comparision(
    control_group: GroupScrap,
    study_group: GroupScrap
) -> tuple[Figure, Axes]:
    fig, ax = two_group_bar_plot(
        group_1_dict=control_group.mean_min_distance_per_tp,
        group_2_dict=study_group.mean_min_distance_per_tp,
        group_names=(control_group.name, study_group.name),
        ylabel="Distance to pallet",
        title="",
        fig_size=(10,6),
        show_rects=False,
        vertical_offset=10,
        gap=0.05,
        show_legend=False,
    )

    return fig, ax

def multigroup_chronic_comparision(
    control_group: GroupScrap,
    study_group: GroupScrap
) -> tuple[Figure, Axes]:
    control_data = {
        "Chronic": control_group.mean_min_distance_per_tp["post_injury_week_8"]
    }

    study_data = {
        "Chronic": study_group.mean_min_distance_per_tp["post_injury_week_8"]
    }

    fig, ax = two_group_bar_plot(
        group_1_dict=control_data,
        group_2_dict=study_data,
        group_names=(control_group.name, study_group.name),
        ylabel="Distance to pallet",
        title="",
        fig_size=(5,7),
        show_rects=False,
        gap=0.05,
        vertical_offset=10,
        show_legend=False,
    )

    return fig, ax
