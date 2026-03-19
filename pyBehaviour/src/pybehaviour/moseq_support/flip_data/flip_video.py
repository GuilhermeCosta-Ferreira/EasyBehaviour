# ================================================================
# 0. Section: IMPORTS
# ================================================================
import cv2
import os
import subprocess

from pathlib import Path

from .name_utils import build_flipped_name



# ================================================================
# 1. Section: Functions
# ================================================================
def flip_video(video_path: Path, output_folder: Path) -> None:
    # 1. Get an output path
    output_path = build_flipped_name(video_path, output_folder)
    os.makedirs(output_folder, exist_ok=True)

    # 2. Build: ffmpeg -i input.mp4 -vf "hflip" -c:a copy output.mp4
    """
    # Loses quality over .avi files
    cmd = ["ffmpeg", "-i", str(video_path),
        "-vf", "hflip", "-c:a",
        "copy", str(output_path)]
    """
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-vf", "hflip",
        "-c:v", "h264_videotoolbox",
        "-q:v", "65",
        "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        str(output_path)
    ]
    """
    """

    # 3. Runs the command
    proc = subprocess.run(cmd, capture_output=True, text=True)

    # 4. Catchs any errors
    if proc.returncode != 0:
        raise RuntimeError(
            "ffmpeg failed\n"
            f"command: {' '.join(cmd)}\n"
            f"stderr:\n{proc.stderr.strip()}"
        )


# ──────────────────────────────────────────────────────
# 1.1 Subsection: Video Shape
# ──────────────────────────────────────────────────────
def get_video_shape(video_path: Path) -> tuple:
    # 1. Load the video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open {video_path}")

    # 2. Extract max for x and y
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    return (width, height)
