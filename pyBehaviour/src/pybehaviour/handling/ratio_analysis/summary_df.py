# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np
import pandas as pd



# ================================================================
# 1. Section: Build a single video summary
# ================================================================
def add_summary(
    name: str,
    condition: str,
    excl: float,
    summary_df: pd.DataFrame,
    dlc_df: pd.DataFrame,
    distance_df: pd.DataFrame,
) -> pd.DataFrame:

    row_data = {
        "animal": name,
        "condition": condition,
        "weight": dlc_df.size,  # Weight is the number of frames
        "frames_excluded": excl,  # Percentage of frames excluded
        "ratio_avg_dist_fingers_mid": distance_df["ratio_dist_mid"].mean(),
        "ratio_avg_dist_fingers_tip": distance_df["ratio_dist_tip"].mean(),
        "ratio_range_dist_mid": (  # Range of motion is the maximum distance between fingers
            distance_df["dist_mid_l"].max() / distance_df["dist_mid_r"].max()
        ),
        "ratio_range_dist_tip": (
            distance_df["dist_tip_l"].max() / distance_df["dist_tip_r"].max()
        ),
        "ratio_var_dist_mid": distance_df["dist_mid_l"].var()
        / distance_df["dist_mid_r"].var(),  # Variance of distance between fingers
        "ratio_var_dist_tip": distance_df["dist_tip_l"].var()
        / distance_df["dist_tip_r"].var(),
        "ratio_avg_dist_cereal_mid": distance_df["ratio_avg_dist_mid"].mean(),
        "ratio_avg_dist_cereal_tip": distance_df["ratio_avg_dist_tip"].mean(),
        "ratio_min_dist_cereal_mid": distance_df["ratio_min_dist_mid"].mean(),
        "ratio_min_dist_cereal_tip": distance_df["ratio_min_dist_tip"].mean(),
    }

    row = pd.DataFrame([row_data])
    summary_df = pd.concat([summary_df, row], ignore_index=True)

    return summary_df

def init_summary_df() -> pd.DataFrame:
    return pd.DataFrame(
        np.nan,
        columns=[
            "animal",
            "condition",
            "weight",
            "frames_excluded",
            "ratio_avg_dist_fingers_mid",
            "ratio_avg_dist_fingers_tip",
            "ratio_range_dist_mid",
            "ratio_range_dist_tip",
            "ratio_var_dist_mid",
            "ratio_var_dist_tip",
            "ratio_avg_dist_cereal_mid",
            "ratio_avg_dist_cereal_tip",
            "ratio_min_dist_cereal_mid",
            "ratio_min_dist_cereal_tip",
        ],
        index=[0],
    )
