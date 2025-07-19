import getBookChVerse
import getSite

def main():
    # Step 1: Launch Book/Chapter/Verse Selector
    book, chapter, verse = getBookChVerse.main()

    # Step 2: Launch Website Selector
    website = getSite.main()

    # Optional: Do something with the combined results
    print("\n--- Final Selection ---")
    print(f"Book: {book}")
    print(f"Chapter: {chapter}")
    print(f"Verse: {verse}")
    print(f"Website: {website}")

if __name__ == "__main__":
    main()
