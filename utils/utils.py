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
import sys
from pathlib import Path

# -------------------------
# Bootstrapping Dependencies
# -------------------------
# Get the absolute path to the *parent* of the current file's directory
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

# Folders in the root directory that contain modules
DEPENDENCY_DIRS = [
    PROJECT_ROOT / "torah_search_bar",
    PROJECT_ROOT / "utils",
    PROJECT_ROOT / "data",
    PROJECT_ROOT / "web_navigator",
    PROJECT_ROOT / "excel_engine"
]

# Add each dependency directory to sys.path if not already added
for path in DEPENDENCY_DIRS:
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.append(path_str)

# absolute paths to subdirectories
TORAH_SEARCH_BAR_DIR = PROJECT_ROOT / "torah_search_bar"
UTILS_DIR = PROJECT_ROOT / "utils"
DATA_DIR = PROJECT_ROOT / "data"
WEB_NAVIGATOR_DIR = PROJECT_ROOT / "web_navigator"
EXCEL_ENGINE_DIR = PROJECT_ROOT / "excel_engine"

# sub-paths
OUTPUT_DATA_DIR = DATA_DIR / "output_data"
OUT_ENG_TORAH_XLSX = OUTPUT_DATA_DIR / "eng_torah_xlsx"

import excel_engine

def terminal_prompt():
    # Ask the user to choose between the options
    print("Choose an option:")
    print("     1. Get a single verse from GUI input retrieved from the metsudah site")
    print("     2. Get a chapter of the Torah: ")
    choice = input("Please enter a number: 1 through 2.      :").strip()
    return choice

def display_verse(verse_str, text_str):
    """
    Displays the verse label and text if both are provided.
    Parameters:
        verse_str (str): The label or reference of the verse (e.g., "Genesis 1:1").
        text_str (str): The text/content of the verse.
    """
    if verse_str and text_str:
        print("Verse Label:", verse_str)
        print("Verse Text:", text_str)
    else:
        print("Verse not found.")

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

def get_torah_ch_verse_num(book_name, chapter_number, json_filename="TorahChapterLengths.json"):
    """
    Given a book name and chapter number, prints the verse numbers for that chapter.

    :param book_name: str - The name of the book (e.g., "Bereshit (Genesis)")
    :param chapter_number: int - The chapter number (e.g., 1)
    :param json_path: str - Path to the JSON file
    """
    # Load the JSON data
    data = load_json(json_filename)
    torah_data = load_json("current_verse_target.json")

    print("JSON loaded successfully:")
    print(json_filename)

    # Validate book
    books = data.get("books", {})
    if book_name not in books:
        print(f"[ERROR] Book '{book_name}' not found in data.")
        return

    chapters = books[book_name].get("chapters", {})

    chapter_str = str(chapter_number)
    if chapter_str not in chapters:
        print(f"[ERROR] Chapter '{chapter_number}' not found in book '{book_name}'.")
        return

    total_verses = chapters[chapter_str]
    print(f"Chapter {chapter_number} of {book_name} has {total_verses} verses:")
    return total_verses