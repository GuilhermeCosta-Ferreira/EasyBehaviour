# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pandas as pd

from pathlib import Path

from pybehaviour.reaching.io import get_labels_path



# ================================================================
# 1. Section: INPUTS
# ================================================================
BASE_FOLDER: Path = Path(__file__).resolve().parents[3] / "data/reaching"
GROUP_FOLDER: Path = BASE_FOLDER / "study"



# ================================================================
# 3. Section: MAIN
# ================================================================
if __name__ == '__main__':
    # 1. Get the sorted csv files
    csv_files = get_labels_path(GROUP_FOLDER / "raw")
    csv_files = [file.name.split("DLC")[0] for file in csv_files]

    # 2. Generate the dataframe
    df = pd.DataFrame(
        {
            "name": csv_files,
            "state": None
        }
    )

    # 3. Save it as excel in the group folder
    file_path = GROUP_FOLDER / "file_list_label.xlsx"
    df.to_excel(file_path, index=False)
    print(f"Saved at {file_path}")
