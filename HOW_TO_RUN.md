# 🚀 Run App - Batch File Guide

## What is `run_app.bat`?

A Windows batch file that automatically:
- ✅ Checks if Python is installed
- ✅ Detects Python version
- ✅ Verifies all required files exist
- ✅ Installs missing dependencies
- ✅ Launches the Streamlit app
- ✅ Provides helpful error messages

## How to Use

### **Method 1: Double-Click (Easiest)** ⭐

1. Open File Explorer
2. Navigate to your project folder
3. **Double-click on `run_app.bat`**
4. A command window will open
5. The app will start automatically
6. Browser will open at `http://localhost:8501`

### **Method 2: Command Line**

Open PowerShell in the project folder and run:
```powershell
.\run_app.bat
```

Or:
```cmd
run_app.bat
```

## What Happens When You Run It

```
============================================
   FAKE NEWS DETECTION - STREAMLIT APP
============================================

[✓] Python 3.14.3 detected

[STEP 1] Checking/Installing Dependencies...

[✓] All dependencies installed successfully

[STEP 2] Launching Streamlit App...

============================================
   Starting Fake News Detection App
============================================

Local URL:    http://localhost:8501
Network URL:  http://127.0.0.1:8501

Press Ctrl+C to stop the server
============================================
```

## Features of the Batch File

### 1. **Python Detection**
- Checks if Python is installed
- Displays Python version
- Provides instructions if Python is missing

### 2. **Dependency Check**
- Verifies all required packages are installed
- Automatically installs missing packages:
  - streamlit
  - pandas
  - scikit-learn
  - joblib

### 3. **File Verification**
- Checks for `streamlit_app.py`
- Verifies model files exist:
  - `fake_news_model.pkl`
  - `vectorizer.pkl`
- Warns if optional files are missing

### 4. **Auto-Launch**
- Automatically launches the Streamlit app
- Displays local and network URLs
- Shows instructions for stopping the server

### 5. **Error Handling**
- Clear error messages if something goes wrong
- Helpful guidance on fixing issues
- Pauses before exiting so you can read messages

## Troubleshooting

### Error: "Python is not installed"
**Solution:** 
- Install Python 3.7+ from [python.org](https://www.python.org)
- During installation, **CHECK the "Add Python to PATH"** option
- Restart your computer

### Error: "streamlit_app.py not found"
**Solution:**
- Make sure you're running the batch file from the correct directory
- The batch file should be in the same folder as `streamlit_app.py`

### Error: Dependencies fail to install
**Solution:**
1. Open PowerShell as Administrator
2. Run: `pip install --upgrade pip`
3. Run: `pip install streamlit pandas scikit-learn joblib`
4. Try running the batch file again

### Port 8501 already in use
**Solution:**
- The app is already running on another terminal
- Either close the other instance or use a different port
- In the terminal, Ctrl+C to stop the server
- Wait 5 seconds and try again

## File Structure

Your project should have:
```
Real-time-fake-news-detection-main - Tushar/
├── run_app.bat              ← This file
├── streamlit_app.py         ← Main app (required)
├── fake_news_model.pkl      ← Trained model (required)
├── vectorizer.pkl           ← TF-IDF vectorizer (required)
├── fake_or_real_news.csv    ← Dataset (optional)
├── train_model.py           ← Training script (optional)
└── ... other files
```

## Quick Tips

✅ **Save the batch file location** in your favorites/bookmarks for quick access

✅ **Create a shortcut** - Right-click `run_app.bat` → Send to → Desktop (create shortcut)

✅ **Schedule it** - Windows Task Scheduler can run it automatically

✅ **Network access** - Use the "Network URL" to access from other devices on your network

## What Ports Are Used?

- **8501** - Streamlit web interface (default)
- If busy, you can change it by editing the batch file

## Stopping the App

**In the command window:**
- Press `Ctrl+C` once
- Type `Y` and press Enter
- The window will close

**Or just:**
- Close the command window directly

## Getting Help

If something goes wrong:

1. **Read the error message** - It usually tells you what's wrong
2. **Check requirements** - Make sure all required files exist
3. **Verify Python** - Run `python --version` in PowerShell
4. **Reinstall packages** - Run `pip install streamlit pandas scikit-learn joblib`
5. **Restart everything** - Close the terminal and try again

## Advanced Usage

### Custom Port
Edit the last line of the batch file to:
```batch
python -m streamlit run streamlit_app.py --server.port 8502
```

### Custom Settings
Add more Streamlit options:
```batch
python -m streamlit run streamlit_app.py --client.showErrorDetails=false
```

---

**Everything is set up and ready to go!** 🎉

Just double-click `run_app.bat` and enjoy your Fake News Detection app!
