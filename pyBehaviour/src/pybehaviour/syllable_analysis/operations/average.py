# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

from pathlib import Path
from ..io.dataclass import DataPoint, SylableMetaData



# ================================================================
# 1. Section: Average Syllables
# ================================================================
def get_average_syllables(syllables: np.ndarray) -> np.ndarray:
    # 1. Get all unique timepoints & groups
    tp_and_groups = sorted({(dp.timepoint, dp.group) for dp in syllables})

    # 2. Get the density for the average groups
    average_syllables = []
    for tp, g in tp_and_groups:
        path = Path("AVERAGE")
        counts = np.mean(
            a=np.vstack([dp.counts for dp in syllables if (dp.timepoint == tp and dp.group == g)]),
            axis=0)
        metadata = SylableMetaData(
            group=g,
            timepoint=tp,
            mouse="AVERAGE"
        )

        # 3. Store it
        datapoint = DataPoint(path, counts,metadata)
        average_syllables.append(datapoint)

    return np.array(average_syllables)
