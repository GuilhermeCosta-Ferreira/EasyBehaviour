# ================================================================
# 0. Section: IMPORTS
# ================================================================
from matplotlib import pyplot as plt

from pathlib import Path

from pybehaviour.reaching import(
    scrap_folder,
    multigroup_comparision,
)



# ================================================================
# 1. Section: INPUTS
# ================================================================
DLC_FOLDER: Path = Path("../data/dlc")
COMPARING_GROUP_FOLDER: Path = DLC_FOLDER / "71_reaching"
COMPARING_GROUP_NAME: str = "#71_MdD_MdV_regen"

CONTROL_GROUP_FOLDER: Path = DLC_FOLDER / "46_reaching"
CONTROL_GROUP_NAME: str = "#46_untreated_injury"



# ================================================================
# 2. Section: MAIN
# ================================================================
if __name__ == '__main__':
    study_group = scrap_folder(COMPARING_GROUP_FOLDER, COMPARING_GROUP_NAME)
    control_group = scrap_folder(CONTROL_GROUP_FOLDER, CONTROL_GROUP_NAME)

    multigroup_comparision(control_group, study_group)
    plt.show()
