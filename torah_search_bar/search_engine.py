import json
import os

def load_json_files(data_folder="book_data"):
    all_data = []
    for filename in os.listdir(data_folder):
        if filename.endswith(".json"):
            with open(os.path.join(data_folder, filename)) as f:
                all_data.append(json.load(f))
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
