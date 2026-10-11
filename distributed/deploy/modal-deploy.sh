#!/usr/bin/env bash
# EphapticOS 1-click deployment to Modal
#
# Prerequisites: pip install modal && modal setup
#
# Usage:
#   export LLM_API_KEY=sk-xxx
#   bash distributed/deploy/modal-deploy.sh

set -euo pipefail

if [ -z "${LLM_API_KEY:-}" ]; then
    echo "ERROR: LLM_API_KEY environment variable is required"
    exit 1
fi

echo "Deploying EphapticOS to Modal..."

# Create or update the secret group
echo "Setting up secrets..."
modal secret create EphapticOS-secrets \
    LLM_API_KEY="$LLM_API_KEY" \
    LLM_MODEL="${LLM_MODEL:-openai/gpt-4o-mini}" \
    LLM_PROVIDER="${LLM_PROVIDER:-openai}" \
    DB_PROVIDER="${DB_PROVIDER:-sqlite}" \
    2>/dev/null || \
modal secret update EphapticOS-secrets \
    LLM_API_KEY="$LLM_API_KEY" \
    LLM_MODEL="${LLM_MODEL:-openai/gpt-4o-mini}" \
    LLM_PROVIDER="${LLM_PROVIDER:-openai}" \
    DB_PROVIDER="${DB_PROVIDER:-sqlite}"

echo "Deploying app..."
modal deploy distributed/deploy/modal_app.py

echo ""
echo "EphapticOS deployed successfully to Modal!"
echo "Check your Modal dashboard for the endpoint URL."
