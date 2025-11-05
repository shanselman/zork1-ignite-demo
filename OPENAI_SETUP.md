# Using OpenAI API with LLM Zork Player

This guide shows how to use OpenAI, Azure OpenAI, or any OpenAI-compatible API with the Zork player.

## ⚙️ Configuration Options

### Option 1: Environment Variables (Recommended)

Create a `.env` file in the project root:

```bash
# For OpenAI
VLLM_API_URL=https://api.openai.com/v1
VLLM_MODEL_NAME=gpt-4
OPENAI_API_KEY=sk-your-actual-api-key-here
MAX_TURNS=500
```

```bash
# For Azure OpenAI
VLLM_API_URL=https://your-resource.openai.azure.com/openai/deployments/your-deployment
VLLM_MODEL_NAME=gpt-4
OPENAI_API_KEY=your-azure-api-key-here
MAX_TURNS=500
```

### Option 2: Command Line Arguments

```bash
python3 llm_zork_driver.py \
    --vllm-url https://api.openai.com/v1 \
    --model gpt-4 \
    --api-key sk-your-actual-api-key-here \
    --max-turns 500
```

### Option 3: Docker with Environment Variables

```bash
# Set environment variables
export VLLM_API_URL=https://api.openai.com/v1
export VLLM_MODEL_NAME=gpt-4
export OPENAI_API_KEY=sk-your-actual-api-key-here

# Run with docker-compose
docker-compose up
```

Or pass directly to docker:

```bash
docker run \
    -e VLLM_API_URL=https://api.openai.com/v1 \
    -e VLLM_MODEL_NAME=gpt-4 \
    -e OPENAI_API_KEY=sk-your-actual-api-key-here \
    -v $(pwd)/logs:/app/logs \
    zork-llm-player:latest
```

## 🔑 Getting Your OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign in to your account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. **IMPORTANT**: Save it securely - you won't see it again!

## 📝 Quick Start Examples

### Using OpenAI GPT-4

```bash
# Create .env file
cat > .env << EOF
VLLM_API_URL=https://api.openai.com/v1
VLLM_MODEL_NAME=gpt-4
OPENAI_API_KEY=sk-your-key-here
MAX_TURNS=500
EOF

# Run with venv
source venv/bin/activate
python3 llm_zork_driver.py
```

### Using OpenAI GPT-3.5-Turbo (Cheaper)

```bash
python3 llm_zork_driver.py \
    --vllm-url https://api.openai.com/v1 \
    --model gpt-3.5-turbo \
    --api-key sk-your-key-here
```

### Using Azure OpenAI

```bash
python3 llm_zork_driver.py \
    --vllm-url https://YOUR-RESOURCE.openai.azure.com/openai/deployments/YOUR-DEPLOYMENT \
    --model gpt-4 \
    --api-key YOUR-AZURE-KEY
```

## 🎯 Recommended Models

| Model | Performance | Cost | Best For |
|-------|-------------|------|----------|
| `gpt-4` | ⭐⭐⭐⭐⭐ Excellent | 💰💰💰 High | Best gameplay, demos |
| `gpt-4-turbo` | ⭐⭐⭐⭐⭐ Excellent | 💰💰 Medium | Great balance |
| `gpt-3.5-turbo` | ⭐⭐⭐ Good | 💰 Low | Testing, development |

## 💡 Cost Estimates

Approximate costs for a 100-turn game session:

- **GPT-4**: ~$0.30 - $0.60 per session
- **GPT-4-Turbo**: ~$0.15 - $0.30 per session
- **GPT-3.5-Turbo**: ~$0.02 - $0.05 per session

*Note: Costs vary based on prompt length and response size*

## 🔒 Security Best Practices

### ✅ DO:
- Store API keys in `.env` file (already in `.gitignore`)
- Use environment variables
- Rotate keys periodically
- Set spending limits in OpenAI dashboard
- Use separate keys for development/production

### ❌ DON'T:
- Commit API keys to git
- Share keys in chat/email
- Use production keys for testing
- Hardcode keys in source files

## 🐛 Troubleshooting

### "Invalid API Key"
- Double-check your key starts with `sk-`
- Ensure no extra spaces in the key
- Verify key is active at https://platform.openai.com/api-keys

### "Rate Limit Exceeded"
- OpenAI has rate limits per tier
- Add `time.sleep()` between calls if needed
- Consider upgrading your OpenAI tier

### "Model Not Found"
- Verify model name spelling: `gpt-4`, `gpt-3.5-turbo`, etc.
- Check your OpenAI account has access to that model

### High Costs
- Use `gpt-3.5-turbo` for testing
- Set `MAX_TURNS` to lower value (e.g., 50) for testing
- Monitor usage at https://platform.openai.com/usage

## 📊 Example .env File Templates

### For OpenAI (Production)
```bash
# OpenAI Configuration
VLLM_API_URL=https://api.openai.com/v1
VLLM_MODEL_NAME=gpt-4-turbo
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
MAX_TURNS=500
LOG_LEVEL=INFO
```

### For OpenAI (Testing - Cheaper)
```bash
# OpenAI Configuration (Testing)
VLLM_API_URL=https://api.openai.com/v1
VLLM_MODEL_NAME=gpt-3.5-turbo
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
MAX_TURNS=50
LOG_LEVEL=INFO
```

### For Azure OpenAI
```bash
# Azure OpenAI Configuration
VLLM_API_URL=https://your-resource.openai.azure.com/openai/deployments/gpt-4
VLLM_MODEL_NAME=gpt-4
OPENAI_API_KEY=your-azure-api-key-here
MAX_TURNS=500
LOG_LEVEL=INFO
```

### For Local vLLM (Free)
```bash
# Local vLLM Configuration
VLLM_API_URL=http://localhost:8000/v1
VLLM_MODEL_NAME=meta-llama/Llama-3.1-8B-Instruct
OPENAI_API_KEY=EMPTY
MAX_TURNS=500
LOG_LEVEL=INFO
```

## 🎮 Full Workflow Example

```bash
# 1. Create .env file with your OpenAI key
echo "VLLM_API_URL=https://api.openai.com/v1" > .env
echo "VLLM_MODEL_NAME=gpt-4" >> .env
echo "OPENAI_API_KEY=sk-your-key-here" >> .env
echo "MAX_TURNS=100" >> .env

# 2. Activate venv (if using local)
source venv/bin/activate

# 3. Run the game
python3 llm_zork_driver.py

# 4. Watch the AI play!
# Logs will be in logs/ directory
```

## 📚 Additional Resources

- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [OpenAI Pricing](https://openai.com/pricing)
- [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/ai-services/openai-service)

## 🆘 Need Help?

If you're still having issues:

1. Check that `.env` file exists and has correct format
2. Verify API key is valid at OpenAI dashboard
3. Try with `gpt-3.5-turbo` first (cheaper for testing)
4. Check logs in `logs/` directory for error messages
5. Run `python3 test_components.py` to verify setup
