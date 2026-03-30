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
    name: str
    timepoint_dict: dict
    files: np.ndarray
    dates: np.ndarray
    mice: np.ndarray
    group_num: int

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
    def mean_min_distance(self):
        return np.mean(self.min_distances)

    @property
    def min_distances_per_tp(self) -> dict:
        storage = {}
        for file in self.files:
            file_tp = file.timepoint
            if file_tp not in storage:
                storage[file_tp] = []
            storage[file_tp].append(float(file.min_distance))

        return storage

    @property
    def mean_min_distance_per_tp(self) -> dict:
        return {tp: sum(values) / len(values) for tp, values in self.min_distances_per_tp.items()}

    @property
    def min_distance_per_mouse_per_tp(self) -> dict:
        storage = {}
        for file in self.files:
            file_tp = file.timepoint
            file_mouse = file.mouse

            if file_tp not in storage:
                storage[file_tp] = {}
            if file_mouse not in storage[file_tp]:
                storage[file_tp][file_mouse] = []
            storage[file_tp][file_mouse].append(float(file.min_distance))

        return storage

    @property
    def mean_min_distance_per_mouse_per_tp(self) -> dict:
        return {
            tp: {
                mouse: sum(values) / len(values)
                for mouse, values in mouse_dict.items()
            }
            for tp, mouse_dict in self.min_distance_per_mouse_per_tp.items()
        }

    def __len__(self):
        return len(self.files)
