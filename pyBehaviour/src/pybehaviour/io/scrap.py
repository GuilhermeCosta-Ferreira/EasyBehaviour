# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

from typing import TypeVar

from .File import File

T = TypeVar("T", bound=File)



# ================================================================
# 1. Section: Functions
# ================================================================
def scrap_files(files: np.ndarray, mice_to_remove: list, file_class: type[T]) -> np.ndarray:
    list_of_files = []

    # 1. Loop over all files
    for file in files:
        # 1.1 Stores it in a list
        file = file_class(file)

        # 1.2 Removes any mice marked to be removed
        if file.mouse in mice_to_remove:
            continue

        list_of_files.append(file)

    return np.array(list_of_files)
