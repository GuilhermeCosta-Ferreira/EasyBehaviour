# ================================================================
# 0. Section: IMPORTS
# ================================================================
from pathlib import Path

from .GroupScrap import GroupScrap
from .io import (
    get_timepoint_dict,
    get_labels_path,
)
from .metadata import (
    get_unique_metadata,
    DATE_PATTERN,
    MOUSE_PATTERN
)
from .scrap_file import scrap_files



# ================================================================
# 1. Section: Functions
# ================================================================
def scrap_folder(folder_path: Path, group_name: str) -> GroupScrap:
    # 1. Get all the usefull file data from the group folder
    timepoint_dict = get_timepoint_dict(folder_path)

    # 2. Get all the individual file data
    csv_files = get_labels_path(folder_path / "raw_csv")
    files = scrap_files(csv_files, timepoint_dict)

    # 3. Get content info
    dates_present = get_unique_metadata(csv_files, DATE_PATTERN)
    mice_present = get_unique_metadata(csv_files, MOUSE_PATTERN)

    # 4. Saves it in a dataclass
    data = GroupScrap(
        name=group_name,
        timepoint_dict=timepoint_dict,
        files=files,
        dates=dates_present,
        mice=mice_present
    )
    return data
