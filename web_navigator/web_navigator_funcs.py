import json
import os
import webbrowser

def load_eng_website_link(json_filename):
    """
    Load the 'website_eng' URL from a JSON file in the data directory.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "..", "data", json_filename)
    file_path = os.path.normpath(file_path)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Could not find {json_filename} at {file_path}")

    with open(file_path, 'r') as f:
        data = json.load(f)

    return data.get("website_eng")

def open_eng_website(url):
    """
    Open the given URL in the default web browser.
    """
    if url:
        webbrowser.open(url)
    else:
        print("No valid URL found in JSON.")

def open_website_from_json(json_filename):
    """
    Load URL from given JSON file and open it in a browser.
    """
    url = load_eng_website_link(json_filename)
    open_eng_website(url)

# Example usage:
if __name__ == "__main__":
    open_website_from_json("current_verse_target.json")
