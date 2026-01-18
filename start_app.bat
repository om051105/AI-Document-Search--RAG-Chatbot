@echo off
TITLE AI RAG Chatbot - Industrial Starter

echo ===================================================
echo     STARTING INDUSTRIAL RAG CHATBOT SYSTEM
echo ===================================================
echo.

:: 1. Check for API Key
if not exist "backend\.env" (
    echo [WARNING] backend\.env file not found!
    echo Please create one based on backend\.env.example
    echo You need to add your OPENAI_API_KEY.
    echo.
    echo Copying .env.example to .env ...
    copy backend\.env.example backend\.env
    echo.
    echo PLEASE EDIT backend\.env NOW to add your API Key.
    pause
    exit
)

:: 2. Start Backend in a new window
echo [INFO] Starting FastAPI Backend on Port 8000...
:: We use /k to keep the window open if it crashes, so we can see the errors
start "RAG Backend API (DO NOT CLOSE)" cmd /k "cd backend && venv\Scripts\activate && python main.py"

:: 3. Start Frontend in a new window
echo [INFO] Starting Next.js Frontend on Port 3000...
start "RAG Frontend UI (DO NOT CLOSE)" cmd /k "cd frontend && npm run dev"

echo.
echo ===================================================
echo SYSTEM STARTUP INITIATED
echo ===================================================
echo Backend API:  http://localhost:8000/docs
echo Frontend UI:  http://localhost:3000
echo.
echo IMPORTANT:
echo 1. Keep the two black windows OPEN.
echo 2. If you see "Quota Exceeded" in the Backend window, check your OpenAI billing.
echo.
pause
