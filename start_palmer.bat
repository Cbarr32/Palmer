@echo off
cls
echo ================================================
echo     Palmer Intelligence - Starting Services
echo     Advanced Competitive Intelligence Platform
echo ================================================
echo.

echo [1/3] Activating virtual environment...
call venv\Scripts\activate

echo.
echo [2/3] Checking dependencies...
pip install -q anthropic fastapi uvicorn httpx beautifulsoup4 redis python-dotenv pydantic pandas numpy

echo.
echo [3/3] Starting Palmer Intelligence API...
echo.
echo ================================================
echo     API will be available at:
echo     http://localhost:8000
echo     
echo     API Documentation:
echo     http://localhost:8000/docs
echo ================================================
echo.

cd backend
python main.py
