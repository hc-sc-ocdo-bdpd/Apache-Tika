import os
from tika import parser, tika
from pathlib import Path

# ---------------------------
# Configure local Tesseract
# ---------------------------

# Path to your local Tesseract folder
LOCAL_TESSERACT_PATH = r"C:\Users\JOGILL\AppData\Local\Programs\Tesseract-OCR"

# Set TESSDATA_PREFIX so Tika knows where the language data is
os.environ["TESSDATA_PREFIX"] = str(Path(LOCAL_TESSERACT_PATH) / "tessdata")


# ---------------------------
# OCR & Text Extraction Function
# ---------------------------

def extract_text(file_path):
    """
    Extract text from a document or image using Apache Tika.
    If it's an image or scanned PDF, OCR will be used.
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} does not exist.")

    # Parse with Tika
    parsed = parser.from_file(str(file_path))
    text = parsed.get("content", "")

    # Clean whitespace
    if text:
        text = text.strip()
    return text

# ---------------------------
# Test Routine
# ---------------------------

if __name__ == "__main__":
    # List of files to test (can be images or documents)
    test_files = [
        "test_files/sample.pdf",
        "test_files/sample.docx",
        "test_files/sample.txt",
        "test_files/HealthCanada.jpeg",
        "test_files/sample.sqlite"
    ]

    for file_str in test_files:
        file = Path(file_str)  # convert string to Path
        print(f"\nProcessing file: {file.name}")
        try:
            text = extract_text(file)
            if text:
                print(f"✅ Extracted text (first 500 chars):\n{text[:500]}")
            else:
                print("⚠ No text could be extracted from this file.")
        except Exception as e:
            print(f"❌ Error processing {file.name}: {e}")
