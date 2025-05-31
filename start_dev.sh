#!/bin/bash
cd ~/dev/PalmerAI/backend
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
echo "Starting Palmer AI API..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000
