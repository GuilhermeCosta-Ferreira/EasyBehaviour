# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pandas as pd
import numpy as np

from .distances import euclidean_distance, get_finger_pair_distances



# ================================================================
# 1. Section: Update the Distance DF
# ================================================================
def add_finger_distance_df(dlc_df: pd.DataFrame, output_df: pd.DataFrame) -> pd.DataFrame:
    # 1. Total distance between mid and tip part of the fingers for both hands
    output_df['dist_mid_l'] = get_finger_pair_distances(dlc_df, hand='l', finger='mid')
    output_df['dist_tip_l'] = get_finger_pair_distances(dlc_df, hand='l', finger='tip')
    output_df['dist_mid_r'] = get_finger_pair_distances(dlc_df, hand='r', finger='mid')
    output_df['dist_tip_r'] = get_finger_pair_distances(dlc_df, hand='r', finger='tip')

    # 2. Ratio between finger parts' distances in injured and uninjured hand
    output_df['ratio_dist_mid'] = output_df['dist_mid_l']/output_df['dist_mid_r']
    output_df['ratio_dist_tip'] = output_df['dist_tip_l']/output_df['dist_tip_r']

    return output_df

def add_distance_from_cereal(dlc_df: pd.DataFrame, output_df:pd.DataFrame) -> pd.DataFrame:
    # 1. Distance between cereal and nose
    output_df['dist_nose'] = dlc_df.apply(euclidean_distance, axis=1, point_1='cereal', point_2='nose')

    # 2. Build all distances to cereal
    conds = ["l", "r"]
    phals = ["mid", "tip"]
    fingers = ["1", "2", "3", "4"]

    # 3. DBuilds the istance columns
    dist_cols = {("mid", "l"): [], ("mid", "r"): [], ("tip", "l"): [], ("tip", "r"): []}

    # 4. Get's the cereal as numpy
    cx = dlc_df["cereal_x"].to_numpy()
    cy = dlc_df["cereal_y"].to_numpy()

    # 5. Gets the individual distances
    for cond in conds:
        for phal in phals:
            for finger in fingers:
                point = f"{cond}_{phal}_{finger}"
                dx = dlc_df[f"{point}_x"].to_numpy() - cx
                dy = dlc_df[f"{point}_y"].to_numpy() - cy
                col = f"dist_{cond}_{phal}_{finger}"
                output_df[col] = np.hypot(dx, dy)
                dist_cols[(phal, cond)].append(col)

    # 6. Gets the aggregates (avg + min)
    for phal in phals:
        for cond in conds:
            cols = dist_cols[(phal, cond)]
            output_df[f"avg_dist_{phal}_{cond}"] = output_df[cols].mean(axis=1)
            output_df[f"min_dist_{phal}_{cond}"] = output_df[cols].min(axis=1)

    # 7. Gets the ratios (l / r)
    for phal in phals:
        output_df[f"ratio_avg_dist_{phal}"] = output_df[f"avg_dist_{phal}_l"] / output_df[f"avg_dist_{phal}_r"]
        output_df[f"ratio_min_dist_{phal}"] = output_df[f"min_dist_{phal}_l"] / output_df[f"min_dist_{phal}_r"]

    return output_df
