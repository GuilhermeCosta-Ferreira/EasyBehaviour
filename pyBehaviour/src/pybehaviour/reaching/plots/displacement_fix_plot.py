# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pandas as pd
from matplotlib import pyplot as plt

from copy import deepcopy
from matplotlib.figure import Figure
from matplotlib.axes import Axes

from ...plots import plot_lines
from ..io import ReachingFile



# ================================================================
# 1. Section: Functions
# ================================================================
def plot_filter_displacement(
    file_data: ReachingFile,
    proc_file: ReachingFile,
    derivate: bool = False
) -> tuple[Figure, Axes]:
    # 1. Import the clear data
    wrist_df = deepcopy(file_data.wrist_df)
    x_raw, y_raw = get_xy_signal(wrist_df, derivate)

    # 2. Build the processed signal
    proc_wrist_df = deepcopy(proc_file.wrist_df)
    x_proc, y_proc = get_xy_signal(proc_wrist_df, derivate)

    # 3. Initializes the plot
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), layout='constrained')
    title_spec = "" if not derivate else " diff"

    # 4. Fills both subplots with line plots
    fig, axes[0] = plot_lines(
        [x_raw, x_proc],
        ["Original", "Processed"],
        title=f"X position{title_spec} over time",
        ax=axes[0]
    )
    fig, axes[1] = plot_lines(
        [y_raw, y_proc],
        ["Original", "Processed"],
        title=f"Y position{title_spec} over time",
        ax=axes[1]
    )

    return fig, axes


# ──────────────────────────────────────────────────────
# 1.1 Subsection: Helper Functions
# ──────────────────────────────────────────────────────
def get_xy_signal(df: pd.DataFrame, derivate: bool) -> tuple:
    if derivate:
        x = df["x"].diff().to_numpy()
        y = df["y"].diff().to_numpy()
    else:
        x = df["x"].to_numpy()
        y = df["y"].to_numpy()

    return (x, y)
