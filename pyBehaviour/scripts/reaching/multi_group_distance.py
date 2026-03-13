# ================================================================
# 0. Section: IMPORTS
# ================================================================
import os

import numpy as np

from pathlib import Path

from pybehaviour.reaching import scrap_folder


# ================================================================
# 1. Section: INPUTS
# ================================================================
DLC_FOLDER: Path = Path("../data/dlc")
COMPARING_GROUP_FOLDER: Path = DLC_FOLDER / "71_reaching"
#CONTROL_GROUP_FOLDER: Path = DLC_FOLDER / "46_reaching"
CONTROL_GROUP_FOLDER: Path = DLC_FOLDER / "71_reaching"



# ================================================================
# 2. Section: FUNCTIONS
# ================================================================



# ================================================================
# 3. Section: MAIN
# ================================================================
if __name__ == '__main__':
    study_group = scrap_folder(COMPARING_GROUP_FOLDER)
    control_group = scrap_folder(CONTROL_GROUP_FOLDER)

    print(study_group.min_distances_per_tp)
    print(study_group.mean_min_distance_per_tp)
