#!/bin/bash
echo "Setting up Python virtual environment..."

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

echo ""
echo "✅ Setup complete! The virtual environment is ready."
echo "To activate later, run:"
echo "source venv/bin/activate"
