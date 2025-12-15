import os
import sqlite3
from tika import parser
import json

def extract_text(file_path):
    print(f"\n{'='*60}")
    print(f"Processing: {file_path}")
    print('='*60)

    # Handle SQLite separately
    if file_path.endswith(".sqlite"):
        try:
            conn = sqlite3.connect(file_path)
            cursor = conn.cursor()

            # Get tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]

            print("\n📋 TABLES FOUND:")
            print("-" * 60)
            print(tables)

            # Preview first table
            if tables:
                table = tables[0]
                cursor.execute(f"SELECT * FROM {table} LIMIT 5")
                rows = cursor.fetchall()

                print(f"\n📄 PREVIEW FROM TABLE '{table}':")
                print("-" * 60)
                for row in rows:
                    print(row)
            else:
                print("No tables found")

            conn.close()
        except Exception as e:
            print(f"Error reading sqlite file: {e}")

        print("=" * 60)
        return
    else:
        print(file_path, "could not be parsed. Please try again with a .sqlite file!")


if __name__ == "__main__":
    test_files = [
        "test_files/sample.pdf",
        "test_files/sample.docx",
        "test_files/sample.txt",
        "test_files/sample.sqlite"
    ]

    for file_path in test_files:
        extract_text(file_path)
