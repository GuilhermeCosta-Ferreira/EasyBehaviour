# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

from dataclasses import dataclass
from sklearn.decomposition import PCA



# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class Details:
    kept_components: int
    explained_variance: np.ndarray

    @classmethod
    def from_pca(cls, pca: PCA) -> 'Details':
        detail = Details(
            kept_components=pca.n_components_,
            explained_variance=pca.explained_variance_ratio_
        )

        return detail

    @property
    def cumulative_explained_variance(self):
        return np.cumsum(self.explained_variance)

    @property
    def total_explained_variance(self):
        return self.cumulative_explained_variance[-1]

    def __str__(self) -> str:
        answer: str = "|---------------------------------------------|\n"

        answer += f"Nr of components kept: {self.kept_components}\n"
        answer += f"Explained variance /component: {np.round(self.explained_variance,2)}\n"
        answer += f"Cumulative explained variance: {np.round(self.cumulative_explained_variance,2)}\n"
        answer += f"Total explained variance: {np.round(self.total_explained_variance,2)}\n"

        answer += "|---------------------------------------------|"

        return answer
