# ================================================================
# 0. Section: IMPORTS
# ================================================================
import shutil

from pathlib import Path
from tqdm import tqdm

from pybehaviour.moseq_support import(
    ffmpeg_needs_fix,
    remove_rotation_in_dir,
    ffmpeg_fix_stich_crop_mp4)



# ================================================================
# 1. Section: INPUTS
# ================================================================
INPUT_FOLDER_PATH = Path("../data/converted")
OUTPUT_FOLDER_PATH = Path("../data/fixed")



# ================================================================
# 3. Section: MAIN
# ================================================================
if __name__ == "__main__":
    mov_files = sorted(list(INPUT_FOLDER_PATH.glob("*.MOV")) + list(INPUT_FOLDER_PATH.glob("*.mp4")))

    if(len(mov_files) <= 0): print("Folder is empty")

    remove_rotation_in_dir(INPUT_FOLDER_PATH)

    for mov in tqdm(mov_files, desc="Converting", unit="video"):
        needs_fix = ffmpeg_needs_fix(mov)
        if needs_fix: ffmpeg_fix_stich_crop_mp4(mov, OUTPUT_FOLDER_PATH)
        else:
            out_path = OUTPUT_FOLDER_PATH / f"{mov.stem}.mp4"  # or mov.name if you want same extension
            shutil.copy2(mov, out_path)
