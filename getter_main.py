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

        ###########################################################################
        # Step #1 - decide what chapter from what book you want. 
        #         - using hard coded values.

        book = "Genesis"
        chapter = 1

        ###########################################################################
        # Step #2 - Get the Metsudah eng data 
        #         - using their website.

        # Call function to get driver and verse data
        verse_data, driver = metsudah_chumash_web_nav.get_metsudah_ch(book, chapter)

        if not isinstance(verse_data, dict):
            print("[ERROR] verse_data is not a dictionary. Exiting.")
            return

        ###########################################################################
        # Step #3 - Store the chapter data 
        #         - using excel.

        # Define target directory and filename
        directory = utils.OUT_ENG_TORAH_XLSX
        filename = book
        headers = ["Verse", "Verse_String", "Num_Words", "Num_Chars","W1","W2","..."]

        # Step 3.A: Create the Excel file with headers and frozen top row
        xlsx_path = excel_engine.create_excel_m(filename, directory, headers)

        # Step 3.B: Write each verse_ref and verse_text to separate columns in Excel
        if xlsx_path:
            sheet_name = f"{book} CH{chapter}"
            start_row = 1  # Starting row after headers

            for idx, (verse_ref, verse_text) in enumerate(verse_data.items(), start=start_row):
                verse_cell = f"A{idx}"  # Column A for verse_ref
                text_cell = f"B{idx}"   # Column B for verse_text

                excel_engine.write_string_to_excel(xlsx_path, sheet_name=sheet_name, cell=verse_cell, text=verse_ref)
                excel_engine.write_string_to_excel(xlsx_path, sheet_name=sheet_name, cell=text_cell, text=verse_text)

            print(f"Data written to {xlsx_path}")
        else:
            print("Failed to create Excel file.")

        driver.quit()

if __name__ == "__main__":
    main()
