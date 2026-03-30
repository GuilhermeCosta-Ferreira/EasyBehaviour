# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pandas as pd

from pathlib import Path

from .metadata import (
    get_file_metadata,
    MOUSE_PATTERN
)



# ================================================================
# 1. Section: Functions
# ================================================================
class File:
    def __init__(self, path: Path, timepoint_dict: dict) -> None:
        # 1. Metadata
        self.path = path
        self.mouse = get_file_metadata(path, MOUSE_PATTERN)
        if self.mouse is None:
            self.mouse = self.file_name.split("_")[0]
        self.timepoint_dict = timepoint_dict

        # 2. Data
        self.dataframe: pd.DataFrame = pd.read_csv(self.path, header=[1, 2], index_col=0)

        # 3. States
        self.ignore = False



    # ================================================================
    # 2. Section: Metadata Related Properties
    # ===============================================================
    @property
    def file_name(self) -> str:
        return self.path.stem.split("DLC")[0]
