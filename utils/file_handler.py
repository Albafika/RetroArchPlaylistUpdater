import os
from utils.json_handler import load_json, modify_json_file

def process_folders(source_folder, DESTINATION_folder, selected_files):
    """Process the JSON files in both folders with the same name."""
    updated_files = []  # List to store names of updated playlists

    for file_name in selected_files:
        source_file_path = os.path.join(source_folder, file_name)
        DESTINATION_file_path = os.path.join(DESTINATION_folder, file_name)

        print(f"Processing file: {file_name}")

        source_data = load_json(source_file_path)
        DESTINATION_data = load_json(DESTINATION_file_path)

        if source_data and DESTINATION_data:
            modify_json_file(DESTINATION_file_path, source_data, DESTINATION_data)
            updated_files.append(file_name)

    return updated_files
