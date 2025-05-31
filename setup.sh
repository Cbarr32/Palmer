#!/bin/bash

echo "🚀 Setting up Palmer AI..."

# Install backend dependencies
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Initialize database
python init_db.py

# Install frontend dependencies
cd ../frontend
npm install

echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "1. Start the backend: cd backend && python main.py"
echo "2. Start the frontend: cd frontend && npm run dev"
echo ""
echo "Or use Docker: docker-compose up"
