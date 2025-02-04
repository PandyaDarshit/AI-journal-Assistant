#!/bin/bash

# Exit on error
set -e

# Function to initialize the assistant
init_assistant() {
    echo "Initializing Mukti Journal Assistant..."
    
    # Check for required files
    if [ ! -f "system_prompt.txt" ]; then
        echo "Error: system_prompt.txt not found"
        exit 1
    fi
    
    # Create journal directory if it doesn't exist
    mkdir -p /app/journal_entries
    
    # Install requirements if needed
    if [ -f "requirements.txt" ]; then
        echo "Installing Python dependencies..."
        pip3 install --no-cache-dir -r requirements.txt
    fi
}

# Function to start the assistant
start_assistant() {
    echo "Starting Mukti Journal Assistant..."
    python3 main.py
}

# Main execution
main() {
    # Initialize
    init_assistant
    
    # Start the service
    start_assistant
}

# Execute main function
main "$@"