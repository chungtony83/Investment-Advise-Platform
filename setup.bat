@echo off
setlocal

echo Checking Python installation...

rem --- find a Python executable ---
set "PYEXE="
where python >nul 2>&1 && set "PYEXE=python"
if not "%PYEXE%"=="" goto :have_py
where py >nul 2>&1 && set "PYEXE=py -3"

:have_py
if "%PYEXE%"=="" (
  echo Python not found. Please install it (e.g., via pyenv-win) and try again.
  exit /b 1
)

echo Creating Python virtual environment...
%PYEXE% -m venv venv || (echo Failed to create virtual environment.& exit /b 1)

echo Activating virtual environment...
call "venv\Scripts\activate.bat" || (echo Failed to activate virtual environment.& exit /b 1)

echo Upgrading pip...
python -m pip install --upgrade pip || (echo Failed to upgrade pip.& exit /b 1)

if exist requirements.txt (
  echo Installing dependencies from requirements.txt...
  python -m pip install -r requirements.txt || (echo Failed to install dependencies.& exit /b 1)
) else (
  echo No requirements.txt found. Skipping dependency installation.
)

echo.
echo Setup complete! Virtual environment is ready.
echo To activate later:
echo   CMD:        call venv\Scripts\activate.bat
echo   PowerShell: .\venv\Scripts\Activate.ps1
echo To deactivate: deactivate

endlocal
