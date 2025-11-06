# LLM-Driven Zork I Player - Quick Start

## 🎮 What is this?

An autonomous AI agent that plays Zork I by querying an LLM API (OpenAI, vLLM, Azure, etc.). Watch an AI explore the Great Underground Empire!

## 📦 Initial Setup

**First time cloning?** Make sure to get the Fic interpreter submodule:

```bash
# If cloning for the first time
git clone --recurse-submodules https://github.com/yourusername/zork1-ignite-demo.git

# OR if you already cloned without submodules
cd zork1-ignite-demo
git submodule update --init --recursive
```

## 🚀 Quick Start with OpenAI

**Most users will want to use OpenAI (easiest setup):**

```bash
# 1. Get your OpenAI API key from https://platform.openai.com/api-keys

# 2. Create .env file with your key
cat > .env << EOF
VLLM_API_URL=https://api.openai.com/v1
VLLM_MODEL_NAME=gpt-4
OPENAI_API_KEY=sk-your-actual-key-here
MAX_TURNS=100
EOF

# 3. Run setup
./setup.sh
source venv/bin/activate

# 4. Run!
python3 llm_zork_driver.py
```

**OR with command line:**
```bash
python3 llm_zork_driver.py \
    --vllm-url https://api.openai.com/v1 \
    --model gpt-4 \
    --api-key sk-your-key-here \
    --max-turns 100
```

**Cost**: ~$0.30-$0.60 per 100-turn session with GPT-4. Use `gpt-3.5-turbo` for cheaper testing (~$0.02-$0.05).

📖 **Full OpenAI setup guide**: See [OPENAI_SETUP.md](OPENAI_SETUP.md)

---

## 🚀 Quick Start with vLLM (Free, Self-Hosted)

### Option 1: Docker (Recommended)

```bash
# 1. Build the container
docker-compose build

# 2. Set your vLLM server URL
export VLLM_API_URL=http://your-vllm-server:8000/v1
export VLLM_MODEL_NAME=meta-llama/Llama-3.1-8B-Instruct

# 3. Run!
docker-compose up
```

### Option 2: Local Installation

```bash
# 1. Run setup (creates venv and installs dependencies)
./setup.sh

# 2. Activate virtual environment
source venv/bin/activate

# 3. Run with your vLLM server
python3 llm_zork_driver.py \
    --vllm-url http://localhost:8000/v1 \
    --model meta-llama/Llama-3.1-8B-Instruct \
    --max-turns 500
```

## 📋 Prerequisites

### For OpenAI (Easiest)
- OpenAI API key from https://platform.openai.com/api-keys
- Python 3.11+ **OR** Docker

### For vLLM (Free, Self-Hosted)
  ```bash
  # Example: Start vLLM locally
  python -m vllm.entrypoints.openai.api_server \
      --model meta-llama/Llama-3.1-8B-Instruct \
      --port 8000
  ```

- **Docker** (for containerized option) or **Python 3.11+** (for local)

## 📊 Output

Gameplay logs are saved to `logs/`:
- `transcript_*.txt` - Full game transcript
- `llm_queries_*.jsonl` - Detailed turn-by-turn data
- `summary_*.json` - Session statistics

Example output:
```
🔄 Turn 15/500
🤖 LLM Command: north
📍 Location: Kitchen
🏆 Score: 10/350
📜 Game Response:
Kitchen
This is a kitchen...
```

## 🎯 How It Works

```
Game Loop:
1. Read game state from Zork
2. Send state to LLM via vLLM API
3. Parse LLM response to extract command
4. Send command to Zork
5. Repeat until victory, death, or max turns
```

## 🔧 Configuration

Environment variables:
- `VLLM_API_URL` - Your vLLM server URL
- `VLLM_MODEL_NAME` - Model to use
- `MAX_TURNS` - Maximum game turns (default: 500)

Command line options:
```bash
python3 llm_zork_driver.py --help
```

## 📖 Full Documentation

See [README_LLM.md](README_LLM.md) for complete documentation including:
- Architecture details
- Prompt engineering
- Performance tuning
- Troubleshooting
- Development guide

## 🎓 Example Models

Tested with:
- `meta-llama/Llama-3.1-8B-Instruct` ✅
- `meta-llama/Llama-3.1-70B-Instruct` ✅ (better performance)
- `mistralai/Mistral-7B-Instruct-v0.3` ✅
- `Qwen/Qwen2.5-7B-Instruct` ✅

Any OpenAI-compatible API works (OpenAI, Azure OpenAI, Anthropic with proxy, etc.)

## 🐛 Troubleshooting

**"Connection refused"**
- Make sure vLLM server is running
- Check URL format: `http://host:port/v1`
- In Docker, use `http://host.docker.internal:8000/v1` to reach host

**"pexpect" not found**
- Run `./setup.sh` to create venv and install dependencies

**LLM outputs garbage**
- Try a larger/better model
- Adjust temperature in `zork_llm_agent.py`
- Check prompt templates in `prompt_templates.py`

## 📝 Files

Core files:
- `llm_zork_driver.py` - Main game loop orchestrator
- `zork_llm_agent.py` - LLM API client
- `game_parser.py` - Zork output parser
- `prompt_templates.py` - System prompts
- `Dockerfile` & `docker-compose.yml` - Containerization
- `zork1.z3` - Zork I game file

## 🤝 Credits

- Zork I © Infocom (1980)
- Fic interpreter: https://github.com/mjdarby/Fic
- Original source: https://github.com/historicalsource/zork1
