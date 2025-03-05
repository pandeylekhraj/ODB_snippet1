import json

# difference in Json1 and Json2  

def find_differences(start_obj, end_obj, parent_key='', differences=None):
    if differences is None:
        differences = []
    
    all_keys = set(start_obj.keys()).union(set(end_obj.keys()))
    
    for key in all_keys:
        start_value = start_obj.get(key, None)
        end_value = end_obj.get(key, None)
        
        # Check if either value is a list
        if isinstance(start_value, list) or isinstance(end_value, list):
            if ','.join(map(str, start_value)) != ','.join(map(str, end_value)):
                differences.append({'key': parent_key + key, 'start': start_value, 'end': end_value})
        
        # Check for undefined or null values in start_obj
        elif start_value is None:
            differences.append({'key': parent_key + key, 'start': start_value, 'end': end_value})
        
        # Check for undefined or null values in end_obj
        elif end_value is None:
            differences.append({'key': parent_key + key, 'start': start_value, 'end': end_value})
        
        # If both values are objects (i.e., dicts), recursively call the function
        elif isinstance(start_value, dict) or isinstance(end_value, dict):
            find_differences(start_value, end_value, parent_key + key + '/', differences)
        
        # If the values are different, add them to the differences list
        elif start_value != end_value:
            differences.append({'key': parent_key + key, 'start': start_value, 'end': end_value})
    
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
json2 = read_json_from_file('savedata.text')  # Replace with the actual file path
#last_written_value_1 = json1['System']['Transition']['Clients']['readoutfe_SDU_500']['status']['last_written']
#last_written_value_2 = json2['System']['Transition']['Clients']['readoutfe_SDU_500']['status']['last_written']
#print('from Json1',last_written_value_1)
#print('from Json2',last_written_value_2)
json1 = filter_json(json1)  # Replace with the actual file path
json2 = filter_json(json2)  # Replace with the actual file path
print(find_differences(json1,json2))

