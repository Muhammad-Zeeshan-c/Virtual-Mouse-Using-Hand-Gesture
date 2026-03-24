@echo off
title AI Virtual Mouse - Launcher
color 0A

echo ============================================
echo    AI Virtual Mouse - One Click Launcher
echo ============================================
echo.

:: Store the project root directory
set "PROJECT_DIR=%~dp0"

:: --- Check Python ---
where py >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    exit /b 1
)
echo [OK] Python found.

:: --- Check Node/npm ---
where npm >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] npm is not installed or not in PATH.
    pause
    exit /b 1
)
echo [OK] npm found.

:: --- Check if hand_landmarker model exists ---
if not exist "%PROJECT_DIR%src\hand_landmarker.task" (
    echo.
    echo [INFO] Downloading hand_landmarker model...
    curl.exe -L https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task -o "%PROJECT_DIR%src\hand_landmarker.task"
    echo [OK] Model downloaded.
) else (
    echo [OK] Hand landmarker model found.
)

:: --- Install frontend dependencies if needed ---
if not exist "%PROJECT_DIR%frontend\node_modules" (
    echo [INFO] Installing frontend dependencies...
    cd /d "%PROJECT_DIR%frontend"
    call npm install
    cd /d "%PROJECT_DIR%"
)
echo [OK] Frontend dependencies ready.

echo.
echo ============================================
echo    Starting services...
echo ============================================
echo.

:: --- Start Frontend in a NEW terminal that stays open ---
echo [1/2] Starting Frontend...
start "Frontend - React Dashboard" cmd /k "cd /d "%PROJECT_DIR%frontend" && echo Starting React Dashboard... && npm run dev"

:: Wait 3 seconds for frontend to boot
echo Waiting 3 seconds for frontend...
timeout /t 3 /nobreak >nul

:: --- Start Backend in a NEW terminal that stays open ---
echo [2/2] Starting Backend...
start "Backend - Python Engine" cmd /k "cd /d "%PROJECT_DIR%src" && echo Starting AI Virtual Mouse... && py main.py"

echo.
echo ============================================
echo    BOTH SERVICES ARE NOW RUNNING!
echo ============================================
echo.
echo    Dashboard:  http://localhost:5173
echo    Backend:    http://127.0.0.1:8000
echo.
echo    Close the other two windows to stop.
echo    Press any key to close this launcher.
echo ============================================
pause >nul
