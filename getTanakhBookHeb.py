import json
import os

# Load data from the external JSON file
def load_data():
    with open('tanakhOutlineHeb.json', 'r', encoding='utf-8') as file:
        return json.load(file)

def prompt_user_for_book(data):
    #########################################
    # Step 1: Prompt the user for the section
    # 1. Torah (The Pentateuch)
    # 2. Nevi'im (Prophets)
    # 3. Ketuvim (Scriptures)
    #########################################
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
        return None, None
    
    ##############################################
    # Step 2: Prompt the user for the Tanakh book
    ##############################################
    print(f"\nYou selected: {data['sections'][tanakh_divisions]}")
    print("\nPlease choose a book:")

    books = data[tanakh_division_name]
    for key, value in books.items():
        print(f"{key}. {value}")

    book_choice = input("Enter the number corresponding to your choice: ")

    if book_choice in books:
        book_name = books[book_choice]
        print(f"\nYou selected: {book_name}")
        return tanakh_division_name, book_choice, book_name  # Returning both number and name
    else:
        print("Invalid choice. Exiting...")
        return None, None, None  # Return None for all if invalid choice is made

# Function to check if the chapter is valid
def is_valid_chapter(tanakh_division_name, book_choice, chapter_choice, verse_choice=None):
    # Define the directory where the JSON files are stored
    data_directory = 'data'
    
    # Load the appropriate JSON file based on the Tanakh division name
    if tanakh_division_name == "Torah books":
        file_name = "Pentateuch.json"
    elif tanakh_division_name == "Prophets books":
        file_name = "Prophets.json"
    elif tanakh_division_name == "Scriptures books":
        file_name = "Scritpures.json"
    else:
        print("Invalid Tanakh division.")
        return False
    
    # Build the full path to the JSON file
    file_path = os.path.join(data_directory, file_name)
    
    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"File {file_name} not found in {data_directory}.")
        return False
    
    # Read the JSON data
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # Check if the book exists in the loaded data
    if book_choice in data['books']:
        book_data = data['books'][book_choice]
    else:
        print("Invalid book choice.")
        return False
    
    # Check if the chapter exists in the selected book
    if chapter_choice in book_data['chapters']:
        # Get the total verses in the chapter
        total_verses = book_data['chapters'][chapter_choice]
        
        # If a verse number is provided, check if it's valid
        if verse_choice is not None:
            if 1 <= verse_choice <= total_verses:
                return True
            else:
                print(f"Invalid verse choice. Chapter {chapter_choice} has {total_verses} verses.")
                return False
        else:
            return True  # The chapter exists, no need for verse validation if it's not provided
    else:
        print("Invalid chapter choice.")
        return False


def getTanakhBook():
    # Load data from JSON
    data = load_data()
    
    # Prompt user for Tanakh division and its book choice:
    tanakh_division_name, book_choice_num, book_name = prompt_user_for_book(data)

    if not tanakh_division_name:
        print("Exit: Invalid tanakh_division_name")
        return  # Exit if invalid choice was made

    if not book_choice_num:
        print("Exit: Invalid book_choice_num")
        return  # Exit if invalid choice was made

    if not book_name:
        print("Exit: Invalid book_name")
        return  # Exit if invalid choice was made

    # If valid choices are made, print them
    print(f"Tanakh Division: {tanakh_division_name}")
    print(f"Book Choice: {book_choice_num}")
    print(f"Book Name: {book_name}")

    # Return the values if valid choices are made
    return tanakh_division_name, book_choice_num, book_name

if __name__ == "__main__":
    # Get the desired Tanakh book
    tanakh_division_name, book_choice_num, book_name = getTanakhBook()