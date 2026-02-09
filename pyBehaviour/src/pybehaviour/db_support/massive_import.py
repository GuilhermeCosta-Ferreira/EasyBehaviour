# ================================================================
# 0. Section: IMPORTS
# ================================================================
import sqlite3

import pandas as pd
import numpy as np

from pathlib import Path

BEHAVIOUR: str = "ladder"
GROUP_TABLE: str = "groups"
MOUSE_TABLE: str = "mice"
TIMEPOINT_TABLE: str = "timepoints"
LIMIT: int = 500



# ================================================================
# 1. Section: Massive Import
# ================================================================
def massive_import(
    input_path: Path,
    db_path: Path,
    sheet_name: str = "main"):

    # 1. Import into a dataframe and clean NaN into None (for SQLite)
    df = pd.read_excel(input_path, sheet_name=sheet_name)
    df = df.where(pd.notna(df), None)

    # 3. Checks if the other table need updating (should stop if that is the case)
    group_is_stable = process_group_table(df, db_path)
    tp_is_stable = process_timepoint_table(df, db_path)

    print(group_is_stable and tp_is_stable)


    # 6. Updates the observation table



# ──────────────────────────────────────────────────────
# 1.1 Subsection: Helper Functions
# ──────────────────────────────────────────────────────
def process_group_table(input_df: pd.DataFrame, db_path: Path) -> bool:
    # 1. Fetch the group table to get the group id's
    group_table_df = extract_table(db_path, GROUP_TABLE)

    # 2. Get the groups in both df
    new_groups = np.unique(input_df["Group"])
    old_groups = np.unique(group_table_df["group_id"])

    # 3. Get's if there are any missing values
    missing_in_old = np.setdiff1d(new_groups, old_groups)
    if(len(missing_in_old) != 0):
        print(f"These groups are missing, please update before massive import: {missing_in_old}")
        return False
    else:
        return True

def process_timepoint_table(input_df: pd.DataFrame, db_path: Path) -> bool:
    # 1. Fetch the tp table to get the tp codes
    tp_table_df = extract_table(db_path, TIMEPOINT_TABLE)
    group_table_df = extract_table(db_path, GROUP_TABLE)

    # 2. Get the pairs in the input (group, weeks after)
    unique_pairs = (input_df[["Group", "Timepoint (week)"]].drop_duplicates())

    # 3. Get the group dicts for injury/ablation
    type_dict = group_table_df[["group_id", "study_type"]]
    col = np.ravel(type_dict[["study_type"]])
    cond = np.array([("ablation" in str(x).lower()) for x in col])
    type_dict["study_type"] = np.where(cond, "ablation", "injury")

    # 4. Translte the unique pairs
    unique_pairs_groups = np.array(unique_pairs["Group"])
    translated_type = [
        np.array(type_dict[type_dict["group_id"] == pair]["study_type"])[0]
        if len(type_dict[type_dict["group_id"] == pair]) > 0 else None
        for pair in unique_pairs_groups
    ]
    unique_pairs["Group"] = translated_type

    # 5. Checks if everything is in the timepoints table
    unique_pairs = list(map(tuple, unique_pairs.to_numpy()))
    tp_table_pairs = np.array(tp_table_df[["event_type", "weeks_after_event"]])
    for entry in unique_pairs:
        if int(entry[1]) > 0 and entry not in tp_table_pairs:
            return False

    return True

def process_metrics():
    pass

def extract_table(db_path: Path, table_name: str):
    with sqlite3.connect(db_path) as conn:
        table_df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT {LIMIT};", conn)

    if len(table_df) == LIMIT: print(f"Limit of entries reached ({LIMIT})")

    return table_df
