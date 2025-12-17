# Use Python 3.12 slim-bookworm for smaller image size
FROM python:3.12-slim-bookworm

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies in a single layer
# - openjdk-17-jre-headless: Required for Apache Tika (Java 17 LTS)
# - git: Required for installing packages from GitHub
# - tesseract-ocr: Optional for OCR functionality
# - build-essential: For compiling Python packages if needed
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        openjdk-17-jre-headless \
        git \
        tesseract-ocr \
        tesseract-ocr-eng \
        tesseract-ocr-fra \
        build-essential \
        gcc \
        g++ && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Verify Java installation
RUN java -version

# Create necessary directories
RUN mkdir -p /app/test_files /app/outputs /app/models

# Copy requirements file first (for better layer caching)
COPY requirements.txt .

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install OCDO packages directly from GitHub
RUN pip install --no-cache-dir \
    git+https://github.com/hc-sc-ocdo-bdpd/file-processing.git \
    git+https://github.com/hc-sc-ocdo-bdpd/file-processing-ocr.git

# Copy application code
COPY file_processing/ ./file_processing/
COPY test_files/ ./test_files/
COPY sample_tests/ ./sample_tests/

# Set proper permissions
RUN chmod -R 755 /app

# Default command - run the main demo
# This can be overridden at runtime
CMD ["python", "file_processing/Tika_demo.py"]