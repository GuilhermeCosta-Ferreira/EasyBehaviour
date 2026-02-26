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
TO_FLIP_FOLDER: Path = Path("../data/flip_runway/to_flip")
FLIPPED_FOLDER: Path = Path("../data/flip_runway/flipped")



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
    mp4_files = np.array([p for p in TO_FLIP_FOLDER.iterdir() if p.is_file() and p.suffix.lower() == ".mp4"])

    analysed_data = []
    for mp4 in tqdm(mp4_files, desc="Flip Videos", unit="video"):
        flip_video(mp4, FLIPPED_FOLDER)
