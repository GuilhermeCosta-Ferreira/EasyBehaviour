# ================================================================
# 0. Section: IMPORTS
# ================================================================
import json

import numpy as np

from pathlib import Path

from .GroupScrap import GroupScrap
from .io import (
    get_timepoint_dict,
    get_labels_path,
)
from ...io import (
    get_unique_metadata,
    DATE_PATTERN,
    MOUSE_PATTERN
)
from .scrap_file import scrap_files



# ================================================================
# 1. Section: Functions
# ================================================================
def scrap_folder(
    folder_path: Path,
    group_name: str,
    group_number: int,
    mice_to_keep: Path,
    csv_folder_name: str = "raw"
) -> GroupScrap:
    # 1. Get all the usefull file data from the group folder
    timepoint_dict = get_timepoint_dict(folder_path)

    # 2. Remove mice that are not to be included
    with open(mice_to_keep, "r") as f:
        mice_to_keep_all = json.load(f)
    group_keep_info = next(item for item in mice_to_keep_all["to_keep"] if item["group_id"] == group_number)
    mice_to_remove = group_keep_info["remove"]

    # 3. Get all the individual file data
    csv_files = get_labels_path(folder_path / csv_folder_name)
    files = scrap_files(csv_files, timepoint_dict, mice_to_remove)

    # 4. Get content info
    dates_present = get_unique_metadata(csv_files, DATE_PATTERN)
    mice_present = get_unique_metadata(csv_files, MOUSE_PATTERN)
    mice_filtered = np.array([mouse for mouse in mice_present if mouse not in mice_to_remove])

    # 5. Saves it in a dataclass
    data = GroupScrap(
        name=group_name,
        timepoint_dict=timepoint_dict,
        files=files,
        dates=dates_present,
        mice=mice_filtered,
        group_num=group_number
    )
    return data
