import os
import re

def remove_duplicate_lines(lines):
    """
    Removes duplicate lines from the list of lines.
    
    Args:
    - lines (list): List of lines to filter.
    
    Returns:
    - unique_lines (list): List of unique lines.
    """
    seen = set()  # A set to track lines we've already seen
    unique_lines = []
    for line in lines:
        if line not in seen:
            unique_lines.append(line)
            seen.add(line)
    return unique_lines

def read_settings_file(settings_file_path, expected_detectors):
    """
    Reads the threshold settings file and determines which detector-DCRC pairs are synchronized, unsynchronized, or missing.
    
    Args:
    - settings_file_path (str): Path to the trigger settings file.
    - expected_detectors (list): List of expected detector IDs.
    
    Returns:
    - syn_detectors (list): List of synchronized detectors.
    - unsyn_detectors (list): List of unsynchronized detectors.
    - missing_detectors (list): List of missing detectors.
    """
    # Ensure the settings file exists
    if not os.path.isfile(settings_file_path):
        print("Trigger file not found!")
        return [], [], []

    # Read the file
    with open(settings_file_path) as f:
        lines = f.readlines()
    lines = remove_duplicate_lines(lines)

    # Initialize data structures
    detector_to_times = {}  # Mapping (detector_id, dcrc) to their recorded trigger times
    active_detectors_dcrc = set()  # Collect active (detector_id, dcrc) pairs from the data

    for line in lines:
        regex = r"Detector\s+ID:\s*(\d+)\s+DCRC:\s*(\d+)\s+Trigger\s+Time:\s*(\d+)\s+Trigger\s+Time\s+Fraction:\s*(\d+)"
        match = re.search(regex, line)
        if match:
            detector_id = int(match.group(1))
            dcrc = int(match.group(2))
            trigger_time = int(match.group(3))
            trigger_time_fraction = int(match.group(4))
            time_combined = trigger_time + trigger_time_fraction / 1E7  # Convert fraction

            active_detectors_dcrc.add((detector_id, dcrc))

            if (detector_id, dcrc) not in detector_to_times:
                detector_to_times[(detector_id, dcrc)] = set()
            detector_to_times[(detector_id, dcrc)].add(time_combined)

    # Initialize result lists
    syn_detectors = []
    unsyn_detectors = []
    missing_detectors = []

    # Check synchronization for each expected detector
    for detector_id in expected_detectors:
        dcrc_status = []  # Store status for both DCRC 0 and 1
        syn_found = False  # Flag to check if syn or unsyn status is found

        # Check for DCRC 0 and DCRC 1
        for dcrc in [0, 1]:
            key = (detector_id, dcrc)
            if key in active_detectors_dcrc:
                times = detector_to_times.get(key, set())
                if len(times) > 0:
                    syn_detectors.append(f"Det{detector_id} DCRC{dcrc} syn")
                    syn_found = True
                else:
                    unsyn_detectors.append(f"Det{detector_id} DCRC{dcrc} unsyn")
                    syn_found = True
            else:
                # For missing detectors, just report the Detector ID
                if detector_id not in [int(d.split(' ')[0][3:]) for d in missing_detectors]:
                    missing_detectors.append(f"Det{detector_id}")

        # If no syn/unsyn found, mark the detector as missing
        if not syn_found:
            if detector_id not in [int(d.split(' ')[0][3:]) for d in missing_detectors]:
                missing_detectors.append(f"Det{detector_id}")

    return syn_detectors, unsyn_detectors, missing_detectors

# Example usage:
settings_file_path = 'path_to_trigger_file.txt'  # Update with your actual file path
expected_detectors = [50, 51, 52]  # List of expected detectors

# Get the synchronization status
syn, unsyn, missing = read_settings_file(settings_file_path, expected_detectors)

# Print the result
print("Synchronized Detectors:")
for line in syn:
    print(line)

print("\nUnsynchronized Detectors:")
for line in unsyn:
    print(line)

print("\nMissing Detectors:")
for line in missing:
    print(line)

