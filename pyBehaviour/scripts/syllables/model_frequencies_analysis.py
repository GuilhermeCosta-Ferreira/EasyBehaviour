# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

from matplotlib import pyplot as plt
from pathlib import Path
from pybehaviour.syllable_analysis import (
    get_syllable_density,
    get_average_syllables
)



# ================================================================
# 1. Section: INPUTS
# ================================================================
RESULTS_FOLDER: Path = Path("../data/syllables/results")
"""
FAVORITE_MODELS: list[str] =  [
    "2026_02_11-13_18_50",
    "2026_02_11-13_52_58",
    "2026_02_11-14_31_04"
]
"""
FAVORITE_MODELS: list[str] =  [
    "model_50_all"
]



# ================================================================
# 2. Section: FUNCTIONS
# ================================================================
def inspect_model_denisty_distribution(folder: Path, limit: tuple):
    syllables = get_syllable_density(folder)
    average_syllables = get_average_syllables(syllables)

    centers = np.arange(0, 100 + 1)  # integer centers

    plt.figure()
    for syl in average_syllables:
        plt.plot(
            centers,
            syl.counts,
            marker="o",
            label=f"#{syl.group}_{syl.timepoint}"
        )

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
        inspect_model_denisty_distribution(
            folder = model,
            limit = (0, 21))
    plt.show()
