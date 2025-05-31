#!/bin/bash
# Palmer Intelligence API - Quick Test Script

echo "Testing Palmer Intelligence API..."
echo ""

# Check if API is running
if ! curl -s http://localhost:8000 > /dev/null 2>&1; then
    echo "❌ API is not running. Start it first with: python start_api.py"
    exit 1
fi

echo "✅ API is running"
echo ""

# Test quick scan
echo "=== Testing Quick Scan ==="
curl -X POST "http://localhost:8000/api/v1/quick-scan" \
  -H "Content-Type: application/json" \
  -d '{"target_url": "example.com"}' \
  -s | python -m json.tool | head -20

echo ""
echo "Full test completed. For more tests, use the /docs endpoint."
