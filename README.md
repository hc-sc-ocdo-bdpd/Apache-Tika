# Apache Tika vs OCDO File Processing Comparison

Comparing two document processing libraries: **Apache Tika** (industry-standard) and **Health Canada's OCDO File Processing** (Python-native). Demonstrates text extraction, metadata analysis, and performance benchmarking.

---

## Features

- Text extraction from PDFs, Word docs, Excel, images
- Metadata comparison
- Performance benchmarking
- Side-by-side output comparison
- Docker support

---

## Quick Start

### Docker
```bash
# Clone repository
git clone https://github.com/hc-sc-ocdo-bdpd/Apache-Tika.git
cd Apache Tika

# Build and run
docker build -t Apache-Tika .
docker run Apache Tika

# With your own files
docker run -v "/path/to/files:/app/test_files" file-processing
```

### Local Installation
```bash
# Prerequisites: Python 3.12+, Java 21+

# Setup
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Install
pip install -r requirements.txt

# Run
python compare_processors.py
```

---

## Project Structure
```
file-processing-comparison/
├── demo.py              # Tika demonstrations
├── HC_demo.py              # OCDO demonstrations
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── test_files/              # Sample documents
```

---

## Comparison

| Feature | Apache Tika | OCDO |
|---------|-------------|------|
| File Formats | 1000+ | Common formats |
| Setup | Requires Java | Python-only |

---

## Requirements

- Python 3.12+
- Java 21+ (for Tika)
- Docker (optional)

---