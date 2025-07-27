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
from torah_search_bar import gui_getter, getSite
import json_funcs                 # utils directory
import utils                      # utils directory
import metsudah_chumash_web_nav   # web_navigator directory
import excel_engine               # excel_engine directory

def main():

    # Ask the user to choose between the options
    choice = utils.terminal_prompt()
    if choice == "1":
        # Longest verse: Esther 8:9, Shortest verse: 1 Chronicles 1:1
        # Longest has 77 words in eng, So I take that x3 for any translation.
        # Gets a verse from teh metsudah site based on gui input
        metsudah_chumash_web_nav.get_and_display_metsudah_verse_m()
    elif choice == "2":

        book = "Genesis"
        chapter = 1

        # Call function to get driver and verse data
        verse_data, driver = metsudah_chumash_web_nav.get_metsudah_ch(book, chapter)

        if not isinstance(verse_data, dict):
            print("[ERROR] verse_data is not a dictionary. Exiting.")
            return

        for verse_ref, verse_text in verse_data.items():
            print(f"{verse_ref}: {verse_text}")

        driver.quit()


    else:
        print("Have a nice Day !")



if __name__ == "__main__":
    main()
