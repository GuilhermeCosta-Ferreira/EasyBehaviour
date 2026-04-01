# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pandas as pd
import numpy as np

from typing import cast
from pathlib import Path
from functools import cached_property

from ...io import (
    DATE_PATTERN,
    File,
    get_file_metadata,
)

from .distance import get_mindist
from .video import get_best_frame
from .tracking import get_best_label



# ================================================================
# 1. Section: Functions
# ================================================================
class ReachingFile(File):
    def __init__(self, path: Path, timepoint_dict: dict) -> None:
        super().__init__(path)

        # 1. Metadata
        self.date = get_file_metadata(path, DATE_PATTERN)
        self.timepoint_dict = timepoint_dict

    # ================================================================
    # 2. Section: Video Related Properties
    # ================================================================
    @property
    def best_frame(self):
        return get_best_frame(self.video_path, self.min_distance_idx)



    # ================================================================
    # 3. Section: Metadata Related Properties
    # ================================================================
    @property
    def timepoint(self) -> str:
        translation = [k for k, dates in self.timepoint_dict.items() if self.date in dates]
        return str(translation[0]) if translation else ""



    # ================================================================
    # 4. Section: Tracking Related Properties
    # ================================================================
    @cached_property
    def _mindist_data(self) -> tuple:
        df = self.dataframe
        try:
            distance_data, _ = get_mindist(df)
        except:
            print(f"Only Nans present at {self.path}")
            distance_data = (np.nan, np.nan)
        return distance_data

    @property
    def min_distance(self) -> float:
        return self._mindist_data[1]

    @property
    def min_distance_idx(self) -> int:
        return self._mindist_data[0]

    @property
    def best_label(self) -> tuple:
        return get_best_label(self.wrist_df, self.min_distance_idx)

    @property
    def wrist_df(self) -> pd.DataFrame:
        return cast(pd.DataFrame, self.dataframe["wrist"].copy())

    @wrist_df.setter
    def wrist_df(self, new_wrist_df: pd.DataFrame) -> None:
        expected_cols = ["x", "y", "likelihood"]
        if list(new_wrist_df.columns) != expected_cols:
            raise ValueError(f"wrist_df must have columns {expected_cols}")

        self.dataframe.loc[:, ("wrist", "x")] = new_wrist_df["x"].to_numpy()
        self.dataframe.loc[:, ("wrist", "y")] = new_wrist_df["y"].to_numpy()
        self.dataframe.loc[:, ("wrist", "likelihood")] = new_wrist_df["likelihood"].to_numpy()

        self._invalidate_cached_properties()

    def _invalidate_cached_properties(self) -> None:
        self.__dict__.pop("_mindist_data", None)
