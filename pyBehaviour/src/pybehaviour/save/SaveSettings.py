# ================================================================
# 0. Section: IMPORTS
# ================================================================
from dataclasses import dataclass, field

from datetime import datetime



# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class SaveSettings:
    name: str = f"plot_{datetime.today()}"
    format: list[str] = field(default_factory=lambda: ["svg", "pdf"])
