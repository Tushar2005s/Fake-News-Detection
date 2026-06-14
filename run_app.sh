#!/bin/bash

# Quick Start Script for Fake News Detection App (Linux/Mac)

echo ""
echo "========================================"
echo "    Fake News Detection - Quick Start"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.7+ from python.org"
    exit 1
fi

echo "[1/3] Checking/Installing dependencies..."
pip3 install -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo "✓ Dependencies installed"

echo ""
echo "[2/3] Training the model (if not already trained)..."
if [ -f "fake_news_model.pkl" ]; then
    echo "✓ Model already exists, skipping training"
else
    echo "Training new model..."
    python3 train_model.py
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to train model"
        echo "Make sure fake_or_real_news.csv exists"
        exit 1
    fi
    echo "✓ Model trained successfully"
fi

echo ""
echo "[3/3] Starting Streamlit app..."
echo ""
echo "========================================"
echo "The app will open in your browser"
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo ""

streamlit run streamlit_app.py
