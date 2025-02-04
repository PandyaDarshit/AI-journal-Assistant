FROM ubuntu:22.04

# Install necessary packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Create directory for journal entries
RUN mkdir -p /app/journal_entries

# Copy application files
COPY . .

# Set up volume for persistent storage
VOLUME ["/app/journal_entries"]

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Entry point
ENTRYPOINT ["./entrypoint.sh"]