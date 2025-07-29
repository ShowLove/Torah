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
    BASE_DIR / "excel_engine",
    BASE_DIR / "xml_engine",
    BASE_DIR / "docx_engine"
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
import TanachXML_engine           # xml_engine directory
import docx_engine                # docx_engine directory

def main():

    # Hard Coded Values
    # Books - Genesis, Exodus, Leviticus, Numbers, Deuteronomy
    #          בראשית  שמות    ויקרא      במדבר    דברים
    # Books Heb - 
    hc_book = "Genesis"
    hc_book_heb = "בראשית"
    hc_book_xml = "Genesis.xml"
    hc_chapter = 1
    hc_verse = 1
    hc_word_index = 3

    # Ask the user to choose between the options
    choice = utils.terminal_prompt()
    if choice == "1":
        # Gets a verse from teh metsudah site based on gui input
        metsudah_chumash_web_nav.get_and_display_metsudah_verse_m()
    elif choice == "2":
        # From - Hard Coded Values
        # Get a chapter from the Metsudah Eng translation site and save it in excel.
        metsudah_chumash_web_nav.save_torah_chapter_to_excel_m(hc_book, hc_chapter)
    elif choice == "3":
        # Open the Eng Metsudah translation site
        web_utils.main_open_website_with_chrome(utils.METSUDAH_ENG_SITE)
    elif choice == "4":
        # From - Hard Coded Values
        # Get a book from the Metsudah Eng translation site and save it in excel.
        metsudah_chumash_web_nav.save_entire_torah_book_to_excel_m(hc_book)
    elif choice == "5":
        # Get a Verse and Word in Verse from the TanachXML data base based on Leningrad Codex.
        TanachXML_engine.example_usage(utils.HEB_TORAH_BOOK_DATA_XML, hc_book_xml, hc_chapter, hc_verse, hc_word_index)
    elif choice == "6":

        heb_verse_num = utils.get_hebrew_verse_num(hc_verse, utils.H_VERSE_NUM_JSON)
        heb_verse = TanachXML_engine.get_verse(utils.HEB_TORAH_BOOK_DATA_XML, hc_book_xml, hc_chapter, hc_verse)
        heb_string = str(heb_verse_num) + "   " + str(heb_verse)
        print(f"Hebrew Verse Number is --> {heb_verse_num}")
        print(f"Hebrew Verse is --> {heb_verse}")
        print(heb_string)

        header = hc_book + " Chapter " + str(hc_chapter)
        heb_text = "תּוֹרָה - סֵפֶר " + hc_book_heb
        file_name = hc_book + "_Ch_" + str(hc_chapter) + ".docx"
        docx_engine.create_docx_with_header(header, heb_text, utils.METSUDAH_DOCX_ENG_OUTPUT, file_name)
    else:
        print("Have a nice day !")

if __name__ == "__main__":
    main()
