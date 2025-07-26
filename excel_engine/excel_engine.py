import os
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment, PatternFill
from pathlib import Path

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

    # Ensure filename has .xlsx extension
    if not filename.lower().endswith(".xlsx"):
        filename += ".xlsx"

    file_path = os.path.join(directory, filename)

    # Create a new Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"

    # Save the workbook
    wb.save(file_path)
    #print(f"Excel file created: {file_path}")

    return file_path

def style_excel_header(file_path, header_names):
    """
    Applies a styled header row to the first row of an existing Excel file.

    Args:
        file_path (str): Path to the existing Excel (.xlsx) file.
        header_names (list): List of strings representing column headers.

    Returns:
        bool: True if successful, False otherwise.
    """
    if not os.path.exists(file_path):
        print(f"[ERROR] File not found: {file_path}")
        return False

    try:
        wb = load_workbook(file_path)
        ws = wb.active

        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
        header_align = Alignment(horizontal="center", vertical="center")

        for col_idx, header in enumerate(header_names, start=1):
            cell = ws.cell(row=1, column=col_idx, value=header)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = header_align

        wb.save(file_path)
        #print(f"Header styled and saved to: {file_path}")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to apply header: {e}")
        return False

def freeze_excel_header_row(file_path, sheet_name=None):
    """
    Freezes the first row of an existing Excel sheet so the header stays visible when scrolling.

    Args:
        file_path (str): Path to the existing Excel file.
        sheet_name (str, optional): Name of the sheet to freeze the header in. 
                                    If None, the active sheet is used.

    Returns:
        bool: True if successful, False if file/sheet not found.
    """
    try:
        wb = load_workbook(file_path)
        ws = wb[sheet_name] if sheet_name else wb.active

        # Freeze the first row
        ws.freeze_panes = ws['A2']

        # Save changes
        wb.save(file_path)
        #print(f"[INFO] First row frozen in: {file_path}")
        return True

    except FileNotFoundError:
        print(f"[ERROR] File not found: {file_path}")
        return False
    except KeyError:
        print(f"[ERROR] Sheet '{sheet_name}' not found in file: {file_path}")
        return False
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return False


def create_excel_m(filename: str, directory: Path, headers: list[str]):
    """
    Creates an Excel file with a styled header and frozen header row.

    Args:
        filename (str): Desired Excel filename, with or without '.xlsx' extension.
        directory (Path): Target directory to save the Excel file.
        headers (list[str]): List of column headers.

    Returns:
        Path: Full path to the created Excel file, or None if there was an error.
    """
    # Ensure filename has the .xlsx extension
    if not filename.endswith(".xlsx"):
        filename += ".xlsx"

    # Ensure directory exists
    if not directory.exists():
        print(f"[ERROR] Directory does not exist: {directory}")
        return None

    xlsx_path = directory / filename

    # Create the file
    create_excel_file(filename, directory)

    # Apply headers
    style_excel_header(xlsx_path, headers)

    # Freeze header row
    freeze_excel_header_row(xlsx_path)

    #print(f"[INFO] Excel file created and styled: {xlsx_path}")
    return xlsx_path