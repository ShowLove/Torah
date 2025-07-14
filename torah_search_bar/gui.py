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

def on_result_selected(event, result_box, result_metadata, selected_book_variation, fields_to_show):
    """
    Handles selection from the result box and reveals input fields (like chapter/verse).
    
    Parameters:
    - event: The triggering event.
    - result_box: The Listbox widget containing search results.
    - result_metadata: A dict mapping result indices to book names.
    - selected_book_variation: A StringVar to store the selected book key.
    - fields_to_show: A list of (label_widget, entry_widget) tuples to pack and show.
    """
    selected_index = result_box.curselection()
    if selected_index:
        index = selected_index[0]
        book_key = result_metadata.get(index)
        if book_key:
            selected_book_variation.set(book_key)

            # Show all provided label/entry pairs
            for label, entry in fields_to_show:
                label.pack(padx=5, pady=5)
                entry.pack(fill='x', padx=5)

            # Focus the first entry field
            if fields_to_show:
                fields_to_show[0][1].focus_set()

def create_gui():
    root = tk.Tk()
    root.title("TORAH SEARCH")

    # Define StringVar variables
    search_var = tk.StringVar()
    selected_book_variation = tk.StringVar()
    chapter_num = tk.StringVar()
    verse_num = tk.StringVar()

    # Search input field
    ttk.Label(root, text="TORAH BOOK:").pack(padx=5, pady=5)
    book_entry = ttk.Entry(root, textvariable=search_var)
    book_entry.pack(fill='x', padx=5)

    # Result listbox
    result_box = tk.Listbox(root, width=80)
    result_box.pack(padx=5, pady=10, fill='both', expand=True)

    # Chapter and Verse widgets (initially hidden)
    chapter_label = ttk.Label(root, text="CHAPTER:")
    chapter_entry = ttk.Entry(root, textvariable=chapter_num)
    verse_label = ttk.Label(root, text="VERSE:")
    verse_entry = ttk.Entry(root, textvariable=verse_num)

    # Group label/entry pairs for reuse
    fields_to_show = [(chapter_label, chapter_entry), (verse_label, verse_entry)]

    # Bind result selection to generic handler
    result_box.bind("<<ListboxSelect>>", lambda event: on_result_selected(
        event, result_box, result_metadata, selected_book_variation, fields_to_show))
    result_box.bind("<Return>", lambda event: on_result_selected(
        event, result_box, result_metadata, selected_book_variation, fields_to_show))

    # Search button
    ttk.Button(
        root,
        text="Search Book",
        command=lambda: perform_search(search_var, result_box)
    ).pack(pady=5)

    # Allow Enter key in entry to trigger search
    book_entry.bind('<Return>', lambda event: perform_search(search_var, result_box))

    # Handle window close
    def on_close():
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_close)

    # Launch GUI
    root.mainloop()

    # Return values after GUI closes
    return selected_book_variation.get(), chapter_num.get(), verse_num.get()

# Run and print results
if __name__ == "__main__":
    book, chapter, verse = create_gui()
    print(f"Selected Book: {book}")
    print(f"Chapter: {chapter}")
    print(f"Verse: {verse}")
