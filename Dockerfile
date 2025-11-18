# Use official Python runtime as base image
FROM python:3.12-slim

# Set working directory in container
WORKDIR /app

# Install Java and Git (required for Tika and git dependencies)
RUN apt-get update && \
    apt-get install -y openjdk-21-jre-headless git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Command to run when container starts
CMD ["python", "demo.py"]