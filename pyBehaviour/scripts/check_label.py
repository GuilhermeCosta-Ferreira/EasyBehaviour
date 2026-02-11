# ================================================================
# 0. Section: IMPORTS
# ================================================================
from pathlib import Path
from pybehaviour.moseq_support import plot_labeled_frame
from matplotlib import pyplot as plt


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
    plot_labeled_frame(
        video_path=Path("../data/flip_handling/to_flip/71_MdVMdD_1A_handling_W1_1_converted.mp4"),
        h5_path=Path("../data/flip_handling/to_flip/71_MdVMdD_1A_handling_W1_1_convertedDLC_resnet50_HandlingCerealJan13shuffle1_100000.h5"),
        target_frame=100)

    plot_labeled_frame(
        video_path=Path("../data/flip_handling/flipped/71_MdVMdD_1A_handling_W1_1_flipped.mp4"),
        h5_path=Path("../data/flip_handling/flipped/71_MdVMdD_1A_handling_W1_1_flippedDLC_resnet50_HandlingCerealJan13shuffle1_100000.h5"),
        target_frame=100)

    plt.show()
