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
GROUP_FOLDER: Path = DLC_FOLDER / "71_reaching"
GROUP_NAME: str = "#71_MdD_MdV_regen"



# ================================================================
# 2. Section: MAIN
# ================================================================
if __name__ == '__main__':
    study_group = scrap_folder(GROUP_FOLDER, GROUP_NAME)
