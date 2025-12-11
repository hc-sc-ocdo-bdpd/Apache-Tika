#!/usr/bin/env python3
"""
File Duplicate Detection - Using Apache Tika
Compares files using byte comparison
"""

import warnings
warnings.filterwarnings('ignore')

from tika import parser as tika_parser
import os
from pathlib import Path
from collections import defaultdict
import hashlib


class FileDuplicateDetector:
    """Detect duplicate files by comparing byte content"""
    
    def __init__(self, folder_path="test_files"):
        self.folder_path = Path(folder_path)
        self.results = {
            "duplicates": [],
            "unique_files": [],
            "errors": []
        }
    
    def get_file_hash(self, filepath):
        """Generate hash from file bytes for comparison"""
        hasher = hashlib.md5()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    
    def get_file_size(self, filepath):
        """Get file size in bytes"""
        return os.path.getsize(filepath)
    
    def find_duplicates_by_size(self):
        """Find potential duplicates by file size"""
        size_groups = defaultdict(list)
        
        for filepath in self.folder_path.iterdir():
            if filepath.is_file():
                size = self.get_file_size(filepath)
                size_groups[size].append(filepath)
        
        potential_duplicates = {size: files for size, files in size_groups.items() if len(files) > 1}
        return potential_duplicates
    
    def find_duplicates_by_hash(self, size_groups):
        """Find actual duplicates by comparing file hashes"""
        all_duplicates = []
        
        for size, files in size_groups.items():
            hash_groups = defaultdict(list)
            for filepath in files:
                file_hash = self.get_file_hash(filepath)
                hash_groups[file_hash].append(filepath)
            
            for file_hash, duplicate_files in hash_groups.items():
                if len(duplicate_files) > 1:
                    duplicate_group = {
                        "hash": file_hash,
                        "size_bytes": size,
                        "files": [str(f) for f in duplicate_files]
                    }
                    all_duplicates.append(duplicate_group)
        
        return all_duplicates
    
    def run_analysis(self):
        """Run complete duplicate detection analysis"""
        print(f"\nScanning folder: {self.folder_path}")
        
        if not self.folder_path.exists():
            print(f"❌ Error: Folder not found: {self.folder_path}")
            return
        
        # Step 1: Group by size
        size_groups = self.find_duplicates_by_size()
        
        if not size_groups:
            print("\nNo duplicates found - all files are unique\n")
            return
        
        # Step 2: Compare by hash
        duplicate_groups = self.find_duplicates_by_hash(size_groups)
        
        if not duplicate_groups:
            print("\nNo duplicates found - files with same size have different content\n")
            return
        
        # Final summary
        self.print_summary(duplicate_groups)
    
    def print_summary(self, duplicate_groups):
        """Print final summary"""
        print("\n" + "="*70)
        print("DUPLICATE FILES DETECTED")
        print("="*70)
        
        total_duplicates = sum(len(group['files']) for group in duplicate_groups)
        total_groups = len(duplicate_groups)
        
        print(f"\n📊 Statistics:")
        print(f"  Duplicate groups found: {total_groups}")
        print(f"  Total duplicate files: {total_duplicates}")
        
        print(f"\n📁 Duplicate Groups:")
        for idx, group in enumerate(duplicate_groups, 1):
            print(f"\n  Group {idx}:")
            print(f"    Files: {len(group['files'])}")
            print(f"    Size: {group['size_bytes']} bytes")
            print(f"    Hash: {group['hash'][:16]}...")
            for filepath in group['files']:
                print(f"      - {Path(filepath).name}")
        
        # Calculate space wasted
        wasted_space = sum((len(group['files']) - 1) * group['size_bytes'] 
                          for group in duplicate_groups)
        print(f"\nSpace wasted by duplicates: {wasted_space:,} bytes ({wasted_space/1024:.2f} KB)")
        print()


def main():
    """Main execution"""
    test_dir = Path("test_files")
    
    if not test_dir.exists() or len(list(test_dir.iterdir())) == 0:
        print("\n❌ No files found in 'test_files' folder")
        print("Please add files to the folder and run again.\n")
        return
    
    detector = FileDuplicateDetector("test_files")
    detector.run_analysis()


if __name__ == "__main__":
    main()