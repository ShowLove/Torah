import json
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
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

def select_chumash_options(driver, book="Genesis", chapter="1", verse="1"):
    """
    Selects the given book, chapter, and verse from the dropdown menus
    on the Chumash search form.

    Args:
        driver (WebDriver): A Selenium WebDriver instance
        book (str): Name of the book (e.g., "Genesis")
        chapter (str): Chapter number as string (e.g., "1")
        verse (str): Verse number as string (e.g., "1")

    Returns:
        None
    """
    try:
        # Locate and select the book
        book_select = Select(driver.find_element(By.NAME, "bookq"))
        book_select.select_by_visible_text(book)
        time.sleep(0.5)
    except Exception as e:
        print(f"Error selecting book: {e}")

    # Select the chapter
    try:
        chapter_select = Select(driver.find_element(By.NAME, "chapterq"))

        # Extract all option texts to debug
        all_chapter_options = [opt.text.strip() for opt in chapter_select.options if opt.text.strip()]
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
            print(f"Chapter selected: {matching_option}")
        else:
            print(f"Chapter option not found for Chapter {chapter_number}. Options were: {all_chapter_options}")

        time.sleep(0.5)
    except Exception as e:
        print(f"Error selecting chapter: {e}")

    # Select the verse
    try:
        verse_select = Select(driver.find_element(By.NAME, "textq"))
        verse_select.select_by_visible_text(str(int(verse)))
    except Exception as e:
        print(f"Verse option not found: {verse}, error: {e}")

    time.sleep(0.5)


# Example usage
if __name__ == "__main__":
    open_website_with_driver("current_verse_target.json")
