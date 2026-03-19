# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pandas as pd
import numpy as np

from .interpolate import interpolate
from ..io import File
from ...logger import logger

NAN_RATIO_LIMIT: float = 25



# ================================================================
# 1. Section: Functions
# ================================================================
def likelihood_filter(data_file: File,
    threshold: float,
    ratio_limit: float = NAN_RATIO_LIMIT,
    fill_nan: bool = True
) -> pd.DataFrame:
    # 1. Extract the data
    wrist_df = data_file.wrist_df.copy()

    # 2. Apply the likelihood filetring
    x, y = low_likelihood_to_nan(wrist_df, threshold, ratio_limit)

    # 3. Interpolates NaN values if needed
    if fill_nan:
        x = interpolate(x)
        y = interpolate(y)

    # 4. Store back into df
    wrist_df["x"] = x
    wrist_df["y"] = y

    # 5. Compute the NaN ratio
    nan_ratio = wrist_df["x"].isna().mean() * 100
    nan_nr = wrist_df["x"].isna().sum()

    if(nan_ratio > ratio_limit):
        nan_msg = f"The {data_file.path} has too many NaNs: {nan_nr} ({nan_ratio:.2f}%)"
        logger.warning(nan_msg)
        data_file.ignore = True

    return wrist_df


# ──────────────────────────────────────────────────────
# 1.1 Subsection: Helper Functions
# ──────────────────────────────────────────────────────
def low_likelihood_to_nan(
    wrist_df: pd.DataFrame,
    threshold: float,
    ratio_limit: float
) -> tuple:
    # 1. Extract the data
    likelihood = np.array(wrist_df["likelihood"])
    x = wrist_df["x"].to_numpy()
    y = wrist_df["y"].to_numpy()

    # 2. Fill the low likelihood as NaNs
    x = np.where(likelihood < threshold, np.nan, x)
    y = np.where(likelihood < threshold, np.nan, y)

    return x, y
