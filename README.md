# Apache Tika vs OCDO File Processing Comparison

A comprehensive comparison tool for evaluating two document processing libraries: **Apache Tika** and **Health Canada's OCDO File Processing**. This project demonstrates text extraction, metadata analysis, language detection, OCR capabilities, and performance benchmarking.

---

## Features

- **Text Extraction**: Extract content from PDFs, Word documents, Excel files, images, and more
- **Metadata Analysis**: Compare metadata extraction capabilities between both libraries
- **Language Detection**: Identify document languages using fastText models
- **OCR Support**: Extract text from images using Tesseract (Tika) and built-in OCR (OCDO)
- **Performance Benchmarking**: Speed and accuracy comparisons
- **Batch Processing**: Process entire directories of files
- **Duplicate Detection**: Find duplicate files by content hash
- **Database Support**: Extract data from SQLite databases and SQL scripts
- **Docker Support**: Containerized environment for easy deployment

---

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
  - [Local Installation](#local-installation)
  - [Docker Installation](#docker-installation)
- [Usage Examples](#usage-examples)
- [Project Structure](#project-structure)
- [Available Scripts](#available-scripts)
- [Test Files](#test-files)
- [Comparison Results](#comparison-results)

---

## Requirements

### For Local Installation:
- **Python**: 3.12 or higher
- **Java**: JDK 21 or higher (for Apache Tika)
- **Tesseract OCR**: For image text extraction (optional)
- **Git**: For cloning and package installation

### For Docker Installation:
- **Docker**: Latest version
- **Docker Compose**: Latest version (optional)

---

## Installation

### Local Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/hc-sc-ocdo-bdpd/Apache-Tika.git
cd Apache-Tika
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac/Linux
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Install OCDO Packages
```bash
pip install git+https://github.com/hc-sc-ocdo-bdpd/file-processing.git
pip install git+https://github.com/hc-sc-ocdo-bdpd/file-processing-ocr.git
```

#### 5. Install Tesseract (Optional - for OCR)
**Windows:**
- Download from: https://github.com/UB-Mannheim/tesseract/wiki
- Install to default location or add to PATH

**Mac:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

#### 6. Verify Java Installation
```bash
java -version
# Should show Java 21 or higher
```

---

### Docker Installation

#### Option 1: Using docker-compose (Recommended)
```bash
# Clone repository
git clone https://github.com/hc-sc-ocdo-bdpd/Apache-Tika.git
cd Apache-Tika

# Build and run
docker-compose up --build

# Run in detached mode
docker-compose up -d
```

#### Option 2: Using Docker directly
```bash
# Build image
docker build -t apache-tika-comparison .

# Run container
docker run apache-tika-comparison

# Run with your own test files
docker run -v "/path/to/your/files:/app/test_files" apache-tika-comparison

# Run with output directory mounted
docker run -v "/path/to/output:/app/output" apache-tika-comparison
```

---

## Usage Examples

### Basic Text Extraction (Tika)
```python
from tika import parser

# Extract text from any file
parsed = parser.from_file("test_files/sample.pdf")
content = parsed.get("content", "")
metadata = parsed.get("metadata", {})

print(f"Content: {content[:200]}")  # First 200 chars
print(f"Metadata fields: {len(metadata)}")
```

### Basic Text Extraction (OCDO)
```python
from file_processing import File

# Initialize File object
file = File("test_files/sample.pdf")

# Access content and metadata
text = file.metadata.get('text', 'No text extracted')
print(f"File Name: {file.file_name}")
print(f"File Size: {file.size} bytes")
print(f"Content: {text[:200]}")
```

### Language Detection (Tika)
```python
from file_processing.Tika_language_detection import detect_file_language

result = detect_file_language("test_files/sample.pdf")
if result["fasttext_predictions"]:
    top = result["fasttext_predictions"][0]
    print(f"Language: {top['lang_name']} ({top['lang']})")
    print(f"Confidence: {top['prob']:.2%}")
```

### Language Detection (OCDO)
```python
from file_processing.HC_language_detection import detect_file_language

result = detect_file_language("test_files/sample.pdf")
if result["fasttext_predictions"]:
    top = result["fasttext_predictions"][0]
    print(f"Language: {top['lang_name']} ({top['lang']})")
    print(f"Confidence: {top['prob']:.2%}")
```

### OCR Text Extraction (Tika/Tesseract)
```python
from file_processing.tika_ocr import *

# Automatically detects Tesseract installation
image_path = "test_files/sample_image.jpeg"
im = Image.open(image_path)
text = pytesseract.image_to_string(im, lang='eng')
print(text)
```

### OCR Text Extraction (OCDO)
```python
from file_processing import File
from file_processing_ocr.ocr_decorator import OCRDecorator

# Wrap file with OCR capabilities
file_processor = File("test_files/sample_image.jpeg")
ocr_file = OCRDecorator(file_processor)
ocr_file.process()

# Access OCR text
print(ocr_file.metadata.get('ocr_text', 'No OCR text'))
```

### Batch Processing
```python
from file_processing.batch_processor import process_directory

# Process all files in directory
results = process_directory("test_files", output_csv="results.csv")
print(f"Processed {len(results)} files")
```

### Find Duplicate Files
```python
from file_processing.duplicate_detector import FileDuplicateDetector

detector = FileDuplicateDetector("test_files")
detector.run_analysis()
```

---

## Project Structure

```
Apache-Tika/
├── file_processing/
│   ├── HC-demo.py                    # OCDO basic demo
│   ├── HC_language_detection.py      # OCDO language detection
│   ├── HC_ocr.py                     # OCDO OCR demo
│   ├── Tika_demo.py                  # Tika basic demo
│   ├── Tika_detect_filetype.py       # Tika MIME type detection
│   ├── Tika_language_detection.py    # Tika language detection
│   ├── Tika_metadata_extractor.py    # Tika metadata extraction
│   ├── tika_ocr.py                   # Tika OCR with Tesseract
│   ├── Metadata_tests.py             # Comprehensive comparison tests
│   ├── batch_processor.py            # Batch file processing
│   ├── duplicate_detector.py         # Find duplicate files
│   └── demo_db.py                    # Database/SQL processing
├── test_files/                       # Sample documents for testing
│   ├── sample.pdf
│   ├── sample.docx
│   ├── sample.txt
│   ├── sample.sqlite
│   ├── sample_image.jpeg
│   ├── HealthCanada.jpeg
│   ├── Special Characters.txt
│   ├── Texte en Français.txt
│   └── Mathematical and Scientific Equations.txt
├── outputs/                          # Generated output files
│   ├── extraction_results.csv
│   ├── metadata.json
│   └── comparison_test_results_*.json
├── models/                           # Downloaded language models
│   └── lid.176.ftz                   # fastText language model (auto-downloaded)
├── sample_tests/                     # Unit tests
│   └── test_language_detection.py
├── requirements.txt                  # Python dependencies
├── Dockerfile                        # Docker configuration
├── docker-compose.yml                # Docker Compose configuration
├── .dockerignore                     # Docker ignore patterns
├── .gitignore                        # Git ignore patterns
└── README.md                         # This file
```

---

## Available Scripts

### Core Demos
| Script | Description |
|--------|-------------|
| `Tika_demo.py` | Basic Apache Tika text extraction demo |
| `HC-demo.py` | Basic OCDO File Processing demo |
| `Metadata_tests.py` | Comprehensive comparison test suite |

### Specialized Processing
| Script | Description |
|--------|-------------|
| `Tika_detect_filetype.py` | Detect MIME types using Tika |
| `Tika_language_detection.py` | Language detection with Tika + fastText |
| `HC_language_detection.py` | Language detection with OCDO + fastText |
| `Tika_metadata_extractor.py` | Detailed metadata extraction |
| `tika_ocr.py` | OCR with Tesseract (Tika) |
| `HC_ocr.py` | OCR with OCDO built-in support |

### Batch Operations
| Script | Description |
|--------|-------------|
| `batch_processor.py` | Process entire directories |
| `duplicate_detector.py` | Find duplicate files by hash |
| `demo_db.py` | Process SQLite/SQL files |

---

## est Files

The `test_files/` directory contains diverse sample documents:

- **PDF**: `sample.pdf` - Standard PDF document
- **Word**: `sample.docx` - Microsoft Word document
- **Text**: `sample.txt`, `sample - Copy.txt` - Plain text files
- **Database**: `sample.sqlite` - SQLite database
- **Images**: `sample_image.jpeg`, `HealthCanada.jpeg` - OCR test images
- **Special Characters**: `Special Characters.txt` - Unicode, math symbols, etc.
- **French Text**: `Texte en Français.txt` - Language detection testing
- **Equations**: `Mathematical and Scientific Equations.txt` - Scientific notation

---

## Comparison Results

### Strengths by Tool

**Apache Tika:**
- Supports 1000+ file formats
- Extensive metadata extraction
- Strong community support
- Requires Java runtime
- Slower startup time

**OCDO File Processing:**
- Pure Python implementation
- No Java dependency
- Faster for common formats
- Simpler setup
- Built-in OCR support
- Fewer supported formats
- Less metadata detail

### Performance Benchmarks
Run `Metadata_tests.py` to generate detailed comparison reports including:
- Text extraction accuracy
- Metadata completeness
- Special character handling
- Large file performance
- Error handling

Results are saved to `outputs/comparison_test_results_*.json`

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/Tika`)
3. Commit your changes (`git commit -m 'Iniitial commit'`)
4. Push to the branch (`git push origin feature/Tika`)
5. Open a Pull Request

### Development Setup
```bash
# Install dev dependencies
pip install -r requirements.txt

# Run tests
python -m pytest sample_tests/

# Format code
black file_processing/
```

---

## Contact

For questions or support, please open an issue on GitHub or contact the OCDO team at Health Canada.

---