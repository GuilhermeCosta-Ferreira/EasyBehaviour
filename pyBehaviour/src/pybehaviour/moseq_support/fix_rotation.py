# ================================================================
# 0. Section: IMPORTS
# ================================================================
import os
import subprocess

from pathlib import Path
from tqdm import tqdm



# ================================================================
# 1. Section: Functions
# ================================================================
def remove_rotation_in_dir(video_dir: str | Path, exts=(".mp4", ".avi", ".mov", ".mkv")):
    for name in tqdm(os.listdir(video_dir), desc="Checking for Rotation", unit="video"):
      if not name.lower().endswith(exts):
          #print("wrong file")
          continue

      in_path = os.path.join(video_dir, name)
      rot = check_rotation(in_path) % 360

      if rot == 0:
          #print("no issue")
          continue

      tmp_path = in_path + ".tmp.mp4"   # temp output
      # strip rotation metadata only (no re-encode)
      subprocess.check_call([
          "ffmpeg", "-y",
          "-i", in_path,
          "-c", "copy",
          "-metadata:s:v", "rotate=0",
          tmp_path
      ])

      os.replace(tmp_path, in_path)
      print(f"Fixed rotation tag: {name} (was {rot} deg)")


# ──────────────────────────────────────────────────────
# 1.1 Subsection: Helper Functions
# ──────────────────────────────────────────────────────
def check_rotation(path: str) -> int:
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream_tags=rotate",
        "-of", "default=nw=1:nk=1",
        path,
    ]
    out = subprocess.check_output(cmd, text=True).strip()
    return int(out) if out else 0
