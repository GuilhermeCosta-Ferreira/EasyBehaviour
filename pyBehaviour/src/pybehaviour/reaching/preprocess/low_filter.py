# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np
import pandas as pd

from scipy.signal import butter, sosfiltfilt

from ..io import File



# ================================================================
# 1. Section: Functions
# ================================================================
def low_pass_filter(data_file: File) -> pd.DataFrame:
    # 1. Extract the data
    wrist_df = data_file.wrist_df.copy()

    # 2. Apply the filter
    x = apply_low_pass_filter(wrist_df["x"].to_numpy())
    y = apply_low_pass_filter(wrist_df["y"].to_numpy())

    # 3. Add back into the wrist_df
    wrist_df["x"] = x
    wrist_df["y"] = y

    return wrist_df


# ──────────────────────────────────────────────────────
# 1.1 Subsection: Helper Functions
# ──────────────────────────────────────────────────────
def apply_low_pass_filter(
    data: np.ndarray,
    cutoff: float = 7.0,
    fs: float = 60.0
) -> np.ndarray:
    # 1. center the data
    data_mean = np.mean(data)
    data = data - data_mean

    # 2. Apply the low pass filter and add back the mean
    sos = butter(4, cutoff, btype="low", fs=fs, output="sos")
    data_filtered = sosfiltfilt(sos, data) + data_mean

    return data_filtered
