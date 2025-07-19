import json
import os

def update_selection_json(book=None, chapter=None, verse=None, website=None, folder="data", filename="current_verse_target.json"):
    """
    Conditionally updates the current_verse_target.json file with any combination of
    book, chapter, verse, and website. Skips any value left as None.
    """
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, filename)

    # Load existing data if the file exists, otherwise start fresh
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
    else:
        data = {}

    if book is not None:
        data["book"] = book
    if chapter is not None:
        data["chapter"] = chapter
    if verse is not None:
        data["verse"] = verse
    if website is not None:
        data["website"] = website

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Updated selection in {file_path}")
