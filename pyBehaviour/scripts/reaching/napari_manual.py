"""
Functions to run with the napari enviroment for napari app to check labels and update for reaching task

python scripts/reaching/napari_manual.py \
  --v "2B_2025-12-10_trial1.avi" \
  --csv "2B_2025-12-10_trial1DLC_resnet50_REACHING_MOUSEBOT_2Apr1shuffle1_500000.csv"

"""
# ================================================================
# 0. Section: IMPORTS
# ================================================================
import napari
import json
import re

import numpy as np
import pandas as pd

from pathlib import Path



# ================================================================
# 1. Section: Functions
# ================================================================
ROOT: Path = Path(__file__).resolve().parents[3]
BASE_FOLDER: Path = ROOT / "data/reaching"

COLORS: list = ["red", "blue", "yellow"]*100
INPUT_FOLDER: Path = BASE_FOLDER / "study"
OUT_FOLDER: Path = INPUT_FOLDER / "processed"

MOUSE_PATTERN: str = r"_([0-9]+[A-Z]?)_"
MICE_TO_KEEP: Path = ROOT / "data" / "mice_to_keep.json"

GROUP_NUMBER: int = 71


# ================================================================
# 1. Section: Functions
# ================================================================
def add_labels(
    viewer : napari.Viewer,
    size: int = 6
):
    pts = np.empty((0, 3), dtype=float)
    wrist_layer = viewer.add_points(pts, name=str("wrist"), size=size, face_color = "red")

    return wrist_layer

def build_csv(wrist_layer, ref_csv, out_csv):
    df = pd.read_csv(ref_csv, header=[0, 1, 2], index_col=0)
    df.columns.names = ["scorer", "bodyparts", "coords"]

    out = df.copy()
    out.loc[:, :] = np.nan

    # keep robot_arm data
    robot_mask = out.columns.get_level_values("bodyparts") == "robot_arm"
    out.loc[:, robot_mask] = df.loc[:, robot_mask]

    bp_mask = out.columns.get_level_values("bodyparts") == "wrist"
    scorer = out.columns[bp_mask].get_level_values("scorer")[0]

    x_col = (scorer, "wrist", "x")
    y_col = (scorer, "wrist", "y")
    l_col = (scorer, "wrist", "likelihood")

    pts = np.asarray(wrist_layer.data, dtype=float)

    if pts.size == 0:
        out.to_csv(out_csv)
        print(f"Saved empty/manual template to: {out_csv}")
        return

    ann = pd.DataFrame(pts, columns=["frame", "y", "x"])
    ann["frame"] = ann["frame"].round().astype(int)

    # keep last click per frame
    ann = ann.sort_values("frame").drop_duplicates(subset="frame", keep="last")

    # keep only valid frame numbers
    ann = ann[(ann["frame"] >= out.index.min()) & (ann["frame"] <= out.index.max())]

    frames = ann["frame"].to_numpy()

    out.loc[frames, x_col] = ann["x"].to_numpy()
    out.loc[frames, y_col] = ann["y"].to_numpy()
    out.loc[frames, l_col] = 1.0

    out.to_csv(out_csv)
    print(f"Saved manual DLC-style CSV to: {out_csv}")

def add_wristrobot_distance(df: pd.DataFrame) -> tuple:
    wrist_x = df[('wrist', 'x')]
    wrist_y = df[('wrist', 'y')]
    robot_x = df[('robot_arm', 'x')]
    robot_y = df[('robot_arm', 'y')]

    distances = np.sqrt((wrist_x - robot_x)**2 + (wrist_y - robot_y)**2)
    df[('distance', 'wrist_robot')] = distances

    return df, distances

def get_mindist(df: pd.DataFrame) -> tuple:
    # check if the ('distance', 'wrist_robot') exists, if not add it
    df, distances = add_wristrobot_distance(df)

    #get the bodyparts coords where distance is minimum
    min_distance_idx = distances.idxmin()
    min_distance = np.round(distances.agg('min'),2)

    return (min_distance_idx, min_distance, distances), df

def get_file_metadata(file: Path, pattern: str) -> str | None:
    # 1. Define the pattern
    pattern_re = re.compile(pattern)

    # 2. Finds the pattern
    match = pattern_re.search(file.name)
    return match.group(0) if match else None



# ================================================================
# 1. Section: MAIN
# ================================================================
if __name__ == '__main__':
    video_folder = INPUT_FOLDER / "videos"
    csv_folder = INPUT_FOLDER/ "raw"
    videos = sorted([p for ext in ("*.avi", "*.mp4", "*.mov", "*.mkv") for p in video_folder.glob(ext)])
    csv_files = sorted([p for ext in ("*.csv",) for p in csv_folder.glob(ext)])

    for video_path in videos:
        csv_path = next((csv for csv in csv_files if video_path.stem in csv.stem), None)

        mouse_id = get_file_metadata(video_path, MOUSE_PATTERN)
        if mouse_id is None:
            mouse_id = str(video_path.name).split("_")[0]
        else:
            mouse_id = mouse_id.replace("_", "")

        # 2. Remove mice that are not to be included
        with open(MICE_TO_KEEP, "r") as f:
            mice_to_keep_all = json.load(f)
        group_keep_info = next(item for item in mice_to_keep_all["to_keep"] if item["group_id"] == GROUP_NUMBER)
        mice_to_remove = group_keep_info["remove"]

        if mouse_id in mice_to_remove:
            print(f"{video_path} was ignored since {mouse_id} is to be removed")
            continue

        if csv_path is None:
            print(f"No CSV found for {video_path.name}")
            csv_path = csv_files[0]

        viewer = napari.Viewer()

        # Get the min distance that DLC produces
        df = pd.read_csv(csv_path, header=[1,2], index_col=0)
        min_dist, _ = get_mindist(df)
        start_frame = min_dist[0]
        print(f"Min_dist frame: {min_dist[0]} Min_dist distance: {min_dist[1]}")

        viewer.open(video_path)

        try:
            tmax = viewer.layers[0].data.shape[0] - 1
            start = int(np.clip(start_frame, 0, tmax))
            viewer.dims.set_point(0, start)
        except Exception:
            pass

        wrist_layer = add_labels(viewer, size=6)

        napari.run()

        # runs after you close the napari window
        out_csv = OUT_FOLDER / csv_path.name
        build_csv(wrist_layer, csv_path, out_csv)
