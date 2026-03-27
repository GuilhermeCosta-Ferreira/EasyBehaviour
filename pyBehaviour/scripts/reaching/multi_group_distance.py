# ================================================================
# 0. Section: IMPORTS
# ================================================================
from matplotlib import pyplot as plt

from pathlib import Path

from pybehaviour.reaching import(
    scrap_folder,
    multigroup_comparision,
    multigroup_chronic_comparision
)



# ================================================================
# 1. Section: INPUTS
# ================================================================
ROOT: Path = Path(__file__).resolve().parents[3]
BASE_FOLDER: Path = ROOT / "data/reaching"

COMPARING_GROUP_FOLDER: Path = BASE_FOLDER / "study"
COMPARING_GROUP_NAME: str = r"Treated$^{MdD-MdV}$"
COMPARING_GROUP_NUMBER: int = 71

CONTROL_GROUP_FOLDER: Path = BASE_FOLDER / "control"
CONTROL_GROUP_NAME: str = "#46 Untreated Injury"
CONTROL_GROUP_NUMBER: int = 46

OUTPUT_FOLDER: Path = ROOT / "out/reaching"



# ================================================================
# 2. Section: MAIN
# ================================================================
if __name__ == '__main__':
    # 1. Load the data
    study_group = scrap_folder(COMPARING_GROUP_FOLDER, COMPARING_GROUP_NAME, COMPARING_GROUP_NUMBER, csv_folder_name="processed")
    control_group = scrap_folder(CONTROL_GROUP_FOLDER, CONTROL_GROUP_NAME, CONTROL_GROUP_NUMBER)

    # 2. Plot the data
    multigroup_comparision(control_group, study_group, OUTPUT_FOLDER, is_save=True)
    multigroup_chronic_comparision(control_group, study_group, OUTPUT_FOLDER, is_save=True)
    plt.show()
