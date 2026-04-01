# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pandas as pd

from functools import cached_property
from pathlib import Path

from ...io import File
from ..distance import(
    add_distance_from_cereal,
    add_finger_distance_df
)
from .dataframe import get_dlc_dataframe
from ..preprocessing import filter_by_likelihood



# ================================================================
# 1. Section: Functions
# ================================================================
class HandlingFile(File):
    def __init__(self, path: Path, likelihood_threshold: float) -> None:
        super().__init__(path)

        self.likelihood_threshold = likelihood_threshold

        self.dataframe = get_dlc_dataframe(self.path)
        self.filtered_dataframe, self.exclusion_rate = filter_by_likelihood(self.dataframe, self.likelihood_threshold)



    # ================================================================
    # 2. Section: Data
    # ================================================================
    @cached_property
    def distance_df(self) -> pd.DataFrame:
        distance_df = pd.DataFrame()
        distance_df = add_finger_distance_df(self.dataframe, distance_df)
        distance_df = add_distance_from_cereal(self.dataframe, distance_df)

        return distance_df
