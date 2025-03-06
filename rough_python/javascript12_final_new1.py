import json

# Function to recursively remove keys ending with "last_written"
def remove_last_written_keys(data):
    if isinstance(data, dict):
        return {k: remove_last_written_keys(v) for k, v in data.items() if not k.endswith("last_written")}
    elif isinstance(data, list):
        return [remove_last_written_keys(item) for item in data]
    return data

# Function to find differences between two JSON objects
def find_differences(start_obj, end_obj, parent_key='', differences=None):
    if differences is None:
        differences = []

    all_keys = set(start_obj.keys()).union(set(end_obj.keys()))

    for key in all_keys:
        start_value = start_obj.get(key, None)
        end_value = end_obj.get(key, None)

        if isinstance(start_value, list) or isinstance(end_value, list):
            if ','.join(map(str, start_value)) != ','.join(map(str, end_value)):
                differences.append({'key': parent_key + key, 'start': start_value, 'end': end_value})

        elif start_value is None or end_value is None:
            differences.append({'key': parent_key + key, 'start': start_value, 'end': end_value})

        elif isinstance(start_value, dict) or isinstance(end_value, dict):
            find_differences(start_value, end_value, parent_key + key + '/', differences)

        elif start_value != end_value:
            differences.append({'key': parent_key + key, 'start': start_value, 'end': end_value})

    return differences

# Function to read JSON from file
def read_json_from_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to filter unnecessary keys from the "System" section
def filter_json(data):
    if 'System' in data:
        keys_to_remove = ['Buffers', 'Transition', 'Flush', 'Tmp']
        for key in keys_to_remove:
            data['System'].pop(key, None)
    return data

# Example usage:
json1 = read_json_from_file('savedata1.text')
json2 = read_json_from_file('savedata.text')

json1 = filter_json(json1)
json2 = filter_json(json2)

# Remove all keys ending with "last_written"
json1_filtered = remove_last_written_keys(json1)
json2_filtered = remove_last_written_keys(json2)

# Find differences between filtered JSON data
differences = find_differences(json1_filtered, json2_filtered)

print(differences)

