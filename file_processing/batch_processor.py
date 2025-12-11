# batch_processor.py
import warnings
warnings.filterwarnings('ignore')

from tika import parser
import os
import csv
from pathlib import Path

def process_directory(directory_path, output_csv="extraction_results.csv"):
    """Process all files in a directory and save results to CSV"""
    
    results = []
    
    print(f"\nScanning directory: {directory_path}")
    print("="*70)
    
    # Get all files in directory
    for root, dirs, files in os.walk(directory_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            
            try:
                
                # Parse file
                parsed = parser.from_file(file_path)
                metadata = parsed.get("metadata", {})
                content = parsed.get("content", "")
                
                # Extract key information
                result = {
                    "filename": filename,
                    "path": file_path,
                    "mime_type": metadata.get("Content-Type", "Unknown"),
                    "file_size": os.path.getsize(file_path),
                    "word_count": len(content.split()) if content else 0,
                    "char_count": len(content) if content else 0,
                    "author": metadata.get("Author", "Unknown"),
                    "created": metadata.get("Creation-Date", "Unknown")
                }
                
                results.append(result)
                
            except Exception as e:
                print(f"  Error: {str(e)}")
                results.append({
                    "filename": filename,
                    "path": file_path,
                    "error": str(e)
                })

    # Save to CSV
    if results:
        # Ensure the output directory exists
        os.makedirs("outputs", exist_ok=True)

        # Build the output path inside the folder
        output_path = os.path.join("outputs", output_csv)

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
    
        print(f"\nResults saved to {output_path}")
        print(f"Processed {len(results)} files\n")
    
    return results

if __name__ == "__main__":
    process_directory("test_files")