from file_processing import File

# Initialize a File object
file = File(r"C:\Dev\File Processing\test_files\sample.docx")

# Access metadata
print(f"File Name: {file.file_name}")
print(f"File Size: {file.size} bytes")
print(f"Owner: {file.owner}")

# Access extracted text (if applicable)
print(f"Text Content: {file.metadata.get('text', 'No text extracted')}")