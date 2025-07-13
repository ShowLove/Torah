import tkinter as tk
from tkinter import ttk
from search_engine import load_json_files, search_data

# Load data at startup
data = load_json_files()
result_metadata = {}  # Maps listbox indices to books


def perform_search(search_var, result_box):
    """
    Searches and populates results. Also maps result index to book.
    """
    global result_metadata
    query = search_var.get()
    result_box.delete(0, tk.END)
    result_metadata.clear()

    index = 0
    for book in data:
        results = search_data(query, [book])  # Search in each book
        for res in results:
            result_box.insert(tk.END, str(res))
            result_metadata[index] = book  # Map index to book
            index += 1


def create_gui():
    # Create the main Tkinter window
    root = tk.Tk()
    root.title("TORAH SEARCH")  # Set the window title

    # Define StringVar variables to hold user input
    search_var = tk.StringVar()             # Holds the search term entered by the user
    selected_book_variation = tk.StringVar()# Will hold the selected book from search results
    chapter_num = tk.StringVar()            # Will hold the user-inputted chapter number
    verse_num = tk.StringVar()              # Will hold the user-inputted verse number

    # Label and entry field for the book search
    ttk.Label(root, text="TORAH BOOK:").pack(padx=5, pady=5)
    book_entry = ttk.Entry(root, textvariable=search_var)  # Entry widget for search input
    book_entry.pack(fill='x', padx=5)  # Expand entry horizontally

    # Create a Listbox to show matching book names after search
    result_box = tk.Listbox(root, width=80)
    result_box.pack(padx=5, pady=10, fill='both', expand=True)

    # Create labels and entry fields for CHAPTER and VERSE (initially hidden)
    chapter_label = ttk.Label(root, text="CHAPTER:")
    chapter_entry = ttk.Entry(root, textvariable=chapter_num)

    verse_label = ttk.Label(root, text="VERSE:")
    verse_entry = ttk.Entry(root, textvariable=verse_num)

    # Function triggered when a search result is selected (by click or Enter key)
    def on_result_selected(event=None):
        selected_index = result_box.curselection()  # Get the currently selected index
        if selected_index:
            index = selected_index[0]
            book_key = result_metadata.get(index)  # Get book name from metadata mapping
            if book_key:
                selected_book_variation.set(book_key)  # Save selected book

                # Show CHAPTER and VERSE fields when a book is selected
                chapter_label.pack(padx=5, pady=5)
                chapter_entry.pack(fill='x', padx=5)
                verse_label.pack(padx=5, pady=5)
                verse_entry.pack(fill='x', padx=5)

                chapter_entry.focus_set()  # Move cursor to chapter input

    # Bind mouse click selection and Enter key to trigger selection handler
    result_box.bind("<<ListboxSelect>>", on_result_selected)
    result_box.bind("<Return>", on_result_selected)

    # Button that performs the book search
    ttk.Button(
        root,
        text="Search Book",
        command=lambda: perform_search(search_var, result_box)  # Run search on click
    ).pack(pady=5)

    # Allow pressing Enter in the book search field to trigger the search
    book_entry.bind('<Return>', lambda event: perform_search(search_var, result_box))

    # Define a cleanup function to close the GUI window
    def on_close():
        root.destroy()

    # Bind the window close event to the cleanup function
    root.protocol("WM_DELETE_WINDOW", on_close)

    # Start the Tkinter event loop (shows window and listens for user input)
    root.mainloop()

    # Return the values selected/inputted by the user after the window closes
    return selected_book_variation.get(), chapter_num.get(), verse_num.get()

# Run and print results
if __name__ == "__main__":
    book, chapter, verse = create_gui()
    print(f"Selected Book: {book}")
    print(f"Chapter: {chapter}")
    print(f"Verse: {verse}")
