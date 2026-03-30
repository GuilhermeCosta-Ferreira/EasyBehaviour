# ================================================================
# 0. Section: IMPORTS
# ================================================================
import cv2
from pathlib import Path



# ================================================================
# 1. Section: Functions
# ================================================================
def get_nr_fames(video_path: Path) -> int:
    # 1. Open video file
    video_data = cv2.VideoCapture(video_path)

    nr_frames = int(video_data.get(cv2.CAP_PROP_FRAME_COUNT))
    return nr_frames
