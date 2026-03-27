# ================================================================
# 0. Section: IMPORTS
# ================================================================
import os

from pathlib import Path
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ...plots import two_group_stat_bar_plot, PlotSettings
from ...save import save_plot, SaveSettings
from ..io import GroupScrap



# ================================================================
# 1. Section: Plots for Paper
# ================================================================
def multigroup_comparision(
    control_group: GroupScrap,
    study_group: GroupScrap,
    output_folder: Path,
    is_save: bool = False,
    plt_settings: PlotSettings | None = None,
    save_settings: SaveSettings | None = None,
) -> tuple[Figure, Axes]:

    # 1. Get the settings
    if plt_settings is None:
        plt_settings = PlotSettings(
            ylabel="Distance to pallet",
            title="",
            fig_size=(10,6),
            show_rects=False,
            vertical_offset=25,
            gap=0.05,
            show_legend=True,
            lightness_factor=0.11,
            show_points=True,
            show_errorbar=False,
            show_pvalue=True,
        )

    # 2. Generate the plots
    fig, ax = two_group_stat_bar_plot(
        group_1_dict=control_group.mean_min_distance_per_mouse_per_tp,
        group_2_dict=study_group.mean_min_distance_per_mouse_per_tp,
        group_names=[control_group.name, study_group.name],
        plt_settings=plt_settings
    )

    # 3. Get the save settings
    if save_settings is None:
        save_settings = SaveSettings(name="across_tp_analysis")

    # 4. Save if needed
    if is_save:
        output_folder = output_folder / f"{control_group.group_num}_{study_group.group_num}"
        os.makedirs(output_folder, exist_ok=True)
        save_plot(fig, output_folder, save_settings)

    return fig, ax

def multigroup_chronic_comparision(
    control_group: GroupScrap,
    study_group: GroupScrap,
    output_folder: Path,
    is_save: bool = False,
    plt_settings: PlotSettings | None = None,
    save_settings: SaveSettings | None = None,
) -> tuple[Figure, Axes]:
    # 1. Get the chronic data
    control_data = {
        "Chronic": control_group.mean_min_distance_per_mouse_per_tp["post_injury_week_8"]
    }

    study_data = {
        "Chronic": study_group.mean_min_distance_per_mouse_per_tp["post_injury_week_8"]
    }

    # 2. Plot settings
    if plt_settings is None:
        plt_settings = PlotSettings(
            ylabel="Distance to pallet",
            title="",
            fig_size=(4,7),
            show_rects=False,
            gap=0.05,
            vertical_offset=20,
            show_legend=False,
            lightness_factor=0.11,
            show_points=True,
            show_errorbar=False,
            show_pvalue=True,
        )

    # 3. Generate the plot
    fig, ax = two_group_stat_bar_plot(
        group_1_dict=control_data,
        group_2_dict=study_data,
        group_names=[control_group.name, study_group.name],
        plt_settings=plt_settings
    )

     # 3. Get the save settings
    if save_settings is None:
        save_settings = SaveSettings(name="chronic_analysis")

     # 4. Save if needed
    if is_save:
        output_folder = output_folder / f"{control_group.group_num}_{study_group.group_num}"
        os.makedirs(output_folder, exist_ok=True)
        save_plot(fig, output_folder, save_settings)

    return fig, ax
