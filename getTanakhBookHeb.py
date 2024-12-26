import json
import os

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
        file_name = "Scritpures.json"
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
    chapter_choice = input("Enter the chapter number: ")
    verse_choice = input("Enter the verse number (optional): ")
    verse_choice = int(verse_choice) if verse_choice else None

    is_valid = is_valid_chapter(tanakh_division_name, book_name, chapter_choice, verse_choice)

    if is_valid:
        print(f"Chapter {chapter_choice} and Verse {verse_choice if verse_choice else ''} are valid!")
    else:
        print("Invalid chapter or verse choice.")

if __name__ == "__main__":
    tanakh_division_name, book_choice_num, book_name = getTanakhBook()

    if tanakh_division_name and book_choice_num and book_name:
        get_chapter_and_verse_from_user(tanakh_division_name, book_name)
    else:
        print("No valid selection was made. Exiting...")