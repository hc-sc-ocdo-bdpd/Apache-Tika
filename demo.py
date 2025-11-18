# demo.py
from tika import parser
import json

def extract_text(file_path):
    """Extract text from any file type"""
    print(f"\n{'='*60}")
    print(f"Processing: {file_path}")
    print('='*60)
    
    # Parse the file
    parsed = parser.from_file(file_path)
    
    # Get metadata
    metadata = parsed.get("metadata", {})
    content = parsed.get("content", "")
    
    # Display metadata
    print("\n📋 METADATA:")
    print("-" * 60)
    for key, value in list(metadata.items())[:10]:  # Show first 10 metadata fields
        print(f"{key}: {value}")
    
    # Display content preview
    print("\n📄 CONTENT PREVIEW:")
    print("-" * 60)
    if content:
        preview = content.strip()[:500]  # First 500 characters
        print(preview)
        if len(content) > 500:
            print("\n... (truncated)")
    else:
        print("No content extracted")
    
    print('='*60)
    
    return {
        "metadata": metadata,
        "content": content
    }

if __name__ == "__main__":
    # Test with different file types
    test_files = [
        "test_files/sample.pdf",
        "test_files/sample.docx",
        "test_files/sample.txt"
    ]
    
    for file_path in test_files:
        try:
            result = extract_text(file_path)
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")