FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for GUI/CLI support if needed (minimal)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default to CLI mode
CMD ["python", "main_cli.py"]
