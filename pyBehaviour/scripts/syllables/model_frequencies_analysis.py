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
NR_OF_MODELS_TO_INSPECT: int = 3
FAVORITE_MODELS: list[str] = [
    "full_both_71",
    "full_left_71",
    "71_results",
    "model_50_all",
    "v1_2026_02_09-14_30_17",
    "2026_02_11-13_18_50",
    "2026_02_11-13_52_58",
    "2026_02_11-14_31_04"
]
LIMIT: tuple = (0, 31)



# ================================================================
# 2. Section: FUNCTIONS
# ================================================================
def inspect_model_denisty_distribution(folder: Path, limit: tuple):
    syllables = get_syllable_density(folder)
    average_syllables = get_average_syllables(syllables)

    centers = np.arange(0, 100 + 1)
    tp_cmap, group_to_pos = _generate_cmaps(average_syllables)

    plt.figure()
    for syl in average_syllables:
        cmap = tp_cmap[syl.timepoint]
        color = cmap(group_to_pos[syl.group])   # shade depends on timepoint, within group's palette

        plt.plot(
            centers,
            syl.counts,
            marker="o",
            color=color,
            label=f"{syl.group}_{syl.timepoint}"
        )

    plt.xlim((limit[0] - 0.5, limit[1] - 0.5))
    plt.xticks(np.arange(limit[0], limit[1]))
    plt.legend()
    plt.title(f"Model: {folder.stem}")
    plt.show(block=False)

def _generate_cmaps(average_syllables: np.ndarray) -> tuple[dict, dict]:
    # 1. get unique groups/timepoints from your averaged objects
    groups = np.unique([s.group for s in average_syllables])
    timepoints = np.unique([s.timepoint for s in average_syllables])

    # 2. Choose a colormap per timepoint
    palette_cycle = ["Reds", "Blues", "Greens", "Purples", "Oranges", "Greys"]
    timepoint_cmap = {g: plt.get_cmap(palette_cycle[i % len(palette_cycle)])
                  for i, g in enumerate(timepoints)}

    # 3. Map each group to a position in [0.35,0.9] to pick shades and avoid super light
    group_positions = np.linspace(0.35, 0.9, len(groups))
    group_to_pos = {g: group_positions[i] for i, g in enumerate(groups)}

    return (timepoint_cmap, group_to_pos)



# ================================================================
# 3. Section: MAIN
# ================================================================
if __name__ == '__main__':
    # 1. Get the models to inspect
    models = [p for p in RESULTS_FOLDER.iterdir() if p.is_dir()
        and p.stem in FAVORITE_MODELS[:NR_OF_MODELS_TO_INSPECT]]

    # 2. Inspect the models
    for model in models:
        inspect_model_denisty_distribution(
            folder = model,
            limit = LIMIT)
    plt.show()
