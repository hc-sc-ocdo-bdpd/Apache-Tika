# detect_filetype.py
from tika import detector
import os

def detect_file_type(file_path):
    """Detect MIME type of a file"""
    if not os.path.exists(file_path):
        return f"File not found: {file_path}"
    
    mime_type = detector.from_file(file_path)
    
    print(f"\n📁 File: {os.path.basename(file_path)}")
    print(f"🔍 MIME Type: {mime_type}")
    
    return mime_type

if __name__ == "__main__":
    files = [
        "test_files/sample.pdf",
        "test_files/sample.docx",
        "test_files/sample.txt",
        "test_files/sample.mp3"
    ]
    
    print("="*60)
    print("FILE TYPE DETECTION")
    print("="*60)
    
    for file in files:
        try:
            detect_file_type(file)
        except Exception as e:
            print(f"Error: {e}")