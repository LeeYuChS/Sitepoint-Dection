import os
import shutil
import json

def remove_dir_and_create_dir(dir_name):
    """
        remove original file and create a new one
        Args:
            dir_name: original file name
        Returns: None
    """
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        print(dir_name, "Creat OK")
    else:
        shutil.rmtree(dir_name)
        os.makedirs(dir_name)
        print(dir_name, "Remove and Creat OK")

def load_json_data(
    file_path: str,
):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: Data file not found {file_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error: JSON parsing failed - {e}")
        return []