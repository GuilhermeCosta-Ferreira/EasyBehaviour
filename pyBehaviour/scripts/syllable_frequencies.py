# ================================================================
# 0. Section: IMPORTS
# ================================================================
from operator import contains
import os
from pathlib import Path

import pandas as pd
import numpy as np

from matplotlib import pyplot as plt



# ================================================================
# 1. Section: INPUTS
# ================================================================
RESULTS_FOLDER: Path = Path("../data/syllables/results")
FAVORITE_MODELS: list[str] =  [
    "2026_02_11-13_18_50",
    "2026_02_11-13_52_58",
    "2026_02_11-14_31_04"
]



# ================================================================
# 2. Section: FUNCTIONS
# ================================================================
def test_run():
    bl_df = pd.read_csv("../data/syllables/new_test/71_MdVMdD_2A_handling_BL_2_flippedDLC_resnet50_HandlingCerealJan13shuffle1_100000.csv")
    w1_df = pd.read_csv("../data/syllables/new_test/71_MdVMdD_1B_handling_W1_1_flippedDLC_resnet50_HandlingCerealJan13shuffle1_100000.csv")
    w4_df = pd.read_csv("../data/syllables/new_test/71_MdVMdD_1B_handling_W4_8_flippedDLC_resnet50_HandlingCerealJan13shuffle1_100000.csv")
    w8_df = pd.read_csv("../data/syllables/new_test/71_MdVMdD_1B_handling_w8_3_flippedDLC_resnet50_HandlingCerealJan13shuffle1_100000.csv")

    bl = bl_df["syllable"]
    w1 = w1_df["syllable"]
    w4 = w4_df["syllable"]
    w8 = w8_df["syllable"]

    # Option A: actually drop values outside 0..20
    bl = bl[(bl >= 0) & (bl <= 20)]
    w1 = w1[(w1 >= 0) & (w1 <= 20)]
    w4 = w4[(w4 >= 0) & (w4 <= 20)]
    w8 = w8[(w8 >= 0) & (w8 <= 20)]

    common_bl = np.bincount(bl.astype(int)).argmax()
    common_w1 = np.bincount(w1.astype(int)).argmax()
    common_w4 = np.bincount(w4.astype(int)).argmax()
    common_w8 = np.bincount(w8.astype(int)).argmax()

    print(f"Most common of BL {common_bl}")
    print(f"Most common of W1 {common_w1}")
    print(f"Most common of W4 {common_w4}")
    print(f"Most common of W8 {common_w8}")

    # Use identical bins for fair comparison
    bins = range(0, 22)  # bins for integers 0..20 (edges 0..21)

    plt.figure()
    plt.title("BL vs W1 vs W4 vs W8")

    # "line histogram"
    plt.hist(bl, bins=bins, linewidth=2, label="BL")
    plt.hist(w1, bins=bins, linewidth=2, label="W1")
    plt.hist(w4, bins=bins, linewidth=2, label="W4")
    plt.hist(w8, bins=bins, linewidth=2, label="W8")

    plt.xlim(0, 20)      # Option B: just zoom the axis (keep even if you filtered)
    plt.xlabel("Syllable")
    plt.ylabel("Count")
    plt.legend()
    plt.show(block=True)

def inspect(folder: Path, limit: tuple):
    files = np.array([p for p in folder.iterdir() if p.is_file() and p.suffix.lower() == ".csv"])

    bl_files = np.array([p for p in files if contains(p.stem.lower(), "_bl_")])
    w1_files = np.array([p for p in files if contains(p.stem.lower(), "_w1_")])
    w4_files = np.array([p for p in files if contains(p.stem.lower(), "_w4_")])
    w8_files = np.array([p for p in files if contains(p.stem.lower(), "_w8_")])

    bl_hist_store = []
    w1_hist_store = []
    w4_hist_store = []
    w8_hist_store = []
    for file in files:
        file_df = pd.read_csv(file)
        syl = file_df["syllable"]
        bins = np.arange(0 - 0.5, 100 + 1.5, 1)  # one bin per integer
        counts, edges = np.histogram(syl, bins=bins, density=True)

        if(file in bl_files): bl_hist_store += [counts]
        elif(file in w1_files): w1_hist_store += [counts]
        elif(file in w4_files): w4_hist_store += [counts]
        elif(file in w8_files): w8_hist_store += [counts]


    average_bl_counts = np.mean(bl_hist_store, axis=0)
    average_w1_counts = np.mean(w1_hist_store, axis=0)
    average_w4_counts = np.mean(w4_hist_store, axis=0)
    average_w8_counts = np.mean(w8_hist_store, axis=0)
    centers = np.arange(0, 100 + 1)  # integer centers

    plt.figure()
    plt.plot(centers, average_bl_counts, marker="o", label="BL")
    plt.plot(centers, average_w1_counts, marker="o", label="W1")
    plt.plot(centers, average_w4_counts, marker="o", label="W4")
    plt.plot(centers, average_w8_counts, marker="o", label="W8")
    plt.xlim((limit[0] - 0.5, limit[1] - 0.5))
    plt.xticks(np.arange(limit[0], limit[1]))
    plt.legend()
    plt.title(f"Model: {folder.stem}")
    plt.show(block=False)



# ================================================================
# 3. Section: MAIN
# ================================================================
if __name__ == '__main__':
    models = [p for p in RESULTS_FOLDER.iterdir() if p.is_dir()]

    """
    for model in models:
        inspect(
            folder = model,
            limit = (0, 21))
    plt.show()
    """
