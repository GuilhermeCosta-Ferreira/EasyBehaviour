# ================================================================
# 0. Section: IMPORTS
# ================================================================
import re
import json

import numpy as np

from pathlib import Path

DATE_PATTERN: str = r"\d{4}-\d{1,2}-\d{1,2}"
MOUSE_PATTERN: str = r"_([0-9]+[A-Z]?)_"



# ================================================================
# 1. Section: Metadata extraction from file name
# ================================================================
def get_unique_metadata(files: np.ndarray, pattern: str):
    # 1. Define the pattern
    pattern_re = re.compile(pattern)

    # 2. Iterates over the files and finds the uniques
    uniques = sorted({m.group().replace("_", "") for f in files if (m := pattern_re.search(f.name))})
    return np.asarray(uniques)

def get_file_metadata(file: Path, pattern: str) -> str | None:
    # 1. Define the pattern
    pattern_re = re.compile(pattern)

    # 2. Finds the pattern
    match = pattern_re.search(file.name)
    return match.group(0).replace("_", "") if match else None

def get_video_path(folder_path: Path, file_name: str) -> Path:
    base = folder_path.parent / "videos" / file_name

    for ext in (".avi", ".mp4", ".MOV"):
        candidate = base.with_suffix(ext)
        if candidate.exists():
            return candidate

    raise FileNotFoundError(
        f"No video file found for {file_name} with extensions .avi, .mp4, or .MOV"
    )

def get_mice_to_remove(mice_to_keep: Path, group_number: int) -> list:
    with open(mice_to_keep, "r") as f:
        mice_to_keep_all = json.load(f)
    group_keep_info = next(item for item in mice_to_keep_all["to_keep"] if item["group_id"] == group_number)
    return group_keep_info["remove"]

def get_labels_path(folder_path: Path, ending: str = "*.csv") -> np.ndarray:
    # 1. Gets all the csv files in the group folder
    return np.asarray(sorted(folder_path.glob(ending)))
