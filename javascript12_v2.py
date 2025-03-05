import json
def find_differences(start_obj, end_obj, parent_key='', differences=None):
    if differences is None:
        differences = {}

    # Get all the unique keys from both objects
    all_keys = set(start_obj.keys()).union(set(end_obj.keys()))
    
    # Iterate through all keys
    for key in all_keys:
        # Build the current key's path
        current_key = parent_key + key
        
        # Case where the values are lists
        if isinstance(start_obj.get(key), list) or isinstance(end_obj.get(key), list):
            # Compare lists by joining them into a string for easy comparison
            if str(start_obj.get(key)) != str(end_obj.get(key)):
                differences[current_key] = end_obj.get(key)
        
        # Case where the values are dictionaries
        elif isinstance(start_obj.get(key), dict) and isinstance(end_obj.get(key), dict):
            # Recurse into the nested dictionaries with updated parent_key
            find_differences(start_obj.get(key), end_obj.get(key), current_key + '/', differences)
        
        # Case where the values are primitive types (strings, numbers, etc.)
        elif start_obj.get(key) != end_obj.get(key):
            differences[current_key] = end_obj.get(key)
    
    return differences

# Example usage
def read_json_from_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Example usage:
json1 = read_json_from_file('savedata1.text')  # Replace with the actual file path
json2 = read_json_from_file('savedata.text')  # Replace with the actual file path
last_written_value_1 = json1['System']['Transition']['Clients']['readoutfe_SDU_500']['status']['last_written']
last_written_value_2 = json2['System']['Transition']['Clients']['readoutfe_SDU_500']['status']['last_written']
print('from Json1',last_written_value_1)
print('from Json2',last_written_value_2)

print(find_differences(json1,json2))

