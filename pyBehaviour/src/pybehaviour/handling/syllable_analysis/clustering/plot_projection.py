# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

from matplotlib import pyplot as plt

from matplotlib.figure import Figure
from matplotlib.axes import Axes
from .ResultsProjection import ResultsProjection



# ================================================================
# 1. Section: 2D Plot
# ================================================================
def plot_projection_2d(
    results: ResultsProjection,
    type: str = "PCA",
    title: str = "Placeholder"
) -> tuple[Figure, Axes]:

    # 1. Extracts the timepoints
    timepoints = np.array([p.timepoint for p in results.meta])
    unique_tp = np.unique(timepoints)

    # 2. initialize the markers
    markers = ['s','^','D','v','P','X','*','<','>']
    colors = ["red", "green", "blue", "purple"]

    # 3. Loops over the possible timepoints
    fig, ax = plt.subplots()
    for i, tp in enumerate(unique_tp):
        # 4. Plots the individual projected data
        idx = (timepoints == tp)
        ax.scatter(results.data[idx, 0], results.data[idx, 1], zorder=0,
            color=colors[i], s=25, alpha=0.25, edgecolors='none')

        # 5. Plots the projected average of the grouped data (by tp)
        average_point = results.data[idx].mean(axis=0)
        ax.scatter(average_point[0], average_point[1],
            label=f"Average_{str(tp)}", s=50, alpha=1, edgecolors='none',
            color=colors[i], marker=markers[i % len(markers)], zorder=1)

    # 6. Set up the axis
    axis_label = "PC" if type.lower() == "pca" else "UMAP"
    ax.set_xlabel(f"{axis_label}1")
    ax.set_ylabel(f"{axis_label}2")

    # 7 Set up the title and labels
    ax.legend()
    ax.set_title(f"Model: {title}")

    # 8. Finishes the plot
    plt.tight_layout()
    plt.show(block=False)

    return fig, ax



# ================================================================
# 1. Section: 2D Plot
# ================================================================
def plot_projection_3d(
    results: ResultsProjection,
    type: str = "PCA",
    title: str = "Placeholder"
) -> tuple[Figure, Axes]:

    # 1. Extracts the timepoints
    timepoints = np.array([p.timepoint for p in results.meta])
    unique_tp = np.unique(timepoints)

    # 2. initialize the markers
    markers = ['s','^','D','v','P','X','*','<','>']
    colors = ["red", "green", "blue", "purple"]

    # 3. Loops over the possible timepoints
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    for i, tp in enumerate(unique_tp):
        # 4. Plots the individual projected data
        idx = (timepoints == tp)
        ax.scatter(results.data[idx, 0], results.data[idx, 1], results.data[idx, 2],
            zorder=0, color=colors[i], s=25, alpha=0.25, edgecolors='none')

        # 5. Plots the projected average of the grouped data (by tp)
        average_point = results.data[idx].mean(axis=0)
        ax.scatter(average_point[0], average_point[1], average_point[2],
            label=f"Average_{str(tp)}", s=50, alpha=1, edgecolors='none',
            color=colors[i], marker=markers[i % len(markers)], zorder=1)

    # 6. Set up the axis
    axis_label = "PC" if type.lower() == "pca" else "UMAP"
    ax.set_xlabel(f"{axis_label}1")
    ax.set_ylabel(f"{axis_label}2")
    ax.set_zlabel(f"{axis_label}3")

    # 7 Set up the title and labels
    ax.legend()
    ax.set_title(f"Model: {title}")

    # 8. Finishes the plot
    plt.tight_layout()
    plt.show(block=False)

    return fig, ax
