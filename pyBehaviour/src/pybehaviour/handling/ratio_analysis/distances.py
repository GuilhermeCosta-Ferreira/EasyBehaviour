# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np
import pandas as pd



# ================================================================
# 1. Section: Distances
# ================================================================
def euclidean_distance(df: pd.DataFrame, point_1:str , point_2: str) -> np.ndarray:
    x_dist = (df[point_1 + '_x'] - df[point_2 + '_x'])
    y_dist = (df[point_1 + '_y'] - df[point_2 + '_y'])

    return np.sqrt(x_dist**2 + y_dist**2)

def get_finger_pair_distances(dlc_df: pd.DataFrame, hand: str, finger: str):
    point = hand + "_" + finger

    dist_12 = dlc_df.apply(euclidean_distance, axis=1, point_1=point+'_1', point_2=point+'_2')
    dist_23 = dlc_df.apply(euclidean_distance, axis=1, point_1=point+'_2', point_2=point+'_3')
    dist_34 = dlc_df.apply(euclidean_distance, axis=1, point_1=point+'_3', point_2=point+'_4')
    tot_dist = dist_12 + dist_23 + dist_34

    return tot_dist
