#!/bin/sh
# Entrypoint script to pass environment variables as arguments

python3 /app/llm_zork_driver.py \
    --vllm-url "${VLLM_API_URL}" \
    --model "${VLLM_MODEL_NAME}" \
    --api-key "${OPENAI_API_KEY}" \
    --max-turns "${MAX_TURNS}"
