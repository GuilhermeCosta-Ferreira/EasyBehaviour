"""
Functions to run with the napari enviroment for napari app to check labels and update for reaching task
"""
# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np
import pandas as pd
import napari
import argparse

COLORS = ["red", "blue", "yellow"]*100

# ================================================================
# 1. Section: Functions
# ================================================================
def add_labels(
    viewer : napari.Viewer,
    csv_path: str,
    p_cutoff: float = 1,
    size: int = 6
):
    """Read a DLC 3-row-header CSV and add one Points layer per bodypart."""
    df = pd.read_csv(csv_path, header=[0, 1, 2])
    bodyparts = df.columns.get_level_values(1).unique()

    added = 0
    print(df.head())
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



# ================================================================
# 1. Section: MAIN
# ================================================================
if __name__ == '__main__':
    ap = argparse.ArgumentParser(description="Open a video in napari and overlay DLC CSV keypoints.")
    ap.add_argument("--video", required=True, help="Path to video (mp4/avi).")
    ap.add_argument("--csv", required=True, help="Path to DLC CSV (3-row header format).")
    ap.add_argument("--p", type=float, default=0.9, help="Likelihood cutoff (default: 0.9).")
    ap.add_argument("--size", type=float, default=6, help="Point size (default: 6).")
    args = ap.parse_args()

    viewer = napari.Viewer()
    viewer.open(args.video)

    n = add_labels(viewer, args.csv, p_cutoff=args.p, size=args.size)
    print(f"Added {n} bodypart layers from: {args.csv}")

    napari.run()
