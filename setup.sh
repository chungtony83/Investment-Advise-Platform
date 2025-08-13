#!/bin/bash
set -e  # exit on error

echo "🔍 Checking Python installation..."

# Use python3 explicitly
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install it first (e.g., via Homebrew: brew install python)."
    exit 1
fi

# Create virtual environment
echo "⚙️ Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check requirements.txt
if [[ -f "requirements.txt" ]]; then
    echo "📥 Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "⚠️ No requirements.txt found, skipping dependency installation."
fi

echo ""
echo "✅ Setup complete! Virtual environment is ready."
echo "To activate later, run:"
echo "source venv/bin/activate"