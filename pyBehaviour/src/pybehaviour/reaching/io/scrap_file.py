# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

from .File import File



# ================================================================
# 1. Section: Functions
# ================================================================
def scrap_files(files: np.ndarray, timepoint_dict: dict) -> np.ndarray:
    list_of_files = []

    # 1. Loop over all files
    for file in files:
        # 1.1 Stores it in a list
        list_of_files.append(
            File(
                path=file,
                timepoint_dict=timepoint_dict
            )
        )

    return np.array(list_of_files)
