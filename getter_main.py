import sys
import os

######################################################################
# Dependency Folders: torah_search_bar, data, utils ##################
# torah_search_bar
current_dir = os.path.dirname(os.path.abspath(__file__))
torah_search_bar_path = os.path.join(current_dir, "torah_search_bar")
sys.path.append(torah_search_bar_path)
# data
data_path = os.path.join(current_dir, "data")
sys.path.append(data_path)
# utils
utils_path = os.path.join(current_dir, "utils")
sys.path.append(utils_path)
######################################################################

from torah_search_bar import getBookChVerse, getSite

def main():

    book, chapter, verse = getBookChVerse.main()
    website = getSite.main()

    print("\n--- Final Selection ---")
    print(f"Book: {book}")
    print(f"Chapter: {chapter}")
    print(f"Verse: {verse}")
    print(f"Eng Website: {website}")


if __name__ == "__main__":
    main()
