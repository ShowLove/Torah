import tkinter as tk
from tkinter import ttk
from search_engine import load_json_files, search_data

# Load JSON data from the "data/" folder at startup
data = load_json_files()

def perform_search(search_var, result_box):
    """
    Runs when the user clicks the "Search" button.
    Performs a search on the loaded data and displays results.
    """
    query = search_var.get()  # Get user input from the entry field
    results = search_data(query, data)  # Run the search
    result_box.delete(0, tk.END)  # Clear previous results
    for res in results:
        result_box.insert(tk.END, str(res))  # Add each result to the list

def create_gui():
    """
    Sets up and runs the Tkinter GUI.
    """
    root = tk.Tk()
    root.title("JSON Search")  # Set window title

    search_var = tk.StringVar()

    # Label for the search bar
    ttk.Label(root, text="Search:").pack(padx=5, pady=5)

    # Entry field for search input
    ttk.Entry(root, textvariable=search_var).pack(fill='x', padx=5)

    # Create the results Listbox before passing to the button
    result_box = tk.Listbox(root, width=80)
    result_box.pack(padx=5, pady=10, fill='both', expand=True)

    # Button to trigger the search
    ttk.Button(
        root,
        text="Search",
        command=lambda: perform_search(search_var, result_box)
    ).pack(pady=5)

    # Run the GUI loop
    root.mainloop()

# Run the GUI
if __name__ == "__main__":
    create_gui()
