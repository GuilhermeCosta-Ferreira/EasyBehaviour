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
DLC_FOLDER: Path = Path("../data/dlc/71_reaching")



# ================================================================
# 2. Section: FUNCTIONS
# ================================================================



# ================================================================
# 3. Section: MAIN
# ================================================================
if __name__ == '__main__':
    csv_files_names = np.array([filename for filename in os.listdir(DLC_FOLDER) if filename.endswith('.csv')])
    timepoint_json = np.array([filename for filename in os.listdir(DLC_FOLDER) if filename.endswith('.json')])

    print(scrap_folder(DLC_FOLDER).timepoints)
