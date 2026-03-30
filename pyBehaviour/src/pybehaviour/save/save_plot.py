# ================================================================
# 0. Section: IMPORTS
# ================================================================
from pathlib import Path
from matplotlib.figure import Figure

from .SaveSettings import SaveSettings



# ================================================================
# 1. Section: Functions
# ================================================================
def save_plot(
    fig: Figure,
    path: Path,
    save_settings: SaveSettings = SaveSettings(),
):
    base_path = path / save_settings.name
    for form in save_settings.format:
        out_path = base_path.with_suffix(f".{form}")
        fig.savefig(out_path, bbox_inches="tight")
