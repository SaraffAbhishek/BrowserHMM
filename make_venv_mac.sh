#!/bin/bash

echo "🔧 Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "⬇️ Installing dependencies..."
pip install -r requirements.txt

echo "🚀 Running the HMM tracking agent..."
python app.py
