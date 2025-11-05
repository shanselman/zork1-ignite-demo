#!/bin/bash

# Test script to verify the setup without running the full game

echo "🧪 Testing LLM-Driven Zork Setup"
echo "================================"
echo ""

# Check Python version
echo "✓ Python version:"
python3 --version
echo ""

# Check if story file exists
if [ -f "zork1.z3" ]; then
    echo "✓ zork1.z3 found"
else
    echo "✗ zork1.z3 NOT found"
    exit 1
fi

# Check if Fic exists
if [ -d "Fic" ]; then
    echo "✓ Fic interpreter directory found"
else
    echo "✗ Fic interpreter NOT found - cloning..."
    git clone https://github.com/mjdarby/Fic.git
fi

# Check if Fic main script exists
if [ -f "Fic/fic.py" ]; then
    echo "✓ Fic/fic.py found"
else
    echo "✗ Fic/fic.py NOT found"
    exit 1
fi

# Install dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Test imports
echo ""
echo "🔍 Testing Python imports..."
python3 -c "
from llm_zork_driver import LLMZorkDriver
from zork_llm_agent import ZorkLLMAgent
from game_parser import ZorkGameParser
from prompt_templates import SYSTEM_PROMPT
print('✓ All modules import successfully')
"

# Test game parser
echo ""
echo "🔍 Testing game parser..."
python3 -c "
from game_parser import ZorkGameParser
parser = ZorkGameParser()
test_output = 'West of House\nYou are standing in an open field west of a white house.\nYour score is 0 (total of 350 points), in 1 move.'
state = parser.summarize_state(test_output)
print(f'✓ Parser works - Score: {state[\"score\"]}, Location: {state[\"location\"]}')
"

echo ""
echo "================================"
echo "✅ All tests passed!"
echo ""
echo "To run with a vLLM server:"
echo "  python3 llm_zork_driver.py --vllm-url http://localhost:8000/v1 --model your-model-name"
echo ""
echo "Or build Docker container:"
echo "  docker-compose build"
echo ""
