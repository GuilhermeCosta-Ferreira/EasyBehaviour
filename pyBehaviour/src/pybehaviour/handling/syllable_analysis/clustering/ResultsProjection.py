# ================================================================
# 0. Section: IMPORTS
# ================================================================
import umap
import numpy as np

from dataclasses import dataclass
from sklearn.decomposition import PCA

from .Details import Details



# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class ResultsProjection:
    reducer: PCA | umap.UMAP
    data: np.ndarray
    meta: np.ndarray

    @property
    def details(self) -> Details | None:
        if(isinstance(self.reducer, PCA)):
            return Details.from_pca(self.reducer)
        else:
            return None



# ──────────────────────────────────────────────────────
# 1.1 Subsection: Helper Functions
# ──────────────────────────────────────────────────────
