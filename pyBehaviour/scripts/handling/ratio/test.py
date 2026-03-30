# ================================================================
# 0. Section: IMPORTS
# ================================================================
from pathlib import Path
from pybehaviour.io import Group



# ================================================================
# 1. Section: INPUTS
# ================================================================
ROOT: Path = Path(__file__).resolve().parents[4]
BASE_FOLDER: Path = ROOT / "data" / "handling"

COMPARING_GROUP_FOLDER: Path = BASE_FOLDER / "study"
COMPARING_GROUP_NAME: str = r"Treated$^{MdD-MdV}$"
COMPARING_GROUP_NUMBER: int = 71

CONTROL_GROUP_FOLDER: Path = BASE_FOLDER / "control"
CONTROL_GROUP_NAME: str = "#46 Untreated Injury"
CONTROL_GROUP_NUMBER: int = 46

TO_KEEP_PATH: Path = ROOT / "data" / "mice_to_keep.json"
OUTPUT_FOLDER: Path = ROOT / "out" / "handling"



# ================================================================
# 2. Section: FUNCTIONS
# ================================================================



# ================================================================
# 3. Section: MAIN
# ================================================================
if __name__ == '__main__':
    study_group = Group(
        COMPARING_GROUP_FOLDER,
        COMPARING_GROUP_NAME,
        COMPARING_GROUP_NUMBER,
        TO_KEEP_PATH
    )
    control_group = Group(
        CONTROL_GROUP_FOLDER,
        CONTROL_GROUP_NAME,
        CONTROL_GROUP_NUMBER,
        TO_KEEP_PATH
    )
