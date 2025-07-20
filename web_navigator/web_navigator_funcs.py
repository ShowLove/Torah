import json
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

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

# Example usage
if __name__ == "__main__":
    open_website_with_driver("current_verse_target.json")
