# ================================================================
# 0. Section: IMPORTS
# ================================================================
from dataclasses import dataclass
from operator import contains



# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class Label:
    name: str
    x: float
    y: float


    @property
    def color(self) -> str:
        if(self.name == "cereal"): return "yellow"
        elif(contains(self.name, "l") or contains(self.name, "left")): return "red"
        elif(contains(self.name, "r") or contains(self.name, "right")): return "blue"
        else: return "yellow"

    @property
    def alpha(self) -> float:
        if(contains(self.name, "mid")): return 0.25
        else: return 1



# ──────────────────────────────────────────────────────
# 1.1 Subsection: Helper Functions
# ──────────────────────────────────────────────────────
