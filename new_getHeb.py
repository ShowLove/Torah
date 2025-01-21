import utils

from docx import Document
from docx.shared import Pt
from docx.shared import Inches
import re
import os
from docx.shared import RGBColor



if __name__ == "__main__":
    # Extract the parasha details
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
        print(f"Parasha Name: {parasha_name}")
        print(f"Book Name: {book_name}")
        print(f"Start Chapter: {start_chapter}, Start Verse: {start_verse}")
        print(f"End Chapter: {end_chapter}, End Verse: {end_verse}")
        print(f"Tanakh Section: {tanakh_section}")
    else:
        print("No parasha details found.")

    # Step 4: Ask the user whether to add notes to verses
    add_notes = input("\nWould you like to add notes to the verses? (yes/no): ").strip().lower()

    # Step 1: get the paths
    eng_folder_path = utils.load_tanakh_path(utils.ENG_DOCX_FOLDER)
    heb_folder_path = utils.load_tanakh_path(utils.HEB_DOCX_FOLDER)
    output_folder_path = utils.load_tanakh_path(utils.OUTPUT_DOCX_FOLDER)
    hebrew_file_path = "hebrew_text.docx"
    english_file_path = "english_text.docx"
    output_file_path = "combined_output.docx"

    filename = f"{book_name}_{start_chapter}.docx"
    folder_path = utils.load_tanakh_path(utils.ENG_DOCX_FOLDER)
    folder_path = os.path.join(folder_path, parasha_name)