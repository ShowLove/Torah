# getter_main.py
import sys
import os

######################################################################
# Dependency Folders: torah_search_bar, data, utils ##################
######################################################################
current_dir = os.path.dirname(os.path.abspath(__file__))

# torah_search_bar
sys.path.append(os.path.join(current_dir, "torah_search_bar"))

# data
sys.path.append(os.path.join(current_dir, "data"))

# utils
utils_path = os.path.join(current_dir, "utils")
sys.path.append(utils_path)

# web_navigator
web_navigator_path = os.path.join(current_dir, "web_navigator")
sys.path.append(web_navigator_path)
######################################################################

from torah_search_bar import getBookChVerse, getSite
import findParashaFromVerse  # Make sure this file exists in utils
import web_navigator_funcs   # Make sure this file exists in web_navigator

def inquireForParasha():
    book, chapter, verse = getBookChVerse.main()
    website = getSite.main()

    # Ensure chapter and verse are integers
    chapter = int(chapter)
    verse = int(verse)

    print("\n--- Final Selection ---")
    print(f"Book: {book}")
    print(f"Chapter: {chapter}")
    print(f"Verse: {verse}")
    print(f"Eng Website: {website}")

    # Get the Parasha from the verse
    parasha = findParashaFromVerse.get_parasha(book, chapter, verse)
    print(f"Parasha: {parasha}")
    return parasha

def main():
    parashaName = inquireForParasha()
    print(f"Parasha Name: {parashaName}")

    web_navigator_funcs.open_website_from_json("current_verse_target.json")

if __name__ == "__main__":
    main()
