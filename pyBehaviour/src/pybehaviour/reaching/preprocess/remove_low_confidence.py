# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pandas as pd
import numpy as np

from ..io import File
from ...logger import logger

NAN_RATIO_LIMIT: float = 25



# ================================================================
# 1. Section: Functions
# ================================================================
def low_likelihood_to_nan(
    data_file: File,
    threshold: float,
    ratio_limit: float = NAN_RATIO_LIMIT
) -> pd.DataFrame:
    # 1. Extract the data
    wrist_df = data_file.wrist_df
    likelihood = np.array(wrist_df["likelihood"])
    x = np.array(wrist_df["x"])
    y = np.array(wrist_df["y"])

    # 2. Fill the low likelihood as NaNs
    x = np.where(likelihood < threshold, np.nan, x)
    y = np.where(likelihood < threshold, np.nan, y)

    # 3. Rebuilds the df
    wrist_df = pd.DataFrame(
        {
            "x": x,
            "y": y,
            "likelihood": likelihood,
        },
        index=wrist_df.index,
    )

    # 4. Compute the NaN ratio
    nan_ratio = wrist_df["x"].isna().mean() * 100
    nan_nr = wrist_df["x"].isna().sum()
    if(nan_ratio > ratio_limit):
        nan_msg = f"The {data_file.path} has too many NaNs: {nan_nr} ({nan_ratio:.2f}%)"
        logger.warning(nan_msg)
        data_file.ignore = True

    return wrist_df
