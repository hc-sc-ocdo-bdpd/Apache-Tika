from PIL import Image
import pytesseract
import sys
import os
import getpass
from pathlib import Path
from file_processing_test_data import get_test_files_path, get_all_test_files

# Get the path to the test files directory
test_files_path = get_test_files_path()
image_path = test_files_path / 'ocr_text.jpg'

# Image path
#image_path = r"test_files\\HealthCanada.jpeg"

# Tesseract auto-detection
error_message = "Tesseract is not installed or cannot be found. Please install Tesseract OCR."

try:
    pytesseract.get_tesseract_version()
except:
    if sys.platform == 'win32':
        possible_paths = [
            "C:/Program Files/Tesseract-OCR/tesseract.exe",
            "C:/Program Files (x86)/Tesseract-OCR/tesseract.exe",
            Path('C:/Users') / getpass.getuser() / 'AppData/Local/Programs/Tesseract-OCR/tesseract.exe'
        ]
        for path in possible_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                break
        else:
            raise Exception(error_message)
    elif sys.platform == 'linux':
        linux_path = '/usr/bin/tesseract'
        if not os.path.exists(linux_path):
            raise Exception(error_message)
        pytesseract.pytesseract.tesseract_cmd = linux_path
    elif sys.platform == 'darwin':
        macos_path = '/usr/local/bin/tesseract'
        if not os.path.exists(macos_path):
            raise Exception(error_message)
        pytesseract.pytesseract.tesseract_cmd = macos_path
    else:
        raise Exception(error_message)

print("\nPytesseract OCR Test")
print("="*50)

# Check if image exists
if not os.path.exists(image_path):
    print(f"Error: Image not found: {image_path}")
    print(f"\nCurrent directory: {os.getcwd()}")
    exit()

# Extract text
try:
    print(f"Processing: {image_path}")

    im = Image.open(image_path)
    text = pytesseract.image_to_string(im, lang='eng')
    
    print("="*50)
    print("EXTRACTED TEXT:")
    print("="*50)
    print(text)
    print("="*50)
    print(f"\nWords found: {len(text.split())}")
    
except Exception as e:
    print(f"Error: {e}")