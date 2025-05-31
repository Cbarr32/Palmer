#!/bin/bash
set -e

echo "🚀 Setting up Palmer Intelligence API Development Environment..."

# Update system packages
sudo apt-get update
sudo apt-get install -y postgresql-client redis-tools

# Install Python dependencies
pip install --upgrade pip
pip install poetry

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install project dependencies
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    # Create requirements.txt if it doesn't exist
    cat > requirements.txt << 'REQ'
fastapi==0.104.1
uvicorn[standard]==0.24.0
anthropic==0.7.0
httpx==0.25.2
beautifulsoup4==4.12.2
pydantic==2.5.0
python-dotenv==1.0.0
python-multipart==0.0.6
aiofiles==23.2.1
redis==5.0.1
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9
pytest==7.4.3
pytest-asyncio==0.21.1
black==23.11.0
ruff==0.1.6
REQ
    pip install -r requirements.txt
fi

# Install development dependencies
pip install pytest-cov httpx-mock faker

# Create necessary directories
mkdir -p logs
mkdir -p data
mkdir -p tests

# Setup pre-commit hooks
cat > .pre-commit-config.yaml << 'PRECOMMIT'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
PRECOMMIT

pip install pre-commit
pre-commit install

echo "✅ Development environment setup complete!"
