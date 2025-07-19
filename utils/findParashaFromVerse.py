import json
import os

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