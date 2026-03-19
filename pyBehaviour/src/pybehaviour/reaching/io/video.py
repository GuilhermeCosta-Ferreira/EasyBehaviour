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

def get_best_frame(video_path: Path, best_idx: int):
    # 1. Open video file
    video_data = cv2.VideoCapture(video_path)

    # 2. Set position to frameidx (index starts at 0)
    video_data.set(cv2.CAP_PROP_POS_FRAMES, best_idx)

    # 3. Extract the frame and convert to RGB
    ret, frame = video_data.read()
    if ret:
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    else:
        return None
