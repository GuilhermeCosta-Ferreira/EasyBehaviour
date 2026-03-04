# ================================================================
# 0. Section: Imports
# ================================================================
import os
import re

import numpy as np



# ================================================================
# 1. Section: DLC Folder Management
# ================================================================
def extract_dlc_file_data(dlc_path: str) -> tuple:
    # 1. Check all csv files in the folder
    csv_files_names = np.array([filename for filename in os.listdir(dlc_path) if filename.endswith('.csv')])
    labeled_videos_names = np.array([filename for filename in os.listdir(dlc_path) if filename.endswith('.mp4')])

    # Regex to match YYYY-MM-DD (with optional zero padding)
    date_pattern = re.compile(r"\d{4}-\d{1,2}-\d{1,2}")

    # Get the dates from the filenames
    dates = []
    for filename in csv_files_names:
        match = date_pattern.search(filename)
        if match:
            dates.append(match.group())  # Extract the matched date
        else:
            dates.append(None)  # If no date found, keep placeholder

    dates = np.array(dates)

    # crop the csv_names to get the first digit after 2 letters after ReachingBot
    # Pattern: "ReachingBot<bot>_<mouse>_<date>" where mouse can be numbers or alphanumeric (e.g., 1A, 3B)
    mouse_pattern = re.compile(r"ReachingBot\d+_([0-9]+[A-Z]?)_\d{4}-\d{1,2}-\d{1,2}")

    mice_numbers = []
    for filename in csv_files_names:
        match = mouse_pattern.search(filename)
        if match:
            mice_numbers.append(match.group(1))
        else:
            mice_numbers.append(None)

    try: mice_numbers = np.array(mice_numbers, dtype=int)
    except ValueError:
        print("⚠️ Mice numbers contain non-integer values, storing as strings.")
        mice_numbers = np.array(mice_numbers)

    trial_identifiers = np.array([filename[:-4] for filename in csv_files_names])

    mouse_order = np.argsort(mice_numbers)
    csv_files_names = csv_files_names[mouse_order]
    #labeled_videos_names = labeled_videos_names[mouse_order]
    labeled_videos_names = [file.replace('.csv', '_labeled.mp4') for file in csv_files_names]
    mice_numbers = mice_numbers[mouse_order]
    dates = dates[mouse_order]
    trial_identifiers = trial_identifiers[mouse_order]

    return (csv_files_names, labeled_videos_names, mice_numbers, dates, trial_identifiers)



def clean_dlc_unused_data(dlc_path: str) -> None:
    # Get all files in the directory
    files_to_delete = []
    for filename in os.listdir(dlc_path):
        if filename.endswith(('.h5', '.pickle', '.avi')):
            files_to_delete.append(filename)

    # Delete the files
    for filename in files_to_delete:
        file_path = os.path.join(dlc_path, filename)
        os.remove(file_path)
        print(f"Deleted: {filename}")

    print(f"Deleted {len(files_to_delete)} files (.h5, .pickle, .avi)")
