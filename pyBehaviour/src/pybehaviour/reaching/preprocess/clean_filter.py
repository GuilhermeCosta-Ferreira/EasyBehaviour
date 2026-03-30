# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pandas as pd

from ..io import ReachingFile



# ================================================================
# 1. Section: Functions
# ================================================================
def clean_filter(data_file: ReachingFile) -> pd.DataFrame:
    return data_file.wrist_df
