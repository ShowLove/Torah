import json
import os

def update_selection_json(book=None, chapter=None, verse=None, website_eng=None, website_heb=None, folder="data", filename="current_verse_target.json"):
    """
    Conditionally updates the current_verse_target.json file with any combination of
    book, chapter, verse, website_eng, and website_heb. Skips any value left as None.
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
    if website_eng is not None:
        data["website_eng"] = website_eng
    if website_heb is not None:
        data["website_heb"] = website_heb

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Updated selection in {file_path}")
