# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np
from pathlib import Path

from .metadata import (
    get_mice_to_remove,
    get_labels_path,
    get_unique_metadata,
    MOUSE_PATTERN
)
from .scrap import scrap_files



# ================================================================
# 1. Section: Functions
# ================================================================
class Group:
    def __init__(
        self,
        folder_path: Path,
        group_name: str,
        group_number: int,
        mice_to_keep: Path,
        csv_folder_name: str = "raw"
    ) -> None:
        # 1. Metadata
        self.folder_path = folder_path
        self.name = group_name
        self.number = group_number
        self.mice_to_remove = get_mice_to_remove(mice_to_keep, group_number)

        # 2. Data
        csv_files = get_labels_path(folder_path / csv_folder_name)
        self.files = scrap_files(csv_files, self.mice_to_remove)
        mice_present = get_unique_metadata(csv_files, MOUSE_PATTERN)
        self.mice = np.array([mouse for mouse in mice_present if mouse not in self.mice_to_remove])
