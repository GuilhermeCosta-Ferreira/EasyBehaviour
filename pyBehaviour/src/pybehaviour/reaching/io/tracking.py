# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pandas as pd



# ================================================================
# 1. Section: Functions
# ================================================================
def get_best_label(bp_df: pd.DataFrame, best_idx: int) -> tuple[int, int]:
    x = bp_df.loc[best_idx]['x']
    y = bp_df.loc[best_idx]['y']

    return (int(x), int(y))
