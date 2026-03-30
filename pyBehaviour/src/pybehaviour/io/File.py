# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pandas as pd

from pathlib import Path

from .metadata import (
    get_video_path,
    get_file_metadata,
    MOUSE_PATTERN
)
from .video import get_nr_fames



# ================================================================
# 1. Section: Functions
# ================================================================
class File:
    def __init__(self, path: Path) -> None:
        # 1. Metadata
        self.path = path
        self.mouse = get_file_metadata(path, MOUSE_PATTERN)
        if self.mouse is None:
            self.mouse = self.file_name.split("_")[0]

        # 2. Data
        self.dataframe: pd.DataFrame = pd.read_csv(self.path, header=[1, 2], index_col=0)



    # ================================================================
    # 2. Section: Video Related Properties
    # ================================================================
    @property
    def video_path(self) -> Path:
        return get_video_path(self.path.parent, self.file_name)

    @property
    def nr_frames(self) -> int:
        return get_nr_fames(self.video_path)



    # ================================================================
    # 2. Section: Metadata Related Properties
    # ===============================================================
    @property
    def file_name(self) -> str:
        return self.path.stem.split("DLC")[0]
