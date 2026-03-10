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
CONTROL_GROUP_FOLDER: Path = DLC_FOLDER / "46_reaching"



# ================================================================
# 2. Section: FUNCTIONS
# ================================================================



# ================================================================
# 3. Section: MAIN
# ================================================================
if __name__ == '__main__':
    csv_files_names = np.array([filename for filename in os.listdir(COMPARING_GROUP_FOLDER) if filename.endswith('.csv')])
    timepoint_json = np.array([filename for filename in os.listdir(COMPARING_GROUP_FOLDER) if filename.endswith('.json')])

    study_group = scrap_folder(COMPARING_GROUP_FOLDER)

    print(study_group.min_distances_per_tp)
    print(study_group.mean_min_distance_per_tp)
