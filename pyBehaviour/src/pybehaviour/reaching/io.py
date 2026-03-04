# ================================================================
# 0. Section: IMPORTS
# ================================================================
import re
import json

import numpy as np

from pathlib import Path

from .GroupScrap import GroupScrap
from ..logger import logger

DATE_PATTERN: str = r"\d{4}-\d{1,2}-\d{1,2}"
MOUSE_PATTERN: str = r"ReachingBot\d+_([0-9]+[A-Z]?)_\d{4}-\d{1,2}-\d{1,2}"



# ================================================================
# 1. Section: Functions
# ================================================================
def scrap_folder(folder_path: Path) -> GroupScrap:
    # 1. Get all the usefull file data from the group folder
    timepoint_dict = get_timepoint_dict(folder_path)
    csv_files = get_labels_path(folder_path)

    # 2. Get content info
    dates_present = get_dates(csv_files)
    mice_present = get_mice(csv_files)

    # 3. Saves it in a dataclass
    data = GroupScrap(
        timepoint_dict=timepoint_dict,
        files=csv_files,
        dates=dates_present,
        mice=mice_present
    )
    return data


# ──────────────────────────────────────────────────────
# 1.1 Subsection: Individual scrappers
# ──────────────────────────────────────────────────────
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

def get_labels_path(folder_path: Path) -> np.ndarray:
    # 1. Gets all the csv files in the group folder
    return np.asarray(sorted(folder_path.glob("*.csv")))

def get_dates(files: np.ndarray) -> np.ndarray:
    # 1. Define the pattern
    date_pattern = re.compile(DATE_PATTERN)

    # 2. Iterates over the files and finds the uniques
    dates = sorted({m.group() for f in files if (m := date_pattern.search(f.name))})
    return np.asarray(dates)

def get_mice(files: np.ndarray) -> np.ndarray:
    # 1. Define the pattern
    mouse_pattern = re.compile(MOUSE_PATTERN)

    # 2. Iterates over the files and finds the uniques
    mice = sorted({m.group(1) for f in files if (m := mouse_pattern.search(f.name))})
    return np.asarray(mice)
