# getter_main.py
import sys
import os
import time


######################################################################
# Dependency Folders: torah_search_bar, data, utils ##################
######################################################################
current_dir = os.path.dirname(os.path.abspath(__file__))

# torah_search_bar
sys.path.append(os.path.join(current_dir, "torah_search_bar"))

# data
sys.path.append(os.path.join(current_dir, "data"))

# utils
utils_path = os.path.join(current_dir, "utils")
sys.path.append(utils_path)

# web_navigator
web_navigator_path = os.path.join(current_dir, "web_navigator")
sys.path.append(web_navigator_path)
######################################################################

from torah_search_bar import getBookChVerse, getSite
import findParashaFromVerse       # Make sure this file exists in utils
import metsudah_chumash_web_nav   # Make sure this file exists in web_navigator

def inquireForParasha():
    book, chapter, verse = getBookChVerse.main()
    website = getSite.main()

    # Ensure chapter and verse are integers
    chapter = int(chapter)
    verse = int(verse)

    print("\n--- Final Selection ---")
    print(f"Book: {book}")
    print(f"Chapter: {chapter}")
    print(f"Verse: {verse}")
    print(f"Eng Website: {website}")

    # Get the Parasha from the verse
    parasha = findParashaFromVerse.get_parasha(book, chapter, verse)
    print(f"Parasha: {parasha}")

    return parasha, book, chapter, verse, website

def main():
	# Get Torah Data to navigate ther web and do the backend with
    parasha, book, chapter, verse, website = inquireForParasha()
    print(f"{parasha} {book}, ch:{chapter} v:{verse}")
    print(f"From WebSite: {website}")

    #Open the Eng website
    driver = metsudah_chumash_web_nav.open_website_from_json("current_verse_target.json")

    if driver:
        try:
            # --- Add your page interaction logic here ---
            # For example, get the page title:
            print("Page Title:", driver.title)

            # Example hardcoded values — these would come from your JSON or logic
            #book = "Exodus"
            #chapter = 2
            #verse = 2

            # Interact with the page to select options
            driver = metsudah_chumash_web_nav.select_chumash_options(driver, book, chapter, verse)
            time.sleep(3)  # Pause for 3 seconds

        finally:
            driver.quit()

if __name__ == "__main__":
    main()
