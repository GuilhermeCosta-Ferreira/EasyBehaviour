# ================================================================
# 0. Section: IMPORTS
# ================================================================
import re

from pathlib import Path



# ================================================================
# 1. Section: Gets Flipped File Path
# ================================================================
def build_flipped_name(file_path: Path, output_folder: Path) -> Path:
    name = file_path.name
    name = re.sub(r"(clean|converted)", "flipped", name, flags=re.IGNORECASE)

    output_path = output_folder / name
    return output_path
