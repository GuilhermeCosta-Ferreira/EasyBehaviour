# ================================================================
# 0. Section: IMPORTS
# ================================================================
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ...plots import two_group_bar_plot
from ..io import GroupScrap



# ================================================================
# 1. Section: Functions
# ================================================================
def multigroup_comparision(
    control_group: GroupScrap,
    study_group: GroupScrap
) -> tuple[Figure, Axes]:
    fig, ax = two_group_bar_plot(
        group_1_dict=control_group.mean_min_distance_per_tp,
        group_2_dict=study_group.mean_min_distance_per_tp,
        group_names=(control_group.name, study_group.name),
        ylabel="Minimum Distance (px)",
        title=f"Analysis over timepoins of Group {study_group.name} vs Control",
        fig_size=(8,8),
        show_rects=False
    )

    return fig, ax
