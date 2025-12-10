# metadata_extractor.py
from tika import parser
import json
import os
from datetime import datetime

def extract_detailed_metadata(file_path):
    """Extract and organize detailed metadata"""
    parsed = parser.from_file(file_path)
    metadata = parsed.get("metadata", {})
    
    # Organize metadata by category
    organized = {
        "basic_info": {},
        "document_properties": {},
        "technical_details": {},
        "dates": {},
        "author_info": {}
    }
    
    # Categorize metadata
    for key, value in metadata.items():
        key_lower = key.lower()
        
        if "date" in key_lower or "time" in key_lower:
            organized["dates"][key] = value
        elif "author" in key_lower or "creator" in key_lower:
            organized["author_info"][key] = value
        elif "type" in key_lower or "format" in key_lower:
            organized["basic_info"][key] = value
        elif "page" in key_lower or "word" in key_lower or "character" in key_lower:
            organized["document_properties"][key] = value
        else:
            organized["technical_details"][key] = value
    
    # Display organized metadata
    print(f"\n{'='*70}")
    print(f"DETAILED METADATA: {file_path}")
    print('='*70)
    
    for category, items in organized.items():
        if items:
            print(f"\n📌 {category.replace('_', ' ').upper()}:")
            print('-'*70)
            for k, v in items.items():
                print(f"  {k}: {v}")
    
    return organized

def save_metadata_to_json(file_path, output_file="metadata.json"):
    """Save metadata to JSON file"""
    metadata = extract_detailed_metadata(file_path)
    
    # Build full output path
    output_path = os.path.join("outputs", output_file)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Metadata saved to {output_file}")

if __name__ == "__main__":
    file_path = "test_files/sample.pdf"
    save_metadata_to_json(file_path)