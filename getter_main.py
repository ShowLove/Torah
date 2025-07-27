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
import web_utils                  # web_navigator directory
import excel_engine               # excel_engine directory

def main():

    # Ask the user to choose between the options
    choice = utils.terminal_prompt()
    if choice == "1":
        # Gets a verse from teh metsudah site based on gui input
        metsudah_chumash_web_nav.get_and_display_metsudah_verse_m()
    elif choice == "2":
        book = "Genesis"
        chapter = 5
        # Get a chapter from the chumash site and save it in excel.
        metsudah_chumash_web_nav.save_torah_chapter_to_excel_m(book, chapter)
    elif choice == "3":
        eng_website_url = "http://www.mnemotrix.com/texis/vtx/chumash"
        web_utils.main_open_website_with_chrome(eng_website_url)
    else:
        print("Have a nice day !")

if __name__ == "__main__":
    main()
