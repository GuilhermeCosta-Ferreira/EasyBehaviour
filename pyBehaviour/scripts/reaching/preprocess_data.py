# ================================================================
# 0. Section: IMPORTS
# ================================================================
import shutil

import pandas as pd

from pathlib import Path

from pybehaviour.reaching import (
    scrap_folder,
    review_preprocess,
    generate_all_possible_preprocess
)



# ================================================================
# 1. Section: INPUTS
# ================================================================
BASE_FOLDER: Path = Path(__file__).resolve().parents[3] / "data/reaching"

GROUP_FOLDER: Path = BASE_FOLDER / "study"
GROUP_NAME: str = "#71_MdD_MdV_regen"
PROCESSED_FOLDER: Path = GROUP_FOLDER / "processed"

FILE_PATH: Path = GROUP_FOLDER / "file_list_label.xlsx"
JSON_PATH: Path = BASE_FOLDER / "reaching_states.json"



# ================================================================
# 2. Section: FUNCTIONS
# ================================================================
def move_good_quality(file, out_path: Path) -> Path:
    csv_path = file.path

    destination = out_path / csv_path.name
    shutil.copy2(csv_path, destination)

    return destination

def get_file_state(file, labels_df: pd.DataFrame) -> int | None:
    match = labels_df.loc[
        labels_df["name"] == file.file_name, "state"
    ]
    if not match.empty:
        return int(match.iloc[0])
    else:
        return None



# ================================================================
# 3. Section: MAIN
# ================================================================
if __name__ == '__main__':
    video_labels_df = pd.read_excel(FILE_PATH)
    study_group = scrap_folder(GROUP_FOLDER, GROUP_NAME, csv_folder_name="raw")

    for file in study_group.files:
        # 1. Extract the file's state label
        state = get_file_state(file, video_labels_df)
        if state is None:
            print(f"{file.file_name} not found in dataframe")
            continue

        # 2. If it is perfect video, it can get stored directly (no change needed)
        if state == 0:
            dest = move_good_quality(file, PROCESSED_FOLDER)

        # 3. If it did not reach, it will not get moved
        elif state == 1:
            continue

        # 4. Aply automation selection
        elif state == 2:
            possible_files = generate_all_possible_preprocess(file)
            review_preprocess(possible_files, PROCESSED_FOLDER)
