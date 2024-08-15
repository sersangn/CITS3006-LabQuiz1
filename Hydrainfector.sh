#!/bin/bash

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null
then
    echo "PyInstaller could not be found. Please install it using 'pip install pyinstaller'."
    exit 1
fi

# Define the Python script to be compiled
SCRIPT_NAME="malware.py"

# Define output directories
WIN_OUTPUT_DIR="dist/windows"
LINUX_OUTPUT_DIR="dist/linux"

# Ensure output directories exist
mkdir -p "$WIN_OUTPUT_DIR"
mkdir -p "$LINUX_OUTPUT_DIR"

# Compile for Windows
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    echo "Compiling for Windows..."
    pyinstaller --onefile --distpath "$WIN_OUTPUT_DIR" --workpath "build/windows" --specpath "spec/windows" "$SCRIPT_NAME"
    echo "Windows executable created in $WIN_OUTPUT_DIR"
    
    # Run the compiled Windows executable
    echo "Running the compiled executable..."
    start "" "$WIN_OUTPUT_DIR/malware.exe"
fi

# Compile for Linux/macOS
if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
    echo "Compiling for Linux/macOS..."
    pyinstaller --onefile --distpath "$LINUX_OUTPUT_DIR" --workpath "build/linux" --specpath "spec/linux" "$SCRIPT_NAME"
    echo "Linux/macOS executable created in $LINUX_OUTPUT_DIR"
    
    # Run the compiled Linux/macOS executable
    echo "Running the compiled executable..."
    chmod +x "$LINUX_OUTPUT_DIR/malware"
    "$LINUX_OUTPUT_DIR/malware"
fi
