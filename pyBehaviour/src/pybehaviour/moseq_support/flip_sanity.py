# ================================================================
# 0. Section: IMPORTS
# ================================================================
import cv2

import numpy as np
import pandas as pd

from pathlib import Path
from typing import cast
from matplotlib import pyplot as plt

from .Label import Label
from .flip_data import get_video_shape



# ================================================================
# 1. Section: Functions
# ================================================================
def plot_labeled_frame(video_path: Path, h5_path: Path, target_frame: int):
    video_shape = get_video_shape(video_path)
    print(video_shape)
    frame = extract_frame(video_path, target_frame)
    print(frame.shape)
    labels = get_frame_labels(h5_path, target_frame, video_shape)

    plt.figure(figsize=(10,10))
    plt.imshow(frame)
    for lb in labels:
        plt.scatter(lb.x, lb.y, s=20, label=lb.name, color=lb.color, alpha=lb.alpha)
    plt.legend()
    plt.show(block=False)


def extract_frame(video_path: Path, target_frame: int) -> np.ndarray:
    # 1. Load the video or die trying
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open {video_path}")

    # 2. Get the indexed frame or die trying
    cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
    ret, frame = cap.read()
    if not ret:
        raise RuntimeError("Could not read the frame")
    cap.release()

    return frame

def get_frame_labels(h5_path: Path, target_frame: int, video_shape) -> np.ndarray:
    h5_df = cast(pd.DataFrame, pd.read_hdf(h5_path, key="df_with_missing"))
    frame_df = h5_df.loc[target_frame]

    df = frame_df.unstack(level="coords")          # columns: x, y, likelihood
    df = df.reset_index(level="scorer", drop=True)  # index: bodyparts

    labels = [
            Label(name=part, x=float(r["x"]), y=float(r["y"]))
            for part, r in df.iterrows()
            if "x" in df.columns and "y" in df.columns
        ]

    return np.array(labels, dtype=object)

# ──────────────────────────────────────────────────────
# 1.1 Subsection: Helper Functions
# ──────────────────────────────────────────────────────
