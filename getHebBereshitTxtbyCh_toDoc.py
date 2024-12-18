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


# Function to click a specific link
def click_link(driver, link_text):
    try:
        link = driver.find_element(By.LINK_TEXT, link_text)
        link.click()
        print(f"Link with text '{link_text}' clicked.")
    except Exception as e:
        print(f"An error occurred while clicking the link '{link_text}': {e}")

##################################################################################
# Main process to get Genesis and feed the URL into the verse-grabbing function
##################################################################################
def get_Genesis_and_verses(chapter_number, section_option, book_option):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.chabad.org/library/bible_cdo/aid/63255/jewish/The-Bible-with-Rashi.htm")  # Replace with your desired URL
    
    TORAH_OPTION = "Torah (The Pentateuch)"
    NEVIIM_OPTION = "Nevi'im (Prophets)"
    KETUVIM_OPTION = "Ketuvim (Scriptures)"

    # Define valid book options
    VALID_BOOK_OPTIONS = [
        "Bereshit (Genesis)",
        "Shemot (Exodus)",
        "Vayikra (Leviticus)",
        "Bamidbar (Numbers)",
        "Devarim (Deuteronomy)"
    ]

    try:
        # Step 1: Select the desired section
        if section_option.lower() == "torah":
            select_option(driver, "Section", TORAH_OPTION)
        elif section_option.lower() == "nevi'im":
            select_option(driver, "Section", NEVIIM_OPTION)
        elif section_option.lower() == "ketuvim":
            select_option(driver, "Section", KETUVIM_OPTION)
        else:
            print("Invalid section option provided.")
            return

        # Step 2: Validate and select the desired book
        if book_option not in VALID_BOOK_OPTIONS:
            print(f"Invalid book option. Please choose one of the following: {', '.join(VALID_BOOK_OPTIONS)}")
            return 
        select_option(driver, "Book", book_option)
        print(f"Selected book: {book_option}")

        # Step 3: Select the desired chapter
        chapter_dropdown = Select(driver.find_element(By.NAME, "Chapter"))
        chapter_text = f"Chapter {int(chapter_number)}"  # Build the visible text for the chapter
        chapter_dropdown.select_by_visible_text(chapter_text)
        print(f"Selected chapter: {chapter_text}")
        
    finally:
        time.sleep(5)  # Wait to observe the result
        driver.quit()



##################################################################################
# Encapsulated main function
##################################################################################
def main_get_gen_ch():
    # Define valid books and their mappings
    book_mapping = {
        "1": "Bereshit (Genesis)",
        "2": "Shemot (Exodus)",
        "3": "Vayikra (Leviticus)",
        "4": "Bamidbar (Numbers)",
        "5": "Devarim (Deuteronomy)"
    }

    # Prompt the user for the chapter number between 1 and 50
    chapter_number = input("Enter the chapter number (1-50): ").strip()

    # Validate the chapter number input
    if chapter_number.isdigit() and 1 <= int(chapter_number) <= 50:
        # Convert chapter number to two-digit string if necessary
        chapter_number = chapter_number.zfill(2)

        # Prompt the user for the book selection
        print("Select a book:")
        for num, book in book_mapping.items():
            print(f"{num}. {book}")

        book_choice = input("Enter the number corresponding to the book (1-5): ").strip()

        # Validate the book choice input
        if book_choice in book_mapping:
            book_option = book_mapping[book_choice]
            # Pass validated inputs to the function
            get_Genesis_and_verses(
                chapter_number=int(chapter_number), 
                section_option="Torah",
                book_option=book_option
            )
        else:
            print("Invalid book choice. Please select a number between 1 and 5.")
    else:
        print("Invalid chapter number. Please enter a number between 1 and 50.")

def main_get_gen():
    # Iterate through chapters 1 to 50
    for chapter_number in range(1, 51):
        # Convert the chapter number to a two-digit string if necessary
        chapter_number_str = str(chapter_number).zfill(2)
        # Get the verses for the chapter
        get_Genesis_and_verses(chapter_number=2, section_option="Torah", book_option="Bereshit (Genesis)")

##################################################################################
# Function to open a website in Google Chrome on macOS
##################################################################################
def main_open_website_with_chrome(website_url):
    try:
        # Path to the Google Chrome executable on macOS
        chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        subprocess.Popen([chrome_path, website_url])  # Launch Chrome without tying it to the Python script
        print(f"Website {website_url} opened in Google Chrome successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

##################################################################################
# Call prompt_user_choice in the main entry point
##################################################################################
def prompt_user_choice():
    # Ask the user to choose between the options
    print("Choose an option:")
    print("1. Get Genesis Chapter for a specific number")
    print("2. Get Genesis Chapters 1-50")
    print("3. Open english Torah Site")

    choice = input("Please enter a number: 1 through 3.: ").strip()

    if choice == "1":
        # Call the function to get a specific Genesis chapter
        main_get_gen_ch()
    elif choice == "2":
        # Call the function to get all Genesis chapters from 1 to 50
        main_get_gen()
    elif choice == "3":
        # Call the function to get all Genesis chapters from 1 to 50
        eng_website_url = "https://www.chabad.org/library/bible_cdo/aid/63255/jewish/The-Bible-with-Rashi.htm"
        main_open_website_with_chrome(eng_website_url)
    else:
        print("Invalid choice. Please enter a number: 1 through 3.")
        prompt_user_choice()  # Recurse until a valid choice is made

##################################################################################
# Move all the current word files in current directory to a specific folder. 
##################################################################################
def move_word_files_to_folder(destination_folder):
    # Get the current directory
    current_directory = os.getcwd()

    # Ensure the destination folder exists, if not create it
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Loop through all files in the current directory
    for file_name in os.listdir(current_directory):
        # Check if the file is a Word document (.docx)
        if file_name.endswith('.docx'):
            # Construct the full file path
            source_file = os.path.join(current_directory, file_name)
            destination_file = os.path.join(destination_folder, file_name)

            # Move the file (replace if it already exists)
            try:
                shutil.move(source_file, destination_file)
                print(f"Moved: {file_name}")
            except Exception as e:
                print(f"Error moving {file_name}: {e}")

##################################################################################
# Call prompt_user_choice in the main entry point
##################################################################################
if __name__ == "__main__":
    # Ask the user to choose between the options - retrieve data 
    prompt_user_choice()