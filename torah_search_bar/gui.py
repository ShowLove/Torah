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
    root = tk.Tk()
    root.title("TORAH SEARCH")

    # Variables for selections
    search_var = tk.StringVar()
    selected_book_variation = tk.StringVar()
    chapter_num = tk.StringVar()
    verse_num = tk.StringVar()

    # Book Search
    ttk.Label(root, text="TORAH BOOK:").pack(padx=5, pady=5)
    book_entry = ttk.Entry(root, textvariable=search_var)
    book_entry.pack(fill='x', padx=5)

    # Search results list
    result_box = tk.Listbox(root, width=80)
    result_box.pack(padx=5, pady=10, fill='both', expand=True)

    # CHAPTER and VERSE widgets (initially hidden)
    chapter_label = ttk.Label(root, text="CHAPTER:")
    chapter_entry = ttk.Entry(root, textvariable=chapter_num)

    verse_label = ttk.Label(root, text="VERSE:")
    verse_entry = ttk.Entry(root, textvariable=verse_num)

    def on_result_selected(event=None):
        selected_index = result_box.curselection()
        if selected_index:
            index = selected_index[0]
            book_key = result_metadata.get(index)
            if book_key:
                selected_book_variation.set(book_key)

                # Show CHAPTER and VERSE input fields
                chapter_label.pack(padx=5, pady=5)
                chapter_entry.pack(fill='x', padx=5)
                verse_label.pack(padx=5, pady=5)
                verse_entry.pack(fill='x', padx=5)

                chapter_entry.focus_set()

    # Bind selection and Enter key
    result_box.bind("<<ListboxSelect>>", on_result_selected)
    result_box.bind("<Return>", on_result_selected)

    # Search button
    ttk.Button(
        root,
        text="Search Book",
        command=lambda: perform_search(search_var, result_box)
    ).pack(pady=5)

    # Also trigger search on Enter key in entry box
    book_entry.bind('<Return>', lambda event: perform_search(search_var, result_box))

    def on_close():
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

    # Return values after GUI closes
    return selected_book_variation.get(), chapter_num.get(), verse_num.get()


# Run and print results
if __name__ == "__main__":
    book, chapter, verse = create_gui()
    print(f"Selected Book: {book}")
    print(f"Chapter: {chapter}")
    print(f"Verse: {verse}")
