# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np
import pandas as pd

from pathlib import Path

from .distance_df import add_distance_from_cereal, add_finger_distance_df
from .io import get_dlc_dataframe
from .preprocessing import filter_by_likelihood
from .summary_df import init_summary_df, add_summary



# ================================================================
# 1. Section: Builds Group
# ================================================================
def build_batch_summary_df(
    input_dir: Path,
    conditions: np.ndarray | list,
    threshold: float = 0.6
) -> pd.DataFrame:

    # 1. Initialize the summary df
    summary_df = init_summary_df()

    # 2. Loops over the conditions
    for condition_name in conditions:
        subfolder_path = input_dir / condition_name

        # 3. Builds the group summary
        summary_df = build_group_summary(
            subfolder_path,
            summary_df,
            threshold,
            condition_name,)

    # 3. Drop first row containing NaN used for initialization
    summary_df = summary_df.drop(0)

    return summary_df



# ================================================================
# 2. Section: Group Summary
# ================================================================
def build_group_summary(
    subfolder_path: Path,
    initial_summary_df: pd.DataFrame,
    threshold: float,
    condition_name: str
) -> pd.DataFrame:

    # 1. Loop over all videos in a group
    for file_name in subfolder_path.glob("*.csv"):
        file_name = file_name.name

        # 2. Update the summary with the video summary
        initial_summary_df = build_video_summary(
            subfolder_path,
            initial_summary_df,
            file_name,
            threshold,
            condition_name)

    return initial_summary_df



# ================================================================
# 3. Section: Video Summary
# ================================================================
def build_video_summary(
    subfolder_path: Path,
    summary_df: pd.DataFrame,
    file_name: str,
    threshold: float,
    condition_name: str
) -> pd.DataFrame:

    # 1. Initializes the DLC DF
    dlc_df = get_dlc_dataframe(subfolder_path, file_name)
    dlc_df, excl = filter_by_likelihood(dlc_df, threshold)

    # 2. Compute the identifiers
    name = file_name.split("_")[1]  # Animal name
    print(
        f"[{condition_name}] Animal: {name} | File: {file_name} | Frames Excluded: {excl:.2f}%"
    )
    if excl >= 50:
        print("Video likely to be EXCLUDED due to high frame loss (≥ 50%)")

    # 3. Initializes the Distance DF
    distance_df = pd.DataFrame()
    distance_df = add_finger_distance_df(dlc_df, distance_df)
    distance_df = add_distance_from_cereal(dlc_df, distance_df)

    return add_summary(name, condition_name, excl, summary_df, dlc_df, distance_df)
