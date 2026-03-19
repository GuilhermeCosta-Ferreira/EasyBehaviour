# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pandas as pd

from typing import cast
from pathlib import Path
from functools import cached_property

from .metadata import (
    get_video_path,
    get_file_metadata,
    MOUSE_PATTERN,
    DATE_PATTERN
)
from .distance import get_mindist
from .video import get_nr_fames, get_best_frame
from .tracking import get_best_label



# ================================================================
# 1. Section: Functions
# ================================================================
class File:
    def __init__(self, path: Path, timepoint_dict: dict) -> None:
        # 1. Metadata
        self.path = path
        self.mouse = get_file_metadata(path, MOUSE_PATTERN)
        self.date = get_file_metadata(path, DATE_PATTERN)
        self.timepoint_dict = timepoint_dict

        # 2. Data
        self.dataframe: pd.DataFrame = pd.read_csv(self.path, header=[1, 2], index_col=0)

        # 3. States
        self.ignore = False

    # ================================================================
    # 2. Section: Video Related Properties
    # ================================================================
    @property
    def video_path(self) -> Path:
        return get_video_path(self.path.parent, self.file_name)

    @property
    def nr_frames(self) -> int:
        return get_nr_fames(self.video_path)

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

    @property
    def file_name(self) -> str:
        return self.path.stem.split("DLC")[0]



    # ================================================================
    # 4. Section: Tracking Related Properties
    # ================================================================
    @cached_property
    def _mindist_data(self) -> tuple:
        df = self.dataframe
        distance_data, _ = get_mindist(df)
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
