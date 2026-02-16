# ================================================================
# 0. Section: IMPORTS
# ================================================================
from pathlib import Path
from matplotlib import pyplot as plt

from pybehaviour.syllable_analysis import (
    get_syllable_density,
    get_pca,
    get_umap,
    plot_projection_2d,
    plot_projection_3d
)



# ================================================================
# 1. Section: INPUTS
# ================================================================
RESULTS_FOLDER: Path = Path("../data/syllables/results")
NR_OF_MODELS_TO_INSPECT: int = 3
FAVORITE_MODELS: list[str] =  [
    "full_both_71",
    "full_left_71",
    "71_results",
    "model_50_all",
    "2026_02_11-13_18_50",
    "2026_02_11-13_52_58",
    "2026_02_11-14_31_04",
]



# ================================================================
# 2. Section: MAIN
# ================================================================
if __name__ == '__main__':
    # 1. Get the models to inspect
    models = [p for p in RESULTS_FOLDER.iterdir() if p.is_dir()
        and p.stem in FAVORITE_MODELS[:NR_OF_MODELS_TO_INSPECT]]

    # 2. Generate PCA and UMAP 2D and 3D Projections per model
    for model in models:
        syllables = get_syllable_density(model)
        result = get_pca(syllables)
        plot_projection_2d(result, type="PCA")
        plot_projection_3d(result, type="PCA")

        result = get_umap(syllables, 4, 0.5)
        plot_projection_2d(result, type="UMAP")
        plot_projection_3d(result, type="UMAP")
    plt.show()
