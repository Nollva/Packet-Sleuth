# Use a lightweight Python version compatible with ARM (Pi)
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies for Scapy (libpcap)
RUN apt-get update && apt-get install -y \
    libpcap0.8 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the Flask port
EXPOSE 5000

# Command to run the app
# Note: Python needs to run unbuffered so logs show up immediately
CMD ["python", "-u", "server.py"]