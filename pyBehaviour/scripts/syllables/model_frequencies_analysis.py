# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

from matplotlib import pyplot as plt
from pathlib import Path
from pybehaviour.syllable_analysis import (
    get_syllable_density
)



# ================================================================
# 1. Section: INPUTS
# ================================================================
RESULTS_FOLDER: Path = Path("../data/syllables/results")
FAVORITE_MODELS: list[str] =  [
    "2026_02_11-13_18_50",
    "2026_02_11-13_52_58",
    "2026_02_11-14_31_04"
]



# ================================================================
# 2. Section: FUNCTIONS
# ================================================================
def inspect(folder: Path, limit: tuple):
    syllable_store = get_syllable_density(folder)


    average_bl_counts = np.mean(
        a=np.vstack([dp.counts for dp in syllable_store if dp.timepoint == "BL"]),
        axis=0
    )
    average_w1_counts = np.mean(
        a=np.vstack([dp.counts for dp in syllable_store if dp.timepoint == "Post_W1"]),
        axis=0
    )
    average_w4_counts = np.mean(
        a=np.vstack([dp.counts for dp in syllable_store if dp.timepoint == "Post_W4"]),
        axis=0
    )
    average_w8_counts = np.mean(
        a=np.vstack([dp.counts for dp in syllable_store if dp.timepoint == "Post_W8"]),
        axis=0
    )
    centers = np.arange(0, 100 + 1)  # integer centers

    plt.figure()
    plt.plot(centers, average_bl_counts, marker="o", label="BL")
    plt.plot(centers, average_w1_counts, marker="o", label="W1")
    plt.plot(centers, average_w4_counts, marker="o", label="W4")
    plt.plot(centers, average_w8_counts, marker="o", label="W8")
    plt.xlim((limit[0] - 0.5, limit[1] - 0.5))
    plt.xticks(np.arange(limit[0], limit[1]))
    plt.legend()
    plt.title(f"Model: {folder.stem}")
    plt.show(block=False)



# ================================================================
# 3. Section: MAIN
# ================================================================
if __name__ == '__main__':
    # models = [p for p in RESULTS_FOLDER.iterdir() if p.is_dir()] # all models
    models = [p for p in RESULTS_FOLDER.iterdir() if p.is_dir() and p.stem in FAVORITE_MODELS]


    for model in models:
        inspect(
            folder = model,
            limit = (0, 21))
    plt.show()
