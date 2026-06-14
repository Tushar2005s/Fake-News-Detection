@echo off
REM Fake News Detection Streamlit App - Windows Launcher

echo.
echo ========================================
echo   Fake News Detection - Streamlit App
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from python.org
    pause
    exit /b 1
)

echo [1/2] Installing dependencies...
pip install -q pandas scikit-learn joblib streamlit
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed

echo.
echo [2/2] Starting Streamlit app...
echo.
echo ========================================
echo The app will open in your browser
echo URL: http://localhost:8501
echo Press Ctrl+C to stop the server
echo ========================================
echo.

streamlit run streamlit_app.py

pause
