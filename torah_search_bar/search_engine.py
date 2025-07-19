import os
import json
from pathlib import Path

def load_json_files(data_folder=None):
    """
    Load all JSON files from the specified data folder.

    If no data_folder is provided, defaults to the 'book_data' folder
    relative to this file's location.
    
    Args:
        data_folder (str or Path): Relative or absolute path to folder containing JSON files.

    Returns:
        list: List of loaded JSON content (dicts or lists).
    """
    # Determine default path if none provided
    if data_folder is None:
        base_path = Path(__file__).resolve().parent
        data_folder = base_path / "book_data"
    else:
        data_folder = Path(data_folder).resolve()

    # Validate folder existence
    if not data_folder.exists() or not data_folder.is_dir():
        raise FileNotFoundError(f"The directory '{data_folder}' does not exist or is not a directory.")

    all_data = []
    for filename in data_folder.glob("*.json"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                all_data.append(json.load(f))
        except json.JSONDecodeError as e:
            print(f"Warning: Could not parse {filename.name}: {e}")
        except Exception as e:
            print(f"Error reading {filename.name}: {e}")

    return all_data



def search_data(query, data):
    results = []
    query = query.lower()
    for item in data:
        for key, value in item.items():
            if query in str(value).lower():
                results.append(item)
                break
    return results
