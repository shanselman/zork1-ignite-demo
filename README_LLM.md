# LLM-Driven Zork I Player

This project contains an autonomous LLM agent that plays Zork I by querying a vLLM server for next actions.

## Architecture

```
┌─────────────────────────────────────────────────┐
│          Docker Container                       │
│  ┌──────────────────────────────────────────┐  │
│  │   LLM Driver (llm_zork_driver.py)       │  │
│  │   - Game loop orchestrator               │  │
│  │   - Logging and state tracking           │  │
│  └────────┬────────────────────┬─────────────┘  │
│           │                    │                │
│           ▼                    ▼                │
│  ┌─────────────────┐  ┌──────────────────────┐ │
│  │ Fic Interpreter │  │  LLM Agent           │ │
│  │ (Z-machine)     │  │  - vLLM API client   │ │
│  │ + zork1.z3      │  │  - Prompt engineering│ │
│  └─────────────────┘  └──────────┬───────────┘ │
│                                  │             │
└──────────────────────────────────┼─────────────┘
                                   │
                                   ▼
                          ┌─────────────────┐
                          │  vLLM Server    │
                          │  (External)     │
                          └─────────────────┘
```

## Components

### 1. **llm_zork_driver.py**
Main orchestrator that:
- Spawns Fic interpreter process using pexpect
- Manages game loop (max 500 turns by default)
- Coordinates between game and LLM agent
- Logs all gameplay to files

### 2. **zork_llm_agent.py**
LLM agent that:
- Queries vLLM API using OpenAI-compatible interface
- Maintains conversation context
- Cleans and validates LLM outputs
- Handles error recovery

### 3. **game_parser.py**
Parser that extracts:
- Score and moves
- Current location
- Inventory items
- Game state (death, victory, errors)

### 4. **prompt_templates.py**
Contains:
- System prompt with game rules
- Few-shot examples
- Error recovery prompts

## Setup

### Prerequisites

1. **vLLM Server Running**
   ```bash
   # Example: Start vLLM with Llama model
   python -m vllm.entrypoints.openai.api_server \
       --model meta-llama/Llama-3.1-8B-Instruct \
       --port 8000
   ```

2. **Docker installed** (or run locally with Python 3.11+)

### Option 1: Docker (Recommended)

```bash
# Build the image
docker-compose build

# Configure vLLM URL (edit .env or set environment variable)
export VLLM_API_URL=http://your-vllm-server:8000/v1
export VLLM_MODEL_NAME=meta-llama/Llama-3.1-8B-Instruct

# Run
docker-compose up
```

### Option 2: Local Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Ensure Fic interpreter is available
git clone https://github.com/mjdarby/Fic.git

# Run
python3 llm_zork_driver.py \
    --vllm-url http://localhost:8000/v1 \
    --model meta-llama/Llama-3.1-8B-Instruct \
    --max-turns 500
```

## Usage

### Basic Usage

```bash
# Using docker-compose
docker-compose up

# Or with custom settings
docker run -e VLLM_API_URL=http://host:8000/v1 \
           -e MAX_TURNS=1000 \
           -v $(pwd)/logs:/app/logs \
           zork-llm-player:latest
```

### Command Line Arguments

```bash
python3 llm_zork_driver.py --help

Options:
  --vllm-url URL          vLLM API base URL (default: http://localhost:8000/v1)
  --model NAME            Model name (default: meta-llama/Llama-3.1-8B-Instruct)
  --story-file PATH       Path to zork1.z3 (default: zork1.z3)
  --max-turns N           Maximum turns (default: 500)
  --log-dir DIR           Log directory (default: logs/)
```

### Environment Variables

```bash
VLLM_API_URL            # vLLM server URL
VLLM_MODEL_NAME         # Model to use
MAX_TURNS               # Maximum game turns
LOG_LEVEL               # Logging level
```

## Output

The system generates three log files per session:

1. **transcript_YYYYMMDD_HHMMSS.txt**
   - Full game transcript with commands and responses
   - Human-readable format

2. **llm_queries_YYYYMMDD_HHMMSS.jsonl**
   - JSON Lines format with detailed turn information
   - Includes LLM queries and game state

3. **summary_YYYYMMDD_HHMMSS.json**
   - Session summary with final statistics
   - Score, turns played, completion percentage

Example summary:
```json
{
  "timestamp": "2024-11-04T22:15:30",
  "total_turns": 127,
  "final_score": 45,
  "max_score": 350,
  "completion_percentage": 12.86,
  "model": "meta-llama/Llama-3.1-8B-Instruct"
}
```

## Prompt Engineering

The system uses carefully crafted prompts:

1. **System Prompt**: Explains Zork rules and command format
2. **Game State Template**: Formats current state for LLM
3. **Error Recovery**: Helps LLM recover from invalid commands

Key techniques:
- Constrain output to single command
- Use few-shot examples
- Maintain rolling context window (last 20 exchanges)
- Stop tokens to prevent verbose responses

## Performance Tips

1. **Model Selection**
   - Larger models (70B+) perform better
   - Instruction-tuned models recommended
   - Models with reasoning capabilities excel

2. **Tuning Parameters**
   - `temperature=0.7`: Balance exploration/exploitation
   - `max_tokens=50`: Short responses only
   - Context window: Keep last 20 turns

3. **vLLM Configuration**
   - Use tensor parallelism for large models
   - Increase GPU memory for longer contexts
   - Enable continuous batching

## Troubleshooting

### "Connection refused" error
- Ensure vLLM server is running
- Check VLLM_API_URL is correct
- Use `host.docker.internal` instead of `localhost` in Docker

### Game hangs/timeouts
- Increase pexpect timeout in driver
- Check Fic interpreter is working: `python3 Fic/fic.py zork1.z3`

### LLM outputs invalid commands
- Adjust prompt templates
- Lower temperature
- Try different model
- Check command cleaning logic in `zork_llm_agent.py`

### Poor gameplay performance
- Use larger/better model
- Increase context window
- Add more few-shot examples
- Fine-tune prompts for your model

## Development

### Running Tests

```bash
# Test Fic interpreter
python3 Fic/fic.py zork1.z3

# Test game parser
python3 -c "from game_parser import ZorkGameParser; print(ZorkGameParser().clean_output('test'))"

# Test LLM agent (requires vLLM)
python3 -c "from zork_llm_agent import ZorkLLMAgent; agent = ZorkLLMAgent('http://localhost:8000/v1', 'model'); print(agent.get_next_command('You are in a forest.'))"
```

### Extending

- **Add new prompts**: Edit `prompt_templates.py`
- **Improve parsing**: Modify `game_parser.py`
- **Change LLM behavior**: Update `zork_llm_agent.py`
- **Add features**: Extend `llm_zork_driver.py`

## Credits

- **Zork I**: Infocom (1980)
- **Fic Interpreter**: https://github.com/mjdarby/Fic
- **Original Source**: https://github.com/historicalsource/zork1

## License

Educational/research use. Original Zork I is copyright Infocom.
