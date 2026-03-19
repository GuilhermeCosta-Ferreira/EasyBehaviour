# ================================================================
# 0. Section: IMPORTS
# ================================================================
from matplotlib import pyplot as plt

from pathlib import Path

from pybehaviour.reaching import(
    scrap_folder,
    low_likelihood_to_nan,
    low_pass_filter
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

    target_file = study_group.files[VIDEO_NR]

    print(target_file.video_path)
    print(target_file.timepoint)
    print(target_file.best_label)
    print(target_file.min_distance)

    wrist_point = target_file.best_label

    plt.figure()
    plt.imshow(target_file.best_frame)
    plt.scatter(wrist_point[0], wrist_point[1])
    plt.show(block=False)
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

    wrist_point = target_file.best_label
    print(wrist_point)

    plt.figure()
    plt.imshow(target_file.best_frame)
    plt.scatter(wrist_point[0], wrist_point[1])
    plt.title("Low Pass filtering")
    plt.show(block=True)


    target_file = study_group.files[VIDEO_NR]
    wrist_df = low_likelihood_to_nan(target_file, 0.90)

    plt.figure()
    plt.plot(wrist_df["x"].diff().to_numpy())
    plt.show(block=False)

    target_file.wrist_df = wrist_df

    print(target_file.best_label)
    print(target_file.min_distance)

    plt.figure()
    plt.imshow(target_file.best_frame)
    plt.scatter(wrist_point[0], wrist_point[1])
    plt.title("Likelihood filtering")
    plt.show(block=True)
