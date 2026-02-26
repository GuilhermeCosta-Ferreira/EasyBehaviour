# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pandas as pd
import numpy as np

from pathlib import Path

from .group_analysis import build_batch_summary_df



# ================================================================
# 1. Section: Builds Average df
# ================================================================
def build_average_df(
    input_dir: Path,
    conditions: np.ndarray | list,
    threshold: float = 0.8
) -> pd.DataFrame:

    # 1. Compute data per video
    data_per_video = build_batch_summary_df(input_dir, conditions, threshold)

    # 2. Drop the videos in which over 50% of frames are excluded
    data_per_video = data_per_video[data_per_video['frames_excluded'] < 50]

    # 3. Identify feature columns
    non_feature_columns = ['animal', 'condition', 'weight', 'frames_excluded']
    feature_columns = [col for col in data_per_video.columns if col not in non_feature_columns]

    # 4. Group by `animal` and `condition` and compute weighted averages
    weighted_avgs = data_per_video.groupby(['animal', 'condition']).apply(
        lambda group: compute_weighted_avg(group, feature_columns=feature_columns)
    )
    weighted_avgs = weighted_avgs.reset_index()

    return weighted_avgs


# ──────────────────────────────────────────────────────
# 1.1 Subsection: Helper Functions
# ──────────────────────────────────────────────────────
def compute_weighted_avg(group: pd.DataFrame, feature_columns: list) -> pd.DataFrame:
    weights = group['weight']
    weighted_avg = group[feature_columns].multiply(weights, axis=0).sum() / weights.sum()

    return weighted_avg
