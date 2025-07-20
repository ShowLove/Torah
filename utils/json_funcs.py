import json
import os

def set_parasha_json(parasha, json_path=None):
    """
    Updates the 'parasha' field in a JSON file with the given parasha name.

    :param parasha: str - The parasha name to insert
    :param json_path: Optional path to the JSON file to update
    :return: bool - True if successful, False otherwise
    """
    try:
        # Default to data/current_verse_target.json relative to this file
        if json_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            json_path = os.path.join(current_dir, '..', 'data', 'current_verse_target.json')

        # Load existing data
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Update the parasha field
        data['parasha'] = parasha

        # Save the updated data back to the file
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

        print(f"Updated parasha selection to {parasha} in {json_path}")
        return True

    except Exception as e:
        print(f"Error updating parasha in JSON: {e}")
        return False

def get_parasha(book, chapter, verse, json_path=None):
    """
    Returns the name of the parasha that contains the given book, chapter, and verse.

    :param book: str - The book name (e.g., "Genesis")
    :param chapter: int - The chapter number
    :param verse: int - The verse number
    :param json_path: Optional path to the ParashotData.json file
    :return: str or None - The name of the parasha, or None if not found
    """
    # Default to data/ParashotData.json relative to this file
    if json_path is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, '..', 'data', 'ParashotData.json')

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for parasha in data.get("ParashaNames", []):
        if parasha.get("Book") != book:
            continue

        start_ch = parasha["Start"]["Chapter"]
        start_vs = parasha["Start"]["Verse"]
        end_ch = parasha["End"]["Chapter"]
        end_vs = parasha["End"]["Verse"]

        # Normalize to a comparable range
        if (chapter > start_ch or (chapter == start_ch and verse >= start_vs)) and \
           (chapter < end_ch or (chapter == end_ch and verse <= end_vs)):
            return parasha.get("standard")

    return None