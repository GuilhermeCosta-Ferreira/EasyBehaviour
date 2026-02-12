# ================================================================
# 0. Section: IMPORTS
# ================================================================
import numpy as np

from dataclasses import dataclass
from pathlib import Path



# ================================================================
# 1. Section: DataPoint as Syllable Histograms
# ================================================================
@dataclass
class SylableMetaData:
    group: int
    timepoint: str
    mouse: str

@dataclass
class DataPoint:
    path: Path
    counts: np.ndarray
    metadata: SylableMetaData

    @property
    def file_name(self):
        return self.path.stem

    @property
    def group(self):
        return self.metadata.group

    @property
    def timepoint(self):
        return self.metadata.timepoint

    @property
    def mouse(self):
        return self.metadata.mouse
