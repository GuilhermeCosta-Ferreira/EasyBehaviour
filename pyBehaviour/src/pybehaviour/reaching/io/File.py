# ================================================================
# 0. Section: IMPORTS
# ================================================================
import cv2

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
    def _mindist_data(self) -> tuple:
        df = pd.read_csv(self.path, header=[1, 2], index_col=0)
        distance_data, _ = get_mindist(df)
        return distance_data

    @property
    def timepoint(self) -> str:
        translation = [k for k, dates in self.timepoint_dict.items() if self.date in dates]
        return str(translation[0]) if translation else ""

    @property
    def min_distance(self) -> float:
        return self._mindist_data[1]

    @property
    def min_distance_idx(self) -> int:
        return self._mindist_data[0]

    @property
    def nr_frames(self) -> int:
        # 1. Open video file
        video_data = cv2.VideoCapture(self.path)

        nr_frames = int(video_data.get(cv2.CAP_PROP_FRAME_COUNT))
        return nr_frames

    @property
    def best_frame(self):
        # 1. Open video file
        video_data = cv2.VideoCapture(self.path)

        # 2. Set position to frameidx (index starts at 0)
        video_data.set(cv2.CAP_PROP_POS_FRAMES, self.min_distance_idx)

        # 3. Extract the frame and convert to RGB
        ret, frame = video_data.read()
        if ret:
            return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        else:
            return None
