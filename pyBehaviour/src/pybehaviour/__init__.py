from matplotlib import pyplot as plt
from pathlib import Path

from .styling.style_initializer import init_style

# Start the Style
init_style()

BASE_DIR = Path(__file__).resolve().parents[0]
plt.style.use(BASE_DIR / Path("styling/nr_style_paper.mplstyle"))
