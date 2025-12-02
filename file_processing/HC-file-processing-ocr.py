from file_processing import File
from file_processing_ocr.ocr_decorator import OCRDecorator
from file_processing_test_data import get_test_files_path, get_all_test_files

# Get the path to the test files directory
test_files_path = get_test_files_path()
file_path = test_files_path / 'HealthCanada.jpeg'

# Wrap the file path in a File processor
file_processor = File(file_path)

# Wrap the file processor with OCR capabilities
ocr_file = OCRDecorator(file_processor)

# Process the file and extract OCR text
ocr_file.process()

# Access the OCR text
print(ocr_file.metadata.get('ocr_text', 'No OCR text extracted'))
