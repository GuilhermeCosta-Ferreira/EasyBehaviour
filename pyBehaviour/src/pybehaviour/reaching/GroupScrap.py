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
