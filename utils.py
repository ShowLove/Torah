import os
import json
import time
import shutil
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

# Eng Constants
PARASHOT_NOW = "now_parasha.json"
TANAKH_OUTLINE_ENG = "tanakhOutlineEng.json"
DATA_FOLDER = "data"
PENTATEUCH_FILE_ENG = "Pentateuch_eng.json"
PROPHETS_FILE_ENG = "Prophets_eng.json"
SCRIPTURES_FILE_ENG = "Scriptures_eng.json"
TORAH_BOOKS = "Torah books"
PROPHETS_BOOKS = "Prophets books"
SCRIPTURES_BOOKS = "Scriptures books"
TANAKH_DOCX_FOLDER = "tanakh_docs"
ENG_DOCX_FOLDER = "eng_docs"
PARASHOT_LIST_ENG_FILE = 'torah_parashot_eng.json'
DOCX_HEBREW_FONT = "Frank Ruehl" # Use Frank Ruehl for Hebrew text on Word
FONT_SIZE = 18  # Font size in points
MARGIN_SIZE = Pt(18)  # Margin size in points
VERSE_ID_FONT_SIZE = 12  # Smaller font size for the verse ID

# Heb Constants
TANAKH_DOCX_FOLDER = "tanakh_docs"
ENG_DOCX_FOLDER = "eng_docs"
HEB_DOCX_FOLDER = "hebrew_docs"
OUTPUT_DOCX_FOLDER = "output_docs"

# Heb Constants
DOCX_HEBREW_FONT = "Frank Ruehl"  # Use Frank Ruehl for Hebrew text on Word
DOCX_ENGLISH_FONT = "Times New Roman"  # Use Times New Roman for English text
FONT_SIZE_HEB = 16  # Font size in points
FONT_SIZE_ENG = 12  # Font size in points
MARGIN_SIZE = Pt(12)  # Margin size in points

# Heb Constants
PARASHOT_NOW_HEB = "now_parasha_heb.json"



def get_parasha_details_heb(file_path):
    """
    Extracts Parasha details from a JSON file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        list: A list of dictionaries with Parasha details.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        parasha_details = []
        for parasha in data.get("Parashot", []):
            details = {
                "parasha_name": parasha.get("Parasha"),
                "book_name": parasha.get("Book"),
                "start_chapter": parasha.get("Start", {}).get("Chapter"),
                "start_verse": parasha.get("Start", {}).get("Verse"),
                "end_chapter": parasha.get("End", {}).get("Chapter"),
                "end_verse": parasha.get("End", {}).get("Verse"),
                "tanakh_section": parasha.get("Tanakh Section"),
            }
            parasha_details.append(details)

        return parasha_details

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def get_parasha_details_heb2(file_path):
    """
    Extracts Parasha details and num_parasha from a JSON file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        list: A list of dictionaries with Parasha details and num_parasha.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        parasha_details = []

        # Safely extract num_parasha
        num_parasha = None
        if "Num_Parasha" in data and isinstance(data["Num_Parasha"], list):
            num_parasha = data["Num_Parasha"][0].get("num_parasha")  # Use .get()

        # Extract Parashot details
        for parasha in data.get("Parashot", []):
            details = {
                "parasha_name": parasha.get("Name"),
                "book_name": parasha.get("Book"),
                "start_chapter": parasha.get("Start", {}).get("Chapter"),
                "start_verse": parasha.get("Start", {}).get("Verse"),
                "end_chapter": parasha.get("End", {}).get("Chapter"),
                "end_verse": parasha.get("End", {}).get("Verse"),
                "tanakh_section": parasha.get("Tanakh Section"),
                "num_parasha": num_parasha,  # Add num_parasha to each parasha details
            }
            parasha_details.append(details)

        return parasha_details

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

############################################################################# ENG

# Utility Functions
def load_data(json_filename, return_path_only=False):
    """
    Load JSON data from a file in the specified data folder.

    :param json_filename: Name of the JSON file.
    :param return_path_only: If True, only return the file path.
    :return: Parsed JSON data or file path.
    """
    file_path = os.path.join(DATA_FOLDER, json_filename)
    if return_path_only:
        return file_path

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    print(f"Error: The file {json_filename} does not exist in the '{DATA_FOLDER}' folder.")
    return None

def load_tanakh_path(folder_name):
    """
    Construct the path for a folder inside the TANAKH_DOCX_FOLDER.

    :param folder_name: Folder name inside TANAKH_DOCX_FOLDER.
    :return: Full path to the folder.
    """
    return os.path.join(TANAKH_DOCX_FOLDER, folder_name)

def print_parashah_info(file_name):
    """
    Load and print Parashot details from a JSON file.

    :param file_name: Path to the JSON file containing Torah Parashot data.
    """
    try:
        with open(file_name, 'r') as file:
            data = json.load(file)

        for parashah in data.get('Parashot', []):
            print(f"Parashah: {parashah.get('Name', 'N/A')}")
            print(f"Book: {parashah.get('Book', 'N/A')}")
            print(f"Tanakh Section: {parashah.get('Tanakh Section', 'N/A')}")
            start = parashah.get('Start', {})
            end = parashah.get('End', {})
            print(f"Start: Chapter {start.get('Chapter', 'N/A')}, Verse {start.get('Verse', 'N/A')}")
            print(f"End: Chapter {end.get('Chapter', 'N/A')}, Verse {end.get('Verse', 'N/A')}")
            print("-" * 40)
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: There was an issue decoding the JSON data in the file '{file_name}'.")
    except KeyError as e:
        print(f"Error: Missing expected key {e} in the JSON data.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Selenium Utilities
def init_webdriver():
    """
    Initialize and configure a Selenium WebDriver instance.

    :return: Configured WebDriver instance.
    """
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    return webdriver.Chrome(service=service, options=options)

def get_tanakh_scraper_inputs(get_end_chapter=False):
    """
    Handles user input for Tanakh scraping: book selection, chapter, and verse range.
    
    Parameters:
        get_end_chapter (bool): Flag to enable input for end chapter choice.

    Returns:
        tuple: (tanakh_division_name, book_name, chapter_choice, start_verse_choice, end_verse_choice, [end_chapter_choice if enabled])
               or None if any input is invalid.
    """
    DEBUG = True  # Toggle for debug print statements

    # Step 1: Choose the desired Book
    tanakh_division_name, book_choice_num, book_name = getTanakhBook()

    # Exit if invalid input
    if not tanakh_division_name or not book_choice_num or not book_name:
        print(f"Invalid book choice. line: {inspect.currentframe().f_lineno}: Exiting...")
        return None

    # Step 2: Choose the chapter and verse range
    chapter_choice, start_verse_choice, end_verse_choice = get_chapter_and_verse_from_user(tanakh_division_name, book_name)
    if not chapter_choice or not start_verse_choice or not end_verse_choice:
        print(f"Invalid chapter or verse range. line: {inspect.currentframe().f_lineno}: Exiting...")
        return None

    # Step 3 (Optional): Get end chapter choice if flag is enabled
    end_chapter_choice = chapter_choice  # Default to the same chapter if not provided
    if get_end_chapter:
        try:
            end_chapter_choice = int(input("Enter the end chapter number: "))
            if int(end_chapter_choice) < int(chapter_choice):
                print("End chapter: {end_chapter_choice} cannot be less than the start chapter: {chapter_choice}. Exiting...")
                return None
        except ValueError:
            print(f"Invalid input for end chapter. line: {inspect.currentframe().f_lineno}: Exiting...")
            return None

    # Print details for debugging
    if DEBUG:
        print(f"TANAKH: {tanakh_division_name}, {book_name}, {chapter_choice}:{start_verse_choice}-{end_verse_choice}")
        if get_end_chapter:
            print(f"End Chapter: {end_chapter_choice}")

    # Return tuple including end_chapter_choice if enabled
    if get_end_chapter:
        return tanakh_division_name, book_name, chapter_choice, start_verse_choice, end_verse_choice, end_chapter_choice
    return tanakh_division_name, book_name, chapter_choice, start_verse_choice, end_verse_choice

def getTanakhBook():
    # used in get_tanakh_scraper_inputs

    DEBUG = True  # Toggle for debug print statements

    data = load_data(TANAKH_OUTLINE_ENG)
    tanakh_division_name, book_choice_num, book_name = prompt_user_for_book(data)

    if not tanakh_division_name or not book_choice_num or not book_name:
        print(f"Exit: Invalid choice made. line: {inspect.currentframe().f_lineno}: Exiting...")
        return None, None, None

    if DEBUG:
        print(f"Tanakh Division: {tanakh_division_name}")
        print(f"Book Choice: {book_choice_num}")
        print(f"Book Name: {book_name}")

    return tanakh_division_name, book_choice_num, book_name


def get_chapter_and_verse_from_user(tanakh_division_name, book_name):

    # Used in get_tanakh_scraper_inputs

    # Prompt for chapter and verse input
    chapter_choice = input("Enter the chapter number: ")
    start_verse_choice = input("Enter the start verse number: ")
    end_verse_choice = input("Enter the end verse number: ")
    start_verse_choice = int(start_verse_choice) if start_verse_choice else None
    end_verse_choice = int(end_verse_choice) if end_verse_choice else None

    # Validate chapter and verse using the is_valid_chapter function
    is_valid = is_valid_chapter(tanakh_division_name, book_name, chapter_choice, end_verse_choice)

    if is_valid:
        print(f"Chapter {chapter_choice} and Verse {end_verse_choice if end_verse_choice else ''} are valid!")
        return chapter_choice, start_verse_choice, end_verse_choice  # Return the valid chapter and verse values
    else:
        print(f"Invalid chapter or verse choice. line: {inspect.currentframe().f_lineno}: Exiting...")
        return None, None, None  # Return None if invalid


def prompt_user_for_book(data):

    # Used in getTanakhBook

    print("Please choose a section:")
    for key, value in data['sections'].items():
        print(f"{key}. {value}")
    
    tanakh_divisions = input("Enter the number corresponding to your choice: ")

    if tanakh_divisions == "1":
        tanakh_division_name = "Torah books"
    elif tanakh_divisions == "2":
        print(f"\n{tanakh_divisions}: Not yet coded - TODO")
        tanakh_division_name = "Prophets books"
        return None, None, None
    elif tanakh_divisions == "3":
        print(f"\n{tanakh_divisions}: Not yet coded - TODO")
        tanakh_division_name = "Scriptures books"
        return None, None, None
    else:
        print(f"Invalid choice. line: {inspect.currentframe().f_lineno}: Exiting...")
        return None, None, None
    
    print(f"\nYou selected: {data['sections'][tanakh_divisions]}")
    print("\nPlease choose a book:")

    books = data[tanakh_division_name]
    for key, value in books.items():
        print(f"{key}. {value}")

    book_choice = input("Enter the number corresponding to your choice: ")

    if book_choice in books:
        book_name = books[book_choice]
        print(f"\nYou selected: {book_name}")
        return tanakh_division_name, book_choice, book_name
    else:
        print(f"Invalid choice. line: {inspect.currentframe().f_lineno}: Exiting...")
        return None, None, None

def is_valid_chapter(tanakh_division_name, book_choice, chapter_choice, verse_choice=None):

    # Used in get_chapter_and_verse_from_user

    if tanakh_division_name == TORAH_BOOKS:
        file_name = PENTATEUCH_FILE_ENG
    elif tanakh_division_name == PROPHETS_BOOKS:
        file_name = PROPHETS_FILE
    elif tanakh_division_name == SCRIPTURES_BOOKS:
        file_name = SCRIPTURES_FILE
    else:
        print(f"Invalid Tanakh division. line: {inspect.currentframe().f_lineno}: Exiting...")
        return False

    data = load_data(file_name)
    if data is None:
        return False

    if book_choice in data['books']:
        book_data = data['books'][book_choice]
    else:
        print(f"Invalid book choice: {book_choice}, read file: {file_name}. line: {inspect.currentframe().f_lineno}: Exiting...")
        return False

    if chapter_choice in book_data['chapters']:
        total_verses = book_data['chapters'][chapter_choice]
        
        if verse_choice is not None:
            if 1 <= verse_choice <= total_verses:
                return True
            else:
                print(f"Invalid verse choice. Chapter {chapter_choice} has {total_verses} verses.")
                return False
        else:
            return True
    else:
        print(f"Invalid chapter choice. line: {inspect.currentframe().f_lineno}: Exiting...")
        return False

def get_parasha_details(file_path):
    """
    Extracts Parasha details from a JSON file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        list: A list of dictionaries with Parasha details (Parasha, Book, Start, End, Start Chapter).
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        parasha_details = []
        for parasha in data.get("Parashot", []):
            details = {
                "Parasha": parasha.get("Parasha"),
                "Book": parasha.get("Book"),
                "Start": parasha.get("Start"),
                "End": parasha.get("End"),
                "Start_Chapter": parasha.get("Start", {}).get("Chapter"),  # Extracts the Start Chapter (e.g., 13)
            }
            parasha_details.append(details)

        return parasha_details

    except Exception as e:
        print(f"An error occurred: {e}")
        return []
# Additional utility functions can be added as needed for specific tasks.
