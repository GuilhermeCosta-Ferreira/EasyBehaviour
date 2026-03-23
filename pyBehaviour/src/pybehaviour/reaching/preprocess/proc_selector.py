# ================================================================
# 0. Section: IMPORTS
# ================================================================
from matplotlib import pyplot as plt

from matplotlib.figure import Figure
from matplotlib.axes import Axes
from pathlib import Path
from typing import cast

from ..plots import plot_best_frame
from ..io import File



# ================================================================
# 1. Section: Functions
# ================================================================
def review_preprocess(files: list[File], output_path: Path):
    accepted_file = None

    for file in files:
        min_dist = file.min_distance
        name = file.file_name
        title = f"{name} with MinDistance: {min_dist:.2f}"
        fig, ax = cast(tuple[Figure, Axes], plot_best_frame(file, title))

        decision = {"accepted": False}

        def on_key(event):
            if event.key == "y":
                decision["accepted"] = True
                plt.close(fig)
            elif event.key == "n":
                plt.close(fig)
        fig.canvas.mpl_connect("key_press_event", on_key)

        plt.show()

        if decision["accepted"]:
            accepted_file = file
            break

    if accepted_file is not None:
        output_file = output_path / accepted_file.path.name
        accepted_file.dataframe.to_csv(output_file)
        print(f"Accepted plot index saved: {output_file}")
    else:
        print(f"No plot was accepted. this means {files[0].file_name} will get ignored")
