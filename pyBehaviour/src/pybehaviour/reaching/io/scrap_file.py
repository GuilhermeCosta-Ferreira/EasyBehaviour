# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

from .ReachingFile import ReachingFile



# ================================================================
# 1. Section: Functions
# ================================================================
def scrap_files(files: np.ndarray, timepoint_dict: dict, mice_to_remove: list) -> np.ndarray:
    list_of_files = []

    # 1. Loop over all files
    for file in files:
        # 1.1 Stores it in a list
        file = ReachingFile(
            path=file,
            timepoint_dict=timepoint_dict
        )

        # 1.2 Removes any mice marked to be removed
        if file.mouse in mice_to_remove:
            continue

        list_of_files.append(file)

    return np.array(list_of_files)
