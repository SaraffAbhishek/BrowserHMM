@echo off
echo Setting up Python virtual environment...
python -m venv venv
call venv\Scripts\activate

echo Installing requirements...
pip install -r requirements.txt

echo Running the HMM tracking agent...
python app.py
