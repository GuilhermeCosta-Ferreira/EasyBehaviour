# ================================================================
# 0. Section: IMPORTS
# ================================================================
import umap

import numpy as np

from typing_extensions import Any
from .preprocessing import(
    get_data_ready,
    numerical_stabilization
)
from .ResultsProjection import ResultsProjection



# ================================================================
# 1. Section: Functions
# ================================================================
def get_umap(
    syllables: np.ndarray,
    nr_neighbours: int,
    min_distance: float
) -> ResultsProjection:
    # 1. Extract the data
    data, meta = get_data_ready(syllables)

    # 2. Processes the data
    data = numerical_stabilization(data)

    # 3. Applies UMAP
    reducer = umap.UMAP(
        n_components=3,
        n_neighbors=nr_neighbours,
        min_dist=min_distance,
        metric="cosine"
    )
    embedding: Any = reducer.fit_transform(data)

    # 4. Stores as Results
    results = ResultsProjection(
        reducer=reducer,
        data=embedding,
        meta=meta
    )

    return results
