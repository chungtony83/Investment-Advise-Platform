@echo off
echo Setting up Python virtual environment...

python -m pip install --upgrade pip

REM Create virtual environment
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt

echo.
echo ✅ Setup complete! The virtual environment is ready.
echo To activate later, run:
echo venv\Scripts\activate
pause
