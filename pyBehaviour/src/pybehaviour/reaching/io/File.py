# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pandas as pd

from pathlib import Path
from functools import cached_property

from .metadata import (
    get_file_metadata,
    MOUSE_PATTERN,
    DATE_PATTERN
)
from .distance import get_mindist



# ================================================================
# 1. Section: Functions
# ================================================================
class File:
    def __init__(self, path: Path, timepoint_dict: dict) -> None:
        self.path = path
        self.mouse = get_file_metadata(path, MOUSE_PATTERN)
        self.date = get_file_metadata(path, DATE_PATTERN)
        self.timepoint_dict = timepoint_dict


    @cached_property
    def _mindist_data(self):
        df = pd.read_csv(self.path, header=[1, 2], index_col=0)
        distance_data, _ = get_mindist(df)
        return distance_data

    @property
    def timepoint(self):
        translation = [k for k, dates in self.timepoint_dict.items() if self.date in dates]
        return str(translation[0]) if translation else ""

    @property
    def min_distance(self):
        return self._mindist_data[1]

    @property
    def min_distance_idx(self):
        return self._mindist_data[0]
