# ================================================================
# 0. Section: IMPORTS
# ================================================================
import re

import pandas as pd
import numpy as np

from tqdm import tqdm

from pathlib import Path



# ================================================================
# 1. Section: INPUTS
# ================================================================
ROOT: Path = Path(__file__).resolve().parents[4]
BASE_FOLDER: Path = ROOT / "data" / "handling"

GROUP_FOLDER: Path = BASE_FOLDER / "control"
GROUP_NAME: str = "#46_injured_untreated"
GROUP_NUMBER: int = 46

PROCESSED_FOLDER: Path = GROUP_FOLDER / "processed"
RAW_FOLDER: Path = GROUP_FOLDER / "raw"

PATTERN: str = r'^(?P<group_number>\d+)_(?P<mouse_nr>[A-Z]\d+)_Kelloggs_(?P<timepoint>BL|1|4)_(?P<trial>[a-z]\d?)_selected(?P<model>DLC_.+)$'
CONVERTION_RULES: list = [
    ("foot_i", "left_foot"),
    ("foot_ui", "right_foot"),
    ("i_mid_1", "l_mid_1"),
    ("i_mid_2", "l_mid_2"),
    ("i_mid_3", "l_mid_3"),
    ("i_mid_4", "l_mid_4"),
    ("i_tip_1", "l_tip_1"),
    ("i_tip_2", "l_tip_2"),
    ("i_tip_3", "l_tip_3"),
    ("i_tip_4", "l_tip_4"),
    ("ui_mid_1", "r_mid_1"),
    ("ui_mid_2", "r_mid_2"),
    ("ui_mid_3", "r_mid_3"),
    ("ui_mid_4", "r_mid_4"),
    ("ui_tip_1", "r_tip_1"),
    ("ui_tip_2", "r_tip_2"),
    ("ui_tip_3", "r_tip_3"),
    ("ui_tip_4", "r_tip_4"),
]



# ================================================================
# 2. Section: FUNCTIONS
# ================================================================
def change_column_names(df: pd.DataFrame, rename_map: list | dict = CONVERTION_RULES) -> pd.DataFrame:
    # 1. Convert to dict if needed
    if isinstance(rename_map, list):
        rename_map = dict(rename_map)

    # 2. Rename each column name to the reference
    df = df.copy()
    df.columns = pd.MultiIndex.from_tuples(
        [
            (scorer, rename_map.get(bodypart, bodypart), coord)
            for scorer, bodypart, coord in df.columns
        ]
    )
    return df

def change_file_name(file_name: str, pattern: str = PATTERN) -> str:
    # 1. Extract the info from the path name into a dict
    match = re.match(pattern, file_name)
    if not match:
        raise ValueError(f"File {file_name} had no match")
    info = match.groupdict()

    # 2. deal with the mouse number
    mouse_out = f"{info["mouse_nr"][1]}{info["mouse_nr"][0]}"

    # 3. deal with the timepoint
    timepoint_map = {
        "1": "w1",
        "4": "w4",
        "BL": "BL",
    }
    timepoint_out = timepoint_map[info["timepoint"]]

    # 4. Deal with the trial number (a, a1, etc)
    trial_out = ord(info["trial"][0]) - ord('a') + 1
    if(len(info["trial"]) > 1):
        suff = int(info["trial"][1])
        trial_out = 7 + 2*trial_out - 2 + suff

    # 5. Builds the new name
    treatment = "untreated"
    new_name = (
        f"{info['group_number']}_{treatment}_{mouse_out}_handling_"
        f"{timepoint_out}_{str(trial_out)}_converted{info['model']}"
    )

    return new_name



# ================================================================
# 3. Section: MAIN
# ================================================================
if __name__ == '__main__':
    csv_files = np.asarray(sorted(RAW_FOLDER.glob("*.csv")))

    for file in tqdm(csv_files, unit="file", desc="Converting"):
        df = pd.read_csv(file, header=[0, 1, 2])
        df = change_column_names(df)

        file_name = change_file_name(file.stem)
        out_path = PROCESSED_FOLDER / f"{file_name}{file.suffix}"
        df.to_csv(out_path)
