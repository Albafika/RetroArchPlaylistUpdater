import json
import os

def load_json(file_path):
    """Load a JSON file and return its content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: File '{file_path}' is not valid JSON.")
        return None

def save_json(file_path, data):
    """Save the provided data to a JSON file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        print(f"Data successfully saved to '{file_path}'.")
    except Exception as e:
        print(f"Error saving file '{file_path}': {e}")

def modify_json_file(file_path, source_data, DESTINATION_data):
    """Modify the DESTINATION JSON data based on the source JSON data."""
    if 'items' in source_data and 'items' in DESTINATION_data:
        DESTINATION_data['items'] = source_data['items']
        if 'default_core_path' in DESTINATION_data and 'default_core_name' in DESTINATION_data:
            default_core_path = DESTINATION_data['default_core_path']
            default_core_name = DESTINATION_data['default_core_name']
            for item in DESTINATION_data['items']:
                if 'core_path' in item:
                    item['core_path'] = default_core_path
                if 'core_name' in item:
                    item['core_name'] = default_core_name

        if 'scan_content_dir' in DESTINATION_data:
            scan_content_dir = DESTINATION_data['scan_content_dir']
            for item in DESTINATION_data['items']:
                if 'path' in item:
                    current_path = item['path']
                    dir_name, file_name = os.path.split(current_path)
                    new_path = os.path.join(scan_content_dir, file_name)
                    item['path'] = new_path
            update_path_separators(DESTINATION_data)
            save_json(file_path, DESTINATION_data)
        else:
            print(f"Error: 'scan_content_dir' not found in {file_path}.")
    else:
        print(f"Error: 'items' not found in the source or DESTINATION file: {file_path}.")

def update_path_separators(DESTINATION_data):
    """Update the path separators in the items' paths to match the separator used in 'scan_content_dir'."""
    if 'scan_content_dir' in DESTINATION_data:
        scan_content_dir = DESTINATION_data['scan_content_dir']
        new_separator = '\\' if '\\' in scan_content_dir else '/'
        for item in DESTINATION_data.get('items', []):
            if 'path' in item:
                current_path = item['path']
                normalized_path = current_path.replace(os.sep, new_separator)
                item['path'] = normalized_path
        print(f"Paths updated to use '{new_separator}' as the separator.")
    else:
        print(f"Error: 'scan_content_dir' not found in DESTINATION data.")
