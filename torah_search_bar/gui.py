import tkinter as tk
from tkinter import ttk
from search_engine import load_json_files, search_data

# Load JSON data at startup
data = load_json_files()

# Global to map listbox index → source book
result_metadata = {}

# Global to hold selected book variation from result
selected_book_variation = None

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

def on_result_selected(event):
    """
    Triggered when user selects a result in the Listbox.
    Finds the corresponding book and saves its first variation.
    """
    global selected_book_variation
    widget = event.widget
    if widget.curselection():
        index = widget.curselection()[0]
        book_data = result_metadata.get(index)
        if book_data:
            selected_book_variation = book_data["variations"][0]
            print(f"Selected Book Variation: {selected_book_variation}")

def create_gui():
    """
    Creates the Tkinter GUI
    """
    root = tk.Tk()
    root.title("JSON Search")

    search_var = tk.StringVar()

    ttk.Label(root, text="Search:").pack(padx=5, pady=5)
    ttk.Entry(root, textvariable=search_var).pack(fill='x', padx=5)

    result_box = tk.Listbox(root, width=80)
    result_box.pack(padx=5, pady=10, fill='both', expand=True)

    # Bind listbox click
    result_box.bind("<<ListboxSelect>>", on_result_selected)

    ttk.Button(
        root,
        text="Search",
        command=lambda: perform_search(search_var, result_box)
    ).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
