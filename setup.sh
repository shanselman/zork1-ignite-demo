#!/bin/bash

# Setup script for LLM-Driven Zork

echo "🚀 Setting up LLM-Driven Zork Environment"
echo "=========================================="
echo ""

# Check if we're in a virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    
    echo "✓ Virtual environment created"
    echo ""
    echo "🔧 Activating virtual environment..."
    source venv/bin/activate
else
    echo "✓ Already in virtual environment: $VIRTUAL_ENV"
fi

echo ""
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo "✓ Dependencies installed"
echo ""

# Clone Fic if needed
if [ ! -d "Fic" ] || [ ! -f "Fic/fic.py" ]; then
    echo "📥 Cloning Fic interpreter..."
    rm -rf Fic
    git clone https://github.com/mjdarby/Fic.git
    echo "✓ Fic cloned"
else
    echo "✓ Fic interpreter already present"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To use the system:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Set up your vLLM server"
echo "  3. Run: python3 llm_zork_driver.py --vllm-url http://localhost:8000/v1 --model your-model"
echo ""
echo "Or use Docker:"
echo "  docker-compose build && docker-compose up"
echo ""
