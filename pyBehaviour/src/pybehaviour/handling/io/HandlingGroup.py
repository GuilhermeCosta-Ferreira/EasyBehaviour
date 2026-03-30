# ================================================================
# 0. Section: IMPORTS
# ================================================================
from pathlib import Path

from ...io import Group



# ================================================================
# 1. Section: Functions
# ================================================================
class HandlingGroup(Group):
    def __init__(
        self,
        folder_path: Path,
        group_name: str,
        group_number: int,
        mice_to_keep: Path,
        csv_folder_name: str = "raw"
    ) -> None:
        super().__init__(folder_path, group_name, group_number, mice_to_keep, csv_folder_name)
