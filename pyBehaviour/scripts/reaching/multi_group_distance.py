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
BASE_FOLDER: Path = Path(__file__).resolve().parents[3] / "data/reaching"

COMPARING_GROUP_FOLDER: Path = BASE_FOLDER / "study"
COMPARING_GROUP_NAME: str = r"Treated$^{MdD-MdV}$"

CONTROL_GROUP_FOLDER: Path = BASE_FOLDER / "control"
CONTROL_GROUP_NAME: str = "#46 Untreated Injury"



# ================================================================
# 2. Section: MAIN
# ================================================================
if __name__ == '__main__':
    study_group = scrap_folder(COMPARING_GROUP_FOLDER, COMPARING_GROUP_NAME)
    control_group = scrap_folder(CONTROL_GROUP_FOLDER, CONTROL_GROUP_NAME)

    multigroup_comparision(control_group, study_group)
    multigroup_chronic_comparision(control_group, study_group)
    plt.show()
