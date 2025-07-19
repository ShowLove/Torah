import tkinter as tk
from tkinter import ttk
import json
import os
import gui_utils

def load_websites():
    """
    Loads website list from data/websites.json.
    """
    file_path = os.path.join("data", "websites.json")
    with open(file_path, "r") as f:
        return json.load(f)

def create_eng_site_getter():
    """
    Creates the GUI, waits for selection, and exits with selected website.
    """
    data = load_websites()
    site_names = [site["name"] for site in data]
    selected_site = {"value": None}  # Use dict for mutable scope in nested function

    def on_site_selected(event):
        selected_site["value"] = selected_site_var.get()
        root.destroy()  # Close GUI

    root = tk.Tk()
    root.title("ENG WEBSITE SELECTOR")

    selected_site_var = tk.StringVar()

    # Label
    ttk.Label(root, text="Select a Website:").pack(padx=5, pady=5)

    # Dropdown (Combobox)
    dropdown = ttk.Combobox(root, textvariable=selected_site_var, values=site_names, state="readonly")
    dropdown.pack(fill='x', padx=5)
    dropdown.bind("<<ComboboxSelected>>", on_site_selected)

    root.mainloop()

    return selected_site["value"]

# Example usage
def main():
    website = create_eng_site_getter()
    print(f"Selected Website: {website}")

    # Update JSON using the utility function
    gui_utils.update_selection_json(website_eng=website)
    return website

if __name__ == "__main__":
    main()
