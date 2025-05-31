#!/bin/bash
# Palmer Intelligence API - Development Session Starter

echo "Starting Palmer Intelligence API Development Session..."
echo ""

# Navigate to project
cd ~/dev/PalmerAI

# Show current status
echo "=== Git Status ==="
git status --short
echo ""

# Check if API is running
if lsof -i:8000 > /dev/null 2>&1; then
    echo "✅ API is already running on port 8000"
else
    echo "❌ API is not running"
    echo "Would you like to start it? (y/n)"
    read -r response
    if [[ "$response" == "y" ]]; then
        echo "Starting API..."
        python start_api.py &
        sleep 3
        if lsof -i:8000 > /dev/null 2>&1; then
            echo "✅ API started successfully!"
        else
            echo "❌ Failed to start API. Check logs."
        fi
    fi
fi
echo ""

# Check environment
echo "=== Environment Check ==="
if [ -f .env ]; then
    if grep -q "ANTHROPIC_API_KEY" .env; then
        echo "✅ ANTHROPIC_API_KEY is configured"
    else
        echo "❌ ANTHROPIC_API_KEY is missing in .env"
    fi
else
    echo "❌ .env file not found"
fi
echo ""

# Show recent commits
echo "=== Recent Commits ==="
git log --oneline -5
echo ""

# Show TODO items from code
echo "=== TODO Items ==="
grep -r "TODO" backend/ --include="*.py" 2>/dev/null | head -10 || echo "No TODO items found"
echo ""

# Show API endpoints
echo "=== API Endpoints ==="
echo "Quick Scan: http://localhost:8000/api/v1/quick-scan"
echo "Full Analysis: http://localhost:8000/api/v1/analyze"
echo "Industry Report: http://localhost:8000/api/v1/industry-report"
echo "API Docs: http://localhost:8000/docs"
echo ""

# Project stats
echo "=== Project Stats ==="
echo "Python files: $(find backend/ -name "*.py" | wc -l)"
echo "Total lines: $(find backend/ -name "*.py" -exec wc -l {} + | tail -1 | awk '{print $1}')"
echo ""

# Show next steps
echo "=== Next Steps (from checkpoint) ==="
echo "1. Add virtual environment setup"
echo "2. Implement basic error handling"
echo "3. Add result caching with Redis"
echo "4. Create proper logging system"
echo ""

echo "Ready for development! 🚀"
echo ""

# Optional: Open VS Code
echo "Open VS Code? (y/n)"
read -r vscode_response
if [[ "$vscode_response" == "y" ]]; then
    code .
fi
