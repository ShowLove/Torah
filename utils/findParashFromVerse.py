import json
import os

def load_parashot(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data["ParashaNames"]

def is_verse_in_range(book, chapter, verse, parasha):
    # Check book match first
    if parasha.get("Book") != book:
        return False

    start = parasha["Start"]
    end = parasha["End"]

    # Compare chapter/verse for start <= (chapter, verse) <= end
    start_ch, start_v = start["Chapter"], start["Verse"]
    end_ch, end_v = end["Chapter"], end["Verse"]

    # Check if (chapter, verse) >= (start_ch, start_v)
    if (chapter < start_ch) or (chapter == start_ch and verse < start_v):
        return False

    # Check if (chapter, verse) <= (end_ch, end_v)
    if (chapter > end_ch) or (chapter == end_ch and verse > end_v):
        return False

    return True

def find_parasha(book, chapter, verse, json_path='data/parasha.json'):
    parashot = load_parashot(json_path)

    for parasha in parashot:
        if is_verse_in_range(book, chapter, verse, parasha):
            return parasha["standard"]

    return None  # Not found

def main():
    # Replace with your actual book, chapter, verse
    book_input = "Genesis"
    chapter_input = 1
    verse_input = 5

    parasha = find_parasha(book_input, chapter_input, verse_input)
    if parasha:
        print(f"The verse {book_input} {chapter_input}:{verse_input} is in the parasha: {parasha}")
    else:
        print("Parasha not found for the given verse.")

if __name__ == "__main__":
    main()
