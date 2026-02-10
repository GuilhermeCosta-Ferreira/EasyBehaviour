# ================================================================
# 0. Section: IMPORTS
# ================================================================
import os
import shutil

from pathlib import Path

from .flip_data import(
    flip_video,
    flip_h5,
    build_flipped_name,
    get_video_shape
)



# ================================================================
# 1. Section: Functions
# ================================================================
def flip_analysis_horizontal(
    video_path: Path,
    h5_path: Path,
    injured_hand: str, # either "l" or "r"
    output_folder: Path,
):

    # 1. Flip the data if applicable
    if(injured_hand.lower() == "r"):
        # 2. Extract frame and shape
        video_shape = get_video_shape(video_path)

        # 3. Flip video (use ffmpeg) and h5
        flip_video(video_path, output_folder)
        flip_h5(h5_path, video_shape, output_folder)
    else:
        os.makedirs(output_folder, exist_ok=True)
        out_h5_path = build_flipped_name(h5_path, output_folder)
        out_video_path = build_flipped_name(video_path, output_folder)
        shutil.copy2(h5_path, out_h5_path)
        shutil.copy2(video_path, out_video_path)
