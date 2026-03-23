# ================================================================
# 0. Section: IMPORTS
# ================================================================
import json

import pandas as pd
from matplotlib import pyplot as plt

from pathlib import Path

import pybehaviour as pyb # important for styling



# ================================================================
# 1. Section: INPUTS
# ================================================================
BASE_FOLDER: Path = Path(__file__).resolve().parents[3] / "data/reaching"
GROUP_FOLDER: Path = BASE_FOLDER / "study/raw"
FILE_PATH: Path = GROUP_FOLDER.parent / "file_list_label.xlsx"
JSON_PATH: Path = BASE_FOLDER / "reaching_states.json"



# ================================================================
# 3. Section: MAIN
# ================================================================
if __name__ == '__main__':
    file = pd.read_excel(FILE_PATH)

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)

    # Build id -> name mapping
    id_to_name = {item["id"]: item["name"] for item in config["states"]}

    # Get valid state ids
    states = file["state"].dropna().astype(int)

    # Percentage of each state
    percentages = states.value_counts(normalize=True).sort_index() * 100

    # Ensure all states appear, even if missing in the data
    all_ids = sorted(id_to_name.keys())
    percentages = percentages.reindex(all_ids, fill_value=0)

    # Translate ids to names
    x_labels = [id_to_name[i] for i in all_ids]

    plt.figure()
    plt.bar(x_labels, percentages.values)
    plt.ylabel("Percentage (%)")
    plt.xlabel("State")
    plt.title("State distribution")
    plt.xticks(rotation=45)
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.show()
