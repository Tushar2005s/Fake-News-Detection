@echo off
REM ============================================
REM Fake News Detection - Streamlit App Launcher
REM ============================================

setlocal enabledelayedexpansion

REM Change to the script's directory
cd /d "%~dp0"

echo.
echo ============================================
echo    FAKE NEWS DETECTION - STREAMLIT APP
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python 3.7+ from: https://www.python.org
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [✓] Python !PYTHON_VERSION! detected
echo.

REM Check if model files exist
if not exist "fake_news_model.pkl" (
    echo [WARNING] Model file not found: fake_news_model.pkl
    echo [INFO] Please ensure the model files are in this directory
    echo.
)

if not exist "vectorizer.pkl" (
    echo [WARNING] Vectorizer file not found: vectorizer.pkl
    echo [INFO] Please ensure the vectorizer file is in this directory
    echo.
)

REM Check if dataset exists
if not exist "fake_or_real_news.csv" (
    echo [INFO] Dataset not found: fake_or_real_news.csv
    echo [INFO] This is optional - only needed for retraining the model
    echo.
)

REM Check if streamlit_app.py exists
if not exist "streamlit_app.py" (
    echo.
    echo [ERROR] streamlit_app.py not found in current directory!
    echo Current directory: %cd%
    echo.
    pause
    exit /b 1
)

echo [STEP 1] Checking/Installing Dependencies...
echo.

REM Try to import required packages
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo Installing streamlit...
    pip install -q streamlit
    if errorlevel 1 (
        echo [ERROR] Failed to install streamlit
        pause
        exit /b 1
    )
)

python -c "import pandas" >nul 2>&1
if errorlevel 1 (
    echo Installing pandas...
    pip install -q pandas
    if errorlevel 1 (
        echo [ERROR] Failed to install pandas
        pause
        exit /b 1
    )
)

python -c "import sklearn" >nul 2>&1
if errorlevel 1 (
    echo Installing scikit-learn...
    pip install -q scikit-learn
    if errorlevel 1 (
        echo [ERROR] Failed to install scikit-learn
        pause
        exit /b 1
    )
)

python -c "import joblib" >nul 2>&1
if errorlevel 1 (
    echo Installing joblib...
    pip install -q joblib
    if errorlevel 1 (
        echo [ERROR] Failed to install joblib
        pause
        exit /b 1
    )
)

echo [✓] All dependencies installed successfully
echo.

echo [STEP 2] Launching Streamlit App...
echo.
echo ============================================
echo    Starting Fake News Detection App
echo ============================================
echo.
echo Local URL:    http://localhost:8501
echo Network URL:  http://127.0.0.1:8501
echo.
echo Press Ctrl+C to stop the server
echo ============================================
echo.

REM Launch Streamlit app
python -m streamlit run streamlit_app.py

REM If app exits, show message
echo.
echo [INFO] Streamlit app has closed
echo.
pause
exit /b 0
