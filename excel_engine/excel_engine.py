import os
from openpyxl import Workbook

def create_excel_file(filename, directory):
    """
    Creates an Excel file with the given filename in the specified directory.

    Args:
        filename (str): Name of the Excel file to create (e.g., 'report.xlsx').
        directory (str): Directory path where the Excel file should be created.

    Returns:
        str: Full path to the created Excel file, or None if directory doesn't exist.
    """
    if not os.path.isdir(directory):
        print(f"[ERROR] Directory does not exist: {directory}")
        return None

    file_path = os.path.join(directory, filename)

    # Create a new Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"

    # Optionally write some data here
    ws['A1'] = "Hello"
    ws['B1'] = "World"

    # Save the workbook
    wb.save(file_path)
    print(f"Excel file created: {file_path}")

    return file_path

def test():
    print("Test !!!!!!!!")
    return