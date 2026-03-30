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



# ================================================================
# 1. Section: Functions
# ================================================================
class HandlingFile(File):
    def __init__(self, path: Path) -> None:
        super().__init__(path)

        self.dataframe = get_dlc_dataframe(self.path)

    @cached_property
    def distance_df(self) -> pd.DataFrame:
        distance_df = pd.DataFrame()
        distance_df = add_finger_distance_df(self.dataframe, distance_df)
        distance_df = add_distance_from_cereal(self.dataframe, distance_df)

        return distance_df
