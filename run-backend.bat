@echo off
echo ========================================
echo Starting Backend Server
echo ========================================
echo.

cd backend
call venv\Scripts\activate.bat

echo Starting FastAPI server on http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
