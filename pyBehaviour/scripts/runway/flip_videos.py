"""
On the works
"""

# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

from pathlib import Path
from tqdm import tqdm

from pybehaviour.moseq_support import flip_video



# ================================================================
# 1. Section: INPUTS
# ================================================================
TO_FLIP_FOLDER: Path = Path("../data/flip/flip_ladder/to_flip")
FLIPPED_FOLDER: Path = Path("../data/flip/flip_ladder/flipped")
#ACCEPTED_VIDEO_FORMATS: list = [".mp4", ".avi"]
ACCEPTED_VIDEO_FORMATS: list = [".avi"]



# ================================================================
# 2. Section: FUNCTIONS
# ================================================================
def extract_id(name: str) -> str:
    return "_".join(Path(name).stem.split("_")[:3])


# ================================================================
# 3. Section: MAIN
# ================================================================
if __name__ == '__main__':
    # Get the files in the folder
    accepted = {ext.lower() for ext in ACCEPTED_VIDEO_FORMATS}
    video_files = [p for p in TO_FLIP_FOLDER.iterdir() if p.is_file() and p.suffix.lower() in accepted]

    analysed_data = []
    for video in tqdm(video_files, desc="Flip Videos", unit="video"):
        flip_video(video, FLIPPED_FOLDER)
