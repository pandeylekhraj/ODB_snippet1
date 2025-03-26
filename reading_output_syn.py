import os.path
import re
from collections import Counter

def read_settings_file(settings_file_path, detector_range=15):
    """
    Reads the threshold settings file and determines which detectors are synchronized, unsynchronized, or missing.
    If detectorId 255 is present, it uses its timestamp for comparison.
    If detectorId 255 is missing, it falls back to using the mode of trigger times.

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
    #print(lines)
    # Initialize data structures
    detector_to_times = {}  # Mapping detector IDs to their recorded trigger times
    time_list = []  # Store trigger times for mode calculation
    active_detectors = set()  # Collect active detectors from the data
    expected_detectors = set(range(1, detector_range))  # Expected detectors strictly within range
    time_255 = None  # Store the trigger time for detector 255

    for line in lines:
        regex = r"Detector\s+ID:\s*(\d+)\s+Trigger\s+Time:\s*(\d+)\s+Trigger\s+Time\s+Fraction:\s*(\d+)"
        match = re.search(regex, line)
        #print(match)
        if match:
            detector_id = int(match.group(1))
            trigger_time = int(match.group(2))
            trigger_time_fraction = int(match.group(3))
            time_combined = trigger_time + trigger_time_fraction / 1E7  # Convert fraction

            if detector_id == 255:
                time_255 = time_combined  # Capture detector 255's time

            if detector_id > detector_range:
                continue  # Ignore detectors beyond the given range

            time_list.append(time_combined)
            active_detectors.add(detector_id)

            if detector_id not in detector_to_times:
                detector_to_times[detector_id] = set()
            detector_to_times[detector_id].add(time_combined)
    #print(time_list)
    # Determine the reference time
    if time_255 is not None:
        ref_time = time_255  # Use detector 255's time
    else:
        # If detector 255 is not found, fallback to the mode of trigger times
        if time_list:
            ref_time, _ = Counter(time_list).most_common(1)[0]  # Use the mode of the trigger times
            print(f"Using mode of trigger times as reference: {ref_time}")  # Debugging mode time
        else:
            # No valid trigger times found
            return [], [], list(expected_detectors)

    # Classify detectors **only within detector_range**
    detectors_syn = sorted([d for d in active_detectors if ref_time in detector_to_times.get(d, set())])
    detectors_nosyn = sorted([d for d in active_detectors if ref_time not in detector_to_times.get(d, set())])
    missing_detectors = sorted(expected_detectors - active_detectors)
    #print(detectors_syn,missing_detectors)
    return detectors_syn, detectors_nosyn, missing_detectors

# Example usage:
#trigger_file_path = '/home/cdms/packages/dqm/python/dqm/deciders/syn_dcrc_info/24250321_151636/syn_trigger_F0225.txt'  # Path to your trigger data file
#detector_range = 54  # Change to any desired range
#result = read_settings_file(trigger_file_path, detector_range)
