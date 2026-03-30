# ================================================================
# 0. Section: IMPORTS
# ================================================================
from pathlib import Path
from tqdm import tqdm

from pybehaviour.reaching import scrap_folder



# ================================================================
# 1. Section: INPUTS
# ================================================================
ROOT: Path = Path(__file__).resolve().parents[3]
BASE_FOLDER: Path = ROOT / "data/reaching"

GROUP_FOLDER: Path = BASE_FOLDER / "study"
GROUP_NAME: str = r"Treated$^{MdD-MdV}$"
GROUP_NUMBER: int = 71

TO_KEEP_PATH: Path = ROOT / "data" / "mice_to_keep.json"

OUTPUT_FOLDER: Path = GROUP_FOLDER / "processed"



# ================================================================
# 2. Section: FUNCTIONS
# ================================================================
def detect_separator(line: str) -> str:
    return "\t" if line.count("\t") > line.count(",") else ","



# ================================================================
# 3. Section: MAIN
# ================================================================
if __name__ == '__main__':
    group = scrap_folder(GROUP_FOLDER, GROUP_NAME, GROUP_NUMBER, TO_KEEP_PATH)

    model = "DLC_resnet50_REACHING_MOUSEBOT_2Apr1shuffle1_500000"
    for file in tqdm(group.files, unit='files', desc='Fixing'):
        output_file = OUTPUT_FOLDER / file.path.name

        with open(file.path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if not lines:
            continue

        first_line = lines[0].rstrip("\n")
        sep = detect_separator(first_line)
        first_cell = first_line.split(sep)[0].strip()

        with open(output_file, "w", encoding="utf-8", newline="") as f:
            if first_cell == "scorer":
                # File already has the full header, just copy it
                f.writelines(lines)
            else:
                # File is missing the scorer row, add it
                n_cols = len(first_line.split(sep))
                new_first_line = sep.join(["scorer"] + [model] * (n_cols - 1)) + "\n"
                f.write(new_first_line)
                f.writelines(lines)
