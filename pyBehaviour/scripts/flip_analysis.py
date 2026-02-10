# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

from pathlib import Path
from tqdm import tqdm

from pybehaviour.moseq_support import(
    flip_analysis_horizontal,
    Analysed
)



# ================================================================
# 1. Section: INPUTS
# ================================================================
TO_FLIP_FOLDER: Path = Path("../data/flip_handling/to_flip")
FLIPPED_FOLDER: Path = Path("../data/flip_handling/flipped")
HAND_DICT: dict = {
    '44_Vsx2ablation_211': "l",
    '44_Vsx2ablation_299': "r",
    '46_untreated_3B': "l",
    '46_untreated_4B': "r",
    '46_untreated_5B': "l",
    '65_Propriotreated_1B': "r",
    '65_Propriotreated_2A': "r",
    '65_Propriotreated_2B': "l",
    '65_Propriotreated_3B': "r",
    '65_Propriotreated_4A': "r",
    '65_Propriotreated_4B': "r",
    '65_Propriotreated_5A': "l",
    '71_MdVMdD_1A': "r",
    '71_MdVMdD_1B': "r",
    '71_MdVMdD_2A': "r",
    '71_MdVMdD_2B': "r",
    '71_MdVMdD_3A': "r",
    '71_MdVMdD_3B': "r",
    '71_MdVMdD_4A': "r",
    '71_MdVMdD_4B': "r",
    '71_MdVMdD_5A': "r",
    '71_MdVMdD_5B': "r",
}



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
    h5_files = np.array([p for p in TO_FLIP_FOLDER.iterdir() if p.is_file() and p.suffix.lower() == ".h5"])

    # Makes sure everyone is here
    if(mp4_files.shape != h5_files.shape):
        raise ValueError(f"Count mismatch: {len(mp4_files)} .mp4 vs {len(h5_files)} .h5")

    # Groups in a dataclass
    ids = []
    for mp4 in mp4_files:
        identifier = extract_id(mp4)
        ids.append(identifier)

    #print(np.unique(ids))


    analysed_data = []
    for mp4 in mp4_files:
        identifier = extract_id(mp4)
        video_tag = mp4.stem

        # Get the corresponding h5
        h5 = [p for p in h5_files if mp4.stem in p.name]
        if len(h5) == 0:
            raise FileNotFoundError(f"No .h5 contains tag: {mp4.stem}")
        if len(h5) > 1:
            raise ValueError(f"Multiple .h5 files contain tag {mp4.stem}: {[m.name for m in h5]}")

        data = Analysed(
            identifier=identifier,
            video_path=mp4,
            h5_path=h5[0],
            hand=HAND_DICT[identifier]
        )
        analysed_data.append(data)

    for dt in tqdm(analysed_data, desc="Flipping", unit="pack"):
        flip_analysis_horizontal(
            video_path=dt.video_path,
            h5_path=dt.h5_path,
            injured_hand=dt.hand,
            output_folder=FLIPPED_FOLDER
        )
