# ================================================================
# 0. Section: IMPORTS
# ================================================================
from pybehaviour.db_support import massive_import
from pathlib import Path



# ================================================================
# 1. Section: INPUTS
# ================================================================
INPUT_PATH = Path("../data/import_db/ladder.xlsx")
INPUT_PAGE_NAME: str = "main"
DB_PATH = Path("../dataBehaviour/db/app.sqlite")


# ================================================================
# 2. Section: FUNCTIONS
# ================================================================



# ================================================================
# 3. Section: MAIN
# ================================================================
if __name__ == '__main__':
    massive_import(INPUT_PATH, DB_PATH, sheet_name=INPUT_PAGE_NAME)
