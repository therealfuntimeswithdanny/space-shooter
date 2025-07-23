#!/bin/bash
cd "/Users/danny/Documents/Documents - iMac/space-shooter"

# Check for python3
if ! command -v python3 &> /dev/null; then
    echo "python3 not found. Installing with Homebrew..."
    if ! command -v brew &> /dev/null; then
        echo "Homebrew not found. Please install Homebrew first: https://brew.sh/"
        exit 1
    fi
    brew install python
fi

# Check for pygame
if ! python3 -c "import pygame" &> /dev/null; then
    echo "pygame not found. Installing with pip..."
    python3 -m pip install --user pygame
fi

python3 day3.py