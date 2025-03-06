import json

# Function to find and remove duplicate "last_written" values while keeping one
def remove_duplicate_last_written(data):
    seen_values = set()  # Stores unique "last_written" values
    to_remove = []  # Stores paths of duplicate occurrences

    # Recursively traverse the JSON and track "last_written" values
    def recurse(d, path=""):
        if isinstance(d, dict):
            new_dict = {}
            for k, v in d.items():
                new_path = f"{path}/{k}" if path else k
                if isinstance(v, dict) and "last_written" in v:
                    last_written_val = v["last_written"]
                    if last_written_val in seen_values:
                        to_remove.append(new_path)  # Mark duplicate for removal
                    else:
                        seen_values.add(last_written_val)
                        new_dict[k] = v  # Keep first occurrence
                else:
                    new_dict[k] = recurse(v, new_path)
            return new_dict
        elif isinstance(d, list):
            return [recurse(item, f"{path}[{idx}]") for idx, item in enumerate(d)]
        return d

    # First pass to collect duplicates
    filtered_data = recurse(data)

    return filtered_data

# Function to read JSON from file
def read_json_from_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Example usage:
json_data = read_json_from_file('savedata.json')

# Remove duplicate "last_written" values while keeping one instance
json_optimized = remove_duplicate_last_written(json_data)

# Save optimized JSON back to a file
with open('optimized_json.json', 'w') as f:
    json.dump(json_optimized, f, indent=2)

print("Duplicates removed! JSON size reduced while keeping one instance of each last_written value.")

