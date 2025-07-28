import xml.etree.ElementTree as ET
from pathlib import Path
import os

# Masoretic Text -  https://tanach.us/Tanach.xml
# The Unicode/XML Leningrad Codex (UXLC) is a transcription of the Leningrad Codex (LC) 
# into a modern computer format (Unicode, XML). The UXLC text is a fork of the Groves Centers
# Westminster Leningrad Codex [ WLC 4.20, Revision 1950 of 2016-01-25 ]. The text is updated 
# semi-annually to better match the LC from reader suggestions through a formal and automated 
# process; more than a thousand changes have been made to date. The Hebrew text is version 
# controlled to provide a fixed reference for derived work. 
# The current release is UXLC 2.3 (27.4) of 31 March 2025 06:24. See the Technical page for further details.

# -------------------------
# Bootstrapping Dependencies
# -------------------------
# Get the absolute path to the *parent* of the current file's directory
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

# Folders in the root directory that contain modules
DEPENDENCY_DIRS = [
    PROJECT_ROOT / "utils"
]

# -------------------------
# Import Dependencies
# -------------------------
import utils                      # utils directory

def get_verse(filepath, filename, chapter, verse):
    """
    Returns the full verse as a list of words from the given XML Torah book.
    
    Args:
        filepath (str): Directory where the XML file is located.
        filename (str): Name of the XML file (e.g., 'Genesis.xml').
        chapter (int): Chapter number.
        verse (int): Verse number.

    Returns:
        List[str]: List of Hebrew words in the verse.
    """
    full_path = os.path.join(filepath, filename)
    tree = ET.parse(full_path)
    root = tree.getroot()

    # Find the verse node
    verse_node = root.find(f".//c[@n='{chapter}']/v[@n='{verse}']")
    if verse_node is None:
        raise ValueError(f"Verse not found: {chapter}:{verse} in {filename}")

    return [w.text for w in verse_node.findall("w")]

def get_word_in_verse(filepath, filename, chapter, verse, word_index):
    """
    Returns the N-th word in a specified verse (1-based index).

    Args:
        filepath (str): Directory where the XML file is located.
        filename (str): Name of the XML file (e.g., 'Genesis.xml').
        chapter (int): Chapter number.
        verse (int): Verse number.
        word_index (int): The word position in the verse (1-based).

    Returns:
        str: The N-th word in the verse.
    """
    words = get_verse(filepath, filename, chapter, verse)
    if word_index < 1 or word_index > len(words):
        raise IndexError(f"Word index {word_index} out of range for verse {chapter}:{verse}.")
    return words[word_index - 1]

def example_usage(filepath, filename, chapter, verse, word_index):

    chapter = 1
    verse = 1
    word_index = 3

    print("Full verse:")
    words = get_verse(filepath, filename, chapter, verse)
    print(" ".join(words))

    print(f"\nWord {word_index} in verse:")
    word = get_word_in_verse(filepath, filename, chapter, verse, word_index)
    print(word)

    # To test:
    # example_usage()
