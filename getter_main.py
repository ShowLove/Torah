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
    hc_chapter = 6
    hc_verse = 8
    hc_word_index = 3
    get_notes = True

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
        # Get a Chapter using eng Metsudah translation and the Hebrew.
        docx_engine.get_metsudah_ch_docx(hc_book, hc_book_heb, hc_chapter)
    elif choice == "7":
        # Get a Chapter with notes using eng Metsudah translation and the Hebrew.
        docx_engine.get_metsudah_ch_docx(hc_book, hc_book_heb, hc_chapter, True)
    elif choice == "8":
        # Get all chapters in a Book using eng Metsudah translation and the Hebrew.
        docx_engine.metsudah_book_chapters_to_word(hc_book, hc_book_heb, get_notes)
    else:
        print("Have a nice day !")

if __name__ == "__main__":
    main()
