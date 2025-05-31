@echo off
echo Starting Palmer Intelligence...
start cmd /k cd backend && ..\venv\Scripts\python main.py
timeout /t 3
start http://localhost:8000
