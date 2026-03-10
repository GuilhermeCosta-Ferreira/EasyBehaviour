# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

from dataclasses import dataclass



# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class GroupScrap:
    timepoint_dict: dict
    files: np.ndarray
    dates: np.ndarray
    mice: np.ndarray

    @property
    def timepoints(self):
        # 1. We leverage list property called intersection
        present_dates = set(self.dates.tolist())  # or set(self.dates)

        # 2. All timepoints (not dates) present in the folder
        return [
                tp
                for tp, accepted_dates in self.timepoint_dict.items()
                if present_dates.intersection(accepted_dates)
            ]

    @property
    def min_distances(self) -> np.ndarray:
        min_distances = []
        for file in self.files:
            min_distances.append(file.min_distance)

        return np.array(min_distances)

    @property
    def mean_minimal_distance(self):
        return np.mean(self.min_distances)



    def __len__(self):
        return len(self.files)
