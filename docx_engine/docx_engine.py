from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

# DOCX Constants
DOCX_HEBREW_FONT = "Frank Ruehl"  # Use Frank Ruehl for Hebrew text on Word
DOCX_ENGLISH_FONT = "Times New Roman"  # Use Times New Roman for English text
FONT_SIZE_HEB = 16  # Font size in points
FONT_SIZE_ENG = 12  # Font size in points
MARGIN_SIZE = Pt(12)  # Margin size in points

def create_docx_with_header(eng_str: str, heb_str: str, file_path: str, file_name: str):
    """
    Create a DOCX document with a styled bilingual header.

    Args:
        eng_str (str): English header text.
        heb_str (str): Hebrew header text.
        file_path (str): Folder path to save the document.
        file_name (str): Name of the DOCX file to save.

    Returns:
        Document: A python-docx Document object with the header created.
    """
    doc = Document()

    # Add Hebrew header
    heb_para = doc.add_paragraph()
    heb_run = heb_para.add_run(heb_str)
    heb_run.font.name = DOCX_HEBREW_FONT
    heb_run.font.size = Pt(FONT_SIZE_HEB)
    heb_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    # Add English header
    eng_para = doc.add_paragraph()
    eng_run = eng_para.add_run(eng_str)
    eng_run.font.name = DOCX_ENGLISH_FONT
    eng_run.font.size = Pt(FONT_SIZE_ENG)
    eng_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Set margins
    sections = doc.sections
    for section in sections:
        section.top_margin = MARGIN_SIZE
        section.bottom_margin = MARGIN_SIZE
        section.left_margin = MARGIN_SIZE
        section.right_margin = MARGIN_SIZE

    # Save file
    os.makedirs(file_path, exist_ok=True)
    full_path = os.path.join(file_path, file_name)
    doc.save(full_path)

    return doc

def append_paragraph_to_docx(doc: Document, text: str, is_hebrew: bool = False):
    """
    Appends a paragraph with specified text to a DOCX Document object.

    Args:
        doc (Document): An existing python-docx Document object.
        text (str): Text content to append.
        is_hebrew (bool): Whether the text is Hebrew (sets font/alignment accordingly).
    """
    para = doc.add_paragraph()
    run = para.add_run(text)
    
    if is_hebrew:
        run.font.name = DOCX_HEBREW_FONT
        run.font.size = Pt(FONT_SIZE_HEB)
        para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    else:
        run.font.name = DOCX_ENGLISH_FONT
        run.font.size = Pt(FONT_SIZE_ENG)
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT

# Example usage:
# create_docx_with_header("Genesis - Chapter 1", "\u05d1\u05e8\u05d0\u05e9\u05d9\u05ea \u05e4\u05e8\u05e7 \u05d0", "/path/to/folder", "output.docx")
