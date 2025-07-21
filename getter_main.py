# getter_main.py
import sys
import os
import time


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
import json_funcs                 # utils
import generic_funcs              # utils
import metsudah_chumash_web_nav   # web_navigator

def display_verse(verse_str, text_str):
    """
    Displays the verse label and text if both are provided.
    Parameters:
        verse_str (str): The label or reference of the verse (e.g., "Genesis 1:1").
        text_str (str): The text/content of the verse.
    """
    if verse_str and text_str:
        print("Verse Label:", verse_str)
        print("Verse Text:", text_str)
    else:
        print("Verse not found.")

def inquireForParasha():
    book, chapter, verse = getBookChVerse.main()
    website = getSite.main()

    # Ensure chapter and verse are integers
    chapter = int(chapter)
    verse = int(verse)

    # Get the Parasha from the verse
    parasha = json_funcs.get_parasha(book, chapter, verse)
    json_funcs.set_parasha_json(parasha)
    print(f"Parasha: {parasha}")

    return parasha, book, chapter, verse, website

def metsudah_eng_verse_getter_from_gui():

    ######## 1. Get Torah Data from our GUI ##############################################
    parasha, book, chapter, verse, website = inquireForParasha()
    print(f"{parasha} {book}, ch:{chapter} v:{verse} \nFrom WebSite: {website}")

    # Check for missing inputs
    if not website or parasha is None:
        missing = []
        if not website:
            missing.append("website")
        if parasha is None:
            missing.append("Parasha")
        print(f"[ERROR] No valid {' and '.join(missing)} provided. Exiting.")
        return None, None, None

    ######## 2. Get a specific verse from the Torah on the metsudah site. ##################
    driver, verse_str, text_str = metsudah_chumash_web_nav.get_metsudah_verse(book, chapter, verse)
    if not driver:
        print("[ERROR] Could not initialize web driver or page load failed.")
        return None, None, None

    return driver, verse_str, text_str

def main():

    #driver, verse_str, text_str = metsudah_eng_verse_getter_from_gui()
    #display_verse(verse_str, text_str)
    #driver.quit()

    generic_funcs.get_torah_chapter("Genesis", 1)

if __name__ == "__main__":
    main()
