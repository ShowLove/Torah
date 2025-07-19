import tkinter as tk
from tkinter import ttk
from search_engine import load_json_files, search_data
import tkinter.messagebox as messagebox
import gui_utils

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
            # Instead of printing the full result, just show the canonical book name
            result_box.insert(tk.END, book["book"])
            result_metadata[index] = book["book"]  # Map index to book name string
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

def create_search_ui(root):
    search_var = tk.StringVar()
    selected_book_variation = tk.StringVar()

    # Book search label + entry
    ttk.Label(root, text="TORAH BOOK:").pack(padx=5, pady=5)
    book_entry = ttk.Entry(root, textvariable=search_var)
    book_entry.pack(fill='x', padx=5)

    # Result box
    result_box = tk.Listbox(root, width=80)
    result_box.pack(padx=5, pady=10, fill='both', expand=True)

    # Search button
    ttk.Button(
        root,
        text="Search Book",
        command=lambda: perform_search(search_var, result_box)
    ).pack(pady=5)

    # Trigger search on Enter
    book_entry.bind('<Return>', lambda event: perform_search(search_var, result_box))

    return search_var, selected_book_variation, result_box

def create_labeled_entry(root, label_text, text_variable):
    label = ttk.Label(root, text=label_text)
    entry = ttk.Entry(root, textvariable=text_variable)
    return label, entry

def prompt_user_and_exit(root, condition_func, prompt_text):
    """
    Prompts the user with a Yes/No dialog and closes the GUI if they confirm.

    Parameters:
    - root: The Tk root window (used for closing)
    - condition_func: A callable that returns True if the prompt should be shown
    - prompt_text: The message to display in the dialog
    """
    if condition_func():
        if messagebox.askyesno("Exit?", prompt_text):
            root.destroy()

def create_gui():
    root = tk.Tk()
    root.title("TORAH SEARCH")

    # Setup search section
    search_var, selected_book_variation, result_box = create_search_ui(root)

    # Create chapter and verse fields
    chapter_num = tk.StringVar()
    verse_num = tk.StringVar()

    chapter_label, chapter_entry = create_labeled_entry(root, "CHAPTER:", chapter_num)
    verse_label, verse_entry = create_labeled_entry(root, "VERSE:", verse_num)

    fields_to_show = [(chapter_label, chapter_entry), (verse_label, verse_entry)]

    # Bind result selection to show chapter/verse fields
    result_box.bind("<<ListboxSelect>>", lambda event: on_result_selected(
        event, result_box, result_metadata, selected_book_variation, fields_to_show))
    result_box.bind("<Return>", lambda event: on_result_selected(
        event, result_box, result_metadata, selected_book_variation, fields_to_show))

    # called twice because it’s being passed separately in each bind() call 
    exit_prompt_text = "You've entered the verse. Exit now?"
    verse_entry.bind("<Return>", lambda event: prompt_user_and_exit(
        root, lambda: verse_num.get().strip(), exit_prompt_text))
    verse_entry.bind("<FocusOut>", lambda event: prompt_user_and_exit(
        root, lambda: verse_num.get().strip(), exit_prompt_text))

    # Handle window close
    root.protocol("WM_DELETE_WINDOW", root.destroy)

    # Start event loop
    root.mainloop()

    # Return values after GUI closes
    return selected_book_variation.get(), chapter_num.get(), verse_num.get()


# Run and print results
def main():
    # Launch the GUI and capture results
    book, chapter, verse = create_gui()

    # Print selected results
    print(f"Selected Book: {book}")
    print(f"Chapter: {chapter}")
    print(f"Verse: {verse}")

    # Update JSON using the utility function
    gui_utils.update_selection_json(book=book, chapter=chapter, verse=verse)
    return book, chapter, verse

if __name__ == "__main__":
    main()
