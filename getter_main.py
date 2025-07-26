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

def main():

    # Ask the user to choose between the options
    choice = utils.terminal_prompt()
    if choice == "1":
        # Longest verse: Esther 8:9, Shortest verse: 1 Chronicles 1:1
        # Longest has 77 words in eng, So I take that x3 for any translation.
        # Gets a verse from teh metsudah site based on gui input
        metsudah_chumash_web_nav.get_and_display_metsudah_verse_m()
    elif choice == "2":

        total_verses_in_ch = utils.get_torah_ch_verse_num("Genesis", 1)
        print(f"Total Verses = {total_verses_in_ch}")
        for verse in range(1, total_verses_in_ch + 1):
            print(f"Verse {verse}")

        filen_name = "fooo_test_2"
        HEADERS = ["verse", "verse string", "verse", "vw1", "vw2","..."]
        excel_engine.create_excel_m(filen_name, utils.OUT_ENG_TORAH_XLSX, HEADERS)
    else:
        print("Have a nice Day !")
        metsudah_chumash_web_nav.get_metsudah_ch("Genesis", 1)


if __name__ == "__main__":
    main()
