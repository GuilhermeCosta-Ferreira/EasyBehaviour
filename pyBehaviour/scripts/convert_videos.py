# ================================================================
# 0. Section: IMPORTS
# ================================================================
from pathlib import Path
from tqdm import tqdm

from pybehaviour.dlc_support import ffprobe_codecs, convert_mov



# ================================================================
# 1. Section: INPUTS
# ================================================================
INPUT_REFERENCE_VIDEO_PATH: Path = Path("../data/converter_input_reference.MOV") # target video to convert to
OUTPUT_REFERENCE_VIDEO_PATH: Path = Path("../data/converter_reference_video.mp4") # target video to convert to

INPUT_FOLDER_PATH = Path("../data/videos_to_convert")
OUTPUT_FOLDER_PATH = Path("../data/converted")
OUTPUT_FORMAT = "mp4"



# ================================================================
# 2. Section: FUNCTIONS
# ================================================================
def reference_setup():
    reference_codec = ffprobe_codecs(INPUT_REFERENCE_VIDEO_PATH)

    print(reference_codec)

def convert_folder():
    if not INPUT_FOLDER_PATH.exists():
        print(f"Folder does not exist: {INPUT_FOLDER_PATH.resolve()}")
        return

    mov_files = sorted(INPUT_FOLDER_PATH.glob("*.MOV"))
    if not mov_files:
        print(f"No .MOV files found in: {INPUT_FOLDER_PATH.resolve()}")
        return

    for mov in tqdm(mov_files, desc="Converting", unit="video"):
        convert_mov(mov, OUTPUT_FOLDER_PATH, OUTPUT_FORMAT)

# ================================================================
# 3. Section: MAIN
# ================================================================
if __name__ == "__main__":
    convert_folder()
