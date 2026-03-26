# ================================================================
# 0. Section: IMPORTS
# ================================================================
from dataclasses import dataclass, field



# ================================================================
# 1. Section: Functions
# ================================================================
@dataclass
class PlotSettings:
    ylabel: str = "Metric"
    title: str = "Title of the Plot"
    fig_size: tuple = (8, 8)
    ylim: tuple | None = None
    show_rects: bool = True
    colors: list[str] = field(default_factory=lambda: ["NR_GREY", "NR_RED"])
    width: float = 0.25
    gap: float = 0.0
    vertical_offset: float = 0.0
    show_legend: bool = True
