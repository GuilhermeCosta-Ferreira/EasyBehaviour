# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np
import pandas as pd

from pathlib import Path

from ..dataclass import DataPoint
from .metadata import get_metadata



# ================================================================
# 1. Section: Extraction and Labeling
# ================================================================
def get_syllable_density(folder: Path) -> np.ndarray:
    # 1. Extract the files and uses the names to sort the timepoints/groups
    file_list = get_file_list(folder)

    syllables = []
    for file in file_list:
        # 2. Extract the video data from moseq
        file_df = pd.read_csv(file)
        syl = file_df["syllable"]

        # 3. Etract all the data we need
        bins = np.arange(0 - 0.5, 100 + 1.5, 1)  # one bin per integer
        counts, edges = np.histogram(syl, bins=bins, density=True)
        syllbale_metadata = get_metadata(file)

        # 4. Assigns and stores the datapoint
        data_point = DataPoint(file, counts, syllbale_metadata)
        syllables.append(data_point)

    return np.array(syllables)


# ──────────────────────────────────────────────────────
# 1.1 Subsection: Get the files
# ──────────────────────────────────────────────────────
def get_file_list(folder: Path) -> np.ndarray:
    return np.array(
        [p for p in folder.iterdir() if p.is_file() and p.suffix.lower() == ".csv"]
    )
