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

def get_torah_chapter(book_name, chapter_number, json_filename="TorahChapterLengths.json"):
    """
    Given a book name and chapter number, prints the verse numbers for that chapter.

    :param book_name: str - The name of the book (e.g., "Bereshit (Genesis)")
    :param chapter_number: int - The chapter number (e.g., 1)
    :param json_path: str - Path to the JSON file
    """
    # Load the JSON data
    data = load_json(json_filename)

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
    for verse in range(1, total_verses + 1):
        print(f"Verse {verse}")