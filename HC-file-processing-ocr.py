from file_processing import File
from file_processing_ocr.ocr_decorator import OCRDecorator

# Initialize a File object
file = File('path/to/your/image_or_pdf_file.pdf')

# Wrap the file processor with OCR capabilities
ocr_file = OCRDecorator(file)

# Process the file and extract OCR text
ocr_file.process()

# Access the OCR text
print(ocr_file.metadata.get('ocr_text', 'No OCR text extracted'))