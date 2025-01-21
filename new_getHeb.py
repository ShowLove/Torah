import utils

from docx import Document
from docx.shared import Pt
from docx.shared import Inches
import re
import os
from docx.shared import RGBColor



if __name__ == "__main__":
    #################################
    # Eng
    #################################
    now_parasha_path = utils.load_data(utils.PARASHOT_NOW, return_path_only=True)
    parasha_details = utils.get_parasha_details_heb(now_parasha_path)

    if parasha_details:
        # Extract the first parasha's details into individual variables
        first_parasha = parasha_details[0]
        parasha_name = first_parasha["parasha_name"]
        book_name = first_parasha["book_name"]
        start_chapter = first_parasha["start_chapter"]
        start_verse = first_parasha["start_verse"]
        end_chapter = first_parasha["end_chapter"]
        end_verse = first_parasha["end_verse"]
        tanakh_section = first_parasha["tanakh_section"]

        # Print the details
        print(f"Parasha Name:\t\t\t {parasha_name}")
        print(f"Book Name:\t\t\t {book_name}")
        print(f"Start Chapter:\t\t\t {start_chapter}, Start Verse: {start_verse}")
        print(f"End Chapter:\t\t\t {end_chapter}, End Verse: {end_verse}")
        print(f"Tanakh Section:\t\t\t {tanakh_section}")
    else:
        print("No parasha details found.")

    # Step 1: get the paths
    eng_folder_path = utils.load_tanakh_path(utils.ENG_DOCX_FOLDER)
    heb_folder_path = utils.load_tanakh_path(utils.HEB_DOCX_FOLDER)
    output_folder_path = utils.load_tanakh_path(utils.OUTPUT_DOCX_FOLDER)
    hebrew_file_path = "hebrew_text.docx"
    english_file_path = "english_text.docx"
    output_file_path = "combined_output.docx"

    #################################
    # Heb
    #################################
    now_parasha_path_heb = utils.load_data(utils.PARASHOT_NOW_HEB, return_path_only=True)
    parasha_details_heb = utils.get_parasha_details_heb2(now_parasha_path_heb)

    if parasha_details_heb:
        # Extract the first parasha's details into individual variables
        first_parasha_heb = parasha_details_heb[0]
        parasha_name_heb = first_parasha_heb["parasha_name"]
        book_name_heb = first_parasha_heb["book_name"]
        start_chapter_heb = first_parasha_heb["start_chapter"]
        start_verse_heb = first_parasha_heb["start_verse"]
        end_chapter_heb = first_parasha_heb["end_chapter"]
        end_verse_heb = first_parasha_heb["end_verse"]
        tanakh_section_heb = first_parasha_heb["tanakh_section"]

        # Print the details
        print(f"\nParasha Name Heb:\t\t\t {parasha_name_heb}")
        print(f"Book Name Heb:\t\t\t\t {book_name_heb}")
        print(f"Start Chapter Heb:\t\t\t {start_chapter_heb}, Start Verse: {start_verse_heb}")
        print(f"End Chapter Heb:\t\t\t {end_chapter_heb}, End Verse: {end_verse_heb}")
        print(f"Tanakh Section Heb:\t\t\t {tanakh_section_heb}")
    else:
        print("No parasha details found.")

    # Step 2. Get folder paths
    # Eng
    eng_filename = f"{book_name}_{start_chapter}.docx"
    eng_folder_path = utils.load_tanakh_path(utils.ENG_DOCX_FOLDER)
    eng_folder_path = os.path.join(eng_folder_path, parasha_name)
    print(f"English filename:\t {eng_filename}")
    print(f"English folder name:\t {eng_folder_path}")
    # Heb
    heb_filename = f"{book_name}_{start_chapter}.docx"
    heb_folder_path = utils.load_tanakh_path(utils.ENG_DOCX_FOLDER)
    heb_folder_path = os.path.join(eng_folder_path, parasha_name)
    print(f"English filename:\t {eng_filename}")
    print(f"English folder name:\t {eng_folder_path}")

    # Step 3: Ask the user whether to add notes to verses
    add_notes = input("\nWould you like to add notes to the verses? (yes/no): ").strip().lower()

