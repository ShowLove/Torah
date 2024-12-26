import json
                                                                    ################################################################################################
from selenium import webdriver                                      # For automating and controlling the web browser
from selenium.webdriver.common.by import By                         # For locating elements on the web page
from selenium.webdriver.chrome.service import Service               # For initializing and configuring the ChromeDriver
from webdriver_manager.chrome import ChromeDriverManager            # Manages downloading and setting up ChromeDriver
from selenium.webdriver.support.ui import Select                    # For interacting with drop-down menus (select elements)
import time                                                         # For pausing the execution of the program (e.g., sleep or wait)
import subprocess                                                   # For running system commands and interacting with the system shell
from bs4 import BeautifulSoup                                       # For parsing and navigating HTML or XML content
from selenium.webdriver.support.ui import WebDriverWait             # For waiting for elements to appear on the page
from selenium.webdriver.support import expected_conditions as EC    # For defining the expected conditions for elements
from docx import Document                                           # For creating and modifying Word documents
import os                                                           # For file and directory operations (e.g., working with paths, creating folders)
import shutil                                                       # For file operations (e.g., moving, copying, and deleting files)
                                                                    ################################################################################################

# Load data from the external JSON file
def load_data():
    with open('tanakhOutlineHeb.json', 'r', encoding='utf-8') as file:
        return json.load(file)

def prompt_user_for_book(data):
    print("Please choose a section:")
    for key, value in data['sections'].items():
        print(f"{key}. {value}")
    
    tanakh_divisions = input("Enter the number corresponding to your choice: ")

    if tanakh_divisions == "1":
        tanakh_division_name = "Torah books"
    elif tanakh_divisions == "2":
        tanakh_division_name = "Prophets books"
    elif tanakh_divisions == "3":
        tanakh_division_name = "Scriptures books"
    else:
        print("Invalid choice. Exiting...")
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
        print("Invalid choice. Exiting...")
        return None, None, None

def is_valid_chapter(tanakh_division_name, book_choice, chapter_choice, verse_choice=None):
    data_directory = 'data'
    
    if tanakh_division_name == "Torah books":
        file_name = "Pentateuch.json"
    elif tanakh_division_name == "Prophets books":
        file_name = "Prophets.json"
    elif tanakh_division_name == "Scriptures books":
        file_name = "Scriptures.json"
    else:
        print("Invalid Tanakh division.")
        return False
    
    file_path = os.path.join(data_directory, file_name)
    
    if not os.path.isfile(file_path):
        print(f"File {file_name} not found in {data_directory}.")
        return False
    
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    if book_choice in data['books']:
        book_data = data['books'][book_choice]
    else:
        print("Invalid book choice.")
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
        print("Invalid chapter choice.")
        return False

def getTanakhBook():
    data = load_data()
    tanakh_division_name, book_choice_num, book_name = prompt_user_for_book(data)

    if not tanakh_division_name or not book_choice_num or not book_name:
        print("Exit: Invalid choice made")
        return None, None, None

    print(f"Tanakh Division: {tanakh_division_name}")
    print(f"Book Choice: {book_choice_num}")
    print(f"Book Name: {book_name}")

    return tanakh_division_name, book_choice_num, book_name

def get_chapter_and_verse_from_user(tanakh_division_name, book_name):
    # Prompt for chapter and verse input
    chapter_choice = input("Enter the chapter number: ")
    verse_choice = input("Enter the verse number (optional): ")
    verse_choice = int(verse_choice) if verse_choice else None

    # Validate chapter and verse using the is_valid_chapter function
    is_valid = is_valid_chapter(tanakh_division_name, book_name, chapter_choice, verse_choice)

    if is_valid:
        print(f"Chapter {chapter_choice} and Verse {verse_choice if verse_choice else ''} are valid!")
        return chapter_choice, verse_choice  # Return the valid chapter and verse values
    else:
        print("Invalid chapter or verse choice.")
        return None, None  # Return None if invalid

##################################################################################
##################################################################################
# Web scraper functions
##################################################################################
##################################################################################


##################################################################################
# Generic function to select an option from a dropdown
##################################################################################
def select_option(driver, dropdown_name, option_text):
    try:
        dropdown = Select(driver.find_element(By.NAME, dropdown_name))
        dropdown.select_by_visible_text(option_text)
        print(f"Option '{option_text}' selected from dropdown '{dropdown_name}'.")
    except Exception as e:
        print(f"Error selecting option '{option_text}' from dropdown '{dropdown_name}': {e}")

##################################################################################
# Function to click a specific link
##################################################################################
def click_link(driver, link_text):
    try:
        link = driver.find_element(By.LINK_TEXT, link_text)
        link.click()
        print(f"Link with text '{link_text}' clicked.")
    except Exception as e:
        print(f"An error occurred while clicking the link '{link_text}': {e}")

if __name__ == "__main__":
    tanakh_division_name, book_choice_num, book_name = getTanakhBook()
    chapter_choice, verse_choice = get_chapter_and_verse_from_user(tanakh_division_name, book_name)
    print(f"TANAKH: {tanakh_division_name}, {book_name}, {chapter_choice}:{verse_choice} ")

    # Open the website
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.chabad.org/library/bible_cdo/aid/63255/jewish/The-Bible-with-Rashi.htm")  # Replace with your desired URL

    # Step 1: Select the desired tanakh section
    if tanakh_division_name == "Torah books":
        tanakh_division_name = "Torah (Pentateuch)"
    elif tanakh_division_name == "Prophets books":
        tanakh_division_name = "Nevi'im (Prophets)"
    elif tanakh_division_name == "Scriptures books":
        tanakh_division_name = "Ketuvim (Scriptures)"
    else:
        print("Invalid choice. Exiting...")

    select_option(driver, "Section", tanakh_division_name)

    # Step 2: Select the book
    select_option(driver, "Book", book_name)

    # Step 3: Select the desired chapter
    # TODO
