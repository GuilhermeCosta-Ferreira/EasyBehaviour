# ================================================================
# 0. Section: IMPORTS
# ================================================================
from pathlib import Path
from matplotlib import pyplot as plt

from pybehaviour.handling.ratio_analysis import (
    build_average_df,
    plot_multiple_parameters,
    plot_single_parameter,
)



# ================================================================
# 1. Section: INPUTS
# ================================================================
INPUT_FOLDER: Path = Path("../data/dlc")
CONDITIONS: list = ["71_handling", "71_handling"]
THRESHOLD: float = 0.5

SELECTED_PARAMS = [
    "ratio_avg_dist_fingers_tip",
    "ratio_range_dist_tip",
    "ratio_var_dist_tip",
    "ratio_avg_dist_cereal_tip",
    "ratio_min_dist_cereal_tip",
]
LABELS = [
    "Distance between\nfingers",
    "Fingers range\nof motion",
    "Finger position\nvariance",
    "Average distance\nfrom cereal",
    "Closest finger\ndistance from cereal",
]



# ================================================================
# 2. Section: MAIN
# ================================================================
if __name__ == "__main__":
    summary_df = build_average_df(INPUT_FOLDER, CONDITIONS, threshold=THRESHOLD)

    plot_multiple_parameters(summary_df, CONDITIONS, SELECTED_PARAMS, LABELS, "No animal Excluded")

    parameter = "ratio_avg_dist_fingers_tip"
    title = "Distance between fingers"
    ylabel = "Ratio Injured/Uninjured"
    figure_name = "distance_fingers_prova.pdf"
    direction_ttest = "greater"

    plot_single_parameter(summary_df, CONDITIONS, parameter, title, ylabel, figure_name, direction_ttest)

    parameter = "ratio_min_dist_cereal_tip"
    title = "Distance from cereal"
    ylabel = "Ratio Injured/Uninjured"
    figure_name = "distance_cereal_.pdf"
    direction_ttest = "less"

    plot_single_parameter(summary_df, CONDITIONS, parameter, title, ylabel, figure_name, direction_ttest)

    plt.show()
