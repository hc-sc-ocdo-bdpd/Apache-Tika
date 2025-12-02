FROM python:3.12-slim

WORKDIR /app

# Install system dependencies (Git is required!)
RUN apt-get update && \
    apt-get install -y openjdk-21-jre-headless git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python packages from requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install OCDO package directly from GitHub
RUN pip install git+https://github.com/hc-sc-ocdo-bdpd/file-processing.git
RUN pip install git+https://github.com/hc-sc-ocdo-bdpd/file-processing-ocr.git

# Copy your application code
COPY . .

# Run your script
CMD ["python", "demo.py"]