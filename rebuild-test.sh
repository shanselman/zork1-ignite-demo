#!/bin/bash

# Rebuild and test script for Docker container
# This ensures a clean rebuild with latest code changes

set -e  # Exit on any error

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║          DOCKER REBUILD AND TEST SCRIPT                              ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Stop everything
echo "🛑 Step 1: Stopping all containers..."
docker-compose down --remove-orphans
echo "✅ Containers stopped"
echo ""

# Step 2: Remove old container
echo "🗑️  Step 2: Removing old container..."
docker rm -f zork-llm-player 2>/dev/null || echo "   (container not found, skipping)"
echo "✅ Old container removed"
echo ""

# Step 3: Remove old image
echo "🗑️  Step 3: Removing old image..."
docker rmi zork-llm-player:latest 2>/dev/null || echo "   (image not found, skipping)"
echo "✅ Old image removed"
echo ""

# Step 4: Show what files will be copied
echo "📦 Step 4: Files that will be copied into container:"
echo "   Core files:"
ls -lh llm_zork_driver.py zork_llm_agent.py game_parser.py prompt_templates.py 2>/dev/null | awk '{print "   ", $9, "(" $5 ")"}'
echo "   Config files:"
ls -lh Dockerfile entrypoint.sh docker-compose.yml 2>/dev/null | awk '{print "   ", $9, "(" $5 ")"}'
echo ""

# Step 5: Check .env file
echo "🔍 Step 5: Checking .env file..."
if [ -f .env ]; then
    echo "✅ .env file exists"
    echo "   Contents (with key hidden):"
    cat .env | sed 's/sk-[^ ]*/sk-HIDDEN/g' | sed 's/^/   /'
else
    echo "⚠️  WARNING: No .env file found!"
    echo "   Create one with:"
    echo "   cat > .env << 'END'"
    echo "   VLLM_API_URL=https://api.openai.com/v1"
    echo "   VLLM_MODEL_NAME=gpt-4o-mini"
    echo "   OPENAI_API_KEY=sk-your-key-here"
    echo "   MAX_TURNS=100"
    echo "   END"
fi
echo ""

# Step 6: Build fresh
echo "🔨 Step 6: Building fresh Docker image (this will take a minute)..."
docker-compose build --no-cache --progress=plain 2>&1 | tee /tmp/docker-build.log | tail -20
BUILD_EXIT_CODE=${PIPESTATUS[0]}

if [ $BUILD_EXIT_CODE -eq 0 ]; then
    echo "✅ Build completed successfully!"
else
    echo "❌ Build failed! Check /tmp/docker-build.log for details"
    exit 1
fi
echo ""

# Step 7: Verify image
echo "🔍 Step 7: Verifying new image..."
docker images zork-llm-player:latest --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"
echo ""

# Step 8: Check what's in the image
echo "🔍 Step 8: Verifying files in container image..."
echo "   Checking llm_zork_driver.py last modified date:"
docker run --rm zork-llm-player:latest ls -lh /app/llm_zork_driver.py | awk '{print "   ", $6, $7, $8, $9}'
echo ""
echo "   Checking entrypoint.sh:"
docker run --rm zork-llm-player:latest cat /app/entrypoint.sh | head -5
echo "   ..."
echo ""

# Step 9: Test environment variable passing
echo "🔍 Step 9: Testing environment variable passing..."
echo "   Running test container to check env vars..."
VLLM_API_URL=https://api.openai.com/v1 \
VLLM_MODEL_NAME=gpt-4o-mini \
OPENAI_API_KEY=test-key-123 \
docker-compose run --rm zork-llm env | grep -E "(VLLM|OPENAI)" | sed 's/^/   /'
echo ""

# Step 10: Show what will run
echo "📋 Step 10: Container will run this command:"
echo "   $(docker inspect zork-llm-player:latest -f '{{.Config.Cmd}}')"
echo ""

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                         BUILD COMPLETE!                              ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "To run the container:"
echo "  docker-compose up"
echo ""
echo "To run with verbose output:"
echo "  docker-compose up --verbose"
echo ""
echo "To watch logs:"
echo "  docker-compose logs -f"
echo ""
echo "Build log saved to: /tmp/docker-build.log"
echo ""
