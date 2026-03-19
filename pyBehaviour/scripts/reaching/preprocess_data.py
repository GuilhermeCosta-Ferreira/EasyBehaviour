# ================================================================
# 0. Section: IMPORTS
# ================================================================
from matplotlib import pyplot as plt

from pathlib import Path
from copy import deepcopy

from pybehaviour.reaching import(
    scrap_folder,
    likelihood_filter,
    low_pass_filter,
    plot_best_frame
)



# ================================================================
# 1. Section: INPUTS
# ================================================================
DLC_FOLDER: Path = Path("../data/dlc")
GROUP_FOLDER: Path = DLC_FOLDER / "71_reaching"
GROUP_NAME: str = "#71_MdD_MdV_regen"
VIDEO_NR: int = 400



# ================================================================
# 2. Section: MAIN
# ================================================================
if __name__ == '__main__':
    study_group = scrap_folder(GROUP_FOLDER, GROUP_NAME)

    target_file = deepcopy(study_group.files[VIDEO_NR])

    print(target_file.video_path)
    print(target_file.timepoint)
    print(target_file.best_label)
    print(target_file.min_distance)

    plot_best_frame(target_file)

    plt.figure()
    plt.plot(target_file.wrist_df["x"].diff().to_numpy())
    plt.show(block=True)

    x = target_file.wrist_df["x"]
    y = target_file.wrist_df["y"]
    target_file.wrist_df = low_pass_filter(target_file)
    x_filtered = target_file.wrist_df["x"]
    y_filtered = target_file.wrist_df["y"]

    plt.figure()
    plt.plot(x, label="original")
    plt.plot(x_filtered, label="filtered")
    plt.legend()
    plt.title("X")
    plt.show(block=False)

    plt.figure()
    plt.plot(y, label="original")
    plt.plot(y_filtered, label="filtered")
    plt.legend()
    plt.title("Y")
    plt.show(block=False)

    print(target_file.best_label)
    plot_best_frame(target_file, "Low Pass Filtered Best Frame")
    plt.show()

    target_file = deepcopy(study_group.files[VIDEO_NR])
    wrist_df = likelihood_filter(target_file, 0.90, fill_nan=False)

    plt.figure()
    plt.plot(wrist_df["x"].diff().to_numpy())
    plt.show(block=False)

    target_file.wrist_df = wrist_df

    print(target_file.best_label)
    print(target_file.min_distance)

    plot_best_frame(target_file, "Likelihood Filtered Best Frame")
    plt.show()
