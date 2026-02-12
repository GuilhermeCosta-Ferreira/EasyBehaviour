# ================================================================
# 0. Section: IMPORTS
# ================================================================
import umap

import numpy as np

from pathlib import Path
from typing_extensions import Any
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

from pybehaviour.syllable_analysis import get_syllable_density



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
def plot_cluster(folder: Path):
    syllables = get_syllable_density(folder)

    # Builds the data
    data = []
    meta = []
    for syl in syllables:
        data.append(syl.counts)
        meta.append(syl.metadata)

    data = np.array(data)
    data = data + 1e-8
    log_data = np.log(data)
    data = log_data - log_data.mean(axis=1, keepdims=True)

    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)

    #pca = PCA(n_components=2)   # or however many components you want
    pca = PCA(n_components=0.95)  # keep 95% variance
    data_pca = pca.fit_transform(data_scaled)

    timepoints = np.array([p.timepoint for p in meta])
    uniq = np.unique(timepoints)

    plot_2d(uniq, timepoints, data_pca, folder.stem, type="PCA")
    #plot_3d(uniq, timepoints, data_pca, folder.stem)

    reducer = umap.UMAP(
        n_components=2,
        n_neighbors=4,
        min_dist=0.1,
        metric="cosine"
    )

    embedding: Any = reducer.fit_transform(data)

    plot_2d(uniq, timepoints, embedding, folder.stem)
    #plot_3d(uniq, timepoints, embedding, folder.stem)




def plot_2d(uniq, timepoints, data_pca, model, type = None):
    plt.figure()
    for tp in uniq:
        idx = (timepoints == tp)
        plt.scatter(data_pca[idx, 0], data_pca[idx, 1], label=str(tp), s=25)

    if(type == "PCA"):
        plt.xlabel("PC1")
        plt.ylabel("PC2")
    else:
        plt.xlabel("UMAP1")
        plt.ylabel("UMAP2")

    plt.legend(title="Timepoint")
    plt.title(f"Model: {model}")
    plt.show(block=False)

def plot_3d(uniq, timepoints, data_pca, model):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    for tp in uniq:
        idx = (timepoints == tp)
        ax.scatter(
            data_pca[idx, 0], data_pca[idx, 1], data_pca[idx, 2],
            label=str(tp), s=25
        )

    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    ax.set_zlabel("PC3")
    ax.legend(title="Timepoint")
    ax.set_title(f"Model: {model}")
    plt.show(block=False)




# ================================================================
# 3. Section: MAIN
# ================================================================
if __name__ == '__main__':
    models = [p for p in RESULTS_FOLDER.iterdir() if p.is_dir() and p.stem in FAVORITE_MODELS]

    for model in models:
        plot_cluster(model)
    plt.show()
