import json
import os
import time
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from typing import Tuple
import time
from pathlib import Path



# -------------------------
# Bootstrapping Dependencies
# -------------------------
# Get the absolute path to the *parent* of the current file's directory
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

# Folders in the root directory that contain modules
DEPENDENCY_DIRS = [
    BASE_DIR / "web_navigator",
    PROJECT_ROOT / "utils",
    PROJECT_ROOT / "excel_engine"
]

# -------------------------
# Import Dependencies
# -------------------------
from torah_search_bar import gui_getter, getSite
import utils                      # utils directory
import json_funcs                 # utils directory
import excel_engine               # excel_engine directory

def inquireForParasha(book, chapter, verse):

    # Ensure chapter and verse are integers
    chapter = int(chapter)
    verse = int(verse)

    # Get the Parasha from the verse
    parasha = json_funcs.get_parasha(book, chapter, verse)
    json_funcs.set_parasha_json(parasha)
    print(f"Parasha: {parasha}")

    return parasha, book, chapter, verse

def load_eng_website_link(json_filename):
    """
    Load the 'website_eng' URL from a JSON file in the data directory.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "..", "data", json_filename)
    file_path = os.path.normpath(file_path)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Could not find {json_filename} at {file_path}")

    with open(file_path, 'r') as f:
        data = json.load(f)

    return data.get("website_eng"), data.get("book"), data.get("chapter"), data.get("parasha", "Unknown")

def load_json(json_filename):
    """
    Safely load JSON data from a file in the data directory with error checking.

    :param json_filename: str - Filename of the JSON file to load.
    :return: dict - Parsed JSON data.
    :raises FileNotFoundError: If the file does not exist.
    :raises ValueError: If the file is not valid JSON.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "..", "data", json_filename)
    file_path = os.path.normpath(file_path)

    if not os.path.exists(file_path):
        logging.error(f"[ERROR] File not found: {file_path}")
        raise FileNotFoundError(f"Could not find {json_filename} at {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        logging.error(f"[ERROR] Failed to parse JSON in {file_path}: {e}")
        raise ValueError(f"Invalid JSON in {json_filename}: {e}")

    if not isinstance(data, dict):
        logging.error(f"[ERROR] Expected JSON object in {json_filename}, got {type(data)}")
        raise ValueError(f"Expected JSON object in {json_filename}, got {type(data)}")

    return data

def load_json_fields(json_filename, *fields, default=None, folder="data"):
    """
    Load specific fields from a JSON file located in the given folder.

    :param json_filename: Name of the JSON file
    :param fields: Fields to retrieve from the JSON
    :param default: Default value if a field is missing
    :param folder: Folder where the JSON file is stored
    :return: Tuple of values corresponding to the requested fields
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "..", folder, json_filename)
    file_path = os.path.normpath(file_path)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Could not find {json_filename} at {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return tuple(data.get(field, default) for field in fields)


def open_website_from_json(json_filename):
    """
    Load URL from given JSON file and open it using a Selenium WebDriver. Returns the driver.
    """
    url, book, chapter, parasha = load_eng_website_link(json_filename)

    if not url:
        print("No valid URL found in JSON.")
        return None

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        print(f"Opening {url} for {book} ch:{chapter} parasha:({parasha})")
        driver.get(url)
        time.sleep(2)

        final_url = driver.current_url
        driver.get(final_url)
        time.sleep(2)

        return driver

    except Exception as e:
        print(f"Error loading URL: {e}")
        driver.quit()
        return None

def select_chumash_options(driver, book="Genesis", chapter="1", verse="1", debug=False):
    """
    Selects the given book, chapter, and verse from the dropdown menus
    on the Chumash search form.

    Args:
        driver (WebDriver): A Selenium WebDriver instance
        book (str): Name of the book (e.g., "Genesis")
        chapter (str): Chapter number as string (e.g., "1")
        verse (str): Verse number as string (e.g., "1")
        debug (bool): Whether to print debug information

    Returns:
        None
    """
    try:
        # Locate and select the book
        book_select = Select(driver.find_element(By.NAME, "bookq"))
        book_select.select_by_visible_text(book)
        time.sleep(0.5)
    except Exception as e:
        print(f"Error selecting book dropdown: {e}")

    # Select the chapter
    chapter_select = Select(driver.find_element(By.NAME, "chapterq"))
    try:
        # Extract all option texts to debug
        all_chapter_options = [opt.text.strip() for opt in chapter_select.options if opt.text.strip()]
        if debug:
            print("Available chapter options:", all_chapter_options)

        # Attempt matching using startswith (since some options have leading spaces)
        chapter_number = int(chapter)
        matching_option = None
        for option_text in all_chapter_options:
            if option_text.startswith(f"Chapter {chapter_number}"):
                matching_option = option_text
                break

        if matching_option:
            chapter_select.select_by_visible_text(matching_option)
            if debug:
                print(f"Chapter selected: {matching_option}")
        else:
            print(f"Chapter option not found for Chapter {chapter_number}. Options were: {all_chapter_options}")

        time.sleep(0.5)
    except Exception as e:
        print(f"Error selecting chapter dropdown: {e}")

    # Select the verse
    verse_select = Select(driver.find_element(By.NAME, "textq"))
    try:
        verse_select.select_by_visible_text(str(int(verse)))
    except Exception as e:
        print(f"Verse option not found: {verse}. Error: {e}")
    time.sleep(0.5)

    return driver

def click_go_button(driver, timeout=10):
    """
    Clicks the "GO" button on the Chumash search page and returns the driver.

    :param driver: Selenium WebDriver object
    :param timeout: Maximum wait time in seconds for the button to become clickable
    :return: Selenium WebDriver object
    """
    try:
        go_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='GO']"))
        )
        go_button.click()
    except Exception as e:
        print(f"[ERROR] Could not click GO button: {e}")

    return driver

def extract_verse_data(driver: WebDriver, verse_number: int) -> Tuple[str, str, WebDriver]:
    """
    Extracts verse and text from a Metsudah Chumash HTML page using the given Selenium driver.

    Parameters:
        driver (WebDriver): An active Selenium WebDriver instance.
        verse_number (int): The verse number to extract.

    Returns:
        Tuple[str, str, WebDriver]: A tuple containing:
            - The verse label (e.g., 'Verse 17:')
            - The verse text (everything after </b> and before the next <p>)
            - The WebDriver instance
    """
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    target_label = f"Verse {verse_number}:"

    # Find all <b> tags
    for bold in soup.find_all("b"):
        if bold.text.strip() == target_label:
            verse_tag = bold
            verse_string = bold.text.strip()

            # Extract all the text after the </b> until the next <p>
            text_parts = []
            for sibling in bold.next_siblings:
                if sibling.name == 'p':
                    break
                if isinstance(sibling, str):
                    text_parts.append(sibling.strip())
                elif sibling.name is None:
                    text_parts.append(str(sibling).strip())

            verse_text = ' '.join(filter(None, text_parts)).replace('\n', ' ').strip()
            return verse_string, verse_text, driver

    return "", "", driver  # fallback if verse not found

def get_metsudah_verse(book, chapter, verse):
    # Open the English website
    driver = open_website_from_json("current_verse_target.json")

    if not driver:
        return None, None, None

    try:
        print("Initial Page Title:", driver.title)

        # Select book, chapter, and verse
        driver = select_chumash_options(driver, book, chapter, verse)
        time.sleep(3)  # Allow the page to update

        # Click the GO button
        driver = click_go_button(driver)
        print("After GO Click Page Title:", driver.title)
        time.sleep(3)  # Wait for content to load

        # Extract the verse and text
        verse_str, text_str, driver = extract_verse_data(driver, verse)

        return driver, verse_str, text_str

    except Exception as e:
        print("An error occurred:", e)
        return driver, None, None

def get_torah_data_from_gui_prompt():

    book, chapter, verse = gui_getter.get_book_ch_verse_from_gui()
    website = getSite.main()
    parasha = inquireForParasha(book, chapter, verse)
    print(f"{parasha} {book}, ch:{chapter} v:{verse} \nFrom WebSite: {website}")

    return book, chapter, verse, website, parasha

def metsudah_eng_verse_getter(book, chapter, verse, website, parasha):

    # Check for missing inputs
    if not website or parasha is None:
        missing = []
        if not website:
            missing.append("website")
        if parasha is None:
            missing.append("Parasha")
        print(f"[ERROR] No valid {' and '.join(missing)} provided. Exiting.")
        return None, None, None

    ######## 3. Get a specific verse from the Torah on the metsudah site. ##################
    driver, verse_str, text_str = get_metsudah_verse(book, chapter, verse)
    if not driver:
        print("[ERROR] Could not initialize web driver or page load failed.")
        return None, None, None

    return driver, verse_str, text_str

def get_metsudah_ch(book, chapter):
    # Open the English website
    driver = open_website_from_json("current_verse_target.json")

    if not driver:
        return None, None

    try:
        print("Initial Page Title:", driver.title)

        # Select book, chapter, and verse
        starting_verse = "1"
        driver = select_chumash_options(driver, book, chapter, starting_verse)
        time.sleep(3)  # Allow the page to update

        # Click the GO button
        driver = click_go_button(driver)
        print("After GO Click Page Title:", driver.title)
        time.sleep(3)  # Wait for content to load

        total_verses_in_ch = utils.get_torah_ch_verse_num(book, chapter)
        verse_data = {}  # Dictionary to hold verse:text mapping

        for verse in range(1, total_verses_in_ch + 1):
            verse_str, text_str, driver = extract_verse_data(driver, verse)
            verse_data[verse_str] = text_str
            #print(f"{verse_str} {text_str}")

        return verse_data, driver

    except Exception as e:
        print(f"[ERROR] Exception occurred: {e}")
        return None, driver

def get_and_display_metsudah_verse_m():
    book, chapter, verse, website, parasha = get_torah_data_from_gui_prompt();
    driver, verse_str, text_str = metsudah_eng_verse_getter(book, chapter, verse, website, parasha)
    if not driver:
        return

    utils.display_verse(verse_str, text_str)
    driver.quit()

def save_torah_chapter_to_excel(torah_book: str, chapter: int):
    """
    Fetches English Metsudah Torah text for a given book and chapter,
    and writes the verse references and texts to an Excel file.

    Args:
        torah_book (str): Name of the Torah book (e.g., "Genesis").
        chapter (int): Chapter number to retrieve.
    """

    # Step 1: Fetch the verse data from Metsudah
    verse_data, driver = get_metsudah_ch(torah_book, chapter)

    if not isinstance(verse_data, dict):
        print("[ERROR] verse_data is not a dictionary. Exiting.")
        return

    # Step 2: Prepare Excel writing
    sheet_name = f"{torah_book} CH{chapter}"
    directory = utils.OUT_ENG_TORAH_XLSX
    filename = torah_book
    headers = ["Verse", "Verse_String"]

    # Step 3: Create Excel file with headers
    xlsx_path = excel_engine.create_excel_m(filename, directory, headers, sheet_name)

    # Step 4: Write verse data
    if xlsx_path:
        start_row = 2
        for idx, (verse_ref, verse_text) in enumerate(verse_data.items(), start=start_row):
            verse_cell = f"A{idx}"
            text_cell = f"B{idx}"
            excel_engine.write_string_to_excel(xlsx_path, sheet_name=sheet_name, cell=verse_cell, text=verse_ref)
            excel_engine.write_string_to_excel(xlsx_path, sheet_name=sheet_name, cell=text_cell, text=verse_text)

        print(f"Data written to {xlsx_path}")
    else:
        print("Failed to create Excel file.")

    driver.quit()

    # Step 5: Auto-adjust column widths
    final_xlsx_file = directory / f"{filename}.xlsx"
    excel_engine.autofit_excel_columns(final_xlsx_file, sheet_name)

# Example usage
if __name__ == "__main__":
    open_website_with_driver("current_verse_target.json")
