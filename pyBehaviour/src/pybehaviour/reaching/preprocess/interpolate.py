# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np



# ================================================================
# 1. Section: Functions
# ================================================================
def interpolate(data: np.ndarray) -> np.ndarray:
    # 1. Extract the data
    data = np.asarray(data, dtype=float).copy()

    # 2. Check if there are NaN to fill
    nan_mask = np.isnan(data)
    if not nan_mask.any():
        return data

    # 3. Check if there is enough "data"
    valid_mask = ~nan_mask
    if not valid_mask.any():
        return data

    # 4. Apply the Mask
    x = np.arange(len(data))
    data[nan_mask] = np.interp(x[nan_mask], x[valid_mask], data[valid_mask])

    return data
