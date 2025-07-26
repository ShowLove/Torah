# getter_main.py
import sys
import os
from pathlib import Path


# -------------------------
# Bootstrapping Dependencies
# -------------------------
BASE_DIR = Path(__file__).resolve().parent
PARENT_DIRS = [
    BASE_DIR / "torah_search_bar",
    BASE_DIR / "utils",
    BASE_DIR / "data",
    BASE_DIR / "web_navigator",
    BASE_DIR / "excel_engine"
]

for path in PARENT_DIRS:
    sys.path.append(str(path))

# -------------------------
# Import Dependencies
# -------------------------
from torah_search_bar import getBookChVerse, getSite
import json_funcs                 # utils directory
import utils                      # utils directory
import metsudah_chumash_web_nav   # web_navigator directory
import excel_engine               # excel_engine directory


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

def get_and_display_metsudah_verse_m():
    driver, verse_str, text_str = metsudah_eng_verse_getter_from_gui()
    if not driver:
        return
    utils.display_verse(verse_str, text_str)
    driver.quit()

def main():

    # Ask the user to choose between the options
    choice = utils.terminal_prompt()
    if choice == "1":
        # Longest verse: Esther 8:9, Shortest verse: 1 Chronicles 1:1
        # Longest has 77 words in eng, So I take that x3 for any translation.
        get_and_display_metsudah_verse_m()
    elif choice == "2":
        #utils.get_torah_chapter("Genesis", 1)

        filen_name = "fooo_test_2"
        HEADERS = ["verse", "verse string", "verse", "vw1"]
        excel_engine.create_excel_m(filen_name, utils.OUT_ENG_TORAH_XLSX, HEADERS)
    else:
        print("Have a nice Day !")


if __name__ == "__main__":
    main()
