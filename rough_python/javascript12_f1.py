import json

# difference in Json1 and Json2  
# Function to find differences and report only differences from json2

# Function to find differences and report only differences from json2
def find_differences1(json1, json2, parent_key='', differences=None):
    if differences is None:
        differences = []

    all_keys = set(json1.keys()).union(set(json2.keys()))

    for key in all_keys:
        start_value = json1.get(key, None)
        end_value = json2.get(key, None)

        # If both values are lists
        if isinstance(start_value, list) or isinstance(end_value, list):
            # Compare arrays as strings
            if ','.join(map(str, start_value)) != ','.join(map(str, end_value)):
                differences.append({parent_key + key: end_value})

        # Check if key exists only in json2 or if the values are different
        elif start_value != end_value:
            # If the key is only in json2 or the values are different
            differences.append({parent_key + key: end_value})

        # If both values are objects (dict), recursively find differences
        elif isinstance(start_value, dict) or isinstance(end_value, dict):
            sub_differences = find_differences(start_value, end_value, parent_key + key + '/', differences)
            if sub_differences:  # Only add non-empty differences
                differences.append({parent_key + key: sub_differences})
    return differences


def find_differences(json1, json2, parent_key='', differences=None):
    if differences is None:
        differences = []

    # Combine the keys from both json1 and json2
    all_keys = set(json1.keys()).union(set(json2.keys()))

    for key in all_keys:
        start_value = json1.get(key, None)
        end_value = json2.get(key, None)

        # If both values are lists
        if isinstance(start_value, list) or isinstance(end_value, list):
            # Compare arrays as strings
            if ','.join(map(str, start_value)) != ','.join(map(str, end_value)):
                # Append to differences if values are different and non-empty
                if end_value:  # Don't add if empty
                    differences.append({parent_key + key: end_value})

        # Check if key exists only in json2 or if the values are different
        elif start_value != end_value:
            # If the key is only in json2 or the values are different and non-empty
            if end_value is not None and end_value != '':
                differences.append({parent_key + key: end_value})

        # If both values are objects (dict), recursively find differences
        elif isinstance(start_value, dict) or isinstance(end_value, dict):
            sub_differences = find_differences(start_value, end_value, parent_key + key + '/', differences)
            if sub_differences:  # Only add non-empty differences
                differences.append({parent_key + key: sub_differences})

    return differences


# Example usage
def read_json_from_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def filter_json(data):
    # Ensure we only modify the 'System' key if it exists
    if 'System' in data:
        # List of keys to remove from 'System'
        keys_to_remove = ['Buffers', 'Transition', 'Flush', 'Tmp']
        
        # Loop through the list and remove each key from 'System' if it exists
        for key in keys_to_remove:
            data['System'].pop(key, None)

    return data

# Example usage:
json1 = read_json_from_file('savedata1.text')  # Replace with the actual file path
json2 = read_json_from_file('savedata.text')  # Replace with the actual file pathi
print(json1['System']['Clients'])
filtered_json1 = filter_json(json1)
filtered_json2 = filter_json(json2)
last_written_value_1 = json1['System']
last_written_value_2 = json2['System']
#print('from Json1',last_written_value_1)
#print('from Json2',last_written_value_2)

print(find_differences(json1,json2))

