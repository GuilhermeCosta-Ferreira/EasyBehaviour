# ================================================================
# 0. Section: IMPORTS
# ================================================================
from pathlib import Path

from pybehaviour.moseq_support import flip_analysis_horizontal



# ================================================================
# 1. Section: INPUTS
# ================================================================



# ================================================================
# 2. Section: FUNCTIONS
# ================================================================



# ================================================================
# 3. Section: MAIN
# ================================================================
if __name__ == '__main__':
    flip_analysis_horizontal(
        video_path=Path("../data/syllables/test/44_Vsx2ablation_211_w4_clean.mp4"),
        h5_path=Path("../data/syllables/test/44_Vsx2ablation_211_w4_cleanDLC_resnet50_HandlingCerealJan13shuffle1_100000.h5"),
        injured_hand="r",
        output_folder=Path("../data/syllables/flipped")
    )
