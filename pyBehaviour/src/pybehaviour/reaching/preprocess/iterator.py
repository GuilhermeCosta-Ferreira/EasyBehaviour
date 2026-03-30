# ================================================================
# 0. Section: IMPORTS
# ================================================================
from copy import deepcopy

from ..io import ReachingFile
from .clean_filter import clean_filter
from .low_filter import low_pass_filter
from .remove_low_confidence import likelihood_filter

LIKELIHOOD_THRESHOLDS = [0.50, 0.90, 0.99]
LOW_PASS_CUTOFFS = [7.0, 5.0, 3.0]

DEFAULT_PROCESSES: list[list[tuple]] = [
    [(clean_filter, {})],
    [(low_pass_filter, {})],
    *[
        [(likelihood_filter, {"threshold": threshold, "fill_nan": False})]
        for threshold in LIKELIHOOD_THRESHOLDS
    ],
    *[
        [
            (low_pass_filter, {"cutoff": cutoff}),
            (likelihood_filter, {"threshold": threshold, "fill_nan": False}),
        ]
        for cutoff in LOW_PASS_CUTOFFS
        for threshold in LIKELIHOOD_THRESHOLDS
    ],
    *[
        [
            (likelihood_filter, {"threshold": threshold, "fill_nan": True}),
            (low_pass_filter, {"cutoff": cutoff}),
        ]
        for cutoff in LOW_PASS_CUTOFFS
        for threshold in LIKELIHOOD_THRESHOLDS
    ],
]


# ================================================================
# 1. Section: Functions
# ================================================================
def generate_all_possible_preprocess(data_file: ReachingFile, processes_list: list[list[tuple]] = DEFAULT_PROCESSES) -> list:
    # 1. Create a file storage
    file_storage = []

    # 2. Iterate over all the combination of processes
    for processes in processes_list:
        file_storage.append(apply_preprocess(data_file, processes))

    # 3. Sort them by the closest point
    file_storage.sort(key=lambda file: file.min_distance)

    # 4. Remove any repetition
    unique_files = []
    last_distance = None
    for file in file_storage:
        if last_distance is None or file.min_distance != last_distance:
            unique_files.append(file)
            last_distance = file.min_distance

    return unique_files


# ──────────────────────────────────────────────────────
# 1.1 Subsection: Helper Functions
# ──────────────────────────────────────────────────────
def apply_preprocess(data_file: ReachingFile, processes: list[tuple]) -> ReachingFile:
    # 1. Copy so we don't change the file on the go
    out_file = deepcopy(data_file)

    # 2. Apply all the processes that have been defined
    for proc, params in processes:
        out_file.wrist_df = proc(out_file, **params)

    return out_file
