# Use lightweight Python image
FROM python:3.9-slim

# Prevent Python from writing pyc files & enable logs immediately
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (better caching)
COPY flow/requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir \
        -r requirements.txt \
        promptflow==1.18.5 \
        gunicorn==22.0.0 \
        "uvicorn>=0.27.0,<1.0.0" \
        keyrings.alt

# Copy application code
COPY flow/ /app/

# Expose port (adjust if needed)
EXPOSE 8080

# Start app (adjust module name if different)
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "2", "-b", "0.0.0.0:8080", "app:app"]