import utils

from docx import Document
from docx.shared import Pt
from docx.shared import Inches
import re
import os
from docx.shared import RGBColor

def get_full_filename(partial_filename, search_dir):
    """
    Returns the full filename (without path) that matches the given partial filename within the specified directory.
    
    Args:
        partial_filename (str): Partial filename to search for.
        search_dir (str): Directory path to search in.
    
    Returns:
        str: Full filename if a match is found, else None.
    """
    try:
        for root, dirs, files in os.walk(search_dir):
            for file in files:
                if partial_filename in file:
                    return file  # Return just the filename
        print("get_full_filename function did NOT return a value")
        return None  # Return None if no match is found
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def remove_second_colon(para_text, paragraph):
    # This regex will match ": (כח):" and remove the second colon at the end
    para_text = re.sub(r"(:\((\D+)\)‪):", r" (\2)‪:", para_text)
    
    # Now we return the modified paragraph with the second colon removed
    new_paragraph = paragraph
    new_paragraph.clear()  # Clear previous runs
    new_paragraph.add_run(para_text)  # Add the modified text without the second colon
    
    return new_paragraph

def weave_torah_files(parasha_name, hebrew_file_path, english_file_path, output_file_path):
    """
    Combine Hebrew and English texts from Word documents into a single Word file.
    Preserve original formatting of Hebrew and English documents.

    Args:
        hebrew_file_path (str): Path to the Hebrew Word document.
        english_file_path (str): Path to the English Word document.
        output_file_path (str): Path for the combined Word document output.
    """
    # Load Hebrew and English Word files
    hebrew_doc = Document(hebrew_file_path)
    english_doc = Document(english_file_path)

    # Prepare the output Word document
    output_doc = Document()

    # Set narrow margins
    section = output_doc.sections[0]
    section.left_margin = Inches(0.5)
    section.right_margin = Inches(0.5)
    section.top_margin = Inches(0.5)
    section.bottom_margin = Inches(0.5)

    hebrew_index = 0
    english_index = 0

    # Process paragraphs and align Hebrew and English text
    while hebrew_index < len(hebrew_doc.paragraphs):
        # Add the Hebrew paragraph with formatting
        hebrew_paragraph = hebrew_doc.paragraphs[hebrew_index]
        output_paragraph = output_doc.add_paragraph()

        # Set the Hebrew font and size
        for run in hebrew_paragraph.runs:
            run_new = output_paragraph.add_run(run.text)
            run_new.bold = run.bold
            run_new.italic = run.italic
            run_new.underline = run.underline
            run_new.font.name = utils.DOCX_HEBREW_FONT
            run_new.font.size = Pt(utils.FONT_SIZE_HEB)

        # Align Hebrew text to the right (Right-to-left alignment)
        output_paragraph.alignment = 1
        output_paragraph.paragraph_format.bidi = True

        hebrew_index += 1

        # Add the corresponding English paragraph with formatting
        if english_index < len(english_doc.paragraphs):
            english_paragraph = english_doc.paragraphs[english_index]
            output_paragraph = output_doc.add_paragraph()

            # Set the English font and size
            for run in english_paragraph.runs:
                run_new = output_paragraph.add_run(run.text)
                run_new.bold = run.bold
                run_new.italic = run.italic
                run_new.underline = run.underline
                run_new.font.name = utils.DOCX_ENGLISH_FONT
                run_new.font.size = Pt(utils.FONT_SIZE_ENG)

            # Align English text to the left (Left-to-right alignment)
            output_paragraph.alignment = 0
            output_paragraph.paragraph_format.bidi = False

            english_index += 1

    # Check if Hebrew paragraphs exist and prepare the first line for the file name
    if hebrew_doc.paragraphs:
        first_line_hebrew = hebrew_doc.paragraphs[0].text.strip()
        safe_first_line_hebrew = "".join([c if c.isalnum() or c.isspace() else "_" for c in first_line_hebrew])
    else:
        safe_first_line_hebrew = "combined"

    # Ensure the output path exists
    os.makedirs(output_file_path, exist_ok=True)

    # Define the output file path using the cleaned Hebrew text
    docx_name = f"{parasha_name}_{safe_first_line_hebrew}.docx"
    docx_name = clean_hebrew_filename(docx_name)
    final_path_result = os.path.join(output_file_path, docx_name)

    # Remove the existing file if it already exists
    if os.path.exists(final_path_result):
        os.remove(final_path_result)
        print(f"Existing file found and removed: {final_path_result}")

    # Save the combined document
    output_doc.save(final_path_result)
    print(f"Combined document saved as: {final_path_result}")
    
    return final_path_result

def add_notes_to_verses(file_path):
    """
    Adds a notes section to each verse in a .docx file while preserving formatting 
    and replaces the original file. The output file has narrow margins.

    Args:
        file_path (str): Path to the .docx file to process.
    """
    # Load the document
    doc = Document(file_path)
    
    # Extract the header (assumes it's the first paragraph with the chapter name)
    header_text = None
    for para in doc.paragraphs:
        if "Chapter" in para.text:
            header_text = para.text.strip()
            break
    
    if not header_text:
        raise ValueError("No header containing 'Chapter' found in the document.")
    
    # Create a new document to rewrite the content
    new_doc = Document()

    # Set narrow margins for the new document
    section = new_doc.sections[0]
    section.left_margin = Inches(0.5)   # 0.5 inches left margin
    section.right_margin = Inches(0.5)  # 0.5 inches right margin
    section.top_margin = Inches(0.5)    # 0.5 inches top margin
    section.bottom_margin = Inches(0.5) # 0.5 inches bottom margin

    for para in doc.paragraphs:
        para_text = para.text.strip()
        
        # Copy the paragraph while preserving formatting
        new_paragraph = new_doc.add_paragraph()
        new_paragraph.alignment = para.alignment  # Preserve alignment
        for run in para.runs:
            new_run = new_paragraph.add_run(run.text)
            new_run.bold = run.bold
            new_run.italic = run.italic
            new_run.underline = run.underline
            new_run.font.name = run.font.name
            new_run.font.size = run.font.size
            new_run.font.color.rgb = run.font.color.rgb
        
        # Check if the paragraph is a verse
        if para_text.startswith("Verse"):
            # Extract the verse number using regex
            match = re.match(r"Verse (\d+)", para_text)
            if match:
                verse_number = match.group(1)
                # Add the notes paragraph for the verse
                notes_paragraph = new_doc.add_paragraph()
                notes = f"[notes]( {header_text} Verse {verse_number} )[end_notes]"
                notes_paragraph.alignment = 0  # Align notes to the left (customize if needed)
                notes_run = notes_paragraph.add_run(notes)
                # Optional: Style the notes text (customize if needed)
                notes_run.italic = True
                notes_run.font.color.rgb = RGBColor(211, 211, 211)  # Set the notes text to light grey
    
    # Delete the original file if it exists
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Existing file deleted: {file_path}")
    
    # Save the reformatted content back to the original file
    new_doc.save(file_path)
    print(f"Formatted document saved as: {file_path}")

def clean_hebrew_filename(filename):
    """
    Clean a Hebrew filename string to a consistent format.
    
    Args:
        filename (str): The original filename string.
        
    Returns:
        str: The cleaned filename string.
    """
    # Replace spaces with underscores
    cleaned_string = re.sub(r"\s+", "_", filename)
    # Replace multiple underscores with a single underscore
    cleaned_string = re.sub(r"_{2,}", "_", cleaned_string)
    # Ensure proper format for "Chapter"
    cleaned_string = re.sub(r"_Chapter_", " Chapter_", cleaned_string)
    # Ensure proper format for "Verses"
    cleaned_string = re.sub(r"_Verses_", " Verses_", cleaned_string)
    # Remove extra underscores after "Chapter" and "Verses"
    cleaned_string = re.sub(r"(?<=Chapter)_+", "_", cleaned_string)
    cleaned_string = re.sub(r"(?<=Verses)_+", "_", cleaned_string)
    # Remove trailing underscores
    cleaned_string = re.sub(r"_+$", "", cleaned_string)
    # Handle dangling underscores before ".docx"
    cleaned_string = re.sub(r"_\.docx$", ".docx", cleaned_string)
    
    return cleaned_string

def format_docx_file(file_path):
    """
    Formats the content of a .docx file, applies consistent formatting while preserving
    the content as-is, and replaces the original file.

    Args:
        file_path (str): Path to the .docx file to process.
    """
    # Load the document
    doc = Document(file_path)
    
    # Create a new document to rewrite the content
    new_doc = Document()

    # Set narrow margins for the new document
    section = new_doc.sections[0]
    section.left_margin = Inches(0.5)   # 0.5 inches left margin
    section.right_margin = Inches(0.5)  # 0.5 inches right margin
    section.top_margin = Inches(0.5)    # 0.5 inches top margin
    section.bottom_margin = Inches(0.5) # 0.5 inches bottom margin

    # Regex to detect Hebrew characters
    hebrew_range = r"[\u0590-\u05FF]"

    for para in doc.paragraphs:
        para_text = para.text.strip()
        
        # Create a new paragraph in the formatted document
        new_paragraph = new_doc.add_paragraph()
        new_paragraph.alignment = para.alignment  # Preserve alignment
        
        # Loop through the runs in the original paragraph and reapply formatting
        for run in para.runs:
            new_run = new_paragraph.add_run(run.text)
            
            # Preserve original run formatting
            new_run.bold = run.bold
            new_run.italic = run.italic
            new_run.underline = run.underline
            new_run.font.color.rgb = run.font.color.rgb

            # Apply consistent font and size based on content
            if re.search(hebrew_range, run.text):  # If the text contains Hebrew characters
                new_run.font.name = utils.DOCX_HEBREW_FONT
                new_run.font.size = Pt(utils.FONT_SIZE_HEB)
            else:  # Non-Hebrew text
                new_run.font.name = utils.DOCX_ENGLISH_FONT
                new_run.font.size = Pt(utils.FONT_SIZE_ENG)

    # Delete the original file if it exists
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Existing file deleted: {file_path}")
    
    # Save the reformatted content back to the original file
    new_doc.save(file_path)
    print(f"Formatted document saved as: {file_path}")

if __name__ == "__main__":

    # Ask the user whether to add notes to verses
    add_notes = input("\nWould you like to add notes to the verses? (yes/no): ").strip().lower()

    eng_folder_path = utils.load_tanakh_path(utils.ENG_DOCX_FOLDER)
    heb_folder_path = utils.load_tanakh_path(utils.HEB_DOCX_FOLDER)
    output_folder_path = utils.load_tanakh_path(utils.OUTPUT_DOCX_FOLDER)
    hebrew_file_path = "hebrew_text.docx"
    english_file_path = "english_text.docx"
    output_file_path = "combined_output.docx"

    #################################
    # Step 1 : Get the paths
    #################################

    #################################
    # Eng paths
    #################################
    # utils.PARASHOT_NOW is a string
    now_parasha_path = utils.load_data(utils.PARASHOT_NOW, return_path_only=True)
    parasha_details = utils.get_parasha_details_heb(now_parasha_path)
    if parasha_details:
        # Extract the first parasha's details into individual variables
        first_parasha = parasha_details[0]
        parasha_name = first_parasha["parasha_name"]
        book_name = first_parasha["book_name"]
        start_chapter = first_parasha["start_chapter"]
        start_verse = first_parasha["start_verse"]
        end_chapter = first_parasha["end_chapter"]
        end_verse = first_parasha["end_verse"]
        tanakh_section = first_parasha["tanakh_section"]

        # Print the details
        print(f"Parasha Name:\t\t\t {parasha_name}")
        print(f"Book Name:\t\t\t {book_name}")
        print(f"Start Chapter:\t\t\t {start_chapter}, Start Verse: {start_verse}")
        print(f"End Chapter:\t\t\t {end_chapter}, End Verse: {end_verse}")
        print(f"Tanakh Section:\t\t\t {tanakh_section}")
    else:
        print("No parasha details found.")

    # Get folder paths for Eng
    eng_filename = f"{book_name}_{start_chapter}.docx"
    eng_folder_path = utils.load_tanakh_path(utils.ENG_DOCX_FOLDER)
    eng_folder_path = os.path.join(eng_folder_path, parasha_name)
    print(f"\nEnglish filename:\t {eng_filename}")
    print(f"English folder name:\t {eng_folder_path}")

    #################################
    # Heb paths
    #################################
    now_parasha_path_heb = utils.load_data(utils.PARASHOT_NOW_HEB, return_path_only=True)
    parasha_details_heb = utils.get_parasha_details_heb2(now_parasha_path_heb)
    if parasha_details_heb:
	    # Extract the first parasha's details into individual variables
	    first_parasha_heb = parasha_details_heb[0]
	    parasha_name_heb = first_parasha_heb["parasha_name"]
	    book_name_heb = first_parasha_heb["book_name"]
	    start_chapter_heb = first_parasha_heb["start_chapter"]
	    start_verse_heb = first_parasha_heb["start_verse"]
	    end_chapter_heb = first_parasha_heb["end_chapter"]
	    end_verse_heb = first_parasha_heb["end_verse"]
	    tanakh_section_heb = first_parasha_heb["tanakh_section"]
	    num_parasha = first_parasha_heb["num_parasha"]  # Fix: Use first_parasha_heb

	    # Print the details
	    print(f"\nParasha Name Heb:\t\t\t {parasha_name_heb}")
	    print(f"Book Name Heb:\t\t\t\t {book_name_heb}")
	    print(f"Start Chapter Heb:\t\t\t {start_chapter_heb}, Start Verse: {start_verse_heb}")
	    print(f"End Chapter Heb:\t\t\t {end_chapter_heb}, End Verse: {end_verse_heb}")
	    print(f"Tanakh Section Heb:\t\t\t {tanakh_section_heb}")
	    print(f"num_parasha:\t\t\t {num_parasha}")
    else:
	    print("No parasha details found.")


    # Get folder paths for Heb
    heb_filename = f"{book_name_heb}_CH_{start_chapter}"
    heb_folder_path = utils.load_tanakh_path(utils.HEB_DOCX_FOLDER)
    end_heb_path_name = str(num_parasha) + "_" + parasha_name
    heb_folder_path = os.path.join(heb_folder_path, end_heb_path_name)
    # Get the full filename from the partial filename
    heb_filename = get_full_filename(heb_filename, heb_folder_path)
    print(f"Hebrew filename:\t {heb_filename}")
    print(f"Hebrew folder name:\t {heb_folder_path}")

    ###################################################
    # Step 2: weave heb_file and english_file into one
    ###################################################

    # Weave files together then save the document
    bug_baindaid_eng_filename = eng_filename + ".docx"
    english_file = os.path.join(eng_folder_path, bug_baindaid_eng_filename)
    heb_file = os.path.join(heb_folder_path, heb_filename)
    print(f"\nfinal Hebrew filename:\t {heb_file}")
    print(f"final Eng folder name:\t {english_file}")
    final_output = weave_torah_files(parasha_name_heb, heb_file, english_file, output_folder_path)

    ###################################################
    # Step 3: Add notes if needed
    ###################################################

    # Add notes if needed, then save the document
    if add_notes == 'yes':
        add_notes_to_verses(final_output)
        print("\nNotes have been added to the verses.")

    # Get an instance of the document
    print(f"final_output3:\t {final_output}")
    doc = Document(final_output)

    ###################################################
    # Step 4: Processing - remove colon
    ###################################################

    # Iterate over paragraphs and remove second Heb verse number colon
    for para in doc.paragraphs:
        para_text = para.text.strip()
        new_paragraph = remove_second_colon(para_text, para)

    print(f"final_output:\t {final_output}")

    # Save the modified document
    doc.save(final_output)

    ###################################################
    # Step 5: Processing - final output
    ###################################################

    # Format the document (you can add your specific formatting logic here)
    format_docx_file(final_output)
    print(f"\nDocument saved and formatted: {final_output}")
