# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

from matplotlib.figure import Figure
from matplotlib.axes import Axes

from ...plots import plot_imshow_with_labels
from ..io import File



# ================================================================
# 1. Section: Functions
# ================================================================
def plot_best_frame(data_file: File, title: str = "Best Frame") -> tuple[Figure, Axes] | None:
    if data_file.best_frame is not None:
        frame = data_file.best_frame
    else:
        raise FileNotFoundError(f"No frame found from the file {data_file.path}")

    return plot_imshow_with_labels(
        img = frame,
        points = [data_file.best_label],
        point_labels = ["Wrist"],
        title = title
    )
