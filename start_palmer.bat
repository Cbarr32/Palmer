@echo off
cls
echo ============================================
echo Palmer Intelligence - Starting Services
echo ============================================
echo.
echo Activating virtual environment...
call venv\Scripts\activate

echo Installing/Updating dependencies...
pip install -q anthropic fastapi uvicorn httpx beautifulsoup4 redis python-dotenv pydantic pandas numpy

echo Starting Palmer Intelligence API...
cd backend
python main.py
