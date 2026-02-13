# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

from matplotlib import pyplot as plt

from sklearn.decomposition import PCA

from .preprocessing import (
    get_data_ready,
    numerical_stabilization,
)
from .ResultsProjection import ResultsProjection



# ================================================================
# 1. Section: Functions
# ================================================================
def get_pca(syllables: np.ndarray, show_details: bool = False) -> ResultsProjection:
    # 1. Extract the data
    data, meta = get_data_ready(syllables)

    # 2. Processes the data
    data = numerical_stabilization(data)

    # 3. Extract the PCA
    pca = PCA(n_components=3)
    data_pca = pca.fit_transform(data)
    result = ResultsProjection(pca, data_pca, meta)

    # 4. Show details if needed
    if(show_details):
        pca_details = result.details
        print(pca_details)

    return result
