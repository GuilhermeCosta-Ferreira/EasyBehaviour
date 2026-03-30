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
    plot_best_frame,
    plot_filter_displacement
)



# ================================================================
# 1. Section: INPUTS
# ================================================================
BASE_FOLDER: Path = Path(__file__).resolve().parents[3] / "data/reaching"
GROUP_FOLDER: Path = BASE_FOLDER / "study"
GROUP_NAME: str = "#71_MdD_MdV_regen"
VIDEO_NR: int = 400



# ================================================================
# 2. Section: MAIN
# ================================================================
if __name__ == '__main__':
    study_group = scrap_folder(GROUP_FOLDER, GROUP_NAME)

    target_file = deepcopy(study_group.files[VIDEO_NR])

    print("Raw Signal")
    print(target_file.video_path)
    print(target_file.timepoint)
    print(target_file.best_label)
    print(target_file.min_distance)

    plot_best_frame(target_file)

    plt.figure()
    plt.plot(target_file.wrist_df["x"].diff().to_numpy())
    plt.show(block=True)


    # ──────────────────────────────────────────────────────
    # 2.1 Subsection: Low Pass Filter
    # ──────────────────────────────────────────────────────
    target_file.wrist_df = low_pass_filter(target_file)

    plot_filter_displacement(study_group.files[VIDEO_NR], target_file)
    plot_filter_displacement(study_group.files[VIDEO_NR], target_file, derivate=True)
    plot_best_frame(target_file, "Low Pass Filtered Best Frame")

    print("\nLow Pass Filter")
    print(target_file.best_label)
    print(target_file.min_distance)
    plt.show()


    # ──────────────────────────────────────────────────────
    # 2.2 Subsection: Likelihood Filter
    # ──────────────────────────────────────────────────────
    target_file = deepcopy(study_group.files[VIDEO_NR])
    target_file.wrist_df = likelihood_filter(target_file, 0.90, fill_nan=True)

    plot_filter_displacement(study_group.files[VIDEO_NR], target_file)
    plot_filter_displacement(study_group.files[VIDEO_NR], target_file, derivate=True)
    plot_best_frame(target_file, "Likelihood Filtered Best Frame")

    print("\nLikelihood Filter")
    print(target_file.best_label)
    print(target_file.min_distance)
    plt.show()


    # ──────────────────────────────────────────────────────
    # 2.3 Subsection: LP + LH (Fill)
    # ──────────────────────────────────────────────────────
    target_file = deepcopy(study_group.files[VIDEO_NR])
    target_file.wrist_df = low_pass_filter(target_file)
    target_file.wrist_df = likelihood_filter(target_file, 0.90, fill_nan=True)

    plot_filter_displacement(study_group.files[VIDEO_NR], target_file)
    plot_filter_displacement(study_group.files[VIDEO_NR], target_file, derivate=True)
    plot_best_frame(target_file, "LP + LH (Fill) Best Frame")

    print("\nLP + LH (Fill) Filter")
    print(target_file.best_label)
    print(target_file.min_distance)
    plt.show()


    # ──────────────────────────────────────────────────────
    # 2.4 Subsection: LP + LH (No Fill)
    # ──────────────────────────────────────────────────────
    target_file = deepcopy(study_group.files[VIDEO_NR])
    target_file.wrist_df = low_pass_filter(target_file)
    target_file.wrist_df = likelihood_filter(target_file, 0.90, fill_nan=False)

    plot_filter_displacement(study_group.files[VIDEO_NR], target_file)
    plot_filter_displacement(study_group.files[VIDEO_NR], target_file, derivate=True)
    plot_best_frame(target_file, "LP + LH (No Fill) Best Frame")

    print("\nLP + LH (No Fill) Filter")
    print(target_file.best_label)
    print(target_file.min_distance)
    plt.show()


    # ──────────────────────────────────────────────────────
    # 2.5 Subsection: LH (Fill) + LP
    # ──────────────────────────────────────────────────────
    target_file = deepcopy(study_group.files[VIDEO_NR])
    target_file.wrist_df = likelihood_filter(target_file, 0.90, fill_nan=True)
    target_file.wrist_df = low_pass_filter(target_file)

    plot_filter_displacement(study_group.files[VIDEO_NR], target_file)
    plot_filter_displacement(study_group.files[VIDEO_NR], target_file, derivate=True)
    plot_best_frame(target_file, "LH (Fill) + LP Best Frame")

    print("\nLH (Fill) + LP Filter")
    print(target_file.best_label)
    print(target_file.min_distance)
    plt.show()
