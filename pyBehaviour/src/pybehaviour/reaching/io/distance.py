# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pandas as pd
import numpy as np



# ================================================================
# 1. Section: Functions
# ================================================================
def get_mindist(df: pd.DataFrame) -> tuple[tuple, pd.DataFrame]:
    # 1. Check if the ('distance', 'wrist_robot') exists, if not add it
    df = add_wristrobot_distance(df)

    # 2. Get the bodyparts coords where distance is minimum
    distances = df[('distance', 'wrist_robot')]
    min_distance_idx = distances.idxmin()
    min_distance = np.round(distances.agg('min'),2)

    return (min_distance_idx, min_distance), df


# ──────────────────────────────────────────────────────
# 1.1 Subsection: Helper Functions
# ──────────────────────────────────────────────────────
def add_wristrobot_distance(df: pd.DataFrame) -> pd.DataFrame:
    try:
        wrist_x = df[('wrist', 'x')]
        wrist_y = df[('wrist', 'y')]
        robot_x = df[('robot_arm', 'x')]
        robot_y = df[('robot_arm', 'y')]
    except:
        raise ValueError(f"{df.head()}")

    distances = np.sqrt((wrist_x - robot_x)**2 + (wrist_y - robot_y)**2)
    df[('distance', 'wrist_robot')] = distances

    return df
