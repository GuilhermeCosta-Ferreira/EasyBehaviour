# ================================================================
# 0. Section: IMPORTS
# ================================================================
import re

from pathlib import Path
from operator import contains

from .dataclass import SylableMetaData
from ...logger import logger



# ================================================================
# 1. Section: Functions
# ================================================================
def get_metadata(file: Path) -> SylableMetaData:
    # 1. Extract the meta
    group = get_group(file.stem)
    timepoint = get_timepoint(file.stem)
    mouse = get_mouse(file.stem)

    # 2. Fills the instance
    metadata = SylableMetaData(
        group=group,
        timepoint=timepoint,
        mouse=mouse,
    )

    return metadata


# ──────────────────────────────────────────────────────
# 1.1 Subsection: Get the individual metadata
# ──────────────────────────────────────────────────────
def get_timepoint(file: str) -> str:
    if(contains(file.lower(), "_bl_")): return "BL"
    elif(contains(file.lower(), "_w1_")): return "Post_W1"
    elif(contains(file.lower(), "_w4_")): return "Post_W4"
    elif(contains(file.lower(), "_w8_")): return "Post_W8"
    else:
        logger.warning(f"Timepoint not found in {file}")
        return "undefined"

def get_group(file: str) -> int:
    return int(file[:2])

def get_mouse(file: str) -> str:
    # 1. Extract the content from the file name
    mouse = re.search(r'_(\d+)([A-Za-z])_|_([A-Za-z])(\d+)_', file)

    # 2. Asserts we find something
    if not mouse:
        logger.warning(f"Mouse not found in {file}")
        return "undefined"

    # 3. Separates the number and cage
    if mouse.group(1) is not None:        # _numberletter_
        num, cage = mouse.group(1), mouse.group(2)
    else:                              # _letternumber_
        cage, num = mouse.group(3), mouse.group(4)

    return f"{num}{cage.upper()}"
