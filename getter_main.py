import sys
import os

# Add the torah_search_bar folder to the system path
current_dir = os.path.dirname(os.path.abspath(__file__))
torah_search_bar_path = os.path.join(current_dir, "torah_search_bar")
sys.path.append(torah_search_bar_path)

# Now imports from submodules should work
from torah_search_bar import getBookChVerse, getSite

def main():
    book, chapter, verse = getBookChVerse.main()
    website = getSite.main()

    print("\n--- Final Selection ---")
    print(f"Book: {book}")
    print(f"Chapter: {chapter}")
    print(f"Verse: {verse}")
    print(f"Website: {website}")


if __name__ == "__main__":
    main()
