# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pandas as pd

from pathlib import Path

from ...io import File



# ================================================================
# 1. Section: Functions
# ================================================================
class FileHandling(File):
    def __init__(self, path: Path) -> None:
        super().__init__(path)

        self.timepoint = 0
