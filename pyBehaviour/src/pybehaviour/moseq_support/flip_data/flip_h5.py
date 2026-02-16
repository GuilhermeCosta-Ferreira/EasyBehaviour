# ================================================================
# 0. Section: IMPORTS
# ================================================================
import os

import pandas as pd

from pathlib import Path
from typing import cast

from .name_utils import build_flipped_name



# ================================================================
# 1. Section: Functions
# ================================================================
def flip_h5(h5_path: Path, video_shape: tuple, output_folder: Path) -> None:
    # 1. Load H5
    h5_df = cast(pd.DataFrame, pd.read_hdf(h5_path, key="df_with_missing"))
    h5_x_df = h5_df.xs("x", level="coords", axis=1)
    h5_y_df = h5_df.xs("y", level="coords", axis=1)

    # 2. Flip coordinates and get bp
    x_flipped = video_shape[0] - h5_x_df
    paired_bd = get_paired_bp(x_flipped)

    # 3. Loops over the pairs and switch the assigned ones
    scorer = x_flipped.columns.get_level_values("scorer")[0]
    for pair in paired_bd:
        if None in pair: continue

        # 1. Get the data
        left_x_data = x_flipped[(scorer, pair[0])]
        right_x_data = x_flipped[(scorer, pair[1])]
        left_y_data = h5_y_df[(scorer, pair[0])]
        right_y_data = h5_y_df[(scorer, pair[1])]

        # 2. Assigns the data
        x_flipped[(scorer, pair[0])] = right_x_data
        x_flipped[(scorer, pair[1])] = left_x_data
        h5_y_df[(scorer, pair[0])] = right_y_data
        h5_y_df[(scorer, pair[1])] = left_y_data

    # 4. Apply changes
    idx = pd.IndexSlice
    h5_df.loc[:, idx[:, :, "x"]] = x_flipped.to_numpy()
    h5_df.loc[:, idx[:, :, "y"]] = h5_y_df.to_numpy()

    # 5. Store file
    output_path = build_flipped_name(h5_path, output_folder)
    os.makedirs(output_folder, exist_ok=True)
    h5_df.to_hdf(
        output_path,
        key="df_with_missing",  # same key DLC uses
        mode="w"                # overwrite if file exists
    )



# ──────────────────────────────────────────────────────
# 1.2 Subsection: Handle Bodyparts
# ──────────────────────────────────────────────────────
def get_paired_bp(df):
    # 1. Get bodyparts in order of appearance in the columns
    bodyparts = list(dict.fromkeys(df.columns.get_level_values("bodyparts")))

    # 2. Initialize for loop
    bp_set = set(bodyparts)
    pairs = []
    used = set()

    for bp in bodyparts:
        # 1. Assure it does not go over already paired bp
        if bp in used:
            continue

        # 2. Get the righ counterpart
        r = right_of(bp)

        # 3. If it's a left part and the matching right exists, pair them
        if r is not None and r in bp_set:
            pairs.append((bp, r))
            used.add(bp)
            used.add(r)
        # 4. If it's a right part whose left exists, skip (will be handled when left is seen)
        elif bp.startswith("r_") and ("l_" + bp[2:]) in bp_set:
            continue
        # 5. Otherwise singleton
        else:
            pairs.append((bp, None))
            used.add(bp)

    return pairs

def right_of(bp: str) -> str | None:
    if bp.endswith("_left"):
        return bp[:-5] + "_right"
    if bp.startswith("l_"):
        return "r_" + bp[2:]
    return None
