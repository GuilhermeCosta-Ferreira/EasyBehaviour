# ================================================================
# 0. Section: IMPORTS
# ================================================================
import os

import pandas as pd

from pathlib import Path



# ================================================================
# 1. Section: Functions
# ================================================================
def get_dlc_dataframe(folder_path: Path, file_name: str) -> pd.DataFrame:
    # 1. Builds the file path
    file_path = os.path.join(folder_path, file_name)

    # 2. Create header combining second and third rows (e.g. nose_x)
    header = pd.read_csv(file_path, nrows=2, header=0)
    combined_columns = header.iloc[0] + "_" + header.iloc[1]

    # 3. Builds the dataframe with the column naming fixed
    dlc_df = pd.read_csv(file_path, skiprows=2, header=None)
    dlc_df.columns = combined_columns

    # 4. Convert all cells excluding header to numbers
    dlc_df = dlc_df.iloc[1:].astype(float)
    dlc_df = dlc_df.rename(columns={dlc_df.columns[0]: 'frame_idx'})

    # 5. Rename first column as frame_idx containing integers
    dlc_df['frame_idx'] = dlc_df['frame_idx'].astype(int)

    # 6. Drop likelihoods of nose and feet to avoid filtering too many points
    dlc_df = dlc_df.drop(columns=['nose_likelihood', 'foot_left_likelihood', 'foot_right_likelihood'])

    return dlc_df
