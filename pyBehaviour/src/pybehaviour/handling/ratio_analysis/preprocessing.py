# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pandas as pd



# ================================================================
# 1. Section: Filters
# ================================================================
def filter_by_likelihood(dlc_df: pd.DataFrame, threshold: float) -> tuple[pd.DataFrame, float]:
    # 1. Extract the data
    initial_size = dlc_df.size
    likelihood_cols = [col for col in dlc_df.columns if col.endswith('likelihood')]

    # 2. Builds a mask
    bad_marker_mask = (dlc_df[likelihood_cols] < threshold)

    # 3. Filter the dataset accroding to the mask
    filtered_df = dlc_df.loc[bad_marker_mask.sum(axis=1) <= 2].reset_index(drop=True)

    # 4. Calculates the video loss
    size_post = filtered_df.size
    excl =  (initial_size - size_post) / initial_size * 100

    return filtered_df, excl
