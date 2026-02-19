"""
Functions to run with the napari enviroment for napari app to check labels and update for reaching task

python scripts/check_labels.py \
  --v "2B_2025-12-10_trial1.avi" \
  --csv "2B_2025-12-10_trial1DLC_resnet50_REACHING_MOUSEBOT_2Apr1shuffle1_500000.csv"

"""
# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np
import pandas as pd
import napari
import argparse



# ================================================================
# 1. Section: Functions
# ================================================================
COLORS: list = ["red", "blue", "yellow"]*100
INPUT_FOLDER: str = "../data/napari_reaching/"



# ================================================================
# 1. Section: Functions
# ================================================================
def add_labels(
    viewer : napari.Viewer,
    csv_path: str,
    p_cutoff: float = 1,
    size: int = 6
) -> int:
    df = pd.read_csv(csv_path, header=[0, 1, 2])
    bodyparts = df.columns.get_level_values(1).unique()

    added = 0
    for idx, bp in enumerate(bodyparts):
        try:
            x = df.xs((bp, "x"), axis=1, level=[1, 2]).to_numpy().ravel()
            y = df.xs((bp, "y"), axis=1, level=[1, 2]).to_numpy().ravel()
            p = df.xs((bp, "likelihood"), axis=1, level=[1, 2]).to_numpy().ravel()
        except Exception:
            continue

        frames = np.arange(x.shape[0])
        keep = np.isfinite(x) & np.isfinite(y) & (p >= p_cutoff)
        pts = np.column_stack([frames[keep], y[keep], x[keep]])

        if len(pts):
            viewer.add_points(pts, name=str(bp), size=size, face_color = COLORS[idx])
            added += 1

    return added

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



# ================================================================
# 1. Section: MAIN
# ================================================================
if __name__ == '__main__':
    ap = argparse.ArgumentParser(description="Open a video in napari and overlay DLC CSV keypoints.")
    ap.add_argument("--v", required=True, help="Path to video (mp4/avi).")
    ap.add_argument("--csv", required=True, help="Path to DLC CSV (3-row header format).")
    ap.add_argument("--p", type=float, default=0.9, help="Likelihood cutoff (default: 0.9).")
    ap.add_argument("--size", type=float, default=6, help="Point size (default: 6).")
    ap.add_argument("--frame", type=int, default=0, help="Frame index to start on (default: 0).")
    args = ap.parse_args()

    viewer = napari.Viewer()

    video_path = INPUT_FOLDER + args.v
    csv_path = INPUT_FOLDER + args.csv

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

    n = add_labels(viewer, csv_path, p_cutoff=args.p, size=args.size)
    print(f"Added {n} bodypart layers from: {args.csv}")

    napari.run()
