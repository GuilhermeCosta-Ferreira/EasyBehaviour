# ================================================================
# 0. Section: IMPORTS
# ================================================================
from dataclasses import dataclass
from pathlib import Path



# ================================================================
# 1. Section: Dataclass for Analyzed
# ================================================================
@dataclass
class Analysed:
    identifier: str # group-mouse code (file name contains it)
    video_path: Path
    h5_path: Path
    hand: str
