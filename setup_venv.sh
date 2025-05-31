#!/bin/bash
# Setup virtual environment for Palmer Intelligence API

echo "Setting up Python virtual environment..."

# Create venv if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
else
    echo "❌ requirements.txt not found"
fi

echo ""
echo "Virtual environment is ready!"
echo "To activate it manually, run: source venv/bin/activate"
