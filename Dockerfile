FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Clone Fic interpreter
RUN git clone https://github.com/mjdarby/Fic.git /app/Fic

# Copy requirements and install Python packages
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY zork1.z3 /app/
COPY llm_zork_driver.py /app/
COPY zork_llm_agent.py /app/
COPY game_parser.py /app/
COPY prompt_templates.py /app/

# Create logs directory
RUN mkdir -p /app/logs

# Environment variables with defaults
#ENV VLLM_API_URL="http://localhost:8000/v1"
#ENV VLLM_MODEL_NAME="meta-llama/Llama-3.1-8B-Instruct"
#ENV OPENAI_API_KEY="EMPTY"
#ENV MAX_TURNS="500"
#ENV LOG_LEVEL="INFO"

# Copy entrypoint script
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh /app/llm_zork_driver.py

# Default command - use entrypoint to pass env vars as arguments
CMD ["/app/entrypoint.sh"]
