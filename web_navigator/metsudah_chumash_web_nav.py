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

# Example usage
if __name__ == "__main__":
    open_website_with_driver("current_verse_target.json")
