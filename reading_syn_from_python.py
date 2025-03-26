import os.path
import re
from collections import Counter

def read_settings_file(settings_file_path, detector_range=15):
    """
    Reads the threshold settings file and determines which detectors are synchronized, unsynchronized, or missing.

    Args:
    - settings_file_path (str): Path to the trigger settings file.
    - detector_range (int): Defines the range of expected detectors (default: 15).

    Returns:
    - detectors_syn (list): Synchronized detectors within the given range.
    - detectors_nosyn (list): Unsynchronized detectors within the given range.
    - missing_detectors (list): Detectors missing within the given range.
    """

    # Ensure the settings file exists
    if not os.path.isfile(settings_file_path):
        print("syn trigger file not found!")
        return [], [], []

    # Read the file
    with open(settings_file_path) as f:
        lines = f.readlines()

    # Initialize data structures
    detector_to_times = {}  # Mapping detector IDs to their recorded trigger times
    time_list = []  # Store trigger times for mode calculation
    active_detectors = set()  # Collect active detectors from the data
    expected_detectors = set(range(1, detector_range))  # Expected detectors strictly within range

    for line in lines:
        match = re.search(r"Detector ID: (\d+), Trigger Time: (\d+), Trigger Time Fraction: (\d+)", line)
        if match:
            detector_id = int(match.group(1))

            # Ignore detectors beyond detector_range
            if detector_id > detector_range:
                continue

            trigger_time = int(match.group(2))
            trigger_time_fraction = int(match.group(3))
            time_combined = trigger_time + trigger_time_fraction / 1E7  # Convert fraction

            time_list.append(time_combined)
            active_detectors.add(detector_id)

            if detector_id not in detector_to_times:
                detector_to_times[detector_id] = set()
            detector_to_times[detector_id].add(time_combined)

    # Find the mode (most repeated) trigger time
    if not time_list:
        #print("No valid trigger times found in the file.")
        return [], [], list(expected_detectors)

    most_common_time, most_common_count = Counter(time_list).most_common(1)[0]
    #print(f"Most repeated Trigger Time (Mode): {most_common_time} occurred {most_common_count} times.\n")

    # Classify detectors **only within detector_range**
    detectors_syn = sorted([d for d in active_detectors if most_common_time in detector_to_times.get(d, set())])
    detectors_nosyn = sorted([d for d in active_detectors if most_common_time not in detector_to_times.get(d, set())])
    missing_detectors = sorted(expected_detectors - active_detectors)

    #print(f"SYN (synchronized) Detectors: {detectors_syn}")
    #print(f"UNSYN (unsynchronized) Detectors: {detectors_nosyn}")
    #print(f"MISSING Detectors: {missing_detectors}")

    return detectors_syn, detectors_nosyn, missing_detectors

# Example usage:
trigger_file_path = 'syn_dcrc_info.txt'  # Path to your trigger data file
detector_range = 30# Change to any desired range
#result = read_settings_file(trigger_file_path, detector_range)
