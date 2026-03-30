# ================================================================
# 0. Section: IMPORTS
# ================================================================
import json

import numpy as np

from pathlib import Path

from ...logger import logger



# ================================================================
# 1. Section: Functions
# ================================================================
def get_timepoint_dict(folder_path: Path) -> dict:
    # 1. Get all the json files in the group folder
    timepoint_json = sorted(folder_path.glob("*.json"))

    # 2. Makes sure we only get one
    if len(timepoint_json) > 1:
        logger.warning(
            "Timepoint JSONS found where more than one, defaulting to the first\n"
            f"{len(timepoint_json)} found, selected: {timepoint_json[0]}"
        )
    json_path = timepoint_json[0]

    # 3. Loads the file into a dict
    with json_path.open("r", encoding="utf-8") as f:
        return json.load(f)

def get_labels_path(folder_path: Path, ending: str = "*.csv") -> np.ndarray:
    # 1. Gets all the csv files in the group folder
    return np.asarray(sorted(folder_path.glob(ending)))
